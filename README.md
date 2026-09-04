# BorPil: bor esaslı, lityumsuz katı hâl EV bataryası tasarımı ve simülasyon paketi

*[English version below](#borpil-boron-based-lithium-free-solid-state-ev-battery-design-and-simulation-package)*

Lityum ağırlıklı pil kimyalarına alternatif olarak, **bor** içeren ve elektrikli araçlarda
kullanılabilecek bir batarya tasarımı: disiplinler arası bir bilim ekibinin (kimya, fizik,
malzeme bilimi, matematik/geometri, biyoloji, sistem mühendisliği ve iki bağımsız hakem)
kararları, hesapları ve simülasyonları. Her sayısal iddia `borpil/` paketindeki modellerden
üretilir; kod değişirse rapor değişir.

## Ne öneriyoruz?

**BorPil-A:** Lityum içermeyen, **bor esaslı katı elektrolitli**, sodyum-metal anotlu,
tamamen katı hâl bir elektrikli araç bataryası.

```
Al folyo | Na₃V₂(PO₄)₃ + Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ kompozit katot | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ ayırıcı (30 µm) | Na metal | Al folyo
```

Bor, hücrede **enerji taşıyan iyonun otoyolu**dur: [B₁₂H₁₂]²⁻ ve [B₁₀H₁₀]²⁻ kafes anyonları
oda sıcaklığında hızla dönen, geniş boşluklu bir kristal kafes kurar; Na⁺ bu kafes içinde
düşük enerji engeliyle (Ea ≈ 0.4 eV) hareket eder. Bu sınıf ("hidroborat" veya
"kloso-borat" elektrolitler) 2014'ten bu yana literatürde en hızlı gelişen katı elektrolit
ailelerinden biridir ve Li-iyon'daki yanıcı organik elektrolitin yerini alır.

## Anahtar sayılar (modelden; `borpil rapor`)

| Büyüklük | BorPil-A (1. nesil, tasarım noktası) | BorPil-A-alt (muhafazakâr alt tahmin) | Li-iyon LFP | Li-iyon NMC811 |
|---|---:|---:|---:|---:|
| Hücre enerji yoğunluğu | **201 Wh/kg, 337 Wh/L** | 175 Wh/kg, 276 Wh/L | 170 / 380 | 265 / 700 |
| 75 kWh paket kütlesi / hacmi | **523 kg / 401 L** (145 Wh/kg) | 602 kg / 490 L | ~613 kg / 329 L | ~393 kg / 179 L |
| Lityum | **0 kg** | 0 | 6.8 kg | 8.2 kg |
| Kobalt / Nikel | **0 / 0** | 0 / 0 | 0 / 0 | 6.8 / 56 kg |
| Bor (paket başına) | **72 kg** | 95 kg | 0 | 0 |
| Yanıcı sıvı elektrolit | **yok** | yok | var | var |
| WLTP-benzeri menzil (C-segment, 20 °C, ısıtıcı 35 °C) | **~475 km** (ısıtıcısız 490) | — | — | — |
| Çalışma sıcaklığı | 35–60 °C hedef ("sıcak batarya"); soğukta ısıtıcı ile | | | |
| Hücre malzeme maliyeti (varsayım) | 134 USD/kWh (SE 50 USD/kg); 92 (SE 20 USD/kg) | 158 | ~55 | ~70 |

Tasarım noktası (30 µm ayırıcı, 20 µm Na fazlası, 15 Ω·cm² arayüz) ile alt tahmin (60 µm,
50 µm, 30 Ω·cm²) arasındaki **175–201 Wh/kg** bandı, 1. nesil için savunulabilir aralıktır.

Varyantlar: **A-Fe** (vanadyumsuz, 176 Wh/kg, 105 USD/kWh malzeme), **A0** (NaCrO₂,
kanıtlanmış pencere, 182 Wh/kg), **B** (karba-kloso-borat + 3.9 V katot, 277 Wh/kg — 2. nesil,
pahalı), **C** (sert karbon anot, dendritsiz, 144 Wh/kg), **S** (Na-S, ~400 Wh/kg — spekülatif,
uzun vade).

## Neden bu yol?

1. **Bor içeriği anlamlı ve işlevsel.** Hücre kütlesinin ~%20'si bor; bor "katkı" değil,
   iyonik iletimin kendisidir. 75 kWh'lik bir paket ~72 kg bor tüketir.
2. **Li'siz ve kritik-metalsiz.** Na (tuz), B (Türkiye dünya rezervinin ~%73'üne sahip),
   V veya Fe/Mn, Al, C. Kobalt, nikel, bakır, lityum yok.
3. **Güvenlik.** Yanıcı organik elektrolit yok. Kloso-boratlar kimyasal olarak olağanüstü
   kararlı (B₁₂ kafesi aromatik-benzeri 3-boyutlu delokalizasyon), suda hidroliz etmeyen
   tuzlar. Termal kaçak zinciri (elektrolit buharı + O₂ salımı) kırılır. Kalan risk Na metaldir
   (`docs/05`).
4. **Sıcaklık dostu.** Kloso-borat iletkenliği sıcaklıkla artar; hücre 35–60 °C'de daha iyi
   çalışır. Aktif soğutma yerine yalıtım + düşük güçlü ısıtıcı yeter.
5. **Üretilebilirlik.** Kloso-boratlar yumuşak (soğuk preslenebilir), sülfür elektrolitler
   gibi H₂S salmaz, oksit elektrolitler gibi sinterleme gerektirmez. Mevcut pouch hattına
   yakın bir proses akışı mümkündür (`docs/03`).

## Sınırlar (açıkça)

- **Hızlı şarj**, Na kaplama kritik akım yoğunluğu ile sınırlıdır: 1.5 mA/cm² @ 25 °C
  (literatür 0.5–2), 4.5 mA/cm² @ 45 °C. 75 kW şarj (3.2 mA/cm²) yalnız ≥ 40 °C'de; soğuk pakette
  önce ısıtma. Deneysel doğrulama zorunlu.
- **Hidroborat oksidasyon sınırı ~3 V** (termodinamik); NVP'nin 3.37 V platosu ve ~3.8 V kesimi
  pasifleştirici arayüzle (Asakura 2020 türü) çalışır; model bu durumu **uyarı** olarak bayraklar.
  A0 (NaCrO₂, kesim 3.4 V) bu riski büyük ölçüde azaltır.
- **Soğuk performans:** −10 °C'de tepe güç ~7 kW; sürüş öncesi ön ısıtma gerekir (−10 → 35 °C
  için 6.5 kWh, tercihen şebekeden). Isıtıcı olmadan −20 °C stres senaryosunda ilk ~7 dakika
  güç kısıtı yaşanır, paket I²R ile kendini ısıtır.
- **Maliyet:** kloso-borat tuzlarının bugünkü fiyatı laboratuvar ölçeğindedir (>1000 USD/kg).
  Paket maliyeti SE fiyatına doğrusal bağlı: 20 → 165, 50 → 230, 100 → 340, 200 → 558 USD/kWh.
  Ekonomik eşik SE ≤ 20–25 USD/kg.
- **Ömür:** katı hâl Na hücrelerinde 1000+ çevrim henüz laboratuvar ölçeğinde gösterilmiştir;
  ticari EV için 1500–3000 çevrim hedefi doğrulanmalıdır.
- **Vanadyum:** 46 kg V/araç; 1 M araç/yıl küresel V üretiminin ~%40'ı olur → A-Fe yolu
  stratejik olarak paralel yürütülür.

## Depo yapısı

```
borpil/            Python paketi (modeller)
  sabitler.py        fiziksel sabitler, molar kütleler
  malzemeler.py      malzeme veri tabanı (elektrolitler, katotlar, anotlar, Li-iyon referansları)
  termodinamik.py    Gibbs → E°, Nernst, bor-hava & DBFC teorik sınırları, DBFC menzil uzatıcı
  elektrolit.py      kloso-borat iletkenliği (Arrhenius, faz geçişi), ASR, kritik akım yoğunluğu
  geometri.py        [B12H12]2- ikosahedronu, bcc kafes boşluk analizi, pouch/paket geometrisi
  hucre.py           katman yığını → Wh/kg, Wh/L, element bütçesi, maliyet (varyantlar A, A-alt, A0, A-Fe, B, C, S)
  paket.py           EV paketi boyutlandırma (seri/paralel, kütle, hacim, ısıl, maliyet)
  simulasyon.py      OCV+R eşdeğer devre, toplu ısıl model, WLTP-benzeri sürüş çevrimi, güç haritası
  karsilastirma.py   Li-iyon ile karşılaştırma tablosu
  rapor.py, cli.py   rapor + grafik üretimi, komut satırı
docs/              tasarım dokümanları (Türkçe)
  00_ekip_ve_yontem.md            ekip rolleri, yöntem, karar günlüğü
  01_tasarim_ozeti.md             yönetici özeti
  02_kimya_ve_termodinamik.md     neden bor, aday kimyalar, kloso-borat mekanizması, kaynaklar
  03_malzeme_ve_uretim.md         sentez rotaları, reçeteler, proses akışı, maliyet
  04_hucre_ve_paket_tasarimi.md   hücre/paket/araç sayıları, ısıl strateji, BMS
  05_guvenlik_cevre_saglik.md     güvenlik, toksikoloji, yaşam döngüsü
  06_riskler_trl_yol_haritasi.md  TRL, risk kaydı, bağımsız hakem bulguları (21 madde), doğrulama planı, KPI
cikti/             otomatik üretilen rapor (RAPOR.md) ve grafikler
tests/             birim testleri (39)
```

## Kurulum ve kullanım

```bash
pip install -r requirements.txt
python -m borpil.cli termo                 # teorik sınırlar (bor-hava, DBFC, metal-hava kıyas)
python -m borpil.cli hucre A               # hücre yığın modeli (A, A-alt, A0, A-Fe, B, C, S)
python -m borpil.cli hucre A --ayirici 20 --alan-kapasitesi 4 --sicaklik 60
python -m borpil.cli paket A --kwh 75 --volt 400
python -m borpil.cli surus A --ortam -10 --isitici 35
python -m borpil.cli rapor                 # cikti/RAPOR.md + grafikler
python -m pytest -q
```

Tüm sayısal iddialar koddan üretilir; varsayımlar (özellikle maliyetler) veri sınıflarında
açıkça işaretlenmiştir (`maliyet_varsayim`). Ayrıntılar: `docs/02` (kimya), `docs/03`
(malzeme/üretim), `docs/04` (hücre/paket), `docs/05` (güvenlik/çevre), `docs/06` (riskler,
hakem bulguları ve yol haritası), `cikti/RAPOR.md` (sayılar).

---

# BorPil: boron-based, lithium-free solid-state EV battery design and simulation package

A battery design that uses **boron** instead of lithium-heavy chemistries and is suitable for
electric vehicles: the decisions, calculations and simulations of an interdisciplinary science
team (chemistry, physics, materials science, mathematics/geometry, biology, systems engineering,
plus two independent reviewers). Every numerical claim is generated by the models in the
`borpil/` package; if the code changes, the report changes.

## What do we propose?

**BorPil-A:** A lithium-free, all-solid-state electric-vehicle battery with a **boron-based
solid electrolyte** and a sodium-metal anode.

```
Al foil | Na₃V₂(PO₄)₃ + Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ composite cathode | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ separator (30 µm) | Na metal | Al foil
```

In this cell, boron is the **highway of the energy-carrying ion**: the [B₁₂H₁₂]²⁻ and
[B₁₀H₁₀]²⁻ cage anions build a crystal lattice with fast-rotating anions and wide interstitial
space at room temperature, in which Na⁺ moves with a low energy barrier (Ea ≈ 0.4 eV). This
class ("hydroborate" or "closo-borate" electrolytes) has been one of the fastest-developing
solid-electrolyte families in the literature since 2014 and replaces the flammable organic
electrolyte of Li-ion cells.

## Key numbers (from the model; `borpil rapor`)

| Quantity | BorPil-A (1st gen, design point) | BorPil-A-alt (conservative lower estimate) | Li-ion LFP | Li-ion NMC811 |
|---|---:|---:|---:|---:|
| Cell energy density | **201 Wh/kg, 337 Wh/L** | 175 Wh/kg, 276 Wh/L | 170 / 380 | 265 / 700 |
| 75 kWh pack mass / volume | **523 kg / 401 L** (145 Wh/kg) | 602 kg / 490 L | ~613 kg / 329 L | ~393 kg / 179 L |
| Lithium | **0 kg** | 0 | 6.8 kg | 8.2 kg |
| Cobalt / Nickel | **0 / 0** | 0 / 0 | 0 / 0 | 6.8 / 56 kg |
| Boron (per pack) | **72 kg** | 95 kg | 0 | 0 |
| Flammable liquid electrolyte | **none** | none | yes | yes |
| WLTP-like range (C-segment, 20 °C, heater set to 35 °C) | **~475 km** (490 without heater) | — | — | — |
| Operating temperature | 35–60 °C target ("warm battery"); heater in cold climates | | | |
| Cell material cost (assumption) | 134 USD/kWh (SE at 50 USD/kg); 92 (SE at 20 USD/kg) | 158 | ~55 | ~70 |

The **175–201 Wh/kg** band between the design point (30 µm separator, 20 µm Na excess,
15 Ω·cm² interface) and the lower estimate (60 µm, 50 µm, 30 Ω·cm²) is the defensible range for
the first generation.

Variants: **A-Fe** (vanadium-free, 176 Wh/kg, 105 USD/kWh materials), **A0** (NaCrO₂, proven
stability window, 182 Wh/kg), **B** (carba-closo-borate + 3.9 V cathode, 277 Wh/kg — 2nd gen,
expensive), **C** (hard-carbon anode, dendrite-free, 144 Wh/kg), **S** (Na-S, ~400 Wh/kg —
speculative, long term).

## Why this route?

1. **The boron content is substantial and functional.** About 20% of the cell mass is boron;
   boron is not an "additive" but the ionic conduction itself. A 75 kWh pack consumes ~72 kg of boron.
2. **Lithium-free and free of critical metals.** Na (salt), B (Turkey holds ~73% of world
   reserves), V or Fe/Mn, Al, C. No cobalt, nickel, copper or lithium.
3. **Safety.** No flammable organic electrolyte. Closo-borates are chemically exceptionally
   stable (the B₁₂ cage shows aromatic-like three-dimensional delocalisation), salts that do not
   hydrolyse in water. The thermal-runaway chain (electrolyte vapour + O₂ release) is broken.
   The remaining risk is Na metal (`docs/05`).
4. **Temperature-friendly.** Closo-borate conductivity increases with temperature; the cell works
   better at 35–60 °C. Insulation plus a low-power heater replaces active cooling.
5. **Manufacturability.** Closo-borates are soft (cold-pressable), release no H₂S like sulfide
   electrolytes, and need no sintering like oxide electrolytes. A process flow close to existing
   pouch-cell lines is feasible (`docs/03`).

## Limitations (stated explicitly)

- **Fast charging** is limited by the critical current density for Na plating: 1.5 mA/cm² at
  25 °C (literature 0.5–2), 4.5 mA/cm² at 45 °C. 75 kW charging (3.2 mA/cm²) only at ≥ 40 °C; a
  cold pack must be heated first. Experimental validation is mandatory.
- **Hydroborate oxidation limit ~3 V** (thermodynamic); the 3.37 V plateau and ~3.8 V cut-off of
  NVP rely on a passivating interface (Asakura 2020 type); the model flags this as a **warning**.
  A0 (NaCrO₂, 3.4 V cut-off) largely removes this risk.
- **Cold performance:** peak power at −10 °C is ~7 kW; pre-heating before driving is required
  (6.5 kWh for −10 → 35 °C, preferably from the grid). Without a heater, in the −20 °C stress
  scenario the first ~7 minutes are power-limited while the pack self-heats through I²R.
- **Cost:** today's closo-borate salt prices are laboratory-scale (>1000 USD/kg). Pack cost
  scales linearly with SE price: 20 → 165, 50 → 230, 100 → 340, 200 → 558 USD/kWh. Economic
  threshold SE ≤ 20–25 USD/kg.
- **Cycle life:** 1000+ cycles in solid-state Na cells have so far been shown only at laboratory
  scale; the 1500–3000 cycle target for commercial EVs must be validated.
- **Vanadium:** 46 kg V per vehicle; 1 M vehicles/year would be ~40% of global V production →
  the A-Fe route is pursued strategically in parallel.

## Repository layout

```
borpil/            Python package (models)
  sabitler.py        physical constants, molar masses
  malzemeler.py      materials database (electrolytes, cathodes, anodes, Li-ion references)
  termodinamik.py    Gibbs → E°, Nernst, boron-air & DBFC theoretical limits, DBFC range extender
  elektrolit.py      closo-borate conductivity (Arrhenius, phase transition), ASR, critical current density
  geometri.py        [B12H12]2- icosahedron, bcc lattice void analysis, pouch/pack geometry
  hucre.py           layer stack → Wh/kg, Wh/L, element budget, cost (variants A, A-alt, A0, A-Fe, B, C, S)
  paket.py           EV pack sizing (series/parallel, mass, volume, thermal, cost)
  simulasyon.py      OCV+R equivalent circuit, lumped thermal model, WLTP-like drive cycle, power map
  karsilastirma.py   comparison table against Li-ion
  rapor.py, cli.py   report + figure generation, command line
docs/              design documents (Turkish)
  00_ekip_ve_yontem.md            team roles, method, decision log
  01_tasarim_ozeti.md             executive summary
  02_kimya_ve_termodinamik.md     why boron, candidate chemistries, closo-borate mechanism, references
  03_malzeme_ve_uretim.md         synthesis routes, recipes, process flow, cost
  04_hucre_ve_paket_tasarimi.md   cell/pack/vehicle numbers, thermal strategy, BMS
  05_guvenlik_cevre_saglik.md     safety, toxicology, life cycle
  06_riskler_trl_yol_haritasi.md  TRL, risk register, independent review findings (21 items), validation plan, KPIs
cikti/             auto-generated report (RAPOR.md) and figures
tests/             unit tests (39)
```

## Installation and usage

```bash
pip install -r requirements.txt
python -m borpil.cli termo                 # theoretical limits (boron-air, DBFC, metal-air comparison)
python -m borpil.cli hucre A               # cell stack model (A, A-alt, A0, A-Fe, B, C, S)
python -m borpil.cli hucre A --ayirici 20 --alan-kapasitesi 4 --sicaklik 60
python -m borpil.cli paket A --kwh 75 --volt 400
python -m borpil.cli surus A --ortam -10 --isitici 35
python -m borpil.cli rapor                 # cikti/RAPOR.md + figures
python -m pytest -q
```

All numerical claims are produced by the code; assumptions (especially costs) are explicitly
marked in the data classes (`maliyet_varsayim`). Details: `docs/02` (chemistry), `docs/03`
(materials/manufacturing), `docs/04` (cell/pack), `docs/05` (safety/environment), `docs/06`
(risks, review findings and roadmap), `cikti/RAPOR.md` (numbers).
