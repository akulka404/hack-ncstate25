from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Get latest block number
latest_block = w3.eth.block_number

# Loop through last 10 blocks and print transactions
for block_num in range(latest_block - 10, latest_block + 1):
    block = w3.eth.get_block(block_num, full_transactions=True)
    print(f"\n🔹 Block {block_num}: {len(block.transactions)} Transactions")
    for tx in block.transactions:
        print(f"   Tx Hash: {tx.hash.hex()}")
        print(f"   From: {tx['from']}")
        print(f"   To: {tx['to']}")
        print(f"   Value: {w3.from_wei(tx['value'], 'ether')} ETH")
        print(f"   Gas: {tx['gas']} | Gas Price: {w3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
