---
name: nyhetsbrev
description: Skriver et nyhetsbrev i selskapets tone fra markedsprofilen, lager utkastet i E-postmarkedsføring og sjekker hvem som kan få det etter markedsføringsloven § 15, før det sendes. Bruk denne når brukeren vil skrive eller sende et nyhetsbrev, en kampanje-e-post eller et tilbud på e-post til kunder eller leads.
---

# Nyhetsbrev

Et nyhetsbrev er markedsføring på e-post, og reglene er strenge: det går bare
til dem som har samtykket, eller til eksisterende kunder når vilkårene i
markedsføringsloven § 15 tredje ledd er oppfylt. Samtykkeporten i Roret
avgjør det for hver mottaker når utsendelsen sendes. Din jobb er å skrive
godt, vise brukeren hvem som får brevet og hvorfor, og aldri gå rundt porten.

Krever Markedsføring og E-postmarkedsføring. Selskap: `firmaprofil`.
Skriveregler: `roret-prinsipper`.

## Steg 1: Konteksten

```
markedsprofil(company_id=<id>)
hent_kampanjer(company_id=<id>)
hent_innholdskalender(company_id=<id>)
```

Fra profilen: tonen, budskapet, ordene vi ikke bruker og avsenderen. Fra
kampanjene: kampanjen nyhetsbrevet hører til, og lærdommen fra tidligere
brev. Fra kalenderen: hva som alt er sendt eller planlagt, så brevene ikke
kolliderer.

## Steg 2: Avklar

Tema, mottakere (en liste i E-postmarkedsføring eller leads), kampanje og
når. Spør, hvis det ikke er klart.

## Steg 3: Skriv

Emne, forhåndsvisningstekst og teksten, i tonen fra profilen. Kravene:

- **Hvem det er fra** (ehandelsloven § 9): avsendernavnet og selskapets navn
  skal stå tydelig, i avsenderen og nederst i brevet.
- **At det er markedsføring** (ehandelsloven § 9): det skal gå fram når
  e-posten mottas. Et nyhetsbrev fra en avsender mottakeren kjenner, med et
  emne som sier hva det er («Nyhetsbrev», «Tilbud»), holder normalt. Går
  brevet til eksisterende kunder på unntaket, merker Roret emnet «Reklame:»
  selv.
- **Avmelding** (markedsføringsloven § 15 og personvernforordningen art. 21):
  Odoo legger til lenken for å melde seg av. Fjern den aldri.
- **Bare egne tilsvarende ytelser** til kunder på unntaket: tilbud på det
  kundeforholdet bygger på, ikke på noe helt annet.

Vis utkastet og vent på ja.

## Steg 4: Lag utkastet

Til en liste:

```
lag_nyhetsbrevutkast(emne=<emne>, innhold_html=<html>, liste_ids=[<id>],
                     kampanje_id=<id>, avsender=<"Navn <adresse>">,
                     forhandsvisning=<tekst>, company_id=<id>)
```

Til leads: `lead_ids=[...]` i stedet for `liste_ids`. Utkastet sendes ikke.

## Steg 5: Hvem kan få det

```
mottakere_med_samtykke(mailing_id=<id fra utkastet>, company_id=<id>)
```

Vis `kan_faa`, fordelingen per grunnlag (samtykke og kundeforhold) og hvorfor
resten holdes utenfor (`grunner`). Svaret har bare antall. Hent aldri navn
eller adresser for å sende til dem på andre måter.

- Mange **uten_samtykke**: det er regelen, ikke en feil. Foreslå å samle inn
  samtykke (skjemaet på nettsiden), ikke å sende likevel.
- **uten_bekreftelse**: lista eller utsendelsen er ikke bekreftet for
  unntaket for eksisterende kunder. Det kan bare brukeren bekrefte, i Odoo, og
  bare når vilkårene er oppfylt: adressen er mottatt ved salg, brevet gjelder
  egne tilsvarende ytelser, og kunden fikk reservere seg da adressen ble
  samlet inn. Slå opp `lov_oppslag("markedsføringsloven § 15 tredje ledd")`
  hvis brukeren er i tvil. Du bekrefter aldri på brukerens vegne.

## Steg 6: Send

- **Til en liste:** brukeren sender eller planlegger utsendelsen i
  E-postmarkedsføring i Odoo. Porten avgjør på nytt da.
- **Til leads:** `send_masseutsendelse(subject=..., body_html=..., lead_ids=[...], campaign=<kampanjens navn>, company_id=<id>)`.
  Det blir et forslag som et menneske godkjenner, og kortet viser hvor mange
  som holdes utenfor. Sjekk først med
  `mottakere_med_samtykke(lead_ids=[...], company_id=<id>)`.

Svarer Odoo at nyhetsbrev krever oppsett hos Roret, er serveren for
e-postmarkedsføring ikke satt opp i basen. Da går ingen nyhetsbrev ennå. Si
det, og be brukeren ta kontakt med Roret. Prøv aldri å sende brevet som vanlig
e-post i stedet.

Si aldri at brevet er sendt før det er gjort.

## Etterpå

Åpninger, klikk og avmeldinger:
`hent_epost_engasjement(mailing_id=<id>)`, eller hele kampanjen med
`kampanjeresultat(kampanje_id=<id>)`.
