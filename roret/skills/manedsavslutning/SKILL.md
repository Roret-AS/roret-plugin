---
name: manedsavslutning
description: Arbeidsflyt for å lukke en måned i regnskapet, steg for steg med godkjenning før hvert neste steg — bankavstemming, innboks og bilag, utkast, uavstemte betalinger, arkiv, MVA-kontroll og resultat, til slutt månedsrapporten. Bruk denne når brukeren vil avslutte måneden, lukke perioden, gjøre månedsavslutning eller «month-end», eller spør hva som gjenstår før måneden er ferdig.
---

# Månedsavslutning

En sjekkliste brukeren går gjennom sammen med deg. Hvert steg: hent status,
vis den kort, foreslå hva som bør gjøres, og **spør før dere går videre**.
Brukeren kan hoppe over et steg. Noter i så fall det i oppsummeringen.

Før start: bruk `firmaprofil` for selskap, og bli enige om måneden (standard:
forrige måned). Regn ut `date_from` (første dag) og `date_to` (siste dag).

## Steg 1: Bank

```
hent_uavstemte_banklinjer(company_id=<id>, date_to="<date_to>", limit=100)
```

Status: antall og sum per bankkonto. Mål: null uavstemte linjer i måneden.
Er det linjer igjen, tilby å ta dem med `avstem-bank`-skillen nå.

Sjekk også at banksaldoen i Odoo stemmer med kontoutskriften på siste dag:
`likvidbeholdning(company_id=<id>, as_of_date="<date_to>")`. Be brukeren
bekrefte mot nettbanken. `balance` er i selskapets valuta. En bankkonto i
valuta har saldoen slik banken viser den i `balance_in_account_currency`
(med `account_currency`): det er den som skal stemme med kontoutskriften.

→ «Bank er ferdig / har N linjer igjen. Gå videre til bilag?»

## Steg 2: Innboks og mottatte bilag

```
hent_dokumenter(company_id=<id>, only_inbox=True, only_unfiled=True, limit=50)
```

Status: dokumenter som ikke er behandlet. Bilag fra måneden som ligger i
innboksen, mangler i regnskapet. Tilby `bokfor-bilag`.

→ Spør før neste steg.

## Steg 3: Utkast

```
hent_utkastfakturaer(company_id=<id>, limit=100)
```

Status: utkast med dato i måneden, både kunde- og leverandørfakturaer.
For hvert: skal det bokføres, rettes eller slettes? Bokføring og sletting
følger `roret-prinsipper` §2.

→ Spør før neste steg.

## Steg 4: Uavstemte betalinger

```
hent_uavstemte_betalinger(company_id=<id>, limit=100)
```

Status: betalinger registrert i Odoo som ikke er avstemt mot bank. Ofte en
dobbeltregistrering eller en betaling som skal matches mot en banklinje.

→ Spør før neste steg.

## Steg 5: Arkiv

```
hent_uarkiverte_vedlegg(res_model="account.move", since_date="<date_from>", limit=50, company_id=<id>)
```

Status: bilag med vedlegg som ikke ligger i dokumentarkivet. Tilby å arkivere
dem med `arkiver_vedlegg` (`bokfor-bilag` steg 5). Sjekk også at
leverandørfakturaer i måneden har vedlegg i det hele tatt.

→ Spør før neste steg.

## Steg 6: MVA-kontroll

```
mva_sammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>)
```

Sammenlign med forrige måned og se etter det som skiller seg ut: en MVA-kode
som plutselig er tom, store beløp uten MVA, kjøp fra utlandet uten snudd
avregning. `base` er grunnlaget per kode. Salg til utlandet (kode 52, 0 %)
har ingen avgift og står bare med grunnlaget. Er `sales_without_tax_code`
over null, finnes det salgsfakturalinjer uten MVA-kode (en linje uten
produkt får ingen kode av seg selv). De kommer ikke med i MVA-meldingen før
koden er satt, så vis dem og spør. Er dette siste måned i en MVA-termin, gå
videre med `mva-termin`-skillen.

→ Spør før neste steg.

## Steg 7: Resultat og periodisering

```
resultatsammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>, detail_by_account=True)
```

Se etter det som mangler eller er dobbelt: husleie, lønn, avskrivninger,
forsikring og abonnementer som pleier å komme hver måned. Spør brukeren om
periodiseringer (forskuddsbetalt, påløpt) som skal føres. Selve
periodiseringen gjør brukeren eller regnskapsføreren i Odoo.

Har selskapet bankkontoer, fordringer eller gjeld i valuta, spør om de skal
omvurderes til kursen på siste dag. Ved årets slutt skal de det
(regnskapsloven § 5-9, bekreft med `lov_oppslag`). Roret regner ikke ut
omvurderingen selv ennå: regnskapsføreren fører den som et bilag i Odoo, og
reverserer det første dag i neste periode.

→ Spør om dere skal lage rapporten.

## Steg 8: Månedsrapport og oppsummering

Lag rapporten med `manedsrapport`-skillen for samme måned og selskap.
Avslutt med en sjekkliste:

```
## Månedsavslutning <måned> — <selskap>
- [x] Bank avstemt (saldo bekreftet mot nettbanken)
- [x] Innboks tom
- [ ] 2 utkast står igjen (leverandør X, Y), venter på svar
- [x] Ingen uavstemte betalinger
- [x] Vedlegg arkivert
- [x] MVA uten avvik
- [ ] Periodisering av forsikring, regnskapsfører tar det
```

Foreslå at perioden låses når alt er ferdig (låsedato for regnskapet og for
MVA). Det krever rollen Regnskap: Administrator. Roret-kunder ber Roret
(support@roret.no) om å sette datoen, og i Roret for Odoo gjør administratoren
hos bedriften det under Regnskap → Konfigurasjon → Innstillinger. Les datoene
tilbake etterpå:
`odoo_search_read("res.company", [["id", "=", <id>]], ["fiscalyear_lock_date", "tax_lock_date"])`.
