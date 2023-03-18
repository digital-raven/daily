import unittest
from datetime import datetime

from daily.parse_date import parse_date, get_title_from_date


class TestParseDate(unittest.TestCase):

    def test_basic_date_parsing(self):
        """ Can turn words into datetimes.
        """
        exp = datetime.today().date()
        act = parse_date('today')
        self.assertEqual(exp, act)

    def test_basic_time_parsing(self):
        """ Only has up to minute precision.
        """
        exp = datetime.now()
        exp = datetime(exp.year, exp.month, exp.day, exp.hour, exp.minute)
        act = parse_date('now')
        self.assertEqual(exp, act)

    def test_title_parsing(self):
        """ Dates should turn into titles.
        """
        format_ = '%Y-%m-%d, %a'
        exp = datetime.today().strftime(format_)
        act = get_title_from_date('today')

        self.assertEqual(exp, act)

    def test_title_parsing_custom_format(self):
        """ Can parse into an arbitrary format.
        """
        format_ = '%Y-%m-%d'
        exp = datetime.today().strftime(format_)
        act = get_title_from_date('today', format_)

        self.assertEqual(exp, act)


if __name__ == '__main__':
    unittest.main()
