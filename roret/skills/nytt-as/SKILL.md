---
name: nytt-as
description: Fører stiftelsen av et nytt aksjeselskap i Roret — aksjeeierne som kontakter, aksjeklassen med pålydende, stiftelsen i aksjeeierboken med aksjenummer, og bokføringen av aksjekapitalen og overkursen mot banken — og kontrollerer at aksjeeierboken og hovedboka viser samme aksjekapital. Sier for hvert steg om Claude eller brukeren gjør det, med stien i Roret. Bruk denne når selskapet er nystiftet, brukeren vil føre stiftelsen eller aksjeeierne inn i aksjeeierboken, spør hvordan aksjekapitalen bokføres, eller når konto for aksjekapital står i null etter stiftelsen.
---

# Nytt AS

Når et aksjeselskap stiftes, skal to ting stemme med stiftelsesdokumentet:
aksjeeierboken (hvem eier hvor mange aksjer, med aksjenummer) og
hovedboka (aksjekapitalen og overkursen som er innbetalt). Roret fører ikke
det ene av det andre. Brukeren fører begge i Roret, og Claude forbereder
tallene og kontrollerer at de stemmer.

Aksjeeierboken og hovedboka er låst for Assistent. Følg `roret-prinsipper`,
og bruk `firmaprofil` for selskapet (`<C>` er `company_id`). Krever at
brukeren har regnskapsrollen: tilgangen til aksjeeierboken følger
regnskapsgruppene, og menyen står i Styring → Eierskap.

## Steg 1: Tallene fra stiftelsesdokumentet

**Hvem:** brukeren gir stiftelsesdokumentet i samtalen. Claude leser og
regner.

Be om stiftelsesdokumentet og vedtektene (PDF eller bilde), og les:

- stiftelsesdatoen (dagen dokumentet ble undertegnet)
- aksjekapitalen, antall aksjer og pålydende per aksje
- aksjeinnskuddet per aksje (tegningskursen), og dermed overkursen
- hver stifter: navn, org.nr for selskaper, antall aksjer
- hvordan innskuddet er betalt: penger til bankkonto, eller noe annet
  (tingsinnskudd)

Kontroller at antall aksjer ganger pålydende er aksjekapitalen, og at
antall ganger kursen er det samlede innskuddet. Overkursen er differansen.
Slå opp kravene til aksjekapital, innskudd og innbetaling ved stiftelse med
`lov_oppslag` (aksjeloven kapittel 2 og 3), og oppgi paragrafene. Tingsinnskudd
og kapital som ikke er innbetalt: anbefal regnskapsfører eller revisor, og
før ikke noe før det er avklart.

Legg dokumentene i dokumentarkivet med `last_opp_dokument` når brukeren vil
det.

## Steg 2: Aksjeeierne som kontakter

**Hvem:** Claude lager kontaktene etter ja. Brukeren legger inn fødselsdatoen
til personene i Roret.

Finn hver aksjeeier med `finn_kunde(query="<navn>")`, og lag dem som mangler:

```
opprett_kontakt(name="<navn>", is_company=False, email="<e-post>", street="<gate>", zip="<postnr>", city="<sted>", country_id=<land-id>, company_id=<C>)
opprett_kontakt(name="<selskap>", is_company=True, company_registry="<orgnr>", company_id=<C>)
```

Aksjeeierboken skal ha fødselsdatoen til personene. Den skriver brukeren inn
selv: Kontakter → aksjeeieren → **Fødselsdato**. Be ikke om fødselsnummer.

## Steg 3: Aksjeklassen

**Hvem:** brukeren, i Roret. Claude kontrollerer.

Les det som finnes:

```
odoo_search_read("roret.aksjeklasse", [], ["id", "name", "palydende", "antall_aksjer", "aksjekapital"], company_id=<C>)
```

Finnes ingen klasse, lager brukeren den: Styring → Eierskap →
**Aksjeklasser** → **Ny**. Navnet er «Ordinære aksjer» når selskapet bare har
én klasse. Brukeren fyller inn **Pålydende** fra stiftelsesdokumentet. Flere
klasser står i vedtektene.

## Steg 4: Stiftelsen i aksjeeierboken

**Hvem:** brukeren, i Roret. Claude lager tabellen og kontrollerer etterpå.

Lag tabellen først: én linje per stifter, med antall aksjer, kursen og
aksjenummer fra og til. Aksjenummerne går fortløpende fra 1, og hver stifter
får sitt intervall. Vis den til brukeren.

Brukeren fører én transaksjon per stifter: Styring → Eierskap →
**Aksjetransaksjoner** → **Ny**:

| Felt | Verdi |
|---|---|
| Type | Stiftelse |
| Aksjeklasse | Klassen fra steg 3 |
| Dato | Stiftelsesdatoen |
| Innført i aksjeeierboken | Dagen den føres |
| Erverver | Stifteren |
| Antall aksjer | Fra tabellen |
| Aksjenummer fra og til | Fra tabellen. Fyll inn begge, Roret regner ikke ut «til» |
| Kurs per aksje | Aksjeinnskuddet per aksje |

Skriv gjerne i **Merknad** at transaksjonen bygger på stiftelsesdokumentet.

Kontroller etterpå:

```
odoo_search_read("roret.aksjetransaksjon", [["type", "=", "stiftelse"]], ["dato", "erverver_id", "antall", "kurs", "belop", "nummer_fra", "nummer_til"], company_id=<C>)
```

Summen av antall skal være antall aksjer, summen av `belop` det samlede
innskuddet, og aksjekapitalen på klassen (steg 3) skal være lik den i
stiftelsesdokumentet. Aksjeeierboken med eierandeler står under Styring →
Eierskap → **Aksjeeiere**.

## Steg 5: Bokfør aksjekapitalen

**Hvem:** brukeren bokfører i Roret. Claude finner kontoene, regner ut
beløpene og kontrollerer.

Aksjeeierboken bokfører ingenting. Uten dette steget står kontoen for
aksjekapital i null. Finn kontoene:

```
odoo_search_read("account.account", ["|", ["name", "ilike", "aksjekapital"], ["name", "ilike", "overkurs"]], ["id", "code", "name"], context={"lang": "nb_NO"}, company_id=<C>)
```

I norsk standard kontoplan er det 2000 Aksjekapital og 2020 Overkurs. Vis
kontoene og beløpene: aksjekapitalen på den ene, overkursen på den andre,
og hele innskuddet inn på banken. Det er ingen MVA.

**Kom innskuddet inn på selskapets bankkonto i Roret** (det vanlige): når
kontoutskriften med innbetalingen er importert, finner Claude linja med
`hent_uavstemte_banklinjer(company_id=<C>)`. Brukeren avstemmer den: Regnskap
→ kortet **Bank** → **Avstem** → linja → fanen **Manuell postering**. Der
føres aksjekapitalen og overkursen på hver sin konto, og så **Avstem**.

**Ble innskuddet betalt før kontoutskriftene i Roret begynner,** hører det
hjemme i åpningsbalansen. Brukeren eller regnskapsføreren fører det som et
bilag: Regnskap → Bokføring → **Bilag** → **Ny**, med bankens bekreftelse
på innbetalingen som vedlegg. Er brukeren usikker, ta det med
regnskapsføreren før noe føres.

## Steg 6: Kontroller

**Hvem:** Claude.

```
saldo_per_konto(account_codes=["<konto for aksjekapital>", "<konto for overkurs>"], company_id=<C>)
```

Saldoen på kontoen for aksjekapital skal være lik aksjekapitalen i
aksjeeierboken, og overkursen lik differansen fra steg 1. Si fra om noe ikke
stemmer, og hvilken side som mangler.

## Etterpå

- **Reelle rettighetshavere:** Styring → Eierskap →
  **Reelle rettighetshavere**. Slå opp hvem som regnes som det med
  `lov_oppslag` (hvitvaskingsloven).
- **Styret og generalforsamlingen:** `styremote` og `frister`. Varsler om
  generalforsamling eller årsregnskap for år før stiftelsen gjelder ikke
  selskapet. MVA-frister gjelder først fra registreringen i
  Merverdiavgiftsregisteret (`firmaprofil`, `mva.registrert_fra`).
- **Videre oppsett:** `sett-opp-bedriften` for bank, KID og første faktura.
