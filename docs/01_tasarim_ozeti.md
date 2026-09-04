# 01 — Tasarım Özeti (Yönetici Özeti)

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
   yakın bir proses akışı mümkündür (bkz. `docs/03`).

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

Ayrıntılar: `docs/02` (kimya), `docs/03` (malzeme/üretim), `docs/04` (hücre/paket),
`docs/05` (güvenlik/çevre), `docs/06` (riskler, hakem bulguları ve yol haritası),
`cikti/RAPOR.md` (sayılar).
