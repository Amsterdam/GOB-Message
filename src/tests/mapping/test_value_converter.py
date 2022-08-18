from unittest import TestCase
from gobmessage.mapping.value_converter import ValueConverter


class TestValueConverter(TestCase):

    def test_jn_to_bool(self):
        testcases = [
            ('J', True),
            ('N', False),
            ('Other', None),
            (None, None),
        ]
        for input, expected in testcases:
            self.assertEqual(expected, ValueConverter.jn_to_bool(input))

    def test_to_date(self):
        testcases = [
            ('20210216', '2021-02-16'),
            (None, None),
        ]

        for input, expected in testcases:
            self.assertEqual(expected, ValueConverter.to_date(input))

    def test_to_incomplete_date(self):
        testcases = [
            ('00000000', '0000-00-00'),
            ('20000000', '2000-00-00'),
            ('20001000', '2000-10-00'),
            ('20001010', '2000-10-10'),
            ('20200504', '2020-05-04'),
            (None, None)
        ]
        testcases_raise = ['0000', '000000000']

        for input, expected in testcases:
            self.assertEqual(expected, ValueConverter.to_incomplete_date(input))

        for test in testcases_raise:
            with self.assertRaises(ValueError):
                ValueConverter.to_incomplete_date(test)

    def test_to_datetime(self):
        testcases = [
            ('20181101162418910', '2018-11-01T16:24:18.910000'),
            ('20181101162418910123', '2018-11-01T16:24:18.910123'),
            (None, None),
        ]

        for input, expected in testcases:
            self.assertEqual(expected, ValueConverter.to_datetime(input))

    def test_filter_aot_methods(self):
        vot = 'xxxx01xxxxxxxx'
        lps = 'xxxx02xxxxxxxx'
        sps = 'xxxx03xxxxxxxx'

        self.assertEqual(vot, ValueConverter.filter_vot(vot))
        self.assertEqual(lps, ValueConverter.filter_lps(lps))
        self.assertEqual(sps, ValueConverter.filter_sps(sps))

        self.assertIsNone(ValueConverter.filter_vot(sps))
        self.assertIsNone(ValueConverter.filter_lps(vot))
        self.assertIsNone(ValueConverter.filter_sps(vot))

        self.assertIsNone(ValueConverter.filter_vot(None))
