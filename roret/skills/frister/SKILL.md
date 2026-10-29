---
name: frister
description: Lager selskapets fristkalender ut fra firmaprofilen i Odoo — MVA-melding, a-melding, forskuddstrekk og arbeidsgiveravgift, forskuddsskatt, aksjonærregisteroppgave, skattemelding, generalforsamling og årsregnskap — og viser bare fristene som gjelder selskapet. Bruk denne når brukeren spør «hvilke frister har vi», «når er neste MVA-frist», «hva må gjøres før nyttår», vil ha en årskalender, eller når mandagsbrief eller månedsavslutning trenger kommende frister.
---

# Frister

## Steg 1: Hva gjelder selskapet

Hent profilen med `firmaprofil`: organisasjonsform, MVA-registrering og
terminlengde, regnskapsår, og om lønn og a-melding kjøres i Roret. Har
selskapet Styring, gir `styrets_oversikt(company_id=<id>)` også styrets
frister (generalforsamling, årsregnskap, skattemelding, innkallinger) slik
Roret har regnet dem. Bruk dem når de finnes.

Mangler noe i profilen (for eksempel MVA-termin), spør brukeren.

## Steg 2: Standardfristene

Dette er de vanlige fristene for et selskap med kalenderår som regnskapsår.
**Bekreft dem med `lov_oppslag` (eller skatteetaten.no og brreg.no) før de
brukes som fasit**, og si fra hvis du ikke har kunnet bekrefte. En frist som
faller på lørdag, søndag eller helligdag, flyttes til neste virkedag.

| Frist | Gjelder | Når |
|---|---|---|
| A-melding | Alle som betaler lønn | 5. i måneden etter |
| Forskuddstrekk og arbeidsgiveravgift | Alle som betaler lønn | 15. januar, 15. mars, 15. mai, 15. juli, 15. september, 15. november |
| MVA-melding, alminnelig termin (annenhver måned) | MVA-registrerte | 10. april (jan–feb), 10. juni (mar–apr), 31. august (mai–jun), 10. oktober (jul–aug), 10. desember (sep–okt), 10. februar (nov–des) |
| MVA-melding, årstermin | MVA-registrerte med innvilget årstermin | 10. mars året etter |
| Aksjonærregisteroppgave | AS | 31. januar |
| Forskuddsskatt | AS | 15. februar og 15. april |
| Skattemelding | AS og personlig næringsdrivende | 31. mai |
| Ordinær generalforsamling | AS | Innen 30. juni |
| Årsregnskap til Regnskapsregisteret | Regnskapspliktige (blant annet AS) | Innen 31. juli |
| Forskuddsskatt | Personlig næringsdrivende (ENK) | 15. mars, 15. juni, 15. september, 15. desember |

Har selskapet avvikende regnskapsår, gjelder ikke tabellen for årsoppgjøret.
Si det, og slå opp reglene.

## Steg 3: Vis fristene

Vis bare det som gjelder selskapet, kommende frister først:

```
## Frister for Eksempel AS — neste 60 dager
| Dato | Frist | Status |
|---|---|---|
| 5. november | A-melding for oktober | Lønn for oktober er kjørt |
| 15. november | Forskuddstrekk og arbeidsgiveravgift sep–okt | |
| 10. desember | MVA-melding sep–okt | Uavstemte banklinjer i perioden: 4 |
```

Legg på status der du kan hente den raskt:
- A-melding: `lonnskjoring_status(period_month="YYYY-MM", company_id=<id>)`.
- MVA-termin: antall uavstemte banklinjer og utkast i perioden
  (`hent_uavstemte_banklinjer`, `hent_utkastfakturaer`). Selve kontrollen
  gjøres i `mva-termin`.

Ber brukeren om hele året, vis en årskalender per måned.

## Påminnelser

Tilby å legge fristene som aktiviteter i Odoo for den ansvarlige, etter ja:
`hent_aktivitetstyper()` og så
`planlegg_aktivitet(model="res.partner", res_id=<selskapets partner>, activity_type_id=<gjøremål>, summary=<frist>, date_deadline=<dato>, user_id=<ansvarlig>)`.
Gjør det for én frist om gangen, eller for en liste brukeren har godkjent.

## Ansvar

Kalenderen er en hjelp, ikke en garanti. Endringer i regelverket og
individuelle avtaler med Skatteetaten (for eksempel utsatt frist via
regnskapsfører) går foran. Si det kort når du viser fristene første gang.
