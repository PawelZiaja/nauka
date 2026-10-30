# Repozytorium „nauka”

Strona z aplikacjami do nauki na sprawdziany (szkoła podstawowa), publikowana przez GitHub Pages:
https://pawelziaja.github.io/nauka/  – login GitHub: **PawelZiaja**, gałąź `main`, katalog główny.

Do tworzenia i poprawiania aplikacji ZAWSZE używaj skilla `.claude/skills/nauka-na-sprawdzian`
(najpierw SKILL.md, potem `references/claude-code.md` – tam jest cały przebieg pracy w Claude Code).

## Struktura
- `klasa-X/przedmiot/temat.html` – aplikacja; obok `temat.json` – jej treść (poprawki rób w JSON i przebudowuj).
- `index.html` – spis wszystkich aplikacji, generowany przez `scripts/spis.py` ze skilla. Odświeżaj po każdej zmianie.
- Nazwy folderów i plików: małe litery, bez polskich znaków, myślniki. Dzieci są obecnie w klasie 5 i 7 (rok 2026/27).

## Pierwsze uruchomienie – gdy poproszę „przygotuj wszystko”
1. Sprawdź i doinstaluj narzędzia według `references/claude-code.md` (konfiguracja, punkty 1–3: Git, GitHub CLI, Python + Pillow, Node + jsdom w `~/.nauka-narzedzia`).
2. Sprawdź `gh auth status`. Jeśli nie jestem zalogowany – zatrzymaj się i poproś, żebym sam wpisał w terminalu `gh auth login` (GitHub.com → HTTPS → Login with a web browser), a potem `gh auth setup-git`. Nigdy nie proś o token ani hasło.
3. Przetestuj `klasa-5/polski/rzeczownik-przymiotnik.html` skryptem `test_aplikacji.js`.
4. Jeśli ten folder nie jest jeszcze repozytorium git: `git init -b main`, `git add .`, `git commit -m "Start strony z aplikacjami"`, `gh repo create nauka --public --source . --remote origin --push`. Jeśli repozytorium `nauka` już istnieje na GitHubie – zapytaj mnie, co zrobić.
5. Włącz GitHub Pages: `gh api -X POST repos/PawelZiaja/nauka/pages -f "source[branch]=main" -f "source[path]=/"` (jeśli już włączone – pomiń).
6. Podaj mi adres strony i aplikacji; po 1–2 minutach sprawdź `gh api repos/PawelZiaja/nauka/pages` (status „built”).

## Zasady
- Prośba o aplikację to zwykle jedno zdanie: tytuł sprawdzianu i/lub ścieżka do folderu ze zdjęciami. Klasę, wielkość puli, typy zadań, obrazki i mapy ustalasz sam według skilla (krok 0 w SKILL.md): krótka analiza i plan, potem od razu budowa – bez czekania na moją odpowiedź.
- Każda nowa aplikacja i każda poprawka idzie na stronę: zbuduj, przetestuj, odśwież spis, commit i push bez dodatkowego pytania. Na koniec podaj adres, liczby, kategorie i źródła obrazków.
- Repozytorium jest publiczne: bez imion i nazwisk dzieci, nazwy szkoły i skanów podręczników.
- Nie usuwaj plików i nie rób `push --force` bez mojej wyraźnej prośby.
