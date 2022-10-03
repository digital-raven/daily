import os
import unittest

from daily.Entry import Entry
from daily.Journal import Journal
from daily.parse_date import get_title_from_date

resources = '{}/resources'.format(os.path.dirname(__file__))


class TestEntry(unittest.TestCase):

    def test_single_load_rst(self):
        """ Single entry loaded and the title should update.
        """
        path = f'{resources}/rst/today.rst'
        with open(path) as f:
            text = f.read()

        entry = Entry.createFromRst(text)

        journal = Journal()

        # This line should update the title
        journal[entry] = entry

        exp = get_title_from_date('today')
        self.assertEqual(exp, entry.title)

    def test_single_load_md(self):
        """ Single entry loaded and the title should update.
        """
        path = f'{resources}/md/today.md'
        with open(path) as f:
            text = f.read()

        entry = Entry.createFromMd(text)

        journal = Journal()

        # This line should update the title
        journal[entry] = entry

        exp = get_title_from_date('today')
        self.assertEqual(exp, entry.title)

    def test_load_from_file_rst(self):
        path = f'{resources}/rst'

        journal = Journal()
        journal.load(path, entries=['today.rst'], entry_format='rst')

        with open(f'{path}/today.rst') as f:
            text = f.read()
        entry = Entry.createFromRst(text)

        self.assertEqual(entry.getRst(), journal[entry.title].getRst())

    def test_load_from_file_md(self):
        path = f'{resources}/md'

        journal = Journal()
        journal.load(path, entries=['today.md'], entry_format='md')

        with open(f'{path}/today.md') as f:
            text = f.read()
        entry = Entry.createFromMd(text)

        self.assertEqual(entry.getMd(), journal[entry.title].getMd())


if __name__ == '__main__':
    unittest.main()
