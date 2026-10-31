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

Én fil gir ett utkast. Har du både PDF og XML for samme faktura, send bare
én av dem. Har brukeren mange filer, ta dem i porsjoner på fem til ti, og vis
utkastene for hver porsjon før du går videre.

Går ikke `motta_bilag` (for eksempel et bilde uten tekst), lag utkastet selv
fra det du leste:

1. Finn leverandøren: `finn_kunde(query="<navn eller org.nr>")`. Den søker
   ikke i alle feltene for org.nr, så søk også
   `odoo_search_read("res.partner", ["|", ["company_registry", "=", "<orgnr>"], ["l10n_no_bronnoysund_number", "=", "<orgnr>"]], ["id", "name"])`
   (utelat feltet som ikke finnes). Finnes den ikke, foreslå
   `opprett_kontakt(name=..., is_company=True, company_registry="<orgnr>", vat=..., company_id=<id>)`
   og vent på ja. Bruk gjerne `kundesjekk`-skillen.
2. `opprett_faktura(partner_id=<id>, lines=[...], move_type="in_invoice", invoice_date="YYYY-MM-DD", ref="<leverandørens fakturanr>", company_id=<id>)`

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
- KID eller betalingsreferanse er med, ellers blir betalingen vanskelig.
- Fakturaen er ikke registrert fra før. Står det noe i `mulige_dubletter`,
  vis det og spør før du bokfører.

Rett feil med `oppdater_fakturalinje(line_id=..., account_id=..., tax_ids=[...], company_id=<id>)`
etter ja til den konkrete endringen (fra hva, til hva). Slå opp kontoer og
skatter, aldri gjett id-er.

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
opprett_utlegg_fra_dokument(employee_id=<id>, name="<kort beskrivelse>", total_amount=<beløp>, product_id=<kategori>, date="YYYY-MM-DD", payment_mode="own_account", receipt_file={"name": "...", "content_base64": "..."}, company_id=<id>)
```

Ligger kvitteringen alt i Odoo, bruk `attachment_id` i stedet for
`receipt_file`. Utlegget lages som utkast. Den ansatte eller lederen sender
det til godkjenning i Odoo.

## Steg 5: Arkiver dokumentet på riktig post

Etter at bilaget er laget, legg dokumentet på bilaget i arkivet. Det kan tas
med i samme ja som utkastet, hvis du sa det da:

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
- Et bokført bilag rettes med kreditnota, aldri sletting (`roret-prinsipper` §4).
- Spørsmål om dokumentasjonskrav, oppbevaringstid eller fradragsrett for
  MVA: slå opp med `lov_oppslag` og oppgi paragrafen. Gjelder bilaget en
  tidligere periode, bruk `lov_gjaldt`.
