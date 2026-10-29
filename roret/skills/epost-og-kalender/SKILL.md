---
name: epost-og-kalender
description: Veileder Claude i å bruke e-post, kalender og dokumenter fra Microsoft 365 (Outlook, Teams, SharePoint) eller Google Workspace (Gmail, Kalender, Drive) sammen med Odoo via roret-MCP-en. Bruk denne når en forespørsel krysser e-post eller kalender og Odoo, for eksempel «lag et lead av denne e-posten», «logg tråden på kunden», «møtet med X i morgen — finn salgsmuligheten», eller «legg dokumentet fra SharePoint/Drive på kunden i Odoo».
---

# E-post, kalender og Odoo

Kundens e-post og kalender ligger i Microsoft 365 eller Google Workspace.
Kunder, salg, fakturaer og regnskap ligger i Odoo. Behandle dem som ett
arbeidsmiljø, men vit hvor fasiten er.

## Hva som er fasit hvor

| Hva | Fasit |
|---|---|
| E-post og chat (Teams) | Microsoft 365 / Gmail (lesing via connectoren) |
| Møter med eksterne | Outlook- eller Google-kalenderen |
| Kunder, leads, salgsmuligheter | Odoo (`res.partner`, `crm.lead`) |
| Fakturaer, betalinger, regnskap | Odoo |
| Oppgaver og oppfølging | Odoo-aktiviteter (`mail.activity`) |
| Avtaler og tilbud som dokument | SharePoint/Drive som original, kopi i Odoos dokumentarkiv knyttet til posten |

## Hvilken connector

- **Microsoft 365:** `outlook_email_search`, `outlook_calendar_search`,
  `chat_message_search`, `find_meeting_availability`, `sharepoint_search`,
  `read_resource`.
- **Google Workspace:** connectorens søk i Gmail, Kalender og Drive.

Finnes ingen av dem, si at de kan kobles til under Innstillinger → Connectors.
roret-MCP-en virker fullt ut uten dem.

## Mønstre

### A. E-post → lead

1. Finn e-posten med connectorens søk.
2. `finn_kunde(query=<avsender eller domene>)`.
3. Ny: `opprett_lead(name=..., contact_name=..., email=..., description=<oppsummering>, source="E-post")`.
   Kjent kunde: notat eller oppfølging på kunden i stedet.
   Se `innboks-til-leads` for gjennomgang av hele innboksen.

### B. E-posttråd → notat på kunde eller salgsmulighet

1. Hent tråden.
2. Skriv en kort oppsummering: hvem, når, hva som ble avtalt.
3. `skriv_i_chatter(model="crm.lead", res_id=<id>, body=<oppsummering>)`.
   Standard er internt notat (`as_email=False`). Send aldri som e-post uten
   at brukeren ber om det.

### C. Møte i kalenderen → aktivitet i Odoo

1. Finn møtet i kalenderen.
2. Finn kunden ut fra deltakernes e-post: `finn_kunde(query=<e-post>)`.
3. Hører møtet til en salgsmulighet:
   `hent_aktivitetstyper()` og så
   `planlegg_aktivitet(model="crm.lead", res_id=<id>, activity_type_id=<møte>, summary=<emne>, date_deadline=<møtedato>)`.
4. Etter møtet: `marker_aktivitet_ferdig(activity_id=..., feedback=<kort referat>)`
   og et notat med det som ble avtalt.

Interne møter som skal synes i Odoo-kalenderen:
`opprett_kalenderhendelse(name=..., start=..., stop=..., res_model=..., res_id=...)`.
Den tar lokal tid.

### D. Dokument fra SharePoint/Drive → arkivet i Odoo

1. Finn dokumentet og hent innholdet (`read_resource` i Microsoft 365).
2. `last_opp_dokument(name=<filnavn>, content_base64=<innhold>, res_model=<modell>, res_id=<id>)`.
3. Tilby et kort notat på posten om hva som ble lagt ved.

### E. Teams eller chat → kontekst før en handling

Søk i chat etter kundenavnet før du endrer en salgsmulighet, hvis brukeren
viser til en samtale. Gjengi det relevante kort, ikke hele chatten.

## Regler

- Lesing i e-post og kalender trenger ingen bekreftelse. Alt som oppretter
  eller endrer noe i Odoo, gjør det (`roret-prinsipper` §2).
- Kopier ikke persondata mellom systemene uten grunn. Oppsummer, og fjern
  fødselsnummer, kontonummer og helseopplysninger (`roret-prinsipper` §9).
- Tilgangsfeil i connectoren skyldes lisens eller rettigheter hos
  Microsoft/Google. Formidle feilen og foreslå å spørre IT.
