""" Parsergroups for daily.
"""

import argparse


def create_filter_opts():
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group(
        'filter options',
        'Filter for entries on the specified criteria.')
    group.add_argument(
        '--after',
        metavar='DATE',
        help='Filter for transactions after this date.')
    group.add_argument(
        '--before',
        metavar='DATE',
        help='Filter for entries after this date.')
    group.add_argument(
        '-d, --date',
        help='The entry on this date.')
    group.add_argument(
        '--tags',
        help='Filter for entries with any of the mentioned tags.',
        metavar='TAGS', default='')

    return parser
