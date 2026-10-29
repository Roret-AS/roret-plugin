---
name: selskapshandling
description: Fører utbytte, tilbakebetaling av innbetalt kapital og lån til aksjonær gjennom Roret Styring fra forslag til vedtak, bilag, betaling og rapportering, med aksjelovens kontroller underveis. Bruk denne når brukeren vil ta ut utbytte, betale tilbake overkurs eller aksjekapital, låne ut penger til en aksjonær, spør hvor en selskapshandling står, eller trenger betalingslisten eller bilaget for en utdeling.
---

# Selskapshandling

En selskapshandling kjører én handling på skinner: forslag → vedtak →
dokumenter → eventuell innsending og ventetid → bokføring → betaling →
rapportering. Roret eier rekkefølgen og sperrene. Du hjelper brukeren
gjennom dem, men vedtak treffes av styret og generalforsamlingen i møtene, og
protokollene signeres der.

Krever Styring og at brukeren er styresekretær. Skriveregler:
`roret-prinsipper`. Selskap: `firmaprofil`.

## Hvor står vi?

```
hent_selskapshandlinger(only_open=True, company_id=<id>)
forklar_selskapshandling(action_id=<id>)
```

`forklar_selskapshandling` sier hva som står for tur, hva som stopper det og
hva brukeren må gjøre, med paragraf. Gi svaret videre på norsk, med
paragrafen. Detaljer: `hent_selskapshandling(action_id=<id>)`.

## Ny handling

1. Avklar type og beløp:
   - `dividend`: utbytte
   - `capital_repayment`: tilbakebetaling av innbetalt kapital (overkurs
     eller aksjekapital)
   - `shareholder_loan`: lån til aksjeeier (vedtas av styret)
2. Kjør alltid forhåndsvisningen først:

```
foresla_selskapshandling(action_type="dividend", amount=<kr>, dry_run=True, company_id=<id>)
```

   Forhåndsvisningen viser utbyttegrunnlaget, kontrollene med paragraf,
   aksjeeierne, åpne lån som kan motregnes og møtedatoene. Gå gjennom den med
   brukeren. Sperrer den, forklar hvorfor og hva som kan gjøres.
3. **Forsvarlighetsvurderingen.** Still dette spørsmålet for seg, med
   paragrafene fra forhåndsvisningen (aksjeloven §§ 3-4 og 8-1 (4)): «Har
   styret vurdert at egenkapitalen og likviditeten er forsvarlig etter
   utdelingen?» Bare et ja til akkurat det spørsmålet gir
   `board_assessed_prudence=True`. Et «ja, kjør» til noe annet er ikke et ja
   til dette. Anta det aldri.
4. Lag utkastene etter ja:

```
foresla_selskapshandling(action_type="dividend", amount=<kr>,
                         board_date=<YYYY-MM-DD>, general_meeting_date=<YYYY-MM-DD>,
                         board_assessed_prudence=True, dry_run=False, company_id=<id>)
```

   Det lager handlingen, styresaken, generalforsamlingen og eventuelt
   mellombalansen som utkast. Ingenting sendes. Innkalling og signering går
   fra møtene i Roret (se `styremote`).

Valg du kan sette: `simplified` (forenklet generalforsamling),
`on_annual_general_meeting`, `interim_balance` og `interim_balance_date`
(mellombalanse), `offset_loan_id` og `offset_amount` (motregning i lån).
For lån: `borrower_id`, `loan_security` og `loan_terms`.

## Vedtak som allerede er fattet

Har generalforsamlingen vedtatt utbytte med signert protokoll, men ingen
handling ble laget (for eksempel fordi Styring kom etterpå): finn vedtaket
med `hent_vedtak(search="utbytte")` og kjør etter ja
`start_selskapshandling_fra_vedtak(decision_item_id=<id>)`.

## Bilag og betaling

- Bilaget: `lag_bilag_for_selskapshandling(action_id=<id>)` lager det som
  utkast, etter ja. **Bokfør det aldri med `bokfor_bilag`.** Den som
  bokfører, bruker «Bokfør og betal» i selskapshandlingen i Roret. Det
  kontrollerer bilaget mot mottakerne og lager betalingsordren.
- Betalingslisten: `hent_betalingsliste_for_selskapshandling(action_id=<id>)`
  viser hvem som skal ha hva, til hvilken konto og med hvilken melding.
  Utbetalingen godkjennes i nettbanken.

Utbetaling før lovvilkårene er oppfylt (for eksempel før en mellombalanse er
registrert) er sperret av Roret. Forklar sperren, ikke prøv å gå rundt den.

## Regler

Skatt, kildeskatt, aksjonærregisteroppgave og vilkårene i aksjeloven
kapittel 3 og 8: slå opp med `lov_oppslag` og svar med paragraf. Anbefal
regnskapsfører eller revisor ved tvil om grunnlaget.
