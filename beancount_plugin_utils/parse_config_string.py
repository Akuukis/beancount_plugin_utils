import ast
from collections import namedtuple
from copy import deepcopy
from typing import List, Set, Tuple, Union

from beancount.core.data import Posting, Transaction, new_metadata
from beancount.core.inventory import Inventory

import beancount_plugin_utils.metaset as metaset


PluginUtilsConfigError = namedtuple('PluginUtilsConfigError', 'source message entry')

def parse_config_string(config_string):
    """
    Args:
      config_string: A configuration string in JSON format given in source file.

    Example:
        # 1. Define a config structure first. See `class Config` above and adjust it as needed.

        # 2. Parse config string. Just copy/paste this block.
        config_dict, config_error = parse_config_string(config_dict_string)
        if config_error:
            return entries, [config_error]

        # 3. Apply transforms (e.g. from `str` to `date`) where needed.
        # Wrap each transform separately in a try-except, and return PluginUtilsConfigError with a nice error message.
        try:
            if "open_date" in config_dict:
                config_dict['open_date'] = None if config_dict['open_date'] is None else date.fromisoformat(config_dict['open_date'])
        except:
            return entries, [PluginUtilsConfigError(
                new_metadata('<example_plugin>', 0),
                'Plugin "share" received bad "open_date" value - it must be a valid date, formatted in UTC (e.g. "2000-01-01").',
                None,
            )]

        # 4. Create config itself. Just copy/paste this block. Done!
        config = Config(**config_dict)

    Returns:
        None or a dict of the configuration string.
        None or PluginUtilsConfigError.
    """
    try:
        if len(config_string) == 0:
            config_obj = {}
        else:
            config_obj = ast.literal_eval(config_string)
    except:
        return {}, PluginUtilsConfigError(
            new_metadata('<example_plugin>', 0),
            'Invalid plugin configuration, skipping the plugin. The config: {}'.format(config_string),
            None,
        )

    if not isinstance(config_obj, dict):
        return {}, PluginUtilsConfigError(
            new_metadata('<example_plugin>', 0),
            'Invalid plugin configuration: Must be a single dict, skipping the plugin. The config: {}'.format(config_string),
            None,
        )

    return config_obj, None
