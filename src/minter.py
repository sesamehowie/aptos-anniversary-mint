from loguru import logger
from src.client import AptosClient
from data.config import COLLECTION_ID, MINTER_CONTRACT_ADDRESS
from aptos_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from aptos_sdk.bcs import Serializer
from src.decorators import retry

"""
payload = {
            "function": "0x96c192a4e3c529f0f6b3567f1281676012ce65ba4bb0a9b20b46dec4e371cccd::unmanaged_launchpad::mint",
            "type_arguments": [],
            "arguments": [
                {
                    "inner": "0xd42cd397c41a62eaf03e83ad0324ff6822178a3e40aa596c4b9930561d4753e5"
                },
                {"vec": ["1"]},
            ],
            "type": "entry_function_payload",
        }
"""


class Minter(AptosClient):
    def __init__(self, account_name, private_key, proxy=None) -> bool:
        super().__init__(private_key, proxy)

        self.account_name = account_name
        self.collection_id = COLLECTION_ID
        self.minter = MINTER_CONTRACT_ADDRESS
        self.fail_text = "Failed to mint Anniversary NFT"

    @retry
    def mint(self):
        logger.info(
            f"{self.account_name} | {self.address} | Minting Aptos 2 Year Anniversary NFT..."
        )

        try:
            payload = EntryFunction.natural(
                f"{self.minter}::unmanaged_launchpad",
                "mint",
                [
                    TransactionArgument(self.collection_id, Serializer.str),
                    TransactionArgument(1, Serializer.u64),
                ],
            )
            signed_transaction = self.create_bcs_signed_transaction(
                self.signer, TransactionPayload(payload)
            )
            tx = self.submit_bcs_transaction(signed_transaction)
            self.wait_for_transaction(tx)
            logger.success(f"{self.account_name} | {self.address} | Mint Successful!")
            return True
        except Exception as e:
            if "ERR_COIN_OUT_NUM_LESS_THAN_EXPECTED_MINIMUM" in str(e):
                logger.error(
                    f"{self.account_name} | {self.address} | {self.fail_text}: high loss_ratio"
                )
                return False
            elif "INSUFFICIENT_BALANCE" in str(e):
                logger.error(
                    f"{self.account_name} | {self.address} | {self.fail_text}: insufficient balance"
                )
                return False
            logger.error(
                f"{self.account_name} | {self.address} | {self.fail_text}: something went wrong: {e}"
            )
            return False
