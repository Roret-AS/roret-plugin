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
Denne skillen tillater `odoo_create`, `odoo_write` og `odoo_call_button` for
kallene i [metode.md](metode.md),
og bare de, alltid etter forhåndsvisning. Les metode.md før steg 4.

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
- **Kunde- og leverandørlisten** som Excel, med e-post, telefon og
  leverandørenes bankkonto.
- **Bilag med vedlegg** og EHF-filene, til arkivet.

## Steg 3: Kontroller SAF-T-fila

SAF-T-fila er for stor til å limes inn i samtalen. Kontroller den med
skriptet som følger skillen, i kodekjøringen (Claude-appen med fila lastet
opp, eller Claude Code). Skriptet ligger i skillens egen mappe:
`<skillmappa>/scripts/saft_les.py`. Pakk ut ZIP-fila først. Skriptet trenger
lxml. Installer den i et eget miljø, så den ikke blandes med noe annet:

```
python3 -m venv .saft-venv
.saft-venv/bin/pip install lxml
.saft-venv/bin/python -I <skillmappa>/scripts/saft_les.py <fil.xml> --json grunnlag.json
```

Har kodekjøringen lxml fra før, holder det med
`python3 -I <skillmappa>/scripts/saft_les.py <fil.xml> --json grunnlag.json`.

Skriptet skriver ingenting i Roret. Det viser versjon, selskap, periode,
antall kontoer, kunder, leverandører og bilag, og kontrollerer at bilagene
går i null, at totalene stemmer, at inngående saldo pluss bevegelse er lik
utgående per konto og per partner, og at reskontroen stemmer med hovedboken.
`grunnlag.json` har kontoene, partnerne, MVA-kodene og månedssummene som
neste steg trenger.

⛔ Stopp ved avvik: annet org.nr enn selskapet, bilag som ikke går i null,
totaler eller reskontro som ikke stemmer. Forklar avviket og be brukeren
rette det i det gamle systemet og ta ut fila på nytt.

Åpne poster som skriptet utleder av transaksjonene, er bare en kontroll.
Det som var åpent ved periodestart, ligger bare som en sum per partner, og
fila sier ikke hvilken betaling som lukket hvilken faktura. Bruk
reskontrolisten fra steg 2.

Har ikke Claude kodekjøring, be om saldobalansen og Excel-listene i stedet,
og si at kontrollen av fila må gjøres av Roret.

## Steg 4–13: Overføringen

Følg [metode.md](metode.md). Stoppunktene:

4. **Kontoplanen.** Kildekonto → konto i Roret (finnes, eller ny med foreslått
   type). ⛔ Brukeren godkjenner tabellen.
5. **MVA-kodene.** Kildens kode → standardkode → avgift i Roret. ⛔ Godkjenning,
   særlig for koder uten standardkode og delvis fradrag.
6. **Bankkontoer og bankjournaler.** ⛔ Godkjenning.
7. **Kunder og leverandører.** Antall nye, dubletter (sjekk org.nr), og avvik
   mot Enhetsregisteret (`kundesjekk`). ⛔ Godkjenning.
8. **Leverandørenes bankkontoer.** ⛔ Uttrykkelig ja til at de kan brukes til
   betaling.
9. **Migreringsjournaler og overgangskonto.** ⛔ Godkjenning.
10. **Åpningsbalansen** som ett bilag, med kilde per linje og differansen mot
    udisponert resultat. ⛔ Godkjenning før bokføring.
11. **Åpne fakturaer** med original KID og forfall, uten MVA. Summen per
    partner skal stemme med SAF-T. ⛔ Godkjenning av lista før bokføring.
12. **Avstemmingsrapporten** (kontrollene i metode.md). ⛔ Alle grønne, ellers
    forklar og rett. Brukeren, og helst regnskapsføreren, godkjenner.
13. **Lås perioden** før byttedatoen. ⛔ Godkjenning.

## Steg 14: Arkiver historikken

Store filer lastes opp av brukeren i Rorets dokumentarkiv i nettleseren, ikke
gjennom samtalen. Foreslå mappen «Regnskap og skatt / Historikk <system> /
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
