# uncomment imports if you wanna use the balance checker snippet below in main()

# import os
import asyncio
# from pathlib import Path
from random import shuffle, randint
from itertools import cycle
from src.minter import Minter
from src.account import AptosAccount
# from src.utils import random_sleep, write_csv
from data.config import PRIVATE_KEYS, PROXIES # , CWD
from data.settings import SHUFFLE_KEYS, SHUFFLE_PROXIES


proxies = PROXIES
keys = PRIVATE_KEYS


if SHUFFLE_KEYS:
    shuffle(keys)

if SHUFFLE_PROXIES:
    shuffle(proxies)

proxy_cycle = cycle(proxies)


async def get_balance(account_name, private_key, proxy) -> list:
    account = AptosAccount(private_key=private_key)
    balance = round(await account.get_balance() / 10**8, 4)
    return [str(account_name), account.wallet_address, balance]


async def run_account(account_name: str | int, private_key: str, proxy: str) -> bool:
    minter = Minter(account_name=account_name, private_key=private_key, proxy=proxy)
    res = await minter.mint_nft()
    await asyncio.sleep(randint(20, 25))
    return res


async def main() -> None:
    i = 1
    # # BALANCE CHECKER SNIPPET
    # results = []

    # for key in keys:
    #     proxy = next(proxy_cycle)
    #     account_name = str(i)

    #     task = asyncio.create_task(
    #         get_balance(account_name=account_name, private_key=key, proxy=proxy)
    #     )
    #     result = await task
    #     results.append(result)

    # if results:
    #     write_csv(
    #         file_name=os.path.join(CWD, "data/results/results.csv"),
    #         data=results,
    #         header=["account_num", "wallet_address", "APT balance"],
    #     )

    for key in keys:
        proxy = next(proxy_cycle)
        account_name = str(i)
        task = asyncio.create_task(
            run_account(account_name=account_name, private_key=key, proxy=proxy)
        )
        await task
        await asyncio.sleep(randint(10, 15))
        i += 1


if __name__ == "__main__":
    asyncio.run(main())
