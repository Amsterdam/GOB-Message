from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from freezegun import freeze_time

from gobmessage.hr.kvk.message import (IMPORT_OBJECT, KvkUpdateMessage, KvkUpdateMessageProcessor, MESSAGE_EXCHANGE,
                                       UPDATE_OBJECT_COMPLETE_KEY, UpdateObject, kvk_message_handler,
                                       MaatschappelijkeActiviteitenMapper)


@patch("gobmessage.hr.kvk.message.KvkDataService", MagicMock())
class TestKvkUpdateMessageProcessor(TestCase):

    def test_process(self):
        message = KvkUpdateMessage()
        message.kvk_nummer = 123
        message.vestigingsnummer = 456

        p = KvkUpdateMessageProcessor()
        p._process_inschrijving = MagicMock()

        self.assertEqual(p._process_inschrijving.return_value, p.process(message))
        p._process_inschrijving.assert_called_with(p.dataservice.ophalen_inschrijving_by_kvk_nummer.return_value)
        p.dataservice.ophalen_inschrijving_by_kvk_nummer.assert_called_with(123)

    def test_process_inschrijving(self):
        p = KvkUpdateMessageProcessor()
        process_result = MagicMock()
        p._process_entity = MagicMock(return_value=[process_result])

        class TestMapper:
            pass

        p.inschrijving_entities = {
            'm.a': TestMapper,
            'some_other': TestMapper,
        }

        res = p._process_inschrijving({'product': {'m': {'a': {'some': 'inschrijving'}}}})
        self.assertEqual([process_result], res)

        p._process_entity.assert_called_with({'some': 'inschrijving'}, ANY)
        call_args = p._process_entity.call_args
        self.assertIsInstance(call_args[0][1], TestMapper)

    def test_process_entity(self):
        p = KvkUpdateMessageProcessor()
        p._start_workflow = MagicMock()
        mapper = MagicMock()

        res = p._process_entity({'some': 'source'}, mapper)[0]
        self.assertIsInstance(res, UpdateObject)
        self.assertEqual(res.catalogue, mapper.catalogue)
        self.assertEqual(res.collection, mapper.collection)
        self.assertEqual(res.entity_id, mapper.get_id.return_value)
        mapper.get_id.assert_called_with(mapper.map.return_value)
        mapper.map.assert_called_with({'some': 'source'})
        p._start_workflow.assert_called_with(res, mapper.map.return_value, mapper)

    def test_process_entity_mac(self):
        p = KvkUpdateMessageProcessor()
        p._start_workflow = MagicMock()
        vestigingen_result = [MagicMock(), MagicMock()]
        p._get_vestigingen = MagicMock(return_value=vestigingen_result)
        mapper = MagicMock(spec=MaatschappelijkeActiviteitenMapper)

        res = p._process_entity({'some': 'source'}, mapper)
        self.assertEqual(vestigingen_result, res[1:3])
        p._get_vestigingen.assert_called_with(mapper.get_vestigingsnummers.return_value)

    @patch("gobmessage.hr.kvk.message.VestigingenMapper")
    def test_get_vestigingen(self, mock_vestigingen_mapper):
        p = KvkUpdateMessageProcessor()
        vestigingnummers = [1380, 140]
        p.dataservice = MagicMock()
        p.dataservice.ophalen_vestiging_by_vestigingsnummer.return_value = {'product': 'vestiging'}
        p._process_entity = MagicMock(return_value=['a'])

        self.assertEqual([
            'a', 'a'
        ], p._get_vestigingen(vestigingnummers))

        p.dataservice.ophalen_vestiging_by_vestigingsnummer.assert_has_calls([
            call(1380),
            call(140),
        ])

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
                'collection': 'the coll',
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
