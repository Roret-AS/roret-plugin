# Flytte fra HubSpot

HubSpot er ofte salg, kundeservice og abonnementer på én gang, ikke regnskap.
Flyttingen gjøres i Roret, på serveren, ikke gjennom samtalen: en bedrift har
gjerne titusenvis av kontakter, og det går ikke gjennom konteksten. Du hjelper
brukeren med å forberede, leser prøvekjøringen sammen med brukeren og går
gjennom det som må gjøres før HubSpot sies opp.

**Tokenet skal aldri inn i samtalen.** Be aldri om tilgangstokenet fra HubSpot,
og lim det aldri inn noe sted selv. Brukeren limer det inn i Roret, i skjemaet
for flyttingen. Roret bruker det bare mens hentingen går, og sletter det
etterpå.

**Hvor:** «Kom i gang» → «Flytt kundene og salget fra HubSpot», eller CRM →
Importer og synkroniser → Flytt fra HubSpot. Det krever Salg med oppsett, som
bedriftens administrator har. Ser ikke brukeren punktet, er modulen
`roret_migrering_hubspot` ikke installert i tenanten: be Roret om det
(support@roret.no).

Menystiene i HubSpot under er hentet fra HubSpots egne hjelpesider og kan ha
endret seg. Spør hva brukeren ser hvis et punkt ikke finnes.

## Hva som flyttes, og hvor det havner

| Fra HubSpot | I Roret |
|---|---|
| Selskaper | Kunder (firma). Dubletter slås sammen på org.nr. og domene, og et selskap som finnes i Roret fra før, kobles i stedet for å lages på nytt |
| Kontakter | Kontakter under firmaet. Dubletter slås sammen på e-post |
| Pipelines og stadier for deals | CRM-team med de samme stadiene, eller hoppes over (brukeren velger per pipeline) |
| Deals | Salgsmuligheter med selger, beløp, valuta i beskrivelsen, dato og stadium. Vunne i stadiet for vunnet, tapte arkivert med grunnen «Tapt i HubSpot» |
| Eiere (selgere) | Brukerne i Roret med samme e-post. Ingen brukere lages |
| Tilbud | Historikk på salgsmuligheten, med linjene og PDF-en. Ikke ordre i Roret |
| Notater, samtaler, e-post og møter | Historikk (chatteren) på kontakten, firmaet, muligheten eller saken, med HubSpots tidspunkt |
| Åpne oppgaver | Aktiviteter hos den som eier dem |
| Saker (tickets) | Saker i Kundeservice, ett team per pipeline |
| Abonnementer (Commerce) | Abonnementer med frekvens, valuta (prisliste per valuta), pris og neste fakturadato. På pause i HubSpot: i gang og på pause i Roret, med årsaken «Pause i HubSpot» |
| Samtykke til markedsføring | Samtykkebevis på e-postadressen. Den som har meldt seg av, svartelistes |
| Egendefinerte felt | Bare de brukeren velger, som tekst i notatene. Ingen nye felt i Roret |

**Gamle kontakter blir igjen.** Kontakter og selskaper uten aktivitet,
salgsmulighet eller sak de siste 24 månedene (kan endres) flyttes ikke. Det
samme gjelder salgsmuligheter og saker uten aktivitet i perioden.
Abonnementene flyttes alltid.

**Blir igjen i HubSpot:** markedsførings-e-post og lister, skjemaer og chat på
nettsiden, arbeidsflyter, nettsidene (egen flytting), fakturaer og betalinger
(de hører til regnskapet), vedlegg på notater og e-post, objektet «Leads»,
og egendefinerte felt som ikke er valgt.

## Før flyttingen

1. **Riktig konto.** Har brukeren HubSpot koblet til Claude, sjekk at det er
   bedriftens konto (portalnavn og valuta) før du leser noe.
2. **Kartlegg** med lesing hvis HubSpot er koblet til: antall kontakter og
   selskaper, deals per pipeline, tilbud, saker, og abonnementer per status,
   frekvens og valuta. Da vet dere hva prøvekjøringen bør vise.
3. **Pipelines:** gå gjennom deal-pipelinene med brukeren. Noen er
   driftstavler (frakt, oppfølging) med mange åpne deals og uten lukket
   stadium. Roret hopper over dem som standard, men brukeren velger.
4. **Overgangen for abonnementene:** avtal datoen Roret skal fakturere fra.
   En periode med neste faktura før datoen faktureres av HubSpot. Spør
   hvordan kundene betaler: kort (automatisk trekk) eller faktura. Korttrekket
   i Roret kobler kortet i Stripe til kunden på e-post.
5. **Pause og ubetalt:** et abonnement på pause i HubSpot settes på pause i
   Roret fra flyttingen, uten dato for gjenopptak, og faktureres ikke før
   noen trykker «Gjenoppta». Et ubetalt abonnement flyttes uten fakturering
   og merkes «Ubetalt i HubSpot». Spør brukeren hvilke som er gratis med
   vilje, og hvilke som ikke betaler. Systemene skiller ikke mellom dem.
6. **Selgerne:** brukerne i Roret må finnes før flyttingen, med samme e-post
   som i HubSpot, ellers får det de eier, ingen selger.

⛔ Oppsummer: pipelines som flyttes og hoppes over, datoen for abonnementene,
og om selgerne har brukere. Få ja før brukeren starter.

## Den private appen i HubSpot

Brukeren må være superadministrator i HubSpot.

1. Innstillinger (tannhjulet) → Integrasjoner → Private apper → lag en ny app.
   Kall den «Flytting til Roret».
2. Under Omfang krysser brukeren av for bare lesing:
   `crm.objects.companies.read`, `crm.objects.contacts.read`,
   `crm.objects.deals.read`, `crm.objects.owners.read`,
   `crm.objects.quotes.read`, `crm.objects.line_items.read`,
   `crm.objects.subscriptions.read`, `crm.schemas.companies.read`,
   `crm.schemas.contacts.read`, `crm.schemas.deals.read`, `tickets`,
   `e-commerce` og `sales-email-read`.
3. Lag appen og kopier tokenet rett inn i Roret. Ikke i samtalen.

Mangler en tilgang, flyttes ikke den delen, og prøvekjøringen sier hvilken.

## Prøvekjøringen

Brukeren limer inn tokenet og trykker «Koble til HubSpot», velger pipelines,
felt og datoen, og trykker «Start prøvekjøringen». Hentingen går i bakgrunnen,
med mange kontakter en stund. Ingenting skrives i Roret.

Les rapporten med `odoo_search_read` på `roret.migrering.kjoring`
(feltene `name`, `tilstand`, `fremdrift`, `rapport`, `feilmelding`), og
avvikene på `roret.migrering.avvik` (`type`, `ekstern_id`, `alvor`,
`melding`) for den kjøringen. Gå gjennom «Det viktigste» i rapporten punkt for
punkt:

- Selgere uten bruker: lag brukerne, eller godta at det de eier står uten
  selger.
- Dubletter og det som finnes fra før: stemmer det med det brukeren venter?
- Abonnementer som venter på overgangen, står på pause, er ubetalte eller må
  sjekkes. Abonnementene på pause står under Abonnementer → «På pause», med
  årsaken «Pause i HubSpot».
- Felt som blir igjen i HubSpot: er det noe brukeren trenger?
- Stadier som er felles for alle team i Roret (for eksempel «Kvalifisert» og
  «Forslag»): de vises også i pipelinene fra HubSpot. Skal de bort, gjør
  brukeren det under CRM → Konfigurasjon → Stadier.
- Tilganger som mangler.

Endrer brukeren pipelines, filteret eller datoen, trykker hen «Oppdater
prøvekjøringen». Feltene og org.nr.-feltet krever en ny flytting.

Stopper hentingen (HubSpot svarer ikke, eller dagsgrensen er nådd), er
tokenet slettet. Brukeren limer det inn på nytt og trykker «Prøv igjen», og
hentingen fortsetter der den stoppet.

⛔ Brukeren trykker «Flytt nå» selv i Roret når rapporten er gjennomgått.

## Etter flyttingen

Rapporten arkiveres av seg selv i dokumentarkivet, i mappen «Flytting til
Roret», med en kontroll av at Roret fikk de samme tallene som prøvekjøringen.
Finn den med `finn_dokumenter` hvis brukeren spør etter den.

- [ ] Kontrollen i rapporten stemmer, og avvikene er gått gjennom.
- [ ] Kjør flyttingen på nytt (knappen «Kjør på nytt») rett før overgangen.
      Det som er flyttet, flyttes ikke på nytt, men abonnementene får ny neste
      fakturadato, og nye kontakter og saker kommer med. Er et abonnement
      gjenopptatt i HubSpot, gjenopptas det i Roret. En pause noen har endret
      i Roret, står.
- [ ] Stopp faktureringen i HubSpot før datoen Roret fakturerer fra, så
      kundene ikke får faktura fra begge.
- [ ] Ta ut en eksport av samtykkene i HubSpot (tekst og tidspunkt). Beviset
      ligger der.
- [ ] Slett den private appen i HubSpot. Da virker tokenet ikke lenger.

## Før HubSpot sies opp

- [ ] Fornyelsesdatoen i HubSpot-avtalen: den avgjør når HubSpot kan slås av.
- [ ] Skjemaer og chat på nettsiden er byttet til Roret.
- [ ] Fakturaene og betalingene fra HubSpot er avstemt i regnskapet.
- [ ] Det som blir igjen (markedsføringslister, arbeidsflyter, vedlegg) er
      lastet ned eller bevisst lagt igjen.
