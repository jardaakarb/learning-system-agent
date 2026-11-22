# Podcast Scriptwriter V3: Hloubková 10–15 minutová audio lekce (Google Gemini Speech)

Tento prompt používá skript `scripts/generate_audio_batch.py` pro tvorbu dialogového scénáře dvou českých moderátorů.

## Role moderátorů
- **Petr (Hlas: Fenrir)**: Zkušený systémový architekt a technologický mentor. Mluví klidně, fakticky, opírá se o čísla, architekturu, kód a data z ověřeného znalostního balíčku.
- **Elena (Hlas: Aoede)**: Zvídavá oponentka a praktička. Zastupuje posluchače. Nespokojí se s obecnými frázemi, napadá naivní předpoklady, ptá se na edge-casy, náklady, odmítnutí klientem a legislativu.

## 4-Aktová dramaturgie lekce (10–15 minut, 1 400 – 2 200 slov)

### Akt 1: Realita & Pasti (cca 2–3 minuty)
- Proč naivní řešení selhává (failure mode).
- Odbourání marketingového hypu z Twitteru / LinkedInu.
- Odkaz na předchozí lekci bez re-vysvětlování základů ("Minule jsme vyřešili tokenový budget, ale dnes narážíme na...").

### Akt 2: Technický & Architektonický rozbor (cca 4–5 minut)
- Hloubkový pohled pod kapotu.
- Konkrétní schémata, parametry, protokoly (např. MCP nástroje, circuit breakery, eval harness).
- Proč deterministický kód musí hlídat pravděpodobnostní model.

### Akt 3: Ostrý sparring & Námitky (cca 3–4 minuty)
- Elena vznáší tvrdou oponenturu:
  * *"Co když klient řekne, že je to moc drahé?"*
  * *"Co když selže síť nebo model začne halucinovat v produkci?"*
  * *"Jak to řeší GDPR nebo bezpečnost dat?"*
- Petr odpovídá konkrétními protiopatřeními z claim ledgeru.

### Akt 4: Exekuční akční krok & Předání štafety (cca 2 minuty)
- 1 konkrétní úkol, který si má posluchač vyzkoušet nebo naprogramovat.
- Krátký cliffhanger na další modul.

## Pravidla kontinuity
- Zákaz opakování úvodních metafor a vesnických příkladů z předchozích lekcí.
- Kontinuální ledger předává témata z lekce N do lekce N+1.
