#!/usr/bin/env python3
"""Tworzy stronę startową index.html ze spisem wszystkich aplikacji w katalogu i jego podfolderach,
pogrupowanych według klasy i przedmiotu (dane brane z config każdej aplikacji).
Struktura na stronie: klasa-5/polski/temat.html, klasa-7/historia/temat.html itd.
Użycie: python3 spis.py katalog_glowny [tytuł strony]"""
import sys, re, html, json
from pathlib import Path
kat = Path(sys.argv[1]); tytul = sys.argv[2] if len(sys.argv) > 2 else 'Nauka na sprawdziany'
apps = {}
for f in sorted(kat.rglob('*.html')):
    czesci = f.relative_to(kat).parts
    if f.name == 'index.html' or any(p.startswith('.') or p in ('robocze', 'node_modules') for p in czesci): continue
    t = f.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<title>(.*?)</title>', t)
    p = re.search(r'"przedmiot":"(.*?)"', t); k = re.search(r'"klasa":"?(\d+)', t)
    klasa = k.group(1) if k else '?'; przedm = p.group(1) if p else 'Inne'
    apps.setdefault(klasa, {}).setdefault(przedm, []).append((m.group(1) if m else f.stem, f.relative_to(kat).as_posix()))
sekcje = []
for klasa in sorted(apps, key=lambda x: int(x) if x.isdigit() else 99):
    przedm = ''.join(f'<h3>{html.escape(p)}</h3>' + ''.join(f'<a class="it" href="{html.escape(h)}">{html.escape(t)}</a>' for t, h in sorted(lst)) for p, lst in sorted(apps[klasa].items()))
    sekcje.append(f'<details open><summary>Klasa {klasa}</summary>{przedm}</details>')
n = sum(len(l) for d in apps.values() for l in d.values())
page = f'''<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{html.escape(tytul)}</title>
<style>:root{{--bg:#fbfbf6;--s:#fff;--t:#1c2233;--m:#5b6478;--l:#d5dbe6;--i:#1e3a8a;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--bg:#17211e;--s:#1f2b27;--t:#eef2ea;--m:#a6b5ac;--l:#33443d;--i:#e8f0e6;color-scheme:dark}}}}
body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--t);font-size:18px}}
main{{max-width:560px;margin:0 auto;padding:24px 16px 40px}}h1{{color:var(--i);font-size:1.8rem;margin:8px 0 16px}}
summary{{font-size:1.35rem;font-weight:700;color:var(--i);padding:12px 0;cursor:pointer}}
h3{{margin:14px 0 6px;font-size:1rem;color:var(--m);font-weight:600}}
.it{{display:block;padding:16px;margin:8px 0;border:2px solid var(--l);border-radius:14px;background:var(--s);color:var(--i);text-decoration:none;font-weight:600}}
</style></head><body><main><h1>{html.escape(tytul)}</h1>{''.join(sekcje) or "<p>Brak aplikacji.</p>"}</main></body></html>'''
(kat / 'index.html').write_text(page, encoding='utf-8'); print(f'index.html: {n} aplikacji')
