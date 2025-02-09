import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from visualization_tool import fetch_from_mongo


def draw_transaction_graph(G, pos, seller, buyer, volume, price, total_cost):
    """Draw the original star graph and highlight the transaction with an arrow."""
    fig, ax = plt.subplots(figsize=(2, 2))  # Smaller figure size

    # Draw all nodes and edges
    nx.draw_networkx_nodes(
        G, pos, node_size=300, node_color="lightgray", edgecolors="black", linewidths=0.5, ax=ax
    )
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=6, font_color="black", ax=ax)

    # Highlight seller and buyer nodes
    nx.draw_networkx_nodes(
        G, pos, nodelist=[seller], node_size=300, node_color="red", edgecolors="black", linewidths=0.5, ax=ax
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=[buyer], node_size=300, node_color="green", edgecolors="black", linewidths=0.5, ax=ax
    )

    # Draw a directed arrow for the transaction
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(seller, buyer)],
        edge_color="blue",
        width=1.5,
        arrowstyle="->",
        arrowsize=10,
        ax=ax,
    )

    # Add transaction details as a title
    ax.set_title(
        f"Transaction:\nSeller: {seller} → Buyer: {buyer}\n"
        f"Volume: {volume} kWh | Price: ${price}/kWh | Total Cost: ${total_cost}",
        fontsize=6,
        color="black",
        loc="center",
        pad=10,
    )

    ax.axis("off")  # Remove axes for a clean look
    plt.tight_layout()  # Reduce white space around the graph
    return fig


def vizmagic_page():
    """Main visualization page logic."""
    st.title("Trade Visualization")

    # Fetch transactions from the database
    transactions = fetch_from_mongo()

    if transactions.empty:
        st.warning("No transactions found in the database.")
        return

    # Create the original star graph
    G = nx.Graph()
    nodes = ["H1", "H2", "H3", "H4", "H5"]
    G.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            G.add_edge(nodes[i], nodes[j])
    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    # State to track which transaction to display
    if "transaction_index" not in st.session_state:
        st.session_state.transaction_index = 0

    index = st.session_state.transaction_index

    if index < len(transactions):
        row = transactions.iloc[index]

        st.subheader(f"Transaction {index + 1}")

        # Display transaction details
        st.write(f"Seller: {row['Seller']} → Buyer: {row['Buyer']}")
        st.write(f"Volume: {round(row['Volume (kWh)'], 2)} kWh")
        st.write(f"Price: ${round(row['Price ($/kWh)'], 2)}/kWh")
        st.write(f"Total Cost: ${round(row['Total Cost ($)'], 2)}")

        # Draw the transaction graph
        fig = draw_transaction_graph(
            G,
            pos,
            row['Seller'],
            row['Buyer'],
            round(row['Volume (kWh)'], 2),
            round(row['Price ($/kWh)'], 2),
            round(row['Total Cost ($)'], 2),
        )
        st.pyplot(fig)

        # Navigation buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Previous Transaction") and index > 0:
                st.session_state.transaction_index -= 1
                st.rerun()

        with col2:
            if st.button("Next Transaction") and index < len(transactions) - 1:
                st.session_state.transaction_index += 1
                st.rerun()


# Run the app
if __name__ == "__main__":
    vizmagic_page()
