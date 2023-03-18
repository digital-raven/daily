import os
from datetime import datetime
from glob import glob

from daily.Entry import Entry, get_entries_from_md, get_entries_from_rst
from daily.parse_date import get_title_from_date


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
    in_tags = not args.tags or any([x for x in args.tags if x in entry.tags])

    return in_date and in_tags


class Journal:
    def __init__(self, entry_format='rst'):
        self.entries = dict()  # Looked up by title.
        self.modified = set()  # Only write modified entries to disk.

    def load(self, journal, entries=None, entry_format='rst'):
        """ Load entries from the specified journal.

        Args:
            journal: Path to the journal.
            entries: Optional; Specific entry files to load.
            entry_format: rst or md

        Raises:
            FileNotFoundError if the journal file doesn't exist.
            PermissionError if the journal file couldn't be read.

            ValueError if an entry in the journal contains an invalid entry.
            The message will indicate which entry and the error.
        """
        if entry_format not in ['md', 'rst']:
            raise ValueError('entry_format must be rst or md.')

        match_ = f'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].{entry_format}'

        paths = []
        if entries:
            paths = [f'{journal}/{x}' for x in entries]
        else:
            paths = glob(f'{journal}/{match_}')

        for path in paths:
            path = f'{path}'
            with open(path) as f:
                text = f.read()

            new_entries = []
            try:
                if entry_format == 'rst':
                    new_entries = get_entries_from_rst(text)
                elif entry_format == 'md':
                    new_entries = get_entries_from_md(text)

            except ValueError as ve:
                raise ValueError(f'Entry {path} is invalid: {ve}')

            for new_entry in new_entries:
                self.entries[new_entry.title] = new_entry

    def write(self, journal, entry_format='rst'):
        """ Write this journal to disk.

        Args:
            journal: Directory to write.
        """
        if entry_format not in ['md', 'rst']:
            raise ValueError('entry_format must be rst or md.')

        os.makedirs(journal, exist_ok=True)

        for key in self.modified:
            entry = self.entries[key]
            name = get_title_from_date(entry.title, '%Y-%m-%d')
            path = f'{journal}/{name}.{entry_format}'
            with open(path, 'w') as f:
                if entry_format == 'rst':
                    f.write(entry.getRst(force=True))
                elif entry_format == 'md':
                    f.write(entry.getMd(force=True))

        self.modified = set()

    def updateEntries(self, new_entries, exp_entries=None, exp_headings=None):
        """ Update or add a bunch of entries at once.

        Args:
            new_entries: List of entries with new content.
            exp_entries: A list of the old entries being updated. If an entry
                is present here, but not in new_entries, then it will be
                removed from the journal.
            exp_headings: See updateEntry.
        """
        exp_entries = exp_entries or []

        new_entries = {x.id: x for x in new_entries}
        exp_entries = {x.id: x for x in exp_entries}

        # Compare IDs to determine which entries to delete
        del_entries = [x for x in exp_entries.values() if x.id not in new_entries]

        # Delete removed entries. This won't delete the entries on disk; just
        # prevent them from being updated.
        for entry in del_entries:
            del self[entry]

        # Update old entries or add new ones.
        for id_, entry in new_entries.items():
            if id_ in exp_entries:
                self.updateEntry(exp_entries[id_], entry, exp_headings)
            else:
                self.updateEntry(entry, entry, exp_headings)

    def updateEntry(self, entry, new_entry, exp_headings=None):
        """ Update an entry.

        The proper way to use this method is as follows..

            entry = journal.updateEntry(entry, new_entry)

        because the entry reference may be reassigned internally.

        Args:
            title: The entry (or its title) to update.
            new_entry: New Entry instance containing the values to use.
            exp_headings: Expected headings. If not present in the new entry,
                then they will be deleted from the current one.

        Returns:
            An internal reference to the updated entry..

        Raises:
            ValueError if the title of the new entry could not be
                parsed as a date.
        """
        title = entry
        if type(title) == Entry:
            title = entry.title

        entry = self[title]
        old_title = entry.title
        new_entry.title = get_title_from_date(new_entry.title)

        entry.update(new_entry, exp_headings)

        # Delete and replace the old entry in case title changed.
        del self[old_title]
        if old_title in self.modified:
            self.modified.remove(old_title)

        self[entry.title] = entry
        self.modified.add(entry.title)
        return entry

    def __getitem__(self, title):
        """ Get an entry or create one if it doesn't exist.

        Args:
            title: Can be an entry or the title of one.

        Returns:
            The corresponding Entry for the title.

        Raises:
            ValueError if the title was invalid.
        """
        if type(title) == Entry:
            title = title.title

        try:
            return self.entries[title]
        except KeyError:
            title = get_title_from_date(title)

            if title not in self.entries:
                entry = Entry(title, headings={}, tags=[])
                self.entries[title] = entry
                return self.entries[title]
            else:
                return self.entries[title]

    def __setitem__(self, title, entry):
        if type(title) == Entry:
            title = title.title

        if title not in self.entries:
            title = get_title_from_date(title)

        self.entries[title] = entry
        entry.title = title

    def __delitem__(self, entry):
        """ Delete an entry.

        Usable as `del journal[entry]`.

        Args:
            entry: An entry instance or title of one.
        """
        if type(entry) == Entry:
            entry = entry.title

        del self.entries[entry]

    def __iter__(self):
        """ The Journal class supports iteration through entries.
        """
        for key in self.entries:
            yield self[key]
