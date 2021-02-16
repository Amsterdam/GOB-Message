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
