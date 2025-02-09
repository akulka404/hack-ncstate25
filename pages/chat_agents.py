import streamlit as st
import requests
import json
import time

H1 = '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'
H2 = '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'
H3 = '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'
H4 = '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'
H5 = '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'

import streamlit as st
import requests
import json
import time

# Central Regulatory Rate (shared among all houses)
CENTRAL_REGULATORY_RATE = 0.12  # Example: $0.12 per kWh

# Houses with their buying/selling preferences
houses = {
    "H1": {"role": "sell", "lowest_selling_price": 0.10, "power_available_kWh": 50, "current_deal": None},
    "H2": {"role": "buy", "highest_buying_price": 0.15, "power_needed_kWh": 30, "current_deal": None},
    "H3": {"role": "sell", "lowest_selling_price": 0.11, "power_available_kWh": 40, "current_deal": None},
    "H4": {"role": "buy", "highest_buying_price": 0.13, "power_needed_kWh": 20, "current_deal": None},
    "H5": {"role": "sell", "lowest_selling_price": 0.09, "power_available_kWh": 25, "current_deal": None},
}

# Attach central regulatory rate to all houses
for house in houses:
    houses[house]["central_regulatory_rate"] = CENTRAL_REGULATORY_RATE

# Agent Configurations (Each house is an AI agent)
AGENTS = [
    {"name": "H1", "api_key": H1},
    {"name": "H2", "api_key": H2},
    {"name": "H3", "api_key": H3},
    {"name": "H4", "api_key": H4},
    {"name": "H5", "api_key": H5},
]

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def get_response_from_agent(agent, message, previous_agent):
    """
    Sends a negotiation message to an AI agent and retrieves its response.
    """
    house_data = houses[agent["name"]]  # Get house details for this agent

    # Construct prompt with house's role and market conditions
    prompt = f"""
    You are house {agent['name']} in a smart energy trading system.
    Your role: {house_data['role']}
    {"Lowest selling price: $" + str(house_data['lowest_selling_price']) + "/kWh" if house_data['role'] == "sell" else ""}
    {"Highest buying price: $" + str(house_data['highest_buying_price']) + "/kWh" if house_data['role'] == "buy" else ""}
    {"Power available: " + str(house_data['power_available_kWh']) + " kWh" if house_data['role'] == "sell" else ""}
    {"Power needed: " + str(house_data['power_needed_kWh']) + " kWh" if house_data['role'] == "buy" else ""}
    Central regulatory rate: ${CENTRAL_REGULATORY_RATE}/kWh.

    Negotiate with other houses but do NOT make a deal that goes against your best interest.
    If a fair deal is NOT possible, say you back out.

    Your last message was from {previous_agent}: "{message}"

    Reply with a **short response** (max 2 sentences) and **use emojis**. 
    """

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
    }

    headers = {
        "Authorization": f"Bearer {agent['api_key']}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


def make_deal(seller, buyer, price_per_kWh, power_transferred_kWh):
    """
    Handles a successful deal between a seller and a buyer.
    Updates power availability and records the transaction.
    """
    houses[seller]["power_available_kWh"] -= power_transferred_kWh
    houses[buyer]["power_needed_kWh"] -= power_transferred_kWh

    deal = {
        "seller": seller,
        "buyer": buyer,
        "price_per_kWh": price_per_kWh,
        "power_transferred_kWh": power_transferred_kWh,
        "status": "Completed ✅"
    }

    houses[seller]["current_deal"] = deal
    houses[buyer]["current_deal"] = deal

    return deal


def chat_between_agents():
    """
    Simulates negotiation between 5 AI-powered houses until a deal is reached.
    Each response prints immediately in the UI.
    """
    st.title("🏡 AI Energy Market - House Negotiation")
    st.write("Watch 5 AI agents negotiate energy deals!")

    # Initialize session state for tracking conversation
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "chat_finished" not in st.session_state:
        st.session_state.chat_finished = False

    # Start the negotiation process
    if st.button("Start Negotiation") and not st.session_state.chat_finished:
        initial_message = "Who wants to trade power? Please make an offer. ⚡"
        st.session_state.conversation.append({"from": "Market", "to": "All", "message": initial_message})

        next_message = initial_message
        previous_agent = "Market"
        deal_reached = False
        round_counter = 0

        while not deal_reached:
            sender = AGENTS[round_counter % len(AGENTS)]  # Cycle through agents
            receiver = AGENTS[(round_counter + 1) % len(AGENTS)]  # Next agent in line

            response = get_response_from_agent(sender, next_message, previous_agent)

            # Format message in UI as "🏡 H1 ➝ H2: Message"
            formatted_message = f"🏡 {sender['name']} ➝ {receiver['name']}: {response}"
            st.session_state.conversation.append({"from": sender['name'], "to": receiver['name'], "message": response})
            st.write(formatted_message)
            time.sleep(1)  # Delay for realism

            # Check if a deal is reached
            if "deal confirmed" in response.lower() or "agreement reached" in response.lower():
                deal = make_deal(sender['name'], receiver['name'], houses[sender['name']]["lowest_selling_price"], 30)
                deal_reached = True
                st.success(f"✅ **Deal finalized!** {deal['seller']} sells {deal['power_transferred_kWh']} kWh to {deal['buyer']} at ${deal['price_per_kWh']}/kWh 🔥")
                break
            elif "back out" in response.lower():
                st.warning(f"🚫 {sender['name']} decided to back out. No deal made.")
                deal_reached = True
                break

            next_message = response
            previous_agent = sender['name']
            round_counter += 1

        st.session_state.chat_finished = True  # Stop further conversations

    # Display conversation log
    st.write("### 📝 Conversation Log")
    for entry in st.session_state.conversation:
        st.markdown(f"**🏡 {entry['from']} ➝ {entry['to']}:** {entry['message']}")

    # Reset conversation
    if st.session_state.chat_finished:
        if st.button("Restart Negotiation"):
            st.session_state.conversation = []
            st.session_state.chat_finished = False
            st.experimental_rerun()
