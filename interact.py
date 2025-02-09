from web3 import Web3
import json

# Connect to Hardhat local blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    print("Failed to connect to Hardhat node")
    exit()

print("Connected to Hardhat local blockchain")

# Set addresses
seller = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
buyer = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

# Set private keys (DO NOT USE ON MAINNET)
seller_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
buyer_private_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

# Load contract ABI
with open("/Users/ani/Downloads/hack-ncstate25/gridwise-blockchain/artifacts/contracts/EnergyTrading.sol/EnergyTrading.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]

# Deployed contract address
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract = w3.eth.contract(address=contract_address, abi=abi)

print("Contract loaded successfully")

# Get trade count
print(f"Total Trades: {contract.functions.tradeCount().call()}")

# Create a trade
tx = contract.functions.createTrade(buyer, 5, w3.to_wei(0.12, 'ether')).build_transaction({
    'from': seller,
    'gas': 500000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': w3.eth.get_transaction_count(seller)
})

# Sign and send the transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key=seller_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # ✅ Fixed here
w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Trade Created! Transaction Hash: {tx_hash.hex()}")

# Verify trade exists
trade = contract.functions.getTrade(0).call()
print("Trade Details:", trade)

# Buyer completes the trade
tx = contract.functions.completeTrade(0).build_transaction({
    'from': buyer,
    'value': w3.to_wei(0.6, 'ether'),
    'gas': 500000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': w3.eth.get_transaction_count(buyer)
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=buyer_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # ✅ Fixed here
w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Trade Completed! Transaction Hash: {tx_hash.hex()}")

# Verify completion
trade = contract.functions.getTrade(0).call()
print("Updated Trade Details:", trade)
