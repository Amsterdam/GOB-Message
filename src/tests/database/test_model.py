from unittest import TestCase
from unittest.mock import MagicMock

from gobmessage.database.model import KvkUpdateMessage, UpdateObject


class TestKvkUpdateMessage(TestCase):

    def test_repr(self):
        message = KvkUpdateMessage()
        message.id = 42

        self.assertEqual("<KvkUpdateMessage 42>", str(message))

    def test_get_next_queued_update_object(self):
        message = KvkUpdateMessage()

        uo1 = MagicMock()
        uo2 = MagicMock()
        uo3 = MagicMock()
        uo4 = MagicMock()
        uo3.status = UpdateObject.STATUS_QUEUED
        uo4.status = UpdateObject.STATUS_QUEUED

        message.update_objects = [uo1, uo2, uo3, uo4]
        self.assertEqual(uo3, message.get_next_queued_update_object())

        message.update_objects = []
        self.assertIsNone(message.get_next_queued_update_object())


class TestUpdateObject(TestCase):

    def test_repr(self):
        u = UpdateObject()
        u.catalogue = 'cat'
        u.collection = 'coll'
        u.entity_id = 42

        self.assertEqual("<UpdateObject cat coll 42>", str(u))
