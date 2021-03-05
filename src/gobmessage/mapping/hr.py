from gobmessage.mapping.mapper import Mapper
from gobmessage.mapping.value_converter import ValueConverter


class MaatschappelijkeActiviteitenMapper(Mapper):
    catalogue = 'hr'
    collection = 'maatschappelijkeactiviteiten'
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
        },
        'registratie_tijdstip_onderneming': (
            ValueConverter.to_datetime,
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.registratie.registratieTijdstip'
        ),
        'datum_aanvang_onderneming': (
            ValueConverter.to_date,
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.registratie.datumAanvang'
        ),
        'datum_einde_onderneming': (
            ValueConverter.to_date,
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.registratie.datumEinde'
        ),
        'totaal_werkzame_personen':
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.totaalWerkzamePersonen',
        'voltijd_werkzame_personen':
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.voltijdWerkzamePersonen',
        'deeltijd_werkzame_personen':
            'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.deeltijdWerkzamePersonen',
        'handelt_onder_handelsnamen': {
            '_base': 'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.handeltOnder',
            '_list': True,
            'omschrijving': 'handelsnaam.naam',
            'tijdstip_registratie': (ValueConverter.to_datetime, 'handelsnaam.registratie.registratieTijdstip'),
            'datum_aanvang_handelsnaam': (ValueConverter.to_date, 'handelsnaam.registratie.datumAanvang'),
            'datum_einde_handelsnaam': (ValueConverter.to_date, 'handelsnaam.registratie.datumEinde'),
            'volgorde': 'handelsnaam.volgorde',
        },
        'heeft_hoofdvestiging': {
            'bronwaarde': 'maatschappelijkeActiviteit.wordtGeleidVanuit.commercieleVestiging.vestigingsnummer|'
                          'maatschappelijkeActiviteit.wordtGeleidVanuit.nietCommercieleVestiging.vestigingsnummer',
        },
        'heeft_sbi_activiteiten_voor_onderneming': {
            '_list': True,
            '_base': 'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.sbiActiviteit',
            'bronwaarde': 'sbiCode.code',
        },
        'heeft_sbi_activiteiten_voor_maatschappelijke_activiteit': {
            '_list': True,
            '_base': 'maatschappelijkeActiviteit.sbiActiviteit',
            'bronwaarde': 'sbiCode.code',
        },
        'wordt_uitgeoefend_in_commerciele_vestiging': {
            '_list': True,
            '_base': 'maatschappelijkeActiviteit.manifesteertZichAls.onderneming.wordtUitgeoefendIn',
            'bronwaarde': 'commercieleVestiging.vestigingsnummer',
        },
        'wordt_uitgeoefend_in_niet_commerciele_vestiging': {
            '_list': True,
            '_base': 'maatschappelijkeActiviteit.wordtUitgeoefendIn',
            'bronwaarde': 'nietCommercieleVestiging.vestigingsnummer',
        },
        'heeft_bezoekadres': {
            'bronwaarde': 'maatschappelijkeActiviteit.bezoekLocatie.volledigAdres',
        },
        'heeft_postadres': {
            'bronwaarde': 'maatschappelijkeActiviteit.postLocatie.volledigAdres',
        },
    }
