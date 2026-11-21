---
name: produkter
description: Legger inn varene og tjenestene til en bedrift i Roret — pris med og uten MVA, riktig MVA-kode, kostpris, enhet, kategori, lagervare og beholdning, bilder, publisering i nettbutikken og forhandlerpris med egen prisliste — og sier for hvert steg om Claude eller brukeren gjør det, med stien i Roret. Bruk denne når brukeren vil legge inn produktene sine, bygge en varekatalog, importere en prisliste fra et regneark, sette forhandlerpriser, legge ut varer i nettbutikken eller rette pris og MVA på et produkt.
---

# Produkter

Hjelp brukeren med en katalog der hvert produkt har riktig pris, MVA-kode og
kostpris, og der lager, bilder, nettbutikk og forhandlerpris er på plass.
Claude lager og endrer produktene med `opprett_produkt` og
`oppdater_produkt`. De går uten godkjenning, og rører aldri MVA, kontoer
eller kostpris etterpå. Resten gjør brukeren i Roret, eller Claude foreslår
det med de rå verktøyene, som venter på godkjenning i appen
**Assistent → Til godkjenning**.

Følg `roret-prinsipper`, og bruk `firmaprofil` for selskapet (`<C>` er
`company_id`). Bare tjenester for et nytt selskap: `sett-opp-bedriften` steg 6
holder. Produkter som skal faktureres fast: `abonnement`.

## Steg 1: Lista over produktene

**Hvem:** brukeren gir lista i samtalen, som tekst eller regneark. Claude
leser den.

For hvert produkt: navn, varenummer, salgspris (og om den er med eller uten
MVA), kostpris, enhet (stk, kg, time), om det er en vare eller en tjeneste,
om det skal på lager, og om det skal i nettbutikken. Varer med varianter
(størrelse, farge, duft): se steg 7.

Finn det som finnes fra før, så ingenting lages to ganger:

```
odoo_search_read("product.product", [["default_code", "in", ["<varenummer>", "<varenummer>"]]], ["id", "name", "default_code", "list_price", "product_tmpl_id"], context={"active_test": false}, company_id=<C>)
```

`opprett_produkt` lager ikke et nytt produkt når varenummeret finnes. Svaret
har da `already_exists`.

## Steg 2: Pris og MVA

**Hvem:** Claude regner og viser. Er MVA-koden feil på et produkt, retter
brukeren den i Roret.

1. **Satsen.** Slå opp MVA-satsen for varene med `lov_oppslag` (for
   eksempel næringsmidler, bøker, persontransport og tjenester som er
   unntatt), også når du mener å vite den. Oppgi lov og paragraf.
2. **Med eller uten MVA.** `list_price` regnes med selskapets MVA-oppsett,
   og er vanligvis uten MVA. Kontroller det på MVA-koden produktet får:

```
odoo_search_read("account.tax", [["type_tax_use", "=", "sale"], ["active", "=", true]], ["id", "name", "amount", "price_include"], context={"lang": "nb_NO"}, company_id=<C>)
```

   Er `price_include` `false`, og brukeren har priser med MVA: regn ut
   prisen uten MVA, rund til øre, og vis begge for hvert produkt. Kontroller
   at prisen uten MVA gir nøyaktig prisen med MVA tilbake, og juster øret når
   den ikke gjør det. Brukeren godkjenner lista med begge prisene.
3. **MVA-koden.** Et nytt produkt får selskapets standard-MVA, og verktøyene
   setter den aldri. Trenger et produkt en annen kode, lager Claude produktet,
   og brukeren endrer koden: Lager (eller Salg) → **Produkter** → produktet →
   fanen **Generell informasjon** → **Salgsavgifter**.

## Steg 3: Enhet og kategori

**Hvem:** Claude slår opp. Ingenting endres.

```
odoo_search_read("uom.uom", [["name", "ilike", "<enhet>"]], ["id", "name"], context={"lang": "nb_NO"})
odoo_search_read("product.category", [], ["id", "complete_name"], context={"lang": "nb_NO"}, company_id=<C>)
```

Uten `uom_id` blir enheten stykk, også for varer som selges per kilo.
Kategorien bestemmer inntekts- og kostnadskontoen og lagerverdsettingen, og
kan ikke endres herfra etterpå. Spør når det er uklart, og la Odoos standard
stå når bedriften ikke bruker kategorier.

## Steg 4: Lag produktene

**Hvem:** Claude, etter ja til hele lista.

Vis lista (navn, varenummer, pris uten og med MVA, kostpris, enhet, kategori,
lager) og få ett ja. Tørrkjør det første, og lag resten:

```
opprett_produkt(name="<navn>", type="consu", is_storable=True, list_price=<pris uten MVA>, standard_price=<kostpris>, default_code="<varenummer>", uom_id=<enhet>, categ_id=<kategori>, description_sale="<tekst på tilbud og faktura>", dry_run=True, company_id=<C>)
```

- `type`: `consu` for en vare, `service` for en tjeneste.
- `is_storable=True` bare for varer bedriften holder lager av. Det krever
  Lager.
- **Kostprisen kan bare settes nå.** Senere endres den i Roret, fordi en ny
  kostpris på en lagervare kan endre lagerverdien i regnskapet. Spør etter
  den før produktet lages.
- Rett navn, pris, varenummer eller tekst etterpå med
  `oppdater_produkt(product_id=<id>, list_price=<ny pris>, dry_run=True, company_id=<C>)`.
  Prisen på tilbud og ordrer som finnes, endres ikke.

Si hvor mange som er laget, og hvilke som fantes fra før.

## Steg 5: Beholdning

**Hvem:** brukeren, i Roret. Claude kontrollerer etterpå.

Beholdningen legges inn etter at kostprisen står, for lagerverdien regnes av
den. Brukeren åpner Lager → **Produkter** → produktet → **Prognose** →
**Oppdater lager** → **Ny**, velger lagerstedet og skriver antallet under
**Telt mengde**. Den grå tabellen med eksempeltekst som vises først, er bare
et eksempel. Mange varer: Lager → Operasjoner → **Fysisk inventar** viser alle
på én side. Ser brukeren noe annet, spør hva som står på skjermen.

Kontroller:

```
odoo_search_read("product.product", [["default_code", "in", ["<varenummer>"]]], ["name", "qty_available"], company_id=<C>)
```

## Steg 6: Bilder og nettbutikken

**Hvem:** brukeren laster opp bildene i Roret. Claude foreslår publiseringen,
og brukeren godkjenner i Assistent → Til godkjenning.

Bildene: Lager (eller Salg) → **Produkter** → produktet → klikk på bildet
øverst til høyre og last opp. `last_opp_nettsidebilde` er for sidene på
nettstedet, ikke for produktene.

Før produktene legges ut, sjekk at nettbutikken viser prisene slik
regelverket krever for forbrukere. Slå opp kravene med `lov_oppslag`
(prisopplysningsforskriften, også om enhetspris for varer som selges etter
vekt eller volum), og les innstillingen:

```
odoo_search_read("website", [], ["name", "show_line_subtotals_tax_selection"], company_id=<C>)
```

`tax_excluded` betyr at butikken viser prisene uten MVA. Det kan ikke
brukeren endre selv: be Roret om det (support@roret.no) før produktene legges
ut. Legg så ut produktene samlet, høyst 100 per kall. Det blir ett forslag:

```
odoo_write("product.template", [<id>, <id>], {"is_published": true}, company_id=<C>)
```

`id` er malen til produktet (`id` i svaret fra `opprett_produkt`). Brukeren
kan også legge ut ett og ett: produktet → fanen **Salg** → **Er publisert**.
Be brukeren åpne butikken som besøkende og se på pris og bilde før kundene
gjør det.

## Steg 7: Varianter

**Hvem:** brukeren ber Roret slå på varianter. Claude lager produktene uten.

Varianter (størrelse, farge, duft) krever en innstilling brukeren ikke når,
og verktøyene kan ikke lage dem. Lag produktet uten varianter, eller ett
produkt per variant med eget varenummer. Be Roret slå på varianter
(support@roret.no). Etterpå legger brukeren dem inn: produktet → fanen
**Attributter og varianter**.

## Steg 8: Forhandlerpris

**Hvem:** brukeren lager prislista i Roret. Claude foreslår den på
forhandlerne og kontrollerer nettbutikken.

Prislister er låst for Assistent. Brukeren lager prislista: Salg → Produkter
→ **Prislister** → **Ny**. Gi den et navn, og legg inn regelen (rabatt eller
fast pris) for produktene eller kategoriene den gjelder.

**Har bedriften nettbutikk,** kan en ny prisliste bli butikkens pris for
alle besøkende. Be brukeren tømme **Nettsted** på fanen **Ecommerce** i
prislista, og kontroller:

```
odoo_search_read("product.pricelist", [], ["id", "name", "website_id", "selectable"], company_id=<C>)
```

Har forhandlerlista `website_id`, si fra med en gang. Da får alle i
nettbutikken forhandlerprisen.

Sett prislista på forhandlerne samlet, høyst 100 per kall. Det blir ett forslag:

```
odoo_write("res.partner", [<id>, <id>], {"property_product_pricelist": <prisliste-id>}, company_id=<C>)
```

Brukeren kan også gjøre det på hver forhandler: Kontakter → forhandleren →
fanen **Salg og kjøp** → **Prisliste**. Et nytt tilbud til en forhandler får
da prisen fra lista.

## Viktig

- Si pris uten og med MVA hver gang du viser en pris, og hvilken av dem som
  står i Roret.
- MVA-satser, prisopplysning og enhetspris: slå opp med `lov_oppslag`, og
  oppgi paragrafen.
- Lag aldri samme produkt to ganger. Bruk varenummeret.
