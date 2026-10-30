# Praca w Claude Code (komputer rodzica + repozytorium GitHub)

W Claude Code nie ma narzędzia Artifact – aplikacje trafiają prosto do repozytorium `nauka`, które GitHub Pages wystawia jako stronę.

## Jednorazowa konfiguracja (gdy rodzic poprosi „przygotuj środowisko”)
Sprawdź po kolei i doinstaluj tylko to, czego brakuje (Windows: `winget install --id <id> -e`; macOS: `brew install`):
1. Git (`Git.Git`), GitHub CLI (`GitHub.cli`), Python 3 (`Python.Python.3.12`), Node.js LTS (`OpenJS.NodeJS.LTS`). Po instalacji może być potrzebne nowe okno terminala.
2. `python -m pip install pillow`
3. Narzędzia testowe poza repozytorium: `mkdir ~/.nauka-narzedzia && cd ~/.nauka-narzedzia && npm init -y && npm i jsdom@24`.
4. Logowanie do GitHuba robi **rodzic sam**: poproś, żeby w terminalu wpisał `gh auth login` (GitHub.com → HTTPS → Login with a web browser), a potem `gh auth setup-git`. Nigdy nie proś o token ani hasło w czacie.
5. Repozytorium: jeśli `gh repo view nauka` działa – `gh repo clone <login>/nauka`. Jeśli nie istnieje – zapytaj, czy je utworzyć, i wtedy: `gh repo create nauka --public --add-readme --clone`.
6. GitHub Pages: `gh api repos/<login>/nauka/pages` – jeśli 404, włącz: `gh api -X POST repos/<login>/nauka/pages -f "source[branch]=main" -f "source[path]=/"`.
7. Dodaj do repozytorium `.gitignore` z `node_modules/`, `*.zip`, `robocze/`.

## Każda nowa aplikacja
Rodzic podaje zwykle jedno zdanie (tytuł i/lub ścieżkę do folderu ze zdjęciami) – resztę ustalasz sam według `SKILL.md` (krok 0).
1. `git pull` w repozytorium.
2. Zdjęcia od rodzica mogą leżeć gdziekolwiek na dysku (np. `Downloads\Photos-…`). Zmniejszone kopie do oglądania i pobrane pliki z sieci trzymaj w katalogu tymczasowym (scratchpad), każde pobranie w osobnym folderze. Generator (`gen.py`), `dane.json` i gotowe obrazki – w `robocze/<przedmiot>/` (ignorowany przez git). **Żadnych stron podglądu ani plików HTML w `robocze/` ani nigdzie w repozytorium** poza samymi aplikacjami.
3. W generatorze wklejaj obrazki od razu jako `data:` URI (SVG – base64; zdjęcia i mapy – zmniejszone do 1100 px JPEG), żeby `temat.json` w repozytorium był samodzielny i dał się przebudować bez folderu `robocze`.
4. Buduj prosto do docelowego miejsca: `python <skill>/scripts/buduj.py robocze/<przedmiot>/dane.json klasa-X/przedmiot/temat.html`. Na Windows uruchamiaj Pythona z `-X utf8` (inaczej komunikaty z polskimi znakami i emoji wywracają skrypt).
5. Test: `NODE_PATH=~/.nauka-narzedzia/node_modules node <skill>/scripts/test_aplikacji.js klasa-X/przedmiot/temat.html` (PowerShell: `$env:NODE_PATH="$HOME\.nauka-narzedzia\node_modules"`, ścieżki bezwzględne). Potem przejrzyj losowe 20–30 pytań.
6. Spis: `python <skill>/scripts/spis.py . "Nauka na sprawdziany"` (pomija `robocze/`, `node_modules/` i ukryte foldery). Sprawdź w `index.html`, że nie ma pozycji „Klasa ?”.
7. Zachowaj plik treści w repozytorium obok aplikacji jako `temat.json` – sprawdź, że nie zawiera ścieżek do prywatnych plików (`grep -c "Downloads\|pawel"` → 0).
8. `git add` (tylko aplikacja, jej JSON i `index.html`) → `git commit -m "Klasa X, przedmiot: temat"` → `git push` – **bez pytania** (tak ustalił rodzic w `CLAUDE.md`).
9. Poczekaj na build GitHub Pages (`gh api repos/<login>/nauka/pages/builds/latest --jq .status` → `built`) i sprawdź, że adres odpowiada (`curl -s -o /dev/null -w "%{http_code}"` → 200).
10. Raport według `SKILL.md`, krok 7, z adresem `https://<login małymi literami>.github.io/nauka/klasa-X/przedmiot/temat.html`.

## Poprawki
Edytuj `temat.json` (nie HTML), przebuduj, przetestuj, commit i push. Nie zmieniaj `config.klucz` – postęp dzieci zostaje.

## Zasady
- Repozytorium jest publiczne: bez imion dzieci, nazwy szkoły i skanów podręczników (patrz `obrazy.md`).
- Nie usuwaj plików ani nie przepisuj historii (`push --force`) bez wyraźnej prośby.
