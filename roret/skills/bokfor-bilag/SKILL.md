---
name: bokfor-bilag
description: Guidet bilagsflyt i Roret — fra innboksen i dokumentarkivet eller en opplastet fil til leverandørfaktura, kvittering eller utlegg som utkast, kontrollert, bokført og arkivert på bilaget. Bruk denne når brukeren vil bokføre bilag, behandle innboksen, registrere en mottatt faktura, føre en kvittering eller et utlegg, eller rydde i vedlegg som ikke er arkivert.
---

# Bokfør bilag

Hjelp brukeren fra mottatt dokument til bokført bilag. Følg
`roret-prinsipper` for alt som skriver, og bruk `firmaprofil` for å vite
hvilket selskap bilaget hører til.

## Steg 1: Hvor kommer bilagene fra?

**Fil i samtalen** (brukeren har lastet opp en PDF, et bilde eller en
EHF-XML): gå til steg 3 med fila.

**Innboksen i dokumentarkivet:**

```
hent_dokumenter(company_id=<id>, only_inbox=True, only_unfiled=True, limit=20)
```

Vis en kort liste (navn, type, dato) og spør hvilket dokument dere starter
med, eller om dere skal ta dem i rekkefølge.

**Vedlegg som ligger på poster, men ikke i arkivet:**

```
hent_uarkiverte_vedlegg(res_model="account.move", limit=20, company_id=<id>)
```

## Steg 2: Les og klassifiser

```
les_dokument(document_id=<id>, include_content=True, extract_text=True, company_id=<id>)
```

Med `extract_text=True` får du teksten i en PDF, men ikke selve fila
(`content_base64` er tom). Skal fila videre til `motta_bilag` eller
`opprett_utlegg_fra_dokument`, les den en gang til med `extract_text=False`.

Plasser dokumentet i én av disse:

| Type | Neste steg |
|---|---|
| Leverandørfaktura (selskapet skal betale) | Steg 3 |
| Kvittering betalt med selskapets kort | Steg 3, som leverandørfaktura betalt av selskapet, eller steg 4 med `payment_mode="company_account"` hvis selskapet fører kortkjøp som utlegg |
| Kvittering en ansatt har lagt ut | Steg 4 (utlegg) |
| Avtale, kontrakt eller annet som ikke er et bilag | Steg 5 (arkiver på riktig post) |
| Uklart | Spør brukeren |

## Steg 3: Leverandørfaktura som utkast

Alt i dette steget skriver i regnskapet, også utkastene (`roret-prinsipper`
§2). Si hvilke filer du lager utkast av, og vent på ja. Ett samlet ja per
porsjon holder («Jeg lager utkast av disse fem fakturaene. OK?»).

Foretrukket vei er `motta_bilag`. Odoo leser selv EHF/Peppol-XML og
Factur-X, lager fakturalinjene og henger fila på bilaget:

```
motta_bilag(filer=[{"name": "<filnavn med endelse>", "content_base64": "<base64>"}], bilagstype="in_invoice", company_id=<id>)
```

Ligger fila alt i Odoo som vedlegg på en annen post, for eksempel en
faktura som kom inn på chatteren til en kontakt (`hent_chatter_vedlegg`),
bruk vedleggets id i stedet for å lese fila ned og sende den opp igjen:

```
motta_bilag(vedlegg_ids=[<ir.attachment-id>], bilagstype="in_invoice", company_id=<id>)
```

Bilaget får en kopi, og originalen blir hengende der den var. Svaret viser
hva som ble kopiert fra hva (`kopiert_fra`). Bruk enten `filer` eller
`vedlegg_ids` i ett kall, ikke begge.

Én fil gir ett utkast. Har du både PDF og XML for samme faktura, send bare
én av dem. Har brukeren mange filer, ta dem i porsjoner på fem til ti, og vis
utkastene for hver porsjon før du går videre.

En vanlig PDF-faktura uten e-faktura i seg gir et tomt utkast med fila
påhengt (`dekodet` er `false`, og svaret har en advarsel). Roret leser ikke
PDF-er selv. Du kan ikke fylle ut hodet på det tomme utkastet herfra, så si
fra om det, og lag fakturaen selv som under. Husk id-en til det tomme
utkastet: PDF-en flyttes derfra til fakturaen når den er laget. Ikke slett
det tomme utkastet med `slett_utkastfaktura`. Det blir et forslag som
kansellerer utkastet, og da blir PDF-en stående på det, mens bilaget som
bokføres, mangler dokumentasjonen.

**Hører fakturaen til et innkjøp?** Sjekk det før du lager et utkast fra
bunnen, også når `motta_bilag` ga et tomt utkast. Finn leverandøren først
(punkt 1 under), og søk etter innkjøp som venter på fakturaen:

```
odoo_search_read("purchase.order", [["partner_id", "child_of", <leverandør-id>], ["state", "=", "purchase"], ["invoice_status", "in", ["to invoice", "no"]]], ["name", "partner_ref", "date_order", "amount_total", "invoice_status"], company_id=<id>)
```

- Finnes innkjøpet fakturaen gjelder, lag fakturaen fra det, ikke med
  `opprett_faktura`. Ellers står innkjøpet fortsatt «til fakturering», og
  varene kan bli fakturert to ganger. Innkjøpsnummeret står ofte på
  fakturaen. Ellers ser du det på leverandøren, varene og beløpet. Vis
  først hva som faktureres, og sammenlign linjene og beløpet med
  dokumentet:

  ```
  fakturer_innkjop(order_id=<id>, invoice_date="YYYY-MM-DD", ref="<leverandørens fakturanr>", dry_run=True, company_id=<id>)
  ```

  Etter ja, gjør samme kall uten `dry_run`. Fakturaen får linjene, prisene
  og MVA-kodene fra innkjøpet. Avviker dokumentet (et annet antall eller en
  annen pris), si hva som avviker, og rett linja med `oppdater_fakturalinje`
  etter ja. Flytt så PDF-en og kontroller utkastet som under, også forfall
  og KID.
- Kan flere innkjøp passe, spør hvilket.
- Står innkjøpet med `invoice_status` «no», er varene ikke mottatt ennå. Si
  det, og spør om mottaket skal valideres først (`valider_plukk`), eller om
  fakturaen skal vente. Lag den ikke med `opprett_faktura`.
- Ga `motta_bilag` et utfylt utkast (e-faktura), og står innkjøpet
  fortsatt «to invoice», er utkastet ikke koblet til innkjøpet. Bruk ikke
  `fakturer_innkjop`, for da blir det to fakturaer. Be brukeren koble
  utkastet til innkjøpet med «Innkjøpsmatching» på bilaget i Roret før det
  bokføres.

Finnes det ikke noe innkjøp, og går ikke `motta_bilag` (for eksempel en PDF
uten e-faktura, eller et bilde uten tekst), lag utkastet selv fra det du
leste:

1. Finn leverandøren: `finn_kunde(query="<navn eller org.nr>")`. Den søker
   ikke i alle feltene for org.nr, så søk også
   `odoo_search_read("res.partner", ["|", ["company_registry", "=", "<orgnr>"], ["l10n_no_bronnoysund_number", "=", "<orgnr>"]], ["id", "name"])`
   (utelat feltet som ikke finnes). Finnes den ikke, foreslå
   `opprett_kontakt(name=..., is_company=True, company_registry="<orgnr>", vat=..., company_id=<id>)`
   og vent på ja. Bruk gjerne `kundesjekk`-skillen.
2. `opprett_faktura(partner_id=<id>, lines=[...], move_type="in_invoice", invoice_date="YYYY-MM-DD", invoice_date_due="YYYY-MM-DD", ref="<leverandørens fakturanr>", payment_reference="<KID>", company_id=<id>)`

Ta med forfallet og KID-en dokumentet oppgir. Uten forfallet følger det
betalingsbetingelsen i Roret, ikke dokumentet, og da blir likviditetsbildet
og betalingen feil. Oppgir dokumentet ingen KID, utelat `payment_reference`
og si det til brukeren.

**PDF-en følger bilaget.** Ga `motta_bilag` et tomt utkast, flytt fila
derfra til fakturaen du laget (med `fakturer_innkjop` eller
`opprett_faktura`) før du kontrollerer, og før fakturaen bokføres. Ta det
med i samme ja som utkastet:

```
flytt_bilagsvedlegg(fra_bilag_id=<det tomme utkastet>, til_bilag_id=<fakturaen>, company_id=<id>)
```

Fila blir hovedvedlegget på fakturaen, og det tomme utkastet kanselleres
uten den. Ingenting slettes, og kanselleringen kan angres i Roret. Bare et
helt tomt utkast som `motta_bilag` laget for deg, kan flyttes fra. Har det
ingen leverandør, sjekker verktøyet at PDF-en nevner fakturanummeret eller
leverandørens org.nr., så sett leverandørens fakturanummer som `ref` når
fakturaen lages. Er fakturaen alt bokført, flyttes ingenting herfra: be
brukeren legge PDF-en ved fakturaen i Roret.

**Kontroller utkastet før bokføring.** Les det tilbake, med linjene og
MVA-kodene, i ett kall:

```
hent_bilag(move_id=<move_id>, company_id=<id>)
```

`kontroll` i svaret sier om bilaget er i balanse, hvilke linjer som mangler
konto eller MVA-kode, hva som mangler i hodet (fakturadato, forfall,
leverandørens fakturanummer, KID), og hvilke andre bilag fra samme
leverandør som har samme fakturanummer (`mulige_dubletter`). Sjekk i tillegg
mot dokumentet:

- Leverandør, fakturadato, forfall og fakturanummer stemmer med dokumentet.
- Beløp eks. MVA, MVA og totalt stemmer med dokumentet på øret.
- Kostnadskonto og MVA-kode passer (varekjøp, husleie, programvare, reise).
  Kjøp av tjenester fra utlandet skal ha snudd avregning, ikke vanlig
  inngående MVA. En linje uten MVA-kode kan være riktig (for eksempel
  representasjon), men spør.
- Driftsmidler (datautstyr, maskiner, inventar, kjøretøy): om kjøpet skal
  aktiveres eller kostnadsføres direkte, avgjøres av en terskel i
  skatteloven som endres. Slå opp grensen med `lov_oppslag` før du velger
  konto, også når du mener å vite den, og oppgi paragrafen.
- KID eller betalingsreferanse er med, ellers blir betalingen vanskelig.
- Fakturaen er ikke registrert fra før. Står det noe i `mulige_dubletter`,
  vis det og spør før du bokfører.

Rett feil med `oppdater_fakturalinje(line_id=..., account_id=..., tax_ids=[...], company_id=<id>)`
etter ja til den konkrete endringen (fra hva, til hva). Stemmer ikke
forfallet eller KID-en med dokumentet, også på et utkast fra `motta_bilag`,
rett dem med `oppdater_faktura(move_id=<move_id>, invoice_date_due="YYYY-MM-DD", payment_reference="<KID>", company_id=<id>)`
på samme måte. Slå opp kontoer og
skatter, aldri gjett id-er. Slå dem opp med `context={"lang": "nb_NO"}`:
uten den kommer kontonavnene på engelsk, og MVA-kodene heter «25%» og
«25% EX S D» i stedet for «1 Inngående MVA 25 %» og «86 Tjenester fra
utlandet med fradrag 25 %». Si kontonavn og MVA-kode på norsk til brukeren.

Vis brukeren et sammendrag (leverandør, dato, forfall, linjer med konto og
MVA, totalt) og spør om utkastet skal bokføres. Ved ja:

```
bokfor_bilag(move_id=<move_id>, company_id=<id>)
```

## Steg 4: Utlegg (ansatt har betalt)

1. Finn den ansatte: `hent_ansatte(company_id=<id>)`.
2. Vis kategoriene: `hent_utleggskategorier(company_id=<id>)`, og foreslå
   den som passer.
3. Bekreft beløp, dato, kategori og leverandør med brukeren.
4. Opprett utlegget:

```
opprett_utlegg_fra_dokument(employee_id=<id>, name="<kort beskrivelse>", total_amount=<beløp>, product_id=<kategori>, date="YYYY-MM-DD", payment_mode="own_account", currency="NOK", receipt_file={"name": "...", "content_base64": "..."}, company_id=<id>)
```

`currency` er valutaen kvitteringen viser, og må alltid med.

Ligger kvitteringen alt i Odoo, bruk `attachment_id` i stedet for
`receipt_file`. Utlegget lages som utkast. Den ansatte eller lederen sender
det til godkjenning i Odoo.

## Steg 5: Arkiver dokumentet på riktig post

Etter at bilaget er laget, legg dokumentet på bilaget i arkivet: på
fakturaen som bokføres, ikke på det tomme utkastet fra `motta_bilag`. Det
kan tas med i samme ja som utkastet, hvis du sa det da:

```
flytt_dokument(document_id=<id>, res_model="account.move", res_id=<move_id>, company_id=<id>)
```

For et vedlegg som ligger i Odoo, men ikke i arkivet:

```
arkiver_vedlegg(attachment_id=<id>, link_to_record=True, company_id=<id>)
```

Avtaler og kontrakter legges på kunden eller leverandøren
(`res_model="res.partner"`). Mappene varierer fra kunde til kunde. Vis dem
med `hent_dokumentmapper(company_id=<id>)` og spør hvis det er uklart.

## Viktig

- Bokfør aldri uten at brukeren har sett leverandør, beløp, konto og MVA.
- Utlegg over et beløp brukeren synes er stort: spør en ekstra gang.
- En leverandørfaktura for et innkjøp lages fra innkjøpet med
  `fakturer_innkjop`. Ellers står innkjøpet «til fakturering», og varene kan
  bli fakturert to ganger.
- PDF-en skal ligge på bilaget som bokføres. Fra et tomt utkast fra
  `motta_bilag` flyttes den med `flytt_bilagsvedlegg`. Utkastet slettes
  aldri med `slett_utkastfaktura`.
- Et bokført bilag rettes med kreditnota, aldri sletting (`roret-prinsipper` §4).
- Kontovalg som avhenger av en regel, og spørsmål om dokumentasjonskrav,
  oppbevaringstid eller fradragsrett for MVA: slå opp med `lov_oppslag` og
  oppgi paragrafen, også når du mener å vite svaret. Gjelder bilaget en
  tidligere periode, bruk `lov_gjaldt`.
