import time
import random
from decimal import Decimal
from pathlib import Path
from loguru import logger
from typing import Optional, Union
from data.settings import SLEEP_BETWEEN_ACCOUNTS


def read_txt(filename: str | Path) -> list:
    with open(filename, "r") as file:
        data = file.read().splitlines()
    return data


def get_explorer_hash_link(tx_hash: str):
    try:
        return f"https://explorer.aptoslabs.com/txn/{tx_hash}?network=mainnet"
    except Exception as e:
        logger.error(f"Ge" f"t explorer hash link error: {str(e)}")


def randfloat(
    from_: Union[int, float, str],
    to_: Union[int, float, str],
    step: Optional[Union[int, float, str]] = None,
) -> float:
    from_ = Decimal(str(from_))
    to_ = Decimal(str(to_))
    if not step:
        step = 1 / 10 ** (min(from_.as_tuple().exponent, to_.as_tuple().exponent) * -1)

    step = Decimal(str(step))
    rand_int = Decimal(str(random.randint(0, int((to_ - from_) / step))))
    return float(rand_int * step + from_)


def prepare_address_for_aptoscan_api(address: str):
    if address.startswith("0x"):
        address = address[2:]
    result_address = "0x"

    beginning_word = True
    for ch in address:
        if beginning_word:
            if ch != "0":
                beginning_word = False
            else:
                continue
        result_address += ch
    return result_address


def random_sleep() -> None:
    rand_t = random.randint(*SLEEP_BETWEEN_ACCOUNTS)
    logger.debug(f"Sleeping for {rand_t} seconds...")
    time.sleep(rand_t)
