from collections import namedtuple
from beancount.parser import printer

BeancountErrorNamedTuple = namedtuple("BeancountError", "source message entry")

class BeancountError(RuntimeError):
    def __init__(self, source, message, entry, named_tuple = BeancountErrorNamedTuple):
        self.source = source
        self.message = message
        self.entry = entry
        self.named_tuple = named_tuple

    def __str__(self):
        return printer.format_error(self.to_named_tuple())

    def to_named_tuple(self):
        return self.named_tuple(self.source, self.message, self.entry)
