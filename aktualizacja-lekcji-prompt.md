# Aktualizacja lekcji na lekcja-dnia.netlify.app

Jak używać: w nowej sesji Claude Code dołącz plik `lessons.json` z aplikacji i wklej tekst spod kreski.
Bez pliku (np. „usuń lekcję z 5 listopada”) zamień pierwsze zdanie na swoją prośbę.

---

Zaktualizuj lekcje na stronie lekcja-dnia.netlify.app. Dołączam lessons.json z mojej aplikacji w Claude.

Kontekst:
- Strona statyczna na Netlify, projekt "lekcja-dnia" (site id 252925fa-3c1d-410d-bfed-abd659b17149). Token jest w zmiennej NETLIFY_AUTH_TOKEN. Git nie działa, więc nie używaj repozytorium.
- Aktualne pliki (index.html, lessons.json, _headers, robots.txt) pobierz z bieżącego wdrożenia przez API Netlify (/sites/{id}/files). Niczego nie generuj od nowa.
- Format: { "exportedAt": "...", "lessons": [...] }, każda lekcja ma pola date (RRRR-MM-DD), kind (book/curiosity), title, author, hook, sections, takeaway, vocab, quiz.

Zasady:
- ŁĄCZ, nie podmieniaj: lekcje z mojego pliku dopisz do tych, które są na stronie. Ta sama data oznacza, że moja wersja zastępuje starą. Niczego nie usuwaj bez mojej prośby (przykładowe lekcje też zostają).
- Sprawdź każdą nową lekcję: słówka występują w tekście, quiz ma 3 pytania, nie ma pól box/due/answers. Jeśli coś jest nie tak, powiedz mi przed wdrożeniem.
- Wdróż przez Netlify CLI: netlify link --id <site id>, potem netlify deploy --prod --dir . (z NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt).
- Na koniec napisz w punktach, które lekcje doszły lub się zmieniły, i podaj linki do nich.

Nie zmieniaj index.html ani wyglądu strony, chyba że o to poproszę.
