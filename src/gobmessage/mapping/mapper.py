from abc import ABC, abstractmethod
from typing import Type


def get_value(d: dict, key: str):
    if not isinstance(d, dict):
        return None
    if '|' in key:
        # Return first value that is not empty
        for or_key in key.split('|'):
            val = get_value(d, or_key)
            if val:
                return val
        return None
    if "." in key:
        head, *tail = key.split('.')
        return get_value(d.get(head, {}), '.'.join(tail))
    return d.get(key)


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

    def _map(self, src, fields: dict):
        """

        :param src: dict or str
        :param fields:
        :return:
        """
        result = {}
        for field_name, source_field in fields.items():
            if source_field == ".":
                result[field_name] = src
            elif isinstance(source_field, tuple):
                args = [get_value(src, field) for field in source_field[1:]]
                result[field_name] = source_field[0](*args)
            elif isinstance(source_field, dict):
                submapping = {k: v for k, v in source_field.items() if not k.startswith('_')}

                if source_field.get('_list', False):
                    assert '_base' in source_field, "Should have _base in combination with _list"
                    base = get_value(src, source_field['_base'])
                    result[field_name] = [
                        self._map(item, submapping)
                        for item in base
                    ] if base else []
                else:
                    result[field_name] = self._map(src, submapping)
            elif isinstance(source_field, str) and source_field[0] == '=':
                result[field_name] = source_field[1:]
            else:
                result[field_name] = get_value(src, source_field)
        return result

    def map(self, source: dict) -> dict:
        return self._map(source, self.fields)

    def get_id(self, mapped_entity: dict) -> str:
        return mapped_entity.get(self.entity_id)


class MapperRegistry:
    mappers = {}

    @classmethod
    def register(cls, mapper: Type[Mapper]):
        if mapper.catalogue not in cls.mappers:
            cls.mappers[mapper.catalogue] = {}
        if mapper.collection in cls.mappers[mapper.catalogue]:
            raise Exception(f"Mapper for {mapper.catalogue} {mapper.collection} already registered")
        cls.mappers[mapper.catalogue][mapper.collection] = mapper

    @classmethod
    def get(cls, catalogue: str, collection: str):
        try:
            return cls.mappers[catalogue][collection]
        except KeyError:
            raise Exception(f"No mapper found for {catalogue} {collection}")
