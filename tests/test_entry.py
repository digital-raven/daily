import os
import unittest

from daily.Entry import Entry, get_entries_from_md, get_entries_from_rst

resources = '{}/resources'.format(os.path.dirname(__file__))


class TestEntry(unittest.TestCase):

    def test_basic_rst_parsing(self):
        """ Single rst entry.
        """
        path = f'{resources}/rst/today.rst'
        with open(path) as f:
            rst = f.read()

        entry = Entry.createFromRst(rst)

        self.assertEqual('today', entry.title)
        self.assertEqual('Today is today\n', entry.headings['notes'])
        self.assertEqual('heading body\n', entry.headings['today heading'])
        self.assertEqual('heading body\n\nmultiline\n', entry.headings['second heading'])
        self.assertEqual('today-id', entry.id)
        self.assertEqual(['birthday'], entry.tags)

    def test_basic_md_parsing(self):
        """ Single md entry.
        """
        path = f'{resources}/md/today.md'
        with open(path) as f:
            md = f.read()

        entry = Entry.createFromMd(md)

        self.assertEqual('today', entry.title)
        self.assertEqual('Today is today\n', entry.headings['notes'])
        self.assertEqual('heading body\n', entry.headings['today heading'])
        self.assertEqual('heading body\n\nmultiline\n', entry.headings['second heading'])
        self.assertEqual('today-id', entry.id)
        self.assertEqual(['birthday'], entry.tags)

    def test_compound_rst_parsing(self):
        """ Multiple entries in one file.
        """
        path = f'{resources}/rst'

        with open(f'{path}/today.rst') as f:
            today = Entry.createFromRst(f.read())

        with open(f'{path}/tomorrow.rst') as f:
            tomorrow = Entry.createFromRst(f.read())

        with open(f'{path}/all.rst') as f:
            all = get_entries_from_rst(f.read())

        self.assertEqual(all, [today, tomorrow])

    def test_compound_md_parsing(self):
        """ Multiple entries in one file.
        """
        path = f'{resources}/md'

        with open(f'{path}/today.md') as f:
            today = Entry.createFromMd(f.read())

        with open(f'{path}/tomorrow.md') as f:
            tomorrow = Entry.createFromMd(f.read())

        with open(f'{path}/all.md') as f:
            all = get_entries_from_md(f.read())

        self.assertEqual(all, [today, tomorrow])


if __name__ == '__main__':
    unittest.main()
