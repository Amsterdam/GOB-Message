from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from gobmessage.api import get_flask_app, _health, _secure_route, GOB_HR_ADMIN, inschrijving_endpoint, vestiging_endpoint


class TestAPI(TestCase):

    def test_health(self):
        self.assertEqual('Connectivity OK', _health())

    @patch("gobmessage.api.is_secured_request")
    @patch("gobmessage.api.extract_roles")
    def test_secure_route(self, mock_extract_roles, mock_is_secured_request):
        mock_request = MagicMock()
        mock_is_secured_request.return_value = False
        mock_extract_roles.return_value = ['role a', 'role b']

        view_func = MagicMock()
        view_func.__name__ = "viewfuncname"
        with patch("gobmessage.api.request", mock_request):
            secure_route = _secure_route(view_func)
            self.assertEqual(("Forbidden", 403), secure_route())

            mock_is_secured_request.return_value = True
            self.assertEqual(("Forbidden", 403), secure_route())

            mock_extract_roles.return_value = ['role a', 'role b', GOB_HR_ADMIN]
            self.assertEqual(view_func.return_value, secure_route())

    @patch("gobmessage.api.CORS", MagicMock())
    @patch("gobmessage.api._secure_route")
    @patch("gobmessage.api.Flask")
    def test_get_flask_app(self, mock_flask, mock_secure_route):
        mock_app = MagicMock()
        mock_flask.return_value = mock_app
        app = get_flask_app()
        mock_flask.assert_called()
        mock_app.route.assert_called()
        mock_secure_route.assert_has_calls([
            call(inschrijving_endpoint),
            call(vestiging_endpoint)
        ])
