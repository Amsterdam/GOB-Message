from unittest import TestCase
from unittest.mock import patch

from gobmessage.hr.endpoint import hr_endpoint


class TestEndpoint(TestCase):

    @patch("gobmessage.hr.endpoint.request")
    @patch("gobmessage.hr.endpoint.Response", lambda x: x)
    def test_hr_endpoint(self, mock_request):

        mock_request.data = b'Some data'
        self.assertEqual('OK: Some data', hr_endpoint())
