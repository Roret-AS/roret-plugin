---
name: avtale-gjennomgang
description: Leser en avtale (kundeavtale, leverandøravtale, abonnementsvilkår, databehandleravtale, leieavtale eller arbeidsavtale) fra dokumentarkivet eller en opplastet fil, og flagger uvanlige eller risikable vilkår opp mot norsk rett med henvisning til lov og paragraf. Bruk denne når brukeren vil ha en avtale gjennomgått før signering, lurer på hva en klausul betyr, eller vil sammenligne vilkår med det loven sier.
---

# Avtalegjennomgang

**Dette er en gjennomgang, ikke juridisk rådgivning.** Si det kort i svaret.
Ved store beløp, lang binding, personopplysninger i stort omfang eller tvil:
anbefal advokat.

## Steg 1: Hent avtalen

- Fra arkivet: `finn_dokumenter(query=<navn eller motpart>)` og så
  `les_dokument(document_id=<id>, include_content=True, extract_text=True)`.
- Fra en post (kunde, salgsmulighet): `hent_dokumenter_for_post(res_model=..., res_id=...)`.
- Lastet opp i samtalen: les fila direkte.

Spør hvilken side brukeren er på (kjøper eller selger, arbeidsgiver eller
arbeidstaker) og om motparten er forbruker eller næringsdrivende. Det avgjør
hvilke regler som er ufravikelige.

## Steg 2: Finn regelverket

| Avtaletype | Lover å slå opp |
|---|---|
| Alle | avtaleloven (særlig § 36 om urimelige vilkår) |
| Salg av varer mellom næringsdrivende | kjøpsloven |
| Salg av varer til forbruker | forbrukerkjøpsloven (ufravikelig), angrerettloven ved fjernsalg |
| Tjenester til forbruker | håndverkertjenesteloven der den passer, angrerettloven |
| Markedsføring, bindingstid, automatisk fornyelse | markedsføringsloven |
| Databehandling | personopplysningsloven og personvernforordningen art. 28 |
| Arbeidsavtale | arbeidsmiljøloven (blant annet § 14-6 om innholdet) |
| Husleie | husleieloven |

Slå opp hver regel du bruker:

```
lov_oppslag(sporsmal="krav til innhold i skriftlig arbeidsavtale", antall=5)
```

Oppgi lov og paragraf for hvert funn. Svarer `lov_oppslag` at oppslaget ikke
er satt opp, si at funnene ikke er kontrollert mot lovteksten
(`roret-prinsipper` §8).

## Steg 3: Gå gjennom vilkårene

Se særlig etter:

- **Pris og betaling:** prisjustering, forfall, forsinkelsesrente, gebyrer
- **Varighet:** bindingstid, oppsigelse, automatisk fornyelse
- **Ansvar:** ansvarsbegrensning, erstatning, dagbøter, force majeure
- **Mangler:** reklamasjonsfrister, utbedring, heving
- **Immaterielle rettigheter og konfidensialitet**
- **Personopplysninger:** databehandleravtale, overføring utenfor EØS,
  underleverandører
- **Tvist:** lovvalg, verneting, voldgift
- **Ensidige endringsrett** for motparten

## Steg 4: Rapport

```
## Avtale med <motpart> — gjennomgang <dato>
Type: leverandøravtale, vi er kjøper, motparten er næringsdrivende.

| # | Klausul | Hva den sier | Vurdering | Hjemmel |
|---|---|---|---|---|
| 1 | 9.2 Ansvar | Ansvar begrenset til 1 måneds vederlag | Lavt tak for en kritisk leveranse | avtaleloven § 36 |

**Bør forhandles:** …
**Greit som det er:** …
**Mangler i avtalen:** …
```

Forslag til ny tekst for en klausul kan skrives på brukerens oppfordring.
Merk dem som forslag.

## Etterpå

Tilby å legge rapporten som internt notat på kunden eller salgsmuligheten
(`skriv_i_chatter(model=..., res_id=..., body=...)`) eller avtalen i arkivet
med `flytt_dokument` hvis den ikke ligger der. Begge deler etter ja.
