# Format treści (dane.json)

```json
{
  "config": {
    "tytul": "Rzeczownik i przymiotnik",
    "przedmiot": "Język polski",
    "klasa": 5,
    "klucz": "pl5-rzeczownik-przymiotnik",
    "tagi": {"n": "Rzeczownik", "a": "Przymiotnik"},
    "liczbaPytan": 15,
    "tryb": "luzno",
    "progi": [[100,6],[90,5],[75,4],[50,3],[30,2],[0,1]],
    "mowa": "en-GB"
  },
  "obrazy": {"mapa": "/mnt/user-data/uploads/mapa.jpg", "komorka": "obrazy/komorka.svg"},
  "fiszki": [ ... ],
  "pytania": [ ... ]
}
```

- `klucz` – identyfikator zapisu postępu (małe litery, cyfry, myślniki). Unikalny dla każdej aplikacji; **przy aktualizacji nie zmieniaj**.
- `tagi` – etykiety fiszek (max 4 kolory). `tryb` – domyślny tryb sprawdzania wpisów.
- `progi` – [minimalny %, ocena], od najwyższej. Domyślne jak wyżej.
- `mowa` – kod języka do czytania na głos (`en-GB`, `en-US`, `de-DE`); przycisk 🔊 pojawia się przy fiszkach z polem `lang`.
- `obrazy` – słownik: klucz → ścieżka do pliku (jpg/png/webp/svg; względna = względem pliku JSON) lub gotowe `data:` URI. `buduj.py` zmniejsza zdjęcia (do 1100 px) i wkleja je do HTML. Jeden obrazek może być użyty w wielu pytaniach – wpisujesz go raz.

## Fiszka
```json
{"tag": "n", "p": "Dopełniacz – jakie pytania?", "o": "kogo? czego?", "w": "Nie ma kogo? – kolegi."}
```
`p` przód, `o` odpowiedź (podkreślona markerem), `w` wyjaśnienie/przykład. `\n` = nowa linia.
Opcjonalnie: `img` (obrazek na przodzie, klucz z `obrazy`), `imgO` (obrazek na odwrocie), `alt` (opis obrazka – wymagany przy obrazku), `dwa: true` (losowo pokazuje stronę `p` albo `o` jako przód – słówka w obie strony), `lang: "p"|"o"` (która strona jest w języku obcym – do wymowy).
Przy więcej niż jednym tagu aplikacja pozwala wybrać zestaw fiszek (np. tylko „Słówka – jedzenie”), więc przy dużych taliach dziel je tagami na tematy.

## Pola wspólne pytań
`t` typ, `q` treść, `ex` wyjaśnienie (wymagane), `c` kategoria (do losowania), opcjonalnie `img` + `alt` + `podpis` (obrazek nad treścią, powiększany dotknięciem; `podpis` np. „Jan Matejko, Bitwa pod Grunwaldem, 1878”), `typ` – własny nagłówek zamiast domyślnego („Stopniuj przymiotnik”), `id` – stały identyfikator (zwykle zbędny).

## Typy

**mc** – jednokrotny wybór (opcje są tasowane):
```json
{"t":"mc","q":"Jaki rodzaj ma „okno”?","o":["męski","żeński","nijaki"],"a":2,"ex":"to okno","c":"rodzaj"}
```

**tf** – prawda/fałsz: `"a": true`.

**in** – wpisz odpowiedź; `a` = lista akceptowanych wariantów (pierwszy = wzorcowy, pokazywany przy błędzie):
```json
{"t":"in","q":"Odmień „mądra sowa” w narzędniku (z kim?).","a":["mądrą sową","z mądrą sową"],"tryb":"koncowka","k":2,"zle":["mądra sowa"],"ex":"…","c":"odmiana"}
```
Opcje: `tryb`, `k`, `cs` (wielkość liter), `zle`, `ph` (podpowiedź w polu), `jedn`.

**num** – liczba; `a` liczba lub lista liczb, `tol` tolerancja, `jedn` jednostka obok pola:
```json
{"t":"num","q":"Pole prostokąta 4 cm × 2,5 cm:","a":10,"jedn":"cm²","ex":"4 · 2,5 = 10","c":"pola"}
```

**gap** – zdanie z luką `[[…]]` (wyróżniona) i przyciskami wyboru; `f` = pełna poprawna forma:
```json
{"t":"gap","q":"To był [[(nie)miły]] dzień.","o":["razem","osobno"],"a":0,"f":"niemiły","ex":"…","typ":"„Nie” – razem czy osobno?","c":"nie"}
```

**pick** – zaznacz wyrazy w zdaniu; `s` zdanie (wyrazy rozdzielone spacjami), `a` indeksy wyrazów (od 0, interpunkcja zostaje przy wyrazie):
```json
{"t":"pick","q":"Zaznacz wszystkie rzeczowniki.","s":"Mały kot spał na poduszce.","a":[1,4],"ex":"…","c":"zaznacz"}
```
Generując, oznaczaj wyrazy w zdaniu znacznikami (np. `*kot`) i licz indeksy skryptem – nie ręcznie.

**match** – dopasuj pary `p: [[lewa, prawa], …]`; prawe strony mogą się powtarzać.

**multi** – kilka pól; każde pole: `l` etykieta, `a` lista wariantów (albo liczba z `num: true`), opcjonalnie własne `tryb`/`k`/`cs`/`tol`:
```json
{"t":"multi","q":"Stopniuj: dobry","pola":[{"l":"Stopień wyższy","a":["lepszy"]},{"l":"Stopień najwyższy","a":["najlepszy"]}],"tryb":"koncowka","k":1,"ex":"…","c":"stopniowanie"}
```

**order** – ułóż w kolejności; `o` w **poprawnej** kolejności (aplikacja tasuje), 3–6 elementów:
```json
{"t":"order","q":"Od najwcześniejszego:","o":["Chrzest Polski","Grunwald","Konstytucja 3 maja"],"ex":"966 → 1410 → 1791","c":"chronologia"}
```

**spot** – wskaż miejsce na obrazku; `cel`: środek `x`, `y` w % (od lewego górnego rogu) i promień `r` w % szerokości obrazka; `f` – słowny opis poprawnego miejsca:
```json
{"t":"spot","q":"Wskaż na mapie Kraków.","img":"mapa","alt":"Mapa Polski","cel":{"x":56,"y":82,"r":5},"f":"południe Polski, nad Wisłą","ex":"…","c":"mapa"}
```
Współrzędne odczytuj z `scripts/siatka.py` – nie zgaduj. `r` dobierz tak, by objął cały obiekt, ale nie sąsiednie (zwykle 4–8).

## Proporcje (orientacyjnie)
Ok. 40–50% wybór (mc/gap/tf), 25–35% wpisywanie (in/num/multi), reszta pick/match/order – zależnie od przedmiotu. Każda kategoria min. ok. 10 pytań.
