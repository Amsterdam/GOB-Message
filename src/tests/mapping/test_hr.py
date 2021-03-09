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
            'registratie': {
                'datumAanvang': '20181101',
                'datumEinde': None,
                'soortMutatie': None,
                'registratieTijdstip': '20181101162418910',
                'registratieTijdstipNoValue': None
            },
            'kvkNummer': '123456789',
            'sbiActiviteit': [
                {
                    'sbiCode': {
                        'code': '01133',
                        'omschrijving': 'Teelt van groenten in de volle grond',
                        'referentieType': 'ActiviteitCode'
                    },
                },
                {
                    'sbiCode': {
                        'code': '01134',
                        'omschrijving': 'Teelt van groenten in de volle grond',
                        'referentieType': 'ActiviteitCode'
                    },
                }
            ],
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
            'bezoekLocatie': {
                'volledigAdres': 'Amstel 1 Amsterdam'
            },
            'postLocatie': {
                'volledigAdres': 'Amstel 1 Amsterdam'
            },
            'wordtUitgeoefendIn': [
                {
                    'extraElementen': None,
                    'relatieRegistratie': {
                        'datumAanvang': '20181101',
                        'datumEinde': None,
                        'soortMutatie': None,
                        'registratieTijdstip': '20181101162418910',
                        'registratieTijdstipNoValue': None
                    },
                    'nietCommercieleVestiging': {
                        'vestigingsnummer': '12344450236',
                    }
                },
                {
                    'extraElementen': None,
                    'relatieRegistratie': {
                        'datumAanvang': '20181101',
                        'datumEinde': None,
                        'soortMutatie': None,
                        'registratieTijdstip': '20181101162418910',
                        'registratieTijdstipNoValue': None
                    },
                    'nietCommercieleVestiging': {
                        'vestigingsnummer': '12344450237',
                    }
                },
            ],
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
                    'sbiActiviteit': [
                        {
                            'extraElementen': None,
                            'registratie': {
                                'datumAanvang': '20181101',
                                'datumEinde': None,
                                'soortMutatie': None,
                                'registratieTijdstip': '20181101162418910',
                                'registratieTijdstipNoValue': None
                            },
                            'sbiCode': {
                                'code': '01131',
                                'omschrijving': 'Teelt van groenten in de volle grond',
                                'referentieType': 'ActiviteitCode'
                            },
                            'isHoofdactiviteit': {
                                'code': 'J',
                                'omschrijving': 'Ja',
                                'referentieType': 'geenRT'
                            },
                            'volgorde': None
                        },
                        {
                            'extraElementen': None,
                            'registratie': {
                                'datumAanvang': '20181101',
                                'datumEinde': None,
                                'soortMutatie': None,
                                'registratieTijdstip': '20181101162418910',
                                'registratieTijdstipNoValue': None
                            },
                            'sbiCode': {
                                'code': '01132',
                                'omschrijving': 'Teelt van groenten in de volle grond',
                                'referentieType': 'ActiviteitCode'
                            },
                            'isHoofdactiviteit': {
                                'code': 'J',
                                'omschrijving': 'Ja',
                                'referentieType': 'geenRT'
                            },
                            'volgorde': None
                        }
                    ],
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
                    'wordtUitgeoefendIn': [
                        {
                            'extraElementen': None,
                            'relatieRegistratie': {
                                'datumAanvang': '20181101',
                                'datumEinde': None,
                                'soortMutatie': None,
                                'registratieTijdstip': '20181101162418910',
                                'registratieTijdstipNoValue': None
                            },
                            'commercieleVestiging': {
                                'vestigingsnummer': '12344450234',
                            }
                        },
                        {
                            'extraElementen': None,
                            'relatieRegistratie': {
                                'datumAanvang': '20181101',
                                'datumEinde': None,
                                'soortMutatie': None,
                                'registratieTijdstip': '20181101162418910',
                                'registratieTijdstipNoValue': None
                            },
                            'commercieleVestiging': {
                                'vestigingsnummer': '12344450235',
                            }
                        },
                    ],
                    'isEenManifestatieVan': None,
                    'isOvergenomenVan': None,
                    'isOvergedragenNaar': None
                }
            },
            'wordtGeleidVanuit': {
                'extraElementen': None,
                'commercieleVestiging': None,
                'nietCommercieleVestiging': {
                    'extraElementen': None,
                    'registratie': {
                        'datumAanvang': '20181101',
                        'datumEinde': None,
                        'soortMutatie': None,
                        'registratieTijdstip': '20181101162418910',
                        'registratieTijdstipNoValue': None
                    },
                    'vestigingsnummer': '123456789',
                },
            },
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
            'heeft_hoofdvestiging': {
                'bronwaarde': '123456789'
            },
            'heeft_sbi_activiteiten_voor_onderneming': [
                {'bronwaarde': '01131'},
                {'bronwaarde': '01132'},
            ],
            'heeft_sbi_activiteiten_voor_maatschappelijke_activiteit': [
                {'bronwaarde': '01133'},
                {'bronwaarde': '01134'},
            ],
            'wordt_uitgeoefend_in_commerciele_vestiging': [
                {'bronwaarde': '12344450234'},
                {'bronwaarde': '12344450235'},
            ],
            'wordt_uitgeoefend_in_niet_commerciele_vestiging': [
                {'bronwaarde': '12344450236'},
                {'bronwaarde': '12344450237'},
            ],
            'heeft_bezoekadres': {
                'bronwaarde': 'Amstel 1 Amsterdam',
            },
            'heeft_postadres': {
                'bronwaarde': 'Amstel 1 Amsterdam',
            },
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
