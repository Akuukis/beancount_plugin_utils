from typing import List, Set
from copy import deepcopy

from beancount.core.data import Transaction, Posting

import beancount_plugin_utils.metaset as metaset


MARK_SEPERATOR = "-"


def normalize_transaction(tx: Transaction, mark_name: str):
    """
    Move marks in tags with name `mark_name` into meta, if any, and merge with marks in meta in a way of metaset.

    Args:
        txs [Transaction]: transaction instances.
        mark_name [str]: the mark name.

    Return:
        new Transaction instance with normalized marks.
    """
    copy = deepcopy(tx)

    for tag in copy.tags:
        if (
            tag == mark_name
            or tag[0 : len(mark_name + MARK_SEPERATOR)] == mark_name + MARK_SEPERATOR
        ):
            copy = copy._replace(
                tags=copy.tags.difference([tag]),
                meta=metaset.add(
                    copy.meta, mark_name, tag[len(mark_name + MARK_SEPERATOR) :] or ""
                ),
            )

    return copy


DEFAULT_APPLICABLE_ACCOUNT_TYPES = set(
    ["Income", "Expenses", "Assets", "Liabilities", "Equity"]
)


def resolve_postings(
    tx: Transaction,
    mark_name: str,
    applicable_account_types: Set[str] = DEFAULT_APPLICABLE_ACCOUNT_TYPES,
    allow_posting_level_mark: bool = True,
):
    """
    Iterates over postings of the transaction, returning most specific mark value for applicable account types.

    Args:
        tx [Transaction]: transaction instance.
        mark_name [str]: the mark.
        applicable_account_types [Set[str]]: set of account types that must be considered, defaults to all five.
        allow_posting_level_mark [bool]: set to False if posting-level marks should raise error instead.
    Yields:
        list of mark values or None.
        posting.
        original posting.
        original transaction.
    """
    copy = deepcopy(tx)

    default_marks = metaset.get(tx.meta, mark_name)
    copy = copy._replace(meta=metaset.clear(tx.meta, mark_name))

    for _posting in copy.postings:
        marks = metaset.get(_posting.meta, mark_name)
        posting = _posting._replace(meta=metaset.clear(_posting.meta, mark_name))

        if len(marks) > 0:
            yield marks, posting, _posting, copy
        elif len(default_marks) > 0:
            if posting.account.split(":")[0] not in applicable_account_types:
                yield None, posting, _posting, copy
            else:
                yield default_marks, posting, _posting, copy
        else:
            yield None, posting, _posting, copy
