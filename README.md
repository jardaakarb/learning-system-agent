# 🧠 Learning System Agent (Systém pro naučení čehokoliv)

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20Code%20%7C%20Antigravity%20%7C%20Cursor-purple)](https://github.com/jardaakarb/learning-system-agent)
[![Language](https://img.shields.io/badge/Language-%C4%8Ce%C5%A1tina-blue)](#)
[![Voice Engine](https://img.shields.io/badge/Voice%20Engine-Google%20Gemini%20Speech-red)](https://ai.google.dev)
[![Alternative Engine](https://img.shields.io/badge/Manual%20Engine-Google%20NotebookLM-green)](https://notebooklm.google.com)

> **Ověřený systém učení v uzavřené smyčce:** Původně vznikl jako záchranný systém, díky kterému se podařilo zvládnout **4 roky zanedbaného studia a 75 komplexních zkouškových otázek za méně než měsíc** a odmaturovat na jedničky a dvojky.
>
> Nyní zabalený do **jednoho agentního skillu**, který vás provede celým procesem od research přes kurikulum až po **automatické generování audio podcastů v češtině**.

**Verze 3:** Odstraňuje vyčerpávající manuální klikání v NotebookLM. Nové **Batch Audio Studio** vygeneruje celou sérii 10–15 minutových hloubkových lekcí naráz do MP3 přes Google Gemini Speech API s automatickou kontinuitou a živou lidskou češtinou. Přehled změn je v [CHANGELOG.md](CHANGELOG.md).

---

## ⚡ Jak tento repozitář použít

### Možnost 1: V Claude Code nebo Antigravity CLI
```bash
"Nainstaluj nebo spusť skill z https://github.com/jardaakarb/learning-system-agent"
```
Agent si načte [SKILL.md](SKILL.md), provede diagnostiku a research, připraví znalostní balíček a spustí dávkové audio studio.

### Možnost 2: V Cursor / Windsurf / GitHub Copilot
Přidejte odkaz na repo nebo zkopírujte obsah [SKILL.md](SKILL.md) do systémového kontextu (např. `.cursorrules`).

### Možnost 3: Přímo ve webovém chatu (ChatGPT, Claude, Gemini)
Zkopírujte text [SKILL.md](SKILL.md) a vložte ho jako první zprávu.

---

## 🔄 Jak celý proces funguje

```mermaid
flowchart TD
    A0["0. Kontrola schopností\n(plný research / omezený / bez webu)"] --> A["1. Diagnostika\n(téma, úroveň, cíl a omezení)"]
    A --> B["2. Mapa oboru a zúžení\n(z široké otázky na jednu konkrétní cestu)"]
    B --> C["3. Hloubkový research\n(otázky, zdroje A-D, experti, triangulace, red team, mezery)"]
    C --> D["4. Znalostní balíček + ověření tvrzení"]
    D --> E["5. User profile + kurikulum od cílových schopností"]
    E --> F["6. Příprava podkladů kurzu"]
    F --> G1["7A. Batch Audio Studio (V3 Doporučeno)\nGoogle Gemini Speech API + FFmpeg\nCelý kurz v MP3 naráz"]
    F -.-> G2["7B. Google NotebookLM (Alternativa)\nRuční generování lekcí"]
    G1 --> H["8. Bonus: kartičky"]
    G1 --> I["9. Aktualizace obsahu"]
```

---

## 🎙️ Verze 3: Batch Audio Studio

Už žádné čekání u webu NotebookLM a ruční přetahování promptů. Skript `scripts/generate_audio_batch.py`:
1. **Generuje hloubkové scénáře (10–15 min):** 4-aktové dialogy (Pasti & realita → Technický rozbor → Ostrý sparring → Akční krok), cca 1 400 až 2 200 slov na epizodu.
2. **Živá čeština bez syntetického plechu:** Moderátoři **Petr (hlas: Fenrir)** a **Elena (hlas: Aoede)** mluví přirozenou, lidskou češtinou přes Google Gemini Speech API.
3. **Automatická kontinuita:** Skript si předává *Continuity Ledger*. Modul 2 navazuje na modul 1 bez opakování základních definic, metafor či vesnických příkladů.
4. **Okamžitá postprodukce přes FFmpeg:** Vložení mikropauz (350 ms), normalizace a komprese do 192 kbps MP3.

### Použití:
```bash
# Vygenerování celého audio kurzu naráz
python scripts/generate_audio_batch.py --course-dir kurz-<téma> --duration 12

# Vygenerování konkrétního modulu
python scripts/generate_audio_batch.py --course-dir kurz-<téma> --duration 12 --module 1
```

---

## 📁 Struktura repozitáře

```
├── SKILL.md                          # Plná specifikace dovednosti (v3)
├── README.md                         # Tento průvodce
├── CHANGELOG.md                      # Historie verzí (v1 -> v2 -> v3)
├── scripts/
│   └── generate_audio_batch.py       # Dávkový generátor scénářů a MP3 podcastů
├── prompts/
│   ├── podcast_scriptwriter_v3.md    # 4-aktový prompt pro skriptovací engine
│   ├── audio_mentor_prompt.md        # Prompt pro manuální NotebookLM (fallback)
│   ├── flashcards_bonus_prompt.md    # Prompt pro kartičky
│   └── deep_research_prompt.md       # Záložní research prompt pro režim bez webu
├── references/
│   ├── research-playbook.md          # Šablony poznámek, ledger, vzory dotazů
│   └── domain-lenses.md              # Doménové čočky (byznys, tech, právo...)
└── templates/
    ├── user_profile_template.md
    ├── curriculum_template.md
    └── knowledge_pack_template.md
```

---

## 👤 Autor
Vytvořil **Jaroslav Karban** ([GitHub: @jardaakarb](https://github.com/jardaakarb)).
Systém postavený na reálných zkušenostech s rychlým studiem a moderními AI technologiemi.
