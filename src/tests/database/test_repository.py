from unittest import TestCase
from unittest.mock import MagicMock, call

from gobmessage.database.repository import (
    KvkUpdateMessageRepository,
    KvkUpdateMessage,
    UpdateObjectRepository,
    UpdateObject
)


class TestKvkUpdateMessageRepository(TestCase):
    """Tests parent Repository class as well as KvkUpdateMessageRepository

    """

    def test_get(self):
        session = MagicMock()
        k = KvkUpdateMessageRepository(session)

        self.assertEqual(session.query.return_value.get.return_value, k.get(42))
        session.assert_has_calls([
            call.query(KvkUpdateMessage),
            call.query().get(42)
        ])

    def test_save(self):
        session = MagicMock()
        k = KvkUpdateMessageRepository(session)
        message = KvkUpdateMessage()

        self.assertEqual(message, k.save(message))
        session.assert_has_calls([
            call.add(message),
            call.flush(),
        ])

    def test_save_all(self):
        objs = ['a', 'b']
        session = MagicMock()
        k = KvkUpdateMessageRepository(session)
        self.assertEqual(objs, k.save_all(objs))

        session.assert_has_calls([
            call.add('a'),
            call.add('b'),
            call.flush(),
        ])


class TestUpdateObjectRepository(TestCase):

    def test_get_active_for_entity_id(self):
        session = MagicMock()
        u = UpdateObjectRepository(session)

        res = u.get_active_for_entity_id(0, 'cat', 'coll', 'entity_id')
        self.assertEqual(session.query.return_value.filter_by.return_value.first.return_value, res)
        session.assert_has_calls([
            call.query(UpdateObject),
            call.query().filter_by(
                update_message_id=0,
                catalogue='cat',
                collection='coll',
                entity_id='entity_id',
                status=UpdateObject.STATUS_STARTED
            ),
            call.query().filter_by().first()
        ])
