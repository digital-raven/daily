import sys

from daily.Journal import Journal, get_title_from_date


def filter_func(entry, args):
    """ Returns True if the entry satisfies the filters in args.
    """
    print(args.after, args.before)
    is_after = not args.after or args.after <= entry.title
    is_before = not args.before or entry.title <= args.before

    in_date = is_after and is_before
    in_tags = not args.tags or any([x for x in args.tags if x in entry.tags])

    return in_date and in_tags


def do_show(args):
    journal = Journal()

    args.tags = [x for x in args.tags.split(',') if x]

    if args.after:
        args.after = get_title_from_date(args.after)
    if args.before:
        args.before = get_title_from_date(args.before)

    if not args.tags and not args.before and not args.after:
        args.after = get_title_from_date('2 weeks ago')
        args.before = get_title_from_date('today')

    if args.before and args.after and args.before < args.after:
        print('ERROR: The "before" date cannot be before the "after" date.')
        sys.exit(1)

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

    entries = [x.getRst(args.headings) for x in journal if filter_func(x, args)]
    print('\n'.join([x for x in entries if x]))
