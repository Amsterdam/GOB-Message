from unittest import TestCase

from gobmessage.mapping.mapper import Mapper


class MapperTestImpl(Mapper):
    catalogue = 'cat'
    collection = 'coll'
    entity_id = 'entity_id'
    version = '0.1'
    fields = {
        'field 1': 'a.c.d',
        'field 2': 'a.b',
        'field 3': 'e',
        'field 4': 'e.f',
    }


class TestMapper(TestCase):

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

        m = MapperTestImpl()
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
        e = MapperTestImpl()
        self.assertEqual('the id', e.get_id({'entity_id': 'the id'}))


