from abc import ABC, abstractmethod

from gobmessage.database.model import KvkUpdateMessage, UpdateObject


class Repository(ABC):

    @property
    @abstractmethod
    def object_class(self):  # pragma: no cover
        pass

    def __init__(self, session):
        self.session = session

    def get(self, id: int):
        return self.session.query(self.object_class).get(id)

    def save(self, obj):
        self.session.add(obj)
        self.session.flush()
        return obj

    def save_all(self, objs: list):
        for obj in objs:
            self.session.add(obj)
        self.session.flush()
        return objs


class KvkUpdateMessageRepository(Repository):
    object_class = KvkUpdateMessage


class UpdateObjectRepository(Repository):
    object_class = UpdateObject

    def get_active_for_entity_id(self, catalogue: str, collection: str, entity_id: str):
        return self.session \
            .query(self.object_class) \
            .filter_by(catalogue=catalogue, collection=collection, entity_id=entity_id,
                       status=UpdateObject.STATUS_STARTED) \
            .order_by(UpdateObject.created_at) \
            .first()
