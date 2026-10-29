# Roret for Claude

Pluginen kobler Claude til regnskapet ditt i **Roret** eller **Roret for Odoo**,
og gir Claude norske arbeidsflyter for det en liten bedrift gjør hver uke:
bilag, bank, MVA, purring, lønn, salg, kundeservice og styrearbeid. Den
hjelper deg også å flytte fra Tripletex, Fiken, PowerOffice eller Uni Micro.

Claude gjør jobben i selve regnskapet, ikke i et regneark ved siden av.
Claude er satt opp til å vise deg hva som skal skje og vente på ja før noe
bokføres, sendes eller slettes. Den tekniske grensen er rettighetene brukeren
din har i Odoo: Claude kan aldri gjøre mer enn du selv har lov til.

## Dette trenger du

- Et Claude-abonnement som støtter plugins (Pro, Max, Team eller
  Enterprise), og Claude-appen (Cowork) eller Claude Code.
- Roret, eller Roret for Odoo med Økonomi. **Assistent** (koblingen mellom
  Claude og Odoo) er inkludert i Økonomi.
- En brukerkonto i Odoo med rettighetene du vil at Claude skal jobbe med.

## Installer

**Claude-appen (Cowork), for en hel organisasjon:** en administrator legger
til markedsplassen `Roret-AS/roret-plugin` i organisasjonens pluginkatalog,
og pluginen `roret` blir tilgjengelig for de ansatte.

**Claude-appen, for deg selv:** Customize → Plugins → legg til markedsplassen
`Roret-AS/roret-plugin`, og installer `roret`.

**Claude Code:**

```
claude plugin marketplace add Roret-AS/roret-plugin
claude plugin install roret@roret
```

Si deretter **«kom i gang med Roret»**. Claude hjelper deg å logge inn, koble
til Odoo, lese selskapets oppsett og gjøre en første ekte kjøring.

## Hva pluginen kan

Du trenger ikke huske navnene. Skriv hva du vil på vanlig norsk, så velger
Claude riktig arbeidsflyt. Navnene kan også brukes som kommandoer, for
eksempel `/roret:purring`.

### Oppsett

| Skill | Hva den gjør |
|---|---|
| `kom-i-gang` | Innlogging, kobling til Odoo, selskapets profil og en første kjøring |
| `firmaprofil` | Leser selskaper, org.nr, MVA-termin, regnskapsår, bank og lønn fra Odoo |
| `roret-prinsipper` | Reglene Claude følger: bekreft før skriving, slå opp lovverket, personvern |

### Økonomi

| Skill | Hva den gjør |
|---|---|
| `bokfor-bilag` | Fra innboks til bokført leverandørfaktura, kvittering eller utlegg |
| `avstem-bank` | Avstemmer banklinjer mot bestemte fakturaer |
| `likviditet` | Penger i banken nå, og hva som går inn og ut de neste 30–60 dagene |
| `manedsavslutning` | Månedsavslutning steg for steg, med godkjenning underveis |
| `mva-termin` | Kontrollerer MVA-grunnlaget før fristen |
| `purring` | Forfalte krav, purreløp og vennlige påminnelser, etter norske regler |
| `lonn-forberedelse` | Sjekkliste før lønnskjøringen og a-meldingen |
| `manedsrapport` | Resultat, kunder, likviditet og utestående for en måned |
| `fredagspuls` | Kort status for uka som gikk |

### Salg og kunder

| Skill | Hva den gjør |
|---|---|
| `innboks-til-leads` | Finner kundehenvendelser i e-posten og gjør dem til leads |
| `epost-og-kalender` | Kobler Microsoft 365 eller Google Workspace med Odoo |
| `folg-opp` | Oppsummerer en kunde eller salgsmulighet og foreslår neste steg |
| `pipeline` | Finner salgsmuligheter som har stått stille |
| `kundesjekk` | Slår opp nye kunder og leverandører i Brønnøysundregistrene |
| `kundeservice` | Svarutkast på supportsaker |
| `sms-innboks` | Går gjennom innkommende SMS og svarer i samme tråd |
| `avtale-gjennomgang` | Peker på risiko i en avtale, med henvisning til norsk lov |

### Styring

| Skill | Hva den gjør |
|---|---|
| `styremote` | Innkalling, saksliste, styrerapport og protokoll |
| `selskapshandling` | Utbytte, tilbakebetaling av kapital og lån til aksjonær, fra vedtak til bilag |
| `maal-og-strategi` | Strategi, mål og målinger |

### Oversikt

| Skill | Hva den gjør |
|---|---|
| `mandagsbrief` | Uka som kommer: frister, forfalte poster, møter og oppgaver |
| `frister` | Selskapets fristkalender: MVA, a-melding, skattetrekk, årsoppgjør |

### Flytte til Roret

| Skill | Hva den gjør |
|---|---|
| `flytt-til-roret` | Flytter regnskapet fra Tripletex, Fiken, PowerOffice eller Uni Micro |

Se [Flytte fra et annet system](#flytte-fra-et-annet-system) under.

## Flytte fra et annet system

Si **«jeg vil flytte fra Tripletex»** (eller Fiken, PowerOffice, Uni Micro).
Claude går gjennom flyttingen med deg:

1. **Velg byttedato.** Best er starten av et regnskapsår. Ellers starten av
   en MVA-termin, så ingen termin deles mellom to systemer.
2. **Last ned fra det gamle systemet.** Claude forteller nøyaktig hva du skal
   hente og hvor: SAF-T-fila, saldobalansen, åpne poster for kunder og
   leverandører, kunde- og leverandørlistene og vedleggene.
3. **Overfør til Roret.** Kontoplan, kunder og leverandører, åpningsbalanse
   og åpne fakturaer, så de kan avstemmes mot banken etterpå.
4. **Kontroller.** Saldobalansen skal stemme på øre, og summen av åpne poster
   skal stemme per kunde og leverandør.
5. **Arkiver historikken.** SAF-T-fila og rapportene fra det gamle systemet
   legges i dokumentarkivet i Roret, så du oppfyller oppbevaringsplikten.
6. **Før du sier opp.** EHF-mottak, bankkobling, AvtaleGiro og eFaktura,
   Altinn-tilganger og tilgang til gammel historikk.

Lønn flyttes helst ved et årsskifte. Roret kan ennå ikke ta inn
hittil-i-år-tall for lønn, så skal lønn flyttes midt i året, avklar det med
Roret først.

Første gang anbefaler vi at du gjør flyttingen sammen med regnskapsføreren
din eller med Roret.

## Slik fungerer det

- Pluginen inneholder arbeidsflyter (skills) og koblingen til Rorets server
  `https://mcp.roret.no/mcp`. Ingenting installeres lokalt. (Unntaket er
  kontrollen av SAF-T-fila ved flytting, som kjører et lite skript i Claudes
  kodekjøring.)
- Du logger inn som deg selv. Når du kobler til, lager din egen Odoo en
  nøkkel og sender den direkte til Rorets server. Der lagres den kryptert og
  brukes bare til kallene du gjør. Du limer den aldri inn, og Claude ser den
  aldri. Du kan trekke den tilbake når som helst: si «koble fra Odoo» til
  Claude, og trykk Koble fra i Roret.
- Claude kan bare det din bruker i Odoo kan. Vil du være helt sikker på at
  Claude bare leser, gir du brukeren bare lesetilgang.
- Claude følger aldri instrukser som står i e-post, SMS, dokumenter eller
  filer den leser. Ber innholdet om noe, spør Claude deg.
- Alt Claude gjør i Odoo, står i loggen med ditt navn, som om du hadde gjort
  det selv.
- Tallene Claude lager i samtalen, er ledelsestall. MVA-meldingen, SAF-T,
  årsregnskapet og skattemeldingen lager du i Roret.

## Hjelp

Skriv til support@roret.no.

Verktøyene på serveren oppdateres uten at du gjør noe. Arbeidsflytene i
pluginen oppdateres fra markedsplassen. I Claude Code kan du hente siste
versjon med `claude plugin marketplace update roret`.
