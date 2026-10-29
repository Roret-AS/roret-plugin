---
name: styremote
description: Hjelper daglig leder med styrearbeidet i Roret Styring — oversikt over hva som venter i styret, forberede styremøte eller generalforsamling med saksliste, lage daglig leders rapport til styret med tall fra regnskapet, skrive protokolltekst fra notater eller transkripsjon, og følge opp vedtak og oppfølgingspunkter. Bruk denne når brukeren nevner styremøte, generalforsamling, styrerapport, protokoll, innkalling, vedtak eller «hva venter i styret».
---

# Styremøte og generalforsamling

Styring er en egen funksjon i Roret. Svarer verktøyene at Styring ikke er
installert, eller at brukeren ikke er styresekretær, si det og stopp.
Skriveregler: `roret-prinsipper`. Selskap: `firmaprofil`.

Viktig om ansvar: verktøyene lager **utkast**. Innkalling, stemmegivning,
utfall og signering skjer i Roret av menneskene som har rollen. Du sender
aldri noe til styret.

## Start alltid med oversikten

```
styrets_oversikt(company_id=<id>)
```

Den gir varsler med paragraf i aksjeloven, frister (generalforsamling,
årsregnskap, skattemelding, innkallinger), kommende møter med sjekkliste,
møter som venter på protokoll eller signatur, åpne oppfølgingspunkter og de
siste vedtakene. Vis det viktigste kort, og spør hva brukeren vil gjøre.

## Forberede et møte

1. Avklar type (`meeting_type`: `board` styremøte, `agm` ordinær
   generalforsamling, `egm` ekstraordinær), dato, klokkeslett og om det er
   skriftlig behandling eller forenklet generalforsamling (`written`).
2. Foreslå saksliste: faste saker (`standard_items=True`) og egne saker fra
   det brukeren nevner, åpne oppfølgingspunkter
   (`hent_oppfolgingspunkter(only_open=True)`) og vedtak som ikke er
   gjennomført (`hent_vedtak(only_not_implemented=True)`).
3. Vis sakslisten. Etter ja:

```
opprett_styremote(date=<YYYY-MM-DD>, meeting_type="board", title=<tittel>,
                  start_time=17.5, written=False, standard_items=True,
                  items=[{"title": ..., "kind": "decision", "proposal": ...}],
                  company_id=<id>)
```

`kind` er `decision`, `information` eller `discussion`. Flere saker senere:
`legg_til_styresak(meeting_id=<id>, title=..., kind=..., proposal=...)`.
Innkallingen sender daglig leder selv fra Roret.

Saker med lovkrav (utbytte, kapitalendring, lån til aksjonær): bruk
`selskapshandling`, som lager både styresaken og generalforsamlingen med de
riktige kontrollene.

## Daglig leders rapport til styret

1. `lag_styrerapport(date_from=..., date_to=..., company_id=<id>)` lager et
   utkast med resultat mot fjoråret og budsjett, balanse, likviditet og funn.
   Utelat datoene for perioden siden forrige rapport.
2. `hent_styrerapport(report_id=<id>)` viser funnene og spørsmålene
   (`sporsmal`) som trenger daglig leders forklaring.
3. Hjelp brukeren å formulere forklaringene, og lagre dem etter ja:
   `husk_forklaring(report_id=<id>, explanations=[{"question_id": ..., "explanation": ...}], commentary=...)`.
   Forklaringer huskes og foreslås igjen neste gang.

Rapporten sendes til styret fra Roret, ikke herfra.

## Protokoll

Har brukeren notater eller en transkripsjon fra møtet:

1. `hent_styremote(meeting_id=<id>)` for sakene og deres `item_id`.
2. Skriv nøktern protokolltekst per sak: hva som ble behandlet, og vedtaket
   slik det ble. Ikke legg til noe som ikke står i notatene. Stemmer og utfall
   settes ikke her, de registreres i Roret.
3. Vis teksten. Etter ja:
   `skriv_protokolltekst(meeting_id=<id>, items=[{"item_id": ..., "minutes": ..., "resolution": ...}])`.

Etter at protokollen er sendt til signering, kan ingenting endres.

## Vedtak og oppfølging

- `hent_vedtak(search=..., date_from=..., only_not_implemented=True)`:
  vedtak som ikke er gjennomført.
- `hent_oppfolgingspunkter(only_open=True)`: hva, hvem, frist, forfalt.

Foreslå hva som bør på neste møte, og pek på det som er forfalt.

## Regler og frister

Spørsmål om innkallingsfrister, vedtaksførhet, flertall, habilitet eller
protokollkrav slås opp med `lov_oppslag` (aksjeloven kapittel 5 og 6) og
besvares med paragraf.
