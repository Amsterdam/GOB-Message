from unittest import TestCase

from gobmessage.database.model import KvkUpdateMessage


class TestKvkUpdateMessage(TestCase):

    def test_repr(self):
        message = KvkUpdateMessage()
        message.id = 42

        self.assertEqual("<KvkUpdateMessage 42>", str(message))
