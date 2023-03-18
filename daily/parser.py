""" daily argument parser.
"""

import argparse
import sys

from daily import __version__
from daily.cli import build_out_subparsers
from daily.parsergroups import create_filter_opts


filter_opts = create_filter_opts()


def print_version():
    class printVersion(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            print(__version__)
            sys.exit(0)
    return printVersion


def create_parser():
    """ Create main parser.

    Returns:
        Reference to the parser. Parse main command line args with
            parser.parse_args().
    """
    parser = argparse.ArgumentParser(
        prog='daily',
        description=(
            'The command-line journal for daily entries. Run "daily" with no '
            'arguments to perform first-time setup.'))

    parser.add_argument(
        '--config',
        help='Select custom configuration file.')

    parser.add_argument(
        '-j', '--journal',
        help='Journal directory.')

    parser.add_argument(
        '-f', '--entry-format', choices=['md', 'rst'],
        help='Text format of the entries.')

    parser.add_argument(
        '--version', nargs=0, help='Print the version of daily and exit.',
        action=print_version())

    # begin subparsers
    subparsers = parser.add_subparsers(
        metavar='command',
        dest='command',
        description='Each has its own [-h, --help] statement.')

    build_out_subparsers(subparsers)

    return parser
