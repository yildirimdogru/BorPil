# BorPil: bor esaslı, lityumsuz katı hâl EV bataryası tasarımı ve simülasyon paketi

*[English version below](#borpil-boron-based-lithium-free-solid-state-ev-battery-design-and-simulation-package)*

Lityum ağırlıklı pil kimyalarına alternatif olarak, **bor** içeren ve elektrikli araçlarda
kullanılabilecek bir batarya tasarımı: disiplinler arası bir bilim ekibinin (kimya, fizik,
malzeme bilimi, matematik/geometri, biyoloji, sistem mühendisliği; iki tur bağımsız inceleme —
kimya/fizik + kod, elektrik-elektronik + batarya üreticisi — ve beş üyeli kurul kararları)
tasarımı, hesapları ve simülasyonları. Her sayısal iddia `borpil/` paketindeki modellerden
üretilir; kod değişirse rapor değişir.

## Ne öneriyoruz?

**BorPil:** Lityum içermeyen, **bor esaslı katı elektrolitli**, sodyum-metal anotlu,
tamamen katı hâl bir elektrikli araç bataryası.

```
Al folyo | Na₃V₂(PO₄)₃ (ALD kaplı) + Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ kompozit katot | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ ayırıcı | Na metal | Al folyo
```

Bor, hücrede **enerji taşıyan iyonun otoyolu**dur: [B₁₂H₁₂]²⁻ ve [B₁₀H₁₀]²⁻ kafes anyonları
oda sıcaklığında hızla dönen, geniş boşluklu bir kristal kafes kurar; Na⁺ bu kafes içinde
düşük enerji engeliyle (Ea ≈ 0.4 eV) hareket eder. Bu sınıf ("hidroborat" veya
"kloso-borat" elektrolitler) 2014'ten bu yana literatürde en hızlı gelişen katı elektrolit
ailelerinden biridir ve Li-iyon'daki yanıcı organik elektrolitin yerini alır.

Kurul kararıyla 1. nesil **ticari baz çizgisi BorPil-A-alt** (60 µm elektrolit, 50 µm Na fazlası,
30 Ω·cm² arayüz — bugün üretilebilir), **hedef/üst bant BorPil-A** (30 µm / 20 µm / 15 Ω·cm²).

## Anahtar sayılar (modelden; `borpil rapor`)

| Büyüklük | BorPil-A-alt (1. nesil baz çizgisi) | BorPil-A (hedef) | Li-iyon LFP | Li-iyon NMC811 |
|---|---:|---:|---:|---:|
| Hücre enerji yoğunluğu | **177 Wh/kg, 279 Wh/L** | 203 Wh/kg, 341 Wh/L | 170 / 380 | 265 / 700 |
| 74 kWh paket (120s3p, 3 bağımsız dizi, pouch-in-frame) | **596 kg / 512 L** (125 Wh/kg) | 519 kg / 418 L (143 Wh/kg) | ~613 kg / 329 L | ~393 kg / 179 L |
| Lityum | **0 kg** | 0 | 6.8 kg | 8.2 kg |
| Kobalt / Nikel | **0 / 0** | 0 / 0 | 0 / 0 | 6.8 / 56 kg |
| Bor (paket başına) | **92 kg** | 70 kg | 0 | 0 |
| Yanıcı sıvı elektrolit | **yok** | yok | var | var |
| WLTP-benzeri menzil (C-segment, 20 °C, ısıl strateji) | **~457 km** (−10 °C ön ısıtılmış 474) | 474 km | — | — |
| DC hızlı şarj 10 → 80 % (paket 45 / 25 / −10 °C) | **32 / 38 / 54 dk** | 34 / 39 / 53 dk | | |
| Çalışma sıcaklığı | sürüşte 35 °C hedef, şarjda 45 °C, 60 °C tavan ("sıcak batarya") | | | |
| Paket maliyeti, gen-1 gerçekçi (SE 50 USD/kg, verim %75) | **412 USD/kWh** | 358 | ~110 | ~130 |
| Paket maliyeti, ölçek senaryosu (SE 25 USD/kg, verim %90) | 234 | 214 | | |

Varyantlar: **A-Fe** (vanadyumsuz, 178 Wh/kg), **A0** (NaCrO₂, kanıtlanmış pencere, 184 Wh/kg),
**LT** (karba-kloso + NVP, 10–45 °C kimya hattı — bulk açılır, CCD kilit kalır, `docs/10`),
**B** (karba-kloso-borat + 3.9 V katot, 281 Wh/kg — 2. nesil, pahalı), **C** (sert karbon anot,
dendritsiz, 144 Wh/kg), **S** (Na-S, ~400 Wh/kg — spekülatif, uzun vade).

## Neden bu yol?

1. **Bor içeriği anlamlı ve işlevsel.** Hücre kütlesinin ~%20–25'i bor; bor "katkı" değil,
   iyonik iletimin kendisidir. 74 kWh'lik bir paket 70–92 kg bor tüketir.
2. **Li'siz ve kritik-metalsiz.** Na (tuz), B (Türkiye dünya rezervinin ~%73'üne sahip),
   V veya Fe/Mn, Al, C. Kobalt, nikel, bakır, lityum yok.
3. **Güvenlik.** Yanıcı organik elektrolit yok. Kloso-boratlar kimyasal olarak olağanüstü
   kararlı (B₁₂ kafesi aromatik-benzeri 3-boyutlu delokalizasyon), suda hidroliz etmeyen
   tuzlar. Termal kaçak zinciri (elektrolit buharı + O₂ salımı) kırılır. Kalan riskler Na metal
   (e.n. 97.8 °C) ve nem/hidrat (`docs/05`).
4. **Sıcaklık dostu.** Kloso-borat iletkenliği sıcaklıkla artar; hücre 35–60 °C'de daha iyi
   çalışır. Yalıtım + düşük güçlü ısıtıcı + tahrik atık ısısı; soğutma yalnız şarjda.
5. **Üretilebilirlik.** Kloso-boratlar yumuşak (soğuk preslenebilir), sülfür elektrolitler
   gibi H₂S salmaz, oksit elektrolitler gibi sinterleme gerektirmez. Pouch-in-frame formatı ve
   sıcak izostatik pres ile pilot hat mümkündür (`docs/03`, `docs/07`).

## Sınırlar (açıkça)

- **Hızlı şarj ve soğuk güç, Na kaplama kritik akım yoğunluğu ile sınırlıdır:** 1.5 mA/cm² @ 25 °C
  (literatür 0.5–2), 4.5 @ 45 °C. 75 kW şarj yalnız paket ≥ 44 °C'de; soğuk pakette şarj süresi
  ısıtma gücüyle belirlenir → DC istasyonda 20 kW şebeke ısıtıcı. −10 °C'de tepe güç ~7 kW; ön ısıtma
  şarttır. Deneysel doğrulama zorunlu.
- **Hidroborat oksidasyon sınırı ~3 V** (termodinamik); NVP'nin 3.37 V platosu ve ~3.8 V kesimi
  **zorunlu ALD kaplama** ile pasifleştirici arayüze dayanır; model bu durumu **uyarı** olarak
  bayraklar. A0 (NaCrO₂) paralel nitelendirme hattı.
- **Yalıtım + ısıtıcı yeni bir tehlike yaratır:** ısıtıcı takılı kalırsa paket kendiliğinden
  sınırlanmaz ve Na erime noktasına yaklaşır → bağımsız 80 °C donanım kesici, ayrı kontaktör, çift NTC
  (ISO 26262 ASIL D → B(D)+B(D)).
- **Soğukta sigorta çalışmaz:** −10 °C'de kısa devre akımı (190–310 A) sürekli çalışma akımının altında;
  akım-plausibilite + dI/dt ile kontaktör açma gerekir.
- **Maliyet:** kloso-borat tuzlarının bugünkü fiyatı laboratuvar ölçeğindedir (>1000 USD/kg); gen-1
  verimi %60–75. Gerçekçi gen-1 paket maliyeti **360–410 USD/kWh** (SE 50 USD/kg); ekonomik hedef
  bandı 165–200 USD/kWh için SE ≤ 25 USD/kg, verim ≥ %90 ve 10 GWh ölçeği **birlikte** gerekir.
- **Ömür:** katı hâl Na hücrelerinde 1000+ çevrim henüz laboratuvar ölçeğinde; 1500–3000 çevrim
  hedefi ve 8 yıl / 160 000 km garanti riski doğrulanmalıdır.
- **Tedarik:** kloso-borat sentez kapasitesi bugün < 10 t/yıl (1 GWh için ~1400 t/yıl gerekir);
  vanadyum 45 kg/araç → A-Fe yolu paralel.

## Depo yapısı

```
borpil/            Python paketi (modeller)
  sabitler.py        fiziksel sabitler, molar kütleler
  malzemeler.py      malzeme veri tabanı (elektrolitler, katotlar, anotlar, Li-iyon referansları)
  termodinamik.py    Gibbs → E°, Nernst, bor-hava & DBFC teorik sınırları, DBFC menzil uzatıcı
  elektrolit.py      kloso-borat iletkenliği (Arrhenius, faz geçişi), ASR, kritik akım yoğunluğu (tek tanım)
  kimya_sicaklik.py  10–45 °C penceresi: bulk σ vs CCD/arayüz taraması, sentez KPI, BorPil-LT
  geometri.py        [B12H12]2- ikosahedronu, bcc kafes boşluk analizi, pouch/paket geometrisi
  hucre.py           katman yığını → Wh/kg, Wh/L, element bütçesi, maliyet, oksidasyon penceresi uyarıları (A, A-alt, A0, A-Fe, B, C, S, LT)
  paket.py           EV paketi: seri/paralel, 3 bağımsız dizi, kütle/hacim, gerilim penceresi–invertör–şarj cihazı–tab–kısa devre kontrolleri, ısıtıcı güvenlik analizi, gen-1 maliyet modeli
  simulasyon.py      ortak akım sınırı (deşarj/şarj/rejen), OCV+R, ısıl model (ısıtıcı, atık ısı, soğutma), WLTP-benzeri ve otoyol çevrimleri, DC hızlı şarj, darbe (AC) ısıtma, güç haritaları
  karsilastirma.py   Li-iyon ile karşılaştırma tablosu
  rapor.py, cli.py   rapor + grafik üretimi, komut satırı
docs/              tasarım dokümanları (Türkçe)
  00_ekip_ve_yontem.md            ekip rolleri, yöntem, karar günlüğü
  01_tasarim_ozeti.md             yönetici özeti
  02_kimya_ve_termodinamik.md     neden bor, aday kimyalar, kloso-borat mekanizması, kaynaklar
  03_malzeme_ve_uretim.md         sentez rotaları, reçeteler, proses akışı, maliyet
  04_hucre_ve_paket_tasarimi.md   hücre/paket/araç sayıları, elektrik mimarisi, ısıl strateji, BMS
  05_guvenlik_cevre_saglik.md     güvenlik (Na, ısıtıcı, kısa devre), toksikoloji, yaşam döngüsü
  06_riskler_trl_yol_haritasi.md  TRL, risk kaydı, 1. tur hakem bulguları, doğrulama planı, KPI
  07_ee_uretim_incelemesi_ve_kurul.md  elektrik-elektronik ve üretici incelemeleri, kurul kararları (P1–P20)
  08_paket_maden_ve_element_butcesi.md paket maden/element oranları (B, Na, V, P, Al; Li/Co/Ni/Cu = 0)
  09_isil_ekosistem_ve_soguk_baslangic.md 3. tur kurul: 35–60 °C, atık ısı 8/10, süperkap, zincirleme ısınma
  10_kimya_10_45C.md                      A1: 10–45 °C kimya hattı (K1 bulk açılır, K3 CCD kilit)
  urun/                                satışa-hazır ürün formu: veri formu, entegrasyon, güvenlik/garanti, broşür
cikti/             otomatik üretilen rapor (RAPOR.md) ve grafikler
tests/             birim testleri (50)
```

## Kurulum ve kullanım

```bash
pip install -r requirements.txt
python -m borpil.cli termo                 # teorik sınırlar (bor-hava, DBFC, metal-hava kıyas)
python -m borpil.cli hucre A-alt           # hücre yığın modeli (A, A-alt, A0, A-Fe, B, C, S, LT)
python -m borpil.cli kimya                 # 10–45 °C kimya taraması (bulk σ vs CCD)
python -m borpil.cli hucre A --ayirici 20 --alan-kapasitesi 4 --sicaklik 60
python -m borpil.cli paket A-alt --kwh 75  # 120s3p, 3 dizi, elektrik/güvenlik kontrolleri (--volt 770: 800 V sınıfı)
python -m borpil.cli surus A-alt --ortam -10 --isitici 35
python -m borpil.cli sarj A-alt --baslangic -10   # DC hızlı şarj, 20 kW şebeke ısıtıcı
python -m borpil.cli rapor                 # cikti/RAPOR.md + grafikler
python -m pytest -q
```

Tüm sayısal iddialar koddan üretilir; varsayımlar (özellikle maliyetler) veri sınıflarında
açıkça işaretlenmiştir (`maliyet_varsayim`). Ayrıntılar: `docs/02` (kimya), `docs/03`
(malzeme/üretim), `docs/04` (hücre/paket), `docs/05` (güvenlik/çevre), `docs/06` (riskler, hakem
bulguları, yol haritası), `docs/07` (elektrik-elektronik/üretici incelemeleri ve kurul kararları),
`docs/08` (paket maden ve element bütçesi), `docs/09` (ısıl ekosistem, soğuk başlangıç, süperkap kurul oturumu), `docs/10` (10–45 °C kimya hattı), `docs/urun/` (EV-74 teknik veri formu, entegrasyon,
güvenlik/garanti, tanıtım broşürü), `cikti/RAPOR.md` (sayılar).

---

# BorPil: boron-based, lithium-free solid-state EV battery design and simulation package

A battery design that uses **boron** instead of lithium-heavy chemistries and is suitable for
electric vehicles: the design, calculations and simulations of an interdisciplinary science team
(chemistry, physics, materials science, mathematics/geometry, biology, systems engineering; two
rounds of independent review — chemistry/physics + code, electrical engineering + battery
manufacturer — and decisions of a five-member council). Every numerical claim is generated by the
models in the `borpil/` package; if the code changes, the report changes.

## What do we propose?

**BorPil:** A lithium-free, all-solid-state electric-vehicle battery with a **boron-based solid
electrolyte** and a sodium-metal anode.

```
Al foil | Na₃V₂(PO₄)₃ (ALD-coated) + Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ composite cathode | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ separator | Na metal | Al foil
```

In this cell, boron is the **highway of the energy-carrying ion**: the [B₁₂H₁₂]²⁻ and
[B₁₀H₁₀]²⁻ cage anions build a crystal lattice with fast-rotating anions and wide interstitial
space at room temperature, in which Na⁺ moves with a low energy barrier (Ea ≈ 0.4 eV). This
class ("hydroborate" or "closo-borate" electrolytes) has been one of the fastest-developing
solid-electrolyte families in the literature since 2014 and replaces the flammable organic
electrolyte of Li-ion cells.

By council decision, the gen-1 **commercial baseline is BorPil-A-alt** (60 µm electrolyte, 50 µm
Na excess, 30 Ω·cm² interface — manufacturable today) and the **target/upper band is BorPil-A**
(30 µm / 20 µm / 15 Ω·cm²).

## Key numbers (from the model; `borpil rapor`)

| Quantity | BorPil-A-alt (gen-1 baseline) | BorPil-A (target) | Li-ion LFP | Li-ion NMC811 |
|---|---:|---:|---:|---:|
| Cell energy density | **177 Wh/kg, 279 Wh/L** | 203 Wh/kg, 341 Wh/L | 170 / 380 | 265 / 700 |
| 74 kWh pack (120s3p, 3 independent strings, pouch-in-frame) | **596 kg / 512 L** (125 Wh/kg) | 519 kg / 418 L (143 Wh/kg) | ~613 kg / 329 L | ~393 kg / 179 L |
| Lithium | **0 kg** | 0 | 6.8 kg | 8.2 kg |
| Cobalt / Nickel | **0 / 0** | 0 / 0 | 0 / 0 | 6.8 / 56 kg |
| Boron (per pack) | **92 kg** | 70 kg | 0 | 0 |
| Flammable liquid electrolyte | **none** | none | yes | yes |
| WLTP-like range (C-segment, 20 °C, thermal strategy) | **~457 km** (474 km at −10 °C when pre-heated from the grid) | 474 km | — | — |
| DC fast charge 10 → 80 % (pack at 45 / 25 / −10 °C) | **32 / 38 / 54 min** | 34 / 39 / 53 min | | |
| Operating temperature | 35 °C target while driving, 45 °C while charging, 60 °C ceiling ("warm battery") | | | |
| Pack cost, realistic gen-1 (SE at 50 USD/kg, 75 % yield) | **412 USD/kWh** | 358 | ~110 | ~130 |
| Pack cost, scale scenario (SE at 25 USD/kg, 90 % yield) | 234 | 214 | | |

Variants: **A-Fe** (vanadium-free, 178 Wh/kg), **A0** (NaCrO₂, proven stability window,
184 Wh/kg), **LT** (carba-closo + NVP, 10–45 °C chemistry track — bulk opens, CCD remains,
`docs/10`), **B** (carba-closo-borate + 3.9 V cathode, 281 Wh/kg — 2nd gen, expensive), **C**
(hard-carbon anode, dendrite-free, 144 Wh/kg), **S** (Na-S, ~400 Wh/kg — speculative, long term).

## Why this route?

1. **The boron content is substantial and functional.** About 20–25 % of the cell mass is boron;
   boron is not an "additive" but the ionic conduction itself. A 74 kWh pack consumes 70–92 kg of boron.
2. **Lithium-free and free of critical metals.** Na (salt), B (Turkey holds ~73 % of world
   reserves), V or Fe/Mn, Al, C. No cobalt, nickel, copper or lithium.
3. **Safety.** No flammable organic electrolyte. Closo-borates are chemically exceptionally
   stable (the B₁₂ cage shows aromatic-like three-dimensional delocalisation), salts that do not
   hydrolyse in water. The thermal-runaway chain (electrolyte vapour + O₂ release) is broken.
   The remaining risks are Na metal (m.p. 97.8 °C) and moisture/hydrate (`docs/05`).
4. **Temperature-friendly.** Closo-borate conductivity increases with temperature; the cell works
   better at 35–60 °C. Insulation + a low-power heater + drivetrain waste heat; cooling only while charging.
5. **Manufacturability.** Closo-borates are soft (cold-pressable), release no H₂S like sulfide
   electrolytes, and need no sintering like oxide electrolytes. A pilot line is feasible with a
   pouch-in-frame format and warm isostatic pressing (`docs/03`, `docs/07`).

## Limitations (stated explicitly)

- **Fast charging and cold power are limited by the critical current density for Na plating:**
  1.5 mA/cm² at 25 °C (literature 0.5–2), 4.5 at 45 °C. 75 kW charging only with the pack ≥ 44 °C; in a
  cold pack the charging time is set by the heating power → 20 kW grid-fed heater at the DC station.
  Peak power at −10 °C is ~7 kW; pre-heating is mandatory. Experimental validation required.
- **Hydroborate oxidation limit ~3 V** (thermodynamic); the 3.37 V plateau and ~3.8 V cut-off of
  NVP rely on a passivating interface enabled by a **mandatory ALD coating**; the model flags this as
  a **warning**. A0 (NaCrO₂) is a parallel qualification track.
- **Insulation + heater creates a new hazard:** a stuck-on heater is not self-limiting in an insulated
  pack and approaches the Na melting point → independent 80 °C hardware cut-off, separate contactor,
  dual NTC (ISO 26262 ASIL D → B(D)+B(D)).
- **Fuses do not work in the cold:** at −10 °C the short-circuit current (190–310 A) is below the
  continuous operating current; current-plausibility + dI/dt contactor opening is required.
- **Cost:** today's closo-borate salt prices are laboratory-scale (>1000 USD/kg); gen-1 yield 60–75 %.
  Realistic gen-1 pack cost **360–410 USD/kWh** (SE at 50 USD/kg); the economic target band of
  165–200 USD/kWh requires SE ≤ 25 USD/kg, yield ≥ 90 % and 10 GWh scale **together**.
- **Cycle life:** 1000+ cycles in solid-state Na cells have so far been shown only at laboratory
  scale; the 1500–3000 cycle target and the 8-year / 160,000 km warranty risk must be validated.
- **Supply:** closo-borate synthesis capacity is < 10 t/yr today (~1400 t/yr needed per GWh);
  vanadium 45 kg per vehicle → the A-Fe route runs in parallel.

## Repository layout

```
borpil/            Python package (models)
  sabitler.py        physical constants, molar masses
  malzemeler.py      materials database (electrolytes, cathodes, anodes, Li-ion references)
  termodinamik.py    Gibbs → E°, Nernst, boron-air & DBFC theoretical limits, DBFC range extender
  elektrolit.py      closo-borate conductivity (Arrhenius, phase transition), ASR, critical current density (single definition)
  kimya_sicaklik.py  10–45 °C window: bulk σ vs CCD/interface scan, synthesis KPIs, BorPil-LT
  geometri.py        [B12H12]2- icosahedron, bcc lattice void analysis, pouch/pack geometry
  hucre.py           layer stack → Wh/kg, Wh/L, element budget, cost, oxidation-window warnings (A, A-alt, A0, A-Fe, B, C, S, LT)
  paket.py           EV pack: series/parallel, 3 independent strings, mass/volume, voltage window–inverter–charger–tab–short-circuit checks, heater safety analysis, gen-1 cost model
  simulasyon.py      shared current limit (discharge/charge/regen), OCV+R, thermal model (heater, waste heat, cooling), WLTP-like and highway cycles, DC fast charge, pulse (AC) heating, power maps
  karsilastirma.py   comparison table against Li-ion
  rapor.py, cli.py   report + figure generation, command line
docs/              design documents (Turkish)
  00_ekip_ve_yontem.md            team roles, method, decision log
  01_tasarim_ozeti.md             executive summary
  02_kimya_ve_termodinamik.md     why boron, candidate chemistries, closo-borate mechanism, references
  03_malzeme_ve_uretim.md         synthesis routes, recipes, process flow, cost
  04_hucre_ve_paket_tasarimi.md   cell/pack/vehicle numbers, electrical architecture, thermal strategy, BMS
  05_guvenlik_cevre_saglik.md     safety (Na, heater, short circuit), toxicology, life cycle
  06_riskler_trl_yol_haritasi.md  TRL, risk register, round-1 review findings, validation plan, KPIs
  07_ee_uretim_incelemesi_ve_kurul.md  electrical-engineering and manufacturer reviews, council decisions (P1–P20)
  08_paket_maden_ve_element_butcesi.md pack mineral/element budget (B, Na, V, P, Al; Li/Co/Ni/Cu = 0)
  09_isil_ekosistem_ve_soguk_baslangic.md 3rd council session: 35–60 °C band, waste-heat 8/10, supercap catalyst
  10_kimya_10_45C.md                      A1: 10–45 °C chemistry track (K1 bulk opens, K3 CCD remains)
  urun/                                product-form set: datasheet, integration, safety/warranty, brochure
cikti/             auto-generated report (RAPOR.md) and figures
tests/             unit tests (50)
```

## Installation and usage

```bash
pip install -r requirements.txt
python -m borpil.cli termo                 # theoretical limits (boron-air, DBFC, metal-air comparison)
python -m borpil.cli hucre A-alt           # cell stack model (A, A-alt, A0, A-Fe, B, C, S, LT)
python -m borpil.cli kimya                 # 10–45 °C chemistry scan (bulk σ vs CCD)
python -m borpil.cli hucre A --ayirici 20 --alan-kapasitesi 4 --sicaklik 60
python -m borpil.cli paket A-alt --kwh 75  # 120s3p, 3 strings, electrical/safety checks (--volt 770: 800 V class)
python -m borpil.cli surus A-alt --ortam -10 --isitici 35
python -m borpil.cli sarj A-alt --baslangic -10   # DC fast charge with 20 kW grid-fed heater
python -m borpil.cli rapor                 # cikti/RAPOR.md + figures
python -m pytest -q
```

All numerical claims are produced by the code; assumptions (especially costs) are explicitly
marked in the data classes (`maliyet_varsayim`). Details: `docs/02` (chemistry), `docs/03`
(materials/manufacturing), `docs/04` (cell/pack), `docs/05` (safety/environment), `docs/06`
(risks, review findings, roadmap), `docs/07` (electrical/manufacturing reviews and council
decisions), `docs/08` (pack mineral and element budget), `docs/09` (thermal ecosystem, cold start, supercap council session), `docs/10` (10–45 °C chemistry track), `docs/urun/` (EV-74 datasheet,
integration, safety/warranty, brochure), `cikti/RAPOR.md` (numbers).
