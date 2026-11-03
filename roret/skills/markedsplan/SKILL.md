---
name: markedsplan
description: Fyller markedsprofilen i Roret i en samtale — tilbudene, målgruppene, budskapet og tonen, konkurrentene, kanalene, budsjettet, avsenderen, årshjulet og målene — og foreslår den for godkjenning. Bruk denne når brukeren vil sette opp markedsføringen, lage en markedsplan, endre tonen, målgruppene eller budsjettet, eller når markedsprofil svarer false.
---

# Markedsplan

Markedsprofilen er det Assistent vet om selskapets markedsføring: hvem vi
selger hva til, hva vi sier, i hvilken tone, i hvilke kanaler og for hvor
mye. Alle de andre markedsskillene leser den først. Her fyller du den i en
samtale med brukeren, og foreslår den. Et menneske med ansvaret for
markedsføringen godkjenner før noe lagres.

Krever Markedsføring i Roret. Svarer verktøyene at det mangler, si det kort
og stopp. Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Steg 1: Hva finnes

```
markedsprofil(company_id=<id>)
```

`false` betyr at selskapet ikke har noen profil. Da går du gjennom alle
delene under. Finnes den, vis kort hva som står, og spør hva brukeren vil
endre. Gå bare gjennom de delene.

## Steg 2: Intervjuet

Én del om gangen, med korte spørsmål. Kom med et utkast brukeren kan rette,
i stedet for å spørre åpent. Utkastene lager du av det Roret allerede vet:

- **Tilbudene:** hva som selger, fra
  `salgssammendrag(date_from=<12 mnd siden>, date_to=<i dag>, company_id=<id>)`
  og produktene i
  `odoo_search_read("product.template", [["sale_ok", "=", True]], ["id", "name", "list_price"])`.
  Spør hvilke som skal markedsføres, og hva som er nytt eller i pakker.
- **Målgruppene:** foreslå dem ut fra de største kundene,
  `toppkunder(date_from=<12 mnd siden>, date_to=<i dag>, company_id=<id>, limit=10)`.
  For hver: bedrift eller forbruker, bransje (NACE-koden fra
  `sok_i_enhetsregisteret`), størrelse, sted, hvem vi snakker med, og
  problemet de har.
- **Budskapet:** verdiforslaget i én eller to setninger, og tre til fem
  hovedbudskap.
- **Tonen:** hva vi gjør og ikke gjør når vi skriver, og ord vi ikke bruker.
  Be om én eller to tekster brukeren liker (fra nettsiden eller et tidligere
  nyhetsbrev). De blir eksempeltekstene.
- **Konkurrentene:** navn, nettsted, og hva som skiller oss fra dem.
- **Kanalene:** linkedin, facebook, instagram, google, nyhetsbrev, sms,
  nettsted, arrangement eller annet. Hva hver brukes til, og tonen når den
  skiller seg fra hovedtonen.
- **Budsjettet:** per kanal og måned, for de neste månedene.
- **Avsenderen:** navnet og adressen nyhetsbrevene sendes fra. Adressen bør
  være på selskapets eget domene.
- **Årshjulet:** sesonger, messer og kampanjeperioder, med datoer.
- **Målene:** enkle mål med tall. Har selskapet Styring, les målene der først
  (`maal-og-strategi`) og skriv bare det som gjelder markedsføringen.

## Steg 3: Vis utkastet

Vis hele profilen kort, del for del, og spør om noe skal rettes. Skriv ikke
inn personopplysninger om kunder i profilen. Den beskriver grupper, ikke
personer.

## Steg 4: Foreslå profilen

Etter ja, send delene som er nye eller endret. Hver del erstatter samme del
i profilen, og en liste erstattes helt, så send hele lista:

```
oppdater_markedsprofil(company_id=<id>, endringer={
  "tilbud": {"beskrivelse": "...", "produkt_ids": [<id>]},
  "maalgrupper": [{"navn": "Borettslag", "kundetype": "bedrift", "nace": ["68.209"],
                   "rolle": "styreleder", "problem": "..."}],
  "budskap": {"verdiforslag": "...", "hovedbudskap": ["...", "..."]},
  "tone": {"gjor": "...", "gjor_ikke": "...", "eksempeltekster": "...",
           "ord_vi_ikke_bruker": ["...", "..."]},
  "konkurrenter": [{"navn": "...", "nettsted": "...", "forskjell": "..."}],
  "kanaler": [{"kanal": "linkedin", "formaal": "...", "tone": "..."}],
  "budsjett": [{"maaned": "2027-03", "kanal": "linkedin", "belop": 5000}],
  "avsender": {"navn": "...", "epost": "..."},
  "aarshjul": [{"navn": "...", "type": "kampanjeperiode", "fra": "2027-09-15",
                "til": "2027-09-22", "gjentas_aarlig": true}],
  "maal": "..."})
```

Svaret er et forslag som venter på godkjenning. Si til brukeren at den
markedsansvarlige godkjenner det i Roret-appen eller i Odoo, og at kortet
viser hva som står nå og hva som blir nytt. Kall ikke verktøyet på nytt for
det samme.

## Rammene for Assistent

Profilen har også rammene for Assistent: et beløpstak per måned og hva
Assistent kan gjøre uten godkjenning. Dem kan du ikke foreslå. Spør om
brukeren vil sette dem, og si at det gjøres i Markedsføring i Odoo. Uten
beløpstak krever alt som koster penger, godkjenning.

## Samtykket

Nyhetsbrev og SMS går bare til dem med samtykke, eller til eksisterende
kunder når vilkårene i markedsføringsloven § 15 tredje ledd er oppfylt.
Spør hvordan selskapet samler inn samtykke (skjemaet på nettsiden) og om
kundene fikk reservere seg da de oppga adressen ved kjøp. Det avgjør hvilke
lister nyhetsbrevene kan gå til (se `nyhetsbrev`).
