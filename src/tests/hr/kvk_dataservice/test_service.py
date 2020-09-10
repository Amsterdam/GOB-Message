import freezegun

from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobmessage.hr.kvk_dataservice.service import KvkDataService


class TestKvkDataService(TestCase):

    @patch("gobmessage.hr.kvk_dataservice.service.HR_CERTFILE", 'certfile.crt')
    @patch("gobmessage.hr.kvk_dataservice.service.HR_KEYFILE", 'keyfile.key')
    @patch("gobmessage.hr.kvk_dataservice.service.KVK_DATASERVICE_ADDRESS", 'https://kvkdataservice')
    @patch("gobmessage.hr.kvk_dataservice.service.requests.Session")
    @patch("gobmessage.hr.kvk_dataservice.service.Transport")
    @patch("gobmessage.hr.kvk_dataservice.service.Client")
    @patch("gobmessage.hr.kvk_dataservice.service.KvkDataServiceBinarySignature")
    def test_get_client(self, mock_signature, mock_client, mock_transport, mock_session):
        service = KvkDataService()
        mock_client.return_value.service._binding_options = {}
        res = service._get_client()

        mock_transport.assert_called_with(session=mock_session())
        mock_signature.assert_called_with('keyfile.key', 'certfile.crt')
        mock_client.assert_called_with(
            'http://schemas.kvk.nl/contracts/kvk/dataservice/catalogus/2015/02/KVK-KvKDataservice.wsdl',
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

    def test_make_request(self):
        service = KvkDataService()
        service._get_client = MagicMock()
        service._generate_reference = MagicMock()

        res = service._make_request('someAction', kwarg1='value1', kwarg2='value2')

        service._get_client().service.someAction.assert_called_with(
            klantreferentie=service._generate_reference(),
            kwarg1='value1',
            kwarg2='value2'
        )
        self.assertEqual(service._get_client().service.someAction(), res)

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
