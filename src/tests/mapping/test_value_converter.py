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

        self.assertEquals(vot, ValueConverter.filter_vot(vot))
        self.assertEquals(lps, ValueConverter.filter_lps(lps))
        self.assertEquals(sps, ValueConverter.filter_sps(sps))

        self.assertIsNone(ValueConverter.filter_vot(sps))
        self.assertIsNone(ValueConverter.filter_lps(vot))
        self.assertIsNone(ValueConverter.filter_sps(vot))

        self.assertIsNone(ValueConverter.filter_vot(None))
