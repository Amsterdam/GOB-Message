from unittest import TestCase
from unittest.mock import MagicMock, call

from gobmessage.database.repository import KvkUpdateMessages, KvkUpdateMessage


class TestKvkUpdateMessages(TestCase):

    def test_get(self):
        session = MagicMock()
        k = KvkUpdateMessages(session)

        self.assertEqual(session.query.return_value.get.return_value, k.get(42))
        session.assert_has_calls([
            call.query(KvkUpdateMessage),
            call.query().get(42)
        ])

    def test_save(self):
        session = MagicMock()
        k = KvkUpdateMessages(session)
        message = KvkUpdateMessage()

        self.assertEqual(message, k.save(message))
        session.assert_has_calls([
            call.add(message),
            call.flush(),
        ])
