import ast
from collections import namedtuple
from copy import deepcopy
from typing import List, Set, Tuple, Union

from beancount.core.data import Posting, Transaction
from beancount.core.inventory import Inventory

import beancount_plugin_utils.metaset as metaset


PluginConfigError = namedtuple('PluginConfigError', 'source message entry')

def parse_config_string(config_string):
    """
    Args:
      config_string: A configuration string in JSON format given in source file.
    Returns:
      A dict of the configuration string.
    """
    try:
        if len(config_string) == 0:
            config_obj = {}
        else:
            config_obj = ast.literal_eval(config_string)
    except:
        raise RuntimeError('Invalid plugin configuration: "{}", skipping the plugin.'.format(config_string))

    if not isinstance(config_obj, dict):
        raise RuntimeError('Invalid plugin configuration: "{}": Must be a single dict, skipping the plugin.'.format(config_string))

    return config_obj
