from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobmessage.hr.endpoint import hr_endpoint, MESSAGE_EXCHANGE, HR_MESSAGE_KEY


class TestEndpoint(TestCase):

    @patch("gobmessage.hr.endpoint.Response", lambda x: x)
    def test_hr_endpoint(self):
        mock_request = MagicMock()
        mock_publish = MagicMock()

        with patch("gobmessage.hr.endpoint.publish", mock_publish), \
            patch("gobmessage.hr.endpoint.request", mock_request):

            mock_request.data = b'Some data'
            self.assertEqual('OK. Message received. Thank you, good bye.', hr_endpoint())
            mock_publish.assert_called_with(MESSAGE_EXCHANGE, HR_MESSAGE_KEY, {'contents': 'Some data'})
