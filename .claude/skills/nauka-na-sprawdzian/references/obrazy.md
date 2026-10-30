# Obrazki w aplikacji

Przydają się w każdym przedmiocie: mapy (geografia, historia), obrazy i ilustracje (polski, historia), przedmioty i zabytki (historia), schematy (biologia, fizyka, chemia), figury i wykresy (matematyka).

## Skąd brać obrazki
1. **Zdjęcia od rodzica** (najlepsze): strony podręcznika, atlas, ilustracje z zeszytu. Pliki są w `/mnt/user-data/uploads/`. Jedno zdjęcie strony zwykle zawiera kilka obrazków – wytnij je (`scripts/wytnij.py`).
2. **Rysunek SVG zrobiony przez Ciebie** – tylko gdy dokładność nie zależy od wierności oryginałowi: figury geometryczne z wymiarami, oś liczbowa i układ współrzędnych, wykresy, schemat obwodu, schemat komórki lub kwiatu, model cząsteczki, oś czasu. Zapisz plik `.svg` w `/home/claude/obrazy/`, z białym tłem i czytelnymi napisami (min. 18 px przy szerokości 400). Nie rysuj „z pamięci” map konturowych krajów ani dzieł sztuki – wyjdą niedokładne; o nie poproś rodzica.
3. **Pliki z Wikimedia Commons** (mapy, obrazy malarzy, zdjęcia zabytków):
   - **claude.ai** – nie da się ich pobrać; poproś rodzica, by pobrał plik i wrzucił go do rozmowy, podaj mu, czego szukać.
   - **Claude Code** – pobierz sam (opis niżej: „Mapy z Wikimedia Commons”). Tylko domena publiczna, CC0, CC BY, CC BY-SA. Autora, tytuł pliku i licencję wpisz w `podpis` każdego zadania z tym obrazkiem i podaj w raporcie końcowym.

Nie wyszukuj i nie wklejaj obrazków przedstawiających przemoc, treści drastycznych itp. – nawet przy historii wojen wybieraj mapy, portrety, przedmioty.

## Prawa autorskie
- Aplikacja tylko dla rodziny (plik, link Claude): zdjęcia z podręcznika są w porządku jako prywatna pomoc do nauki.
- **Publiczna strona** (GitHub Pages itp.): skany podręczników to cudza własność – używaj własnych rysunków SVG, własnych zdjęć i dzieł w domenie publicznej (np. obrazy malarzy zmarłych ponad 70 lat temu). Jeśli w aplikacji są skany z podręcznika, a rodzic planuje stronę publiczną – powiedz mu o tym jednym zdaniem.

## Przygotowanie
```bash
SK=<ścieżka do skilla>
python3 $SK/scripts/siatka.py /mnt/user-data/uploads/strona.jpg /home/claude/siatka.png   # siatka co 10%
# obejrzyj siatka.png narzędziem view, odczytaj prostokąt wycinka w %
python3 $SK/scripts/wytnij.py /mnt/user-data/uploads/strona.jpg /home/claude/obrazy/mapa.jpg 8 12 92 70
python3 $SK/scripts/siatka.py /home/claude/obrazy/mapa.jpg /home/claude/siatka-mapa.png  # współrzędne do „spot”
```
- Zawsze obejrzyj wycinek przed użyciem (czy nic nie ucięte, czy jest czytelny).
- Jeśli na obrazku są podpisy zdradzające odpowiedź (np. nazwy miast na mapie przy zadaniu „wskaż Kraków”), wybierz inny obrazek albo zamaskuj podpisy (np. białe prostokąty w Pillow) – inaczej zadanie nie sprawdza wiedzy.
- `buduj.py` sam zmniejsza zdjęcia do 1100 px i kompresuje. Cel: wszystkie obrazki razem do ok. 3–5 MB.

## Mapy z Wikimedia Commons (Claude Code)

Sprawdzone przy aplikacji „Wody powierzchniowe i powodzie” (geografia kl. 7).

1. **Wybór pliku.** Licencję i adres sprawdź przez API (z nagłówkiem `User-Agent`, inaczej Wikimedia zwraca błąd):
   ```bash
   curl -s -A "nauka-app/1.0 (edu)" "https://commons.wikimedia.org/w/api.php?action=query&titles=File:Relief_Map_of_Poland.svg&prop=imageinfo&iiprop=url|extmetadata&iiextmetadatafilter=LicenseShortName|Artist&iiurlwidth=1280&format=json"
   ```
   Pobierz `thumburl` (PNG wyrenderowany z SVG) do osobnego, pustego folderu w katalogu roboczym.
   - Polska z rzekami i jeziorami, bez napisów: **`Relief Map of Poland.svg`** (TUBS, CC BY-SA 3.0). `Poland location map.svg` nie ma rzek.
   - Inne kraje i kontynenty: pliki `… location map.svg` / `Relief Map of ….svg` / `… in Europe (-rivers -mini map).svg` (NordNordWest, TUBS).
   Najpierw obejrzyj mapę: czy ma potrzebne obiekty i czy **nie ma napisów** zdradzających odpowiedź. Napisy zamaskuj (białe prostokąty w Pillow) albo wybierz inny plik.
2. **Czytelność na telefonie.** Cienkie rzeki pogrub w Pillow: wybierz piksele w kolorze rzek (np. `b>150 and r<120 and b-r>90`), poszerz maskę (`ImageFilter.MaxFilter(3)`) i zamaluj je mocniejszym niebieskim. Obejrzyj wynik.
3. **Współrzędne do `spot`** – licz z długości i szerokości geograficznej, nie na oko. Mapy lokalizacyjne Wikipedii są w odwzorowaniu prostokątnym; granice ramki są w `https://en.wikipedia.org/w/index.php?title=Module:Location_map/data/<Kraj>&action=raw` (Polska: top 55.2, bottom 48.7, left 13.8, right 24.5). Wtedy:
   `x% = (lon − left) / (right − left) · 100`, `y% = (top − lat) / (top − bottom) · 100`.
   Sprawdź odwzorowanie: nanieś kilka miast (np. Warszawa, Kraków, Gdańsk) – muszą leżeć na swoich rzekach. Potem nanieś **wszystkie cele z `r`** na jeden obrazek i obejrzyj: cel obejmuje obiekt, a koła różnych zadań na siebie nie nachodzą (nachodzące – usuń lub zmniejsz `r`). Obiekty niewidoczne na mapie (małe jeziora) – tylko z większym `r` albo wcale.
4. **Mapa z literami** do zadań „która rzeka to A?”: punkt z kolorowym kółkiem i literą, przyciągnięty skryptem do najbliższego piksela rzeki (szukaj koloru z tolerancją – JPEG zmienia kolory).
5. W `podpis`: `Mapa: <autor>, „<tytuł pliku>”, Wikimedia Commons, <licencja> (<co zmieniono, np. rzeki pogrubione>)`.

## Schematy SVG – podgląd

Narysowane SVG obejrzyj przed budową: wklej je **w treść** jednej strony HTML (nie przez `<img src>`, podgląd nie wczyta plików obok) i otwórz w przeglądarce. Taką stronę trzymaj **tylko w katalogu tymczasowym (scratchpad)**, nigdy w repozytorium – inaczej trafi do spisu na stronie.
Na schematach do zadań „co oznaczono numerem…” / „jaki to typ…” nie umieszczaj nazw będących odpowiedzią – tylko numery lub litery i neutralne opisy.

## Jak używać w treści
- `img` + `alt` w pytaniu: obrazek nad treścią, dotknięcie powiększa (można przybliżać palcami).
- `podpis`: autor, tytuł, data – przy dziełach sztuki zawsze.
- Typ `spot`: „wskaż na obrazku” – współrzędne z siatki, nigdy szacowane na oko bez siatki.
- Fiszki: `img` na przodzie („Co to za obraz? Kto go namalował?”), `imgO` na odwrocie (np. schemat z podpisami).
- Jeden obrazek → kilka pytań różnego typu (np. mapa: 5× `spot`, 3× `mc`). Wpisujesz go raz w `obrazy`.
- Każde zadanie z obrazkiem musi mieć sens na małym ekranie – drobne szczegóły tylko przy `spot` z odpowiednio dużym `r`.
