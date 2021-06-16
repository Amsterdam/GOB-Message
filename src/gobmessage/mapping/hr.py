from gobmessage.mapping.mapper import Mapper, MapperRegistry, get_value
from gobmessage.mapping.value_converter import ValueConverter


class VestigingenMapper(Mapper):
    catalogue = 'hr'
    collection = 'vestigingen'
    entity_id = 'vestigingsnummer'
    version = '0.1'

    fields = {
        'eerste_handelsnaam': 'eersteHandelsnaam|naamgeving.naam',  # CV | NCV
        'vestigingsnummer': 'vestigingsnummer',

        # Registratie CV | NCV
        'tijdstip_registratie': (ValueConverter.to_datetime,
                                 'registratie.registratieTijdstip|naamgeving.registratie.registratieTijdstip'),
        'datum_aanvang': (ValueConverter.to_incomplete_date,
                          'registratie.datumAanvang|naamgeving.registratie.datumAanvang'),
        'datum_einde': (ValueConverter.to_incomplete_date,
                        'registratie.datumEinde|naamgeving.registratie.datumEinde'),

        # CV & NCV
        'datum_voortzetting': (ValueConverter.to_incomplete_date,
                               'isOvergenomenVan.datumVoortzetting|isOvergedragenNaar.datumVoortzetting'),

        # Locatie
        'heeft_als_postadres': {
            'bronwaarde': 'postLocatie.volledigAdres',
        },
        'heeft_als_bezoekadres': {
            'bronwaarde': 'bezoekLocatie.volledigAdres'
        },

        # Communicatie
        'communicatienummer': {
            '_base': 'communicatiegegevens.communicatienummer',
            '_list': True,
            'nummer': 'nummer',
            'toegangscode': 'toegangscode',
            'soort': 'soort.omschrijving',
        },
        'emailadres': {
            '_base': 'communicatiegegevens.emailAdres',
            '_list': True,
            'adres': '.',
        },
        'domeinnaam': {
            '_base': 'communicatiegegevens.domeinNaam',
            '_list': True,
            'naam': '.',
        },
        'activiteiten_omschrijving': 'activiteiten.omschrijving',

        # Niet-commerciele vestiging
        'naam': 'naamgeving.naam',
        'verkorte_naam': 'naamgeving.verkorteNaam',  # niet in xsd
        'ook_genoemd': 'naamgeving.ookGenoemd',

        # Commerciele vestiging
        'totaal_werkzame_personen': 'totaalWerkzamePersonen',
        'voltijd_werkzame_personen': 'voltijdWerkzamePersonen',
        'deeltijd_werkzame_personen': 'deeltijdWerkzamePersonen',
        'importeert': (ValueConverter.jn_to_bool, 'activiteiten.importeert.code'),
        'exporteert': (ValueConverter.jn_to_bool, 'activiteiten.exporteert.code'),
        'handelt_onder_handelsnamen': {
            '_base': 'handeltOnder',
            '_list': True,
            'omschrijving': 'handelsnaam.naam',
            'tijdstip_registratie': (ValueConverter.to_datetime, 'handelsnaam.registratie.registratieTijdstip'),
            'datum_aanvang_handelsnaam': (ValueConverter.to_incomplete_date, 'handelsnaam.registratie.datumAanvang'),
            'datum_einde_handelsnaam': (ValueConverter.to_incomplete_date, 'handelsnaam.registratie.datumEinde'),
            'volgorde': 'handelsnaam.volgorde',
        },

        # Activiteiten CV / NCV
        'heeft_sbi_activiteiten': {
            '_list': True,
            '_base': 'activiteiten.sbiActiviteit',
            'bronwaarde': (
                ValueConverter.concat('.'),
                'kvkNummer',  # enriched
                'vestigingsnummer',  # enriched
                'sbiCode.code'
            ),
        },

        # Samenvoeging vestigingen
        'is_overgegaan_in_vestiging': {
            '_list': True,
            '_base': 'isSamengevoegdMet',
            'bronwaarde': 'commercieleVestiging.vestigingsnummer|nietCommercieleVestiging.vestigingsnummer'
        },

        'is_een_uitoefening_van': {
            'bronwaarde':
                'isEenUitoefeningVan.maatschappelijkeActiviteit.kvkNummer|'
                'isEenUitoefeningVan.onderneming.isEenManifestatieVan.maatschappelijkeActiviteit.kvkNummer'
        }
    }

    def map(self, source: dict) -> dict:
        is_cv = 'commercieleVestiging' in source
        source = self._get_cv_or_ncv(source)
        source = self._enrich_activities(source)

        return super().map(source) | {'is_commerciele_vestiging': is_cv}

    def _enrich_activities(self, source: dict) -> dict:
        activities = get_value(source, self.fields['heeft_sbi_activiteiten']['_base'])

        if activities:
            update = {
                'kvkNummer': get_value(source, self.fields['is_een_uitoefening_van']['bronwaarde']),
                'vestigingsnummer': get_value(source, self.fields['vestigingsnummer'])
            }
            source['activiteiten']['sbiActiviteit'] = [act | update for act in activities]

        return source

    def _get_cv_or_ncv(self, source: dict) -> dict:
        return source.get('commercieleVestiging') or source.get('nietCommercieleVestiging', {})

    def get_locaties(self, source: dict) -> list[dict]:
        keys = ['bezoekLocatie', 'postLocatie']
        ves = self._get_cv_or_ncv(source)

        return [ves[key] for key in keys if ves[key] is not None]

    def get_activities(self, source: dict) -> list[dict]:
        return get_value(self._get_cv_or_ncv(source), self.fields['heeft_sbi_activiteiten']['_base'])


MapperRegistry.register(VestigingenMapper)


class LocatiesMapper(Mapper):
    catalogue = 'hr'
    collection = 'locaties'
    entity_id = 'identificatie'
    version = '0.1'

    fields = {
        'identificatie': 'volledigAdres',
        'volgnummer': '=1',
        'volledig_adres': 'volledigAdres',
        'tijdstip_registratie': (ValueConverter.to_datetime, 'registratie.registratieTijdstip'),
        'datum_aanvang': (ValueConverter.to_incomplete_date, 'registratie.datumAanvang'),
        'datum_einde': (ValueConverter.to_incomplete_date, 'registratie.datumEinde'),
        'afgeschermd': (ValueConverter.jn_to_bool, 'afgeschermd.code'),
        'toevoeging_adres': 'toevoegingAdres',
        'straatnaam': 'adres.binnenlandsAdres.straatnaam',
        'huisnummer': 'adres.binnenlandsAdres.huisnummer',
        'huisletter': 'adres.binnenlandsAdres.huisletter',
        'huisnummer_toevoeging': 'adres.binnenlandsAdres.huisnummerToevoeging',
        'postbusnummer': 'adres.binnenlandsAdres.postbusnummer',
        'postcode': (
            ValueConverter.concat(''),
            'adres.binnenlandsAdres.postcode.cijfercombinatie',
            'adres.binnenlandsAdres.postcode.lettercombinatie'
        ),
        'plaats': 'adres.binnenlandsAdres.plaats',
        'straat_huisnummer_buitenland': 'adres.buitenlandsAdres.straatHuisnummer',
        'postcode_plaats_buitenland': 'adres.buitenlandsAdres.postcodeWoonplaats',
        'regio_buitenland': 'adres.buitenlandsAdres.regio',
        'land_buitenland': 'adres.buitenlandsAdres.land',
        'heeft_nummeraanduiding': {
            'bronwaarde': 'adres.binnenlandsAdres.bagId.identificatieNummeraanduiding',
        },
        'heeft_verblijfsobject': {
            'bronwaarde': (ValueConverter.filter_vot, 'adres.binnenlandsAdres.bagId.identificatieAdresseerbaarObject'),
        },
        'heeft_ligplaats': {
            'bronwaarde': (ValueConverter.filter_lps, 'adres.binnenlandsAdres.bagId.identificatieAdresseerbaarObject'),
        },
        'heeft_standplaats': {
            'bronwaarde': (ValueConverter.filter_sps, 'adres.binnenlandsAdres.bagId.identificatieAdresseerbaarObject'),
        }
    }


MapperRegistry.register(LocatiesMapper)


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
            ValueConverter.to_incomplete_date,
            'registratie.datumAanvang'
        ),
        'datum_einde_maatschappelijke_activiteit': (
            ValueConverter.to_incomplete_date,
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
            ValueConverter.to_incomplete_date,
            'manifesteertZichAls.onderneming.registratie.datumAanvang'
        ),
        'datum_einde_onderneming': (
            ValueConverter.to_incomplete_date,
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
            'datum_aanvang_handelsnaam': (ValueConverter.to_incomplete_date, 'handelsnaam.registratie.datumAanvang'),
            'datum_einde_handelsnaam': (ValueConverter.to_incomplete_date, 'handelsnaam.registratie.datumEinde'),
            'volgorde': 'handelsnaam.volgorde',
        },
        'heeft_hoofdvestiging': {
            'bronwaarde': 'wordtGeleidVanuit.commercieleVestiging.vestigingsnummer|'
                          'wordtGeleidVanuit.nietCommercieleVestiging.vestigingsnummer',
        },
        'heeft_sbi_activiteiten_voor_onderneming': {
            '_list': True,
            '_base': 'manifesteertZichAls.onderneming.sbiActiviteit',
            'bronwaarde': (ValueConverter.concat('.'), 'kvkNummer', 'sbiCode.code'),
        },
        'heeft_sbi_activiteiten_voor_maatschappelijke_activiteit': {
            '_list': True,
            '_base': 'sbiActiviteit',
            'bronwaarde': (ValueConverter.concat('.'), 'kvkNummer', 'sbiCode.code'),
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
        }
    }

    def map(self, source: dict) -> dict:
        source = self._enrich_activities(source)
        return super().map(source)

    def _enrich_activities(self, source: dict) -> dict:
        field_kvknr = self.fields['kvknummer']
        update = {field_kvknr: source[field_kvknr]}

        # NietCommercieel
        ncomm_act = get_value(source, self.fields['heeft_sbi_activiteiten_voor_maatschappelijke_activiteit']['_base'])
        if ncomm_act:
            source['sbiActiviteit'] = [activity | update for activity in ncomm_act]

        # Commercieel
        comm_act = get_value(source, self.fields['heeft_sbi_activiteiten_voor_onderneming']['_base'])
        if comm_act:
            source['manifesteertZichAls']['onderneming']['sbiActiviteit'] = \
                [activity | update for activity in comm_act]

        return source

    def get_vestigingsnummers(self, mapped_mac_entity: dict) -> list[int]:
        return [item['bronwaarde'] for item in
                mapped_mac_entity.get('wordt_uitgeoefend_in_commerciele_vestiging', []) +
                mapped_mac_entity.get('wordt_uitgeoefend_in_niet_commerciele_vestiging')]


MapperRegistry.register(MaatschappelijkeActiviteitenMapper)


class SbiActiviteitenMapper(Mapper):
    """Assumes activiteiten are enriched with kvknummer/vestigingsnummer/rsin or bsn to construct relations."""
    catalogue = 'hr'
    collection = 'sbiactiviteiten'
    entity_id = 'sbi_activiteit_nummer'
    version = '0.1'

    fields = {
        'sbi_activiteit_nummer': (
            ValueConverter.concat('.'), 'kvkNummer', 'vestigingsnummer', '<secure_rsin_or_bsn>', 'sbiCode.code'
        ),
        'sbi_code': 'sbiCode.code',
        'omschrijving': 'sbiCode.omschrijving',
        'is_hoofdactiviteit': (ValueConverter.jn_to_bool, 'isHoofdactiviteit.code'),
        'volgorde': 'volgorde',
        'datum_aanvang_sbiactiviteit': (ValueConverter.to_incomplete_date, 'registratie.datumAanvang'),
        'datum_einde_sbiactiviteit': (ValueConverter.to_incomplete_date, 'registratie.datumEinde'),
        'tijdstip_registratie': (ValueConverter.to_datetime, 'registratie.registratieTijdstip'),
        'heeft_als_maatschappelijkactiviteit': {
            'bronwaarde': 'kvkNummer'
        },
        'heeft_als_vestiging': {
            'bronwaarde': 'vestigingsnummer'
        },
        'heeft_als_rechtspersoon': {
            'bronwaarde': 'nog_niet_beschikbaar'
        }
    }


MapperRegistry.register(SbiActiviteitenMapper)
