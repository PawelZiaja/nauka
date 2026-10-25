# Udostępnienie aplikacji bez Claude

**Ważne:** link do artefaktu w Claude otworzy tylko osoba z kontem Claude. Na koncie firmowym (Team/Enterprise) – zwykle tylko osoby z tej organizacji. Dzieci bez konta go nie otworzą. Rozwiązaniem jest plik HTML z tej aplikacji: jest samodzielny (obrazki w środku), więc działa na każdej zwykłej stronie.

## Opcja 1: GitHub Pages (polecana – darmowa, stała, jeden adres na wszystko)
Jednorazowo:
1. Załóż konto na github.com.
2. Utwórz nowe repozytorium, np. `nauka`, ustaw jako **Public** (darmowe Pages wymaga publicznego).
3. W repozytorium: Settings → Pages → Source: „Deploy from a branch”, branch `main`, folder `/ (root)` → Save.

Za każdym razem:
Struktura folderów: `klasa-5/polski/temat.html`, `klasa-7/historia/temat.html` (małe litery, bez polskich znaków, myślniki). Klasa = klasa, w której był materiał – za rok młodsze dziecko skorzysta z folderu starszego.

Za każdym razem:
4. Oddaj rodzicowi plik ZIP z gotową strukturą: `klasa-X/przedmiot/temat.html` + zaktualizowany `index.html` w katalogu głównym. Żeby spis był pełny, odtwórz w `/home/claude/strona/` wszystkie dotychczasowe aplikacje (pliki są w poprzednich rozmowach / w outputs – jeśli ich nie masz, poproś rodzica o listę adresów albo dopisz nową pozycję do jego obecnego `index.html`, który może wrzucić), dodaj nową i uruchom `scripts/spis.py /home/claude/strona`.
5. Rodzic rozpakowuje ZIP i w repozytorium: Add file → Upload files → przeciąga **zawartość** rozpakowanego folderu (folder `klasa-X` i `index.html`) → Commit changes. Przeciąganie folderu zachowuje strukturę (Chrome/Edge). GitHub nie rozpakowuje ZIP-ów sam.
6. Po 1–2 minutach: `https://<login>.github.io/nauka/klasa-X/przedmiot/temat.html`, spis: `https://<login>.github.io/nauka/`. W domenie login jest małymi literami.

Uwagi:
- Strona jest publiczna dla każdego, kto zna adres (aplikacje mają znacznik „noindex”, więc nie trafią do wyszukiwarki). Nie wpisuj w treści imion ani nazwisk dzieci, nazwy szkoły itp.
- Bez skanów podręczników na stronie publicznej (prawa autorskie – patrz `obrazy.md`).
- Postęp dziecka zapisuje się w jego przeglądarce osobno dla każdej aplikacji; aktualizacja pliku (ten sam `klucz`) go nie kasuje.

## Opcja 2: Netlify Drop (najszybsza na próbę)
Wejdź na app.netlify.com/drop i przeciągnij folder z plikami (plik musi się nazywać `index.html`, jeśli to jedyny). Dostajesz adres od razu; żeby strona nie wygasła, trzeba założyć darmowe konto.

## Opcja 3: własny serwer / NAS
Jeśli rodzic ma serwer lub NAS z serwerem WWW – wystarczy wrzucić pliki do katalogu strony. Dostęp spoza domu wymaga już przekierowania portów lub tunelu (np. Cloudflare Tunnel) – to opcja dla kogoś, kto takie rzeczy już robi.

## Opcja 4: sam plik
Wysłany plik trzeba **zapisać i otworzyć w przeglądarce** (Chrome na Androidzie). W podglądzie komunikatora (WhatsApp, Messenger) nic nie da się kliknąć. Na iPhonie otwieranie lokalnych plików HTML jest kłopotliwe – tam lepsza strona.
