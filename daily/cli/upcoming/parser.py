from daily.parsergroups import create_filter_opts


filter_opts = create_filter_opts()


def add_subparser(subparsers):
    sp = subparsers.add_parser(
        'upcoming',
        help='Display upcoming events.',
        description=(
            'These are any entries with an "events" heading within the'
            '(default) range of 2 weeks.'),
        parents=[filter_opts])
