from unittest import TestCase
from unittest.mock import patch


class TestMain(TestCase):

    @patch("gobmessage.__main__.run")
    def test_main_entry(self, mock_run):
        from gobmessage import __main__ as module
        with patch.object(module, "__name__", "__main__"):
            module.init()
            mock_run.assert_called_once()
