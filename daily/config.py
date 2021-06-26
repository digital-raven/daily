""" Configuration related functions.
"""

import configparser
import os
from pathlib import Path


default_conf = '/etc/daily/default.ini'
user_confdir = '{}/.config/daily'.format(Path.home())
user_conf = '{}/daily.ini'.format(user_confdir)


def get_defaults():
    """ Default values for items that should be in a config file.

    These values will be overuled by existing config entries. Useful in
    the event a config file is missing an entry.

    Returns:
        A dictionary that contains all expected entries for a
        configuration file.
    """
    return {
        'journal': './journal.json',
    }


def do_first_time_setup():
    """ Copy default.ini to user conf path.
    """

    # use these vals to create user config if not present in system defaults.
    default_vals = get_defaults()
    default_vals['journal'] = '{}/.local/share/daily/journal.json'.format(Path.home())

    cp = configparser.ConfigParser()

    # create empty string as conf if system default does not exist.
    if os.path.exists(default_conf):
        cp.read(default_conf)
    else:
        cp.read_string('[default]')

    # substitute hardcoded defaults for any absent values.
    for key in default_vals:
        if key not in cp['default'] or not cp['default'][key]:
            cp['default'][key] = str(default_vals[key])

    try:
        os.makedirs(user_confdir)
    except FileExistsError:
        pass

    with open(user_conf, 'w') as f:
        cp.write(f)

    try:
        dir_ = os.path.dirname(cp['default']['journal'])
        os.makedirs(dir_)
    except FileExistsError:
        pass


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
