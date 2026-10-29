---
name: sms-innboks
description: Går gjennom innkommende SMS-svar til selskapets nummer som må følges opp, foreslår svar og sender dem i samme tråd etter forhåndsvisning og godkjenning. Bruk denne når brukeren vil sjekke SMS-innboksen, se hva kunder har svart på SMS, svare på en SMS, eller rydde i «Må følges opp».
---

# SMS-innboks

SMS fra Odoo sendes fra selskapets nummer, og svarene kommer inn i Odoo. Et
svar kobles til posten SMS-en ble sendt fra (kunde, oppgave, sak), står som
notat i chatteren der, og gir den som sendte SMS-en en aktivitet. Svar som
ikke kan kobles, havner i «Må følges opp».

**Forutsetning:** innkommende SMS er satt opp i Roret, og brukeren er i
gruppen for SMS-svar. Skriveregler: `roret-prinsipper`.

**Sikkerhet:**
- **Send aldri en SMS før brukeren har sett forhåndsvisningen og sagt ja.**
  Claude tar aldri kontakt med kunder på egen hånd.
- **Akutt fare først.** Tyder en melding på fare for liv, helse eller store
  verdier, si det øverst i svaret med en gang, før resten av gjennomgangen.
  Foreslå at noen ringer avsenderen, og ved fare at avsenderen ringer
  nødnummer (110, 112 eller 113).
- **Personvern:** SMS-tekstene er kundedata. Vis dem i samtalen, men kopier
  dem ikke videre uten at brukeren ber om det.

## Steg 1: Hent det som venter

```
hent_innkommende_sms()                                   # «må følges opp» (standard)
hent_innkommende_sms(status="alle", siden="2026-10-01")
hent_innkommende_sms(status="koblet", model="res.partner", res_id=<id>)
```

- Svarer verktøyet med en `note` om at innkommende SMS ikke er satt opp eller
  at tilgang mangler: forklar det og stopp.
- Finnes ikke verktøyet: serveren har ikke funksjonen ennå. Si det.

Svar som er blitt supportsaker, følges opp i saken. Hent dem med
`status="alle"` eller med `hent_supportsaker`.

## Steg 2: Forstå hvert svar

For hvert svar: `fra`, `mobil`, `tekst`, `post`, `kobling`, `helpdesk_sak`.

- **`helpdesk_sak` satt:** les saken:
  `les_chatter(model="helpdesk.ticket", res_id=<sak>)`.
- **`post` satt:** les chatteren for å se hva vi sendte:
  `les_chatter(model=<post.model>, res_id=<post.id>)`. Er `kobling` lik
  `"nummer"`, ble svaret koblet på telefonnummer, ikke på meldingen. Sjekk at
  det gjelder riktig post før du svarer.
- **Verken sak eller post:** slå opp nummeret selv (`finn_kunde` søker ikke
  på telefon):
  `odoo_search_read("res.partner", [["phone_sanitized", "=", <mobil>]], ["name", "parent_id"])`.
  Ingen treff: ukjent avsender. Flere treff: spør brukeren.

## Steg 3: Oversikt

| Mottatt | Fra | Tekst (kort) | Gjelder | Forslag |
|---|---|---|---|---|

Forslag per svar:
- **Svar:** spørsmål eller noe som venter på oss.
- **Kvitter ut:** «ok», «takk», «mottatt».
- **Til en person:** krever handling (besøk, fakturaendring, klage).

## Steg 4: Svartekster

- Kort, på norsk, avsluttet med selskapets navn (fra `firmaprofil`).
- Lov ikke noe som ikke er avklart (tidspunkt, kreditering, rabatt).
- Fakturaspørsmål: si at økonomi tar kontakt, og lag en aktivitet (steg 7).

## Steg 5: Forhåndsvis

```
svar_pa_sms(svar_id=<id>, body=<tekst>)       # dry_run=True er standard
```

Vis mottaker (`resolved_recipients`), teksten og hvor SMS-en logges
(`logget_pa`). **Vent på et tydelig ja.**

## Steg 6: Send

```
svar_pa_sms(svar_id=<id>, body=<tekst>, dry_run=False)
```

Svaret krysses av som behandlet når SMS-en er sendt. Bruk
`marker_behandlet=False` hvis det skal bli stående i «Må følges opp».

## Steg 7: Kvitter ut eller send videre

- Svar som ikke trenger respons: vis lista og, etter ja,
  `marker_sms_behandlet(svar_ids=[...])`.
- Må en person gjøre noe: `planlegg_aktivitet` på posten eller saken med
  SMS-teksten i notatet, og kvitter så ut svaret.
- Angre: `marker_sms_behandlet(svar_ids=[...], behandlet=False)`.

## Når brukeren gir fri hånd

Sier brukeren uttrykkelig «kvitter ut alle ok-svarene», kan du vise ett
sammendrag («Kvitterer ut 6 svar og sender 2 SMS, bekreft?») og gjøre det
etter én bekreftelse. Noe som går til en kunde, krever alltid minst den ene
bekreftelsen.

## Spesialtilfeller

- **«STOPP» eller avmelding:** ikke svar. Kvitter ut, og si at kontakten bør
  tas ut av fremtidige utsendelser i Odoo.
- **Flere SMS fra samme nummer:** svar én gang.
- **Uten avsendernummer:** kan bare kvitteres ut.
- **Utenlandsk nummer:** `svar_pa_sms` avviser numre som ikke er norske
  mobilnumre. Foreslå at noen ringer.
- **Tilgangsfeil:** brukeren mangler gruppen for SMS-svar. En administrator
  kan legge den til.
