from unittest import TestCase

from gobmessage.mapping.hr import MaatschappelijkeActiviteitenMapper


class TestMaatschappelijkeActiviteitenMapper(TestCase):
    """Tests both this mapper as well as the parent class methods

    """

    def test_map_mac(self):
        """Integration test

        :return:
        """
        source = {
            'maatschappelijkeActiviteit': {
                'registratie': {
                    'datumAanvang': '20181101',
                    'datumEinde': None,
                    'soortMutatie': None,
                    'registratieTijdstip': '20181101162418910',
                    'registratieTijdstipNoValue': None
                },
                'kvkNummer': '123456789',
                'nonMailing': {
                    'code': 'N',
                    'omschrijving': 'Nee',
                    'referentieType': 'geenRT'
                },
                'incidenteelUitlenenArbeidskrachten': {
                    'code': 'J',
                    'omschrijving': 'Ja',
                    'referentieType': 'geenRT'
                },
                'naam': 'Gemeente Amsterdam',
                'communicatiegegevens': {
                    'extraElementen': None,
                    'registratie': {
                        'datumAanvang': '20181101',
                        'datumEinde': None,
                        'soortMutatie': None,
                        'registratieTijdstip': '20181101162418910',
                        'registratieTijdstipNoValue': None
                    },
                    'communicatienummer': [
                        {
                            'extraElementen': None,
                            'toegangscode': '+31',
                            'nummer': '02099999991',
                            'soort': {
                                'code': 'T',
                                'omschrijving': 'Telefoon',
                                'referentieType': None
                            }
                        },
                        {
                            'extraElementen': None,
                            'toegangscode': '+31',
                            'nummer': '02099999992',
                            'soort': {
                                'code': 'F',
                                'omschrijving': 'Fax',
                                'referentieType': None
                            }
                        }
                    ],
                    'emailAdres': [
                        'nepemailadres@kvk.nl',
                        'nepemailadres2@kvk.nl',
                    ],
                    'domeinNaam': [
                        'www1.kvk.nl',
                        'www2.kvk.nl',
                        'www3.kvk.nl'
                    ]
                },
            }
        }
        m = MaatschappelijkeActiviteitenMapper()
        expected = {
            'kvknummer': '123456789',
            'naam': 'Gemeente Amsterdam',
            'non_mailing': False,
            'datum_aanvang_maatschappelijke_activiteit': '2018-11-01',
            'datum_einde_maatschappelijke_activiteit': None,
            'registratie_tijdstip_maatschappelijke_activiteit': '2018-11-01T16:24:18.910000',
            'incidenteel_uitlenen_arbeidskrachten': True,
            'communicatienummer': [
                {'nummer': '02099999991', 'toegangscode': '+31', 'soort': 'Telefoon'},
                {'nummer': '02099999992', 'toegangscode': '+31', 'soort': 'Fax'},
            ],
            'email_adres': [
                {'adres': 'nepemailadres@kvk.nl'},
                {'adres': 'nepemailadres2@kvk.nl'},
            ],
            'domeinnaam': [
                {'naam': 'www1.kvk.nl'},
                {'naam': 'www2.kvk.nl'},
                {'naam': 'www3.kvk.nl'},
            ]
        }
        self.assertEqual(expected, m.map(source))

    def test_properties(self):
        """Tests properties present and set

        :return:
        """
        props = ['catalogue', 'collection', 'entity_id', 'version', 'fields']

        for prop in props:
            self.assertTrue(
                hasattr(MaatschappelijkeActiviteitenMapper, prop) and getattr(MaatschappelijkeActiviteitenMapper,
                                                                              prop))
