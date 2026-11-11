---
name: flytt-til-roret
description: Flytter regnskapet fra Tripletex, Fiken, PowerOffice Go eller Uni Micro (også DNB Regnskap, SpareBank 1 Regnskap og Eika Regnskap) til Roret — velger byttedato, forteller nøyaktig hva som skal lastes ned og hvor, kontrollerer SAF-T-fila, overfører kontoplan, kunder, leverandører, åpningsbalanse og åpne fakturaer, avstemmer på øre, arkiverer historikken og går gjennom alt som må gjøres før det gamle systemet sies opp. Bruk denne når brukeren vil bytte til Roret, flytte regnskapet, importere fra et annet regnskapsprogram, har en SAF-T-fil, eller nevner noen av disse systemene.
---

# Flytte til Roret

Flyttingen tar med det regnskapet trenger for å fortsette, og arkiverer
resten:

| Flyttes til Roret | Arkiveres i Roret |
|---|---|
| Kontoplan (avvik og nye kontoer) | SAF-T-filene for alle år i oppbevaringstiden |
| Kunder og leverandører, med bankkonto | Saldobalanse, hovedbok og reskontro som PDF |
| Åpningsbalansen, som ett bilag | MVA-meldinger, årsregnskap og skattemeldinger |
| Åpne fakturaer, med original KID og forfall | Bilag med vedlegg, og EHF-filene (XML) |

Historikken importeres ikke linje for linje. Originalfilene fra det gamle
systemet er dokumentasjonen, og de skal oppbevares uansett.

**Slik jobber du:** ett steg om gangen. Hver ⛔ er et stopp der brukeren ser
hva som skal skje og sier ja før du skriver noe. Følg `roret-prinsipper`.
Kontoplanen, journalene, bilagene, bankkontoene og låsedatoene er låst for
Assistent. Dem fører brukeren i Odoo, og du forbereder listene og
kontrollerer etterpå. Skillen tillater `odoo_create` bare for kundene og
leverandørene i [metode.md](metode.md), alltid etter forhåndsvisning, og
bokføring bare med `bokfor_bilag`. Les metode.md før steg 4.

**Første gang** en bedrift flytter, anbefal å gjøre det sammen med
regnskapsføreren eller Roret (support@roret.no). Det er en engangsjobb der
feil merkes med en gang, men de er tunge å rette etterpå.

## Steg 1: Rammen

1. **Selskap:** bruk `firmaprofil`. Org.nr i SAF-T-fila skal være det samme.
2. **Kildesystem:** Tripletex, Fiken, PowerOffice Go eller Uni Micro. For
   Uni Micro: hvilken variant (se [kilder/unimicro.md](kilder/unimicro.md)).
3. **Byttedato:**
   - **Årsskifte er best.** Regnskapsår, MVA-termin, a-melding og SAF-T følger
     da ett system hver.
   - **Terminstart er nest best** (1. januar, mars, mai, juli, september eller
     november ved vanlige terminer). Da må resultatet hittil i år også med.
   - **Midt i en MVA-termin: anbefal ikke.** Rorets MVA-melding tar bare med
     bilag som er bokført i Roret, så den gamle delen av terminen faller ut.
4. **Siste termin i det gamle systemet:** MVA-meldingen for siste termin før
   byttet skal leveres og MVA-oppgjøret føres der, så MVA-kontoene står i null
   og skylden står på oppgjørskontoen (2740).
5. **Lønn:** byttes ved et månedsskifte, helst ved årsskifte. Roret kan ennå
   ikke ta inn hittil-i-år-tall for lønn, bare inngående feriepenger og
   feriepengegrunnlag per ansatt. Skal lønn flyttes midt i året, avklar det
   med Roret først. Samme a-melding-måned skal aldri sendes fra to systemer,
   og arbeidsforholds-ID-ene må videreføres likt.
6. **Årsoppgjøret for siste år i det gamle systemet:** er det ikke ferdig,
   blir åpningsbalansen foreløpig, og det kommer et korreksjonsbilag senere.
   Kunden må beholde tilgang til det gamle systemet til årsregnskap og
   skattemelding er levert.
7. **Rettigheter:** opprette kontoer, journaler og låsedatoer krever rollen
   Regnskap: Administrator, og å godkjenne bankkontoer for utbetaling krever
   en egen rett. Mangler brukeren dem: Roret-kunder ber Roret
   (support@roret.no), og i Roret for Odoo gjør administratoren hos bedriften
   de stegene.

⛔ Oppsummer rammen (selskap, kilde, byttedato, lønn med eller ikke) og få ja.

## Steg 2: Last ned fra det gamle systemet

Les kildeveiledningen og gå gjennom eksportpakken med brukeren:
[Tripletex](kilder/tripletex.md) · [Fiken](kilder/fiken.md) ·
[PowerOffice Go](kilder/poweroffice.md) · [Uni Micro](kilder/unimicro.md).
Menystiene er hentet fra leverandørenes hjelpesider og kan ha endret seg.
Spør hva brukeren ser hvis et punkt ikke finnes.

Dette må du ha før du går videre:

- **SAF-T** fram til dagen før byttedatoen: for siste hele år ved bytte ved
  årsskifte, og for inneværende år fram til byttet ved bytte midt i året. I
  tillegg én fil for hvert tidligere år i oppbevaringstiden (til arkivet).
- **Åpne poster per faktura** for kunder og leverandører per dagen før
  byttedatoen, som Excel eller CSV: fakturanummer, KID, fakturadato, forfall,
  restbeløp og valuta. SAF-T kan ikke erstatte denne lista.
- **Saldobalanse** per samme dato (PDF eller Excel).
- **Ved bytte midt i året:** bevegelsen per konto for hver måned i år fram
  til byttet, som Excel. Det kan være én saldobalanse per måned, eller en
  resultatrapport med én kolonne per måned. Den blir månedsbilagene i
  åpningsbalansen ([metode.md](metode.md), steg 10).
- **Kunde- og leverandørlisten** som Excel, med e-post, telefon og
  leverandørenes bankkonto.
- **Bilag med vedlegg** og EHF-filene, til arkivet.

## Steg 3: Kontroller SAF-T-fila i Roret

SAF-T-fila er for stor til å limes inn i samtalen, så Roret leser den.
Brukeren gjør det i **Flytt regnskapsåret**. Der leses fila på serveren, den
arkiveres i dokumentarkivet med sjekksum, og den kontrolleres i en
prøvekjøring. Prøvekjøringen skriver ingenting i regnskapet.

1. Brukeren åpner Regnskap → Bokføring → Flytt regnskapsåret, lager en ny
   kjøring, laster opp SAF-T-fila slik det gamle systemet lagde den (XML
   eller ZIP) og trykker «Les fila».
2. Under «Valg» settes «Ta med bilag til og med» til dagen før byttedatoen,
   og «MVA-meldingen er levert fra det gamle systemet til og med» til siste
   termin som er levert derfra. Så trykker brukeren «Start prøvekjøringen».
3. **Aldri «Importer nå» i denne flyttingen.** Den knappen fører hvert bilag
   i fila inn i Roret, og sammen med åpningsbalansen blir da alt ført to
   ganger. Å importere hele regnskapsåret er en annen vei, som Roret hjelper
   med.
4. La kjøringen stå til avstemmingen i steg 12 er godkjent. Steg 4–12 leser
   grunnlaget fra den. Roret sletter grunnlaget i en kjøring ingen har endret
   på 30 dager, og setter den til «Forkastet». At du leser den, teller ikke
   som en endring. Sjekk `tilstand` hver gang du leser grunnlaget. Er den
   `forkastet`, må fila leses i en ny kjøring.

Finnes ikke menyvalget, er funksjonen ikke slått på. Roret-kunder ber Roret
om det (support@roret.no). Brukeren trenger rollen Regnskap.

Når statusen er «Prøvekjøringen er klar», leser du kjøringen og avvikene.
`<K>` er kjøringens id:

```
odoo_search_read("roret.migrering.kjoring", [["kilde", "=", "saft"], ["company_id", "=", <C>]], ["id", "tilstand", "saft_versjon", "saft_orgnr", "saft_selskap", "saft_kildesystem", "saft_fra", "saft_til", "saft_antall_bilag", "saft_dokument_id", "tellinger_prove"], order="id desc", limit=1, company_id=<C>)
odoo_search_read("roret.migrering.avvik", [["kjoring_id", "=", <K>]], ["alvor", "type", "ekstern_id", "melding"], limit=200, company_id=<C>)
```

`tellinger_prove` har lista `kontroller`, der hver kontroll har `navn`, `ok`
og `tekst`. Kontrollene sjekker at hvert bilag går i null, at antall bilag og
sum debet stemmer med fila, og at inngående saldo pluss bilagene er lik
utgående saldo per konto og per kunde og leverandør. De sjekker også at
saldobalansen går i null og at reskontroen stemmer med hovedboken.

⛔ Stopp ved avvik: org.nr i fila (`saft_orgnr`) er ikke selskapets, en
kontroll har `ok` lik false, eller perioden (`saft_fra`–`saft_til`) slutter
ikke dagen før byttedatoen. Forklar avviket. Be brukeren rette det i det
gamle systemet, ta ut fila på nytt og lese den i en ny kjøring.

Grunnlaget for steg 4–12 ligger i prøvekjøringens mellomlager,
`roret.migrering.rad` med `kjoring_id` lik `<K>`. Les én `type` om gangen:

| `type` | `ekstern_id` | I `data` |
|---|---|---|
| `konto` | Kontonummeret | `navn`, `ib` og `ub` (inngående og utgående saldo), `standardkonto`, `gruppekode` |
| `kunde`, `leverandor` | Id-en i det gamle systemet | `navn`, `orgnr`, `mva_nr`, adressen, `epost`, `telefon`, og `saldo` per reskontrokonto med `ib` og `ub` |
| `mva` | MVA-koden i det gamle systemet | `standardkode`, `sats`, `navn` |

```
odoo_search_read("roret.migrering.rad", [["kjoring_id", "=", <K>], ["type", "=", "konto"]], ["ekstern_id", "data", "handling", "maal_id", "melding"], limit=1000, company_id=<C>)
```

`ib` og `ub` er beløp skrevet som tekst. Har en konto `ub` lik `null`, står
den i bilagene, men ikke i kontoplanen i fila, og avvikene sier det samme.
Den er ikke uten saldo. Hent den utgående saldoen fra saldobalansen i steg 2,
og ta kontoen med i kontrollene.

`handling` og `maal_id` viser hva prøvekjøringen fant i Roret:

- `finnes` eller `kobles`, med id-en i Roret.
- `ny` når det ikke finnes. For en konto står den foreslåtte kontotypen da i
  `melding`.
- `feil`: kontoen er arkivert i Roret, eller ingen avgift har MVA-kodens
  standardkode.

Bruk dette som utgangspunkt, og kontroller tabellene i steg 4, 5 og 7 selv.

Åpne poster per faktura står ikke i fila. Det som var åpent ved
periodestart, ligger bare som en sum per partner, og fila sier ikke hvilken
betaling som lukket hvilken faktura. Bruk reskontrolisten fra steg 2.

Kan ikke bedriften bruke Flytt regnskapsåret, be om saldobalansen og
Excel-listene i stedet. Si at SAF-T-fila ikke er kontrollert, og at Roret kan
kontrollere den (support@roret.no).

## Steg 4–13: Overføringen

Følg [metode.md](metode.md). Stoppunktene:

4. **Kontoplanen.** Kildekonto → konto i Roret (finnes, eller ny med foreslått
   type). ⛔ Brukeren godkjenner tabellen og oppretter de nye kontoene i Odoo
   inntil videre. Du leser dem tilbake.
5. **MVA-kodene.** Kildens kode → standardkode → avgift i Roret. ⛔ Godkjenning,
   særlig for koder uten standardkode og delvis fradrag.
6. **Bankkontoer og bankjournaler.** ⛔ Godkjenning. Brukeren oppretter
   bankjournalene som mangler, i Odoo. Du leser dem tilbake.
7. **Kunder og leverandører.** Antall nye, dubletter (sjekk org.nr), og avvik
   mot Enhetsregisteret (`kundesjekk`). ⛔ Godkjenning. Firmaer og kontakter
   med org.nr eller MVA-nummer blir i tillegg forslag som godkjennes i
   Roret-appen eller i Odoo, i bolker på høyst 50.
8. **Leverandørenes bankkontoer.** Brukeren legger dem inn i Odoo inntil
   videre. ⛔ Uttrykkelig ja til at de kan brukes til betaling.
9. **Migreringsjournaler og overgangskonto.** ⛔ Godkjenning. Brukeren
   oppretter journalene i Odoo. Du kontrollerer dem.
10. **Åpningsbalansen** som ett bilag, med kilde per linje og differansen mot
    udisponert resultat. ⛔ Godkjenning av tabellen. Brukeren fører utkastet
    i Odoo, du kontrollerer det og bokfører med `bokfor_bilag` (et forslag).
11. **Åpne fakturaer** med original KID og forfall, uten MVA. Summen per
    partner skal stemme med SAF-T. ⛔ Godkjenning av lista. Brukeren
    importerer den i Odoo, du kontrollerer utkastene før bokføring.
12. **Avstemmingsrapporten** (kontrollene i metode.md). ⛔ Alle grønne, ellers
    forklar og rett. Brukeren, og helst regnskapsføreren, godkjenner.
13. **Lås perioden** før byttedatoen. ⛔ Godkjenning. Brukeren setter
    låsedatoene i Odoo, du leser dem tilbake.

## Steg 14: Arkiver historikken

Store filer lastes opp av brukeren i Rorets dokumentarkiv i nettleseren, ikke
gjennom samtalen. SAF-T-fila fra steg 3 ligger alt i arkivet
(`saft_dokument_id` på kjøringen) og skal ikke lastes opp på nytt. Foreslå mappen «Regnskap og skatt / Historikk <system> /
<år>» med begrenset tilgang, fordi SAF-T inneholder personopplysninger. Finn
filene med `hent_dokumenter` og legg dem riktig med `flytt_dokument`.
`last_opp_dokument` passer bare for små filer, som avstemmingsrapporten.

Oppbevaringstiden er fem år etter regnskapsårets slutt (bokføringsloven
§ 13). Paragrafen er endret fra 1. januar 2027, blant annet om oppbevaring av
elektroniske fakturaer i opprinnelig format, så ta vare på EHF-filene (XML),
ikke bare PDF-ene. Bekreft med `lov_oppslag` («oppbevaring av
regnskapsmateriale») og oppgi paragrafen.

## Steg 15: Før det gamle systemet sies opp

Gå gjennom sjekklista i kildeveiledningen punkt for punkt. Det som angår
Roret:

- **EHF:** det gamle systemet må frigi org.nr i Peppol først. Deretter
  registreres selskapet som EHF-mottaker fra Roret: Roret-kunder sier fra til
  Roret, og i Roret for Odoo gjør administratoren det. Fra 1. januar 2027 må
  bokføringspliktige sende e-faktura til andre bokføringspliktige som kan
  motta det (bekreft med `lov_oppslag`), så EHF bør være på plass fra første
  dag.
- **Bank:** Roret-kunder avtaler bankintegrasjonen med Roret. Inntil den er
  på plass, kan kontoutskrifter (camt.053) lastes ned fra nettbanken og leses
  inn i Odoo.
- **KID:** banken må levere OCR-fila til Roret. De åpne fakturaene har
  beholdt sin opprinnelige KID, så innbetalinger på gamle fakturaer finner
  riktig faktura.
- **Altinn:** det gamle systemets tilgang trekkes tilbake etter siste
  innsending derfra, og Roret får sin.

## Steg 16: Etter første termin i Roret

Sjekk at MVA-meldingen bare har bilag fra Roret, at oppgjørskontoen for MVA
fra åpningsbalansen er avstemt mot betalingen, og at overgangskontoen
fortsatt står i null. Kom åpningsbalansen fra et foreløpig årsoppgjør, før
korreksjonsbilaget når det endelige er levert (metode.md).
