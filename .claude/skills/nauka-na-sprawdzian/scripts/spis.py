#!/usr/bin/env python3
"""Tworzy stronę startową index.html ze spisem wszystkich aplikacji w katalogu i jego podfolderach,
pogrupowanych według klasy i przedmiotu (dane brane z config każdej aplikacji).
Struktura na stronie: klasa-5/polski/temat.html, klasa-7/historia/temat.html itd.
Przy każdej aplikacji pasek opanowania fiszek i gwiazdki (z postępu zapisanego w przeglądarce),
na górze seria dni i poziom – te same dane, co w aplikacjach (szablon.html, sekcja GRA).
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
    kl = re.search(r'"klucz":"(.*?)"', t); nf = 0
    if f.with_suffix('.json').exists():
        d = json.loads(f.with_suffix('.json').read_text(encoding='utf-8'))
        kl = d.get('config', {}).get('klucz'); nf = len(d.get('fiszki', []))
    else: kl = kl.group(1) if kl else ''
    apps.setdefault(klasa, {}).setdefault((przedm, czesci[1] if len(czesci) > 2 else ''), []).append((m.group(1) if m else f.stem, f.relative_to(kat).as_posix(), kl, nf))
# Postęp z localStorage: wspólny „nauka-gra” (XP, seria) i „nauka-<klucz>” każdej aplikacji (fiszki, oceny, błędy).
# Tabela poziomów i liczenie serii – tak samo jak w assets/szablon.html.
GRA_JS = r"""
const POZIOMY=[[0,'Nowicjusz'],[100,'Uczeń'],[250,'Odkrywca'],[500,'Badacz'],[900,'Znawca'],[1500,'Ekspert'],[2300,'Mistrz'],[3500,'Profesor'],[5000,'Geniusz']];
const wczytaj=k=>{try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}};
function dzien(o){const d=new Date();d.setDate(d.getDate()-(o||0));return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
const m=(location.search.match(/motyw=(\w+)/)||[])[1],dt=new Date(),mc=dt.getMonth()+1,dz=dt.getDate();
const HW=m?m==='halloween':(mc===10&&dz>=25)||(mc===11&&dz<=2),OG=HW?'🎃':'🔥';
if(HW){document.documentElement.dataset.sezon='halloween';document.querySelector('h1').textContent+=' 🎃';}
const g=Object.assign({xp:0,dni:{},dzis:'',ile:0},wczytaj('nauka-gra')||{});
let o=g.dni[dzien()]?0:1,s=0;while(g.dni[dzien(o+s)])s++;
let i=0;while(i+1<POZIOMY.length&&g.xp>=POZIOMY[i+1][0])i++;const nx=POZIOMY[i+1];
if(g.xp>0){document.getElementById('game').hidden=false;
  document.getElementById('gS').innerHTML=OG+' '+s+' <small>'+(s===1?'dzień':'dni')+' z rzędu</small>';
  document.getElementById('gL').textContent=POZIOMY[i][1];
  document.getElementById('gX').textContent=g.xp+' XP'+(nx?' / '+nx[0]:'');
  document.getElementById('gB').style.width=(nx?(g.xp-POZIOMY[i][0])/(nx[0]-POZIOMY[i][0])*100:100)+'%';
  const ile=g.dzis===dzien()?g.ile:0;
  document.getElementById('gG').textContent=g.dni[dzien()]?'✔ Cel dnia zaliczony':'Cel dnia: '+Math.min(ile,10)+'/10 odpowiedzi albo jeden cały test';
  if(HW&&g.cukD===dzien()&&g.cuk)document.getElementById('gG').textContent+=' · 🍬 '+g.cuk;}
document.querySelectorAll('a.it[data-k]').forEach(a=>{const S=wczytaj('nauka-'+a.dataset.k);if(!S)return;
  const n=+a.dataset.n,k=Math.min(n,Object.values(S.known||{}).filter(Boolean).length),best=S.best||(S.last&&S.last.g)||0;
  const gw=(n&&k>=n?1:0)+(best>=5?1:0)+(S.last&&!(S.errors||[]).length?1:0);
  a.querySelector('.pg').innerHTML=(n?'<span class="bar"><i style="width:'+(k/n*100)+'%"></i></span><span>fiszki '+k+'/'+n+'</span>':'<span style="flex:1">'+(best?'najlepsza ocena: '+best:'')+'</span>')+
    '<span class="st" title="gwiazdki: wszystkie fiszki · test na 5 lub 6 · zero błędów do poprawy">'+'★'.repeat(gw)+'☆'.repeat(3-gw)+'</span>';});
"""
# Podręczniki dzieci (podreczniki.json + okladki/): okładka przy każdym przedmiocie, także bez aplikacji
pod = json.loads((kat / 'podreczniki.json').read_text(encoding='utf-8')) if (kat / 'podreczniki.json').exists() else {}
for klucz, P in pod.items():
    kl, folder = klucz.split('/'); nr = kl.replace('klasa-', '')
    if not any(f == folder for _, f in apps.get(nr, {})): apps.setdefault(nr, {})[(P['przedmiot'], folder)] = []
def ksiazka(nr, folder):
    P = pod.get(f'klasa-{nr}/{folder}')
    if not P: return ''
    return (f'<div class="bk"><img src="{html.escape(P["okladka"])}" alt="Okładka: {html.escape(P["tytul"])}" loading="lazy">'
            f'<span>Podręcznik: <b>{html.escape(P["tytul"])}</b> · {html.escape(P["wydawnictwo"])}<br><small>{html.escape(P["opis"])}</small></span></div>')
sekcje = []
for klasa in sorted(apps, key=lambda x: int(x) if x.isdigit() else 99):
    przedm = ''.join(f'<h3>{html.escape(p)}</h3>' + ksiazka(klasa, fo) + ('' if lst else '<p class="pusto">Aplikacje pojawią się przed sprawdzianem.</p>') + ''.join(f'<a class="it" href="{html.escape(h)}" data-k="{html.escape(kl)}" data-n="{nf}"><span>{html.escape(t)}</span><span class="pg"></span></a>' for t, h, kl, nf in sorted(lst)) for (p, fo), lst in sorted(apps[klasa].items()))
    sekcje.append(f'<details open><summary>Klasa {klasa}</summary>{przedm}</details>')
n = sum(len(l) for d in apps.values() for l in d.values())
page = f'''<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{html.escape(tytul)}</title>
<script>/* licznik odwiedzin GoatCounter (panel: ziaja.goatcounter.com) – tylko na stronie */
if(location.hostname==='pawelziaja.github.io'){{var gc=document.createElement('script');gc.async=true;gc.src='https://gc.zgo.at/count.js';gc.dataset.goatcounter='https://ziaja.goatcounter.com/count';document.head.appendChild(gc);}}</script>
<style>:root{{--bg:#fbfbf6;--s:#fff;--t:#1c2233;--m:#5b6478;--l:#d5dbe6;--i:#1e3a8a;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--bg:#17211e;--s:#1f2b27;--t:#eef2ea;--m:#a6b5ac;--l:#33443d;--i:#e8f0e6;color-scheme:dark}}}}
body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--t);font-size:18px}}
main{{max-width:560px;margin:0 auto;padding:24px 16px 40px}}h1{{color:var(--i);font-size:1.8rem;margin:8px 0 16px}}
summary{{font-size:1.35rem;font-weight:700;color:var(--i);padding:12px 0;cursor:pointer}}
h3{{margin:14px 0 6px;font-size:1rem;color:var(--m);font-weight:600}}
.it{{display:block;padding:16px;margin:8px 0;border:2px solid var(--l);border-radius:14px;background:var(--s);color:var(--i);text-decoration:none;font-weight:600}}
.pg{{display:flex;align-items:center;gap:10px;margin-top:8px;font-size:.85rem;font-weight:500;color:var(--m)}}.pg:empty{{display:none}}
.bar{{flex:1;height:8px;border-radius:99px;background:var(--l);overflow:hidden}}.bar i{{display:block;height:100%;background:var(--i);border-radius:99px}}
.bk{{display:flex;align-items:center;gap:10px;margin:2px 0 6px;font-size:.85rem;color:var(--m)}}.bk img{{width:40px;height:auto;border-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.3)}}
.bk b{{color:var(--t)}}.bk small{{font-size:.78rem}}.pusto{{margin:4px 0 8px;font-size:.85rem;color:var(--m)}}
.st{{color:#d97706;font-size:1rem;letter-spacing:1px}}
.game{{border:2px solid var(--l);border-radius:16px;background:var(--s);padding:12px 14px;margin:0 0 8px}}
.gtop{{display:flex;justify-content:space-between;align-items:center;gap:10px}}.sr{{font-size:1.25rem;font-weight:700;color:#d97706}}
.sr small,.lv span,.goal{{font-size:.85rem;font-weight:500;color:var(--m)}}.lv{{text-align:right}}.lv b{{color:var(--i)}}
:root[data-sezon=halloween]{{--bg:#fbf7ef;--i:#4c1d95;--l:#ddd2ea}}
@media (prefers-color-scheme:dark){{:root[data-sezon=halloween]{{--bg:#17111f;--s:#211830;--t:#f5f0fa;--m:#b9a9c9;--l:#3b2d4d;--i:#fdba74}}}}
.game .bar{{margin:8px 0 6px}}.game .bar i{{background:#d97706}}.goal{{margin:0}}
</style></head><body><main><h1>{html.escape(tytul)}</h1>
<div class="game" id="game" hidden><div class="gtop"><span class="sr" id="gS"></span><span class="lv"><b id="gL"></b><br><span id="gX"></span></span></div><div class="bar"><i id="gB"></i></div><p class="goal" id="gG"></p></div>
{''.join(sekcje) or "<p>Brak aplikacji.</p>"}<script>{GRA_JS}</script></main></body></html>'''
(kat / 'index.html').write_text(page, encoding='utf-8'); print(f'index.html: {n} aplikacji')
