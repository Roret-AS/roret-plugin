---
name: maal-og-strategi
description: Viser selskapets strategi, budsjett og mål fra Roret Styring, hjelper en ansatt eller leder å prioritere mot egne mål, og rapporterer manuelle målinger etter godkjenning. Bruk denne når brukeren spør om strategien, hvordan det går mot budsjett eller mål, hva hen bør prioritere, hvilke mål teamet har, eller vil rapportere fremdrift på et mål. Bruk den også før du foreslår noe som koster tid eller penger, så forslaget følger selskapets valg.
---

# Mål og strategi

Strategien i Roret er data, ikke et dokument: situasjonsbilde, valg, hva
selskapet ikke gjør, antakelser, mål og budsjett. Den er også retningen
agenten skal følge. Krever Styring. Svarer verktøyene at det mangler, si det
kort og fortsett uten.

Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Strategien og budsjettet

```
strategi_oversikt(company_id=<id>)
```

Svaret har:
- **strategi:** situasjonsbilde, valg, hva vi ikke gjør, og antakelsene med
  signal og status. `None` betyr at ingen strategi er vedtatt.
- **budsjett:** årets budsjett mot regnskapet hittil. `{"tilgang": false}`
  betyr at brukeren ikke kan se tallene. Si det, ikke gjett.
- **selskapsmaal:** ambisjon, faktisk, prognose og status (`pa_vei`,
  `i_fare`, `bak`, `naadd`, `mangler`, `ikke_startet`). `faktisk` lik `None`
  betyr at målet ikke er målt, ikke at det er 0.

Vis kort: valgene, mål som er i fare eller bak, antakelser med svakt
signal, og største budsjettavvik. Antakelser som brytes, er det tidligste
varselet om at kursen bør endres. Løft dem.

## Egne mål og prioriteringer

```
mine_maal()                          # brukeren selv
mine_maal(employee_id=<id>)          # en ansatt brukeren leder
```

Hjelp brukeren å prioritere: hvilke mål som ligger bak, hva som flytter dem,
og hva som kan vente. Knytt forslag til selskapets valg i strategien. En
ansatt ser bare sine egne mål, en leder også sine ansattes.

## Rapportere en måling

Bare for mål som rapporteres for hånd (målekilde «manuell» eller
«milepæl»), og bare av den som er ansvarlig. Mål med KPI fra Roret
oppdateres selv hver natt.

1. Bekreft verdi, dato og en kort kommentar med brukeren.
2. Etter ja:

```
registrer_maaling(goal_id=<id>, value=<verdi>, comment=<hva som flyttet tallet>, dato=<YYYY-MM-DD>)
```

## Når du foreslår noe annet

Før du anbefaler et tiltak som koster tid eller penger i en annen skill (for
eksempel en ny kampanje eller et innkjøp), sjekk om det passer med valgene
og «hva vi ikke gjør» i strategien. Går det på tvers, si det.
