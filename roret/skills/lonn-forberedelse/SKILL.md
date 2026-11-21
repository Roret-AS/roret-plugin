---
name: lonn-forberedelse
description: Sjekkliste før lønnskjøringen — status på lønnskjøringen for måneden, nyansatte og sluttere, yrkeskode og virksomhet, fravær og ferie, utlegg som venter på refusjon, ansatte som mangler skattekort, fødselsnummer eller kontonummer, og fristen for a-meldingen. Leser, og foreslår nye ansatte med kontrakt som et menneske godkjenner. Bruk denne når brukeren skal kjøre lønn, spør «er vi klare for lønn», vil ha lønnsforberedelse, vil legge inn ansatte, eller lurer på hva som mangler før a-meldingen.
---

# Lønnsforberedelse

Denne skillen leser, og foreslår nye ansatte (steg 3b). Selve
lønnskjøringen og a-meldingen gjøres i Roret av den som har lønnsrollen.
Bruk `firmaprofil` for selskap, lønnsdag og om lønnen utbetales samme måned
eller måneden etter.

Er lønnen flyttet fra et annet lønnssystem i år, eller skal den flyttes,
følg oppskriften under «Lønn» i `flytt-til-roret` (metode.md): den siste
lønnen i det gamle systemet, lønnsbilaget i Roret og den første lønnen i
Roret.

## Steg 1: Hvilken måned

Bli enige om lønnsmåneden. Se `l10n_no_lonn_utbetales` i firmaprofilen:
etterskuddsvis lønn (september-lønn utbetalt i oktober) rapporteres i
a-meldingen for utbetalingsmåneden.

## Steg 2: Status på kjøringen

```
lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)
```

Er kjøringen laget, beregnet, bekreftet eller betalt? Sammenlign med forrige
måned (`lonnskjoring_status` for måneden før): antall lønnsslipper og netto.

## Steg 3: Ansatte

```
hent_ansatte(company_id=<id>, include_employment_details=True, limit=500)
```

Verktøyet gir navn, stilling og avdeling, ikke start- og sluttdato.
Datoene står på ansettelsen, og den som kjører lønn, kan lese dem:

```
odoo_search_read("hr.version", [["company_id","=",<id>]], ["employee_id","contract_date_start","contract_date_end"])
```

Se etter:

- **Nyansatte** med startdato i måneden: har de kontrakt, lønn og skattekort?
- **Sluttere** med sluttdato i måneden: skal feriepenger utbetales, og er
  sluttdato satt på kontrakten?
- **Endringer** i stillingsprosent eller lønn som skal gjelde fra måneden.
  Dem ser du ikke herfra. Spør brukeren.

Gir kallet tilgangsfeil, har brukeren ikke lønnsrollen. Si det, og ta resten
av sjekklista.

**Yrkeskoden og virksomheten.** A-meldingen krever begge for hvert
arbeidsforhold. Les dem på kontrakten:

```
odoo_search_read("hr.version", [["company_id","=",<id>],["contract_date_start","!=",false]], ["employee_id","job_title","l10n_no_yrkeskode_id","l10n_no_virksomhet_id"])
```

- **Yrkeskoden** er en sjusifret kode fra SSBs yrkeskatalog, og mange koder
  har bransjen og antallet ansatte i parentes. Kontroller hver kode med
  `finn_yrkeskode(stilling=<stillingen>, bransje=<bransjen fra firmaprofil>, antall_ansatte=<antallet med kontrakt>)`.
  Mangler koden, eller står det en bransje eller størrelse i den som ikke
  passer bedriften (for eksempel «butikk – over 9 ansatte» i et elektrofirma
  med fire ansatte), vis brukeren de beste treffene. Koden byttes på den
  ansatte i Roret (Ansatte → den ansatte → Lønnsavregning → Yrkeskode).
- **Virksomheten** er underenheten i Enhetsregisteret. Mangler den på
  kontrakten, velges den samme sted. Har selskapet ingen virksomhet, stopper
  Lønn → Kjør lønn steg 1. I Roret legger Roret den inn
  (support@roret.no). I Roret for Odoo legger lønnsansvarlig den inn under
  Lønn → Konfigurasjon → Virksomheter.

I Roret for Odoo kan en bruker med rollen Innstillinger lese tellerne for det
som mangler i lønnsoppsettet. I Roret har ingen hos kunden den rollen, så
hopp over kallet der og pek på siden **Lønn → Kjør lønn**, som viser det
samme før lønnen godkjennes:

```
odoo_search_read("res.company", [["id","=",<id>]], ["l10n_no_lonn_steg","l10n_no_lonn_mangler_fnr","l10n_no_lonn_mangler_skattekort","l10n_no_lonn_mangler_konto","l10n_no_lonn_mangler_land","l10n_no_lonn_mangler_virksomhet","l10n_no_lonn_otp_steg","l10n_no_lonn_mangler_otp"])
```

Gir kallet tilgangsfeil, si at tellerne ikke kan leses herfra, og pek på
**Lønn → Kjør lønn** i Roret.

## Steg 3b: Nye ansatte

Skal en ansatt legges inn, gjør det med `opprett_ansatt`. Det blir alltid et
forslag et menneske med personalansvar godkjenner i Roret-appen eller i
Roret, og da lages den ansatte med kontrakten. Finn yrkeskoden med
`finn_yrkeskode` først, og vis brukeren verdiene i en tabell (navn, stilling,
startdato, fastlønn med månedslønn eller timelønn, stillingsprosent,
feriepengesats, yrkeskode, fødselsnummer og kontonummer) før du kaller.
Fødselsnummeret og kontonummeret skal komme fra brukeren, aldri gjettes.
Spør om feriepengesatsen: 10,2 er lovens minimum, og 12 gjelder ved avtalt
femte ferieuke. Slå opp satsene med `lov_oppslag`.

```
opprett_ansatt(navn="<navn>", company_id=<id>, startdato="YYYY-MM-DD", yrkeskode="<7 sifre>", stilling="<stilling>", fodselsnummer="<11 sifre>", kontonummer="<11 sifre>", avlonning="fast_lonn", maanedslonn=<beløp>, feriepengesats=<sats>)
```

Én ansatt per kall. Kontoen godkjennes for utbetaling av den som godkjenner
lønnen, i Kjør lønn. Skattekortet hentes når den ansatte er laget (Ansatte →
Handlinger → Hent skattekort fra Skatteetaten).

## Steg 4: Fravær og ferie i måneden

```
odoo_search_read("hr.leave", [["state","in",["confirm","validate1","validate"]],["request_date_from","<=","<siste dag>"],["request_date_to",">=","<første dag>"],["company_id","=",<id>]], ["employee_id","holiday_status_id","request_date_from","request_date_to","number_of_days","state"])
```

Lista viser bare fraværet brukeren selv får se i Roret. Uten rollen for
fravær er det brukerens eget og det hen skal godkjenne, så en tom liste betyr
ikke at ingen har fravær. Si det, og be brukeren kontrollere mot **Fravær** i
Roret, eller mot «Dette er nytt siden forrige lønn» på siden Kjør lønn.

Fravær som ikke er godkjent (`confirm`, `validate1`) bør godkjennes før
kjøringen. Sykefravær ut over arbeidsgiverperioden kan gi refusjon fra NAV.
Slå opp reglene med `lov_oppslag` hvis brukeren spør.

## Steg 5: Utlegg som skal refunderes

```
odoo_search_read("hr.expense", [["payment_mode","=","own_account"],["state","in",["submitted","approved","posted"]],["company_id","=",<id>]], ["employee_id","name","date","total_amount","state"])
```

Innsendte utlegg som ikke er godkjent, og godkjente som ikke er betalt.
Refunderes utlegg med lønnen i selskapet, må de være godkjent før kjøringen.

## Steg 6: Frister

`frister(company_id=<id>, date_from=<første dag>, date_to=<siste dag + 40 dager>)`
gir datoene med hjemmel: a-meldingen den 5. i måneden etter utbetalingen,
forskuddstrekket første virkedag etter utbetalingen, og arbeidsgiveravgiften
annenhver måned. Bruk dem i sjekklista.

## Steg 7: Sjekkliste

```
## Lønn <måned> — <selskap>
- Kjøring: ikke laget ennå
- Nyansatte: Kari Nordmann fra 1. oktober, mangler skattekort
- Yrkeskode: Ola Hansen har «daglig leder (butikk – over 9 ansatte)», foreslått
  «daglig leder (bygg og anlegg – færre enn 10 ansatte)»
- Sluttere: ingen
- Fravær til godkjenning: 2 søknader
- Utlegg til refusjon: 3 godkjente (4 120 kr), 1 venter på godkjenning
- A-melding: frist 5. november (bekreftet)
```

Avslutt med hva som må gjøres før kjøringen, og hvem som gjør det.

## Viktig

- Lønnsdata er personopplysninger. Vis bare det som trengs, og kopier det
  ikke ut av samtalen (`roret-prinsipper` §9).
- Ikke gjett skattetrekk eller feriepenger for enkeltpersoner. Det regner
  lønnsmotoren ut.
