from gobmessage.mapping.mapper import Mapper
from gobmessage.mapping.value_converter import ValueConverter


class MaatschappelijkeActiviteitenMapper(Mapper):
    catalogue = 'hr'
    collection = 'maatschappelijke_activiteiten'
    entity_id = 'kvknummer'
    version = '0.1'

    fields = {
        'kvknummer': 'maatschappelijkeActiviteit.kvkNummer',
        'naam': 'maatschappelijkeActiviteit.naam',
        'non_mailing': (
            ValueConverter.jn_to_bool,
            'maatschappelijkeActiviteit.nonMailing.code'
        ),
        'datum_aanvang_maatschappelijke_activiteit': (
            ValueConverter.to_date,
            'maatschappelijkeActiviteit.registratie.datumAanvang'
        ),
        'datum_einde_maatschappelijke_activiteit': (
            ValueConverter.to_date,
            'maatschappelijkeActiviteit.registratie.datumEinde'
        ),
        'registratie_tijdstip_maatschappelijke_activiteit': (
            ValueConverter.to_datetime,
            'maatschappelijkeActiviteit.registratie.registratieTijdstip'
        ),
        'incidenteel_uitlenen_arbeidskrachten': (
            ValueConverter.jn_to_bool,
            'maatschappelijkeActiviteit.incidenteelUitlenenArbeidskrachten.code'
        ),
        'communicatienummer': {
            '_base': 'maatschappelijkeActiviteit.communicatiegegevens.communicatienummer',
            '_list': True,
            'nummer': 'nummer',
            'toegangscode': 'toegangscode',
            'soort': 'soort.omschrijving',
        },
        'email_adres': {
            '_base': 'maatschappelijkeActiviteit.communicatiegegevens.emailAdres',
            '_list': True,
            'adres': '.',
        },
        'domeinnaam': {
            '_base': 'maatschappelijkeActiviteit.communicatiegegevens.domeinNaam',
            '_list': True,
            'naam': '.',
        }
    }
