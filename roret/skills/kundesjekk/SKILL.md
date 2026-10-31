---
name: kundesjekk
description: Sjekker en ny kunde eller leverandør i Enhetsregisteret (Brønnøysundregistrene) — riktig navn og adresse, organisasjonsform, MVA-registrering, konkurs eller avvikling, og hvem som har roller — og oppretter eller beriker kontakten i Odoo etter godkjenning. Bruk denne når brukeren skal registrere en ny kunde eller leverandør, vil sjekke et org.nr, lurer på om en motpart er konkurs eller MVA-registrert, eller vil rydde i kundekortet.
---

# Kundesjekk mot Enhetsregisteret

Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Steg 1: Finn enheten

**Først Rorets eget oppslag.** Roret slår opp i Enhetsregisteret fra Odoo,
med org.nr eller navn, og sier samtidig om selskapet alt finnes som kontakt:

```
sok_i_enhetsregisteret(query="<org.nr eller navn>", limit=5, company_id=<id>)
```

Svaret har `treff` (org.nr, navn, `beskrivelse`, `verdier` som kan brukes
rett i kontaktkortet, og `partner` når kontakten finnes) og `feil` når
registeret ikke svarer. `beskrivelse` slutter med SLETTET, KONKURS, UNDER
AVVIKLING eller UNDER TVANGSAVVIKLING når selskapet ikke driver. Si det
øverst. Er lista tom og `sokt` er `false`, var teksten for kort eller
ikke et gyldig org.nr, eller brukeren har ikke rett til å lage kontakter.
Sier verktøyet at kunden ikke har oppslaget, gå videre til det åpne API-et
under.

**Ellers det åpne API-et.** Enhetsregisteret har et åpent API uten
innlogging. Bruk Claudes egen nettilgang (WebFetch eller tilsvarende). Det
gir også MVA-registrering, næringskode og roller, som Rorets oppslag ikke
viser:

- Har du org.nr (9 sifre, fjern mellomrom):
  `https://data.brreg.no/enhetsregisteret/api/enheter/<orgnr>`
- Har du bare navnet:
  `https://data.brreg.no/enhetsregisteret/api/enheter?navn=<navn>`
  Vis de beste treffene med org.nr, kommune og organisasjonsform, og la
  brukeren velge.
- Finner du ingenting under `enheter`, kan det være en underenhet
  (avdeling): `https://data.brreg.no/enhetsregisteret/api/underenheter/<orgnr>`.

Har ikke Claude nettilgang i denne økta, be brukeren åpne enheten på
brreg.no og lime inn det som står der. Gjett aldri org.nr eller adresse.

## Steg 2: Les det som betyr noe

| Felt | Hva du ser etter |
|---|---|
| `navn` | Riktig juridisk navn til fakturaen |
| `organisasjonsform` | AS, ENK, NUF, SA, forening … |
| `registrertIMvaregisteret` | Skal fakturaen fra dem ha MVA? Skal vår faktura til dem ha MVA (avhenger av oss)? |
| `konkurs`, `underAvvikling`, `underTvangsavviklingEllerTvangsopplosning` | **Rødt flagg.** Si det øverst |
| `forretningsadresse` (og `postadresse`) | Adresse til kundekortet |
| `naeringskode1` | Bransje |
| `stiftelsesdato`, `antallAnsatte` | Nyetablert? Størrelse? |

Roller (styreleder, daglig leder, signatur):
`https://data.brreg.no/enhetsregisteret/api/enheter/<orgnr>/roller`.
Hent dem når brukeren skal inngå avtale, gi kreditt eller trenger å vite
hvem som kan signere.

## Steg 3: Vis en kort vurdering

```
## Eksempel AS (org.nr 123 456 789)
- AS, stiftet 2019, 12 ansatte, bransje 62.010 Programmeringstjenester
- MVA-registrert: ja
- Konkurs/avvikling: nei
- Adresse: Storgata 1, 0155 Oslo
- Daglig leder: Kari Nordmann. Styreleder: Ola Nordmann
```

Er enheten konkurs eller under avvikling: anbefal forskuddsbetaling eller å
avvente, og si at brukeren bør snakke med regnskapsfører eller advokat før
kreditt gis.

## Steg 4: Dublett i Odoo

```
finn_kunde(query=<orgnr>)
finn_kunde(query=<navn>)
```

`finn_kunde` søker i navn, e-post og MVA-nummer (`vat`), men ikke i feltene
der org.nr står for selskaper som ikke er MVA-registrert. Søk der også
(utelat feltet som ikke finnes, se `odoo_fields_get("res.partner", ["type"])`):

```
odoo_search_read("res.partner", ["|", ["company_registry", "=", "<orgnr>"], ["l10n_no_bronnoysund_number", "=", "<orgnr>"]], ["id", "name"])
```

Kom treffet fra Rorets oppslag, har feltet `partner` alt svaret. Treff:
foreslå å berike det eksisterende kortet i stedet for å lage et nytt.

## Steg 5: Opprett eller berik etter godkjenning

Slå opp Norge og se hvordan selskapet allerede skriver org.nr på kunder:

```
odoo_search_read("res.country", [["code", "=", "NO"]], ["id"])
odoo_search_read("res.partner", [["is_company", "=", true], ["vat", "!=", false]], ["vat"], limit=5)
```

Vis kortet slik det blir, og opprett etter ja:

```
opprett_kontakt(name=<navn>, is_company=True, company_registry=<org.nr>,
                vat=<MVA-nummer i samme format som de andre, bare når MVA-registrert>,
                street=<adresse>, zip=<postnr>, city=<poststed>, country_id=<Norge>,
                email=<hvis kjent>, phone=<hvis kjent>,
                comment="Kontrollert i Enhetsregisteret <dato>", company_id=<company_id>)
```

`company_registry` er organisasjonsnummeret. Verktøyet sjekker
kontrollsifferet og setter det også i Rorets norske felt når kunden har det.
Kom treffet fra Rorets oppslag, står verdiene i `verdier` (bruk
`verdier.country_id.id` som `country_id`). Avviser Odoo MVA-nummeret, vis
feilen og spør i stedet for å prøve varianter i blinde.

Kontaktpersoner (daglig leder) opprettes bare hvis brukeren ber om det, med
`parent_id` satt til firmaet.

## Personvern

Rolleinnehavere er offentlige opplysninger i Enhetsregisteret, men legg bare
inn personer selskapet faktisk skal ha kontakt med.
