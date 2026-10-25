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
1. `git pull` w repozytorium.
2. Treść i obrazki przygotuj w `robocze/` (ignorowany przez git) – zdjęcia od rodzica mogą leżeć gdziekolwiek na dysku, poproś o ścieżkę.
3. Buduj prosto do docelowego miejsca: `python <skill>/scripts/buduj.py robocze/dane.json klasa-X/przedmiot/temat.html`
4. Test: `NODE_PATH=~/.nauka-narzedzia/node_modules node <skill>/scripts/test_aplikacji.js klasa-X/przedmiot/temat.html` (PowerShell: `$env:NODE_PATH="$HOME\.nauka-narzedzia\node_modules"`).
5. Spis: `python <skill>/scripts/spis.py . "Nauka na sprawdziany"`.
6. Zachowaj plik treści w repozytorium obok aplikacji jako `temat.json` (ułatwia późniejsze poprawki) – ale tylko jeśli nie zawiera ścieżek do prywatnych plików; obrazki są już w HTML.
7. `git add` → `git commit -m "Klasa X, przedmiot: temat"` → `git push`. Jeśli rodzic poprosił o wrzucenie na stronę – wypchnij od razu; jeśli tylko o zrobienie aplikacji – pokaż listę zmian i zapytaj.
8. Podaj adres: `https://<login małymi literami>.github.io/nauka/klasa-X/przedmiot/temat.html` (strona odświeża się 1–2 minuty).

## Poprawki
Edytuj `temat.json` (nie HTML), przebuduj, przetestuj, commit i push. Nie zmieniaj `config.klucz` – postęp dzieci zostaje.

## Zasady
- Repozytorium jest publiczne: bez imion dzieci, nazwy szkoły i skanów podręczników (patrz `obrazy.md`).
- Nie usuwaj plików ani nie przepisuj historii (`push --force`) bez wyraźnej prośby.
