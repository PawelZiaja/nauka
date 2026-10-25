---
name: nauka-na-sprawdzian
description: Tworzy interaktywną aplikację do nauki na sprawdzian dla ucznia szkoły podstawowej (klasy 4–8) – fiszki, test z oceną 1–6 i powtórkę błędów – jako jedna strona HTML (link + plik do pobrania lub wrzucenia na własną stronę), także z obrazkami (mapy, obrazy, przedmioty, schematy). Obsługuje polski, matematykę, angielski, niemiecki, historię, biologię, geografię, fizykę i chemię. Używaj ZAWSZE, gdy rodzic lub uczeń prosi o pomoc w nauce na sprawdzian, kartkówkę lub test, o fiszki, quiz, pytania powtórkowe albo „apkę do nauki” z jakiegoś działu – także gdy wrzuca tylko zdjęcie zagadnień, notatek z zeszytu lub stron podręcznika, albo prosi o rozbudowanie lub poprawienie istniejącej aplikacji do nauki.
---

# Nauka na sprawdzian

Z materiału szkolnego powstaje aplikacja mobilna: **fiszki**, **test** (losuje zadania z różnych działów, daje wynik w % i przewidywaną ocenę) oraz **powtórka błędów**. Postęp zapisuje się w przeglądarce dziecka.

Silnik aplikacji jest gotowy i przetestowany (`assets/szablon.html`). Twoja praca to **treść** – plik JSON z fiszkami i pytaniami – oraz jej bezwzględna poprawność. Nie przepisuj silnika od zera; jeśli brakuje typu zadania, dopisz go do szablonu i do testu.

## 1. Ustal, zanim zaczniesz

- **Dla kogo:** która klasa. Jeśli w pamięci jest informacja o dzieciach i ich klasach, użyj jej; jeśli nie wiadomo, o które dziecko chodzi – zapytaj krótko.
- **Przedmiot i dział.**
- **Materiał:** najlepiej zdjęcie zagadnień od nauczyciela, notatek albo stron podręcznika – to one wyznaczają zakres i akcenty. Bez materiału oprzyj się na podstawie programowej dla danej klasy i powiedz o tym.
- **Obrazki** – czy materiał ich wymaga (mapa, obraz, przedmiot historyczny, schemat, wykres). Jeśli tak, a rodzic nie wrzucił zdjęć – poproś o nie (szczegóły: `references/obrazy.md`).
- **Progi ocen** – jeśli rodzic je podał, wpisz do `config.progi`; inaczej użyj domyślnych i wspomnij o tym raz.

Nie zasypuj pytaniami – jeśli zakres jest jasny, buduj.

## 2. Przeczytaj materiały pomocnicze

- `references/klasy.md` – jak pisać dla danej klasy (język, trudność, wielkość puli).
- `references/przedmioty.md` – sekcja dla danego przedmiotu: typy zadań, tryb sprawdzania wpisów, pułapki.
- `references/format-tresci.md` – dokładny format JSON i wszystkie typy zadań z przykładami.
- `references/obrazy.md` – gdy w materiale są obrazki: skąd je brać, jak przyciąć, jak zrobić zadanie „wskaż na obrazku”, prawa autorskie.
- `references/strona.md` – gdy rodzic pyta, jak udostępnić aplikację komuś bez konta Claude (strona internetowa).
- Przykład pełnej, dobrej treści: `przyklady/polski-kl5-rzeczownik-przymiotnik.json` (46 fiszek, 521 pytań). Próbka wszystkich typów: `przyklady/probka-wszystkich-typow.json`.

## 3. Zaplanuj zakres

Rozpisz zagadnienia z materiału na **8–16 kategorii** (pole `c`). Test losuje z różnych kategorii, więc każda powinna mieć sensowną liczbę pytań. Domyślne rozmiary:
- fiszki: 30–60; **języki obce: 80–200** (słówka i zwroty, `dwa: true` – losowy kierunek, `lang` + `config.mowa` – wymowa),
- pula pytań: ok. 300–500 dla pełnego działu, min. ok. 150 dla wąskiego tematu (rodzic woli duże pule – lepiej więcej niż mniej),
- test: 15 zadań (klasa 7–8: można 20).

## 4. Napisz treść generatorem

Przy dużej puli pisz skrypt w Pythonie (`/home/claude/gen.py`): **tabele danych** (np. odmiana wyrazów, daty, wzory, słówka) → z nich różne typy pytań, plus pytania pisane ręcznie (pułapki, zdania z życia ucznia). Tabele ręcznie sprawdzone raz dają setki poprawnych pytań; generowanie losowymi regułami (np. odmiana „z automatu”) – nie, bo produkuje błędy. Użyj stałego ziarna losowania, żeby wynik był powtarzalny.

Zasady treści:
- **Poprawność ponad wszystko.** Sprawdź każdą formę, datę, wzór, wynik. Przy faktach, których nie jesteś pewien (daty, dane liczbowe, nazwy), szukaj w sieci przed wpisaniem. Lepiej usunąć pytanie niż zostawić wątpliwe.
- **Jedna poprawna odpowiedź.** W zadaniach wyboru żadna z błędnych opcji nie może być też poprawna (uwaga na formy o tym samym brzmieniu, wyjątki, synonimy).
- **Każde pytanie ma wyjaśnienie** (`ex`) – krótkie: dlaczego tak, jaka zasada.
- Przykłady z życia ucznia: szkoła, sport, gry, zwierzęta, wycieczki. Bez infantylizmu.
- Polska typografia: cudzysłów „…”, półpauza –.
- Nie cytuj chronionych tekstów (piosenek, dłuższych fragmentów lektur).

## 5. Zbuduj i przetestuj

**W Claude Code (komputer rodzica, repozytorium GitHub) postępuj według `references/claude-code.md`** – zamiast kroków 5–6 poniżej, które dotyczą claude.ai.

```bash
cd /tmp && [ -d node_modules/jsdom ] || npm i jsdom@24 --silent
SK=<ścieżka do tego skilla>
python3 $SK/scripts/buduj.py /home/claude/dane.json /mnt/user-data/outputs/<nazwa>.html
NODE_PATH=/tmp/node_modules node $SK/scripts/test_aplikacji.js /mnt/user-data/outputs/<nazwa>.html
```

`buduj.py` sprawdza strukturę (indeksy, duplikaty, brak wyjaśnień) i składa HTML. `test_aplikacji.js` uruchamia aplikację, wyświetla każde pytanie, sprawdza, że każda poprawna odpowiedź jest przyjmowana, a odpowiedzi z listy `zle` odrzucane, i przechodzi cały test. Napraw wszystko, co zgłoszą – nie publikuj z błędami. Potem przejrzyj losowe 20–30 pytań wzrokiem pod kątem merytoryki i języka.

## 6. Opublikuj i oddaj plik

Zawsze oddawaj **oba**: opublikuj plik narzędziem Artifact (tytuł = temat, jedno emoji jako favicon) **i** pokaż ten sam plik HTML przez `present_files`, żeby rodzic mógł go pobrać i wrzucić na własną stronę. Plik jest samodzielny (obrazki są w środku), działa też bez internetu – trzeba go tylko otworzyć w przeglądarce. Przy aktualizacji istniejącej aplikacji publikuj z jej `url` i **nie zmieniaj `config.klucz`** – wtedy postęp dziecka zostaje (identyfikatory pytań wynikają z ich treści, więc dodawanie pytań nie psuje listy błędów).

## 7. Odpowiedź dla rodzica

Krótko: link i plik, co zawiera (liczba fiszek i pytań, główne działy, obrazki), jak sprawdzane są wpisy. Dodaj jedno zdanie przypomnienia:
> Link z Claude otworzy tylko ktoś zalogowany do Claude (na koncie firmowym – tylko osoby z organizacji). Dla dzieci najlepiej wrzucić plik na własną stronę (patrz `references/strona.md`) albo otworzyć plik w przeglądarce – nie w podglądzie komunikatora, bo tam nic nie da się kliknąć.

Jeśli rodzic ma już stronę z aplikacjami, przypomnij, żeby po wrzuceniu nowego pliku odświeżył spis (`scripts/spis.py`) – albo wygeneruj mu nowy `index.html`.
