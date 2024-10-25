import os
from src.utils import read_txt
from pathlib import Path

CWD = Path(os.getcwd())

COLLECTION_ID: str = (
    "0xd42cd397c41a62eaf03e83ad0324ff6822178a3e40aa596c4b9930561d4753e5"
)
MINTER_CONTRACT_ADDRESS: str = (
    "0x96c192a4e3c529f0f6b3567f1281676012ce65ba4bb0a9b20b46dec4e371cccd"
)
TX_TIMEOUT: int = 10

APTOS_EXPLORER_URL: str = "https://explorer.aptoslabs.com"

PRIVATE_KEYS = read_txt(os.path.join(CWD, Path("data/inputs/private_keys.txt")))

PROXIES = read_txt(os.path.join(CWD, Path("data/inputs/proxies.txt")))

RPC = "https://rpc.ankr.com/http/aptos/v1"
