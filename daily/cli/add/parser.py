from daily.parsergroups import create_filter_opts


filter_opts = create_filter_opts()


def add_subparser(subparsers):
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
