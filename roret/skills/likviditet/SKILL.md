---
name: likviditet
description: Likviditetsbilde for de neste 30 og 60 dagene — penger i banken nå, forventede innbetalinger fra kunder, regninger som forfaller, MVA, skattetrekk, arbeidsgiveravgift og lønn — med det som er estimat tydelig merket. Bruk denne når brukeren spør om likviditet, kontantstrøm, «har vi råd», «hvor mye penger har vi», hva som forfaller framover, eller vil ha en cash flow-oversikt.
---

# Likviditet

Gi et ærlig bilde av pengene framover. Skill mellom det som står i
regnskapet (fakta) og det du anslår (estimat). Bruk `firmaprofil` for
selskap, MVA-termin, lønnsdag og kontoene for trekk og avgift.

## Steg 1: Hent tallene (parallelt der du kan)

La `d30` være i dag + 30 dager og `d60` i dag + 60 dager.

| Hva | Verktøy |
|---|---|
| Bank og kasse i dag | `likvidbeholdning(company_id=<id>)` |
| Kunder som betaler de neste 30 dagene | `hent_fakturaer_som_forfaller(company_id=<id>, move_type="out_invoice", date_to=<d30>)` |
| Kunder som betaler dag 31–60 | `hent_fakturaer_som_forfaller(company_id=<id>, move_type="out_invoice", date_from=<d30 + 1>, date_to=<d60>)` |
| Regninger som forfaller de neste 30 dagene | `hent_fakturaer_som_forfaller(company_id=<id>, move_type="in_invoice", date_to=<d30>)` |
| Regninger dag 31–60 | `hent_fakturaer_som_forfaller(company_id=<id>, move_type="in_invoice", date_from=<d30 + 1>, date_to=<d60>)` |
| Forfalt fra kunder | `hent_forfalte_fakturaer(company_id=<id>, move_type="out_invoice", limit=50)` |
| Forfalt til leverandører | `hent_forfalte_fakturaer(company_id=<id>, move_type="in_invoice", limit=50)` |
| Fordringer og gjeld etter alder | `aldersfordelte_kundefordringer(company_id=<id>, move_type="out_invoice")` og samme med `"in_invoice"` |
| MVA i terminen som løper | `mva_sammendrag(date_from="<terminstart>", date_to="<i dag>", company_id=<id>)` |
| Lønn denne måneden | `lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)` |
| Fristene i vinduet | `frister(company_id=<id>, date_to=<d60>)` |

`sum_restbelop` i `hent_fakturaer_som_forfaller` er summen over alle
treffene, også når lista er kortere (`flere_enn_vist`). Bruk den i tabellen,
ikke en sum du regner av lista.

## Steg 2: Skattetrekk og arbeidsgiveravgift (estimat)

Reglene (bekreft med `lov_oppslag` før du skriver datoer):

- **Forskuddstrekket** forfaller første virkedag etter hver lønnsutbetaling.
  Plasser det sammen med lønnen, i samme kolonne.
- **Arbeidsgiveravgiften** for to måneder betales den 15. i måneden etter
  terminen. `frister` gir datoen.

Saldoen på kontoene gir anslaget. Bruk kontoene fra firmaprofilen
(`lonn.konto_forskuddstrekk`, `lonn.konto_arbeidsgiveravgift`), ellers 2600
og 2770 i standard kontoplan:

```
saldo_per_konto(account_ids=[<trekkonto>, <avgiftskonto>], company_id=<id>)
saldo_per_konto(account_codes=["2600", "2770"], company_id=<id>)
```

Saldoen er negativ for gjeld: 2600 med −41 200 betyr 41 200 kr skyldig
trekk. Merk tallene som estimat. Plasser MVA og arbeidsgiveravgift i
kolonnen der fristen faller, ikke der perioden er: MVA for terminen som
løper nå, betales først etter terminslutt.

## Steg 3: Sett opp bildet

```
## Likviditet <selskap> per <dato>

| | Neste 30 dager | 31–60 dager |
|---|---|---|
| Bank i dag | 412 300 kr | |
| Inn: kundefakturaer som forfaller | +185 000 | +96 000 |
| Ut: leverandørfakturaer som forfaller | −121 500 | −64 000 |
| Ut: MVA (estimat) | −48 200 | |
| Ut: arbeidsgiveravgift (estimat) | | −31 900 |
| Ut: netto lønn og forskuddstrekk (estimat) | −200 000 | −200 000 |
| **Beregnet saldo** | **227 600** | **27 700** |
```

Under tabellen:

- **Forfalt fra kunder:** sum og de største postene. Å få inn dette endrer
  bildet mest. Foreslå `purring`-skillen.
- **Forfalt til leverandører:** det som allerede er for sent.
- **Risiko:** store enkeltkunder, kunder som pleier å betale sent, og om
  saldoen går under null i vinduet.
- **Forutsetninger:** at kundene betaler ved forfall, at lønn er som forrige
  måned, og hva som er estimat.

## Viktig

- Dette er ledelsestall, ikke regnskapsrapportering (`roret-prinsipper` §7).
- Ikke regn med innbetalinger som allerede er forfalt i 60+ dager som sikre.
  Vis dem for seg.
- Har selskapet flere bankkontoer eller valuta, vis dem hver for seg før du
  summerer i NOK.
