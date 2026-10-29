---
name: innboks-til-leads
description: Går gjennom e-postinnboksen (Microsoft 365 eller Gmail) etter henvendelser fra mulige kunder, foreslår hvilke som bør bli leads i Odoo CRM, og oppretter dem etter godkjenning. Bruk denne når brukeren vil finne nye leads i e-posten, gjøre kundehenvendelser om til CRM-leads, eller rydde i innboksen for forespørsler som ikke er fulgt opp.
---

# Innboks til leads

Finn kundehenvendelser i e-posten som ikke er i CRM ennå, og gjør dem om til
leads når brukeren sier ja.

**Forutsetninger:** roret-MCP-en og en e-post-connector (Microsoft 365 eller
Gmail) er koblet til. Mangler e-post-connectoren, be brukeren koble den til
under Innstillinger → Connectors og prøve igjen. Skriveregler:
`roret-prinsipper`.

## Steg 1: Periode og selskap

- Periode: det brukeren sa, ellers de siste 7 dagene. Andre vanlige valg er
  «siden mandag», «i dag» og «alle uleste».
- Selskap og eget e-postdomene: fra `firmaprofil`. Domenet brukes til å skille
  ut intern e-post. Har selskapet flere domener, spør.

## Steg 2: Søk i innboksen

Bruk connectorens e-postsøk (`outlook_email_search` for Microsoft 365, Gmails
søk for Google) for perioden. Utelat som standard:

- avsendere på selskapets eget domene
- automatiske avsendere: noreply, no-reply, ikke-svar, postmaster,
  mailer-daemon, nyhetsbrev
- e-post brukeren selv har sendt

Har brukeren egne filtre, gjelder de først.

## Steg 3: Vurder hver e-post

**Trolig en ny kunde:** spør om pris, tilbud, levering, avtale, demo, møte
eller noe selskapet selger. Avsenderen er ikke kjent fra før.

Sjekk alltid om avsenderen finnes:

```
finn_kunde(query=<avsenders e-post, domene eller firmanavn>)
```

**Ikke et nytt lead:**
- Eksisterende kunde: foreslå heller et notat på kunden eller en oppfølging
  på salgsmuligheten (se `folg-opp`).
- Leverandørtilbud, fakturaer, kvitteringer, kampanjer og nyhetsbrev.
- Søknader, samarbeidsforespørsler og annet som ikke er salg (si fra om dem).

## Steg 4: Vis forslagene

Én linje per e-post:

```
1. [Avsender] «[Emne]» — 21. oktober
   Forslag: nytt lead. Kontakt: [navn fra signatur]. Kort: [1–2 setninger]
2. [Avsender] «[Emne]» — 22. oktober
   Finnes fra før: [kundenavn]. Forslag: notat på kunden og en oppfølging
```

## Steg 5: Opprett etter godkjenning

Spør: «Skal jeg opprette leads for 1, 3 og 5?» Opprett aldri noe uten svar.

For hvert godkjent forslag:

```
opprett_lead(name=<kort emne>, partner_name=<firma>, contact_name=<navn>,
             email=<avsender>, phone=<fra signatur>, vat=<org.nr hvis oppgitt>,
             description=<kort oppsummering>, source="E-post",
             company_id=<company_id>)
```

`opprett_lead` sjekker dubletter selv. Svarer den at kunden finnes, bruk
`skriv_i_chatter(model="res.partner", res_id=<id>, body=<oppsummering>)` i
stedet (internt notat), eller `planlegg_aktivitet` hvis noen må ringe.

Oppsummer til slutt: hvor mange leads, hvem som står som ansvarlig, og hvor de
finnes (CRM → Leads).

## Personvern og vedlegg

- Beskrivelsen skal være en oppsummering, ikke hele e-posten. Ta ikke med
  fødselsnummer, kontonummer eller helseopplysninger.
- Vedlegg (forespørsler, tegninger) hentes ikke automatisk. Tilby å laste
  dem opp etterpå med `last_opp_dokument(..., res_model="crm.lead", res_id=<lead>)`.
- Er e-posten på engelsk, skriv beskrivelsen på norsk og nevn at kunden skrev
  engelsk.

## Tilgangsfeil

Å opprette leads krever salgsrollen i Odoo. Får du tilgangsfeil, følg
`roret-prinsipper` §5.
