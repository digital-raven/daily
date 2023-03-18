from daily.parsergroups import create_filter_opts

filter_opts = create_filter_opts()


def add_subparser(subparsers):
    sp = subparsers.add_parser(
        'show',
        help='Display journal entries.',
        parents=[filter_opts])

    sp.add_argument(
        'headings', metavar='HEADING', nargs='*',
        help='Only show entries made under the specified headings.')
