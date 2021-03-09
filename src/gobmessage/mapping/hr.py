from gobmessage.mapping.mapper import Mapper
from gobmessage.mapping.value_converter import ValueConverter


class LocatiesMapper(Mapper):
    catalogue = 'hr'
    collection = 'locaties'
    entity_id = 'identificatie'
    version = '0.1'

    fields = {
        'identificatie': 'volledigAdres',
        'volgnummer': '=1',
        'volledig_adres': 'volledigAdres',
    }


class MaatschappelijkeActiviteitenMapper(Mapper):
    catalogue = 'hr'
    collection = 'maatschappelijkeactiviteiten'
    entity_id = 'kvknummer'
    version = '0.1'

    fields = {
        'kvknummer': 'kvkNummer',
        'naam': 'naam',
        'non_mailing': (
            ValueConverter.jn_to_bool,
            'nonMailing.code'
        ),
        'datum_aanvang_maatschappelijke_activiteit': (
            ValueConverter.to_date,
            'registratie.datumAanvang'
        ),
        'datum_einde_maatschappelijke_activiteit': (
            ValueConverter.to_date,
            'registratie.datumEinde'
        ),
        'registratie_tijdstip_maatschappelijke_activiteit': (
            ValueConverter.to_datetime,
            'registratie.registratieTijdstip'
        ),
        'incidenteel_uitlenen_arbeidskrachten': (
            ValueConverter.jn_to_bool,
            'incidenteelUitlenenArbeidskrachten.code'
        ),
        'communicatienummer': {
            '_base': 'communicatiegegevens.communicatienummer',
            '_list': True,
            'nummer': 'nummer',
            'toegangscode': 'toegangscode',
            'soort': 'soort.omschrijving',
        },
        'email_adres': {
            '_base': 'communicatiegegevens.emailAdres',
            '_list': True,
            'adres': '.',
        },
        'domeinnaam': {
            '_base': 'communicatiegegevens.domeinNaam',
            '_list': True,
            'naam': '.',
        },
        'registratie_tijdstip_onderneming': (
            ValueConverter.to_datetime,
            'manifesteertZichAls.onderneming.registratie.registratieTijdstip'
        ),
        'datum_aanvang_onderneming': (
            ValueConverter.to_date,
            'manifesteertZichAls.onderneming.registratie.datumAanvang'
        ),
        'datum_einde_onderneming': (
            ValueConverter.to_date,
            'manifesteertZichAls.onderneming.registratie.datumEinde'
        ),
        'totaal_werkzame_personen':
            'manifesteertZichAls.onderneming.totaalWerkzamePersonen',
        'voltijd_werkzame_personen':
            'manifesteertZichAls.onderneming.voltijdWerkzamePersonen',
        'deeltijd_werkzame_personen':
            'manifesteertZichAls.onderneming.deeltijdWerkzamePersonen',
        'handelt_onder_handelsnamen': {
            '_base': 'manifesteertZichAls.onderneming.handeltOnder',
            '_list': True,
            'omschrijving': 'handelsnaam.naam',
            'tijdstip_registratie': (ValueConverter.to_datetime, 'handelsnaam.registratie.registratieTijdstip'),
            'datum_aanvang_handelsnaam': (ValueConverter.to_date, 'handelsnaam.registratie.datumAanvang'),
            'datum_einde_handelsnaam': (ValueConverter.to_date, 'handelsnaam.registratie.datumEinde'),
            'volgorde': 'handelsnaam.volgorde',
        },
        'heeft_hoofdvestiging': {
            'bronwaarde': 'wordtGeleidVanuit.commercieleVestiging.vestigingsnummer|'
                          'wordtGeleidVanuit.nietCommercieleVestiging.vestigingsnummer',
        },
        'heeft_sbi_activiteiten_voor_onderneming': {
            '_list': True,
            '_base': 'manifesteertZichAls.onderneming.sbiActiviteit',
            'bronwaarde': 'sbiCode.code',
        },
        'heeft_sbi_activiteiten_voor_maatschappelijke_activiteit': {
            '_list': True,
            '_base': 'sbiActiviteit',
            'bronwaarde': 'sbiCode.code',
        },
        'wordt_uitgeoefend_in_commerciele_vestiging': {
            '_list': True,
            '_base': 'manifesteertZichAls.onderneming.wordtUitgeoefendIn',
            'bronwaarde': 'commercieleVestiging.vestigingsnummer',
        },
        'wordt_uitgeoefend_in_niet_commerciele_vestiging': {
            '_list': True,
            '_base': 'wordtUitgeoefendIn',
            'bronwaarde': 'nietCommercieleVestiging.vestigingsnummer',
        },
        'heeft_bezoekadres': {
            'bronwaarde': 'bezoekLocatie.volledigAdres',
        },
        'heeft_postadres': {
            'bronwaarde': 'postLocatie.volledigAdres',
        },
    }
