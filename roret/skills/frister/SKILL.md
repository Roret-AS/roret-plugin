---
name: frister
description: Lager selskapets fristkalender ut fra firmaprofilen i Odoo — MVA-melding, a-melding, arbeidsgiveravgift, forskuddstrekk, forskuddsskatt, aksjonærregisteroppgave, skattemelding, generalforsamling og årsregnskap — og viser bare fristene som gjelder selskapet. Bruk denne når brukeren spør «hvilke frister har vi», «når er neste MVA-frist», «hva må gjøres før nyttår», vil ha en årskalender, eller når mandagsbrief eller månedsavslutning trenger kommende frister.
---

# Frister

## Steg 1: De løpende fristene

Roret regner dem ut fra loven og selskapets profil:

```
frister(company_id=<id>, date_from="YYYY-MM-DD", date_to="YYYY-MM-DD")
```

Standard er de neste 60 dagene. Svaret har dato, frist, periode og hjemmel
for MVA-melding og betaling, a-melding, arbeidsgiveravgift, forskuddstrekk og
forskuddsskatt. En frist som faller på helg eller helligdag, er flyttet til
neste virkedag (`flyttet_fra` er datoen i loven).

Les `antakelser` og si dem til brukeren: for eksempel at terminlengden ikke
er kjent og er regnet som annenhver måned. Vet brukeren bedre, kall igjen
med `mva_termin="aarlig"` (eller `"annenhver_maaned"`, `"ingen"`), eller med
`include_payroll=True` når selskapet betaler lønn som ikke kjøres i Roret.

To regler som ofte er feil i gamle oversikter:

- **Forskuddstrekket** forfaller første virkedag etter hver lønnsutbetaling
  (fra 2026). Det betales ikke lenger annenhver måned sammen med
  arbeidsgiveravgiften. Er lønnsdagen ikke satt i Roret, står det i
  `antakelser`, og du må spørre.
- **Arbeidsgiveravgiften** betales fortsatt annenhver måned, den 15. i
  måneden etter terminen.

## Steg 2: Årsoppgjøret

Fristene for årsoppgjøret er ikke med i verktøyet. Har selskapet Styring,
gir `styrets_oversikt(company_id=<id>)` dem slik Roret har regnet dem
(generalforsamling, årsregnskap, skattemelding, innkallinger). Bruk dem når
de finnes.

Ellers er dette de vanlige fristene for et selskap med kalenderår som
regnskapsår. **Bekreft dem med `lov_oppslag` (eller skatteetaten.no og
brreg.no) før de brukes som fasit**, og si fra hvis du ikke har kunnet
bekrefte.

| Frist | Gjelder | Når |
|---|---|---|
| Aksjonærregisteroppgave | AS | 31. januar |
| Skattemelding | AS og personlig næringsdrivende | 31. mai |
| Ordinær generalforsamling | AS | Innen seks måneder etter regnskapsårets slutt (30. juni), aksjeloven § 5-5 |
| Årsregnskap til Regnskapsregisteret | Regnskapspliktige (blant annet AS) | Senest én måned etter at det er fastsatt, regnskapsloven § 8-2. Vanligvis innen 31. juli |

Har selskapet avvikende regnskapsår, gjelder ikke tabellen. Si det, og slå
opp reglene.

## Steg 3: Vis fristene

Vis bare det som gjelder selskapet, kommende frister først:

```
## Frister for Eksempel AS — neste 60 dager
| Dato | Frist | Status |
|---|---|---|
| 5. november | A-melding for oktober | Lønn for oktober er kjørt |
| 16. november | Arbeidsgiveravgift september–oktober (15. er en søndag) | |
| 23. november | Forskuddstrekk fra lønnen 20. november | |
| 10. desember | MVA-melding og betaling, termin 5 | Ikke laget ennå |
```

Legg på status der du kan hente den raskt:
- A-melding: `lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)`.
- MVA-melding: `mva_status(year=<år>, period="<termin>", company_id=<id>)`.
  Selve kontrollen av grunnlaget gjøres i `mva-termin`.

Ber brukeren om hele året, kall `frister` for året og vis en årskalender per
måned.

## Påminnelser

Tilby å legge fristene som aktiviteter i Odoo for den ansvarlige, etter ja:
`hent_aktivitetstyper()` og så
`planlegg_aktivitet(model="res.partner", res_id=<selskapets partner>, activity_type_id=<gjøremål>, summary=<frist>, date_deadline=<dato>, user_id=<ansvarlig>)`.
Gjør det for én frist om gangen, eller for en liste brukeren har godkjent.

## Ansvar

Kalenderen er en hjelp, ikke en garanti. Endringer i regelverket og
individuelle avtaler med Skatteetaten (for eksempel utsatt frist via
regnskapsfører) går foran. Si det kort når du viser fristene første gang.
