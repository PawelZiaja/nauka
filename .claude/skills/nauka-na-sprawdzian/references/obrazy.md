# Obrazki w aplikacji

Przydają się w każdym przedmiocie: mapy (geografia, historia), obrazy i ilustracje (polski, historia), przedmioty i zabytki (historia), schematy (biologia, fizyka, chemia), figury i wykresy (matematyka).

## Skąd brać obrazki
1. **Zdjęcia od rodzica** (najlepsze): strony podręcznika, atlas, ilustracje z zeszytu. Pliki są w `/mnt/user-data/uploads/`. Jedno zdjęcie strony zwykle zawiera kilka obrazków – wytnij je (`scripts/wytnij.py`).
2. **Rysunek SVG zrobiony przez Ciebie** – tylko gdy dokładność nie zależy od wierności oryginałowi: figury geometryczne z wymiarami, oś liczbowa i układ współrzędnych, wykresy, schemat obwodu, schemat komórki lub kwiatu, model cząsteczki, oś czasu. Zapisz plik `.svg` w `/home/claude/obrazy/`, z białym tłem i czytelnymi napisami (min. 18 px przy szerokości 400). Nie rysuj „z pamięci” map konturowych krajów ani dzieł sztuki – wyjdą niedokładne; o nie poproś rodzica.
3. **Pliki z sieci** (np. obraz Matejki z Wikimedia Commons): nie da się ich pobrać z poziomu Claude. Poproś rodzica, by pobrał plik i wrzucił go do rozmowy; podaj mu, czego szukać.

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

## Jak używać w treści
- `img` + `alt` w pytaniu: obrazek nad treścią, dotknięcie powiększa (można przybliżać palcami).
- `podpis`: autor, tytuł, data – przy dziełach sztuki zawsze.
- Typ `spot`: „wskaż na obrazku” – współrzędne z siatki, nigdy szacowane na oko bez siatki.
- Fiszki: `img` na przodzie („Co to za obraz? Kto go namalował?”), `imgO` na odwrocie (np. schemat z podpisami).
- Jeden obrazek → kilka pytań różnego typu (np. mapa: 5× `spot`, 3× `mc`). Wpisujesz go raz w `obrazy`.
- Każde zadanie z obrazkiem musi mieć sens na małym ekranie – drobne szczegóły tylko przy `spot` z odpowiednio dużym `r`.
