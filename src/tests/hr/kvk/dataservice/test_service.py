import freezegun
from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobmessage.hr.kvk.dataservice.service import KvkDataService


class TestKvkDataService(TestCase):

    @patch("gobmessage.hr.kvk.dataservice.service.HR_CERTFILE", 'certfile.crt')
    @patch("gobmessage.hr.kvk.dataservice.service.HR_KEYFILE", 'keyfile.key')
    @patch("gobmessage.hr.kvk.dataservice.service.KVK_DATASERVICE_ADDRESS", 'https://kvkdataservice')
    @patch("gobmessage.hr.kvk.dataservice.service.requests.Session")
    @patch("gobmessage.hr.kvk.dataservice.service.InMemoryCache")
    @patch("gobmessage.hr.kvk.dataservice.service.Transport")
    @patch("gobmessage.hr.kvk.dataservice.service.Client")
    @patch("gobmessage.hr.kvk.dataservice.service.KvkDataServiceBinarySignature")
    def test_get_client(self, mock_signature, mock_client, mock_transport, mock_cache, mock_session):
        service = KvkDataService()
        mock_client.return_value.service._binding_options = {}
        res = service._get_client()

        mock_transport.assert_called_with(session=mock_session(), cache=mock_cache(),
                                          operation_timeout=service.operation_timeout)
        mock_signature.assert_called_with('keyfile.key', 'certfile.crt')
        mock_client.assert_called_with(
            wsdl='http://schemas.kvk.nl/contracts/kvk/dataservice/catalogus/2015/02/KVK-KvKDataservice.wsdl',
            wsse=mock_signature(),
            transport=mock_transport()
        )

        self.assertEqual(mock_client(), res)
        self.assertEqual('https://kvkdataservice', mock_client().service._binding_options['address'])
        self.assertEqual(('certfile.crt', 'keyfile.key'), mock_session().cert)

    def test_generate_reference(self):
        service = KvkDataService()
        with freezegun.freeze_time('2020-09-01 19:00:03'):
            self.assertEqual('GOB-20200901190003000000', service._generate_reference())

    def test_unpack_raw_elements(self):
        service = KvkDataService()

        a_elm = MagicMock()
        a_elm.tag = '{somenamespace}a'
        a_elm.text = 8
        k_elm = MagicMock()
        k_elm.tag= '{thenamespace}k'
        k_elm.text = 55
        z_elm = MagicMock()
        z_elm.tag = '{http://some/other/namespace}z'
        z_elm.text = 9
        in_dict = {
            'a': 1,
            'b': 2,
            'c': ['d', 'e', 'f'],
            'g': {
                'h': 3,
                'i': [{
                    'j': 4,
                    'k': 5,
                    '_raw_elements': [k_elm],
                }, {
                    'l': 6,
                    'm': 7,
                }],
                'n': {
                    'o': 10,
                    'p': 11,
                }
            },
            '_raw_elements': [
                a_elm,
                z_elm,
            ]
        }

        expected = {
            'a': 8,
            'b': 2,
            'c': ['d', 'e', 'f'],
            'g': {
                'h': 3,
                'i': [{
                    'j': 4,
                    'k': 55,
                }, {
                    'l': 6,
                    'm': 7,
                }],
                'n': {
                    'o': 10,
                    'p': 11,
                }
            },
            'z': 9,
        }
        self.assertEqual(expected, service._unpack_raw_elements(in_dict))

    @patch("gobmessage.hr.kvk.dataservice.service.serialize_object")
    def test_make_request(self, mock_serialize):
        service = KvkDataService()
        service._get_client = MagicMock()
        service._generate_reference = MagicMock()
        service._unpack_raw_elements = MagicMock()

        res = service._make_request('someAction', kwarg1='value1', kwarg2='value2')

        service._get_client().service.someAction.assert_called_with(
            klantreferentie=service._generate_reference(),
            kwarg1='value1',
            kwarg2='value2'
        )
        mock_serialize.assert_called_with(service._get_client().service.someAction())
        service._unpack_raw_elements.assert_called_with(mock_serialize.return_value)
        self.assertEqual(service._unpack_raw_elements.return_value, res)

    def test_request_methods(self):
        testcases = [
            ('ophalen_inschrijving_by_kvk_nummer', 'ophalenInschrijving', 'kvkNummer'),
            ('ophalen_inschrijving_by_rsin', 'ophalenInschrijving', 'rsin'),
            ('ophalen_vestiging_by_vestigingsnummer', 'ophalenVestiging', 'vestigingsnummer'),
            ('ophalen_vestiging_by_kvk_nummer', 'ophalenVestiging', 'kvkNummer'),
            ('ophalen_vestiging_by_rsin', 'ophalenVestiging', 'rsin'),
        ]

        service = KvkDataService()
        service._make_request = MagicMock()

        for method_name, action, kwarg_name in testcases:
            method = getattr(service, method_name)

            res = method('some argument')

            # Assert make_request is called with the right kwarg name and the provided argument, and the result is
            # returned
            service._make_request.assert_called_with(action, **{kwarg_name: 'some argument'})
            self.assertEqual(service._make_request(), res)
