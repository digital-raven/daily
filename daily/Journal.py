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

    return '{}-{}-{}, {}'.format(d.year, d.month, d.day, days[d.weekday()])


class Journal:
    def __init__(self):
        self.entries = dict()  # Looked up by title

    def load(self, journal):
        """ Load entries from the specified journal.

        Args:
            journal: Path to the journal.

        Raises:
            FileNotFoundError if the journal file doesn't exist.

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

    def updateEntry(self, title, new_entry, exp_headings=None, replace=False):
        """ Update an entry.

        The proper way to use this method is as follows..

            entry = journal.updateEntry(entry.title, new_entry)

        because the entry reference may be reassigned internally.

        Args:
            title: Title of the entry to update. Must be a date
                parsable by "parsedatetime".
            new_entry: New Entry instance containing the values to use.
            exp_headings: Expected headings. If not present in the new entry,
                then they will be deleted from the current one.
            replace: If True, simply replace the whole entry with the new one.

        Returns:
            An internal reference to the updated entry.

        Raises:
            ValueError if the title of the new entry could not be
                parsed as a date.
        """
        entry = self.getOrCreateEntry(title)
        old_title = entry.title

        # test validity of new title
        get_title_from_date(new_entry.title)

        if replace:
            entry = new_entry
        else:
            entry.update(new_entry, exp_headings)

        # Delete and replace the old entry in case title changed.
        del(self.entries[old_title])
        self.entries[entry.title] = entry

        return entry

    def getEntry(self, title):
        """ Get an entry by its title.

        Args:
            title: Must be a date parsable by "parsedatetime".

        Returns:
            The corresponding Entry, or None if it wasn't found.

        Raises:
            ValueError if the title coulud not be parsed.
        """
        try:
            title = get_title_from_date(title)
            return self.entries[title]
        except KeyError:
            return None

    def getOrCreateEntry(self, title):
        """ Get or create an entry.

        An entry will be created if it doesn't exist.

        Args:
            title: Title of the entry. Must be a date parsable
                by "parsedatetime".

        Returns:
            A new or existing Entry.

        Raises:
            ValueError if the title coulud not be parsed.
        """
        entry = self.getEntry(title)
        if not entry:
            entry = Entry.createBlankEntry(get_title_from_date(title))
            self.entries[entry.title] = entry

        return entry
