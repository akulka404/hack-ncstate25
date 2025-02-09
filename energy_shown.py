from web3 import Web3
import json
import random

# Connect to Hardhat local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    print("Failed to connect to Hardhat node")
    exit()

print("Connected to Hardhat local blockchain")

# House wallet addresses and private keys (Hardhat test accounts)
houses = {
    "H1": {"address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266", "private_key": "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"},
    "H2": {"address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8", "private_key": "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"},
    "H3": {"address": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC", "private_key": "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"},
    "H4": {"address": "0x90F79bf6EB2c4f870365E785982E1f101E93b906", "private_key": "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6"},
    "H5": {"address": "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65", "private_key": "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a"},
}

# Load contract ABI from Hardhat artifacts
with open("/Users/ani/Downloads/hack-ncstate25/gridwise-blockchain/artifacts/contracts/EnergyTrading.sol/EnergyTrading.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Updated Contract Address (Replace with new one after redeployment)
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract = w3.eth.contract(address=contract_address, abi=abi)

print("Contract loaded successfully")

# Simulated energy data for houses
energy_data = {
    "H1": {"solar_output": round(random.uniform(3, 8), 2), "energy_needed": 0, "sell_price": round(random.uniform(0.08, 0.12), 4)},
    "H2": {"solar_output": round(random.uniform(2, 6), 2), "energy_needed": 0, "sell_price": round(random.uniform(0.08, 0.12), 4)},
    "H3": {"solar_output": 0, "energy_needed": round(random.uniform(2, 5), 2)},
    "H4": {"solar_output": 0, "energy_needed": round(random.uniform(1, 4), 2)},
    "H5": {"solar_output": 0, "energy_needed": round(random.uniform(3, 6), 2)},
}

# Track financial transactions (for full history)
transaction_log = {house: {"total_balance": 0.0, "transactions": []} for house in energy_data.keys()}
transaction_log["Main Grid"] = {"total_balance": 0.0, "transactions": []}  # Track grid revenue

# Determine the main grid price (slightly higher than the lowest seller price)
lowest_seller_price = min([data["sell_price"] for data in energy_data.values() if "sell_price" in data])
main_grid_price = round(lowest_seller_price * 1.15, 4)  # 15% higher than lowest seller price

def execute_trade(seller, buyer, energy_amount, price_per_kWh):
    total_price = round(energy_amount * price_per_kWh, 6)  # Total ETH cost

    print(f"\n🔹 Executing Trade:")
    print(f"   - {seller} selling {energy_amount:.2f} kWh to {buyer} at {price_per_kWh:.5f} ETH per kWh")
    print(f"   - Total Price: {total_price:.6f} ETH")

    # If seller is the grid, no blockchain transaction needed
    if seller == "Main Grid":
        print(f"⚡ {buyer} is buying {energy_amount:.2f} kWh from the **Main Grid** at {price_per_kWh:.5f} ETH per kWh.")
        transaction_log[buyer]["transactions"].append({
            "role": "Buyer", "seller": "Main Grid", "energy_bought": energy_amount,
            "price": total_price, "tx_hash": "Main Grid"
        })
        transaction_log["Main Grid"]["transactions"].append({
            "role": "Seller", "buyer": buyer, "energy_sold": energy_amount,
            "price": total_price, "tx_hash": "Main Grid"
        })
        transaction_log[buyer]["total_balance"] -= total_price
        transaction_log["Main Grid"]["total_balance"] += total_price
        return

    # Create blockchain transaction
    energy_amount_wei = int(energy_amount * 10**18)
    price_per_kWh_wei = int(price_per_kWh * 10**18)

    tx = contract.functions.createTrade(
        houses[buyer]["address"],
        energy_amount_wei,
        price_per_kWh_wei
    ).build_transaction({
        'from': houses[seller]["address"],
        'gas': 500000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': w3.eth.get_transaction_count(houses[seller]["address"])
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=houses[seller]["private_key"])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)

    print(f"✅ Trade Created! Tx Hash: {tx_hash.hex()}")

    # Update financial records
    transaction_log[seller]["transactions"].append({
        "role": "Seller", "buyer": buyer, "energy_sold": energy_amount,
        "price": total_price, "tx_hash": tx_hash.hex()
    })
    transaction_log[buyer]["transactions"].append({
        "role": "Buyer", "seller": seller, "energy_bought": energy_amount,
        "price": total_price, "tx_hash": tx_hash.hex()
    })

    transaction_log[seller]["total_balance"] += total_price
    transaction_log[buyer]["total_balance"] -= total_price

    # Update energy data
    energy_data[seller]["solar_output"] -= energy_amount
    energy_data[buyer]["energy_needed"] -= energy_amount

def optimal_energy_allocation():
    sellers = sorted(["H1", "H2"], key=lambda h: energy_data[h]["sell_price"])
    buyers = sorted(["H3", "H4", "H5"], key=lambda h: energy_data[h]["energy_needed"], reverse=True)

    for buyer in buyers:
        while energy_data[buyer]["energy_needed"] > 0:
            for seller in sellers:
                available = energy_data[seller]["solar_output"]
                if available <= 0:
                    continue

                trade_amount = min(energy_data[buyer]["energy_needed"], available)
                execute_trade(seller, buyer, trade_amount, energy_data[seller]["sell_price"])

                if energy_data[buyer]["energy_needed"] <= 0:
                    break  

    # Buy remaining energy from the main grid
    for buyer in buyers:
        if energy_data[buyer]["energy_needed"] > 0:
            execute_trade("Main Grid", buyer, energy_data[buyer]["energy_needed"], main_grid_price)
            energy_data[buyer]["energy_needed"] = 0  

# Run the simulation
optimal_energy_allocation()

# Print JSON output
print("\n📜 **Transaction Summary (JSON Output):**")
print(json.dumps(transaction_log, indent=4))
