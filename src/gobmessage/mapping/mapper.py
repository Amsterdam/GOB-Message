from abc import ABC, abstractmethod


def get_value(d: dict, key: str):
    if not isinstance(d, dict):
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

    def map(self, source: dict) -> dict:
        def map(src, fields: dict):
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
                    result[field_name] = source_field[0](get_value(src, source_field[1]))
                elif isinstance(source_field, dict):
                    submapping = {k: v for k, v in source_field.items() if not k.startswith('_')}

                    if source_field.get('_list', False):
                        assert '_base' in source_field, "Should have _base in combination with _list"

                        result[field_name] = [
                            map(item, submapping)
                            for item in get_value(src, source_field['_base'])
                        ]
                    else:
                        raise NotImplementedError("Not sure what you try to accomplish here.")

                else:
                    result[field_name] = get_value(src, source_field)
            return result
        return map(source, self.fields)

    def get_id(self, mapped_entity: dict) -> str:
        return mapped_entity.get(self.entity_id)
