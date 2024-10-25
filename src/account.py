from loguru import logger
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient
from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from aptos_sdk.transactions import SignedTransaction, RawTransaction

from data.config import RPC


class AptosAccount:
    def __init__(self, private_key: str):
        self.rest_client = RestClient(RPC)
        self.account = Account.load_key(private_key)
        self.wallet_address = self.account.address()

    async def get_balance(self) -> int:
        res = await self.rest_client.account_balance(self.wallet_address)
        logger.info(
            f"{self.wallet_address} | got amount: {res}, in APT: {round(res / 10 ** 8, 4)}"
        )
        return res

    async def sign_transaction(self, raw_transaction: RawTransaction) -> str:
        signature = self.account.sign(raw_transaction.keyed())
        authenticator = Authenticator(
            Ed25519Authenticator(self.account.public_key(), signature)
        )
        signed_transaction = SignedTransaction(raw_transaction, authenticator)
        tx_hash = await self.rest_client.submit_bcs_transaction(signed_transaction)
        return tx_hash
