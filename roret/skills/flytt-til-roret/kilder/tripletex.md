# Flytte fra Tripletex

Menystiene under er hentet fra Tripletex' egne hjelpesider, men Tripletex
endrer menyene. Finner kunden ikke et punkt, spør hva de ser, og let etter
samme ord (for eksempel «SAF-T», «Reskontro», «Eksporter»).

**Vilkår, frister og priser** for oppsigelse og lesetilgang er hentet fra
leverandørens sider per oktober 2026. Sjekk vilkårene i kundens egen avtale
før noe sies opp. Data som ikke er lastet ned før tilgangen stenges, kan
være borte.

## Før eksporten

- Kunden må ha administratorrettighet i Tripletex.
- **Oppsigelsestiden er 3 måneder.** Kunden kan eksportere i oppsigelsestiden,
  men må ikke vente til siste dag.
- Tripletex anbefaler å gjøre ferdig årsoppgjøret for siste år i Tripletex før
  kundeforholdet avsluttes.
- Lås grunnlaget: tøm bilagsmottaket (ubokførte bilag er ikke med i SAF-T),
  avstem bank, lever siste MVA-termin og kjør siste lønn i Tripletex.

## Eksportpakken

1. **SAF-T per regnskapsår.** Regnskap → Årsregnskap → Regnskapsoversikt har
   én SAF-T-fil per år (versjon 1.3, og 1.4 der det tilbys). For inneværende
   år fram til byttedatoen: Regnskap → Kontoplan → «Regnskapseksport (SAF-T)»,
   der datoene og versjonen velges. Filene kommer som ZIP. Ta alle år innenfor
   oppbevaringstiden.
2. **Saldobalanse per byttedato** som Excel (Regnskap → Saldobalanse eller
   rapporten med samme navn).
3. **Åpne poster per byttedato:** Regnskap → Reskontro → Kunder, og →
   Leverandører, bare åpne poster. Excel hvis det tilbys, ellers PDF. Se til
   at fakturanummer, forfall, restbeløp og KID er med.
4. **Kunder og leverandører:** Kunde → Kunde/leverandører, filtrer på type,
   last ned som Excel eller CSV.
5. **Produkter:** Produkt → Produkter → «Last ned XLS-fil».
6. **Hovedbok per år** som Excel: Regnskap → Hovedbok. Eksporten viser maks
   1000 poster per side, så bruk korte perioder.
7. **MVA-meldinger:** Regnskap → Mva-meldinger, PDF og «Mva-spesifikasjon med
   posteringer» for hver termin. Eldre terminer ligger under «Mva-meldinger
   før 2022».
8. **Lønn** (hvis lønn kjøres i Tripletex): Lønn → Ansatte til Excel, Lønn →
   Rapporter → Lønnsrapport per år og «hittil i år», og noter
   arbeidsforholds-ID og startdato for hvert arbeidsforhold, og OTP-avtalen.
9. **Bilag med vedlegg:** Bilag → Bilagsoversikt, filtrer per måned, huk av
   alle og velg «Skriv ut valgte bilag». Lagre som PDF. Gjenta for hver måned.
   Tripletex har ingen knapp som laster ned originalfilene samlet.
10. **Resten:** faste fakturaer, prosjekter, anlegg og åpne ordre som liste
    eller skjermbilde.

## Det SAF-T fra Tripletex ikke har

Vedlegg, produktpriser, lønnsdetaljer og innsendte MVA-meldinger. KID, forfall
og fakturanummer per linje er valgfrie felt i SAF-T, så åpne poster tas fra
reskontroen.

## Før du sier opp

- [ ] Eksportpakken er lastet ned, åpnet, kontrollert og lagret to steder.
- [ ] Bilagsmottaket er tomt, og siste periode er avstemt.
- [ ] Siste MVA-melding fra Tripletex er levert, og tilbakemeldingen er hentet.
- [ ] Siste a-melding fra Tripletex er levert. Ingen måned rapporteres fra
      begge systemene. Arbeidsforholds-ID og startdato videreføres likt i Roret.
- [ ] Årsoppgjøret for siste år er avsluttet, eller det er bestemt hvor det
      gjøres.
- [ ] Faste fakturaer i Tripletex er stoppet.
- [ ] Bankintegrasjonen: betalingsoversikten er tom, og avtalen er deaktivert
      (Bank → Innstillinger → Bankavtaler, eller under Mitt abonnement).
- [ ] KID/OCR-avtalen er flyttet via banken, og det er avklart at betalinger
      med gamle KID-er blir gjenkjent.
- [ ] AvtaleGiro og eFaktura er avklart med banken.
- [ ] EHF-mottaket: Tripletex (via Visma AutoInvoice) har avregistrert org.nr i
      Peppol, og Roret har registrert det. Sjekk bilagsmottaket i Tripletex til
      byttet er bekreftet.
- [ ] Tripletex' tilgang i Altinn er trukket tilbake etter siste innsending.
- [ ] Andre integrasjoner (nettbutikk, Vipps, timeføring) er koblet fra, og
      API-nøkler er slettet.
- [ ] Det er bestemt om kunden skal kjøpe lesetilgang (kjøpes per hele år).
      Uten den slettes kontoen tidligst 30 dager etter sluttdato.
- [ ] **Til slutt:** oppsigelsen sendes under Selskap → Mitt abonnement.
