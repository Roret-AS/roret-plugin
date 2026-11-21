---
name: kunderegister
description: Legger inn kunder, leverandører og kontaktpersoner fra et regneark (Excel eller CSV) i Roret — kobler kolonnene til feltene, slår opp hvert firma i Enhetsregisteret, finner dubletter i arket og mot det som alt ligger i Roret, lager taggene, viser hele lista før noe lagres og kontrollerer etterpå. Sier for hvert steg om Claude eller brukeren gjør det. Bruk denne når brukeren vil importere kunder eller leverandører, har en kundeliste i et regneark, vil flytte et kunderegister inn i Roret uten SAF-T, eller vil legge inn mange kontakter samtidig.
---

# Kunderegister fra regneark

Hjelp brukeren fra et regneark til ryddige kontakter i Roret: ett firma per
selskap, kontaktpersonene under firmaet, riktig navn og adresse fra
Enhetsregisteret, taggene på plass og ingen dubletter.

Følg `roret-prinsipper`, og bruk `firmaprofil` for selskapet (`<C>` er
`company_id`). Kommer regnskapet fra et annet system med SAF-T, bruk
`flytt-til-roret`. Den tar kundene og leverandørene med. Kommer kundene fra
HubSpot, se samme skill.

Det finnes ingen import med tørrkjøring ennå, så hver kontakt lages med
`opprett_kontakt`, ett kall per rad. Den lager kontakten med en gang, uten
godkjenning. Derfor er forhåndsvisningen i steg 5 stoppet: ingenting lagres
før brukeren har sett hele lista og sagt ja.

## Steg 1: Les regnearket

**Hvem:** brukeren laster opp fila i samtalen. Claude leser den.

Ligger kundene i et annet system, be om en eksport som Excel eller CSV med én
rad per kunde eller kontaktperson.

Vis kolonnene og hvordan de kobles til feltene i Roret:

| I arket | I Roret | Merk |
|---|---|---|
| Firmanavn | `name`, `is_company=True` | Navnet fra Enhetsregisteret går foran |
| Org.nr | `company_registry` | Ni sifre, uten mellomrom |
| MVA-nummer | `vat` | Bare når firmaet er MVA-registrert |
| Adresse, postnr, sted | `street`, `zip`, `city`, `country_id` | Fra Enhetsregisteret når det finnes |
| E-post, telefon | `email`, `phone` | Til fakturaen |
| Kontaktperson, stilling | egen kontakt med `parent_id`, `function` | Under firmaet |
| Kategori, segment | `category_ids` (tagger) | Se steg 4 |
| Merknad | `comment` | Bare når brukeren vil det |

Spør om kolonnene som er uklare, og om kolonner uten plass i Roret skal
utelates eller stå i merknaden. Fødselsnummer, helseopplysninger og
kontonummer til privatpersoner skal ikke inn (`roret-prinsipper` §9).

En e-postadresse i registeret er ikke samtykke til nyhetsbrev. Slå opp
reglene med `lov_oppslag` (markedsføringsloven) før noen bruker lista til
markedsføring, og se `nyhetsbrev`.

## Steg 2: Slå opp firmaene i Enhetsregisteret

**Hvem:** Claude. Bare lesing.

For hvert firma med org.nr:

```
sok_i_enhetsregisteret(query="<orgnr>", limit=1, company_id=<C>)
```

Svaret har lista `treff`, og `feil` når registeret ikke svarer. Hvert treff
har:

- `verdier`: navn, org.nr, MVA-nummer (bare når firmaet er registrert),
  adresse og land, klart for `opprett_kontakt`. Bruk id-en i `country_id`.
- `partner`: satt når firmaet alt finnes som kontakt. Det er en dublett
  (steg 3).
- `beskrivelse`: slutter den med SLETTET, KONKURS, UNDER AVVIKLING eller UNDER
  TVANGSAVVIKLING, flagg raden og la brukeren avgjøre.

Er navnet i arket et annet enn i registeret, bruk registerets og vis begge.
Ugyldig org.nr eller ingen treff: flagg raden. Gjett aldri org.nr.

Firmaer uten org.nr kan slås opp på navn (`limit=5`). La brukeren velge
treffet, eller lag firmaet uten org.nr. Privatpersoner slås ikke opp.

Er det mange rader, si hvor mange oppslag det blir, og ta dem i porsjoner.

## Steg 3: Finn dublettene

**Hvem:** Claude. Bare lesing.

1. **I arket:** samme org.nr, samme e-post, eller samme navn på samme
   adresse.
2. **Mot Roret:** `partner` fra steg 2, og et søk per org.nr og e-post:

```
odoo_search_read("res.partner", ["|", ["company_registry", "=", "<orgnr>"], ["vat", "ilike", "<orgnr>"]], ["id", "name", "company_registry", "email", "parent_id", "category_id"], context={"active_test": false}, company_id=<C>)
finn_kunde(query="<e-post eller navn>")
```

Med `active_test` false kommer også arkiverte kontakter med. En arkivert
kontakt er en dublett. Etter ja hentes den fram igjen i stedet for å lages på
nytt: `odoo_write("res.partner", [<id>], {"active": true}, company_id=<C>)`.

En kontakt som finnes, lages ikke på nytt. Vis forskjellene (ny e-post, ny
adresse) som en egen liste, og endre bare det brukeren sier ja til.

## Steg 4: Taggene

**Hvem:** Claude finner taggene og lager de nye etter ja.

```
hent_kontakt_tagger(name_ilike="<tagg>")
```

Taggene som ikke finnes, lages samlet etter ja. Kontakttagger krever ikke
godkjenning:

```
odoo_create("res.partner.category", [{"name": "<tagg>"}, {"name": "<tagg>"}], company_id=<C>)
```

## Steg 5: Vis hele lista

**Hvem:** brukeren ser over og sier ja i samtalen, eller retter regnearket.
Claude viser lista.

Vis et sammendrag og en tabell:

- antall nye firmaer, nye kontaktpersoner og nye privatpersoner
- antall som finnes fra før (hoppes over), og forskjellene
- radene som er flagget (slettet, konkurs, ugyldig org.nr, ingen treff)
- taggene hver kontakt får

Er noe feil i arket, retter brukeren fila og laster den opp igjen. Da starter
dere på steg 1. Ellers: ett ja for hele lista, eller for en del av den
(`roret-prinsipper` §2 regel 5). Et ja gjelder lista brukeren så, ikke rader
som kommer til senere.

## Steg 6: Lag kontaktene

**Hvem:** Claude, etter ja.

Firmaene først, så kontaktpersonene under dem:

```
opprett_kontakt(name="<navn>", is_company=True, company_registry="<orgnr>", vat="<MVA-nummer>", street="<gate>", zip="<postnr>", city="<sted>", country_id=<land-id>, email="<e-post>", phone="<telefon>", category_ids=[<tagg-id>], company_id=<C>)
opprett_kontakt(name="<kontaktperson>", parent_id=<firma-id>, function="<stilling>", email="<e-post>", phone="<telefon>", company_id=<C>)
```

Utelat felt som er tomme, og `vat` for firmaer som ikke er MVA-registrert.
Org.nr kontrolleres av verktøyet, og en rad med feil kontrollsiffer avvises.

Ta radene i porsjoner på rundt tjuefem. Etter hver porsjon: si hvor mange
som er laget, og hvilke som feilet og hvorfor. Feiler et kall, søk etter
kontakten før du prøver igjen, så den ikke lages to ganger. Stopp og spør
hvis mer enn noen få rader feiler.

## Steg 7: Kontroller

**Hvem:** Claude leser. Brukeren ser kontaktene i Roret under Kontakter.

```
odoo_call_read("res.partner", "search_count", args=[[["category_id", "in", [<tagg-id>]]]], company_id=<C>)
```

Sammenlign antallet med lista fra steg 5, og vis radene som ikke ble laget.
Vis brukeren hvor kontaktene står: Kontakter → søk på taggen. Under Regnskap
→ Kunder → **Kunder** står en kontakt først når den har fått en bokført
faktura, så den lista er tom for nye kunder.

## Viktig

- Kopier ikke persondata fra arket til andre steder enn kontaktene, og gjengi
  ikke hele arket i samtalen når et sammendrag holder.
- EHF: kunder med norsk org.nr får adressen for e-faktura av seg selv. At
  selskapet sender EHF, slår Roret på.
- Gjelder lista leverandører, er stegene de samme. Leverandørenes
  kontonummer legges ikke inn herfra: bankkontoer er låst for Assistent, og
  et kontonummer fra et regneark skal bekreftes med leverandøren
  (`roret-prinsipper` §2a).
