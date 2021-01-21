from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from gobmessage.app import KVK_MESSAGE_KEY, KVK_MESSAGE_QUEUE, MESSAGE_EXCHANGE, SERVICEDEFINITION, get_app, run, \
    run_message_thread, UPDATE_OBJECT_COMPLETE_KEY, UPDATE_OBJECT_COMPLETE_QUEUE, update_object_complete_handler


class TestApp(TestCase):

    @patch("gobmessage.app.UpdateObjectRepository")
    @patch("gobmessage.app.DatabaseSession")
    def test_update_object_complete_handler(self, mock_session, mock_repo):

        msg = {
            'header': {
                'catalogue': 'CAT',
                'entity': 'ENT',
                'entity_id': 'entity id',
            }
        }

        res = update_object_complete_handler(msg)
        self.assertEqual(msg, res)
        mocked_session = mock_session.return_value.__enter__.return_value
        mock_repo.assert_called_with(mocked_session)

        mock_repo.return_value.get_active_for_entity_id.assert_called_with('CAT', 'ENT', 'entity id')

        mocked_entity = mock_repo.return_value.get_active_for_entity_id.return_value
        self.assertEqual(mock_repo.return_value.object_class.STATUS_ENDED, mocked_entity.status)
        mock_repo.return_value.save.assert_called_with(mocked_entity)

    @patch("gobmessage.app.os._exit")
    @patch("gobmessage.app.messagedriven_service")
    @patch("gobmessage.app.create_queue_with_binding")
    def test_run_message_thread(self, mock_create_queue, mock_messagedriven_service, mock_os_exit):
        mock = MagicMock()
        mock.attach_mock(mock_create_queue, 'create_queue')
        mock.attach_mock(mock_messagedriven_service, 'messagedriven_service')

        run_message_thread()

        mock.assert_has_calls([
            call.create_queue(exchange=MESSAGE_EXCHANGE, queue=KVK_MESSAGE_QUEUE, key=KVK_MESSAGE_KEY),
            call.create_queue(exchange=MESSAGE_EXCHANGE, queue=UPDATE_OBJECT_COMPLETE_QUEUE,
                              key=UPDATE_OBJECT_COMPLETE_KEY),
            call.messagedriven_service(SERVICEDEFINITION, "Message")
        ])

        mock_messagedriven_service.side_effect = Exception
        run_message_thread()

    @patch("gobmessage.app.Thread")
    @patch("gobmessage.app.get_flask_app")
    def test_get_app(self, mock_flask_app, mock_thread):
        self.assertEqual(mock_flask_app(), get_app())

        mock_thread.assert_called_with(target=run_message_thread)
        mock_thread().start.assert_called_once()

    @patch("gobmessage.app.GOB_MESSAGE_PORT", 1234)
    @patch("gobmessage.app.connect")
    @patch("gobmessage.app.get_app")
    def test_run(self, mock_get_app, mock_connect):
        mock_app = MagicMock()
        mock_get_app.return_value = mock_app
        run()
        mock_app.run.assert_called_with(port=1234)
        mock_connect.assert_called_once()
