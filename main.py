from random import shuffle
from itertools import cycle
from src.minter import Minter
from src.utils import random_sleep
from data.config import PRIVATE_KEYS, PROXIES
from data.settings import SHUFFLE_KEYS, SHUFFLE_PROXIES


proxies = PROXIES
keys = PRIVATE_KEYS


if SHUFFLE_KEYS:
    shuffle(keys)

if SHUFFLE_PROXIES:
    shuffle(proxies)

proxy_cycle = cycle(proxies)


def run_account(account_name: str | int, private_key: str, proxy: str) -> bool:
    minter = Minter(account_name=account_name, private_key=private_key, proxy=proxy)
    return minter.mint()


def main() -> None:
    i = 1

    for key in keys:
        proxy = next(proxy_cycle)
        account_name = str(i)
        
        run_account(account_name=account_name, private_key=key, proxy=proxy)
        random_sleep()


        