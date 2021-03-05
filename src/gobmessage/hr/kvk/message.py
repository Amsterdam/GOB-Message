import datetime

from gobcore.message_broker.config import IMPORT_OBJECT
from gobcore.workflow.start_workflow import start_workflow

from gobmessage.config import MESSAGE_EXCHANGE, UPDATE_OBJECT_COMPLETE_KEY
from gobmessage.database.model import KvkUpdateMessage
from gobmessage.database.repository import KvkUpdateMessageRepository, UpdateObject, UpdateObjectRepository
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk.dataservice.service import KvkDataService
from gobmessage.mapping.mapper import Mapper
from gobmessage.mapping.hr import MaatschappelijkeActiviteitenMapper


class KvkUpdateMessageProcessor:
    source = 'KvK'
    application = 'KvkDataService'
    inschrijving_collections = {
        'maatschappelijkeactiviteiten': MaatschappelijkeActiviteitenMapper,
    }
    vestiging_collections = {}

    def __init__(self):
        self.dataservice = KvkDataService()

    def process(self, message: KvkUpdateMessage) -> list[UpdateObject]:
        res = []
        if message.kvk_nummer:
            inschrijving = self.dataservice.ophalen_inschrijving_by_kvk_nummer(message.kvk_nummer)
            res += self._process_inschrijving(inschrijving)

        if message.vestigingsnummer:
            vestiging = self.dataservice.ophalen_vestiging_by_vestigingsnummer(message.vestigingsnummer)
            res += self._process_vestiging(vestiging)
        return res

    def _process_inschrijving(self, inschrijving: dict) -> list[UpdateObject]:
        res = []
        for collection, mapper in self.inschrijving_collections.items():
            res.append(self._process_entity(inschrijving['product'], mapper()))
        return res

    def _process_vestiging(self, vestiging: dict) -> list[UpdateObject]:
        res = []
        for collection, mapper in self.vestiging_collections.items():
            res.append(self._process_entity(vestiging['product'], mapper()))
        return res

    def _process_entity(self, source: dict, mapper: Mapper) -> UpdateObject:
        mapped_entity = mapper.map(source)

        update_object = UpdateObject()
        update_object.catalogue = mapper.catalogue
        update_object.collection = mapper.collection
        update_object.entity_id = mapper.get_id(mapped_entity)

        self._start_workflow(update_object, mapped_entity, mapper)

        return update_object

    def _start_workflow(self, update_object: UpdateObject, mapped_entity: dict, mapper: Mapper):
        workflow = {
            'workflow_name': IMPORT_OBJECT,
        }
        arguments = {
            'header': {
                'catalogue': update_object.catalogue,
                'entity': update_object.collection,
                'entity_id': update_object.entity_id,
                'entity_id_attr': mapper.entity_id,
                'source': self.source,
                'application': self.application,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'version': mapper.version,
                'on_workflow_complete': {
                    # Picked up by Workflow to notify us when import is complete
                    'exchange': MESSAGE_EXCHANGE,
                    'key': UPDATE_OBJECT_COMPLETE_KEY,
                }

            },
            'contents': {
                **mapped_entity,
            }
        }
        start_workflow(workflow, arguments)


def kvk_message_handler(msg: dict):
    """Message handler for message queue

    :param msg:
    :return:
    """
    message_id = msg['message_id']
    with DatabaseSession() as session:
        repo = KvkUpdateMessageRepository(session)
        message = repo.get(message_id)

        processor = KvkUpdateMessageProcessor()
        update_objs = processor.process(message)
        UpdateObjectRepository(session).save_all(update_objs)

        message.is_processed = True
        repo.save(message)
