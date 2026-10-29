---
name: likviditet
description: Likviditetsbilde for de neste 30 og 60 dagene — penger i banken nå, forventede innbetalinger fra kunder, regninger som forfaller, MVA, skattetrekk, arbeidsgiveravgift og lønn — med det som er estimat tydelig merket. Bruk denne når brukeren spør om likviditet, kontantstrøm, «har vi råd», «hvor mye penger har vi», hva som forfaller framover, eller vil ha en cash flow-oversikt.
---

# Likviditet

Gi et ærlig bilde av pengene framover. Skill mellom det som står i
regnskapet (fakta) og det du anslår (estimat). Bruk `firmaprofil` for
selskap, MVA-termin og lønn.

## Steg 1: Hent tallene (parallelt der du kan)

| Hva | Verktøy |
|---|---|
| Bank og kasse i dag | `likvidbeholdning(company_id=<id>)` |
| Kundefordringer etter alder | `aldersfordelte_kundefordringer(company_id=<id>, move_type="out_invoice")` |
| Leverandørgjeld etter alder | `aldersfordelte_kundefordringer(company_id=<id>, move_type="in_invoice")` |
| Forfalt fra kunder | `hent_forfalte_fakturaer(company_id=<id>, move_type="out_invoice", limit=50)` |
| Forfalt til leverandører | `hent_forfalte_fakturaer(company_id=<id>, move_type="in_invoice", limit=50)` |
| MVA i terminen som løper | `mva_sammendrag(date_from="<terminstart>", date_to="<i dag>", company_id=<id>)` |
| Lønn denne måneden | `lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)` |

For forfall innen 30 og 60 dager, hent åpne fakturaer med forfallsdato i
vinduet:

```
odoo_search_read("account.move", [["move_type","in",["out_invoice","in_invoice"]],["state","=","posted"],["payment_state","in",["not_paid","partial"]],["invoice_date_due","<=","<i dag + 60>"],["company_id","=",<id>]], ["name","partner_id","move_type","invoice_date_due","amount_residual_signed"], limit=500)
```

## Steg 2: Skattetrekk og arbeidsgiveravgift (estimat)

Trekk og avgift for to måneder betales samlet. Saldoen på kontoene for
forskuddstrekk og skyldig arbeidsgiveravgift gir et anslag på neste betaling.
Bruk kontoene selskapet har satt opp for a-meldingen hvis feltene finnes
(`l10n_no_amelding_forskuddstrekk_account_id`,
`l10n_no_amelding_aga_account_id` på `res.company`, se `firmaprofil`), ellers
2600 og 2770 i standard kontoplan. La Odoo summere saldoen per konto. Summer
aldri sider fra `odoo_search_read`: den gir maks 1000 linjer, og summen blir
stille feil når kontoen har flere.

```
odoo_formatted_read_group("account.move.line", [["account_id","in",[<trekkonto>,<avgiftskonto>]],["parent_state","=","posted"],["company_id","=",<id>]], groupby=["account_id"], aggregates=["balance:sum"], company_id=<id>)
```

Merk dette som estimat. Plasser MVA, skattetrekk og arbeidsgiveravgift i
kolonnen der fristen faller, ikke der perioden er: MVA for terminen som løper
nå, betales først etter terminslutt. Hent fristene fra `frister`-skillen, og
bekreft dem med `lov_oppslag` før du skriver datoer.

## Steg 3: Sett opp bildet

```
## Likviditet <selskap> per <dato>

| | Neste 30 dager | 31–60 dager |
|---|---|---|
| Bank i dag | 412 300 kr | |
| Inn: kundefakturaer som forfaller | +185 000 | +96 000 |
| Ut: leverandørfakturaer som forfaller | −121 500 | −64 000 |
| Ut: MVA (estimat) | −48 200 | |
| Ut: skattetrekk og arbeidsgiveravgift (estimat) | | −71 900 |
| Ut: netto lønn (estimat) | −160 000 | −160 000 |
| **Beregnet saldo** | **267 600** | **67 700** |
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
