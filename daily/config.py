""" Configuration related functions.
"""

import configparser
import os
from pathlib import Path


home = Path.home()

default_conf = '/etc/daily/default.ini'
user_confdir = f'{home}/.config/daily'
user_conf = f'{user_confdir}/daily.ini'


default = f"""\
[default]
# Path to journal
journal = {home}/.local/share/daily

# Store entries as md or rst
entry_format = rst
"""


def get_defaults():
    """ Default values for items that should be in a config file.

    These values will be overuled by existing config entries. Useful in
    the event a config file is missing an entry.

    Returns:
        A dictionary that contains all expected entries for a
        configuration file.
    """
    return {
        'journal': f'journal = {home}/.local/share/daily',
        'entry_format': 'rst',
    }


def do_first_time_setup():
    """ Copy default.ini to user conf path.
    """
    try:
        os.makedirs(user_confdir)
    except FileExistsError:
        pass

    with open(user_conf, 'w') as f:
        f.write(default)

    os.makedirs(f'{home}/.local/share/daily', exist_ok=True)


def add_config_args(args, config=None):
    """ Add params from a config file to an ArgumentParser.

    Parameters are only copied if not already set in the
    ArgumentParser.

    Args:
        args: ArgumentParser instance.
        config: Path to config file.

    Returns:
        namedtuple containing config parameters overridden by command
        line arguments.

    Raises:
        FileNotFoundError: Provided config file doesn't exist.
        KeyError: Configuration file has no default section (or no sections).
    """
    config = user_conf if not config else config

    if not os.path.exists(config):
        raise FileNotFoundError('Config {} does not exist.'.format(config))

    cp = configparser.ConfigParser()

    try:
        cp.read(config)
    except Exception as e:
        raise KeyError('Config "{}" is invalid. {}.'.format(config, e))

    if 'default' not in cp:
        raise KeyError('Config {} has no "default" section.'.format(config))

    d = get_defaults()
    d.update(cp['default'])

    # copy vals into args if not already in args.
    for key, val in d.items():
        try:
            if not getattr(args, key):
                setattr(args, key, val)
        except AttributeError:
            setattr(args, key, val)

    return args
