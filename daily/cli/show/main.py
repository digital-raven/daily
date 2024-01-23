import sys

from libzet import zettels_to_str

from daily.load import get_title_from_date, load_entries


def main(args):
    if args.entry_format not in ['rst', 'md']:
        print(f'ERROR: The entry_format setting needs to be either rst or md.')
        sys.exit(1)

    if not any([args.after, args.before, args.date, args.tags]):
        args.after = get_title_from_date('2 weeks ago')
        args.before = get_title_from_date('today')

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

    print(zettels_to_str([e for e in entries if e.title], args.entry_format, args.headings))
