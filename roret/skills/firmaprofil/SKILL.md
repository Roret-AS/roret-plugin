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
2. Hent profilen for alle selskapene brukeren har tilgang til:

```
firmaprofil()
```

Eller for ett selskap: `firmaprofil(company_id=<id>)`. Verktøyet leser bare
feltene kunden har, og aldri nøkler eller passord. Et felt som ikke finnes i
kundens Odoo, er `None`.

Finnes ikke verktøyet (Roret-tjenesten er eldre enn denne skillen), les
selskapene med `odoo_search_read("res.company", [], ["id", "name", "company_registry", "vat", "currency_id"])`
og spør brukeren om resten.

## Steg 2: Les profilen

| Del av svaret | Betyr |
|---|---|
| `company_id`, `navn`, `orgnr` | Selskapet. `orgnr` er organisasjonsnummeret |
| `organisasjonsform`, `regnes_som_aksjeselskap` | AS, ENK osv. Ukjent form regnes som aksjeselskap, som i Roret |
| `regnskapsaar` | Regnskapsårets slutt, om det er kalenderår, når regnskapet i Odoo starter, og hva som er låst |
| `mva.registrering`, `mva.registrert_fra`, `mva.slettet_fra` | Status i Merverdiavgiftsregisteret |
| `mva.termin`, `mva.kilde` | «annenhver_maaned» eller «aarlig», lest av MVA-meldingene i Roret |
| `mva.melding_fra_roret`, `mva.siste_meldinger` | MVA-meldingen sendes fra Roret, og de siste meldingene |
| `aarsregnskap` | Små foretak, revisjon, om regnskapsfører lager årsregnskapet, og grunnlaget for skattemeldingen |
| `lonn.amelding_fra_roret`, `lonn.skattekort_fra_roret` | Lønn og a-melding fra Roret |
| `lonn.lonnsdag`, `lonn.utbetales` | Lønnsdag, og om lønnen utbetales samme måned som den opptjenes eller måneden etter (a-meldingen følger utbetalingen) |
| `lonn.konto_forskuddstrekk`, `lonn.konto_arbeidsgiveravgift` | Kontoene for skyldig forskuddstrekk og arbeidsgiveravgift |
| `lonn.antall_ansatte` | Ansatte i Odoo. `None` når brukeren ikke får lese ansatte |
| `bankkontoer` | Bankjournalene med kontonummer |

Er `mva.registrering` ikke satt, er et `vat` som slutter på «MVA» bare en
pekepinn. Sjekk da i Enhetsregisteret (`kundesjekk`).

### MVA-terminen

`mva.termin` er `None` når selskapet ikke har noen MVA-meldinger i Roret
ennå. Spør da brukeren om selskapet har vanlig termin (annenhver måned) eller
årstermin. Har kunden Odoos eget felt for terminen (Roret for Odoo), står
verdien i `mva.i_odoo`.

### Regnskapsfører

Hvem som er regnskapsfører, står ikke i Odoo. Spør brukeren når det betyr noe
(frister, årsoppgjør, migrering).

## Steg 3: Vis profilen kort

```
## <Selskapsnavn> (org.nr <orgnr>, company_id <id>)
- Organisasjonsform: AS
- MVA: registrert fra 1. mars 2021, terminer annenhver måned
- Regnskapsår: kalenderår
- Bank: DNB 1234.56.78901 (journal «Bank»)
- Lønn: 4 ansatte, a-melding fra Roret, lønnsdag den 20.
```

Mangler noe som en annen skill trenger (for eksempel MVA-termin), si det og
spør brukeren. Foreslå at administratoren fyller det inn i Roret, så alle får
riktig svar neste gang.

## Når flere selskaper

Én Odoo kan ha mange selskaper. Spør hvilket selskap det gjelder når
forespørselen er tvetydig, og send alltid `company_id` videre til
verktøyene. Har brukeren bare ett selskap, bruk det uten å spørre.
