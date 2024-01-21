import os
import sys

from libzet import create_zettel, edit_zettels, load_zettels, load_zettels, move_zettels, save_zettels
from superdate import parse_date

from daily.load import get_title_from_date, load_entries


def _get_filepath(date_, journal, format_):
    """ What should the path to an entry be?

    Args:
        date_: Date of entry
        journal: Directory containing entries.
        format: file extension of entry

    Returns:
        Expected filepath.
    """
    exp = parse_date(date_).strftime(f'%Y-%m-%d.{format_}')
    return os.path.sep.join([journal, exp])


def _correct_entry(z, args):
    """ Correct and save an entry.

    Use like z = _correct_entry(z, entry_format)

    Returns:
        A ref to the corrected entry.
    """
    if 'tags' not in z.attrs:
        z.attrs['tags'] = []

    z.attrs['tags'] = sorted(list(set(z.attrs['tags'])))

    # Sync date and filepath
    z.title = get_title_from_date(z.title)

    exp_path = _get_filepath(z.title, args.journal, args.entry_format)
    if '_loadpath' not in z.attrs:
        z.attrs['_loadpath'] = exp_path

    if z.attrs['_loadpath'] != exp_path:
        z = move_zettels(z, exp_path)[0]
    else:
        save_zettels(z, args.entry_format)

    return z


def main(args):
    """ Add a new entry or update existing entries.
    """
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

    # Possibly create and save a new entry for the date.
    if not any([args.date, args.before, args.after]):
        args.date = 'today'

    if args.date:
        new_zet_path = _get_filepath(args.date, args.journal, args.entry_format)

        # If copying a previous entry
        class _MockArgsCopyPrevious:
            def __init__(self, args):
                self._args = args
                self.after = f'{args.copy_previous} - 1 year'
                self.before = args.copy_previous

            def __getattr__(self, key):
                """ If not referring to any SuperDate attrs then forward to date.
                """
                if key in self.__dict__:
                    return self.__dict__[key]
                else:
                    return self._args.__getattribute__(key)

        # Set up information for new entry.
        title = args.date
        headings = None
        attrs = None
        zettel_format = args.entry_format
        no_edit = True

        if args.copy_previous:
            try:
                prev_zet = sorted(
                    load_entries(_MockArgsCopyPrevious(args)),
                    key=lambda x: x.title)[-1]
                headings = prev_zet.headings
                attrs = prev_zet.attrs
            except IndexError:  # No zettels found.
                pass

        try:
            z = create_zettel(new_zet_path, '', title, headings, attrs, zettel_format, no_edit)
        except FileExistsError:
            z = load_zettels(new_zet_path, args.entry_format)[0]

        _correct_entry(z, args)

    # Load entries
    try:
        entries = load_entries(args)
    except ValueError as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    if not entries:
        print('No matching entries found.')
        sys.exit(1)

    # Edit and save
    modified = edit_zettels(entries, args.entry_format, args.headings, f'failed-adds.{args.entry_format}', delete=True)
    [_correct_entry(z, args) for z in modified]
