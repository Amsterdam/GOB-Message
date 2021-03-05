from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from freezegun import freeze_time

from gobmessage.hr.kvk.message import (IMPORT_OBJECT, KvkUpdateMessage, KvkUpdateMessageProcessor, MESSAGE_EXCHANGE,
                                       UPDATE_OBJECT_COMPLETE_KEY, UpdateObject, kvk_message_handler)


@patch("gobmessage.hr.kvk.message.KvkDataService", MagicMock())
class TestKvkUpdateMessageProcessor(TestCase):

    def test_process(self):
        message = KvkUpdateMessage()
        message.kvk_nummer = None
        message.vestigingsnummer = None

        p = KvkUpdateMessageProcessor()
        p._process_inschrijving = MagicMock()
        p._process_vestiging = MagicMock()

        self.assertEqual([], p.process(message))

        message.kvk_nummer = 123
        message.vestigingsnummer = 456
        p._process_inschrijving.return_value = [1, 2]
        p._process_vestiging.return_value = [3, 4]

        self.assertEqual([1, 2, 3, 4], p.process(message))
        p._process_inschrijving.assert_called_with(p.dataservice.ophalen_inschrijving_by_kvk_nummer.return_value)
        p._process_vestiging.assert_called_with(p.dataservice.ophalen_vestiging_by_vestigingsnummer.return_value)
        p.dataservice.ophalen_inschrijving_by_kvk_nummer.assert_called_with(123)
        p.dataservice.ophalen_vestiging_by_vestigingsnummer.assert_called_with(456)

    def test_process_inschrijving(self):
        p = KvkUpdateMessageProcessor()
        p._process_entity = MagicMock()

        class TestMapper:
            pass

        p.inschrijving_collections = {
            'maatschappelijkeactiviteiten': TestMapper,
            'some_other': TestMapper,
        }

        res = p._process_inschrijving({'product': {'some': 'inschrijving'}})
        self.assertEqual([p._process_entity.return_value, p._process_entity.return_value], res)

        p._process_entity.assert_called_with({'some': 'inschrijving'}, ANY)
        call_args = p._process_entity.call_args
        self.assertIsInstance(call_args[0][1], TestMapper)

    def test_process_vestiging(self):
        p = KvkUpdateMessageProcessor()
        p._process_entity = MagicMock()
        p.vestiging_collections = {}

        # No mappings
        res = p._process_vestiging({'product': {'some': 'inschrijving'}})
        self.assertEqual([], res)
        p._process_entity.assert_not_called()

        # With mapping
        p.vestiging_collections = {'testobj': MagicMock}
        res = p._process_vestiging({'product': {'some': 'inschrijving'}})
        self.assertEqual([p._process_entity.return_value], res)

    def test_process_entity(self):
        p = KvkUpdateMessageProcessor()
        p._start_workflow = MagicMock()
        mapper = MagicMock()

        res = p._process_entity({'some': 'source'}, mapper)
        self.assertIsInstance(res, UpdateObject)
        self.assertEqual(res.catalogue, mapper.catalogue)
        self.assertEqual(res.collection, mapper.collection)
        self.assertEqual(res.entity_id, mapper.get_id.return_value)
        mapper.get_id.assert_called_with(mapper.map.return_value)
        mapper.map.assert_called_with({'some': 'source'})
        p._start_workflow.assert_called_with(res, mapper.map.return_value, mapper)

    @patch("gobmessage.hr.kvk.message.start_workflow")
    def test_start_workflow(self, mock_start_workflow):
        p = KvkUpdateMessageProcessor()
        update_object = UpdateObject()
        update_object.catalogue = 'the cat'
        update_object.collection = 'the coll'
        update_object.entity_id = 'the entity id'

        mapper = MagicMock()

        with freeze_time('2021-01-21 13:43:00'):
            p._start_workflow(update_object, {'some': 'entity'}, mapper)

        mock_start_workflow.assert_called_with({
            'workflow_name': IMPORT_OBJECT,
        }, {
            'header': {
                'catalogue': 'the cat',
                'entity': 'the coll',
                'entity_id': 'the entity id',
                'entity_id_attr': mapper.entity_id,
                'source': 'KvK',
                'application': 'KvkDataService',
                'timestamp': '2021-01-21T13:43:00',
                'version': mapper.version,
                'on_workflow_complete': {
                    'exchange': MESSAGE_EXCHANGE,
                    'key': UPDATE_OBJECT_COMPLETE_KEY,
                },
            },
            'contents': {
                'some': 'entity',
            }
        })


class TestMessage(TestCase):

    @patch("gobmessage.hr.kvk.message.KvkUpdateMessageProcessor")
    @patch("gobmessage.hr.kvk.message.DatabaseSession")
    @patch("gobmessage.hr.kvk.message.KvkUpdateMessageRepository")
    @patch("gobmessage.hr.kvk.message.UpdateObjectRepository")
    def test_kvk_message_handler(self, mock_uo_repo, mock_um_repo, mock_session, mock_processor):
        mocked_message = MagicMock()
        mocked_message.is_processed = False
        mock_um_repo.return_value.get.return_value = mocked_message

        kvk_message_handler({'message_id': 42})

        mock_um_repo.assert_called_with(mock_session.return_value.__enter__.return_value)
        mock_um_repo.return_value.get.assert_called_with(42)

        mock_processor.return_value.process.assert_called_with(mocked_message)
        mock_uo_repo.assert_called_with(mock_session.return_value.__enter__.return_value)
        mock_uo_repo.return_value.save_all.assert_called_with(mock_processor.return_value.process.return_value)

        mock_um_repo.return_value.save.assert_called_with(mocked_message)
        self.assertTrue(mocked_message.is_processed)
