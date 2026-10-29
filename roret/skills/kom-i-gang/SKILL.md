---
name: kom-i-gang
description: Hjelper en ny bruker i gang med Roret i Claude — logge inn på Roret-koblingen, koble Claude til sin egen Odoo med en engangskode, lese selskapets profil, legge til Microsoft 365 eller Google, og gjøre en første ekte kjøring. Bruk denne når brukeren sier «kom i gang», «sett opp Roret», «koble til Odoo», nettopp har installert pluginen, eller når et roret-verktøy svarer at brukeren ikke er innlogget eller ikke koblet til.
---

# Kom i gang med Roret i Claude

Målet er at brukeren på ti minutter kan stille et spørsmål om sitt eget
regnskap og få svar, med sin egen innlogging. Jobb ett steg om gangen, sjekk
hvor brukeren er, og vent der brukeren må gjøre noe.

**Be aldri om passord, og vis aldri tokens eller nøkler.** Innloggingen skjer
i nettleseren. Odoo-nøkkelen lages i brukerens egen Odoo og sendes derfra
direkte til Rorets server, som lagrer den kryptert. Brukeren limer den aldri
inn, og du ser den aldri.

## Steg 0: Hva slags kunde

Spør hvis det ikke er klart:

- **Roret:** regnskapet ligger hos Roret. Roret har laget brukeren og slår på
  Assistent for den.
- **Roret for Odoo:** bedriften har sin egen Odoo med Rorets moduler.
  Administratoren hos bedriften gir tilgang til Assistent.

Brukeren trenger: et Claude-abonnement som støtter plugins og koblinger, en
innlogging til Roret-koblingen, og at Assistent er slått på for brukeren.

## Steg 1: Logg inn på Roret-koblingen

Pluginen har lagt til koblingen `roret` (`https://mcp.roret.no/mcp`). Første
gang må brukeren logge inn:

1. Åpne innstillingene for koblinger i Claude (Customize eller Settings →
   Connectors, avhengig av versjon), og finn **roret**. I Claude Code: skriv
   `/mcp`, velg **roret** og **Authenticate**.
2. Trykk **Connect** eller **Logg inn**. Nettleseren åpner Rorets
   innloggingsside.
3. Logg inn med brukeren Roret har gitt deg (Roret-kunder), eller med
   jobbkontoen fra Microsoft eller Google hvis innloggingssiden tilbyr det.
   Bruk samme e-postadresse som brukeren din i Odoo. Har Roret gitt et
   midlertidig passord, blir brukeren bedt om å lage et nytt.
4. Godkjenn tilgangen. Koblingen skal nå stå som tilkoblet.

Vent på bekreftelse. Feiler det, se feilsøkingen nederst.

## Steg 2: Er Odoo koblet til?

Prøv et kall som bare leser:

```
odoo_search_read("res.company", [], ["id", "name"])
```

- **Får du selskapene:** hopp til steg 4.
- **Svaret sier at brukeren ikke er koblet til Odoo:** gå til steg 3.
- **401 eller «ikke innlogget»:** innloggingen i steg 1 er ikke fullført.

## Steg 3: Koble Claude til Odoo med en engangskode

```
koble_til_odoo()
```

Verktøyet gir en engangskode som gjelder i 10 minutter. Gi brukeren koden og
denne oppskriften:

1. Åpne Roret (Odoo) i nettleseren og logg inn som deg selv.
2. Trykk på profilbildet øverst til høyre → **Mine innstillinger** → fanen
   **Assistent** → **Åpne Assistent**.
3. Lim inn koden og trykk **Koble til**.
4. Odoo viser hvilken Claude-innlogging koden hører til. **Kontroller at det
   er din** før du bekrefter.

Si dette tydelig: koden skal bare limes inn av brukeren selv, i sin egen
Odoo. Har noen andre sendt deg en kode og bedt deg lime den inn, ikke gjør
det.

E-postadressen på innloggingen i steg 1 må være den samme som på brukeren i
Odoo. Er den ikke det, avviser Odoo koblingen.

**Ser brukeren ikke fanen Assistent:**

- Roret-kunde: Assistent er ikke slått på for brukeren ennå. Be brukeren
  skrive til support@roret.no. Det er Roret som slår det på, ikke
  administratoren hos dere, uansett hva verktøyets svar sier.
- Roret for Odoo: administratoren hos bedriften må gi brukeren tilgang til
  Assistent.

Når brukeren har trykket Koble til, kjør kallet fra steg 2 igjen.

**Flere baser** (regnskapsfører med flere klienter, konsern): finnes
`mine_baser()`, viser den hvilke baser brukeren alt har koblet til. En ny base
kobles med `koble_til_odoo(ny_base=True)` og samme oppskrift i den andre
basens Odoo.

## Steg 4: Les selskapets profil

Bruk `firmaprofil`, og vis profilen kort. Spør om noe ser feil ut. Mangler
MVA-termin eller regnskapsfører, spør nå, så slipper brukeren spørsmålet
senere.

## Steg 5: E-post og kalender (valgfritt)

Bruker bedriften Microsoft 365 eller Google Workspace, kan brukeren legge til
den koblingen i Claude (samme sted som i steg 1) og logge inn med
jobbkontoen. Da kan Claude finne kundehenvendelser i innboksen
(`innboks-til-leads`) og ta med møter i `mandagsbrief`. Roret virker fullt ut
uten.

## Steg 6: En første ekte kjøring

Foreslå én ting ut fra situasjonen, og gjør den med brukeren:

- Kommer bedriften fra et annet regnskapssystem: `flytt-til-roret`.
- Ellers, etter hva brukeren bryr seg mest om: `frister` (hva må gjøres de
  neste ukene), `likviditet` (penger inn og ut), `fredagspuls` (status for
  uka) eller `bokfor-bilag` (innboksen).

## Steg 7: Oppsummer

- **Installert lokalt:** ingenting. Koblingen går til Rorets server over
  HTTPS. Odoo-nøkkelen ligger kryptert hos Roret, og brukes bare til
  brukerens egne kall.
- **Innlogging:** brukeren er logget inn som seg selv. Claude kan bare det
  brukeren selv har lov til i Odoo, og alt Claude gjør, står i loggen med
  brukerens navn.
- **Slik bruker du det:** skriv vanlig norsk («hvem skylder oss penger?»,
  «er vi klare for MVA-meldingen?»), eller bruk navnene som kommandoer,
  for eksempel `/roret:purring`.
- **Koble fra:** si «koble fra Odoo» til Claude (`koble_fra_odoo`), og trykk
  **Koble fra** på fanen Assistent i Roret. Da er begge halvdelene borte.

## Feilsøking

| Symptom | Hva du gjør |
|---|---|
| Koblingen står som «needs authentication» | Gjør steg 1 på nytt |
| 401 eller «invalid_token» | Innloggingen er utløpt. Logg inn på nytt |
| Innloggingssiden godtar ikke brukeren | Roret-kunde: kontakt support@roret.no. Roret for Odoo: administratoren hos dere, eller support@roret.no |
| «Ikke koblet til Odoo» | Steg 3 |
| Koden er utløpt | Kjør `koble_til_odoo()` på nytt. Koden gjelder i 10 minutter |
| Odoo avviser koden fordi e-posten ikke stemmer | Roret-kunde: kontakt support@roret.no. Roret for Odoo: administratoren |
| Fanen Assistent finnes ikke | Se steg 3 |
| Innlogget og koblet til, men verktøyene gir tilgangsfeil | Brukeren mangler en rolle i Odoo. Se `roret-prinsipper` §5 |
| Verktøyene vises ikke i Claude | Lukk Claude helt, åpne igjen, og sjekk koblingen |
