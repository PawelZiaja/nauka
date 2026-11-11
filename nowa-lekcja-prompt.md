# Nowa lekcja w czystym czacie Claude

Jak używać: otwórz nowy czat na claude.ai i wklej cały tekst spod kreski.
Lista „Already covered” to stan strony lekcja-dnia.netlify.app na 11.11.2026. Po każdej nowej lekcji dopisz jej tytuł do listy (albo poproś Claude Code o odświeżony plik).
Wynik (JSON) dołącz w Claude Code razem z tekstem z `aktualizacja-lekcji-prompt.md`; strona go dołączy do reszty.

---

You write one daily micro-learning lesson for Paweł: a Polish product owner of EV fleet charging software and an electrical design engineer. He reads English at C1 level and wants to grow his vocabulary. The lesson will also be read by his family and friends.

Today's date: [WPISZ DATĘ RRRR-MM-DD]

Lesson type depends on the date: 2026-11-11 is a BOOK day and the type alternates every day after that (an even number of days after 2026-11-11 → BOOK, odd → CURIOSITY). Work out the type for today's date and say it in one line before the JSON.

- BOOK lesson: pick one book from this list that is NOT in the "Already covered" list: Inspired (Marty Cagan); Continuous Discovery Habits (Teresa Torres); Shape Up (Ryan Singer); Crossing the Chasm (Geoffrey Moore); Good Strategy Bad Strategy (Richard Rumelt); Thinking, Fast and Slow (Daniel Kahneman); Never Split the Difference (Chris Voss); Influence (Robert Cialdini); Crucial Conversations (Patterson et al.); Atomic Habits (James Clear); Deep Work (Cal Newport); The Psychology of Money (Morgan Housel). If all are covered, pick another well-known nonfiction book valuable for a product owner, engineer or salesperson. Explain the book's key ideas entirely in your own words. Do not quote the book.
- CURIOSITY lesson: one surprising, well-documented topic from history, science, engineering, energy, economics or psychology, explained so the reader understands the "why", not just the fact.

Already covered (do not repeat the book, the topic, or a close variant of it):
- 2026-11-05, book: The Mom Test (Rob Fitzpatrick)
- 2026-11-06, book: The Goal (Eliyahu Goldratt)
- 2026-11-07, curiosity: Why Europe runs on 50 Hz and America on 60 Hz (history of grid frequency standards, path dependence)
- 2026-11-08, curiosity: When Electric Cars Ruled the Road (early electric cars, the electric starter, Model T, network effects)

Requirements:
- 650 to 850 words across 4 or 5 sections, natural C1 English: idiomatic, precise, varied, never padded.
- Each section body is 1 to 3 paragraphs separated by a blank line (\n\n). Add a practical angle where it fits (work, product, engineering, everyday life).
- vocab: exactly 6 advanced (C1/C2) words or phrasal expressions that appear VERBATIM in the section text, in the same form. Give an English definition, a Polish translation and a NEW example sentence.
- quiz: exactly 3 multiple-choice questions on the lesson's ideas, 4 options each, one correct; "answer" is the 0-based index; "explanation" is one sentence.
- Before answering, check that each vocab "word" really appears verbatim in a section body.

Reply with the type line, then only this JSON object in one code block (fill in today's date in both places):
{"exportedAt":"RRRR-MM-DD","lessons":[{"date":"RRRR-MM-DD","kind":"book|curiosity","title":"lesson title (for a book: the book title)","author":"author for a book, empty string otherwise","hook":"one or two sentences that make the reader want to read","sections":[{"heading":"...","body":"..."}],"takeaway":"one or two sentences to remember","vocab":[{"word":"...","pos":"noun|verb|adjective|adverb|phrase","definition":"...","pl":"...","example":"..."}],"quiz":[{"question":"...","options":["...","...","...","..."],"answer":0,"explanation":"..."}]}]}
