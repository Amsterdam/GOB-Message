import unittest
from unittest import mock


class TestWsgi(unittest.TestCase):

    @mock.patch('gobmessage.api.get_app')
    def test_wsgi(self, mock_get_app):
        import gobmessage.wsgi
        mock_get_app.assert_called()
