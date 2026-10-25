#!/usr/bin/env python3
"""Sprawdza plik z treścią (JSON) i składa z niego gotową aplikację HTML.

Użycie:
    python3 buduj.py dane.json /mnt/user-data/outputs/nazwa.html

Błędy (❌) przerywają budowanie. Ostrzeżenia (⚠️) trzeba przejrzeć, ale nie blokują.
"""
import json, sys, re, base64, io
from collections import Counter
from pathlib import Path

TYPY = {'mc','tf','in','num','gap','pick','match','multi','order','spot'}
TRYBY = {'scisle','luzno','koncowka'}

def do_data_uri(v, baza=Path('.'), maks=1100):
    """Ścieżka do pliku (jpg/png/webp/gif/svg) albo gotowe data: URI -> zmniejszony data URI."""
    if str(v).startswith('data:'): return v
    path = Path(v)
    if not path.is_absolute(): path = baza / path
    if not path.exists(): raise ValueError(f'brak pliku {v}')
    if path.suffix.lower() == '.svg':
        return 'data:image/svg+xml;base64,' + base64.b64encode(path.read_bytes()).decode()
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path))
    im.thumbnail((maks, maks))
    buf = io.BytesIO()
    if im.mode in ('RGBA','LA','P') and 'transparency' in im.info or im.mode in ('RGBA','LA'):
        im.save(buf, 'PNG', optimize=True); mime = 'png'
    else:
        im.convert('RGB').save(buf, 'JPEG', quality=74, optimize=True, progressive=True); mime = 'jpeg'
    return f'data:image/{mime};base64,' + base64.b64encode(buf.getvalue()).decode()

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    d = json.loads(src.read_text(encoding='utf-8'))
    err, warn = [], []
    cfg = d.get('config', {})
    for k in ('tytul','klucz','przedmiot','klasa'):
        if k not in cfg: err.append(f'config: brak pola „{k}”')
    if not re.fullmatch(r'[a-z0-9-]+', str(cfg.get('klucz',''))): err.append('config.klucz: tylko małe litery, cyfry i myślniki')
    if cfg.get('tryb') and cfg['tryb'] not in TRYBY: err.append('config.tryb: scisle | luzno | koncowka')
    tagi = cfg.get('tagi', {})

    for i, c in enumerate(d.get('fiszki', [])):
        for k in ('p','o'):
            if not c.get(k): err.append(f'fiszka {i}: brak „{k}”')
        if tagi and c.get('tag') not in tagi: warn.append(f'fiszka {i}: tag „{c.get("tag")}” nie ma etykiety w config.tagi')

    seen = set()
    for i, q in enumerate(d.get('pytania', [])):
        t = q.get('t'); w = f'pytanie {i} ({t}): '
        if t not in TYPY: err.append(w+'nieznany typ'); continue
        if not q.get('ex'): err.append(w+'brak wyjaśnienia „ex”')
        if not q.get('c'): warn.append(w+'brak kategorii „c”')
        if q.get('tryb') and q['tryb'] not in TRYBY: err.append(w+'zły tryb')
        key = (t, q.get('q'), q.get('s'), json.dumps(q.get('o') or q.get('p') or q.get('pola'), ensure_ascii=False))
        if key in seen: err.append(w+'duplikat pytania')
        seen.add(key)
        if t in ('mc','gap'):
            o = q.get('o') or []
            if len(o) < 2: err.append(w+'za mało opcji')
            if len(set(o)) != len(o): err.append(w+'powtórzone opcje')
            if not isinstance(q.get('a'), int) or not 0 <= q['a'] < len(o): err.append(w+'zły indeks „a”')
            if t == 'gap' and not re.search(r'\[\[.+?\]\]', q.get('q','')): err.append(w+'brak znacznika [[…]] w zdaniu')
        elif t == 'tf':
            if not isinstance(q.get('a'), bool): err.append(w+'„a” musi być true/false')
        elif t == 'in':
            if not q.get('a') or not all(isinstance(x,str) and x.strip() for x in q['a']): err.append(w+'„a” = lista poprawnych odpowiedzi')
        elif t == 'num':
            a = q.get('a'); a = a if isinstance(a, list) else [a]
            if not a or not all(isinstance(x,(int,float)) for x in a): err.append(w+'„a” musi być liczbą lub listą liczb')
        elif t == 'pick':
            toks = q.get('s','').split(' '); a = q.get('a') or []
            if not a or any(not isinstance(k,int) or k<0 or k>=len(toks) for k in a): err.append(w+'indeksy poza zdaniem')
            if len(set(a)) != len(a): err.append(w+'powtórzone indeksy')
        elif t == 'match':
            p = q.get('p') or []
            if len(p) < 2: err.append(w+'za mało par')
            if len({x[0] for x in p}) != len(p): err.append(w+'powtórzone lewe strony')
        elif t == 'multi':
            pola = q.get('pola') or []
            if not pola: err.append(w+'brak pól')
            for f in pola:
                if not f.get('l') or f.get('a') in (None, [], ''): err.append(w+'pole bez etykiety „l” lub odpowiedzi „a”')
        elif t == 'spot':
            c = q.get('cel') or {}
            if not q.get('img'): err.append(w+'spot wymaga obrazka „img”')
            if not all(isinstance(c.get(k),(int,float)) for k in ('x','y','r')) or not (0<=c.get('x',-1)<=100 and 0<=c.get('y',-1)<=100 and 0<c.get('r',0)<=50):
                err.append(w+'„cel” musi mieć x, y (0–100 %) i r (promień w % szerokości)')
        elif t == 'order':
            o = q.get('o') or []
            if len(o) < 3: err.append(w+'kolejność wymaga min. 3 elementów')
            if len(set(o)) != len(o): err.append(w+'powtórzone elementy')
        tekst = json.dumps({k:v for k,v in q.items() if k not in ('a','pola')}, ensure_ascii=False)
        if re.search(r'(?<![\\\w])\\"[^\\"]{1,40}\\"', tekst): warn.append(w+'proste cudzysłowy "…" – w tekście po polsku używaj „…”')

    # ---- obrazy ----
    obrazy = d.get('obrazy', {})
    uzyte = {x.get(k) for x in d.get('pytania', [])+d.get('fiszki', []) for k in ('img','imgO') if x.get(k)}
    for k in sorted(uzyte):
        if k not in obrazy and not str(k).startswith('data:'): err.append(f'obraz „{k}” nie jest zdefiniowany w „obrazy”')
    for k in obrazy:
        if k not in uzyte: warn.append(f'obraz „{k}” nie jest nigdzie użyty')
    for x in d.get('pytania', [])+d.get('fiszki', []):
        if (x.get('img') or x.get('imgO')) and not x.get('alt'): warn.append(f'brak opisu „alt” przy obrazku „{x.get("img") or x.get("imgO")}”')
    if not err:
        for k, v in list(obrazy.items()):
            try: obrazy[k] = do_data_uri(v, src.parent)
            except Exception as e: err.append(f'obraz „{k}”: {e}')
        total = sum(len(v) for v in obrazy.values())
        if obrazy: print(f'Obrazy: {len(obrazy)}, razem {total//1024} KB')
        if total > 12_000_000: err.append('obrazy zajmują ponad 12 MB – zmniejsz je lub usuń część (limit strony to 16 MB)')
        elif total > 6_000_000: warn.append('obrazy zajmują ponad 6 MB – strona będzie wolno się ładować na telefonie')

    pyt = d.get('pytania', [])
    print(f'Fiszki: {len(d.get("fiszki", []))}   Pytania: {len(pyt)}')
    print('Typy:', dict(Counter(q.get('t') for q in pyt)))
    print('Kategorie:', dict(Counter(q.get('c') for q in pyt)))
    for x in warn[:40]: print('⚠️ ', x)
    if len(warn) > 40: print(f'⚠️  … i {len(warn)-40} więcej')
    for x in err: print('❌', x)
    if err: print(f'\nBudowanie przerwane: {len(err)} błędów.'); sys.exit(2)

    tpl = (Path(__file__).resolve().parent.parent / 'assets' / 'szablon.html').read_text(encoding='utf-8')
    js = json.dumps(d, ensure_ascii=False, separators=(',',':')).replace('</', '<\\/')
    html = tpl.replace('/*__DANE__*/null', js).replace('<title>Nauka na sprawdzian</title>', f'<title>{cfg["tytul"]}</title>')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'\n✅ Zbudowano: {out} ({len(html)//1024} KB)')

if __name__ == '__main__':
    main()
