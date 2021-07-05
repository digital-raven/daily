import json
import os
from datetime import datetime

import parsedatetime as pdt

from daily.Entry import Entry


def get_title_from_date(date):
    """ Generate a more human-readable title.

    Returns:
        A string showing the date in Y-m-d format and the weekday.

    Raises:
        ValueError if date could not be parsed.
    """
    cal = pdt.Calendar()
    d, flag = cal.parse(date)

    if not flag:
        raise ValueError('The date "{}" could not be parsed.'.format(date))

    d = datetime(*d[:3])

    days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    return '{}-{:02d}-{:02d}, {}'.format(d.year, d.month, d.day, days[d.weekday()])


class Journal:
    def __init__(self):
        self.entries = dict()  # Looked up by title

    def load(self, journal):
        """ Load entries from the specified journal.

        Args:
            journal: Path to the journal.

        Raises:
            FileNotFoundError if the journal file doesn't exist.
            PermissionError if the journal file couldn't be read.

            ValueError if an entry in the journal was invalid. The message
            will indicate which entry and the error.
        """
        try:
            with open(journal, 'r') as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError as jde:
            raise ValueError('Parsing the journal {}: {}'.format(journal, jde))

        for entry, num in zip(data, range(1, len(data) + 1)):
            try:
                self.entries[entry['title']] = Entry.fromDict(entry)
            except ValueError as ve:
                raise ValueError('Entry {} is invalid. {}'.format(num, ve))

    def write(self, journal):
        """ Write the journal to disk.

        Args:
            journal: Path to the journal.
        """
        dir_ = os.path.dirname(journal)
        if dir_ and not os.path.isdir(dir_):
            os.makedirs(dir_)

        with open(journal, 'w') as f:
            data = [v.__dict__ for v in sorted(list(self.entries.values()))]
            json.dump(data, f, indent=4)

    def updateEntry(self, entry, new_entry, exp_headings=None, replace=False):
        """ Update an entry.

        The proper way to use this method is as follows..

            entry = journal.updateEntry(entry, new_entry)

        because the entry reference may be reassigned internally.

        Args:
            title: The entry (or its title) to update.
            new_entry: New Entry instance containing the values to use.
            exp_headings: Expected headings. If not present in the new entry,
                then they will be deleted from the current one.
            replace: If True, simply replace the whole entry with the new one.

        Returns:
            An internal reference to the updated entry. None will be returned
            if the new entry contained no content. This means the entry was
            deleted.

        Raises:
            ValueError if the title of the new entry could not be
                parsed as a date.
        """
        title = entry
        if type(title) == Entry:
            title = entry.title

        entry = self[title]
        old_title = entry.title

        entry.update(new_entry, exp_headings, replace)

        # Delete and replace the old entry in case title changed.
        del self[old_title]

        if entry.headings or entry.tags:
            self[entry.title] = entry
            return entry

        return None

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

    def __delitem__(self, title):
        if type(title) == Entry:
            title = title.title

        if title not in self.entries:
            title = get_title_from_date(title)

        del self.entries[title]

    def __iter__(self):
        for key in self.entries:
            yield self[key]
