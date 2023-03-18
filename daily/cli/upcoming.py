""" todo subcommand.

This command is basically just "show", but with some preset filters.
It shows todos between 2 weeks from now.
"""
from libzet import zettels_to_str

from daily.load import get_title_from_date, load_entries


def do_upcoming(args):

    # default date range of +2 weeks
    if not args.before and not args.after:
        args.after = get_title_from_date('today')
        args.before = get_title_from_date('2 weeks from now')

    try:
        entries = load_entries(args)
    except FileNotFoundError as e:
        print(f'ERROR: "{args.journal}" does not exist.')
        sys.exit(1)
    except PermissionError as e:
        print(f'ERROR: "{args.journal}" could not be read.')
        sys.exit(1)
    except ValueError as e:
        print(f'ERROR: "{args.journal}" contains invalid entries. {e}')
        sys.exit(1)

    print(zettels_to_str(entries, args.entry_format, headings=['todo']))
