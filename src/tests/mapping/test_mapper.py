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
        'field 5': {
            '_base': 'g.h',
            '_list': True,
            'field 6': 'i',
            'field 7': 'j',
        },
        'field 8': {
            'field 9': 'a.b',
        },
        'field 10': {
            'field 11': 'a.b|a.c.d',
            'field 12': 'a.c.e|a.b',
            'field 13': 'a.c.e|e.c.f',
        },
        'field 14': {
            '_base': 'n.o.n.e.x.i.s.t.e.n.t',
            '_list': True,
            'field 15': 'a',
        },
        'field 15': '=someconstant',
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
                    'e': None,
                },
            },
            'e': 'E',
            'g': {
                'h': [
                    {
                        'i': 'I1',
                        'j': 'J1',
                    },
                    {
                        'i': 'I2',
                        'j': 'J2',
                    },
                ]
            },
        }

        m = MapperTestImpl()
        expected = {
            'field 1': 'ACD',
            'field 2': 'AB',
            'field 3': 'E',
            'field 4': None,
            'field 5': [
                {'field 6': 'I1', 'field 7': 'J1'},
                {'field 6': 'I2', 'field 7': 'J2'},
            ],
            'field 8': {
                'field 9': 'AB',
            },
            'field 10': {
                'field 11': 'AB',
                'field 12': 'AB',
                'field 13': None,
            },
            'field 14': [],
            'field 15': 'someconstant',
        }

        self.assertEqual(expected, m.map(source))

    def test_get_id(self):
        """Tests parent method from Mapper

        :return:
        """
        e = MapperTestImpl()
        self.assertEqual('the id', e.get_id({'entity_id': 'the id'}))


