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
                'manifesteertZichAls': {
                    'extraElementen': None,
                    'relatieRegistratie': {
                        'datumAanvang': '20181101',
                        'datumEinde': None,
                        'soortMutatie': None,
                        'registratieTijdstip': '20181101162418910',
                        'registratieTijdstipNoValue': None
                    },
                    'onderneming': {
                        'extraElementen': None,
                        'registratie': {
                            'datumAanvang': '20181101',
                            'datumEinde': None,
                            'soortMutatie': None,
                            'registratieTijdstip': '20181101162418910',
                            'registratieTijdstipNoValue': None
                        },
                        'kvkNummer': '90004213',
                        'voltijdWerkzamePersonen': 12,
                        'deeltijdWerkzamePersonen': 4,
                        'totaalWerkzamePersonen': 16,
                        'handeltOnder': [
                            {
                                'extraElementen': None,
                                'relatieRegistratie': None,
                                'handelsnaam': {
                                    'extraElementen': None,
                                    'registratie': {
                                        'datumAanvang': '20181101',
                                        'datumEinde': None,
                                        'soortMutatie': None,
                                        'registratieTijdstip': '20181101162418910',
                                        'registratieTijdstipNoValue': None
                                    },
                                    'naam': 'Handelsnaam 1',
                                    'volgorde': 0
                                }
                            },
                            {
                                'extraElementen': None,
                                'relatieRegistratie': None,
                                'handelsnaam': {
                                    'extraElementen': None,
                                    'registratie': {
                                        'datumAanvang': '20181101',
                                        'datumEinde': None,
                                        'soortMutatie': None,
                                        'registratieTijdstip': '20181101162418910',
                                        'registratieTijdstipNoValue': None
                                    },
                                    'naam': 'Handelsnaam 2',
                                    'volgorde': 1
                                }
                            }
                        ],
                        'isEenManifestatieVan': None,
                        'isOvergenomenVan': None,
                        'isOvergedragenNaar': None
                    }
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
            ],
            'registratie_tijdstip_onderneming': '2018-11-01T16:24:18.910000',
            'datum_aanvang_onderneming': '2018-11-01',
            'datum_einde_onderneming': None,
            'totaal_werkzame_personen': 16,
            'voltijd_werkzame_personen': 12,
            'deeltijd_werkzame_personen': 4,
            'handelt_onder_handelsnamen': [{
                'datum_aanvang_handelsnaam': '2018-11-01',
                'datum_einde_handelsnaam': None,
                'omschrijving': 'Handelsnaam 1',
                'tijdstip_registratie': '2018-11-01T16:24:18.910000',
                'volgorde': 0
            }, {
                'datum_aanvang_handelsnaam': '2018-11-01',
                'datum_einde_handelsnaam': None,
                'omschrijving': 'Handelsnaam 2',
                'tijdstip_registratie': '2018-11-01T16:24:18.910000',
                'volgorde': 1
            }],
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
