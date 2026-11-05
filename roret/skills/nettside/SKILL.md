---
name: nettside
description: Bygger og endrer nettsiden i Odoo: sider, skjemaer, kalkulatorer, bilder, menyer, omdirigeringer, SEO og kode i head. Bruk når brukeren vil lage en ny side, endre tekst, legge til et skjema eller en kalkulator, eller rydde i menyen.
---

# Nettside

Alt på nettsiden kan bygges herfra: sider, deler av siden som header og footer,
kode i `<head>`, bilder, menyer og omdirigeringer. De rå verktøyene er stengt for
det, fordi en side kan kjøre kode.

Skriveregler: `roret-prinsipper`.

## Steg 1: Se hva som finnes

```
hent_nettsted()
hent_nettsted(website_id=<id>)
les_nettside(website_id=<id>, url="/")
```

Svaret fra `les_nettside` har `versjon`, og `spraak_ulike` sier om et annet språk
har egen tekst. Følg det som finnes: fargene, klassene og oppbyggingen på sidene
nettstedet har fra før.

## Steg 2: Endre

**Små endringer på en side som finnes:** bruk `endringer`. De er eksakte
tekstbytter, og alle må treffe, ellers skjer ingenting. Tom `ny` fjerner teksten.

```
lagre_nettside(website_id=<id>, url="/", versjon=<versjon>, endringer=[
    {"gammel": "<h1>Gammel tittel</h1>", "ny": "<h1>Ny tittel</h1>"},
])
```

**Ny side:** `innhold` er det som skal stå i siden. Verktøyet pakker det inn i
nettstedets layout. En ny side er upublisert til du sier noe annet, så vis den
til brukeren før du publiserer.

```
lagre_nettside(website_id=<id>, url="/borettslag/brann", navn="Brann",
               innhold="<section>…</section>", seo_tittel="…", seo_beskrivelse="…")
lagre_nettside(website_id=<id>, url="/borettslag/brann", publisert=True)
```

**Bilder:** last opp først, og bruk adressen du får tilbake. Ligger bildet på
nett, gi `url`: Roret henter det selv, så fila går ikke gjennom samtalen.
`innhold_base64` er for små filer som ikoner, høyst 3 MB. En SVG skriver du rett i
siden. Bruk bare bilder kunden har rett til å bruke.

```
last_opp_nettsidebilde(website_id=<id>, navn="brann.webp", url="https://…/brann.webp")
last_opp_nettsidebilde(website_id=<id>, navn="ikon.png", innhold_base64=<base64>)
```

**Skjemaer** som sender til Odoo, trenger CSRF-tokenet:

```html
<form action="/website/form/" method="post" class="s_website_form"
      data-model_name="crm.lead" data-success-mode="redirect" data-success-page="/takk">
  <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
  …
</form>
```

**Header, footer og annet på alle sidene:** `lagre_nettsidedel`, med `arver_fra`
og `<xpath>`. `position="before"` og `"after"` på en enkel XPath (`//main`,
`//div[@id='x']`) går rett gjennom med vanlig innhold, og alt annet blir et forslag. **CSS, meta-tagger og JSON-LD for hele nettstedet:**
`lagre_nettstedkode`. Andre elementer der blir et forslag. **Meny og gamle adresser:** `lagre_nettsidemeny` og
`lagre_omdirigering`. Flytter du en side, lag en 301 fra den gamle adressen.

## Skript og kalkulatorer

Nytt JavaScript blir et forslag: `status` er `venter_paa_godkjenning`, og et
menneske ser koden og godkjenner den i Roret eller i Odoo. Si det til brukeren,
og ikke prøv å komme rundt det. Svarer verktøyet at Roret ikke kan lage et forslag
ennå, må brukeren gjøre det i Odoo eller slå på verktøyet for basen.

Prøv med `dry_run=True` først. Da ser du hva kontrollen finner, uten at noe
skrives. Det som står på siden fra før, teller ikke, så en tekstendring på en side
med skript går rett gjennom.

Skriv JavaScript som XML: `&lt;` og `&gt;` for `<` og `>`, eller bruk `!=`. Rør
aldri en `<script>` uten at brukeren ba om det.

## Det som ikke går

QWeb-uttrykk som kaller noe (`request.env…`, `.sudo()`, `search()`), `t-raw`,
ukjente direktiver, to attributter med samme navn og elementer inne i `<script>`
eller `<style>` nektes, og godkjenning hjelper ikke. Trengs data fra Odoo på en
side, er et lesende uttrykk som `t-out="product.name"` mulig som forslag. Trengs
mer, må det bli en modul.

Stier Odoo selv bruker (`/web`, `/my`, `/odoo` …) kan ikke brukes. Maler fra
Enterprise-moduler leses og arves ikke.

## Steg 3: Sjekk

Åpne siden anonymt, på mobil og på PC, og se at den ser riktig ut før du sier at
den er ferdig. Si hva du endret, og lenk til siden.
