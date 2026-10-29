---
name: pipeline
description: Går gjennom åpne salgsmuligheter i Odoo CRM, finner dem som har stått stille eller mangler neste steg, og foreslår konkrete oppfølginger som planlegges etter godkjenning. Bruk denne når brukeren vil rydde i pipelinen, spør «hvilke deals har stoppet opp», vil ha en salgsgjennomgang for uka, eller lurer på hva selgerne bør prioritere.
---

# Pipeline-gjennomgang

Selskap: `firmaprofil`. Skriveregler: `roret-prinsipper`.

## Steg 1: Hent åpne salgsmuligheter

```
hent_salgsmuligheter(company_id=<id>, only_open=True, limit=50)
```

Avgrens hvis brukeren ba om det: egne (`user_id`), ett salgsteam
(`team_id`), eller over et beløp (`min_expected_revenue`). Verktøyet sorterer
dem som trenger oppmerksomhet først.

## Steg 2: Finn det som har stoppet opp

For hver salgsmulighet:

```
hent_aktiviteter(model="crm.lead", res_id=<id>)
```

Flagg:

| Signal | Hvorfor |
|---|---|
| Ingen planlagt aktivitet | Ingen eier neste steg |
| Aktivitet over frist | Noe er glemt |
| Ingen kontakt på 14 dager eller mer | Saken kjølner |
| Forventet lukking passert | Datoen eller sannsynligheten er feil |
| Høy sannsynlighet, men lite skjer | Prognosen kan være for optimistisk |

For de 5–10 viktigste (etter beløp og alvor), les siste historikk:
`les_chatter(model="crm.lead", res_id=<id>, limit=5, include_notifications=False)`.

## Steg 3: Vis gjennomgangen

```
## Pipeline — 28. oktober (14 åpne, 2,3 mill. kr forventet)

| Salgsmulighet | Kunde | Beløp | Steg | Sist kontakt | Problem | Forslag |
|---|---|---|---|---|---|---|
| Ny avtale 2027 | Eksempel AS | 240 000 kr | Tilbud | 19 dager | Ingen aktivitet | Ring, avklar beslutningsdato |
```

Avslutt med et kort avsnitt: hva som haster mest, og om prognosen ser
realistisk ut. Dette er ledelsestall (`roret-prinsipper` §7).

## Steg 4: Gjør forslagene om til handling

Spør hvilke forslag som skal gjennomføres. For hvert ja:

- Ny aktivitet: `hent_aktivitetstyper()`, så
  `planlegg_aktivitet(model="crm.lead", res_id=<id>, activity_type_id=..., summary=..., date_deadline=..., user_id=<selger>)`.
- Justere salgsmuligheten:
  `oppdater_salgsmulighet(lead_id=<id>, probability=..., expected_closing=..., stage_id=...)`.
- Grundigere oppfølging av én sak: bruk `folg-opp`.

Endre aldri sannsynlighet, beløp eller steg uten at brukeren har sagt ja til
akkurat den endringen.
