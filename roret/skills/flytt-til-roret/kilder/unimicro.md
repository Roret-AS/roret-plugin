# Flytte fra Uni Micro

**Vilkår, frister og priser** for oppsigelse og lesetilgang er hentet fra
leverandørens sider per oktober 2026. Sjekk vilkårene i kundens egen avtale
før noe sies opp. Data som ikke er lastet ned før tilgangen stenges, kan
være borte.

## Finn ut hvilken variant kunden har

Flere regnskapsprogram bygger på Uni Micro. Spør hvor kunden logger inn:

| Variant | Kjennetegn |
|---|---|
| Unimicro (tidligere Uni Economy) | Nettleser, kjøpt direkte av Uni Micro |
| DNB Regnskap | Regnskapet «i banken» hos DNB |
| SpareBank 1 Regnskap | Regnskapet hos en SpareBank 1-bank |
| Eika Regnskap | Regnskapet hos en Eika-bank |
| Unimicro V3 | Installert på PC eller server (Windows), eldre system med egne rutiner |

Skyvariantene deler plattform og eksport, men menyene, pakkene og
avslutningsvilkårene er ulike. Rapportene ligger for eksempel under
Nøkkeltall → Rapporter i Unimicro, men under Annet → Rapporter i DNB Regnskap
og SpareBank 1 Regnskap. Spør også hvilken pakke kunden har (Basis, Pluss
eller Komplett), fordi noen eksporter krever en bestemt pakke. Eier byrået
lisensen, må byrået gjøre eksporten og avslutningen.

## Før eksporten

- Kunden må være **administrator**. Bare administrator kan eksportere SAF-T.
- **«Avslutt selskap» sletter selskapet med en gang.** Alt må lastes ned først.
- Sikkerhetskopien som tilbys ved avslutning, er ikke en fil kunden får, men
  én gjenoppretting hos Uni Micro. Den er en ekstra sikring, ikke arkivet. Hos
  DNB må den velges i avslutningsveiviseren og kan ikke kjøpes etterpå.
- Lås grunnlaget: lever MVA for siste termin, lever siste a-melding og hent
  tilbakemeldingen, avstem bank, kunder (1500) og leverandører (2400), og rett
  bilagsdifferanser.

## Eksportpakken

1. **SAF-T versjon 1.30 for hvert regnskapsår:** Innstillinger →
   Importsentral → Eksport SAF-T. Fila sendes zippet på e-post. Kontoene må
   være koblet til en SAF-T-gruppe. I V3 ligger eksporten under «Periodiske
   rutiner».
2. **Saldobalanse per byttedato og per 31.12. i fjor,** som Excel og PDF. Bruk
   visningen «Oversikt» og ekspander alle grupper før eksport, ellers kan fila
   bli tom.
3. **Hovedbok eller posteringsjournal per år** (PDF og Excel).
4. **Åpne poster for kunder og leverandører per byttedato:** Rapporter →
   Regnskap → Kontoutskrifter, med fakturanummer, forfall og restbeløp. Mangler
   KID, ta den fra fakturalisten.
5. **Kunder og leverandører:** Importsentral → «Last ned mal» → huk av for
   «Inkluder eksisterende». Det gir e-post og adresser, som ikke er med i
   SAF-T.
6. **Produkter og eiendeler:** samme vei i Importsentral (Produkt, Eiendeler).
7. **Alle utgående fakturaer:** Salg → Faktura → Eksporter, og PDF-ene. Ta også
   en oversikt over repeterende fakturaer, åpne ordre og tilbud.
8. **MVA-historikk:** Regnskap → ⋮ → «Vis tidligere mva-meldinger». Lagre hver
   melding som PDF.
9. **Lønn** (hvis lønn kjøres i Unimicro): lønnsslipper, hittil i år per
   ansatt, feriepengeliste med grunnlag og a-meldingsavstemming for hele året,
   fra fanen Lønn under rapportene. Ta også ansatte og lønnsarter som Excel.
10. **Vedlegg:** skyvariantene kan ikke laste ned alle vedlegg samlet, bare
    ett og ett per bilag. Ta i det minste vedleggene for åpne poster og for
    inneværende år. V3 har «Lagre alle på disk». Ta vare på EHF-filene (XML)
    der det går.

## Særtrekk ved Uni Micro

- Uni Micros egen SAF-T-import tar ikke med MVA-kodene. Det sier noe om hvor
  lite formatet bærer av MVA. Bytt etter en levert termin.
- Lønn: arbeidsforholds-ID må videreføres likt, ellers får a-meldingen avvik.
  Åpne permisjoner legges inn manuelt.

## Før du sier opp

- [ ] Variant, pakke og hvem som eier lisensen er avklart, og kunden er
      administrator.
- [ ] Eksportpakken er lastet ned og kontrollert, og summene stemmer.
- [ ] MVA for siste termin er levert og betalt fra Unimicro.
- [ ] Siste a-melding er levert, og arbeidsforholds-ID-ene er notert.
- [ ] **EHF** er deaktivert under Markedsplass → Produktkjøp. Vent omtrent ett
      døgn til Peppol-katalogen er oppdatert før Roret registrerer.
- [ ] **Autobank:** filoverføringen er avsluttet i nettbanken, og det er
      opprettet en supportsak hos Uni Micro (org.nr, kontonummer, navn). Med en
      bankvariant: avtal med banken hvordan integrasjonen flyttes.
- [ ] Banken har fått beskjed om ny mottaker av OCR/KID-filene, og AvtaleGiro
      og eFaktura er flyttet.
- [ ] Tredjepartsintegrasjoner og tilleggsprodukter er avsluttet.
- [ ] Uni Micros tilgang i Altinn er trukket tilbake etter siste innsending.
- [ ] Sikkerhetskopi er valgt i avslutningsveiviseren, hvis kunden vil ha den.
- [ ] Oppsigelsen er sendt. Unimicro direkte: e-post til
      administrasjon@unimicro.no med ønsket sluttdato. DNB: «Avslutt selskap».
      SpareBank 1: skjema (tilgangen opphører 7 dager etter sluttdato).
- [ ] **«Avslutt selskap» trykkes sist.** Selskapet slettes straks.
