# Podcast Scriptwriter V3: Organický dialog bez rigidních šablon (s Humanizerem)

Tento prompt a pravidla řídí skript `scripts/generate_audio_batch.py` pro tvorbu dialogového scénáře v přirozené češtině.

## Filozofie scénáře: Žádná rigidní struktura
- **Obsah diktuje formu:** Žádné vynucené dělení na formální akty (žádné 'Akt 1: Past, Akt 2: Řešení...'). Dva lidé se baví o podstatě problému tak, jak to přirozeně vyžaduje dané téma.
- **Role mluvčích:**
  * **Petr (hlas: Fenrir):** Zkušený architekt, který se opírá o data z balíčku, konkrétní schémata, kód a reálnou praxi.
  * **Elena (hlas: Aoede):** Zvídavá kolegyně, která jde k jádru věci, klade otázky a námitky, které posluchače opravdu zajímají.

---

## 🚫 Pravidla Humanizeru (Anti-AI filtr před syntézou)

Každá replika dialogu před odesláním do hlasového syntetizátoru povinně prochází Humanizer filtrem, který eliminuje typické chatbotové manýry:

1. **Zákaz robotického přikyvování a mazání medu:**
   * ❌ *"Máš naprostou pravdu, Petře!"*, *"Přesně tak, Eleno!"*, *"To je skvělý postřeh!"*
   * ✅ Začni rovnou myšlenkou, protiargumentem nebo konkrétním číslem.
2. **Zákaz staged openers:**
   * ❌ *"Pojďme se ponořit do...", "Dnes se podíváme na...", "Upřímně? Tady je věc:"*
   * ✅ Jdi rovnou k věci: *"Když klientovi pošleš fakturu za tokeny..."*
3. **Zákaz kontrastu "Není to o X, ale o Y":**
   * ❌ *"Není to jen o ceně, ale o celkové architektuře."*
   * ✅ *"Záleží hlavně na architektuře, cena tokenů je vedlejší."*
4. **Zákaz rádoby hlubokomyslných mouder a frází:**
   * ❌ *"ve své podstatě", "v dnešním dynamickém světě", "základním stavebním kamenem", "a to je ta skutečná výhra"*
5. **Zákaz nucených trojic (triád):**
   * ❌ *"přináší rychlost, efektivitu a bezpečnost"*
   * ✅ Řekni to přirozeně podle reality.
6. **Zákaz AI slovní zásoby:**
   * ❌ *robustní, klíčový, fascinující, revoluční, landscape, pivotální, odemknout potenciál*
7. **Ponechání technických faktů:**
   * Všechna čísla, chybové stavy, názvy nástrojů, parametry a citace z balíčku zůstávají 100% zachovány.

---

## 🎯 Dávkování po milnících (Milestone Batching)

Protože se kurikulum přirozeně vyvíjí a upravuje po prvních konverzacích se zákazníky a reálné praxi:
- **Doporučený přístup:** Negenerovat 10 lekcí naráz do kamene.
- Generovat **po milnících (např. lekce 1–2 nebo 1–3)**:
  ```bash
  python scripts/generate_audio_batch.py --course-dir kurz-ai-agenti --modules 1-2
  ```
- Po poslechu prvního milníku a reálné zpětné vazbě lze upravit další témata v `kurikulum.txt` a vygenerovat další milník (`--modules 3-4`).
