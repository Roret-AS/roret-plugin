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
