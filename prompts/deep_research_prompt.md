# 🔬 Research prompt (záloha, když agent nemá přístup na web)

Použij ho v režimu C ze `SKILL.md`: vyplň `[...]` a vlož do nástroje s hloubkovým researchem (NotebookLM Deep Research, Gemini, ChatGPT, Claude). Výslednou zprávu a seznam zdrojů přines zpět agentovi, ten ji zpracuje (extrakce tvrzení, jistota, mezery).

---

```markdown
Jsi výzkumník. Zpracuj hloubkovou rešerši, ze které se postaví kurz pro konkrétního studenta.

Téma a zúžení: [...]
Student: [úroveň, cíl, omezení, země]
Výzkumné otázky: [...]

Požadavky:
1. Používej přednostně primární zdroje (oficiální dokumentace, ceníky, zákony, studie) a praktiky, kteří ukazují postup a vlastní čísla. Marketing a seznamy typu „10 způsobů, jak vydělat" nepoužívej jako důkaz.
2. U každého klíčového tvrzení uveď zdroj (URL a datum). Čísla uváděj s datem, kontextem a informací, zda jsou svépomocná (self-reported).
3. U každé výzkumné otázky vyhledej i selhání, rizika a protiargumenty. Uveď, kde se zdroje rozcházejí.
4. Vyznač, co potvrzuje víc nezávislých zdrojů a co jen jeden. Co jsi nenašel, napiš jako otevřenou otázku. Nedoplňuj z odhadu.
5. Najdi 3 až 6 nejvěrohodnějších odborníků nebo praktiků, uveď proč jim věřit, jaký mají zájem (prodávají kurz?) a shrň jejich hlavní rámce. Přidej odkazy na jejich nejlepší dlouhé materiály (přednášky, podcasty, články).
6. Výstup: sekce podle výzkumných otázek, na konci seznam zdrojů s datem a tabulka tvrzení s jistotou (vysoká, střední, nízká, sporné).
```
