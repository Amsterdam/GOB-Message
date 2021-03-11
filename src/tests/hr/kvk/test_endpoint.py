from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobmessage.hr.kvk.endpoint import kvk_endpoint, MESSAGE_EXCHANGE, KVK_MESSAGE_KEY


class TestEndpoint(TestCase):

    @patch("gobmessage.hr.kvk.endpoint.DatabaseSession")
    @patch("gobmessage.hr.kvk.endpoint.KvkUpdateMessageRepository")
    @patch("gobmessage.hr.kvk.endpoint.KvkUpdateMessage")
    @patch("gobmessage.hr.kvk.endpoint.KvkUpdateBericht")
    @patch("gobmessage.hr.kvk.endpoint.Response", lambda x: x)
    def test_kvk_endpoint(self, mock_bericht, mock_message, mock_repo, mock_session):
        mock_request = MagicMock()
        mock_request.data = b'Some data'
        mock_publish = MagicMock()

        with patch("gobmessage.hr.kvk.endpoint.publish", mock_publish), \
            patch("gobmessage.hr.kvk.endpoint.request", mock_request):

            self.assertEqual('OK. Message received. Thank you, good bye.', kvk_endpoint())

            mock_bericht.assert_called_with('Some data')

            mock_bericht_rv = mock_bericht.return_value
            mock_message_rv = mock_message.return_value
            self.assertEqual(mock_bericht_rv.get_kvk_nummer.return_value, mock_message_rv.kvk_nummer)
            self.assertEqual('Some data', mock_message_rv.message)

            mock_repo.assert_called_with(mock_session().__enter__())
            mock_repo.return_value.save.assert_called_with(mock_message_rv)

            mock_publish.assert_called_with(MESSAGE_EXCHANGE, KVK_MESSAGE_KEY, {'message_id': mock_repo.return_value.save.return_value.id})
