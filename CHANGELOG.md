# Changelog

## v2

**Cíl:** kurikulum, které stojí na ověřených expertních informacích, ne na obecných znalostech modelu.

### Příčiny slabých kurikul ve v1
1. Fáze 1.5 závisela na třech cizích skillech. Když chyběl, nic nehlídalo, že research neproběhl, a agent mohl psát z hlavy.
2. Kritérium researche byla délka (3 000 až 8 000 slov), ne kvalita: žádné hodnocení zdrojů, žádné křížové ověření, žádné citace.
3. Obsah researche byl předem daný (spolehlivost, GDPR, retainery…), takže research jen potvrzoval hotovou osnovu. Pravidla byla navíc napsaná pro jedno téma (AI agentury) a špatně se hodila na ostatní.
4. Široké téma se nezužovalo. „Vydělat na AI agentech" je několik odlišných cest.
5. Kurikulum byl seznam témat bez cílové schopnosti, cvičení a opory ve zdrojích.
6. Audio prompt obsahoval příklady z jednoho tématu a tvrdil délku, kterou NotebookLM nemusí dodržet.

### Co je nové
- **Fáze 0:** kontrola schopností, režimy A, B, C, záložní postup bez webu.
- **Fáze 2:** mapa oboru a zúžení na jednu cestu.
- **Fáze 3:** výzkumné otázky jako hypotézy, zdroje úrovně A až D, pravidla nezávislosti, těžba expertů se zohledněním jejich zájmu, vlastní výpočty ekonomiky, red team, kolo mezer, kritéria konce, paralelizace přes subagenty.
- **Fáze 4:** modulární znalostní balíček, ledger tvrzení s jistotou, seznam zdrojů, povinné ověření vzorku tvrzení.
- **Fáze 5:** zpětný návrh kurikula (cíl, výstupní schopnost, cvičení, selhání, opora ve zdrojích), obecný Pre-Flight s doménovými čočkami.
- **Fáze 6:** NotebookLM Deep Research a Fast Research jako doplněk, videa přes YouTube zdroje, rozpočet zdrojů.
- **Fáze 7:** obecnější audio prompt s důrazem na poctivost, závěr s cvičením, zpětná vazba po lekci.
- **Fáze 9:** aktualizace rychle zastarávajících částí.
- Nové soubory: `references/`, `templates/knowledge_pack_template.md`, `prompts/deep_research_prompt.md`.

### Co zůstalo
Celý tok s NotebookLM, lekce po jedné s trikem nahrání minulé lekce do zdrojů, kartičky jako bonus, čeština, anti-hype postoj (teď jako obecné pravidlo místo vázaného na jedno téma). Doménová znalost z v1 o AI agenturách je zachována jako příklad hypotéz v `references/domain-lenses.md`.
