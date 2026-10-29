---
name: folg-opp
description: Leser historikk og åpne oppgaver på en kunde eller salgsmulighet i Odoo, oppsummerer hvor saken står, og foreslår og planlegger neste oppfølging. Bruk denne når brukeren vil følge opp en kunde, en deal eller en salgsmulighet, spør «hvor står vi med X», eller vil planlegge neste kontakt.
---

# Følg opp en kunde eller salgsmulighet

Les alltid historikken før du foreslår noe. Kontekst er hele poenget.
Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Steg 1: Finn posten

- Ga brukeren en id, bruk den.
- Ellers søk både som kunde og som salgsmulighet:
  `finn_kunde(query=<tekst>)` og
  `hent_salgsmuligheter(company_id=<id>, partner_id=<kunde fra søket>, only_open=True)`.
- Flere treff: vis dem og spør hvilken.

## Steg 2: Hent konteksten

Salgsmulighet:

```
les_chatter(model="crm.lead", res_id=<id>, limit=15, include_notifications=False)
hent_aktiviteter(model="crm.lead", res_id=<id>)
```

Kunde:

```
les_chatter(model="res.partner", res_id=<id>, limit=15)
hent_aktiviteter(model="res.partner", res_id=<id>)
odoo_search_read("account.move",
  [["partner_id", "child_of", <id>], ["move_type", "=", "out_invoice"],
   ["state", "=", "posted"], ["payment_state", "in", ["not_paid", "partial"]]],
  ["name", "invoice_date", "invoice_date_due", "amount_residual"])
```

Er e-post eller kalender koblet til, kan siste kontakt ligge der i stedet for
i Odoo. Søk på kundens e-postadresse (se `epost-og-kalender`).

## Steg 3: Oppsummer

```
## <Navn>
**Siste kontakt:** 14. oktober — kunden ba om nytt tilbud med færre lisenser
**Status:** Tilbud sendt, 60 %, forventet 120 000 kr, lukking 15. november
**Åpent:** 2 forfalte fakturaer, 18 400 kr (eldste 34 dager)
**Oppgaver:** Ring innkjøper, frist i går
**Forslag:**
1. Ring innkjøper i dag og avklar lisensantall
2. Send purring på faktura 2026/0142 (se `purring`)
```

Pekepinner:
- Er siste melding fra kunden, og den venter på oss: svar først.
- Stille i to uker eller mer: si at saken kan være i ferd med å kjølne.
- Forfalte fakturaer hos en kunde du skal selge mer til: nevn det.

## Steg 4: Hjelp brukeren å handle

Spør hva brukeren vil:

- **Notat eller e-post** på posten:
  `skriv_i_chatter(model=..., res_id=..., body=...)`. Standard er internt
  notat. `as_email=True` sender e-post til alle som følger posten, ikke bare
  kunden, og krever eget ja. Vis mottakerne først, slik `roret-prinsipper` §2
  beskriver.
- **Planlegge en aktivitet:** `hent_aktivitetstyper()` og så
  `planlegg_aktivitet(model=..., res_id=..., activity_type_id=..., summary=..., date_deadline=..., user_id=...)`.
- **SMS:** `send_sms(model=..., res_id=..., body=..., dry_run=True)`, vis
  mottakerne, og send med `dry_run=False` etter ja.
- **Oppdatere salgsmuligheten:**
  `oppdater_salgsmulighet(lead_id=..., probability=..., expected_revenue=..., stage_id=..., expected_closing=...)`.
- **Bare informasjon:** ingenting endres.
