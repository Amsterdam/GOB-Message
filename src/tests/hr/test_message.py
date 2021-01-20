from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from gobmessage.hr.message import hr_message_handler, KvkUpdateBericht


@patch("gobmessage.hr.message.ElementTree", MagicMock())
class TestKvkUpdateBericht(TestCase):

    def test_get_methods(self):
        message = KvkUpdateBericht('some xml string')

        testcases = [
            (
                "get_kvk_nummer",
                "."
                "/gebeurtenisinhoud"
                "/{http://schemas.kvk.nl/schemas/hrip/update/2018/01}UpdateBericht"
                "/{http://schemas.kvk.nl/schemas/hrip/bericht/2018/01}heeftBetrekkingOp"
                "/{http://schemas.kvk.nl/schemas/hrip/bericht/2018/01}kvkNummer"),
            (
                "get_vestigingsnummer",
                "."
                "/gebeurtenisinhoud"
                "/{http://schemas.kvk.nl/schemas/hrip/update/2018/01}UpdateBericht"
                "/{http://schemas.kvk.nl/schemas/hrip/bericht/2018/01}heeftBetrekkingOp"
                "/{http://schemas.kvk.nl/schemas/hrip/bericht/2018/01}wordtUitgeoefendIn"
                "/{http://schemas.kvk.nl/schemas/hrip/bericht/2018/01}vestigingsnummer"
            ),
        ]

        for method_name, xpath in testcases:
            message.xmltree.find.return_value = MagicMock()

            # Should return result
            res = getattr(message, method_name)()
            message.xmltree.find.assert_called_with(xpath)
            self.assertEqual(res, message.xmltree.find().text)

            # No result
            message.xmltree.find.return_value = None
            res = getattr(message, method_name)()
            self.assertIsNone(res)


class TestMessage(TestCase):

    @patch("gobmessage.hr.message.DatabaseSession")
    @patch("gobmessage.hr.message.KvkDataService")
    @patch("gobmessage.hr.message.KvkUpdateMessages")
    @patch("builtins.print")
    def test_hr_message_handler(self, mock_print, mock_messages, mock_data_service, mock_session):
        mocked_message = MagicMock()
        mock_messages.return_value.get.return_value = mocked_message

        # Case with kvk nummer and vestigingsnummer
        hr_message_handler({'message_id': 42})

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

        hr_message_handler({'message_id': 42})

        mock_print.assert_has_calls([
            call("No new data retrieved because 'KvK nummer' was not found in the received message"),
            call("No new data retrieved because 'Vestiging' was not found in the received message"),
        ])
