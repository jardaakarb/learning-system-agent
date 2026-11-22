# Changelog

## v3 (Batch Audio Studio & Google Voice Engine)

**Cíl:** Odstranit vyčerpávající manuální generování audio lekcí po jedné v NotebookLM a nahradit ho plně automatizovaným dávkovým studiem přes Google Speech API s prémiovou přirozenou češtinou, 10–15 minutovými hloubkovými rozbory a automatickou kontinuitou.

### Co řeší v3
- **Odstranění frikce s NotebookLM:** Místo 45–60 minut ručního kopírování promptů do webového rozhraní NotebookLM, čekání na každou lekci a ručního stahování/nahrávání, V3 vygeneruje celou sérii 8–10 lekcí na pozadí jedním příkazem.
- **Konec plechových hlasů:** Žádný syntetický a nepřirozený Edge-TTS. V3 využívá Google Gemini Speech API (`models/gemini-2.5-flash-preview-tts` / Google Cloud TTS), kde hlasy **Petr (Fenrir)** a **Elena (Aoede)** mluví přirozenou, lidsky znějící češtinou s živou intonací, nádechy a reakcemi.
- **Délka 10–15 minut:** Skriptovací engine generuje plnohodnotné 4-aktové dialogy (1 400 až 2 200 slov na epizodu) s hloubkovým rozborem technických detailů, reálných failure modes, kódů a smluvních podmínek.
- **Automatická kontinuita bez halucinací:** Skriptovací engine si mezi moduly předává *Continuity Ledger* (shrnutí toho, co přesně zaznělo). Zákaz opakování metafor, vesnických příkladů či základních definic z minulých dílů.
- **Plná postprodukce přes FFmpeg:** Automatické slepování replik, vkládání mikropauz (350 ms mezi mluvčími), komprese do 192 kbps MP3 a generování textových Markdown transkriptů.
- **Zachování NotebookLM:** NotebookLM zůstává v dokumentaci i promtech plnohodnotně dostupný jako volitelná manuální alternativa (Fáze 7B).

---

## v2 (Research & Epistemic Rigor)

**Cíl:** kurikulum, které stojí na ověřených expertních informacích, ne na obecných znalostech modelu.

### Co je nové ve v2
- **Fáze 0:** kontrola schopností, režimy A, B, C, záložní postup bez webu.
- **Fáze 2:** mapa oboru a zúžení na jednu cestu.
- **Fáze 3:** výzkumné otázky jako hypotézy, zdroje úrovně A až D, pravidla nezávislosti, těžba expertů se zohledněním jejich zájmu, vlastní výpočty ekonomiky, red team, kolo mezer, kritéria konce, paralelizace přes subagenty.
- **Fáze 4:** modulární znalostní balíček, ledger tvrzení s jistotou, seznam zdrojů, povinné ověření vzorku tvrzení.
- **Fáze 5:** zpětný návrh kurikula (cíl, výstupní schopnost, cvičení, selhání, opora ve zdrojích), obecný Pre-Flight s doménovými čočkami.
- **Fáze 6:** NotebookLM Deep Research a Fast Research jako doplněk, videa přes YouTube zdroje, rozpočet zdrojů.
- **Fáze 7:** obecnější audio prompt s důrazem na poctivost, závěr s cvičením, zpětná vazba po lekci.
- **Fáze 9:** aktualizace rychle zastarávajících částí.
- Nové soubory: `references/`, `templates/knowledge_pack_template.md`, `prompts/deep_research_prompt.md`.
