from unittest import TestCase
from unittest.mock import ANY, MagicMock, call, patch

from freezegun import freeze_time

from gobmessage.hr.kvk.message import (IMPORT_OBJECT, KvkUpdateMessage, KvkUpdateMessageProcessor, MESSAGE_EXCHANGE,
                                       UPDATE_OBJECT_COMPLETE_KEY, UpdateObject, kvk_message_handler,
                                       MaatschappelijkeActiviteitenMapper, start_update_object_workflow, MapperRegistry, update_object_complete_handler)
from gobmessage.mapping.mapper import Mapper


@patch("gobmessage.hr.kvk.message.KvkDataService", MagicMock())
class TestKvkUpdateMessageProcessor(TestCase):

    def test_process(self):
        message = KvkUpdateMessage()
        message.kvk_nummer = 123
        message.vestigingsnummer = 456

        p = KvkUpdateMessageProcessor(message)
        p._process_inschrijving = MagicMock()

        self.assertEqual(p._process_inschrijving.return_value, p.process())
        p._process_inschrijving.assert_called_with(p.dataservice.ophalen_inschrijving_by_kvk_nummer.return_value)
        p.dataservice.ophalen_inschrijving_by_kvk_nummer.assert_called_with(123)

    def test_process_inschrijving(self):
        p = KvkUpdateMessageProcessor(MagicMock())
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
        p = KvkUpdateMessageProcessor(MagicMock())
        p._start_workflow = MagicMock()
        mapper = MagicMock()

        res = p._process_entity({'some': 'source'}, mapper)[0]
        self.assertIsInstance(res, UpdateObject)
        self.assertEqual(res.catalogue, mapper.catalogue)
        self.assertEqual(res.collection, mapper.collection)
        self.assertEqual(res.entity_id, mapper.get_id.return_value)
        mapper.get_id.assert_called_with(mapper.map.return_value)
        mapper.map.assert_called_with({'some': 'source'})

    def test_process_entity_mac(self):
        p = KvkUpdateMessageProcessor(MagicMock())
        p._start_workflow = MagicMock()
        vestigingen_result = [MagicMock(), MagicMock()]
        p._get_vestigingen = MagicMock(return_value=vestigingen_result)
        mapper = MagicMock(spec=MaatschappelijkeActiviteitenMapper)

        res = p._process_entity({'some': 'source'}, mapper)
        self.assertEqual(vestigingen_result, res[1:3])
        p._get_vestigingen.assert_called_with(mapper.get_vestigingsnummers.return_value)

    @patch("gobmessage.hr.kvk.message.VestigingenMapper")
    def test_get_vestigingen(self, mock_vestigingen_mapper):
        p = KvkUpdateMessageProcessor(MagicMock())
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


class TestMessage(TestCase):

    @patch("gobmessage.hr.kvk.message.start_workflow")
    def test_start_workflow(self, mock_start_workflow):
        update_object = UpdateObject()
        update_object.catalogue = 'the cat'
        update_object.collection = 'the coll'
        update_object.entity_id = 'the entity id'
        update_object.mapped_entity = {'some': 'entity'}
        update_object.application = 'the application'
        update_object.source = 'the source'

        mapper = MagicMock(spec=Mapper)
        mapper.catalogue = 'the cat'
        mapper.collection = 'the coll'
        MapperRegistry.register(mapper)

        with freeze_time('2021-01-21 13:43:00'):
            start_update_object_workflow(update_object)

        mock_start_workflow.assert_called_with({
            'workflow_name': IMPORT_OBJECT,
        }, {
            'header': {
                'catalogue': 'the cat',
                'entity': 'the coll',
                'collection': 'the coll',
                'entity_id': 'the entity id',
                'entity_id_attr': mapper.entity_id,
                'source': update_object.source,
                'application': update_object.application,
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

    @patch("gobmessage.hr.kvk.message.start_update_object_workflow")
    @patch("gobmessage.hr.kvk.message.KvkUpdateMessageProcessor")
    @patch("gobmessage.hr.kvk.message.DatabaseSession")
    @patch("gobmessage.hr.kvk.message.KvkUpdateMessageRepository")
    @patch("gobmessage.hr.kvk.message.UpdateObjectRepository")
    def test_kvk_message_handler(self, mock_uo_repo, mock_um_repo, mock_session, mock_processor, mock_start_workflow):
        mocked_message = MagicMock()
        mocked_message.is_processed = False
        mock_um_repo.return_value.get.return_value = mocked_message

        uo1 = MagicMock()
        uo2 = MagicMock()
        mock_processor.return_value.process.return_value = [
            uo1,
            uo2,
        ]

        kvk_message_handler({'message_id': 42})

        mock_um_repo.assert_called_with(mock_session.return_value.__enter__.return_value)
        mock_um_repo.return_value.get.assert_called_with(42)

        mock_processor.return_value.process.assert_called_once()
        mock_uo_repo.assert_called_with(mock_session.return_value.__enter__.return_value)
        mock_uo_repo.return_value.save_all.assert_called_with(mock_processor.return_value.process.return_value)

        mock_um_repo.return_value.save.assert_called_with(mocked_message)
        self.assertTrue(mocked_message.is_processed)

        mock_start_workflow.assert_called_with(uo1)
        self.assertEqual(UpdateObject.STATUS_STARTED, uo1.status)
        self.assertNotEqual(UpdateObject.STATUS_STARTED, uo2.status)

    @patch("gobmessage.hr.kvk.message.start_update_object_workflow")
    @patch("gobmessage.hr.kvk.message.UpdateObjectRepository")
    @patch("gobmessage.hr.kvk.message.DatabaseSession")
    def test_update_object_complete_handler(self, mock_session, mock_repo, mock_start_workflow):

        msg = {
            'header': {
                'catalogue': 'CAT',
                'entity': 'ENT',
                'entity_id': 'entity id',
            }
        }
        mapper = MagicMock(spec=Mapper)
        mapper.catalogue = 'CAT'
        mapper.collection = 'ENT'
        MapperRegistry.register(mapper)

        res = update_object_complete_handler(msg)
        self.assertEqual(msg, res)
        mocked_session = mock_session.return_value.__enter__.return_value
        mock_repo.assert_called_with(mocked_session)

        mock_repo.return_value.get_active_for_entity_id.assert_called_with('CAT', 'ENT', 'entity id')

        mocked_entity = mock_repo.return_value.get_active_for_entity_id.return_value
        next = mocked_entity.update_message.get_next_queued_update_object.return_value
        self.assertEqual(mock_repo.return_value.object_class.STATUS_ENDED, mocked_entity.status)
        mock_repo.return_value.save.assert_has_calls([
            call(mocked_entity),
            call(next),
        ])

        mock_start_workflow.assert_called_with(next)
        self.assertEqual(UpdateObject.STATUS_STARTED, next.status)

