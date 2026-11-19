---
name: manedsrapport
description: Lager en månedsrapport for et selskap — resultat, toppkunder, likviditet ved månedsslutt, utestående fordringer, aktivitet og 12-måneders trend, med observasjoner om hva som bør følges opp. Bruk denne når brukeren ber om månedsrapport, månedsoppsummering, resultatet for en måned, eller en økonomisk status for selskapet.
---

# Månedsrapport

Bruk `firmaprofil` for selskap. Har brukeren flere selskaper og ikke sagt
hvilket, spør. Ga brukeren ikke måned, bruk forrige måned.

Regn ut `date_from` (første dag) og `date_to` (siste dag i måneden).

## Hent tallene (parallelt der du kan)

1. `resultatsammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>, detail_by_account=True)`
2. `toppkunder(date_from="<date_from>", date_to="<date_to>", company_id=<id>, limit=10)`
3. `likvidbeholdning(company_id=<id>, as_of_date="<date_to>")`
4. `aldersfordelte_kundefordringer(company_id=<id>, as_of_date="<date_to>", move_type="out_invoice")`
5. `aktivitetssammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>)`
6. `omsetningstrend(company_id=<id>, months_back=12)`
7. `lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)` (hopp over hvis selskapet ikke kjører lønn i Roret)

Feiler ett kall (manglende modul eller tilgang), lag rapporten uten den delen
og si hva som mangler.

Les tallene slik:

- **Driftsinntekter** er `revenue` i `resultatsammendrag`, uten MVA.
- **Bruttofortjeneste** er driftsinntektene minus varekostnaden (kontoene
  4000–4999 i `expense_by_account`). Den står ikke som eget tall.
- **Driftsresultat** er driftsinntektene minus kontoene 4000–7999.
  `resultat` (og `gross_profit`, som er samme tall under et gammelt navn) er
  inntekter minus alle kostnader, også finansposter på 8000-kontoene. Det er
  ikke bruttofortjenesten.
- **Snitt siste 12 måneder** er `mean_monthly_eks_mva` i `omsetningstrend`.
  `mean_monthly` og `total_revenue` er med MVA, i både `omsetningstrend` og
  `toppkunder`, og kan ikke sammenlignes med driftsinntektene. Snittet er
  over månedene som har fakturaer (`actual_months_with_data`). Si hvor mange
  det er når det er færre enn tolv.
- **Kundefordringer** per månedsslutt tar ikke med fakturaer datert etter
  datoen, men restbeløpet er dagens.

## Skriv rapporten

```
## Månedsrapport <måned år> — <selskap>

| | Måneden | Snitt siste 12 mnd |
|---|---|---|
| Driftsinntekter | 1 240 000 kr | 1 105 000 kr |
| Bruttofortjeneste | ... | ... |
| Driftsresultat | ... | ... |
| Bank ved månedsslutt | ... | |
| Kundefordringer (forfalt over 30 dager) | ... | |
```

Deretter:

- **Toppkunder:** de fem største med beløp og andel av omsetningen.
- **Utestående:** kunder med fakturaer forfalt over 30 dager. Merk at tallet
  er utestående **per i dag**, ikke per månedsslutt: fakturaer betalt etter
  månedsslutt er ikke med. Foreslå `purring` hvis det er noe der.
- **Aktivitet:** fakturaer, nye leads, vunne salg, supportsaker.
- **Observasjoner:** det som skiller seg ut mot trenden, kunder som bør
  følges opp, kostnader som har økt.

Hold rapporten under 400 ord. Tall i tabeller, vurderinger i prosa. Norsk
format: «1 234 567 kr».

Avslutt med: «Dette er ledelsestall fra regnskapet, ikke offisielle
rapporter. Årsregnskap, MVA-melding og SAF-T lages i Roret.»

Spør brukeren om en frist eller et krav til innhold (når skal
MVA-meldingen leveres, hva må med i årsregnskapet), slå det opp med
`lov_oppslag` og oppgi paragrafen.
