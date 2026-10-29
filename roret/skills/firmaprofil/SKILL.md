---
name: firmaprofil
description: Leser selskapets profil fra Odoo — selskaper og company_id, org.nr, MVA-registrering og termin, regnskapsår, organisasjonsform, bankkontoer, lønn og a-melding — så andre Roret-skills vet hvilket selskap og hvilke frister de jobber med. Bruk denne første gang i en samtale før du henter tall eller skriver noe, når brukeren spør «hvilke selskaper har jeg», eller når en annen skill trenger MVA-termin, regnskapsår eller selskapets id.
---

# Firmaprofil

Profilen ligger allerede i Odoo. Les den derfra hver gang. Ikke lagre en kopi
i notater eller minne: den blir utdatert, og Odoo er fasiten.

## Steg 1: Hvilke baser og selskaper

1. Prøv `mine_baser()`. Finnes verktøyet, og brukeren har flere baser, spør
   hvilken det gjelder før du går videre. Finnes det ikke, er det én base.
2. Hent selskapene brukeren har tilgang til:

```
odoo_search_read("res.company", [], ["id", "name", "company_registry", "vat", "currency_id", "parent_id"])
```

`company_registry` er organisasjonsnummeret. Om selskapet er MVA-registrert,
står i `l10n_no_mva_registrering` (steg 2). Finnes ikke det feltet, er `vat`
med «MVA» bare en pekepinn. Sjekk da i Enhetsregisteret (`kundesjekk`).

## Steg 2: Norske innstillinger (bare feltene som finnes)

Kundene har ulike moduler. Spør først hvilke felt som finnes:

```
odoo_fields_get("res.company", ["string", "type"])
```

Les deretter de av disse som finnes, for valgt selskap:

| Felt | Betyr |
|---|---|
| `l10n_no_bronnoysund_number` | Org.nr når `company_registry` er tomt |
| `fiscalyear_last_month`, `fiscalyear_last_day` | Regnskapsårets slutt |
| `account_opening_date`, `fiscalyear_lock_date`, `tax_lock_date` | Når regnskapet i Odoo starter, og hva som er låst |
| `l10n_no_mva_registrering`, `l10n_no_mva_registrert_fra`, `l10n_no_mva_slettet_fra` | Status i Merverdiavgiftsregisteret |
| `l10n_no_mvamelding_aktivert` | MVA-melding sendes fra Roret |
| `roret_compliance_organisasjonsform`, `l10n_no_arsregnskap_organisasjonsform` | AS, ENK osv. |
| `l10n_no_skattemelding_regnskapspliktstype`, `l10n_no_skattemelding_virksomhetstype` | Grunnlag for skattemeldingen |
| `l10n_no_arsregnskap_smaa_foretak`, `l10n_no_arsregnskap_revideres_ikke`, `l10n_no_arsregnskap_utarbeidet_av_regnskapsforer` | Årsregnskap: små foretak, revisjon, om regnskapsfører lager det |
| `l10n_no_amelding_aktivert`, `l10n_no_skattekort_aktivert` | Lønn og a-melding fra Roret |
| `l10n_no_lonnsdag`, `l10n_no_lonn_utbetales` | Lønnsdag, og om lønnen utbetales samme måned som den opptjenes eller måneden etter (a-meldingen følger utbetalingen) |
| `l10n_no_amelding_forskuddstrekk_account_id`, `l10n_no_amelding_aga_account_id` | Kontoene for skyldig forskuddstrekk og arbeidsgiveravgift |

```
odoo_search_read("res.company", [["id", "=", <company_id>]], [<feltene som finnes>])
```

**Les aldri felt med `api_key`, `token`, `secret` eller `password` i navnet,**
og heller ikke andre `roret_compliance_`-felt enn organisasjonsformen. De er
hemmeligheter eller interne adresser, og ingen skill trenger dem.

### MVA-terminen

Terminlengden står ikke på selskapet. Les den av MVA-meldingene som finnes:

```
odoo_search_read("l10n.no.mvamelding", [["company_id", "=", <company_id>]], ["aar", "periode", "state"], limit=6, order="aar desc, periode desc")
```

`periode` er `"1"`–`"6"` for annenhver måned (1 = januar–februar) og
`"aarlig"` for årstermin. Finnes ingen meldinger, eller ikke modellen, spør
brukeren om selskapet har vanlig termin eller årstermin. Har kunden feltet
`account_return_periodicity` på selskapet (Roret for Odoo med Enterprise),
kan du lese det i stedet. Feltene `l10n_no_mva_forste_aar` og
`l10n_no_mva_forste_periode` (første termin Roret sender) finnes bare der.

### Regnskapsfører

Hvem som er regnskapsfører, står ikke i Odoo. Spør brukeren når det betyr noe
(frister, årsoppgjør, migrering).

## Steg 3: Bank og ansatte

```
odoo_search_read("account.journal", [["type", "=", "bank"], ["company_id", "=", <company_id>]], ["id", "name", "bank_account_id", "currency_id"])
hent_ansatte(company_id=<company_id>, limit=200)
```

Antall ansatte og om lønn kjøres i Roret avgjør om lønnsfrister skal med i
`frister` og `mandagsbrief`.

## Steg 4: Vis profilen kort

```
## <Selskapsnavn> (org.nr <company_registry>, company_id <id>)
- Organisasjonsform: AS
- MVA: registrert fra 1. mars 2021, terminer annenhver måned
- Regnskapsår: kalenderår
- Bank: DNB 1234.56.78901 (journal «Bank»)
- Lønn: 4 ansatte, a-melding fra Roret
```

Mangler noe som en annen skill trenger (for eksempel MVA-termin), si det og
spør brukeren. Foreslå at administratoren fyller det inn i Roret, så alle får
riktig svar neste gang.

## Når flere selskaper

Én Odoo kan ha mange selskaper. Spør hvilket selskap det gjelder når
forespørselen er tvetydig, og send alltid `company_id` videre til
verktøyene. Har brukeren bare ett selskap, bruk det uten å spørre.
