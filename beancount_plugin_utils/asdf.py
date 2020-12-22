from typing import NamedTuple, Set, List, Union, Tuple
from beancount.core.number import D, Decimal, ONE
from datetime import date, datetime

# https://docs.python.org/3/library/collections.html#collections.namedtuple

class Config(NamedTuple):
    mark_name: str
    meta_name: Union[str, None]
    account_debtors: str
    account_creditors: str
    quantize: Decimal
    open_date: Union[date, None]

config = Config(
    "share",
    "shared",
    "Assets:Debtors",
    "Liabilities:Creditors",
    D(str(0.01)),
    date.fromisoformat('2020-01-01'),
)

print(Config.)
