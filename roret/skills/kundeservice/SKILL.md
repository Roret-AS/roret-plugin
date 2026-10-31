---
name: kundeservice
description: Går gjennom åpne supportsaker i Odoo, leser historikken, foreslår svar og sender dem til kunden etter godkjenning. Bruk denne når brukeren vil ta unna kundeservice, se hvilke saker som venter, svare en kunde på en sak, finne saker uten ansvarlig, eller få en oversikt over supporttrykket.
---

# Kundeservice

Saker hentes fra helpdesk-modulen kunden har (OCA `helpdesk_mgmt` eller
Odoos `helpdesk`). Verktøyet velger selv. Har kunden ingen av dem, svarer
verktøyet det, og da kan kundehenvendelser bare følges opp i chatteren på
kunden (`folg-opp`).

Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Steg 1: Hent sakene

```
hent_supportsaker(company_id=<id>, only_open=True, limit=30)
```

Nyttige avgrensninger: `unassigned=True` (uten ansvarlig),
`assigned_to_user_id=<meg>`, `priority=...`, `partner_id=<kunde>`.

## Steg 2: Prioriter

Vis en tabell sortert etter det som haster:

| Sak | Kunde | Emne | Alder | Ansvarlig | Venter på |
|---|---|---|---|---|---|

Løft øverst: høy prioritet, saker uten ansvarlig, og saker der kunden skrev
sist og har ventet lenge. Tyder en henvendelse på fare for liv, helse eller
store verdier, si det øverst med en gang, før resten.

## Steg 3: Forstå saken

```
les_chatter(model="helpdesk.ticket", res_id=<id>, limit=20, include_notifications=False)
```

Trengs mer: kundens fakturaer eller avtaler (`folg-opp` steg 2), vedlegg
(`hent_chatter_vedlegg(model="helpdesk.ticket", res_id=<id>)` og
`les_vedlegg(attachment_id=...)`).

## Steg 4: Foreslå svar

- Kort, vennlig og konkret, på kundens språk (norsk som standard).
- Avslutt med selskapets navn eller brukerens navn, ikke «Claude».
- Lov ikke noe som ikke er avklart: kreditering, rabatt, leveringsdato,
  refusjon. Foreslå heller en aktivitet til den som kan avgjøre.
- Klager og rettigheter (reklamasjon, angrerett): slå opp med `lov_oppslag`
  (forbrukerkjøpsloven, kjøpsloven, angrerettloven) før du skriver noe om
  hva kunden har krav på.

## Steg 5: Send etter godkjenning

E-posten går til alle som følger saken, ikke bare kunden. Hent dem først:
`odoo_search_read("mail.followers", [["res_model", "=", "helpdesk.ticket"], ["res_id", "=", <id>]], ["partner_id"])`.
Vis teksten og alle mottakerne. Etter et tydelig ja, send, og kontroller
`notified_partner_ids` i svaret mot lista:

```
skriv_i_chatter(model="helpdesk.ticket", res_id=<id>, body=<svaret>, as_email=True)
```

Interne notater (til kolleger) sendes med `as_email=False`, som er standard.

Må noen andre gjøre noe:
`planlegg_aktivitet(model="helpdesk.ticket", res_id=<id>, activity_type_id=..., summary=..., user_id=...)`.

## Steg 6: Stadium, ansvarlig og prioritet

Vis stadiene saken kan flyttes til:

```
hent_supportstadier(team_id=<sakens team>, company_id=<id>)
```

Si hva du vil endre (fra hva, til hva), og endre etter ja:

```
oppdater_supportsak(ticket_id=<id>, stage_id=<stadium>, company_id=<id>)
oppdater_supportsak(ticket_id=<id>, user_id=<bruker>, company_id=<id>)
oppdater_supportsak(ticket_id=<id>, unassign=True, priority="2", company_id=<id>)
```

Ansvarlig er en bruker (res.users), ikke en ansatt. Finn id-en på andre
saker i `hent_supportsaker`, eller med
`odoo_search_read("res.users", [["name", "ilike", "<navn>"]], ["id", "name"])`.

Har stadiet `sender_epost_til_kunden`, sender Odoo e-post til kunden når
saken flyttes dit. Verktøyet avviser da kallet. Si det til brukeren, og kall
igjen med `stage_email_ok=True` bare etter et ja til den e-posten.

## Oversikt over supporttrykket

Spør brukeren om trender: tell åpne saker per kunde og per emne fra
`hent_supportsaker`, og pek på kunder med mange saker og emner som går igjen
(kandidater til en hjelpeside eller en produktendring).
