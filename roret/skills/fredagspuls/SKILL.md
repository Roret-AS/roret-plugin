---
name: fredagspuls
description: Kort status for uka som gikk — aktivitet, penger i banken, ukas største kunder og det som krever oppmerksomhet (uavstemte banklinjer, åpne supportsaker, forfalte oppgaver). Bruk denne når brukeren ber om ukerapport, ukeoppsummering, fredagspuls, eller en rask status for de siste sju dagene.
---

# Fredagspuls

Bruk `firmaprofil` for selskap. Har brukeren flere selskaper og ikke sagt
hvilket, spør.

Periode: `date_from` = i dag minus 6 dager, `date_to` = i dag
(`YYYY-MM-DD`).

## Hent (parallelt)

1. `aktivitetssammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>)`
2. `toppkunder(date_from="<date_from>", date_to="<date_to>", company_id=<id>, limit=3)`
3. `likvidbeholdning(company_id=<id>)`
4. `hent_uavstemte_banklinjer(company_id=<id>, limit=50)`
5. `hent_supportsaker(company_id=<id>, only_open=True, limit=20)`
6. `hent_aktiviteter(only_my=True, state="overdue")`

Mangler kunden kundeservice-modulen, hopp over punkt 5 uten å gjøre et
nummer av det.

## Format

```
## Uka som gikk — uke <N> (<date_from>–<date_to>)

| | Antall |
|---|---|
| Fakturaer bokført | 14 |
| Nye leads | 6 |
| Salg vunnet | 2 |
| Supportsaker opprettet / lukket | 9 / 11 |

**Bank:** 412 300 kr
**Ukas største kunder:** A (48 000 kr), B (31 500 kr), C (22 000 kr)
**Krever oppmerksomhet:** 7 uavstemte banklinjer, 3 åpne supportsaker, 2 forfalte oppgaver
```

Hold det under 200 ord. Avslutt med én kort linje om at tallene er
ledelsestall. Foreslå gjerne én konkret ting for neste uke, for eksempel å
avstemme banken eller følge opp en kunde.
