---
name: mva-termin
description: Kontrollerer MVA-grunnlaget før terminfristen — utkast og uavstemte banklinjer i terminen, MVA-koder som skiller seg ut, kjøp fra utlandet med snudd avregning, sammenligning med forrige termin — og viser status for MVA-meldingen i Roret og hva brukeren selv må gjøre for å sende den. Sender aldri meldingen. Bruk denne når brukeren vil sjekke MVA før fristen, spør «er vi klare for MVA-meldingen», nevner terminoppgave, MVA-termin, mva-melding, eller vil vite hva som skal betales i MVA.
---

# MVA-termin

Målet er at grunnlaget er riktig før meldingen lages, og at brukeren vet hva
som gjenstår. **Du sender aldri MVA-meldingen.** Innsendingen er bindende og
gjøres av et menneske som logger inn med ID-porten (for eksempel BankID) i
Roret. Meldingen regnes først som levert
når tilbakemeldingen fra Skatteetaten er hentet og meldingen står som
fastsatt. «Sendt» alene er ikke ferdig.

## Steg 1: Hvilken termin

Bruk `firmaprofil`: er selskapet MVA-registrert, og har det terminer
annenhver måned eller årstermin? Alminnelige terminer:

| Termin | Måneder |
|---|---|
| 1 | januar–februar |
| 2 | mars–april |
| 3 | mai–juni |
| 4 | juli–august |
| 5 | september–oktober |
| 6 | november–desember |

Fristen for terminen gir
`frister(company_id=<id>, date_from=<terminslutt>, date_to=<terminslutt + 75 dager>)`,
med hjemmel og flytting når fristen faller på helg eller helligdag.

Byttet selskapet til Roret midt i et år, sendes terminene før byttet fra det
gamle systemet. Spør hvilken termin som er den første fra Roret hvis du er i
tvil, og se `firmaprofil` (MVA-terminen). Kontroller aldri en termin som skal
leveres fra det gamle systemet, som om den skulle leveres fra Roret.

## Steg 2: Status for meldingen i Roret

Har kunden Rorets MVA-melding, gir `mva_status` tilstand, beregnet MVA,
avvik fra kontrollene, Skatteetatens svar, betalingen og neste steg. Det
leser bare:

```
mva_status(year=<år>, period="<termin 1–6 eller aarlig>", company_id=<id>)
```

`neste_handling.beskrivelse` sier hva som gjenstår, og `neste_handling.i_roret`
hvilken knapp brukeren trykker. Står `krever_menneske`, må brukeren gjøre det
selv. Sier verktøyet at kunden ikke har MVA-meldingen i Roret, fortsett med
steg 3 og pek på regnskapets egen MVA-rapport.

## Steg 3: Kontroller grunnlaget

Kjør disse for terminens datoer (`date_from`, `date_to`):

1. **Utkast i terminen.** `hent_utkastfakturaer(company_id=<id>, limit=100)`.
   Utkast med dato i terminen er ikke med i grunnlaget. Skal de bokføres
   først?
2. **Uavstemte banklinjer.** `hent_uavstemte_banklinjer(company_id=<id>, date_from="<date_from>", date_to="<date_to>", limit=100)`.
   Penger som har gått inn eller ut uten bilag, kan være salg eller kjøp som
   mangler.
3. **Innboks.** `hent_dokumenter(company_id=<id>, only_inbox=True, only_unfiled=True)`.
   Ubehandlede leverandørfakturaer i terminen gir for lite inngående MVA.
4. **MVA per kode.** `mva_sammendrag(date_from="<date_from>", date_to="<date_to>", company_id=<id>)`,
   og samme for forrige termin. Se etter koder som er tomme nå, men ikke før,
   og store hopp.
5. **Snudd avregning.** Kjøp av tjenester fra utlandet (programvare,
   annonser, skytjenester) skal ha snudd avregning: beregnet utgående MVA og
   fradrag i samme melding. Finn leverandørfakturaer i terminen fra
   utenlandske leverandører:
   `odoo_search_read("account.move", [["move_type","=","in_invoice"],["state","=","posted"],["invoice_date",">=","<date_from>"],["invoice_date","<=","<date_to>"],["partner_id.country_id.code","!=","NO"],["company_id","=",<id>]], ["name","partner_id","amount_untaxed","amount_tax"])`.
   Fakturaer med `amount_tax` 0 og ingen snudd avregning på linjene må
   sjekkes. Slå opp reglene med `lov_oppslag` hvis brukeren er usikker.
6. **Kostnader uten MVA-kode** på kontoer som vanligvis har fradrag: se
   linjer i terminen uten `tax_ids` på kostnadskontoer, og spør om de er
   riktige (for eksempel representasjon, som ikke gir fradrag).

Vis funnene som en kort liste med det som bør rettes før meldingen lages.

## Steg 4: Lag tallene

Er grunnlaget klart, ber du brukeren lage tallene i Roret: åpne meldingen for
terminen (eller lag en ny) og trykk **Hent tallene**. Det henter tallene og
kjører Skatteetatens kontroller lokalt, og sender ingenting. Agenten gjør
ikke dette selv.

Kjør `mva_status` igjen etterpå, og vis beregnet MVA (`fastsatt_mva`) og
avvikene. Blokkerende avvik må rettes før innsending.

## Steg 5: Det brukeren gjør selv

Si tydelig hva som gjenstår, og hvor:

1. Åpne **Regnskap → Rapportering → MVA og skatt → MVA-meldinger** og
   meldingen for terminen. Hovedmenyen kan hete Fakturering i stedet for
   Regnskap, og menyen vises bare for brukere med full regnskapstilgang.
2. Kontroller spesifikasjonen og eventuelle merknader.
3. Trykk **Send inn** og logg inn med ID-porten (for eksempel BankID).
   Personen må ha rett til å sende MVA-melding for selskapet i Altinn.
4. Vent på svaret. Meldingen er levert når den står som **Fastsatt av
   Skatteetaten**. Står den som **Avvist**, sier meldingen hva som må rettes.
5. Bokfør oppgjøret og betal med beløp og KID fra Skatteetaten, innen
   betalingsfristen.

Kom tilbake og sjekk status med `mva_status` når brukeren har sendt. Først
når meldingen står som fastsatt, er terminen ferdig.

## Viktig

- Tallene fra `mva_sammendrag` er en kontroll, ikke meldingen
  (`roret-prinsipper` §7).
- Agenten lager, endrer og sender aldri MVA-meldingen. Den leser status med
  `mva_status`. Alt annet gjør brukeren i Roret.
- Rettelser i en termin som er sendt, gjøres med en ny melding for samme
  termin. Gjelder det en tidligere periode, slå opp reglene med `lov_gjaldt`.
