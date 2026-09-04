# 01 — Tasarım Özeti (Yönetici Özeti)

## Ne öneriyoruz?

**BorPil-A:** Lityum içermeyen, **bor esaslı katı elektrolitli**, sodyum-metal anotlu,
tamamen katı hâl bir elektrikli araç bataryası.

```
   Al folyo | Na₃V₂(PO₄)₃ (ALD kaplı) + Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ kompozit katot | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ ayırıcı | Na metal | Al folyo
```

Bor, hücrede **enerji taşıyan iyonun otoyolu**dur: [B₁₂H₁₂]²⁻ ve [B₁₀H₁₀]²⁻ kafes anyonları
oda sıcaklığında hızla dönen, geniş boşluklu bir kristal kafes kurar; Na⁺ bu kafes içinde
düşük enerji engeliyle (Ea ≈ 0.4 eV) hareket eder. Bu sınıf ("hidroborat" veya
"kloso-borat" elektrolitler) 2014'ten bu yana literatürde en hızlı gelişen katı elektrolit
ailelerinden biridir ve Li-iyon'daki yanıcı organik elektrolitin yerini alır.

İki tur bağımsız inceleme (kimya/fizik + kod; elektrik-elektronik + üretici) ve kurul kararları
sonrasında 1. nesil **ticari baz çizgisi BorPil-A-alt** (60 µm elektrolit, 50 µm Na fazlası,
30 Ω·cm² arayüz — bugün üretilebilir), **hedef/üst bant BorPil-A** (30 µm / 20 µm / 15 Ω·cm²) olarak
belirlenmiştir (docs/07).

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
  şarttır (şebekeden). Deneysel doğrulama zorunlu.
- **Hidroborat oksidasyon sınırı ~3 V** (termodinamik); NVP'nin 3.37 V platosu ve ~3.8 V kesimi
  **zorunlu ALD kaplama** ile pasifleştirici arayüze dayanır; model bu durumu **uyarı** olarak
  bayraklar. A0 (NaCrO₂) paralel nitelendirme hattı.
- **Yalıtım + ısıtıcı yeni bir tehlike yaratır:** ısıtıcı takılı kalırsa paket 3 kW'ta +17–20 K/h ısınır
  ve saatler içinde Na erime noktasına yaklaşır → bağımsız 80 °C donanım kesici, ayrı kontaktör,
  çift NTC (ASIL D → B(D)+B(D)).
- **Soğukta sigorta çalışmaz:** −10 °C'de kısa devre akımı (190–310 A) sürekli çalışma akımının altında;
  akım-plausibilite + dI/dt ile kontaktör açma gerekir.
- **Maliyet:** kloso-borat tuzlarının bugünkü fiyatı laboratuvar ölçeğindedir (>1000 USD/kg); gen-1
  verimi %60–75. Gerçekçi gen-1 paket maliyeti **360–410 USD/kWh** (SE 50 USD/kg); ekonomik hedef
  bandı 165–200 USD/kWh için SE ≤ 25 USD/kg, verim ≥ %90 ve 10 GWh ölçeği **birlikte** gerekir.
  120 USD/kWh mevcut malzeme karmasıyla ulaşılabilir değildir.
- **Ömür:** katı hâl Na hücrelerinde 1000+ çevrim henüz laboratuvar ölçeğinde; 1500–3000 çevrim
  hedefi ve 8 yıl / 160 000 km garanti riski doğrulanmalıdır.
- **Tedarik:** kloso-borat sentez kapasitesi bugün < 10 t/yıl (1 GWh için ~1400 t/yıl gerekir);
  vanadyum 45 kg/araç → A-Fe yolu paralel.

Ayrıntılar: `docs/02` (kimya), `docs/03` (malzeme/üretim), `docs/04` (hücre/paket/ısıl/BMS),
`docs/05` (güvenlik/çevre), `docs/06` (riskler, 1. tur hakem bulguları, yol haritası),
`docs/07` (elektrik-elektronik ve üretici incelemeleri, kurul kararları),
`docs/08` (paket maden ve element bütçesi),
`docs/09` (ısıl ekosistem ve soğuk başlangıç — 3. tur kurul),
`docs/urun/` (satışa-hazır ürün formu: veri formu, entegrasyon, güvenlik/garanti, broşür),
`cikti/RAPOR.md` (sayılar).
