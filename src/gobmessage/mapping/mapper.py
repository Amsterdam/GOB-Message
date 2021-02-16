from abc import ABC, abstractmethod


class Mapper(ABC):

    @property
    @abstractmethod
    def fields(self):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def entity_id(self):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def version(self):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def catalogue(self):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def collection(self):  # pragma: no cover
        pass

    def map(self, source: dict) -> dict:
        def get_value(d: dict, key: str):
            if not isinstance(d, dict):
                return None
            if "." in key:
                head, *tail = key.split('.')
                return get_value(d.get(head, {}), '.'.join(tail))
            return d.get(key)

        result = {}
        for field_name, source_field in self.fields.items():
            if isinstance(source_field, tuple):
                result[field_name] = source_field[0](get_value(source, source_field[1]))
            else:
                result[field_name] = get_value(source, source_field)
        return result

    def get_id(self, mapped_entity: dict) -> str:
        return mapped_entity.get(self.entity_id)
