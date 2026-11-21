---
name: sett-opp-bedriften
description: Setter opp en ny bedrift i Roret fram til første sendte faktura — bedriftsopplysninger og logo, bankkonto med «Send penger», KID, betalingsfrist, tjenester og priser, første kunde, første tilbud og første faktura — og sier for hvert steg om Claude eller brukeren gjør det, med stien i Roret. Bruk denne når en ny bedrift vil komme i gang med fakturering, sier «sett opp bedriften» eller «jeg vil sende min første faktura», spør hvor KID, bankkontoen eller logoen legges inn, eller når `kom-i-gang` foreslår den for et nytt selskap.
---

# Sett opp bedriften

Målet er at bedriften kan sende en riktig faktura som kunden kan betale:
med selskapets navn, adresse og org.nr, kontonummeret, KID når selskapet
har det, riktig MVA og riktig forfall. Ta ett steg om gangen, og vent der
brukeren må gjøre noe i Roret.

Følg `roret-prinsipper` for alt som skriver, og bruk `firmaprofil` for
selskapet (`<C>` under er `company_id`). Noe av oppsettet er låst for
Assistent: selskapet og selskapets kontaktkort, bankkontoene, KID og
journalene. Det gjør brukeren i Roret, og Claude kontrollerer etterpå.
Forslag fra de rå verktøyene venter på godkjenning i Roret, i appen
**Assistent → Til godkjenning**. Si det hver gang et kall blir et forslag.

Skal kundelista, varekatalogen eller faste avtaler inn, bruk `kunderegister`,
`produkter` og `abonnement` når dere kommer dit. Er selskapet et nystiftet
AS, ta `nytt-as` også.

## Steg 1: Se hva som mangler

**Hvem:** Claude leser og viser en liste. Ingenting endres.

```
firmaprofil(company_id=<C>)
odoo_search_read("res.company", [["id", "=", <C>]], ["name", "partner_id", "street", "zip", "city", "email", "phone", "logo"], context={"bin_size": true}, company_id=<C>)
odoo_search_read("res.partner.bank", [["partner_id", "=", <selskapets partner_id>]], ["acc_number", "allow_out_payment"], company_id=<C>)
odoo_search_read("account.journal", [["type", "=", "sale"]], ["name", "invoice_reference_model"], company_id=<C>)
```

Vis en kort tabell: adresse, logo, bankkonto, «Send penger», KID og
tjenester, med «på plass» eller «mangler» og hvem som retter det. På
salgsjournalen betyr `invoice_reference_model` `no` at KID er på, og `odoo`
at betalingsreferansen er fakturanummeret.

## Steg 2: Bedriftsopplysninger og logo

**Hvem:** brukeren, i Roret. Claude henter adressen fra Enhetsregisteret og
kontrollerer etterpå.

Slå opp den offisielle adressen, så brukeren kan skrive den inn likt:

```
sok_i_enhetsregisteret(query="<orgnr>", limit=1, company_id=<C>)
```

Brukeren åpner Kontakter → selskapet sitt:

1. Fyller inn gateadresse, postnummer og sted, og velger **Norge** under
   **Land**. E-post, telefon og nettside står også på fakturaen.
2. Klikker på bildet øverst til høyre i kortet og laster opp logoen.
3. Lagrer.

Les `res.company` på nytt og bekreft at adressen og logoen er der.

## Steg 3: Bankkonto med «Send penger»

**Hvem:** brukeren, i Roret. Claude kontrollerer etterpå.

Uten dette står det ikke noe kontonummer på fakturaen, og Roret sier ikke fra
når den sendes. Be brukeren lese kontonummeret fra nettbanken, ikke fra en
e-post. Claude skriver aldri inn et kontonummer.

1. **Legg inn kontoen:** Kontakter → selskapet → fanen **Fakturering** →
   **Bankkontoer**. Skriv kontonummeret og lagre.
2. **Slå på «Send penger»:** Kontakter → Konfigurasjon → **Bankkonti** →
   åpne kontoen og slå på **Send penger**. Står kontoen som «Ikke betrodd»
   i lista, er den av. Et klikk på kontoen i kontaktkortet åpner den ikke.

Kontroller med kallet på `res.partner.bank` fra steg 1: `allow_out_payment`
skal være `true`.

Kjør så `firmaprofil(company_id=<C>)` igjen. Er `kontonummer` på
bankjournalen fortsatt tomt, er kontoen ikke koblet til bankjournalen. Det
gjør Roret i oppstarten, og før det kan kontoutskriften ikke importeres.
Fakturaen får kontonummeret uansett. Er det ikke gjort etter oppstarten, ber
brukeren Roret om det (support@roret.no). I Roret for Odoo gjør
administratoren hos bedriften det.

## Steg 4: KID

**Hvem:** brukeren bestemmer og slår det på i Roret. Claude kontrollerer.

Spør først om selskapet har KID-avtale (OCR-avtale) med banken. KID er av til
brukeren slår det på, og uten avtale skal det stå av. Da er
betalingsreferansen fakturanummeret.

Har selskapet avtale: Regnskap → Kunder → **KID** → kryss av for **KID på
fakturaene**. Gjør det før den første fakturaen bokføres, for KID-en settes
når fakturaen bokføres. Kontroller etterpå at salgsjournalen har
`invoice_reference_model` `no`.

## Steg 5: Betalingsfrist

**Hvem:** Claude leser og foreslår. Brukeren godkjenner i Assistent → Til
godkjenning, eller endrer fristen på kunden i Roret.

Selskapets standardvilkår står på hver nye faktura. Vis det på det første
utkastet (steg 9). Skal én kunde ha en annen frist, slå opp vilkårene:

```
odoo_search_read("account.payment.term", [], ["id", "name"], context={"lang": "nb_NO"}, company_id=<C>)
```

Vis kunden og vilkåret, og foreslå endringen etter ja. Den blir et forslag:

```
odoo_write("res.partner", [<kunde-id>], {"property_payment_term_id": <vilkår-id>}, company_id=<C>)
```

Brukeren kan også gjøre det selv: Kontakter → kunden → fanen **Salg og kjøp**
→ **Betalingsvilkår**. Finnes ikke vilkåret brukeren vil ha, eller skal
selskapets standard endres, ber brukeren Roret om det (support@roret.no). I
Roret for Odoo gjør administratoren hos bedriften det.

## Steg 6: Tjenester og priser

**Hvem:** Claude lager tjenestene etter ja. Er MVA-koden feil, retter brukeren
den på produktet i Roret.

Spør hva bedriften selger, og prisen per enhet (time, stykk, fastpris).
Selger bedriften varer, bruk `produkter` i stedet. Finn enheten:

```
odoo_search_read("uom.uom", [["name", "ilike", "<enhet>"]], ["id", "name"], context={"lang": "nb_NO"})
```

Prisen i Roret er vanligvis uten MVA. Oppgir brukeren priser med MVA, regn om
med satsen fra `lov_oppslag` og vis begge før du lager noe. Vis lista, få ja,
og lag tjenestene, først med tørrkjøring:

```
opprett_produkt(name="<navn>", type="service", list_price=<pris uten MVA>, uom_id=<enhet>, description_sale="<tekst på tilbud og faktura>", dry_run=True, company_id=<C>)
```

Produktet får selskapets standard-MVA. Slå opp med `lov_oppslag` om den
gjelder tjenesten (noen tjenester er unntatt eller har lavere sats), og les
MVA-koden produktet fikk:

```
odoo_search_read("product.template", [["id", "=", <id>]], ["name", "list_price", "taxes_id"], company_id=<C>)
odoo_search_read("account.tax", [["id", "in", [<tax-id>]]], ["name", "amount", "price_include"], context={"lang": "nb_NO"}, company_id=<C>)
```

Er koden feil, endrer brukeren den: Regnskap → Kunder → **Produkter** →
produktet → fanen **Generell informasjon** → **Salgsavgifter**. Oppgi lov og
paragraf for satsen du bruker.

## Steg 7: Første kunde

**Hvem:** Claude slår opp og lager kontakten etter ja.

Slå opp kunden i Enhetsregisteret og sjekk at den ikke finnes fra før, som
i `kundesjekk`. Lag den med adressen fra registeret:

```
opprett_kontakt(name="<navn>", is_company=True, company_registry="<orgnr>", vat="<MVA-nummer når kunden er registrert>", street="<gate>", zip="<postnr>", city="<sted>", country_id=<Norge>, email="<e-post til faktura>", company_id=<C>)
```

Finn id-en til Norge med
`odoo_search_read("res.country", [["code", "=", "NO"]], ["id"])`.
Slå opp kravene til innholdet i et salgsdokument med `lov_oppslag`
(bokføringsforskriften kapittel 5), og spør etter det som mangler om
kjøperen. Mange kunder samtidig: bruk `kunderegister`.

## Steg 8: Første tilbud

**Hvem:** Claude foreslår tilbudet og legger på linjene. Brukeren godkjenner i
Assistent → Til godkjenning og sender tilbudet fra Roret.

Hopp over steget når bedriften fakturerer uten tilbud, eller ikke har Salg og
CRM. Bruk ikke `foresla_tilbud` her: den krever en tilbudsmal og en
befaring.

1. Foreslå tilbudet med bare kunden. Det blir et forslag:
   `odoo_create("sale.order", {"partner_id": <kunde-id>}, company_id=<C>)`.
   Brukeren kan også lage det tomme tilbudet selv: Salg → **Tilbud** →
   **Ny**, velg kunden og lagre.
2. Når det er godkjent, finn det:
   `odoo_search_read("sale.order", [["partner_id", "=", <kunde-id>], ["state", "=", "draft"]], ["id", "name", "amount_total"], order="id desc", limit=1, company_id=<C>)`.
3. Legg på linjene, én per kall, først med tørrkjøring:
   `oppdater_tilbud(order_id=<id>, product_id=<produkt>, quantity=<antall>, dry_run=True, company_id=<C>)`.
   Vis summen med og uten MVA, og kjør uten `dry_run` etter ja.
4. Brukeren sender det: Salg → **Tilbud** → tilbudet → **Send**. Kunden får
   en lenke og signerer i portalen. Da blir tilbudet en ordre.

Har kunden sagt ja på annen måte, bekreft ordren med
`bekreft_ordre(order_id=<id>, dry_run=True, company_id=<C>)` og så uten
`dry_run`. Det blir et forslag til godkjenning.

## Steg 9: Første faktura

**Hvem:** Claude lager utkastet og kontrollerer det. Brukeren godkjenner
bokføringen i Assistent → Til godkjenning og sender fakturaen fra Roret.

1. **Utkastet.** Fra en ordre:
   `fakturer_ordre(order_ids=[<ordre-id>], dry_run=True, company_id=<C>)`, og
   så uten `dry_run`. Uten tilbud:
   `opprett_faktura(partner_id=<kunde-id>, lines=[{"product_id": <produkt>, "name": "<tekst>", "quantity": <antall>, "price_unit": <pris>}], company_id=<C>)`.
2. **Kontroller.** `hent_bilag(move_id=<id>, company_id=<C>)` viser linjene,
   MVA og det som mangler. Les i tillegg
   `odoo_search_read("account.move", [["id", "=", <id>]], ["partner_bank_id", "invoice_date_due", "invoice_payment_term_id"], company_id=<C>)`.
   `partner_bank_id` er kontonummeret på fakturaen. Er det tomt, gå tilbake
   til steg 3 før fakturaen bokføres. Vis forfallet og vilkåret (steg 5).
3. **Bokfør** etter ja: `bokfor_bilag(move_id=<id>, company_id=<C>)`. Det
   blir et forslag. Når det er godkjent, har fakturaen nummer, og KID hvis
   KID er på. En bokført faktura rettes med kreditnota, aldri ved å endre den.
4. **Send.** Brukeren åpner Regnskap → Kunder → **Fakturaer** → fakturaen →
   **Send**. Be brukeren åpne PDF-en og se at kontonummeret, KID-en og
   adressen står der før den sendes. Sending per post koster et gebyr som
   står i prislista til Roret.

## Steg 10: Oppsummer

**Hvem:** Claude.

Vis hva som er gjort og av hvem, og hva som gjenstår:

- Bankjournalen uten kontonummer (steg 3): Roret, før første kontoutskrift.
- EHF til kunder som vil ha det: Roret slår det på.
- Kontoutskriften og avstemmingen: `avstem-bank` når innbetalingen kommer.
- Ubetalte fakturaer: `purring`.

## Viktig

- Gjett aldri en menysti. Ser brukeren noe annet enn stien over, spør hva som
  står på skjermen.
- Bokfør aldri en faktura uten kontonummer, og send aldri noe til en kunde
  uten at brukeren har sett mottaker, beløp og tekst.
- Satser, krav til fakturaen og fradragsregler: slå opp med `lov_oppslag`,
  også når du mener å vite svaret, og oppgi paragrafen.
