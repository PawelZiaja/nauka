---
name: nauka-na-sprawdzian
description: Tworzy interaktywną aplikację do nauki na sprawdzian dla ucznia szkoły podstawowej (klasy 4–8) – fiszki, test z oceną 1–6 i powtórkę błędów – jako jedna strona HTML (link + plik do pobrania lub wrzucenia na własną stronę), także z obrazkami (mapy, obrazy, przedmioty, schematy). Obsługuje polski, matematykę, angielski, niemiecki, historię, biologię, geografię, fizykę i chemię. Używaj ZAWSZE, gdy rodzic lub uczeń prosi o pomoc w nauce na sprawdzian, kartkówkę lub test, o fiszki, quiz, pytania powtórkowe albo „apkę do nauki” z jakiegoś działu – także gdy wrzuca tylko zdjęcie zagadnień, notatek z zeszytu lub stron podręcznika, albo prosi o rozbudowanie lub poprawienie istniejącej aplikacji do nauki.
---

# Nauka na sprawdzian

Z materiału szkolnego powstaje aplikacja mobilna: **fiszki**, **test** (losuje zadania z różnych działów, daje wynik w % i przewidywaną ocenę) oraz **powtórka błędów**. Postęp zapisuje się w przeglądarce dziecka.

Silnik ma też grywalizację wspólną dla wszystkich aplikacji w tej przeglądarce: punkty XP i poziomy, serię dni z celem dnia (10 odpowiedzi albo cały test) i konfetti; spis (`scripts/spis.py`) pokazuje serię, poziom oraz przy każdej aplikacji pasek opanowania fiszek i gwiazdki 0–3. Zmiana szablonu = przebuduj wszystkie aplikacje z ich `temat.json` Fiszka zawsze mieści się na jednym ekranie (tekst sam się zmniejsza), „Umiem” działa dopiero po odwróceniu karty. Motyw sezonowy Halloween (25.10–2.11, podgląd `?motyw=halloween`) dodaje dynie, duchy, nietoperze, cukierki i dźwięki z Web Audio (przycisk 🔊). Statystyki (GoatCounter, tylko na stronie): każdy test i powtórka mają numer podejścia na urządzeniu, a każdy błąd – pytanie, odpowiedź dziecka i poprawną; raport po kolei: `scripts/raport.py [od] [do] --nazwy kod=imię` (klucz w `GOATCOUNTER_TOKEN`, imion nie zapisuj w repozytorium).

Silnik aplikacji jest gotowy i przetestowany (`assets/szablon.html`). Twoja praca to **treść** – plik JSON z fiszkami i pytaniami – oraz jej bezwzględna poprawność. Nie przepisuj silnika od zera; jeśli brakuje typu zadania, dopisz go do szablonu i do testu.

## 0. Tryb „jedno zdanie” (domyślny)

Rodzic zwykle pisze tylko jedno zdanie: tytuł sprawdzianu, ścieżkę do folderu ze zdjęciami albo jedno i drugie (np. „Sprawdzian z geografii, materiały w C:\…\Photos-1-001(6)”). **Wszystko inne ustalasz sam** według tego skilla – nie dopytuj o klasę, wielkość puli, typy zadań, obrazki ani o zgodę na publikację.

Przebieg:
1. Obejrzyj **wszystkie** materiały (zdjęcia zmniejsz najpierw do ok. 1800 px w katalogu roboczym, żeby dało się je przeczytać).
2. Napisz rodzicowi **krótką analizę** (kilka punktów): tematy i zagadnienia, pojęcia, nazwy własne, dane liczbowe, mapy i schematy z książki, typy zadań – oraz **plan w 2–3 zdaniach** (klasa, liczba fiszek i pytań, kategorie, obrazki). **Nie czekaj na odpowiedź** – od razu buduj.
3. Treść, obrazki, budowa, test, publikacja – kroki 3–5 i `references/claude-code.md`.
4. Raport końcowy (krok 7).

Pytanie zadaj tylko wtedy, gdy bez odpowiedzi nie da się zacząć: nie wiadomo, jaki to przedmiot lub dział, materiały się nie otwierają (np. link do albumu Google Photos – poproś o pobrany folder), albo temat jednakowo pasuje do klas obu dzieci (patrz niżej). Wtedy jedno krótkie pytanie, nie lista.

## 1. Ustal, zanim zaczniesz

- **Dla kogo – klasa.** Ustal sama/sam, w tej kolejności:
  1. jawnie podana klasa w zdaniu rodzica;
  2. nagłówek, numer rozdziału lub tytuł podręcznika na zdjęciach (np. „Planeta Nowa 7”, „klasa 5”);
  3. podstawa programowa: w której klasie jest ten dział (np. fizyka i chemia – tylko 7–8; „wody powierzchniowe Polski” – geografia 7; „ułamki zwykłe – wprowadzenie” – matematyka 4–5);
  4. klasy dzieci z `CLAUDE.md` / pamięci – wybierz tę, która pasuje do działu.
  Gdy dział realnie pasuje do obu klas dzieci (np. „rzeczownik” – kl. 5 i 7 w innym zakresie), a materiałów brak – zapytaj krótko.
- **Przedmiot i dział** – z tytułu lub materiałów.
- **Podręcznik dziecka** – w `podreczniki.json` w katalogu strony (klucz `klasa-X/przedmiot`: tytuł, wydawnictwo, edycja, okładka w `okladki/`). Treść, kolejność działów i nazewnictwo dopasuj do tej książki – szkoły mają różne podręczniki i edycje, więc nie zastępuj jej inną. `buduj.py` sam wstawia okładkę i opis do aplikacji, a `spis.py` – do spisu. Nowy podręcznik = nowa pozycja w JSON i okładka (miniatura ok. 200 px, bez stron ze środka).
- **Materiał:** zdjęcia zagadnień od nauczyciela, notatek albo stron podręcznika wyznaczają zakres i akcenty. Ścieżkę do folderu czytaj w całości. Bez materiału oprzyj się na podstawie programowej dla danej klasy i powiedz o tym w analizie.
- **Obrazki** – zdecyduj sam, gdzie pomagają (mapa, schemat, wykres, obraz). Mapy i dzieła pobierz z Wikimedia Commons na wolnej licencji, schematy narysuj jako SVG (`references/obrazy.md`). O zdjęcia proś tylko wtedy, gdy potrzebny jest konkretny obraz, którego nie ma na wolnej licencji.
- **Progi ocen** – jeśli rodzic je podał, wpisz do `config.progi`; inaczej użyj domyślnych i nie wspominaj o nich.

Nie zasypuj pytaniami – jeśli zakres jest jasny, buduj.

## 2. Przeczytaj materiały pomocnicze

- `references/klasy.md` – jak pisać dla danej klasy (język, trudność, wielkość puli).
- `references/przedmioty.md` – sekcja dla danego przedmiotu: typy zadań, tryb sprawdzania wpisów, pułapki.
- `references/format-tresci.md` – dokładny format JSON i wszystkie typy zadań z przykładami.
- `references/obrazy.md` – gdy w materiale są obrazki: skąd je brać, jak przyciąć, jak zrobić zadanie „wskaż na obrazku”, prawa autorskie.
- `references/strona.md` – gdy rodzic pyta, jak udostępnić aplikację komuś bez konta Claude (strona internetowa).
- Przykład pełnej, dobrej treści: `przyklady/polski-kl5-rzeczownik-przymiotnik.json` (46 fiszek, 521 pytań). Próbka wszystkich typów: `przyklady/probka-wszystkich-typow.json`.

## 3. Zaplanuj zakres

Rozpisz zagadnienia z materiału na **8–16 kategorii** (pole `c`). Test losuje z różnych kategorii, więc każda musi mieć **min. ok. 15 pytań**. Wielkość dobierz sam do ilości materiału:
- fiszki: **60–100** dla pełnego działu (2–3 lekcje), 40–60 dla wąskiego tematu; **języki obce: 80–200** (słówka i zwroty, `dwa: true` – losowy kierunek, `lang` + `config.mowa` – wymowa). Przy więcej niż ~40 fiszkach podziel je tagami na 3–4 zestawy,
- pula pytań: **300–500** dla pełnego działu, ok. 200 dla wąskiego tematu (rodzic woli duże pule – lepiej więcej niż mniej, ale nie dobijaj liczby pytaniami-wydmuszkami),
- test (`liczbaPytan`): klasa 4–6 – **15**, klasa 7–8 – **20**.

## 4. Napisz treść generatorem

Przy dużej puli pisz skrypt w Pythonie (`/home/claude/gen.py`): **tabele danych** (np. odmiana wyrazów, daty, wzory, słówka) → z nich różne typy pytań, plus pytania pisane ręcznie (pułapki, zdania z życia ucznia). Tabele ręcznie sprawdzone raz dają setki poprawnych pytań; generowanie losowymi regułami (np. odmiana „z automatu”) – nie, bo produkuje błędy. Użyj stałego ziarna losowania, żeby wynik był powtarzalny.

Zasady treści:
- **Poprawność ponad wszystko.** Sprawdź każdą formę, datę, wzór, wynik. Każdą nazwę i liczbę porównaj z materiałem; gdy jej tam nie ma – sprawdź w wiarygodnym źródle (np. Wikipedia, GUS, IMGW) przed wpisaniem. Gdy książka zaokrągla (np. 800 km zamiast 808,2 km), trzymaj się książki. Lepiej usunąć pytanie niż zostawić wątpliwe.
- **Zakres i poziom z książki** – zadania podobne do tych z podręcznika, ale nie przepisane dosłownie. Treści spoza materiału dodawaj oszczędnie i wymień je w raporcie.
- **Typy zadań dobieraj do treści** (szczegóły w `references/przedmioty.md`): nazwy wpisywane – `in` w trybie `luzno` z wariantami (z polskimi znakami i bez); przyporządkowanie (rzeka → dorzecze, przyczyna → skutek) – `match` i `mc`; kolejność (chronologia, długości) – `order`; dane liczbowe – `num` z tolerancją; położenie na mapie lub schemacie – `spot` i `mc` z obrazkiem.
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

Zawsze w tym samym układzie, krótko:
- **adres** aplikacji (w Claude Code – adres na stronie; na claude.ai – link i plik),
- **liczba fiszek, pytań i obrazków**, długość testu,
- **lista kategorii** (z liczbą pytań),
- jak sprawdzane są wpisy (jedno zdanie),
- **źródła i licencje** pobranych obrazków (autor, tytuł pliku, licencja),
- co dodano **spoza materiału** i które dane sprawdzono w innych źródłach.

Na claude.ai dodaj jedno zdanie przypomnienia:
> Link z Claude otworzy tylko ktoś zalogowany do Claude (na koncie firmowym – tylko osoby z organizacji). Dla dzieci najlepiej wrzucić plik na własną stronę (patrz `references/strona.md`) albo otworzyć plik w przeglądarce – nie w podglądzie komunikatora, bo tam nic nie da się kliknąć.

Jeśli rodzic ma już stronę z aplikacjami, przypomnij, żeby po wrzuceniu nowego pliku odświeżył spis (`scripts/spis.py`) – albo wygeneruj mu nowy `index.html`.
