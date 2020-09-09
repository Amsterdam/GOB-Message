import freezegun

from zeep import ns

from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from gobmessage.hr.kvk_dataservice.binary_signature import KvkDataServiceBinarySignature


@patch("builtins.open", MagicMock())  # To avoid loading non-existing certificates in the tests
class TestKvkDataServiceBinarySignature(TestCase):

    @patch("gobmessage.hr.kvk_dataservice.binary_signature.utils")
    def test_add_timestamp(self, mock_utils):
        signature = KvkDataServiceBinarySignature('key', 'cert')

        envelope = MagicMock()

        with freezegun.freeze_time('2020-09-01 13:00:00'):
            signature._add_timestamp(envelope)
        mock_security_header = mock_utils.get_security_header()

        mock_security_header.append.assert_called_with(mock_utils.WSU())
        mock_utils.assert_has_calls([
            call.get_security_header(envelope),
            call.WSU('Timestamp'),
            call.WSU('Created', '2020-09-01T13:00:00Z'),
            call.WSU('Timestamp').append(mock_utils.WSU()),
            call.WSU('Expires', '2020-09-01T21:20:00Z'),
            call.WSU('Timestamp').append(mock_utils.WSU()),
        ])

    @patch("gobmessage.hr.kvk_dataservice.binary_signature.utils")
    def test_fix_wsa_headers(self, mock_utils):
        signature = KvkDataServiceBinarySignature('key', 'cert')
        mock_utils.get_or_create_header = MagicMock()

        to_elm = MagicMock()
        message_id_elm = MagicMock()
        message_id_elm.text = 'urn:uuid:the-message-id'

        def mock_find(elm):
            if elm == '{http://www.w3.org/2005/08/addressing}To':
                return to_elm
            elif elm == '{http://www.w3.org/2005/08/addressing}MessageID':
                return message_id_elm
            else:
                raise Exception(f"Not expected: {elm}")

        mock_utils.get_or_create_header().find = mock_find

        signature._fix_wsa_headers(MagicMock())

        # 'urn:' prefix should be removed from MessageID and To element should be set correctly
        self.assertEqual('http://es.kvk.nl/kvk-dataservicePP/2015/02', to_elm.text)
        self.assertEqual('uuid:the-message-id', message_id_elm.text)

    @patch("gobmessage.hr.kvk_dataservice.binary_signature._make_sign_key")
    @patch("gobmessage.hr.kvk_dataservice.binary_signature._sign_envelope_with_key_binary")
    @patch("gobmessage.hr.kvk_dataservice.binary_signature.xmlsec.SignatureContext")
    @patch("gobmessage.hr.kvk_dataservice.binary_signature.detect_soap_env")
    @patch("gobmessage.hr.kvk_dataservice.binary_signature._sign_node")
    @patch("gobmessage.hr.kvk_dataservice.binary_signature.QName", lambda ns, elm: f"{ns}:{elm}")
    def test_sign_envelope(self,
                           mock_sign_node,
                           mock_detect_soap_env,
                           mock_signature_context,
                           mock_sign_envelope,
                           mock_make_sign_key):

        signature = KvkDataServiceBinarySignature('key', 'cert')
        signature.key_data = 'key_data'
        signature.cert_data = 'cert_data'
        signature.password = 'password'

        mock_detect_soap_env.return_value = 'soapenv'

        envelope = MagicMock()
        signature._sign_envelope(envelope)

        mock_make_sign_key.assert_called_with('key_data', 'cert_data', 'password')
        mock_sign_envelope.assert_called_with(
            envelope,
            mock_make_sign_key(),
            signature.signature_method,
            signature.digest_method
        )

        envelope.assert_has_calls([
            call.find('soapenv:Header'),
            call.find().find(f'{ns.WSSE}:Security'),
            call.find().find().find(f'{ns.DS}:Signature'),
            call.find().find(f'{ns.WSA}:To'),
            call.find().find(f'{ns.WSA}:MessageID'),
            call.find().find(f'{ns.WSA}:Action'),
        ])

        mock_sign_node.assert_has_calls([
            call(mock_signature_context(), envelope.find().find().find(), envelope.find().find(),
                 signature.digest_method),
            call(mock_signature_context(), envelope.find().find().find(), envelope.find().find(),
                 signature.digest_method),
            call(mock_signature_context(), envelope.find().find().find(), envelope.find().find(),
                 signature.digest_method),
        ])

        self.assertEqual(mock_make_sign_key(), mock_signature_context().key)

    def test_apply(self):
        signature = KvkDataServiceBinarySignature('key', 'cert')
        signature._add_timestamp = MagicMock()
        signature._fix_wsa_headers = MagicMock()
        signature._sign_envelope = MagicMock()

        mock = MagicMock()
        mock.attach_mock(signature._add_timestamp, '_add_timestamp')
        mock.attach_mock(signature._fix_wsa_headers, '_fix_wsa_headers')
        mock.attach_mock(signature._sign_envelope, '_sign_envelope')

        envelope = MagicMock()
        headers = MagicMock()

        self.assertEqual((envelope, headers), signature.apply(envelope, headers))

        # Should be called in correct order
        mock.assert_has_calls([
            call._add_timestamp(envelope),
            call._fix_wsa_headers(envelope),
            call._sign_envelope(envelope),
        ])

    def test_verify(self):
        mock_envelope = MagicMock()

        signature = KvkDataServiceBinarySignature('key', 'cert')

        # Nothing should have been done with the envelope
        self.assertEqual([], mock_envelope.mock_calls)
        self.assertEqual(mock_envelope, signature.verify(mock_envelope))
