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

| Büyüklük | BorPil-A (1. nesil) | Li-iyon LFP | Li-iyon NMC811 |
|---|---:|---:|---:|
| Hücre enerji yoğunluğu | **191 Wh/kg, 337 Wh/L** | 170 Wh/kg, 380 Wh/L | 265 Wh/kg, 700 Wh/L |
| 75 kWh paket kütlesi | **521 kg** (145 Wh/kg) | ~613 kg | ~393 kg |
| Lityum | **0 kg** | 6.8 kg | 8.2 kg |
| Kobalt / Nikel | **0 / 0** | 0 / 0 | 6.8 / 56 kg |
| Bor (paket başına) | **72 kg** | 0 | 0 |
| Yanıcı sıvı elektrolit | **yok** | var | var |
| WLTP-benzeri menzil (C-segment, 20 °C) | **~490 km** | — | — |
| Çalışma sıcaklığı | 25–60 °C (soğukta düşük güçle çalışır, ısıtıcı ile 25 °C'ye) | | |
| Hücre malzeme maliyeti (varsayım) | 119 USD/kWh (SE 50 USD/kg ile); SE 20 USD/kg'da ~78 | ~55 | ~70 |

Varyantlar: **A-Fe** (vanadyumsuz, 195 Wh/kg, 91 USD/kWh malzeme), **A0** (NaCrO₂, kanıtlanmış
kararlılık penceresi, 173 Wh/kg), **B** (karba-kloso-borat + 3.9 V katot, 261 Wh/kg — 2. nesil),
**C** (sert karbon anot, dendritsiz, 144 Wh/kg), **S** (Na-S, 336 Wh/kg — uzun vade).

## Neden bu yol?

1. **Bor içeriği anlamlı ve işlevsel.** Hücre kütlesinin ~%19'u bor; bor "katkı" değil,
   iyonik iletimin kendisidir. 75 kWh'lik bir paket ~72 kg bor tüketir.
2. **Li'siz ve kritik-metalsiz.** Na (tuz), B (Türkiye dünya rezervinin ~%73'üne sahip),
   V veya Fe/Mn, Al, C. Kobalt, nikel, bakır, lityum yok.
3. **Güvenlik.** Yanıcı organik elektrolit yok. Kloso-boratlar kimyasal olarak olağanüstü
   kararlı (B₁₂ kafesi aromatik-benzeri 3-boyutlu delokalizasyon), havada ve suda hidroliz
   etmeyen tuzlar. Termal kaçak zinciri (elektrolit buharı + O₂ salımı) kırılır.
4. **Sıcaklık dostu.** Kloso-borat iletkenliği sıcaklıkla artar; hücre 45–60 °C'de daha iyi
   çalışır. Aktif soğutma yerine yalıtım + düşük güçlü ısıtıcı yeter.
5. **Üretilebilirlik.** Kloso-boratlar yumuşak (soğuk preslenebilir), sülfür elektrolitler
   gibi H₂S salmaz, oksit elektrolitler gibi sinterleme gerektirmez. Mevcut pouch hattına
   yakın bir proses akışı mümkündür (bkz. `docs/03`).

## Sınırlar (açıkça)

- **Hızlı şarj**, Na kaplama kritik akım yoğunluğu ile sınırlıdır (~1C, ≈75 kW, 45 °C'de).
  Hedef: 2. nesilde 3 mA/cm² → 6 mA/cm².
- **Hidroborat oksidasyon sınırı ~3 V** (termodinamik); NVP'nin 3.37 V'u pasifleştirici
  arayüzle çalışır (Asakura 2020 türü). A0 (NaCrO₂) bu riski taşımaz.
- **Soğuk performans:** −10 °C'de tepe güç ~12 kW; sürüş öncesi ön ısıtma gerekir (5 kWh,
  şebekeden). Li-iyon da benzer ön şartlandırma yapar ama daha az.
- **Maliyet:** kloso-borat tuzlarının bugünkü fiyatı laboratuvar ölçeğindedir. Ekonomik
  eşik SE ≤ 20–25 USD/kg; bu NaBH₄ → B₂H₆/B₁₀H₁₄ → Na₂B₁₂H₁₂/Na₂B₁₀H₁₀ rotasının
  ölçeklenmesini gerektirir.
- **Ömür:** katı hâl Na hücrelerinde 1000+ çevrim henüz laboratuvar ölçeğinde gösterilmiştir;
  ticari EV için 1500–3000 çevrim hedefi doğrulanmalıdır.

Ayrıntılar: `docs/02` (kimya), `docs/03` (malzeme/üretim), `docs/04` (hücre/paket),
`docs/05` (güvenlik/çevre), `docs/06` (riskler ve yol haritası), `cikti/RAPOR.md` (sayılar).
