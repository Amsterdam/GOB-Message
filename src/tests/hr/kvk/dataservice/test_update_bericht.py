from unittest import TestCase
from unittest.mock import MagicMock, patch

from gobmessage.hr.kvk.dataservice.update_bericht import KvkUpdateBericht


@patch("gobmessage.hr.kvk.dataservice.update_bericht.ElementTree", MagicMock())
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
