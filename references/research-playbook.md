# 🔬 Research Playbook

Podrobnosti ke Fázi 3 a 4 v `SKILL.md`. Otevři, když potřebuješ šablonu nebo vzory dotazů.

---

## 1. Složka kurzu

```
kurz-<téma>/
├── 00-brief.md
├── poznamky/
│   ├── vo-01-<téma>.md      # poznámky ke každé výzkumné otázce (VO)
│   ├── experti.md
│   ├── videa.md             # seznam videí pro NotebookLM
│   └── mezery.md
├── balicek/                 # to se nahrává do NotebookLM
│   ├── 00-prehled.md
│   ├── t01-<téma>.md ...
│   ├── ledger.md
│   └── zdroje.md
├── user.txt
├── curriculum.txt
└── notebooklm-dotazy.md     # výzkumné otázky pro slabé moduly
```

---

## 2. Formát poznámky ke zdroji

```markdown
### S12: <název>
- URL: ...
- Autor: ... | Datum: ... | Úroveň: A / B / C / D
- Zájem autora: prodává kurz / nástroj / žádný zjevný
- Typ: dokumentace / ceník / studie / write-up / přednáška / diskuze
- Výňatky:
  1. [tvrzení nebo číslo, přesně co zdroj říká] (kde: sekce či čas)
  2. ...
- Použitelnost: co z toho jde použít a s jakou výhradou
```

Čísla vždy s kontextem: `1 200 USD/měs (self-reported, 1 klient, 2026-03)`.

---

## 3. Ledger tvrzení

| ID | Tvrzení | Jistota | Zdroje | Poznámka |
|---|---|---|---|---|
| C01 | ... | Vysoká | S3 (A), S7 (B), S9 (B) | |
| C02 | ... | Sporné | S4 říká X, S11 říká Y | Rozdíl asi v měřítku |

Jistota: Vysoká, Střední, Nízká, Sporné. Definice v `SKILL.md`, část 3.2.

---

## 4. Vzory dotazů

| Cíl | Vzory |
|---|---|
| Primární fakta | `<produkt> pricing`, `<produkt> documentation limits`, `<zákon> text`, `<téma> filetype:pdf study` |
| Postup od praktiků | `<téma> case study numbers`, `how I built <téma>`, `<téma> architecture walkthrough`, `<téma> github` |
| Selhání | `<téma> lessons learned`, `<téma> postmortem`, `<téma> what went wrong`, `I quit <téma>`, `<téma> scam` |
| Komunita | `<téma> site:reddit.com`, `<téma> site:news.ycombinator.com` |
| Přednášky a podcasty | `<téma> talk transcript`, `<kdo> podcast <téma>`, `<téma> conference` |
| Aktuálnost | `<téma>` + aktuální měsíc a rok, `<téma> changelog`, `<téma> announcement` |
| Právo a rizika | `<téma> GDPR`, `<téma> liability`, `<téma> regulation <země>`, `<téma> terms of service` |
| Lokální trh | stejné dotazy v jazyce trhu + `<země>` |

Tipy: když dotaz vrací jen marketing, přidej slova, která marketing nepoužívá (`postmortem`, `limits`, `unit economics`, `I tried`). Když najdeš dobrý zdroj, projdi, koho cituje a kdo cituje jeho.

---

## 5. Zadání pro subagenta

```markdown
Úkol: Zodpověz tyto výzkumné otázky a zapiš poznámky.
VO: [seznam 2–3 otázek]
Rozsah kurzu: [z 00-brief.md]
Pravidla zdrojů: úrovně A–D, klíčové tvrzení potřebuje 1× A nebo 2× nezávislé B. Cituj jen to, co jsi opravdu otevřel a přečetl. Nevymýšlej čísla ani URL.
Pro každou VO: aspoň 4 různé dotazy, primární zdroje první, aspoň jedno hledání selhání a protiargumentů.
Formát: poznámky ke zdroji podle šablony, uložit do poznamky/vo-XX-<téma>.md
Vrať: cestu k souboru, shrnutí max 10 řádků, seznam mezer a sporů.
```

---

## 6. Test nasycení

Po každém kole si polož tři otázky:
1. Přinesla poslední 3 hledání nějaký nový fakt, zdroj, nebo spor? Když ne, je to nasycené.
2. Má každá VO aspoň 3 použitelné zdroje, z toho jeden A či B?
3. Je u každého klíčového tvrzení jistota a není žádné opřené jen o C nebo D?

---

## 7. Hlídač zdrojů (rychlá kontrola)

- Prodává autor to, o čem píše? (zapiš, nevyřazuj automaticky)
- Ukazuje postup a čísla, nebo jen výsledky?
- Je to datované a nezastaralé?
- Cituje primární zdroje?
- Je to jediný zdroj tohoto tvrzení?
- Slibuje výsledky bez podmínek? (červená vlajka, úroveň D)
