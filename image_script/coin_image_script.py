import os
import shutil

# Define the folder paths
source_folder = r"C:\Users\William\Downloads\png"  # Path to the source folder
destination_folder = r"C:\Users\William\Downloads\selected_coins"  # Path to the new folder

# List of coins to include
coins = [
    "btc", "eth", "ltc", "xrp", "bch", "usdc", "xmr", "xlm",
    "usdt", "qcad", "doge", "link", "matic", "uni", "comp", "aave", "dai",
    "sushi", "snx", "crv", "dot", "yfi", "mkr", "paxg", "ada", "bat", "enj",
    "axs", "dash", "eos", "bal", "knc", "zrx", "sand", "grt", "qnt", "etc",
    "ethw", "1inch", "chz", "chr", "super", "elf", "omg", "ftm", "mana",
    "sol", "algo", "lunc", "ust", "zec", "xtz", "amp", "ren", "uma", "shib",
    "lrc", "ankr", "hbar", "egld", "avax", "one", "gala", "alice", "atom",
    "dydx", "celo", "storj", "skl", "ctsi", "band", "ens", "rndr", "mask",
    "ape"
]

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Copy the selected coin images to the new folder
for coin in coins:
    source_file = os.path.join(source_folder, f"{coin.lower()}.png")
    if os.path.isfile(source_file):
        shutil.copy(source_file, destination_folder)
        print(f"Copied {coin}.png to {destination_folder}")
    else:
        print(f"{coin}.png not found in {source_folder}")

print("Finished copying selected coin images.")
