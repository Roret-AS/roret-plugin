---
name: avstem-bank
description: Guidet bankavstemming i Roret — henter banklinjer som ikke er avstemt, foreslår treff mot bestemte fakturaer eller hovedbokslinjer, og avstemmer etter bekreftelse, også Stripe-utbetalinger med gebyr. Bruk denne når brukeren vil avstemme bank, matche innbetalinger eller utbetalinger mot fakturaer, rydde i uavstemte banktransaksjoner, eller nevner bankavstemming eller reconciliation.
---

# Avstem bank

Følg `roret-prinsipper` §3 strengt: avstem mot bestemte fakturaer, aldri
bare mot kundens konto. Over- og underbetaling avgjøres av brukeren i Odoo.
Bruk `firmaprofil` for selskapet.

## Steg 1: Hent banklinjene

Ga brukeren en bestemt banklinje, gå rett til steg 3.

```
hent_uavstemte_banklinjer(company_id=<id>, limit=20)
```

Har selskapet flere bankkontoer, kan du avgrense med `journal_id`. Vis en
kort liste:

```
1. 19.05.2026  +8 623,65 kr  «Brødrene Hansen AS»       (ingen partner)
2. 12.05.2026  +10 836,00 kr «Faktura 1042»
3. 10.05.2026  −1 249,00 kr  «Varekjøp Grossist AS»
```

## Steg 2: Velg linje

Spør hvilken linje dere starter med, eller om dere skal gå gjennom dem i
rekkefølge.

## Steg 3: Finn treff

Er teksten på banklinja en Stripe-utbetaling, gå til Stripe-flyten under.
Netto utbetaling matcher aldri én faktura. Teksten kan være «Stripe» eller
navnet på banken Stripe utbetaler gjennom (for eksempel «Banking Circle»),
men flere betalingsformidlere bruker samme bank. Bruker selskapet ikke Stripe,
eller er du i tvil, spør.

Ellers:

```
foresla_treff_for_banklinje(bank_line_id=<id>, company_id=<id>)
```

Følg `best_strategy`:

**`single_invoice`:** vis fakturaen og spør.
«Banklinja matcher faktura 2026/0153 på 8 623,65 kr, forfall 16.04.2026.
Skal jeg avstemme?» Ved ja:

```
avstem_banklinje_mot_faktura(bank_line_id=<id>, invoice_id=<id>, company_id=<id>)
```

**`invoice_combination`:** vis fakturaene og summen, og spør. Ved ja:

```
avstem_banklinje_mot_fakturaer(bank_line_id=<id>, invoice_ids=[<id>, <id>], company_id=<id>)
```

**`existing_payment`:** det finnes allerede en registrert betaling som venter.
Forklar det, og vis brukeren hvor den lukkes i avstemmingsbildet i Odoo.

**`needs_review`:** ingen sikker match. Vis `recommendation`, delvise treff
og partnerkandidater, og la brukeren velge:
(a) avstemme i Odoo med delbetaling, (b) hoppe over linja, eller
(c) se mer sammenheng (chatter på kunden, andre åpne fakturaer).

**Ikke en faktura** (lønn, skattetrekk, MVA-oppgjør, lån, overføring mellom
egne kontoer): finn den åpne hovedbokslinja på riktig konto med
`odoo_search_read("account.move.line", [["account_id","=",<konto>],["reconciled","=",False],["parent_state","=","posted"]], ["id","name","date","amount_residual"])`,
vis den, og avstem etter ja:

```
avstem_banklinje_mot_hovedbokslinje(bank_line_id=<id>, counterpart_line_id=<id>, company_id=<id>)
avstem_banklinje_mot_hovedbokslinjer(bank_line_id=<id>, counterpart_line_ids=[<id>, <id>], company_id=<id>)
```

## Stripe-flyten

Stripe slår sammen mange betalinger i én netto utbetaling og trekker gebyret
først. Banklinja viser netto. De åpne kvitteringslinjene på
kvitteringskontoen summerer til brutto. Differansen er gebyret.

1. **Finn kontoene, aldri hardkod id-er.** Spør brukeren hvilken konto
   Stripe-kvitteringene står på hvis du ikke ser det, og slå opp:
   `odoo_search_read("account.account", [["code","=like","1923%"]], ["id","code","name"])`
   (eksempel). Gebyrkontoen er vanligvis 7770 Bank- og kortgebyrer:
   `odoo_search_read("account.account", [["code","=like","7770%"]], ["id","code","name"])`.
2. **Hent kvitteringslinjene** på kvitteringskontoen:
   `odoo_search_read("account.move.line", [["account_id","=",<konto>],["reconciled","=",False],["parent_state","=","posted"]], ["id","name","date","balance","amount_residual"])`.
3. **Finn delmengden** som gir netto. Har brukeren Stripe-connectoren i
   Claude, hent betalingene med gebyr (netto per betaling) i perioden før
   utbetalingen, og match netto mot banklinja. Uten connector: velg linjene
   der dato passer og brutto minus netto blir et rimelig gebyr (vanligvis
   noen prosent). Gir mer enn én kombinasjon samme sum, eller ingen, stopp
   og la brukeren velge.
4. **Vis splitten og spør.** «Stripe-utbetaling 1 889,51 kr = 2 betalinger
   brutto 1 953,00 kr minus gebyr 63,49 kr til 7770. Skal jeg avstemme og
   bokføre gebyret?»
5. Ved ja:

```
avstem_stripe_utbetaling(bank_line_id=<id>, receipt_line_ids=[<id>, <id>], fee_account_id=<7770-id>, company_id=<id>, payout_ref="<po_... hvis kjent>")
```

Verktøyet avviser urimelige gebyrer. Da er utvalget feil. Ikke tving det.
Gebyr for selve betalingsformidlingen er normalt unntatt fra MVA som
finansiell tjeneste. Andre tjenester fra Stripe (for eksempel abonnement på
verktøy) kan gi snudd avregning fordi de kjøpes fra utlandet. Slå opp med
`lov_oppslag`, og spør regnskapsføreren hvis brukeren er i tvil.

## Steg 4: Etter avstemming

Bekreft at linja er avstemt og fakturaen betalt, og spør om dere tar neste
linje. Etter tre avstemminger: oppsummer det som er gjort før dere går videre
(`roret-prinsipper` §2).

## Viktig

- Avstem aldri uten bekreftelse.
- Legg aldri restbeløp på en partnerkonto med `odoo_create` eller `odoo_write`.
- Valutaforskjell eller låst journal: pek på Odoo-UI-et.
