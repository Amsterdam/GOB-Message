from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from gobmessage.__main__ import run_message_thread, MESSAGE_EXCHANGE, HR_MESSAGE_QUEUE, HR_MESSAGE_KEY, \
    SERVICEDEFINITION


class TestMain(TestCase):

    @patch("gobmessage.__main__.create_queue_with_binding")
    @patch("gobmessage.__main__.messagedriven_service")
    def test_run_message_thread(self, mock_messagedriven_service, mock_create_queue):
        mocks = MagicMock()
        mocks.attach_mock(mock_create_queue, 'create_queue')
        mocks.attach_mock(mock_messagedriven_service, 'messagedriven_service')

        run_message_thread()

        mocks.assert_has_calls([
            call.create_queue(exchange=MESSAGE_EXCHANGE, queue=HR_MESSAGE_QUEUE, key=HR_MESSAGE_KEY),
            call.messagedriven_service(SERVICEDEFINITION, "Message")
        ])

    @patch("gobmessage.__main__.Thread")
    @patch("gobmessage.__main__.run_api")
    def test_main_entry(self, mock_run, mock_thread):
        from gobmessage import __main__ as module
        with patch.object(module, "__name__", "__main__"):
            module.init()

            mock_thread.assert_called_with(target=module.run_message_thread)
            mock_thread().start.assert_called_once()
            mock_run.assert_called_once()
