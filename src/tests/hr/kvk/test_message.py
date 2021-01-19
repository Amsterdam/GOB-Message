from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from gobmessage.hr.kvk.message import kvk_message_handler


class TestMessage(TestCase):

    @patch("gobmessage.hr.kvk.message.DatabaseSession")
    @patch("gobmessage.hr.kvk.message.KvkDataService")
    @patch("gobmessage.hr.kvk.message.KvkUpdateMessages")
    @patch("builtins.print")
    def test_kvk_message_handler(self, mock_print, mock_messages, mock_data_service, mock_session):
        mocked_message = MagicMock()
        mock_messages.return_value.get.return_value = mocked_message

        # Case with kvk nummer and vestigingsnummer
        kvk_message_handler({'message_id': 42})

        mock_data_service().ophalen_inschrijving_by_kvk_nummer.assert_called_with(mocked_message.kvk_nummer)
        mock_data_service().ophalen_vestiging_by_vestigingsnummer.assert_called_with(mocked_message.vestigingsnummer)
        mock_print.assert_has_calls([
            call("INSCHRIJVING"),
            call(mock_data_service().ophalen_inschrijving_by_kvk_nummer()),
            call("VESTIGING"),
            call(mock_data_service().ophalen_vestiging_by_vestigingsnummer()),
        ])
        mock_messages.assert_called_with(mock_session.return_value.__enter__.return_value)
        mock_messages.return_value.get.assert_called_with(42)

        # Case without kvk nummer and vestigingsnummer
        mocked_message.kvk_nummer = None
        mocked_message.vestigingsnummer = None

        kvk_message_handler({'message_id': 42})

        mock_print.assert_has_calls([
            call("No new data retrieved because 'KvK nummer' was not found in the received message"),
            call("No new data retrieved because 'Vestiging' was not found in the received message"),
        ])
