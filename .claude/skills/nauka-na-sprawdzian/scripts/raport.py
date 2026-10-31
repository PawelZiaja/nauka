#!/usr/bin/env python3
"""Raport korzystania z aplikacji ze zdarzeń GoatCounter: dla każdego urządzenia testy i powtórki
po kolei (numer podejścia, godzina, ocena, wynik) z listą błędów, a pod spodem fiszki.

Klucz API w zmiennej GOATCOUNTER_TOKEN (nigdy nie wpisuj go do repozytorium).
Użycie: python3 raport.py [od RRRR-MM-DD] [do RRRR-MM-DD] [--nazwy kod=imię,kod=imię]
Bez dat – dzisiaj. Imiona podawaj tylko w poleceniu (repozytorium jest publiczne)."""
import json, os, re, sys, urllib.request, urllib.parse, datetime
from collections import defaultdict

SITE = 'https://ziaja.goatcounter.com/api/v0'

def pobierz(od, do):
    hits, wyklucz = [], []
    while True:
        q = {'start': od, 'end': do, 'limit': 200, 'daily': 'true'}
        if wyklucz: q['exclude_paths'] = ','.join(map(str, wyklucz))
        req = urllib.request.Request(SITE + '/stats/hits?' + urllib.parse.urlencode(q),
                                     headers={'Authorization': 'Bearer ' + os.environ['GOATCOUNTER_TOKEN']})
        d = json.load(urllib.request.urlopen(req, timeout=30))
        hits += d['hits']; wyklucz += [h['path_id'] for h in d['hits']]
        if not d.get('more') or not d['hits']: return hits

def kiedy(h):
    """Pierwszy dzień i godzina z ruchem (GoatCounter podaje rozkład godzinowy w strefie strony)."""
    for s in h.get('stats', []):
        if s.get('daily'):
            g = next((i for i, v in enumerate(s.get('hourly', [])) if v), None)
            return s['day'], g
    return '', None

def main():
    argv, nazwy = sys.argv[1:], {}
    if '--nazwy' in argv:
        i = argv.index('--nazwy'); lista = argv[i + 1] if i + 1 < len(argv) else ''
        nazwy = dict(x.split('=', 1) for x in lista.split(',') if '=' in x); argv = argv[:i] + argv[i + 2:]
    a = [x for x in argv if not x.startswith('--')]
    dzis = datetime.date.today()
    od = a[0] if a else dzis.isoformat()
    do = a[1] if len(a) > 1 else (datetime.date.fromisoformat(od) + datetime.timedelta(days=1)).isoformat()
    # urz -> aplikacja -> {'proby': {(rodzaj,nr): {...}}, 'stare': [...], 'fiszki': set(), 'otwarta': n}
    U = defaultdict(lambda: defaultdict(lambda: {'proby': defaultdict(lambda: {'bledy': []}), 'stare': [], 'fiszki': set(), 'otwarta': 0}))
    for h in pobierz(od, do):
        if not h.get('event'): continue
        cz = h['path'].split(' – ')
        i = next((k for k, c in enumerate(cz) if c.startswith('urz. ')), None)
        if i is None or i < 2: continue
        urz, app, nazwa, dod = cz[i][5:], cz[i - 1], ' – '.join(cz[:i - 1]), cz[i + 1:]
        dzien, godz = kiedy(h)
        A = U[urz][app]
        m = re.match(r'(?:błąd – )?(test|powtórka) #(\d+)(.*)', nazwa)
        if m:
            P = A['proby'][(m.group(1), int(m.group(2)))]
            if nazwa.startswith('błąd'):
                P['bledy'].append(h.get('title', '') or (dod[0] if dod else ''))
            elif 'rozpoczę' in m.group(3):
                P['start'] = (dzien, godz)
            else:
                P['koniec'] = m.group(3).strip(' ,'); P['kiedy'] = (dzien, godz)
        elif nazwa.startswith('test ukończony'):
            A['stare'].append((dzien, godz if godz is not None else -1, nazwa))
        elif nazwa.startswith('fiszk'):
            A['fiszki'].add(nazwa)
        elif nazwa == 'aplikacja otwarta':
            A['otwarta'] += h['count']
    if not U: print(f'Brak zdarzeń {od} – {do}.'); return
    for urz in sorted(U, key=lambda u: (u not in nazwy, nazwy.get(u, u))):
        print(f'\n=== {nazwy.get(urz, "?")} (urz. {urz}) ===')
        for app, A in sorted(U[urz].items()):
            print(f'  [{app}] otwarcia: {A["otwarta"]}')
            for (rodzaj, nr), P in sorted(A['proby'].items(), key=lambda x: (x[0][0] != 'test', x[0][1])):
                d, g = P.get('kiedy') or P.get('start') or ('', None)
                czas = f'{d} ok. {g}:00' if g is not None else d
                print(f'    {rodzaj} #{nr} ({czas}): {P.get("koniec", "nieukończony")}')
                for b in P['bledy']: print(f'       ✗ {b}')
            for d, g, n in sorted(A['stare']):
                print(f'    {d}{f" ok. {g}:00" if g >= 0 else ""}: {n} (stara wersja – bez numeru i błędów; ta sama ocena kilka razy = jeden wpis)')
            if A['fiszki']: print('    fiszki: ' + '; '.join(sorted(A['fiszki'])))

if __name__ == '__main__':
    main()
