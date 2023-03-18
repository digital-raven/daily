import os
import sys
import tempfile
from subprocess import call

from daily.Journal import Journal, entry_filter, get_title_from_date
from daily.Entry import Entry, entries_to_str, str_to_entries


def do_add(args):
    """ Add a new entry or update existing entries.
    """
    journal = Journal()

    if args.entry_format not in ['rst', 'md']:
        print(f'ERROR: The entry_format setting needs to be either rst or md.')
        sys.exit(1)

    editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
    if not editor:
        print(
            'ERROR: No EDITOR or VISUAL environment variable defined. '
            'Export one of those for your preferred text editor and re-run.')
        sys.exit(1)

    dir_ = os.path.dirname(args.journal)
    if os.path.isfile(dir_):
        print('ERROR: {} not a directory.'.format(dir_))
        sys.exit(1)

    try:
        if args.before:
            args.before = get_title_from_date(args.before)
        if args.after:
            args.after = get_title_from_date(args.after)
        if args.date:
            args.date = get_title_from_date(args.date)

        if not any([args.date, args.after, args.before]):
            args.date = get_title_from_date('today')

    except ValueError as ve:
        print('ERROR: {}'.format(ve))
        sys.exit(1)

    if args.no_edit:
        if not args.date:
            args.date = get_title_from_date('today')

        entry = Entry.createBlankEntry(args.date)
        if args.entry_format == 'md':
            print(entry.getMd(force=True))
        elif args.entry_format == 'rst':
            print(entry.getRst(force=True))

        sys.exit(0)

    try:
        journal.load(args.journal, entry_format=args.entry_format)
    except ValueError as ve:
        print('ERROR: {}'.format(ve))
        sys.exit(1)

    old_entries = []
    if any([args.tags, args.before, args.after, args.tags]):
        old_entries = journal.getEntries(args)
    if args.date and not old_entries:
        old_entries.append(journal[args.date])

    if not old_entries:
        print('No matching entries found.')
        sys.exit(1)

    for entry in old_entries:
        entry.addHeadings(args.headings)

        # Ensures an empty line is printed on the generated RST.
        # If no notes are entered then the 'notes' heading is deleted anyway.
        if 'notes' not in entry.headings:
            entry.headings['notes'] = ''

    # Create tmp file and pre-load it with RST for editing.
    _, path = tempfile.mkstemp(suffix=f'.{args.entry_format}', dir=args.journal)

    try:
        text = entries_to_str(old_entries, args.entry_format, args.headings)
        with open(path, 'w') as f:
            f.write(text)

        call([editor, path])

        with open(path, 'r') as f:
            text = f.read().strip()

    finally:
        os.remove(path)

    try:
        new_entries = str_to_entries(text, args.entry_format)
    except ValueError as ve:
        print('ERROR: A new entry is invalid. {}'.format(ve))
        sys.exit(1)

    journal.updateEntries(new_entries, old_entries, args.headings)

    journal.write(args.journal, args.entry_format)
