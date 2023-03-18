""" Main code for the "upcoming" subcommand.

This command is basically just "show", but with some preset filters.
It shows entries between today and 2 weeks from now which contain the
tag "events".
"""

from daily.cli.show import do_show
from daily.Journal import get_title_from_date, Journal


def do_upcoming(args):
    if args.entry_format not in ['rst', 'md']:
        print(f'ERROR: The entry_format format needs to be either rst or md.')
        sys.exit(1)

    if args.after:
        args.after = get_title_from_date(args.after)
    if args.before:
        args.before = get_title_from_date(args.before)

    # default date range of +2 weeks
    if not args.before and not args.after:
        args.after = get_title_from_date('today')
        args.before = get_title_from_date('2 weeks from now')

    if args.before and args.after and args.before < args.after:
        print('ERROR: The "before" date cannot be before the "after" date.')
        sys.exit(1)

    journal = Journal()
    try:
        journal.load(args.journal)
    except FileNotFoundError as e:
        print('ERROR: Journal file "{}" does not exist.'.format(args.journal))
        sys.exit(1)
    except PermissionError as e:
        print('ERROR: Journal file "{}" could not be read.'.format(args.journal))
        sys.exit(1)
    except ValueError as e:
        print('ERROR: Journal "{}" contains invalid JSON. {}'.format(args.journal, e))
        sys.exit(1)

    entries = []
    if args.entry_format == 'rst':
        entries = [x.getRst(['events']) for x in journal]
    elif args.entry_format == 'md':
        entries = [x.getMd(['events']) for x in journal]

    entries = sorted([x.getRst(['events']) for x in journal])
    print('\n'.join([x for x in entries if x]))
