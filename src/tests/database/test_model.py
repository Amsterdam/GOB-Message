from unittest import TestCase

from gobmessage.database.model import KvkUpdateMessage, UpdateObject


class TestKvkUpdateMessage(TestCase):

    def test_repr(self):
        message = KvkUpdateMessage()
        message.id = 42

        self.assertEqual("<KvkUpdateMessage 42>", str(message))


class TestUpdateObject(TestCase):

    def test_repr(self):
        u = UpdateObject()
        u.catalogue = 'cat'
        u.collection = 'coll'
        u.entity_id = 42

        self.assertEqual("<UpdateObject cat coll 42>", str(u))
