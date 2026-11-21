---
name: abonnement
description: Setter opp faste avtaler i Abonnement i Roret — produktene, abonnementsmalene med intervall og faktureringsmåte, avtalene per kunde, start og første faktura — og kontrollerer at ingen avtale blir stående i «Utkast» uten å faktureres. Sier for hvert steg om Claude eller brukeren gjør det, med stien i Roret. Bruk denne når brukeren vil lage abonnementer, serviceavtaler, faste månedsfakturaer eller medlemskap, flytte faste avtaler inn i Roret, eller lurer på hvorfor et abonnement ikke fakturerer eller ikke teller i inntekten per måned.
---

# Abonnement

Et abonnement i Roret er en avtale med én kunde, laget fra en
**abonnementsmal** (hvor ofte og hvordan det faktureres), med linjer for
produktene. Bare avtaler i stadiet **Pågår** faktureres og teller i inntekten
per måned (MRR). En avtale i **Utkast** blir liggende der, uten faktura og
uten at noe sier fra. Det er den vanligste feilen, og steg 7 kontrollerer
den.

Krever funksjonen Abonnement. Følg `roret-prinsipper`, og bruk `firmaprofil`
for selskapet (`<C>` er `company_id`). Det finnes ingen egne verktøy for å
lage maler og avtaler ennå. Denne skillen sier derfor hvilke rå kall som er
lov. De blir forslag som venter på godkjenning i Roret, i appen
**Assistent → Til godkjenning**. Ta alle postene av samme slag i ett kall,
så blir det ett kort å godkjenne, ikke ett per kunde. Ett forslag kan lage
høyst 50 nye poster og endre høyst 100. Flere tas i porsjoner. Fakturaene skal ha
kontonummer og eventuelt KID før de går ut. Er det ikke på plass, ta
`sett-opp-bedriften` først.

## Steg 1: Rammen

**Hvem:** Claude spør og leser. Ingenting endres.

Avklar med brukeren:

- **Hva selges:** planene (for eksempel «Basis» og «Pluss»), prisen per
  periode og hvor ofte de faktureres (månedlig, kvartalsvis, årlig).
- **Hvem:** kundene og planen hver av dem har. Kundene må finnes som
  kontakter. Mange nye kunder: `kunderegister` først.
- **Start:** nye avtaler fra i dag, nye avtaler fra en dato, eller avtaler
  som er fakturert i et annet system fram til en dato.
- **Faktureringsmåte** (steg 2).
- **Forbrukere:** selger bedriften til privatpersoner, slå opp angrerett,
  opplysningsplikt og oppsigelse med `lov_oppslag` før vilkårene skrives.

Les det som finnes:

```
abonnementsinntekt_per_maaned(company_id=<C>)
odoo_search_read("sale.subscription.template", [], ["id", "name", "recurring_interval", "recurring_rule_type", "invoicing_mode"], context={"lang": "nb_NO"}, company_id=<C>)
odoo_search_read("sale.subscription.stage", [], ["id", "name", "type"], context={"lang": "nb_NO"}, company_id=<C>)
```

Svarer verktøyet at Abonnement ikke er installert, har bedriften ikke
funksjonen. Den legges til hos Roret (se hjelpen om funksjoner og pris).
Stadiene har `type`: `draft` er Utkast, `pre` er Klar til start,
`in_progress` er Pågår og `post` er Avsluttet.

## Steg 2: Abonnementsmalene

**Hvem:** Claude foreslår malene. Brukeren godkjenner i Assistent → Til
godkjenning, eller lager dem selv i Roret.

Én mal per måte å fakturere på. Faktureringsmåten bestemmer hva som skjer når
jobben lager fakturaen:

| `invoicing_mode` | I Roret | Hva skjer |
|---|---|---|
| `draft` | Utkast | Fakturaen blir et utkast. Noen må bokføre og sende den |
| `invoice` | Faktura | Fakturaen bokføres, men sendes ikke |
| `invoice_send` | Fakturer og send | Fakturaen bokføres og sendes på e-post til kunden, uten stopp |
| `sale_and_invoice` | Salgsordre og faktura | En ordre og en bokført faktura |

Anbefal **Utkast** for den første runden, så brukeren ser fakturaene før de
går ut. Når de er riktige, kan malen byttes til **Fakturer og send**. Det
sparer én godkjenning per faktura hver periode, men fakturaene går da rett
til kundene. Det er brukerens valg.

Vis malene og foreslå dem samlet etter ja:

```
odoo_create("sale.subscription.template", [{"name": "<navn>", "recurring_interval": 1, "recurring_rule_type": "months", "invoicing_mode": "draft"}], company_id=<C>)
```

`recurring_rule_type` er `days`, `weeks`, `months` eller `years`. Kvartalsvis
er `months` med `recurring_interval` 3.

Brukeren kan også lage malen selv: Abonnementer → Konfigurasjon →
**Abonnementsmaler** → **Ny**, med **Gjenta hver**, **Gjentakelse** og
**Faktureringsmåte**.

## Steg 3: Produktene

**Hvem:** Claude lager produktene etter ja, og foreslår koblingen til malen.
Brukeren godkjenner koblingen i Assistent → Til godkjenning.

Ett produkt per plan, med prisen per periode i malen, uten MVA. Oppgir
brukeren priser med MVA, regn om med satsen fra `lov_oppslag`.

```
opprett_produkt(name="<plan>", type="service", list_price=<pris per periode uten MVA>, default_code="<varenummer>", description_sale="<tekst på fakturaen>", dry_run=True, company_id=<C>)
```

Kjør uten `dry_run` etter ja. Se `produkter` for MVA-koden og kontrollen av
den. Merk produktene som abonnementsprodukter med sin mal, i ett kall:

```
odoo_write("product.template", [<id>, <id>], {"subscribable": true, "subscription_template_id": <mal-id>}, company_id=<C>)
```

`id` er malen til produktet (`id` i svaret fra `opprett_produkt`, ikke
`product_id`). Produkter med ulike maler tar ett kall per mal. Brukeren kan
også gjøre det selv: Abonnementer → Abonnementer → **Produkter** → produktet →
fanen **Salg** → **Produkt for abonnement** og **Abonnementsmal**.

## Steg 4: Avtalene

**Hvem:** Claude foreslår alle avtalene i ett kall. Brukeren godkjenner i
Assistent → Til godkjenning.

**Selges avtalen med et tilbud**, gå heller den veien: et tilbud med
abonnementsproduktet (se `sett-opp-bedriften` steg 8). Når ordren bekreftes,
lager Roret abonnementet og starter det, og første periode faktureres fra
ordren med `fakturer_ordre`. Tilbudet har feltet **Abonnementsmal** når
avtalen skal ha en annen mal enn produktets. Da kan steg 5 og 6 hoppes over.

**Ellers** lages avtalene direkte. Slå opp kundene (`finn_kunde`), prislista
og stadiene fra steg 1:

```
odoo_search_read("product.pricelist", [], ["id", "name", "currency_id"], company_id=<C>)
```

Velg stadium og startdato for hver avtale:

| Situasjon | `stage_id` | `date_start` | Første faktura |
|---|---|---|---|
| Starter i dag | Utkast | i dag | Etter start i steg 5, se steg 6 |
| Starter på en dato | Klar til start | datoen | Jobben starter avtalen og lager fakturaen på datoen |
| Fakturert i et annet system til en dato | Klar til start | første dag som ikke er fakturert | Som over. Perioden som alt er fakturert, faktureres ikke på nytt |

Vis lista (kunde, plan, antall, pris per periode, stadium, startdato), og
foreslå alle etter ja:

```
odoo_create("sale.subscription", [{"partner_id": <kunde-id>, "template_id": <mal-id>, "pricelist_id": <prisliste-id>, "stage_id": <stadium-id>, "date_start": "YYYY-MM-DD", "sale_subscription_line_ids": [[0, 0, {"product_id": <product_id>, "product_uom_qty": 1}]]}], company_id=<C>)
```

- Oppgi alltid `stage_id`. Uten stadium blir avtalen verken startet eller
  fakturert.
- Når jobben starter en avtale i Klar til start, begynner den første perioden
  den dagen. Ligger startdatoen bakover i tid, faktureres ikke dagene før
  det. Si det, og la brukeren avgjøre hvordan de faktureres.
- Oppgi ikke `recurring_next_date` sammen med `date_start` når avtalen lages.
  Da setter Abonnement den til Utkast, uansett stadium.
- Prisen og MVA-koden på linja kommer fra produktet og prislista. Avtalt pris
  for én kunde settes med `"price_unit"` på linja, og rabatt med
  `"discount"`.

## Steg 5: Start avtalene som starter i dag

**Hvem:** Claude foreslår starten. Brukeren godkjenner i Assistent → Til
godkjenning, eller starter avtalene selv i Roret.

Bare avtalene i Utkast. Avtalene i Klar til start starter av seg selv på
datoen. Finn dem og foreslå starten samlet:

```
odoo_search_read("sale.subscription", [["stage_id.type", "=", "draft"]], ["id", "name", "partner_id", "recurring_total"], company_id=<C>)
odoo_call_button("sale.subscription", "action_start_subscription", ids=[<id>, <id>], company_id=<C>)
```

Kortet kan vise metodenavnet «action_start_subscription». Si til brukeren at
det er starten. Brukeren kan også starte en avtale selv: Abonnementer →
Abonnementer → avtalen → klikk **Pågår** i statuslinja øverst.

En avtale som startes, får startdato i dag og neste fakturadato i dag.

## Steg 6: Første faktura

**Hvem:** brukeren lager fakturaen i Roret, eller venter på den daglige
jobben. Claude kontrollerer og bokfører etter ja.

Den daglige jobben lager fakturaen for avtalene som pågår og har neste
fakturadato i dag eller tidligere. Vil brukeren ha fakturaen med en gang: Abonnementer →
Abonnementer → avtalen → **Opprett faktura**. Knappen kan ikke trykkes
herfra. Trykk den bare én gang per avtale.

Med faktureringsmåten Utkast:

1. Finn utkastene: `hent_utkastfakturaer(move_type="out_invoice", company_id=<C>)`.
2. Kontroller hvert: `hent_bilag(move_id=<id>, company_id=<C>)`. Sjekk
   kunden, perioden på linja, beløpet, MVA-koden og at kontonummeret står
   der (se `sett-opp-bedriften` steg 9).
3. Bokfør etter ja: `bokfor_bilag(move_id=<id>, company_id=<C>)`. Hver
   bokføring blir et forslag.
4. Brukeren sender fakturaene: Regnskap → Kunder → **Fakturaer** → velg
   fakturaene → **Send**.

Har selskapet periodisering slått på, lager bokføringen av en faktura for
flere måneder egne bilag for periodiseringen. Si det, så brukeren ikke tror
det er feil.

## Steg 7: Kontroller

**Hvem:** Claude leser og sier fra.

```
abonnementsinntekt_per_maaned(company_id=<C>)
odoo_search_read("sale.subscription", [], ["name", "partner_id", "stage_id", "date_start", "recurring_next_date", "recurring_total"], context={"lang": "nb_NO"}, company_id=<C>)
```

- **Står en avtale i Utkast,** faktureres den aldri. Si det med navn og
  kunde, og gå tilbake til steg 5.
- **Står den uten stadium,** gjelder det samme. Foreslå stadiet med
  `odoo_write` på `stage_id`.
- **Klar til start** med en dato fram i tid teller ikke i MRR før datoen. Si
  det, så null ikke ser ut som en feil.
- **Neste fakturadato** skal være dagen den neste perioden begynner. Sett den
  aldri bakover: da faktureres perioden på nytt.
- Sammenlign MRR med summen brukeren forventer, og forklar forskjellen.

## Etterpå

- Pause og oppsigelse gjør brukeren på avtalen i Roret: **Sett på pause** og
  **Si opp**. Pausene står under Abonnementer → Abonnementer → **På pause**.
- Følg inntekten med `abonnementsinntekt_per_maaned` og
  `abonnementsinntekt_over_tid`, og ubetalte avtaler med `purring`.
- Bytt malen til **Fakturer og send** når den første runden er riktig, om
  brukeren vil det (steg 2).
