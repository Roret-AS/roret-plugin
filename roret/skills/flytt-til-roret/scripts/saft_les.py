"""Les en SAF-T Financial-fil (1.10/1.20/1.30/1.40) og lag et migreringsgrunnlag.

Brukes av skillen flytt-til-roret. Kjøres lokalt, FØR noe skrives i Roret,
og skriver ingenting andre steder enn til JSON-fila du ber om:

    python3 -I saft_les.py <fil.xml> [--json ut.json]

Skriver ut kontroller (balanse, totaler, reskontro mot hovedbok) og bygger:
  * kontoer med inngående/utgående saldo og grupperingskode
  * kunder/leverandører med saldo, også per reskontrokonto
  * MVA-koder (lokal kode -> standardkode)
  * månedssummer per konto og regnskapsperiode (til resultatet hittil i år
    ved bytte midt i året)
  * åpne poster per partner, utledet fra transaksjonene. Det er en
    heuristikk: poster på reskontrolinjer grupperes på ReferenceNumber/CID,
    og summen per gruppe != 0 er en åpen post. Det som var åpent ved
    periodestart, ligger bare som inngående saldo per partner, så åpne
    poster skal hentes fra reskontroen i det gamle systemet. Dette er bare
    en kontroll.

Fila behandles som utrodd data: lxml uten nettverk, uten å løse opp
entiteter og med libxml2s vanlige grenser. Kontrolltegn fjernes fra tekst
før den skrives ut eller lagres.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from decimal import Decimal

from lxml import etree

NS = {'n': 'urn:StandardAuditFile-Taxation-Financial:NO'}
NULL = Decimal('0')
KONTROLLTEGN = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def _t(el, path):
    v = el.findtext(path, namespaces=NS)
    return KONTROLLTEGN.sub('', v).strip() if v else None


def _d(el, path):
    v = _t(el, path)
    return Decimal(v) if v else NULL


def _saldo(el, prefix):
    """Debet positiv."""
    return _d(el, 'n:%sDebitBalance' % prefix) - _d(el, 'n:%sCreditBalance' % prefix)


def _debet_kredit(line):
    """(debet, kredit) etter elementet, ikke etter fortegnet."""
    deb = line.find('n:DebitAmount', NS)
    kre = line.find('n:CreditAmount', NS)
    return (_d(deb, 'n:Amount') if deb is not None else NULL,
            _d(kre, 'n:Amount') if kre is not None else NULL)


def _parti(el, id_tag):
    """Kunde/leverandør. 1.30+: BalanceAccount per konto; 1.10/1.20: rett på elementet."""
    bal = el.findall('n:BalanceAccount', NS)
    if bal:
        per_konto = defaultdict(lambda: [NULL, NULL])
        for b in bal:
            konto = _t(b, 'n:AccountID')
            per_konto[konto][0] += _saldo(b, 'Opening')
            per_konto[konto][1] += _saldo(b, 'Closing')
    else:
        per_konto = {_t(el, 'n:AccountID'): [_saldo(el, 'Opening'), _saldo(el, 'Closing')]}
    adr = el.find('n:Address', NS)
    bank = [(_t(b, 'n:IBANNumber') or _t(b, 'n:BankAccountNumber'))
            for b in el.findall('n:BankAccount', NS)]
    return {
        'id': _t(el, 'n:%s' % id_tag),
        'navn': _t(el, 'n:Name'),
        'orgnr': _t(el, 'n:RegistrationNumber'),
        'mva_nr': _t(el, 'n:TaxRegistration/n:TaxRegistrationNumber'),
        'gate': adr is not None and ' '.join(filter(None, [
            _t(adr, 'n:StreetName'), _t(adr, 'n:Number')])) or None,
        'postnr': adr is not None and _t(adr, 'n:PostalCode') or None,
        'sted': adr is not None and _t(adr, 'n:City') or None,
        'land': adr is not None and _t(adr, 'n:Country') or None,
        'epost': _t(el, 'n:Contact/n:Email'),
        'telefon': _t(el, 'n:Contact/n:Telephone') or _t(el, 'n:Contact/n:MobilePhone'),
        'bankkonto': [b for b in bank if b],
        'betalingsfrist_dager': _t(el, 'n:PartyInfo/n:PaymentTerms/n:Days'),
        'reskontrokonto': [k for k in per_konto if k],
        'saldo_per_konto': {k: {'inngaende': v[0], 'utgaende': v[1]}
                            for k, v in per_konto.items() if k},
        'inngaende': sum((v[0] for v in per_konto.values()), NULL),
        'utgaende': sum((v[1] for v in per_konto.values()), NULL),
    }


def _periode(tr):
    """Regnskapsperioden bilaget er ført i (ÅÅÅÅ-PP), ikke bilagsdatoen.

    En leverandørfaktura datert 28.12. kan være ført i periode 1 året etter.
    Faller tilbake på GLPostingDate og så TransactionDate."""
    aar, per = _t(tr, 'n:PeriodYear'), _t(tr, 'n:Period')
    if aar and per and per.isdigit():
        return '%s-%02d' % (aar, int(per))
    dato = _t(tr, 'n:GLPostingDate') or _t(tr, 'n:TransactionDate') or ''
    return dato[:7]


def les(sti):
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    rot = etree.parse(sti, parser).getroot()
    h = rot.find('n:Header', NS)
    if h is None:
        raise SystemExit('Fant ikke Header i navnerommet %s. Er dette en SAF-T Financial-fil?'
                         % NS['n'])
    res = {
        'versjon': _t(h, 'n:AuditFileVersion'),
        'orgnr': _t(h, 'n:Company/n:RegistrationNumber'),
        'selskap': _t(h, 'n:Company/n:Name'),
        'valuta': _t(h, 'n:DefaultCurrencyCode'),
        'fra': _t(h, 'n:SelectionCriteria/n:SelectionStartDate')
        or '%s-%s' % (_t(h, 'n:SelectionCriteria/n:PeriodStartYear'),
                      _t(h, 'n:SelectionCriteria/n:PeriodStart')),
        'til': _t(h, 'n:SelectionCriteria/n:SelectionEndDate')
        or '%s-%s' % (_t(h, 'n:SelectionCriteria/n:PeriodEndYear'),
                      _t(h, 'n:SelectionCriteria/n:PeriodEnd')),
        'programvare': '%s %s' % (_t(h, 'n:SoftwareID'), _t(h, 'n:SoftwareVersion')),
    }
    mf = rot.find('n:MasterFiles', NS)
    kontoer = []
    for a in mf.findall('n:GeneralLedgerAccounts/n:Account', NS) if mf is not None else []:
        kontoer.append({
            'konto': _t(a, 'n:AccountID'), 'navn': _t(a, 'n:AccountDescription'),
            'standardkonto': _t(a, 'n:StandardAccountID'),           # 1.10/1.20
            'gruppekategori': _t(a, 'n:GroupingCategory'),
            'gruppekode': _t(a, 'n:GroupingCode'),
            'inngaende': _saldo(a, 'Opening'), 'utgaende': _saldo(a, 'Closing'),
        })
    kunder = [_parti(c, 'CustomerID') for c in mf.findall('n:Customers/n:Customer', NS)] if mf is not None else []
    lev = [_parti(s, 'SupplierID') for s in mf.findall('n:Suppliers/n:Supplier', NS)] if mf is not None else []
    reskontro = {('K', p['id']): set(p['reskontrokonto']) for p in kunder}
    reskontro.update({('L', p['id']): set(p['reskontrokonto']) for p in lev})
    # Når kontoen til en partner er ukjent (partneren står ikke i registeret,
    # eller AccountID mangler i 1.10/1.20), brukes kontoene de andre partnerne
    # av samme slag har, og ellers standardkontoplanens 15xx og 24xx.
    felles = {typ: set().union(*(v for (t, _), v in reskontro.items() if t == typ))
              for typ in ('K', 'L')}

    def _er_reskontro(typ, pid, konto):
        kjente = reskontro.get((typ, pid)) or felles[typ]
        if kjente:
            return konto in kjente
        return (konto or '').startswith('15' if typ == 'K' else '24')
    mva = []
    for d in mf.findall('n:TaxTable/n:TaxTableEntry/n:TaxCodeDetails', NS) if mf is not None else []:
        mva.append({'kode': _t(d, 'n:TaxCode'), 'standardkode': _t(d, 'n:StandardTaxCode'),
                    'sats': _t(d, 'n:TaxPercentage'), 'navn': _t(d, 'n:Description'),
                    'grunnlag_pst': [_t(x, '.') for x in d.findall('n:BaseRate', NS)]})
    dims = [{'type': _t(e, 'n:AnalysisType'), 'id': _t(e, 'n:AnalysisID'),
             'navn': _t(e, 'n:AnalysisIDDescription')}
            for e in (mf.findall('n:AnalysisTypeTable/n:AnalysisTypeTableEntry', NS) if mf is not None else [])]

    # Hovedboken
    gle = rot.find('n:GeneralLedgerEntries', NS)
    bevegelse = defaultdict(lambda: NULL)
    per_mnd = defaultdict(lambda: NULL)            # (konto, ÅÅÅÅ-PP) -> beløp
    parti_bev = defaultdict(lambda: NULL)          # ('K'|'L', id) -> beløp på reskontrokontoene
    poster = defaultdict(lambda: {'sum': NULL, 'linjer': 0, 'forfall': None, 'dato': None})
    feil = []
    sum_deb = sum_kre = NULL
    antall = 0
    for tr in (gle.findall('n:Journal/n:Transaction', NS) if gle is not None else []):
        antall += 1
        dato = _t(tr, 'n:TransactionDate')
        periode = _periode(tr)
        linjer = tr.findall('n:Line', NS)
        s = NULL
        for ln in linjer:
            deb, kre = _debet_kredit(ln)
            sum_deb += deb
            sum_kre += kre
            b = deb - kre
            s += b
            konto = _t(ln, 'n:AccountID')
            bevegelse[konto] += b
            per_mnd[(konto, periode)] += b
            for typ, tag in (('K', 'n:CustomerID'), ('L', 'n:SupplierID')):
                pid = _t(ln, tag) or (_t(tr, tag) if len(linjer) == 1 else None)
                if not pid:
                    continue
                if not _er_reskontro(typ, pid, konto):
                    # Partner-id på en inntekts- eller kostnadslinje: ikke reskontro.
                    continue
                parti_bev[(typ, pid)] += b
                ref = _t(ln, 'n:CID') or _t(ln, 'n:ReferenceNumber') or 'TX:' + (_t(tr, 'n:TransactionID') or '?')
                p = poster[(typ, pid, ref)]
                p['sum'] += b
                p['linjer'] += 1
                p['forfall'] = p['forfall'] or _t(ln, 'n:DueDate')
                p['dato'] = p['dato'] or dato
        if s != 0:
            feil.append('Bilag %s går ikke i null (%s)' % (_t(tr, 'n:TransactionID'), s))
    if gle is not None:
        if _d(gle, 'n:TotalDebit') != sum_deb or _d(gle, 'n:TotalCredit') != sum_kre:
            feil.append('TotalDebit/TotalCredit stemmer ikke med linjene (%s/%s mot %s/%s)'
                        % (_d(gle, 'n:TotalDebit'), _d(gle, 'n:TotalCredit'), sum_deb, sum_kre))
        if int(_t(gle, 'n:NumberOfEntries') or 0) != antall:
            feil.append('NumberOfEntries %s, men %s bilag' % (_t(gle, 'n:NumberOfEntries'), antall))

    # Kontroller
    if not kontoer:
        feil.append('Fila har ingen kontoer (MasterFiles/GeneralLedgerAccounts)')
    if not antall:
        feil.append('Fila har ingen bilag (GeneralLedgerEntries). Er perioden riktig?')
    for k in kontoer:
        diff = k['inngaende'] + bevegelse.get(k['konto'], NULL) - k['utgaende']
        if diff:
            feil.append('Konto %s: inngående + bevegelse - utgående = %s' % (k['konto'], diff))
    if sum((k['utgaende'] for k in kontoer), NULL):
        feil.append('Sum utgående saldo over alle kontoer er %s, ikke 0'
                    % sum((k['utgaende'] for k in kontoer), NULL))
    for typ, liste in (('K', kunder), ('L', lev)):
        for p in liste:
            diff = p['inngaende'] + parti_bev.get((typ, p['id']), NULL) - p['utgaende']
            if diff:
                feil.append('%s %s %s: inngående + bevegelse - utgående = %s'
                            % ('Kunde' if typ == 'K' else 'Leverandør', p['id'], p['navn'], diff))
    resk = defaultdict(lambda: NULL)
    for liste in (kunder, lev):
        for p in liste:
            for konto, saldo in p['saldo_per_konto'].items():
                resk[konto] += saldo['utgaende']
    for konto, sum_resk in resk.items():
        gl = next((k['utgaende'] for k in kontoer if k['konto'] == konto), None)
        if gl is not None and gl != sum_resk:
            feil.append('Reskontro mot hovedbok, konto %s: %s mot %s' % (konto, sum_resk, gl))

    aapne = [{'type': t, 'parti': pid, 'ref': ref, **v}
             for (t, pid, ref), v in poster.items() if v['sum'] != 0]
    # Åpne poster fra transaksjonene dekker bare perioden i fila. Det som var
    # åpent ved periodestart, ligger bare i inngående saldo per partner.
    dekning = {}
    for typ, liste in (('K', kunder), ('L', lev)):
        for p in liste:
            fra_tx = sum((a['sum'] for a in aapne if a['type'] == typ and a['parti'] == p['id']), NULL)
            dekning[(typ, p['id'])] = {'utgaende': p['utgaende'], 'aapne_fra_tx': fra_tx,
                                       'uforklart': p['utgaende'] - fra_tx}
    res.update(kontoer=kontoer, kunder=kunder, leverandorer=lev, mva=mva, dimensjoner=dims,
               antall_bilag=antall, sum_debet=sum_deb, sum_kredit=sum_kre,
               maanedsbevegelse={'%s|%s' % k: v for k, v in per_mnd.items()},
               aapne_poster=aapne, dekning={'%s|%s' % k: v for k, v in dekning.items()},
               feil=feil)
    return res


def main():
    ap = argparse.ArgumentParser(description='Kontroller en SAF-T Financial-fil før flytting til Roret.')
    ap.add_argument('fil', help='SAF-T-fila (XML, pakket ut av ZIP)')
    ap.add_argument('--json', metavar='UT', help='skriv migreringsgrunnlaget til denne fila')
    args = ap.parse_args()
    res = les(args.fil)
    print('SAF-T %s for %s (%s), %s–%s, %s' % (res['versjon'], res['selskap'], res['orgnr'],
                                              res['fra'], res['til'], res['programvare']))
    print('Kontoer: %d, kunder: %d, leverandører: %d, MVA-koder: %d, dimensjoner: %d, bilag: %d'
          % (len(res['kontoer']), len(res['kunder']), len(res['leverandorer']), len(res['mva']),
             len(res['dimensjoner']), res['antall_bilag']))
    print('Åpne poster utledet fra transaksjonene (bare kontroll): %d' % len(res['aapne_poster']))
    for k, v in res['dekning'].items():
        if v['uforklart']:
            print('  %s: saldo %s, forklart av poster i perioden %s, uforklart %s'
                  % (k, v['utgaende'], v['aapne_fra_tx'], v['uforklart']))
    print('Kontroller: %s' % ('alle grønne' if not res['feil'] else '%d avvik' % len(res['feil'])))
    for f in res['feil']:
        print('  - ' + f)
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
