---
name: innlegg
description: Skriver innlegg til LinkedIn, Facebook og Instagram i selskapets tone og legger dem som utkast i innholdskalenderen, klare til å sendes til godkjenning. Bruk denne når brukeren vil lage, planlegge eller fylle opp innlegg i sosiale medier, eller se hva som er planlagt og publisert.
---

# Innlegg

Innleggene planlegges i innholdskalenderen i Markedsføring. Assistent skriver
utkastene. En bruker sender dem til godkjenning, og den markedsansvarlige
godkjenner dem før de publiseres. Et innlegg er offentlig i det det
publiseres, så Assistent publiserer aldri og godkjenner aldri.

Krever Markedsføring. Selskap: `firmaprofil`. Skriveregler:
`roret-prinsipper`.

## Steg 1: Konteksten

```
markedsprofil(company_id=<id>)
hent_innholdskalender(fra=<i dag>, til=<om 30 dager>, company_id=<id>)
```

Fra profilen: tonen, tonen per kanal (`kanaler`), budskapet, ordene vi ikke
bruker og årshjulet. Fra kalenderen: hva som er planlagt, hva som venter på
godkjenning, og hullene. Hører innleggene til en kampanje, hent lenkene med
`kampanjeresultat(kampanje_id=<id>, company_id=<id>)` og bruk dem i teksten.

## Steg 2: Skriv

Foreslå ett til fem innlegg: kanal, tidspunkt og tekst.

- **LinkedIn:** for bedriftskunder. Faglig, gjerne med et tall eller en
  erfaring.
- **Facebook:** for forbrukere og nærmiljøet. Kort og konkret.
- **Instagram:** krever minst ett bilde, og alle bildene må være JPEG.
  Teksten er høyst 2 200 tegn, med høyst 30 emneknagger og 20 omtaler (@).
  Ellers stopper Odoo innlegget når det sendes til godkjenning.
- Skriv i tonen fra profilen, og bruk aldri ordene i `ord_vi_ikke_bruker`.
- **Merking** (markedsføringsloven § 8): på selskapets egen side går det fram
  av sammenhengen at innlegget er markedsføring. Et betalt samarbeid med en
  annen, eller et innlegg på en annens konto, må merkes tydelig som reklame.
- Ikke lov noe selskapet ikke kan holde, og ikke vis kunder eller
  personopplysninger uten at brukeren har bekreftet at det er avklart.

## Steg 3: Bildene

Assistent lager ikke bilder. Finn dem i Odoo, for eksempel i
dokumentarkivet med `finn_dokumenter(query=<tekst>)`, eller blant
vedleggene:
`odoo_search_read("ir.attachment", [["mimetype", "like", "image/"], ["name", "ilike", <tekst>]], ["id", "name"])`.
Til Instagram: bruk `["mimetype", "=", "image/jpeg"]` i stedet. Spør brukeren
når du ikke finner et passende bilde.

## Steg 4: Legg dem i kalenderen

Etter ja, for hvert innlegg:

```
planlegg_innlegg(kanal="linkedin", tekst=<tekst>, planlagt_tid=<"YYYY-MM-DD HH:MM">,
                 kampanje_id=<id>, bilde_ids=[<id>], company_id=<id>)
```

Tiden er norsk tid. Innlegget blir et utkast, med egne kopier av bildene.
Fortell brukeren:

1. Innleggene ligger som utkast i Markedsføring → Innholdskalender.
2. En bruker sender dem til godkjenning der, og den markedsansvarlige
   godkjenner dem.
3. Til kanalene er koblet til Roret, publiserer brukeren selv i kanalen og
   markerer innlegget som publisert med lenken. Da kommer det med i
   statistikken.

## Hva er planlagt og publisert

`hent_innholdskalender(fra=<fra>, til=<til>, company_id=<id>)` viser
innleggene med tilstand (utkast, til_godkjenning, godkjent, publisert,
feilet) og statistikk, og nyhetsbrevene i samme periode.
