from time import time
from asyncio import sleep
import random
from src.account import AptosAccount
from aptos_sdk.transactions import (
    TransactionPayload,
    EntryFunction,
    TransactionArgument,
    RawTransaction,
)
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from loguru import logger
from data.settings import MINT_QUANTITY


class Minter(AptosAccount):
    def __init__(self, account_name: str | int, private_key: str, proxy: str):
        super().__init__(private_key)
        self.account_name = account_name
        self.private_key = private_key
        self.proxy = proxy

    def __str__(self) -> str:
        return f"[{self.wallet_address}] | Minting NFT..."

    async def mint_nft(self) -> None:
        balance = await self.get_balance()
        if balance <= 660000:
            logger.warning(
                f"[{self.wallet_address}] | APT balance is not enough for the transaction fee, skipping..."
            )
            return [self.account_name, self.wallet_address, "Not Minted"]

        if isinstance(MINT_QUANTITY, list):
            quantity = random.randint(*MINT_QUANTITY)
        else:
            quantity = MINT_QUANTITY
        try:
            payload = self._get_payload(quantity)
            raw_transaction = RawTransaction(
                sender=self.wallet_address,
                sequence_number=await self.rest_client.account_sequence_number(
                    self.wallet_address
                ),
                payload=payload,
                max_gas_amount=6000,
                gas_unit_price=110,
                expiration_timestamps_secs=int(time()) + 600,
                chain_id=await self.rest_client.chain_id(),
            )
            tx_hash = await self.sign_transaction(raw_transaction)
            await sleep(2)
            await self.rest_client.wait_for_transaction(tx_hash)
            logger.success(
                f"[{self.wallet_address}] | Successfully minted {quantity}"
                f" NFTs: https://explorer.aptoslabs.com/txn/{tx_hash}"
            )
            return [self.account_name, self.wallet_address, "Mint Successful"]
        except Exception as e:
            if "The mint stage max per user balance is insufficient." in str(e):
                logger.warning(
                    f"[{self.wallet_address}] - Already minted more than allowed"
                )
                return True

    @staticmethod
    def _get_payload(quantity: int) -> TransactionPayload:
        return TransactionPayload(
            EntryFunction.natural(
                module="0x96c192a4e3c529f0f6b3567f1281676012ce65ba4bb0a9b20b46dec4e371cccd::unmanaged_launchpad",
                function="mint",
                ty_args=[],
                args=[
                    TransactionArgument(
                        AccountAddress.from_str(
                            "0xd42cd397c41a62eaf03e83ad0324ff6822178a3e40aa596c4b9930561d4753e5"
                        ),
                        Serializer.struct,
                    ),
                    TransactionArgument(
                        [quantity],
                        Serializer.sequence_serializer(value_encoder=Serializer.u64),
                    ),
                ],
            )
        )
