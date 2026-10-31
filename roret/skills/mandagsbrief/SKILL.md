---
name: mandagsbrief
description: Kort brief for uka som kommer — frister, forfalte kundefakturaer og regninger som forfaller, møter, egne oppgaver, oppfølgingspunkter fra styret og banklinjer som venter på avstemming. Bruk denne når brukeren ber om mandagsbrief, ukestart, «hva skjer denne uka», eller når en planlagt oppgave kjører den hver mandag.
---

# Mandagsbrief

Én skjerm, maks rundt 250 ord. Det skal kunne leses på telefonen før første
møte. Selskap: `firmaprofil` (har brukeren flere selskaper, spør én gang
hvilke briefen skal dekke). Briefen bare leser. Den endrer ingenting.

## Hent (parallelt der det går)

La `fra` være i dag og `til` søndag denne uka. Datoer som `YYYY-MM-DD`.

1. Frister de neste 14 dagene:
   `frister(company_id=<id>, date_from=<fra>, date_to=<fra + 14 dager>)`. Har
   selskapet Styring, ta med styrets frister fra `styrets_oversikt`.
2. Forfalte kundefakturaer:
   `hent_forfalte_fakturaer(company_id=<id>, move_type="out_invoice", limit=20)`.
3. Regninger som forfaller denne uka:
   `hent_fakturaer_som_forfaller(company_id=<id>, move_type="in_invoice", date_from=<fra>, date_to=<til>)`.
   Bruk `antall` og `sum_restbelop`.
4. Møter: `hent_kalenderhendelser(date_from=<fra>, date_to=<til>, company_id=<id>)`.
   Er Microsoft 365- eller Google-kalenderen koblet til, ta med møtene
   derfra også (se `epost-og-kalender`), uten dubletter.
5. Egne oppgaver: `hent_aktiviteter(only_my=True, state="overdue")` og
   `hent_aktiviteter(only_my=True, state="today")`.
6. Styret (bare med Styring): `hent_oppfolgingspunkter(only_open=True, company_id=<id>)`.
7. Bank: `hent_uavstemte_banklinjer(company_id=<id>, limit=50)` (bare
   antallet og eldste dato).
8. Likviditet: `likvidbeholdning(company_id=<id>)`.

Feiler ett kall (manglende modul eller tilgang), hopp over den delen og skriv
én linje om det nederst.

## Format

```
## Uke 44 — Eksempel AS

**Frister:** 5. nov a-melding · 16. nov arbeidsgiveravgift
**Penger:** 412 300 kr i bank. 6 forfalte kundefakturaer, 84 200 kr (eldste 41 dager). 3 regninger forfaller, 23 900 kr
**Møter:** tir 10:00 Kunde X · tor 17:30 styremøte
**Oppgaver:** 2 over frist, 4 i dag
**Venter:** 12 uavstemte banklinjer (eldste 9. okt). 1 forfalt oppfølgingspunkt fra styret

**Tre ting denne uka:**
1. …
2. …
3. …
```

De tre tingene er ditt forslag til prioritering: det som har frist, det som
koster penger å la ligge, og det som er glemt. Tall er ledelsestall
(`roret-prinsipper` §7). Én kort linje om det nederst holder.

## Som planlagt oppgave

Briefen passer som planlagt oppgave i Claude (for eksempel hver mandag kl.
07:30). Når den kjører uten bruker til stede: ikke still spørsmål, bruk
selskapet eller selskapene brukeren valgte da oppgaven ble satt opp, og
foreslå handlinger i stedet for å gjøre dem.
