from unittest import TestCase

from gobmessage.mapping.hr import MaatschappelijkeActiviteitenMapper


class TestMaatschappelijkeActiviteitenMapper(TestCase):
    """Tests both this mapper as well as the parent class methods

    """

    def test_map(self):
        """Tests parent method from Mapper

        :return:
        """
        source = {
            'a': {
                'b': 'AB',
                'c': {
                    'd': 'ACD',
                },
            },
            'e': 'E',
        }

        m = MaatschappelijkeActiviteitenMapper()
        m.fields = {
            'field 1': 'a.c.d',
            'field 2': 'a.b',
            'field 3': 'e',
            'field 4': 'e.f',
        }

        expected = {
            'field 1': 'ACD',
            'field 2': 'AB',
            'field 3': 'E',
            'field 4': None,
        }

        self.assertEqual(expected, m.map(source))

    def test_get_id(self):
        """Tests parent method from Mapper

        :return:
        """
        e = MaatschappelijkeActiviteitenMapper()
        e.entity_id = 'entity_id'
        self.assertEqual('the id', e.get_id({'entity_id': 'the id'}))

    def test_properties(self):
        """Tests properties present and set

        :return:
        """
        props = ['catalogue', 'collection', 'entity_id', 'version', 'fields']

        for prop in props:
            self.assertTrue(hasattr(MaatschappelijkeActiviteitenMapper, prop) and getattr(MaatschappelijkeActiviteitenMapper, prop))
