import os
from datetime import datetime
from glob import glob

from libzet import load_zettels
from superdate import parse_date


def get_title_from_date(date, format_='%Y-%m-%d, %a'):
    """ Generate a more human-readable title.

    Returns:
        A string showing the date in Y-m-d format and the weekday.

    Raises:
        ValueError if date could not be parsed.
    """
    return parse_date(date).strftime(format_)


def entry_filter(entry, args):
    """ Returns True if the entry satisfies the filters in args.
    """
    is_after = args.after and entry.title >= args.after
    is_before = args.before and entry.title <= args.before
    is_date = args.date and entry.title == args.date

    if not any([args.after, args.before, args.date]):
        is_after = is_before = is_date = True
    else:
        if args.before and not args.after:
            is_after = True
        if args.after and not args.before:
            is_before = True

    in_date = (is_after and is_before) or is_date
    in_tags = not args.tags or any([x for x in args.tags if x in entry.attrs['tags']])

    return in_date and in_tags


def load_entries(args):
    """ Load entries from args.

    Args:
        The argparse instance used by daily commands.

    Returns:
        A list of the loaded zettels.

    Raises:
        FileNotFoundError if the journal file doesn't exist.
        PermissionError if the journal file couldn't be read.

        ValueError if an entry in the journal contains an invalid entry.
        The message will indicate which entry and the error.
    """
    if args.before:
        args.before = get_title_from_date(args.before)
    if args.after:
        args.after = get_title_from_date(args.after)
    if args.date:
        args.date = get_title_from_date(args.date)

    if args.before and args.after and args.before < args.after:
        print('ERROR: The "before" date cannot be before the "after" date.')
        sys.exit(1)

    args.tags = [x for x in args.tags.split(',') if x]

    match_ = f'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].{args.entry_format}'
    paths = glob(f'{args.journal}/{match_}')

    zettels = load_zettels(paths, args.entry_format)
    zettels = [z for z in zettels if entry_filter(z, args)]

    return zettels
