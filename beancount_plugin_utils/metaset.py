"""
Abstraction on top of beancount's meta `dict` to operate on set of values per single key. `None` is treated as empty dict.

Implements `set` operations, but immutable: `add`, `remove`, `discard`, `clear`

Implements new methods:
- `set` - overwrites with a new set.
- `get` - retrieves a set of values from (meta or {}).
- `has` - boolean whenever `get` would retrieve something.
- `reset` - tidy up suffixes.

Under the hood, each value is saved in a seperate key with unique suffix of digits.
Order not guaranteed.
"""

from typing import List, Set, Union, Tuple
from copy import deepcopy

from beancount.core.data import Transaction, Posting, Meta
from beancount.core.inventory import Inventory

datatype_set = set
DIGITS_SET = datatype_set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])


def contains_key(key: str, meta: str):
    """
    Determines whenever given meta is a mark, which may or may not be suffixed with numbers.

    Truthy meta examples for key "share":
    - share
    - share0
    - share900

    Falsey meta examples for key "share":
    - asdf
    - 42share
    - share42asdf

    Args:
        key [str]: the key.
        meta [str]: the meta.
    Return:
        Bool
    """
    if key is meta:
        return True

    if meta[0 : len(key)] == key and datatype_set(meta[len(key) :]) <= DIGITS_SET:
        return True

    return False


def get(meta: Union[Meta, None], key: str) -> Set[str]:
    return [v for k, v in (meta or {}).items() if contains_key(key, k)]


def has(meta: Union[Meta, None], key: str) -> bool:
    return len(get(meta or {}, key)) > 0


def add(meta: Union[Meta, None], key: str, value: str) -> Meta:
    copy = deepcopy(meta or {})
    safe_key: str

    if not (key in (meta or {})):
        safe_key = key
    else:
        suffix: int = 900 + len([k for k in (meta or {}) if contains_key(key, k)])
        safe_key = key + str(suffix)

    copy[safe_key] = value
    return copy


def discard(meta: Union[Meta, None], key: str) -> Meta:
    copy = deepcopy(meta or {})

    if key in (meta or {}):
        del copy[key]

    return copy


## Not used for now. Disabled to not pollute coverage report.
# def remove(meta: Union[Meta, None], key: str) -> Meta:
#     copy = deepcopy(meta or {})

#     del copy[key]

#     return copy


def clear(meta: Union[Meta, None], key: str) -> Meta:
    copy = deepcopy(meta or {})

    for metakey in [k for k, _ in (meta or {}).items() if contains_key(key, k)]:
        del copy[metakey]

    return copy


# Not used for now. Disabled to not pollute coverage report.
def set(meta: Union[Meta, None], key: str, new_set: Set[str]) -> Meta:
    copy = clear(meta or {}, key)

    for elem in new_set:
        copy = add(copy, key, elem)

    return copy


## Not used for now. Disabled to not pollute coverage report.
# def reset(meta: Union[Meta, None], key: str) -> Meta:
#     elements = get(meta or {}, key)

#     return set(meta or {}, key, elements)
