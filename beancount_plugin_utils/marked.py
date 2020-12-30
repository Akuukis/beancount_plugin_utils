from typing import List, Set, Union
from copy import deepcopy
from collections import namedtuple

from beancount.core.data import Transaction, Posting, new_metadata

import beancount_plugin_utils.metaset as metaset
from beancount_plugin_utils.BeancountError import BeancountError


MARK_SEPERATOR = "-"

PluginUtilsMarkedError = namedtuple('PluginUtilsMarkedError', 'source message entry')


def normalize_transaction(
    mark_name: str,
    tx: Transaction,
    account_types: Union[Set[str], bool] = False,
):
    """
    Move marks in tags with name `mark_name` into meta, if any, and merge with marks in meta in a way of metaset.
    Then, if `account_types` are provided, move marks into postings with the given account types or error if there's none such posting.

    Example:

        try:
            tx, is_marked = marked.normalize_transaction(config.mark_name, entry, ("Income", "Expenses"))
        except BeancountError as e:
            new_entries.append(entry)
            errors.append(e.to_named_tuple())
            continue

        for posting, orig_posting in zip(tx, orig_tx):
            marks = metaset.get(posting)
            # Do your thing.

    Args:
        txs [Transaction]: transaction instances.
        mark_name [str]: the mark name.
        account_types [Set[str], False]: set of account types that must be considered, defaults to False.

    Returns:
        new Transaction instance with normalized marks.
        boolean of whenever mark was used in this transaction.

    Raises:
        BeancountError.
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


    is_used = False
    if metaset.has(copy.meta, mark_name):
        is_used = True

    for posting in copy.postings:
        if metaset.has(posting.meta, mark_name):
            is_used = True
            if not account_types:
                raise BeancountError(
                    new_metadata(posting.meta["filename"], posting.meta["lineno"]),
                    'Mark "{}" can be only applied to transactions, not postings: "{}".'.format(mark_name, posting.account),
                    tx,
                    PluginUtilsMarkedError,
                )
            if not (posting.account.split(":")[0] in account_types):
                raise BeancountError(
                    new_metadata(posting.meta["filename"], posting.meta["lineno"]),
                    'Mark "{}" can be only applied to posting with account types of: {}'.format(mark_name, account_types),
                    tx,
                    PluginUtilsMarkedError,
                )


    if not account_types:
        return copy, is_used

    if not is_used:
        return copy, False

    is_applied = False
    postings = []
    default_marks = metaset.get(copy.meta, mark_name)
    copy = copy._replace(meta=metaset.clear(copy.meta, mark_name))

    for posting in copy.postings:
        marks = metaset.get(posting.meta, mark_name)

        if len(marks) > 0:
            postings.append(posting)
            is_applied = True
        elif len(default_marks) > 0 and (posting.account.split(":")[0] in account_types):
            postings.append(posting._replace(meta=metaset.set(posting.meta, mark_name, default_marks)))
            is_applied = True
        else:
            postings.append(posting)


    print(is_used)
    print(postings)

    if not is_applied:
        raise BeancountError(
            new_metadata(tx.meta["filename"], tx.meta["lineno"]),
            'Mark "{}" on a transaction has no effect because transaction does not have postings with account types of: {}'.format(mark_name, account_types),
            tx,
            PluginUtilsMarkedError,
        )

    copy = copy._replace(
        postings=postings
    )

    return copy, True
