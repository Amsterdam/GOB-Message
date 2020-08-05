from unittest import TestCase
from unittest.mock import patch, call

from gobmessage.hr.message import hr_message_handler


class TestMessage(TestCase):

    @patch("builtins.print")
    def test_hr_message_handler(self, mock_print):
        hr_message_handler({'some': 'message'})

        mock_print.assert_has_calls([
            call("Received message from queue. Handle here"),
            call({'some': 'message'}),
        ])