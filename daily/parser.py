""" daily argument parser.
"""

import argparse

from daily.parsergroups import create_filter_opts


def create_parser():
    """ Create main parser.

    Returns:
        Reference to the parser. Parse main command line args with
            parser.parse_args().
    """
    filter_opts = create_filter_opts()

    parser = argparse.ArgumentParser(
        prog='daily',
        description=(
            'The ultimate command-line journal. Run "daily" with no '
            'arguments to perform first-time setup.'))

    parser.add_argument(
        '--config',
        help='Select custom configuration file.')

    parser.add_argument(
        '-j', '--journal',
        help='Specify the journal to operate on.')

    # begin subparsers
    subparsers = parser.add_subparsers(
        metavar='command',
        dest='command',
        description='Each has its own [-h, --help] statement.')

    # add command
    sp = subparsers.add_parser(
        'add', help='Add a new entry or modify an existing one.')

    sp.add_argument(
        '-d', '--date',
        help='Select the entry for a specific date, instead of "today".',
        default='today')

    sp.add_argument(
        'headings', metavar='HEADING',
        help='Add (or modify) specific headings for an entry.', nargs='*')

    # show command
    sp = subparsers.add_parser(
        'show',
        help='Display journal entries.',
        parents=[filter_opts])

    sp.add_argument(
        'headings', metavar='HEADING', nargs='*',
        help='Only show entries made under the specified headings.')

    return parser
