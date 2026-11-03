---
name: markedsrapport
description: Rapport om markedsføringen for en periode eller en uke — leads, salg og kostnad per kilde og kampanje, kostnad per lead, forbruket mot budsjettet, nyhetsbrevene og innleggene — med avvik og tre forslag. For en uke er tallene de samme som i mandagsrapporten på e-post. Bruk denne når brukeren ber om en markedsrapport eller ukerapporten for markedsføringen, spør hvordan markedsføringen går eller gikk forrige uke, hva som ga kunder, hva en kampanje kostet, eller kostnad per lead.
---

# Markedsrapport

Rapporten svarer på det en markedssjef spør om: hva ga leads og kunder, hva
kostet det, og hva bør vi gjøre annerledes. Den bare leser.

Krever Markedsføring. Selskap: `firmaprofil`. Periode: det brukeren sier,
ellers forrige måned. Datoer som `YYYY-MM-DD`.

**En uke** («forrige uke», «uke 44», «hvordan gikk uka»): hent ukerapporten
med `markedsoversikt(uke=<en dag i uka>, company_id=<id>)`, eller
`markedsoversikt(company_id=<id>)` for forrige hele uke. Tallene er de samme
som i mandagsrapporten på e-post, med uka før til sammenligning. Bruk dem som
de er, og regn ikke om: brukeren skal kjenne dem igjen fra e-posten. Er
`type` «periode» (eldre Markedsføring uten ukerapporten), mangler uka før.
Hent den med en dag i uka før om du vil sammenligne. For en uke erstatter
ukerapporten `markedsoversikt(fra=…, til=…)` i lista under. Hent resten med
`fra` og `til` fra `uke` i svaret.

## Hent (parallelt der det går)

```
markedsoversikt(fra=<fra>, til=<til>, company_id=<id>)
annonseforbruk(fra=<fra>, til=<til>, company_id=<id>)
hent_kampanjer(fra=<fra>, til=<til>, company_id=<id>)
hent_innholdskalender(fra=<fra>, til=<til>, company_id=<id>)
markedsprofil(company_id=<id>)
```

For de to–tre viktigste kampanjene i perioden:
`kampanjeresultat(kampanje_id=<id>, company_id=<id>)` for nyhetsbrevene,
klikkene på lenkene og innleggene.

Er leads eller salg `false`, mangler brukeren tilgang til CRM eller salg.
Ta resten, og si det i én linje.

## Format

```
## Markedsføring — mars 2027 — Eksempel AS

| Kilde | Leads | Salg | Salg eks. mva. |
|---|---|---|---|
| LinkedIn | 12 | 2 | 84 000 kr |
| Nyhetsbrev | 6 | 1 | 31 000 kr |

| Kampanje | Kostnad | Budsjett | Leads | Kostnad per lead |
|---|---|---|---|---|
| Vårkampanje | 8 400 kr | 10 000 kr | 14 | 600 kr |

**Totalt:** 22 leads, 3 salg, 12 400 kr i kostnad, 564 kr per lead
**Nyhetsbrev:** «Våren er her» — 52 % åpnet, 9 % klikket
**Innlegg:** 6 publisert, best: «…» på LinkedIn (1 900 visninger)
**Avvik:** Facebook brukte 40 % mer enn budsjettet, og ga ingen leads

**Tre forslag:**
1. …
2. …
3. …
```

- For en uke: vis endringen mot uka før fra ukerapporten, som «9 leads
  (+3, +50 %)». `prosent` er false når uka før var 0: skriv bare endringen.
- Kostnad per lead regnes per kampanje og totalt, ikke per kilde:
  kostnadslinjene har kampanje og kanal.
- Sammenlign forbruket med budsjettet i profilen og på kampanjene.
- Ta med `merknader` fra verktøyene som betyr noe for tallene: tall fra
  annonsekontoene som mangler, linjer uten valutakurs, eller kostnad som kan
  være telt to ganger.
- Forslagene bygger på tallene og lærdommen fra kampanjene: flytt penger fra
  det som ikke virker, gjenta det som virket, fyll hull i kalenderen.

Avslutt med én linje om at tallene er ledelsestall (`roret-prinsipper` §7).
