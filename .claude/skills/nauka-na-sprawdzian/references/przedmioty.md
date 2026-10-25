# Przedmioty – typy zadań, sprawdzanie, pułapki

Tryby sprawdzania wpisów (`tryb` w pytaniu lub `config.tryb`):
- `luzno` – wybacza brak polskich liter i drobne literówki (1 błąd do 9 liter, 2 przy dłuższych; słowa do 4 liter muszą być dokładne). Dla pojęć, nazw, faktów.
- `koncowka` – jak `luzno`, ale ostatnie `k` liter każdego wyrazu (domyślnie 2) musi być dokładne, łącznie z polskimi znakami. Dla form gramatycznych, gdzie końcówka niesie znaczenie.
- `scisle` – dokładnie (wielkość liter ignorowana, chyba że `cs: true`). Gdy sprawdzana jest sama pisownia.
- `zle` – lista błędnych odpowiedzi, które trzeba odrzucić, nawet jeśli mieszczą się w tolerancji (np. inna forma różniąca się jedną literą). Dodawaj zawsze, gdy literówka może dać inną poprawną formę.

Zasada nadrzędna: tolerancja nie może zaliczyć odpowiedzi, która jest **inną** formą lub innym pojęciem.

## Język polski
- Odmiana (przypadki, osoby, czasy): `in` z `tryb: koncowka`; `mc` „uzupełnij zdanie”; rozpoznawanie formy w zdaniu.
- Części mowy, części zdania: `pick` (zaznacz w zdaniu), `mc`.
- Ortografia (ó/u, rz/ż, ch/h, „nie” razem/osobno, wielka/mała litera): **`gap`** z dwiema–trzema opcjami albo `mc` z dwoma zapisami zdania. Nigdy `in` w trybie `luzno` – tolerancja zaliczyłaby błąd ortograficzny.
- Obrazki: obrazy omawiane na lekcji (opis obrazu, środki wyrazu, autor, tytuł) – `img` + `mc`, `spot` (wskaż na obrazie), fiszki z obrazem na przodzie.
- Lektury: fakty o fabule, bohaterach, czasie i miejscu akcji – sprawdzaj, nie zgaduj. Bez cytowania dłuższych fragmentów.
- Pułapki: synkretyzm form (kota = D. i B.), wyrazy o nietypowym rodzaju (kolega, mysz, muzeum), wyjątki ortograficzne.

## Matematyka
- Obliczenia: `num` (przyjmuje 0,5 / 0.5 / 1/2 / 1 1/2; `tol` dla przybliżeń; `jedn` wyświetla jednostkę obok pola).
- Gdy liczy się postać zapisu („podaj w postaci ułamka nieskracalnego”, „zapisz w notacji wykładniczej”) – `in` z `tryb: scisle` i wariantami zapisu, bo `num` przyjmie każdą równą wartość.
- Zadania wieloetapowe: `multi` z polami na kolejne kroki (każde pole może mieć `num: true`).
- Geometria: narysuj figurę jako SVG z wymiarami (`references/obrazy.md`) albo użyj zdjęcia rysunku z zeszytu; wymiary podaj też w treści.
- Prawda/fałsz dla własności (np. „każdy kwadrat jest prostokątem”), `match` dla wzorów i nazw.
- Pułapki: kolejność działań, jednostki (cm vs cm²), zaokrąglenia – podaj w treści, z jaką dokładnością.

## Angielski i niemiecki
- **Dużo fiszek: 80–200.** Słówka i zwroty z działu, każdy z `dwa: true` (losowy kierunek: pl→obcy i obcy→pl), `lang` po stronie obcej i `config.mowa` (`en-GB` / `de-DE`) – przycisk 🔊 czyta wymowę. Dziel tagami na tematy (np. „Jedzenie”, „Czasowniki”), bo aplikacja pozwala uczyć się wybranego zestawu. W `w` – przykładowe zdanie.
- Słówka w obie strony: `in` z `tryb: scisle` (pisownia jest sprawdzana), z wariantami (`dog`, `a dog`; `do not`, `don't`).
- Gramatyka: `gap` (wybór formy: was/were, der/die/das, am/is/are), `multi` (odmiana czasownika przez osoby), `mc`.
- Niemiecki: rzeczowniki z rodzajnikiem (`der Hund`) i `cs: true`, gdy sprawdzana jest wielka litera rzeczownika. Umlauty są częścią pisowni – warianty „ae/oe/ue” dodaj tylko, jeśli nauczyciel je uznaje.
- Polecenia po polsku (dla klas 4–6 obowiązkowo), przykłady w języku obcym.
- Pułapki: czasowniki nieregularne, liczba mnoga nieregularna, false friends.

## Historia
- Chronologia: **`order`** (3–6 wydarzeń) – najlepszy typ do historii.
- Daty: `num` (rok, `tol: 0`); wieki rzymskie: `in` `scisle` („XIV”, warianty „14”, „XIV wiek”).
- Postacie ↔ wydarzenia, pojęcia ↔ definicje: `match`.
- Przyczyny i skutki: `mc`, `tf`.
- Obrazki: zabytki, przedmioty, obrazy historyczne, mapy – „co przedstawia?”, „z jakiej epoki?”, `spot` na mapie. Fiszki z obrazem na przodzie.
- **Każdą datę i fakt weryfikuj** (podręcznik/sieć) – błędna data to najgorszy możliwy błąd w takiej aplikacji.

## Biologia
- Pojęcia i definicje (`in` `luzno`, `mc`), budowa i funkcje (`match`), klasyfikacja (`pick` w zdaniu, `mc`), procesy krok po kroku (`order`), `tf` dla mitów i faktów.
- Obrazki: schematy budowy (komórka, kwiat, serce) – `spot` („wskaż mitochondrium”) i fiszki z obrazem.
- Pułapki: nazwy podobne (mitochondrium/chloroplast), wyjątki w klasyfikacji (wieloryb – ssak).

## Geografia
- Stolice, rzeki, góry: `in` `luzno` z wariantami nazw; położenie: `mc`; dane liczbowe: `num` z `tol`.
- Mapy: zdjęcie mapy z atlasu/podręcznika (od rodzica) + `spot` („wskaż na mapie…”) i `mc` z obrazkiem. Bez mapy pytaj o położenie słowami.
- Dane statystyczne (ludność, wysokości) sprawdzaj i zaokrąglaj jak w podręczniku.

## Fizyka
- Obliczenia: `num` z `jedn` i rozsądnym `tol`; zadania z kilkoma krokami: `multi`.
- Wzory i jednostki: `match`, `mc`; zamiana jednostek: `multi` z polami `num`.
- Symbole wielkości i jednostek: `in` `scisle` z `cs: true` (m ≠ M, s ≠ S).
- Obrazki: schematy obwodów, wykresy zależności – SVG lub zdjęcie z podręcznika.
- Pułapki: jednostki pochodne, przedrostki (mili/mega), kierunek wektorów w zadaniach słownych.

## Chemia
- Symbole pierwiastków i wzory: `in` `scisle` z `cs: true` (Co ≠ CO). Indeksy dolne: uczeń może wpisać „H2O” lub „H₂O” – oba są przyjmowane; w treści używaj „H₂O”.
- Bilansowanie równań: `multi` z polami na współczynniki (`num: true`), a nie wpisywanie całego równania.
- Wartościowość, nazwy związków: `in` (nazwy `luzno`), `match` (wzór ↔ nazwa).
- Właściwości i zastosowania: `mc`, `tf`.
- Obrazki: modele cząsteczek, sprzęt laboratoryjny („jak nazywa się to naczynie?”), układ okresowy – zdjęcie lub SVG.
