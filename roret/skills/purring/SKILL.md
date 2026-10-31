---
name: purring
description: Oppfølging av forfalte kundefakturaer etter norsk regelverk — viser hvem som skylder hva, hvilket purretrinn hvert krav står på, forklarer gebyr, rente og forskjellen på forbruker og næringsdrivende, og hjelper brukeren å kjøre purreløpet i Roret eller sende en vennlig påminnelse etter bekreftelse. Bruk denne når brukeren vil purre, følge opp ubetalte fakturaer, sende betalingspåminnelse, inkassovarsel, «hvem skylder oss penger», eller spør om purregebyr og forsinkelsesrente.
---

# Purring

Penger inn er ofte det som betyr mest for en liten bedrift. Hjelp brukeren å
følge opp raskt, riktig og høflig. Bruk `firmaprofil` for selskap, og følg
`roret-prinsipper` for alt som sendes til kunder.

## Steg 1: Hvem skylder hva

```
hent_forfalte_fakturaer(company_id=<id>, move_type="out_invoice", limit=100)
aldersfordelte_kundefordringer(company_id=<id>, move_type="out_invoice")
```

Vis per kunde: antall fakturaer, sum, eldste forfall og dager over forfall.
Sorter med det eldste og største øverst. Gjelder det én kunde, hent bare
hennes: `hent_forfalte_fakturaer(company_id=<id>, move_type="out_invoice", partner_id=<kunde>)`. Sjekk at kravet faktisk er ubetalt,
på to måter, før du purrer:

1. Uavstemte innbetalinger som er koblet til kunden:
   `hent_uavstemte_banklinjer(company_id=<id>, partner_id=<id>)`.
2. Uavstemte innbetalinger uten kunde, der banken ikke fant avsenderen:
   `hent_uavstemte_banklinjer(company_id=<id>, only_without_partner=True)`.
   Se etter beløp, KID eller fakturanummer i teksten.

Finner du en innbetaling som kan høre til kravet, avstem først med
`avstem-bank`. Å purre en kunde som har betalt er det verste som kan skje.

## Steg 2: Hvilket trinn står kravene på

Roret har et norsk purreløp (modulen `l10n_no_account_followup` oppå
purremotoren `account_credit_control`). Har kunden det, står hvert krav på et
trinn. Bekreft feltene først med `odoo_fields_get("credit.control.line")`,
og hent deretter:

```
odoo_search_read("credit.control.line", [["partner_id","=",<kunde>],["state","not in",["sent","ignored"]]], ["invoice_id","policy_level_id","state","date_due","amount_due","balance_due","channel"])
```

Forklar på norsk hva som står for tur: påminnelse, purring med gebyr, eller
inkassovarsel. Feiler kallet fordi modellen ikke finnes, har kunden ikke
purreløpet. Hopp til steg 4.

## Steg 3: Regler, satser og forbruker mot næringsdrivende

Forsinkelsesrenten endres hvert halvår, purregebyret når inkassosatsen
endres, og alt kan endres ved lovendringer. **Skriv aldri et beløp eller
en prosent uten å ha slått det opp.** Har kunden purreløpet, ligger satsene
som data:

```
odoo_search_read("l10n.no.followup.rate", [["active","=",True]], ["code","valid_from","value"], order="code, valid_from desc")
```

Ellers: `lov_oppslag("purregebyr og inkassovarsel, maksimalt gebyr og frister")`
og `lov_oppslag("forsinkelsesrente sats")`. Oppgi lov og paragraf.

Det modulen passer på, og som du skal forklare når brukeren spør:

- **Forbruker eller næringsdrivende.** Kunden er forbruker når
  kontakten ikke er et selskap, med mindre `l10n_no_debtor_class` på kunden
  sier noe annet. Forbrukere kan få purregebyr, men aldri
  standardkompensasjon. Næringsdrivende kan få standardkompensasjon, men ikke
  både den og purregebyr for samme krav.
- **Gebyr** krever et varsel sendt tidligst 14 dager etter forfall, med ny
  frist. Antall gebyrbelagte varsler per krav er begrenset.
- **Forsinkelsesrente** løper fra forfall, og faktureres som en egen nota
  (utenfor MVA).
- **Inkasso:** det siste varselet før et krav sendes til inkasso har krav til
  innhold og frist. Vil brukeren sende til inkasso, anbefal et inkassobyrå.

## Steg 4: Velg handling

Spør brukeren hva de vil:

**(a) Kjør purreløpet i Roret** (anbefalt når kunden har det). Brukeren gjør
det selv i Odoo under menyen **Purring** (på engelsk «Credit Control»): lag
en ny kjøring, se gjennom linjene, og send. Gebyr og rente lages da automatisk og riktig, og vaktene
over gjelder. Du kan vise hva kjøringen kommer til å ta med (steg 2), men
du starter den ikke.

**(b) Vennlig påminnelse fra deg**, for et krav som ikke har nådd første
purretrinn, eller når kunden ikke har purreløpet. Den har ikke gebyr.

1. Les siste kontakt: `les_chatter(model="account.move", res_id=<faktura>, limit=5)`.
   Er det en tvist eller en avtale om betalingsutsettelse, stopp og si fra.
2. Skriv et kort utkast: fakturanummer, beløp, opprinnelig forfall,
   kontonummer og KID, og en høflig beskjed om å se bort fra påminnelsen hvis
   betalingen er på vei.
3. Hent hvem som følger fakturaen, fordi e-posten går til dem også:
   `odoo_search_read("mail.followers", [["res_model", "=", "account.move"], ["res_id", "=", <faktura>]], ["partner_id"])`.
   Vis alle mottakerne og teksten, og vent på ja.
4. Send på fakturaen så det logges der, og kontroller `notified_partner_ids`
   i svaret mot lista:

```
skriv_i_chatter(model="account.move", res_id=<faktura>, body="<tekst>", as_email=True, partner_ids=[<mottaker>], company_id=<id>)
```

**(c) Ring eller send SMS.** For store beløp eller viktige kunder er en
samtale ofte bedre. Foreslå `planlegg_aktivitet` på kunden, eller SMS med
`send_sms(..., dry_run=True)` først.

## Steg 5: Oppsummer

List hva som ble sendt eller planlagt, og hva som venter: krav som får
purring med gebyr neste gang purreløpet kjøres, og krav som nærmer seg
inkasso.

## Viktig

- Ett krav per kunde av gangen ved påminnelser fra deg. Ikke masseutsendelse.
- Aldri purr et krav uten å ha sjekket bank først (steg 1).
- Legg aldri gebyr på en påminnelse du sender selv, og lag aldri en gebyr-
  eller rentenota med `opprett_faktura`. Gebyr og rente går gjennom
  purreløpet, der vaktene gjelder. Har ikke kunden purreløpet: Roret-kunder
  kan be Roret slå det på. I Roret for Odoo er purreløpet ikke med ennå.
