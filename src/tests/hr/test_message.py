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

    @patch("gobmessage.hr.message.KvkDataService")
    @patch("gobmessage.hr.message.KvkUpdateBericht")
    @patch("builtins.print")
    def test_hr_message_handler(self, mock_print, mock_bericht, mock_data_service):
        hr_message_handler({'contents': 'message'})

        mock_bericht.assert_called_with('message')
        mock_data_service().ophalen_inschrijving_by_kvk_nummer.assert_called_with(mock_bericht().get_kvk_nummer())
        mock_data_service().ophalen_vestiging_by_vestigingsnummer.assert_called_with(
            mock_bericht().get_vestigingsnummer())

        mock_print.assert_has_calls([
            call("INSCHRIJVING"),
            call(mock_data_service().ophalen_inschrijving_by_kvk_nummer()),
            call("VESTIGING"),
            call(mock_data_service().ophalen_vestiging_by_vestigingsnummer()),
        ])
