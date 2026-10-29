# Flytte fra PowerOffice Go

Menystiene under er hentet fra PowerOffices egne hjelpesider. Finner kunden
ikke et punkt, spør hva de ser.

**Vilkår, frister og priser** for oppsigelse og lesetilgang er hentet fra
leverandørens sider per oktober 2026. Sjekk vilkårene i kundens egen avtale
før noe sies opp. Data som ikke er lastet ned før tilgangen stenges, kan
være borte.

## Tre veier ut av PowerOffice Go

- **Eksportmodulen:** Meny → Innstillinger → Eksport → «Ny eksport». Typene er
  SAF-T Regnskap, Bilag PDF-er, Regnskapsspesifikasjoner (PDF eller Excel, ett
  år om gangen: hovedbok, bilagsjournal, saldobalanse, reskontroer,
  MVA-spesifikasjon) og Lønnsslipper. Alt leveres som ZIP.
- **«Del»-knappen** nederst i lister og rapporter gir Excel eller CSV med
  kolonnene som vises. Legg til kolonnene du trenger (KID, forfall, org.nr)
  før du eksporterer. Skjulte kolonner kommer ikke med.
- API-et trengs ikke for flyttingen.

## Før eksporten

- Lesetilgangen varer 12 måneder etter oppsigelsen, deretter slettes klienten.
  Eksporter i god tid.
- Lås grunnlaget: bokfør alt til byttedatoen, avstem banken, lever siste
  MVA-termin og a-melding fra Go, og sett låsedato.
- SAF-T-eksporten krever at kontaktperson er fylt inn i Firmainnstillinger, og
  at kontoene er koblet til standardkonto eller næringsspesifikasjon.

## Eksportpakken

1. **SAF-T Regnskap versjon 1.30, én fil per regnskapsår,** og inneværende år
   fram til byttedatoen. Feiler eksporten på store volum, kort ned perioden.
2. **Saldobalanse per byttedato** fra rapporten Saldobalanse via «Del» (Excel),
   og per 31.12. året før til kontroll.
3. **Åpne poster per byttedato:** kundereskontro og leverandørreskontro med
   bare åpne poster, med kolonnene fakturanummer, KID, forfall, beløp og
   restbeløp, via «Del» til Excel. **SAF-T fra PowerOffice har ikke åpne
   poster**, så dette steget kan ikke hoppes over.
4. **Regnskapsspesifikasjoner per år** (Excel) fra eksportmodulen.
5. **Kontoplan og MVA-koder** fra Innstillinger → Kontoplan og → Mva-koder via
   «Del».
6. **Kunder, leverandører og produkter** via «Del», med org.nr, adresser,
   e-post og betalingsbetingelser som kolonner.
7. **Bilag PDF-er, én ZIP per år,** fra eksportmodulen. Merk: en ren EHF uten
   PDF gjengis som PDF etter malen, så XML-originalen er ikke med.
8. **MVA:** kvittering (PDF) for hver innsendt MVA-melding.
9. **Lønn** (hvis lønn kjøres i Go): lønnsslipper fra eksportmodulen,
   sammenstillingsrapport for i år og i fjor, feriepengerapport, faste
   lønnslinjer, liste over lønnsarter, OTP-oppsett, og a-meldingene per
   kjøring.
10. **Resten:** anleggsregister med avskrivning hittil i år, prosjekter,
    ufakturerte timer, avdelinger, repeterende fakturaer, åpne tilbud og ordre.

## Før du sier opp

- [ ] Siste MVA-melding fra Go er levert, og kvittering og tilbakemelding er
      lagret.
- [ ] Siste a-melding fra Go er levert. Det er avklart hvilken måned Roret
      rapporterer først.
- [ ] Eksportpakken er lastet ned, kontrollert og lagret to steder.
- [ ] Repeterende fakturaer i Go er stanset.
- [ ] Fakturanummerserien i Roret starter over siste nummer i Go.
- [ ] **EHF:** fjern haken under Innstillinger → Firmainnstillinger →
      Fakturamottak. Vent noen timer, så kan Roret registrere org.nr som
      mottaker.
- [ ] Leverandører som sender faktura på e-post til Go-adressen, har fått ny
      adresse.
- [ ] **eFaktura** er deaktivert (Fakturainnstillinger → Faktura lev.måte).
      Oppsigelsen går til Nets etter 30 dager.
- [ ] **AvtaleGiro** er avviklet hos Nets **først**, og deretter deaktivert i
      Go. Tilbakestillingen i Go kan ikke angres.
- [ ] Banken leverer OCR/KID-fila til Roret, og gamle KID-er kan matches.
- [ ] Ingen godkjente eller ventende betalinger står igjen i Go.
      Bankkontoene er deaktivert under Innstillinger → Bankkontoer, og
      integrasjonsavtalen er flyttet hos banken.
- [ ] Utvidelser (nettbutikk, kasse, integrasjoner) er fjernet under
      Innstillinger → Utvidelser.
- [ ] PowerOffices tilgang i Altinn er trukket tilbake etter siste innsending.
- [ ] Har kunden regnskapsfører i Go: deaktiveringsdatoen settes så
      regnskapsføreren rekker å bli ferdig.
- [ ] **Til slutt:** avslutt modulene under Innstillinger → System →
      Abonnement. Noter datoen klienten slettes (omtrent 12 måneder etter).
