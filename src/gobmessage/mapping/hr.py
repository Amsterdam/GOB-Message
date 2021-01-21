from gobmessage.mapping.mapper import Mapper


class MaatschappelijkeActiviteitenMapper(Mapper):
    catalogue = 'hr'
    collection = 'maatschappelijke_activiteiten'
    entity_id = 'kvknummer'
    version = '0.1'

    fields = {
        'kvknummer': 'maatschappelijkeActiviteit.kvkNummer',
        'naam': 'maatschappelijkeActiviteit.naam',
    }
