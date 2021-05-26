import datetime

from gobcore.message_broker.config import IMPORT_OBJECT
from gobcore.workflow.start_workflow import start_workflow

from gobmessage.config import MESSAGE_EXCHANGE, UPDATE_OBJECT_COMPLETE_KEY
from gobmessage.database.model import KvkUpdateMessage
from gobmessage.database.repository import KvkUpdateMessageRepository, UpdateObject, UpdateObjectRepository
from gobmessage.database.session import DatabaseSession
from gobmessage.hr.kvk.dataservice.service import KvkDataService
from gobmessage.mapping.mapper import Mapper, MapperRegistry
from gobmessage.mapping.hr import MaatschappelijkeActiviteitenMapper, LocatiesMapper, VestigingenMapper


class KvkUpdateMessageProcessor:
    source = 'KvK'
    application = 'KvkDataService'
    inschrijving_entities = {
        'maatschappelijkeActiviteit': MaatschappelijkeActiviteitenMapper,
        'maatschappelijkeActiviteit.postLocatie': LocatiesMapper,
        'maatschappelijkeActiviteit.bezoekLocatie': LocatiesMapper,
    }

    def __init__(self, message: KvkUpdateMessage):
        self.dataservice = KvkDataService()
        self.message = message

    def process(self) -> list[UpdateObject]:
        inschrijving = self.dataservice.ophalen_inschrijving_by_kvk_nummer(self.message.kvk_nummer)
        update_objects = self._process_inschrijving(inschrijving)
        self.message.update_objects = update_objects
        return update_objects

    def _get_base(self, base_path: str, obj: dict) -> dict:
        keys = ['product'] + base_path.split('.')
        current = obj

        try:
            for key in keys:
                current = current[key]
        except KeyError:
            return {}
        return current

    def _process_inschrijving(self, inschrijving: dict) -> list[UpdateObject]:
        res = []
        for base_path, mapper in self.inschrijving_entities.items():
            base = self._get_base(base_path, inschrijving)

            if base:
                res += self._process_entity(base, mapper())
        return res

    def _process_entity(self, source: dict, mapper: Mapper) -> list[UpdateObject]:
        mapped_entity = mapper.map(source)

        update_object = UpdateObject()
        update_object.catalogue = mapper.catalogue
        update_object.collection = mapper.collection
        update_object.entity_id = mapper.get_id(mapped_entity)
        update_object.mapped_entity = mapped_entity
        update_object.source = self.source
        update_object.application = self.application
        update_object.update_message = self.message
        update_objects = [update_object]

        if isinstance(mapper, MaatschappelijkeActiviteitenMapper):
            update_objects += self._get_vestigingen(mapper.get_vestigingsnummers(mapped_entity))
        elif isinstance(mapper, VestigingenMapper):
            update_objects += self._get_locaties(mapper.get_locaties(source))

        return update_objects

    def _get_vestigingen(self, vestigingnummers: list[int]) -> list[UpdateObject]:
        res = []
        mapper = VestigingenMapper()
        for vestigingnummer in vestigingnummers:
            vestiging = self.dataservice.ophalen_vestiging_by_vestigingsnummer(vestigingnummer)
            res += self._process_entity(vestiging['product'], mapper)
        return res

    def _get_locaties(self, locaties: list) -> list[UpdateObject]:
        mapper = LocatiesMapper()
        return [update_obj for loc in locaties for update_obj in self._process_entity(loc, mapper)]


def start_update_object_workflow(update_object: UpdateObject):
    mapper = MapperRegistry.get(update_object.catalogue, update_object.collection)

    workflow = {
        'workflow_name': IMPORT_OBJECT,
    }
    arguments = {
        'header': {
            'message_id': update_object.update_message.id,
            'catalogue': update_object.catalogue,
            'entity': update_object.collection,
            'collection': update_object.collection,
            'entity_id': update_object.entity_id,
            'entity_id_attr': mapper.entity_id,
            'source': update_object.source,
            'application': update_object.application,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'version': mapper.version,
            'on_workflow_complete': {
                # Picked up by Workflow to notify us when import is complete
                'exchange': MESSAGE_EXCHANGE,
                'key': UPDATE_OBJECT_COMPLETE_KEY,
            }

        },
        'contents': {
            **update_object.mapped_entity,
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

        processor = KvkUpdateMessageProcessor(message)
        update_objs = processor.process()

        # Start first
        start_update_object_workflow(update_objs[0])
        update_objs[0].status = UpdateObject.STATUS_STARTED

        UpdateObjectRepository(session).save_all(update_objs)

        message.is_processed = True
        repo.save(message)


def update_object_complete_handler(msg):
    """Callback for when an import flow started by the GOB-Message service is finished.

    :param msg:
    :return:
    """

    with DatabaseSession() as session:
        repo = UpdateObjectRepository(session)
        update_object = repo.get_active_for_entity_id(
            msg['header']['message_id'],
            msg['header']['catalogue'],
            msg['header']['entity'],
            msg['header']['entity_id']
        )
        update_object.status = repo.object_class.STATUS_ENDED
        repo.save(update_object)

        if next := update_object.update_message.get_next_queued_update_object():
            start_update_object_workflow(next)
            next.status = UpdateObject.STATUS_STARTED
            repo.save(next)

    return msg
