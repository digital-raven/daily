from daily.parsergroups import create_filter_opts


filter_opts = create_filter_opts()


def add_subparser(subparsers):
    sp = subparsers.add_parser(
        'add', help='Add a new entry or modify existing ones.',
        parents=[filter_opts])

    sp.add_argument(
        '--no-edit', action='store_true',
        help=("""Create a new empty entry for the given date.
              Only compatible with -d option."""))

    sp.add_argument(
        '--copy-previous', default='', const='yesterday', nargs='?',
        help=("""Copy the content from a previous entry. Plain english date
              phrases are accepted. If this option is provided with no
              argument then its value defaults to "yesterday".

              The idea is to create a large file with information that you want
              to see regularly but don't update frequently. This makes it easier
              to review general day patterns, weight, or weekly goals."""))

    sp.add_argument(
        'headings', metavar='HEADING',
        help='Add (or modify) specific headings for an entry.', nargs='*')
