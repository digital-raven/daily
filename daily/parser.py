""" daily argument parser.
"""

import argparse
import sys

from daily import __version__
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
        help='Specify the journal to operate on.')

    parser.add_argument(
        '--version', nargs=0, help='Print the version of daily and exit.',
        action=print_version())

    # begin subparsers
    subparsers = parser.add_subparsers(
        metavar='command',
        dest='command',
        description='Each has its own [-h, --help] statement.')

    # add command
    create_add_subparser(subparsers)

    # refresh command
    create_refresh_subparser(subparsers)

    # show command
    create_show_subparser(subparsers)

    # upcoming command
    create_upcoming_subparser(subparsers)

    return parser


def create_add_subparser(subparsers):
    sp = subparsers.add_parser(
        'add', help='Add a new entry or modify an existing one.',
        parents=[filter_opts])

    sp.add_argument(
        '--no-edit', action='store_true',
        help=('Create a new empty entry for the given date. '
              'Only compatible with -d option.'))

    sp.add_argument(
        'headings', metavar='HEADING',
        help='Add (or modify) specific headings for an entry.', nargs='*')

    return sp


def create_refresh_subparser(subparsers):
    sp = subparsers.add_parser(
        'refresh',
        help='Refresh a journal to weed out minor errors in bulk.')

    sp.add_argument(
        'headings', metavar='HEADING', nargs='*',
        help='Only show entries made under the specified headings.')

    return sp


def create_show_subparser(subparsers):
    sp = subparsers.add_parser(
        'show',
        help='Display journal entries.',
        parents=[filter_opts])

    sp.add_argument(
        'headings', metavar='HEADING', nargs='*',
        help='Only show entries made under the specified headings.')

    return sp


def create_upcoming_subparser(subparsers):
    sp = subparsers.add_parser(
        'upcoming',
        help='Display upcoming events.',
        description=(
            'These are any entries with an "events" heading within the'
            '(default) range of 2 weeks.'),
        parents=[filter_opts])

    return sp
