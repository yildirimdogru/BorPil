# BorPil EV-74 — Teknik veri formu

**Belge:** BP-TD-074 · Rev A  
**Ürün ailesi:** BorPil EV-74 katı hâl çekiş bataryası  
**Dil:** Türkçe (OEM İngilizce özet §11)  
**Gizli:** OEM ve yetkili entegratör

---

## 1. Ürün tanımı

BorPil EV-74, C-segment binek ve hafif SUV için **lityumsuz, yanıcı sıvı elektrolitsiz**,
tamamen katı hâl bir çekiş paketiidir. İyonik iletim, Na⁺’nın eş-molar kloso-borat kafesinde
(`Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅`) hareketine dayanır; enerji sodyum-metal anot ve NASICON
Na₃V₂(PO₄)₃ (NVP, ALD kaplamalı) katotta depolanır. Bor, hücrede katkı değil **iyon otoyoludur**.

| Katalog | Tasarım kodu | Konum |
|---|---|---|
| **EV-74 Standard** | BorPil-A-alt | **Hacim ürünü** — 60 µm SE, 50 µm Na fazlası |
| EV-74 Pro | BorPil-A | İnce film hattı — 30 µm SE, 20 µm Na, daha yüksek Wh/kg |
| EV-74 Fe | BorPil-A-Fe | Vanadyumsuz katot (Na-Fe-Mn oksit); aynı paket zarfı |

Aksi belirtilmedikçe bu form **Standard** içindir. Pro / Fe sütunları karşılaştırmalı tablolardadır.

**Hücre kimyası (Standard / Pro):**

```
Al folyo | NVP (ALD) + kloso-borat kompozit | kloso-borat ayırıcı | Na metal | Al folyo
```

Katot reçetesi (kütle): %71 NVP / %25 SE / %2 C+CNT / %2 NBR.

---

## 2. Elektrik — paket

| Parametre | Standard | Pro | Birim / koşul |
|---|---:|---:|---|
| Brüt enerji | **74,2** | 74,2 | kWh |
| Kullanılabilir enerji | **68,3** | 68,3 | kWh (%92 SOC penceresi) |
| Mimari | 120s3p | 120s3p | 360 hücre; **3 bağımsız 120s dizi** |
| Hücre | 61,2 Ah pouch | 61,2 Ah | 100 × 300 mm, pouch-in-frame |
| Nominal gerilim | **404** | 404 | V (120 × 3,37 V) |
| Çalışma penceresi | **283–452** | 283–452 | V |
| Sürekli güç | 80 | 80 | kW, paket 45 °C |
| Tepe güç (10 s) | **~210** | ~210 | kW @ 45 °C; **~70 kW @ 25 °C; ~7 kW @ −10 °C** |
| DC hızlı şarj | **75** | 75 | kW, paket ≥ 44–45 °C |
| 10 → 80 % SOC | **32 / 38 / 54** | 34 / 39 / 53 | dk @ 45 / 25 / −10 °C (20 kW şebeke ısıtıcı) |
| Tepe akım | 495 | 495 | A |
| İzolasyon | ≥ 500 | ≥ 500 | Ω/V, HV–şasi |

800 V sınıfı: ayrı SKU, ≤ 228s; 237s pencere invertör DC-link tavanını aşar — sipariş etmeyin.

---

## 3. Mekanik ve ısıl

| Parametre | Standard | Pro |
|---|---:|---:|
| Paket kütlesi | **596 kg** | 519 kg |
| Paket hacmi | **512 L** | 418 L |
| Enerji yoğunluğu | **125 Wh/kg, 145 Wh/L** | 143 Wh/kg, 177 Wh/L |
| Hücre (pouch) | 177 Wh/kg, 279 Wh/L | 203 Wh/kg, 341 Wh/L |
| Ürün zarfı (taban) | **1600 × 1200 × 270 mm** | aynı ayak izi, daha alçak yığın |
| Yüzey (ısıl) | 5,5 m² | 5,5 m² |
| Hücre→paket | kütle 0,72; hacim 0,52 | aynı + 12 kg fikstür |
| Yığın basıncı | **1,2 ± 0,3 MPa** | disk yay, k ≈ 20 N/mm |
| Yalıtım | 12 mm aerojel keçe | k = 0,022 W/(m·K) |
| Isıtıcı | **3 kW PTC** (park/ön şart) | DC şarjda **20 kW şebekeden** |
| Atık ısı | **0,8 kW** tahrik (termostatik) | hedef 35 °C + 5 K’de kapanır |
| Soğutma | ≥ **3 kW** sıvı plaka, T ≥ 60 °C | hızlı şarjda 45 → 55–57 °C |
| Çalışma | sürüş **35 °C** hedef, şarj **45 °C**, tavan **60 °C** | “sıcak batarya” |
| Donanım kesici | **80 °C** bağımsız (BMS’ten ayrı) | Na e.n. 97,8 °C |
| BMS ayırma | 80 °C güç kesme / **90 °C** paket açma | çift NTC |

Parkta 35 °C tutulmaz. V2G akımı CCD(T) ile kapılanır.

---

## 4. Araç düzeyi (C-segment referans)

Referans araç: glider 1350 kg + 150 kg yük + paket; Cd 0,27; A 2,3 m²; Crr 0,009.
Tüketim bataryadan (ısıtıcı dâhil, şebeke şarj kaybı hariç). WLTP-benzeri sentetik çevrim.

| Senaryo | Standard | Pro |
|---|---:|---:|
| 20 °C, ısıl strateji (35 °C + atık ısı) | **457 km** (15,0 kWh/100 km) | 474 km |
| 20 °C, ısıtıcı kapalı | 472 km | 485 km |
| −10 °C, soğuk başlangıç | 440 km | 454 km |
| −10 °C, şebekeden ön ısıtılmış | **474 km** | 486 km |
| 40 °C, otoyol 130 km/h | 309 km | 315 km |

**Soğuk güç:** −10 °C’de tepe ~7 kW. Ön ısıtma (şebeke veya 3 kW PTC) **zorunlu** iş
gereksinimidir, opsiyon değildir.

---

## 5. Malzeme ve kritik metaller

Ayrıntı: `docs/08_paket_maden_ve_element_butcesi.md`.

| | Standard | Pro | Tipik NMC811 74 kWh |
|---|---:|---:|---:|
| Lityum | **0 kg** | 0 | ~8 kg |
| Kobalt / nikel | **0 / 0** | 0 / 0 | ~7 / 56 kg |
| Bakır (hücre) | **0** | 0 | folyo |
| Bor | **92 kg** | 70 kg | 0 |
| Sodyum | **102 kg** | 72 kg | — |
| Vanadyum | **45 kg** | 45 | 0 (Fe SKU: 0) |

---

## 6. Çevre ve kullanım sınırları

| | Değer |
|---|---|
| Depolama (sevk, %30 SOC) | −20…+45 °C, nem kontrollü kapalı kasa |
| Çalışma ortamı | −20…+45 °C ortam; paket kendi ısıl döngüsünü yönetir |
| IP | IP67 paket muhafaza (hedef sınıf); HV konnektör IP67 kilitli |
| Titreşim / darbe | UN 38.3 T3/T4; ECE R100 mekanik |
| Ezme / delme | UN 38.3 T6; GB 38031 — beklenen sonuç: yerel ısınma, paket çapında ısıl kaçak yok |
| Söndürme | **D sınıfı** + inert gaz; **modül düzeyinde su yasak** (Na metal) |

---

## 7. Arayüz özeti

Ayrıntı: entegrasyon kılavuzu.

- HV: 400 V sınıfı, 283–452 V, CCS Combo DC, 500 A cihaz tavanı  
- LV: 12 V BMS + PTC kontaktörü; ısıtıcıya **ayrı kontaktör**  
- Veri: CAN FD (500 kbit/s veya 2 Mbit/s), ISO 15118-2/20 DC  
- Soğutma: su-glikol, 3 kW plaka, 60 °C kapı  
- Mekanik: 8–12 M8/M10 taban pabucu, yığın basıncı araçtan bağımsız (iç yay)

---

## 8. Uyumluluk hedefi (homologasyon seti)

Satışa hazır üründe beklenen dosya:

- UN 38.3 (T1–T8) taşıma  
- ECE R100.03 çekiş bataryası  
- ISO 6469-1 / 6469-3 HV güvenlik  
- ISO 26262: ısıtıcı yolu **ASIL D → B(D)+B(D)**; aşırı şarj ASIL C  
- IEC 62660 hücre; GB 38031 (ihracat Çin)  
- UN/ECE R136 veya eşdeğeri (hafif ticari varyant)  
- REACH (kloso-borat tuzu kaydı); CLP etiket (Na metal, borat tozu işyeri)

---

## 9. Sipariş bilgisi

| Alan | Standard | Pro | Fe |
|---|---|---|---|
| Parça no. | BP-EV74-S-404 | BP-EV74-P-404 | BP-EV74-F-404 |
| Gerilim sınıfı | 400 V | 400 V | 400 V |
| Minimum sipariş | 1 paket (prototip hat) / 50 (seri) | aynı | aynı |
| Sevk SOC | %30 ± 5 | aynı | aynı |

---

## 10. Revizyon

| Rev | Tarih | Not |
|---|---|---|
| A | 2026-09 | Tasarım modeli A-alt / A / A-Fe sayılarıyla ilk ürün formu |

---

## 11. English summary (OEM)

BorPil EV-74 is a **lithium-free, all-solid-state** traction pack: Na metal | closo-borate
SE | ALD-coated NVP. Shipping SKU **Standard**: 74.2 kWh, 404 V, 120s3p with **three
independent strings**, 596 kg / 512 L, **125 Wh/kg**. Usable 68.3 kWh. No Li, Co, Ni or
Cu in the cell stack. **92 kg boron** per pack. DC charge 75 kW only with pack ≥ 44 °C
(10→80 % in 32 min at 45 °C). Drive target 35 °C (“warm battery”). Independent 80 °C
heater cut-off. Class D extinguishing; no water on modules. Full numbers: this datasheet
and `docs/08`.
