from unittest import TestCase
from unittest.mock import patch, MagicMock

from gobmessage.api import get_app, run, _health

class TestAPI(TestCase):

    def test_health(self):
        self.assertEqual('Connectivity OK', _health())

    @patch("gobmessage.api.CORS", MagicMock())
    @patch("gobmessage.api.Flask")
    def test_get_app(self, mock_flask):
        mock_app = MagicMock()
        mock_flask.return_value = mock_app
        app = get_app()
        mock_flask.assert_called()
        mock_app.route.assert_called()

    @patch("gobmessage.api.GOB_MESSAGE_PORT", 1234)
    @patch("gobmessage.api.get_app")
    def test_run(self, mock_get_app):
        mock_app = MagicMock()
        mock_get_app.return_value = mock_app
        run()
        mock_app.run.assert_called_with(port=1234)
