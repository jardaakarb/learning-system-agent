# Vzorové Kurikulum (ukládá se jako soubor `curriculum.txt`)

Mapa 5 až 20 modulů. Podcast i systém se podle ní orientují. Každý modul odpovídá jedné lekci a **vychází z cílové schopnosti**, ne ze seznamu témat.

Vzor je z elektrotechniky, aby bylo vidět, že formát je obecný.

---

```markdown
# Curriculum
Cíl kurzu: Po kurzu umíš navrhnout jištění jednoduché instalace NN a zdůvodnit volbu prvků. Výstup kurzu: Návrh jištění pro zadanou instalaci s odůvodněním u každého prvku.

1. Poruchové proudy v obvodech
    Výstupní schopnost: Po lekci umíš určit, jestli jde o přetížení, nebo zkrat, a odhadnout velikost poruchového proudu.
    Klíčové mechanismy: Ohmův a Kirchhoffovy zákony, impedance smyčky, tepelné a dynamické účinky nadproudů
    Typická selhání: zanedbání impedance smyčky, záměna přetížení se zkratem
    Cvičení: Spočítej zkratový proud pro zadanou smyčku a porovnej s vypínací schopností jističe.
    Opora v balíčku: t01, t02

2. Ochranné prvky NN
    Výstupní schopnost: Po lekci umíš vybrat jistič a charakteristiku podle zátěže.
    Klíčové mechanismy: bimetalová a elektromagnetická spoušť, charakteristiky B, C, D, selektivita
    Typická selhání: jistič s příliš „rychlou" charakteristikou u zátěže s rozběhovým proudem
    Cvičení: Pro tři zátěže vyber charakteristiku a zdůvodni ji.
    Opora v balíčku: t03, t04

3. Ochrana před úrazem a proudové chrániče
    Výstupní schopnost: Po lekci umíš vysvětlit, kdy chránič zafunguje a kdy ne, a proč.
    Klíčové mechanismy: dotyková napětí, součtový transformátor, rozdělení TN-C na TN-S
    Typická selhání: chránič za bodem rozdělení zapojený na společný PEN
    Cvičení: Najdi chybu v zadaném schématu a navrhni opravu.
    Opora v balíčku: t05, t06
```

---

## Pravidla

- Každý modul má **výstupní schopnost** ve tvaru „Po lekci umíš…".
- Každý modul má **cvičení**, které se dělá rukama, ne jen poslechem.
- **Opora v balíčku** odkazuje aspoň na dva zdroje. Modul bez opory nepatří do kurikula.
- Žádný modul nesmí předpokládat znalost, která přijde později.
