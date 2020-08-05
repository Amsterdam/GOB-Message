from unittest import TestCase
from unittest.mock import patch

from gobmessage.hr.endpoint import hr_endpoint, MESSAGE_EXCHANGE, HR_MESSAGE_KEY


class TestEndpoint(TestCase):

    @patch("gobmessage.hr.endpoint.publish")
    @patch("gobmessage.hr.endpoint.request")
    @patch("gobmessage.hr.endpoint.Response", lambda x: x)
    def test_hr_endpoint(self, mock_request, mock_publish):

        mock_request.data = b'Some data'
        self.assertEqual('OK. Message received. Thank you, good bye.', hr_endpoint())
        mock_publish.assert_called_with(MESSAGE_EXCHANGE, HR_MESSAGE_KEY, {'contents': 'Some data'})
