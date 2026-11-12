# 🔍 Doménové čočky

Přidávají se k základním čočkám ze `SKILL.md` (mechanismus, postup, čísla, selhání, rizika, cesta od nuly, aktuálnost). Vyber podle typu tématu. Kontrolní body slouží i pro Pre-Flight kurikula.

---

## Byznys a výdělek
Výzkumné otázky navíc:
- Jaká je jednotková ekonomika (náklady, cena, marže) spočítaná z primárních dat?
- Jaké jsou base rates: kolik lidí, kteří to zkusili, uspělo, a jak se to liší od toho, co se prezentuje?
- Jak získat prvního zákazníka bez referencí a jak změřit výsledek, aby šel použít jako důkaz?
- Co říká právo a daně v zemi studenta (smlouvy, odpovědnost, ochrana dat)?

Kontrola:
- [ ] žádný příjmový slib, jen tvrzení s kontextem
- [ ] každé číslo má vzorec nebo zdroj a datum
- [ ] je tam survivorship bias a základní míra neúspěchu (nebo poznámka, že data chybí)
- [ ] cesta od nuly je realistická (první klient, první reference)
- [ ] právní a daňové minimum

## Technika a programování
- Co funguje v aktuální verzi? Jaké jsou známé limity, ceny, bezpečnostní rizika?
- Jak se to testuje a jak poznám, že to nefunguje?
Kontrola:
- [ ] ke každému modulu funkční příklad nebo cvičení
- [ ] verze a datum ověření
- [ ] způsoby selhání a jak je odhalit (testy, logy, limity)
- [ ] bezpečnost a data

## Akademické téma, zkouška
- Co přesně se zkouší? Jaké jsou typické otázky a typické chyby?
- Jaká je standardní terminologie a výklad v oficiálních materiálech?
Kontrola:
- [ ] kurikulum kopíruje sylabus nebo zkouškové okruhy
- [ ] každý modul se mapuje na konkrétní otázky
- [ ] klíčové pojmy a běžné záměny
- [ ] vlastní materiály uživatele mají přednost před obecnými zdroji

## Rychle se měnící obor
- Co se změnilo za 90 dní? Které zdroje jsou starší než rok a stále platí?
Kontrola:
- [ ] u každého tvrzení datum
- [ ] preferovány primární zdroje (dokumentace, changelog)
- [ ] rychle se měnící části označené, aby šly v Fázi 9 aktualizovat

## Zdraví, právo, finance
- Co říkají oficiální směrnice, zákony, regulátoři?
Kontrola:
- [ ] jen primární a oficiální zdroje pro fakta
- [ ] informativní výklad, žádné osobní doporučení
- [ ] jasně uvedeno, kdy jít k odborníkovi
- [ ] platnost podle země a data

---

## Příklad: Monetizace AI agentů

Autor této dovednosti v první verzi předpokládal u tématu tyto okruhy. V nové verzi jsou to **hypotézy k ověření researchem**, ne hotová pravidla. Je to ukázka, jak se čočky použijí, ne šablona pro každé téma.

Možné cesty při zúžení (Fáze 2): agenturní služby pro malé a střední firmy, vlastní produkt či SaaS, freelance implementace, nástroje pro vývojáře, obsah a vzdělávání. Student vybere jednu.

Výzkumné otázky, které stojí za položení u cesty „služby pro firmy":
- **Spolehlivost:** Jak se staví agenti, kteří nehalucinují a nezacyklí se? (hranice mezi kódem a LLM, evaly, limity opakování, schvalování člověkem)
- **Cesta od nuly:** Jak získat první 1 až 2 piloty bez případových studií? Jak změřit ušetřené hodiny a chybovost?
- **Právo a data:** Odpovědnost za pravděpodobnostní chování, GDPR, zpracování osobních údajů, uchování dat u poskytovatele, kdo drží API klíč.
- **Nabídka a ceny:** Jak vypadají reálné modely (audit, implementace, měsíční správa) a jejich marže? Kolik stojí tokeny a provoz?
- **Akvizice:** Co funguje a co ne při hledání prvních klientů?
- **Selhání:** Proč projekty končí, co klienti odmítají?

Pořadí v kurikulu určí research. Pokud potvrdí, že chybný agent u klienta je drahý a nevratný, patří spolehlivost a právo před prodej. Pokud ne, nemá smysl je tam tlačit.
