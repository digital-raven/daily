import os
import sys
import tempfile
from subprocess import call

from daily.Journal import Journal
from daily.Entry import Entry


def do_add(args):
    """ Add or update an existing entry.
    """
    journal = Journal()

    editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
    if not editor:
        print(
            'ERROR: No EDITOR or VISUAL environment variable defined. '
            'Export one of those for your preferred text editor and re-run.')
        sys.exit(1)

    dir_ = os.path.dirname(args.journal)
    if os.path.isfile(dir_):
        print('ERROR: {} is an existing file.'.format(dir_))
        sys.exit(1)

    if os.path.isfile(args.journal):
        try:
            journal.load(args.journal)
        except ValueError as ve:
            print('ERROR: {}'.format(ve))
            sys.exit(1)

    entry = journal.getOrCreateEntry(args.date)
    entry.addHeadings(args.headings)

    # Ensures an empty line is printed on the generated RST.
    # If no notes are entered then the 'notes' heading is deleted anyway.
    if 'notes' not in entry.headings:
        entry.headings['notes'] = ''

    # Create tmp file and pre-load it with RST for editing.
    _, path = tempfile.mkstemp(suffix='.rst')

    try:
        with open(path, 'w') as f:
            f.write(entry.getRst(args.headings))

        call([editor, path])

        with open(path, 'r') as f:
            text = f.read()

    finally:
        os.remove(path)

    try:
        entry = journal.updateEntry(
            entry.title, Entry.createFromRst(text),
            args.headings, replace=not args.headings)
    except ValueError as ve:
        print('ERROR: Your new entry is invalid. {}'.format(ve))
        sys.exit(1)

    journal.write(args.journal)
