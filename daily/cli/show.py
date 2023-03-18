import sys

from daily.Journal import Journal, get_title_from_date
from daily.Entry import entries_to_str


def do_show(args):
    journal = Journal()

    if args.entry_format not in ['rst', 'md']:
        print(f'ERROR: The entry_format setting needs to be either rst or md.')
        sys.exit(1)

    args.tags = [x for x in args.tags.split(',') if x]

    if args.date:
        args.date = get_title_from_date(args.date)

    if args.after:
        args.after = get_title_from_date(args.after)
    if args.before:
        args.before = get_title_from_date(args.before)

    if not any([args.after, args.before, args.date, args.tags]):
        args.after = get_title_from_date('2 weeks ago')
        args.before = get_title_from_date('today')

    if args.before and args.after and args.before < args.after:
        print('ERROR: The "before" date cannot be before the "after" date.')
        sys.exit(1)

    try:
        journal.load(args.journal, entry_format=args.entry_format)
    except FileNotFoundError as e:
        print('ERROR: Journal file "{}" does not exist.'.format(args.journal))
        sys.exit(1)
    except PermissionError as e:
        print('ERROR: Journal file "{}" could not be read.'.format(args.journal))
        sys.exit(1)
    except ValueError as e:
        print('ERROR: Journal "{}" contains invalid JSON. {}'.format(args.journal, e))
        sys.exit(1)

    entries = journal.getEntries(args)
    print(entries_to_str(entries, args.entry_format, args.headings))
