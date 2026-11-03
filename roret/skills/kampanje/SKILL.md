---
name: kampanje
description: Planlegger en markedskampanje med mål, budsjett, kanaler, periode og sporingslenker, ut fra markedsprofilen og lærdommen fra tidligere kampanjer, og foreslår den for godkjenning. Følger opp med tallene underveis og lærdommen etterpå. Bruk denne når brukeren vil lage, planlegge, følge opp eller evaluere en kampanje.
---

# Kampanje

En kampanje i Roret er et navn i sporingslenkene (UTM) og en plan: mål,
budsjett, kanaler og periode. Leads og salg som kommer via lenkene, får
kampanjen, og kostnaden føres på den. Da kan Roret regne kostnad per lead og
kunde. Assistent foreslår kampanjen, og et menneske godkjenner den.

Krever Markedsføring. Selskap: `firmaprofil`. Skriveregler:
`roret-prinsipper`.

## Steg 1: Før du foreslår

```
markedsprofil(company_id=<id>)
hent_kampanjer(company_id=<id>)
```

- Profilen: målgruppene, kanalene, budsjettet per kanal og måned, årshjulet og
  rammene for Assistent.
- Kampanjene: **les lærdommen fra de tidligere**. Hva kostet de, hva ga de, og
  hva skulle gjøres annerledes? Ta det med i forslaget.
- Har selskapet Styring, sjekk at kampanjen passer med strategien
  (`maal-og-strategi`).

## Steg 2: Planen

Bli enig med brukeren om:

- **Navn:** kort og gjenkjennelig, f.eks. «Vårkampanje 2027». Navnet havner i
  lenkene.
- **Mål:** med et tall, f.eks. «20 leads fra styreledere».
- **Periode:** fra og til.
- **Kanaler:** blant dem profilen sier selskapet bruker.
- **Budsjett:** innenfor budsjettet i profilen for månedene. Går det over, si
  det.
- **Nettside:** siden lenkene skal gå til, f.eks. en landingsside.

Vis planen og vent på ja. Ingenting kjøpes eller publiseres av kampanjen.
Annonsene og innleggene kommer etterpå.

## Steg 3: Foreslå kampanjen

```
opprett_kampanje(navn=<navn>, kanaler=["linkedin", "facebook"], company_id=<id>,
                 fra=<YYYY-MM-DD>, til=<YYYY-MM-DD>, maal=<mål>,
                 budsjett=<beløp>, nettside=<https://…>)
```

Svaret er et forslag. Si at den markedsansvarlige godkjenner det i
Roret-appen eller i Odoo. Kall ikke verktøyet på nytt for det samme.

## Steg 4: Når den er godkjent

```
kampanjeresultat(kampanje_id=<id>, company_id=<id>)
```

`lenker` har én sporingslenke per kanal (`kort`). Bruk dem i innleggene
(`innlegg`), nyhetsbrevene (`nyhetsbrev`) og annonsene. Legg kampanjen på
innleggene og nyhetsbrevene med `kampanje_id`.

## Underveis

`kampanjeresultat` gir kostnaden, leadene per kilde, salget, klikkene på
lenkene, nyhetsbrevene og innleggene. Forbruket mot budsjettet per kanal gir
`annonseforbruk(fra=<fra>, til=<til>, kampanje_id=<id>, company_id=<id>)`.
Sier `merknader` at tallene fra annonsekontoene mangler, er kostnaden bare
det som er bokført og ført for hånd. Si det.

## Etterpå: lærdommen

Når kampanjen er over, skriv lærdommen kort: hva den kostet, hva den ga
(leads, salg, kostnad per lead mot målet) og hva som bør gjøres annerledes.
Vis den til brukeren, og be hen lime den inn i feltet Lærdom på planen i
Markedsføring. Det er den Assistent leser før neste kampanje. Vil brukeren
ha den i loggen på planen også:
`skriv_i_chatter(model="roret.markedsforing.kampanjeplan", res_id=<plan-id>, body=<lærdommen>)`.

Tallene er ledelsestall (`roret-prinsipper` §7).
