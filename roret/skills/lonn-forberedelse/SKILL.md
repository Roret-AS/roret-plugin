---
name: lonn-forberedelse
description: Sjekkliste før lønnskjøringen, kun lesing — status på lønnskjøringen for måneden, nyansatte og sluttere, fravær og ferie, utlegg som venter på refusjon, ansatte som mangler skattekort, fødselsnummer eller kontonummer, og fristen for a-meldingen. Bruk denne når brukeren skal kjøre lønn, spør «er vi klare for lønn», vil ha lønnsforberedelse, eller lurer på hva som mangler før a-meldingen.
---

# Lønnsforberedelse

Denne skillen leser bare. Selve lønnskjøringen og a-meldingen gjøres i
Roret av den som har lønnsrollen. Bruk `firmaprofil` for selskap, lønnsdag
og om lønnen utbetales samme måned eller måneden etter.

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

Se etter:

- **Nyansatte** med startdato i måneden: har de kontrakt, lønn og skattekort?
- **Sluttere** med sluttdato i måneden: skal feriepenger utbetales, og er
  sluttdato satt på kontrakten?
- **Endringer** i stillingsprosent eller lønn som skal gjelde fra måneden.

Er brukeren administrator, gir firmaoppsettet tellerne for det som mangler
(feltene er skjult for andre):

```
odoo_search_read("res.company", [["id","=",<id>]], ["l10n_no_lonn_steg","l10n_no_lonn_mangler_fnr","l10n_no_lonn_mangler_skattekort","l10n_no_lonn_mangler_konto","l10n_no_lonn_mangler_land","l10n_no_lonn_mangler_virksomhet","l10n_no_lonn_otp_steg","l10n_no_lonn_mangler_otp"])
```

Gir kallet tilgangsfeil, si at oppsettet bare vises for administratoren, og
pek på lønnsoppsettet i Roret.

## Steg 4: Fravær og ferie i måneden

```
odoo_search_read("hr.leave", [["state","in",["confirm","validate1","validate"]],["request_date_from","<=","<siste dag>"],["request_date_to",">=","<første dag>"],["company_id","=",<id>]], ["employee_id","holiday_status_id","request_date_from","request_date_to","number_of_days","state"])
```

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

A-meldingen skal leveres innen fristen i måneden etter utbetalingen (normalt
den 5.). Skattetrekk og arbeidsgiveravgift betales samlet for to måneder.
Bekreft datoene med `lov_oppslag` eller `frister`-skillen før du skriver dem.

## Steg 7: Sjekkliste

```
## Lønn <måned> — <selskap>
- Kjøring: ikke laget ennå
- Nyansatte: Kari Nordmann fra 1. oktober, mangler skattekort
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
