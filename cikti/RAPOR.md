# BorPil — Hesaplanmış Tasarım Raporu (otomatik üretildi)

Bu dosya `borpil rapor` komutuyla üretilir; tüm sayılar `borpil` paketindeki modellerden gelir.

## 1. Teorik sınırlar (termodinamik)

| Kimya | Reaksiyon | E° (V) | Kapasite (mAh/g reaktan) | Wh/kg reaktan | Wh/kg ürün (O₂ dâhil) |
|---|---|---:|---:|---:|---:|
| Bor-hava (teorik) | 4B + 3O2 → 2B2O3 | 2.063 | 7438 | 15345 | 4765 |
| Li-hava (Li2O) | 4Li + O2 → 2Li2O | 2.908 | 3862 | 11231 | 5217 |
| Na-hava (Na2O) | 4Na + O2 → 2Na2O | 1.946 | 1166 | 2268 | 1683 |
| Mg-hava (MgO) | 2Mg + O2 → 2MgO | 2.950 | 2205 | 6506 | 3924 |
| Doğrudan borhidrür yakıt pili (DBFC, teorik) | NaBH4 + 2O2 → NaBO2 + 2H2O | 1.647 | 5667 | 9333 | 3467 |

DBFC pratik tahmin: %20 NaBH₄ çözeltisi, 1.0 V, %75 yakıt kullanımı → 850 Wh/kg çözelti, 531 Wh/kg sistem; NaBO₂→NaBH₄ rejenerasyonu dâhil gidiş-dönüş verimi **%16** (rejenerasyon verimi %35 varsayımı). Sonuç: DBFC ana depolama değil, menzil uzatıcı/yakıt yoludur.

## 2. Elektrolit: kloso-borat iletkenliği

| Elektrolit | σ(−10 °C) mS/cm | σ(25 °C) | σ(45 °C) | σ(60 °C) | Ea (eV) | ASR 30 µm @45 °C (Ω·cm²) |
|---|---:|---:|---:|---:|---:|---:|
| Na2B12H12 | 1.59e-06 | 0.0001 | 0.000708 | 0.00263 | 0.80 | 4236.74 |
| Na2B10H10 | 2.67e-05 | 0.001 | 0.00554 | 0.0175 | 0.70 | 541.12 |
| Na2(B12H12)(B10H10) | 0.148 | 1.17 | 3.12 | 6.02 | 0.40 | 0.96 |
| NaCB11H12 | 0.000448 | 0.01 | 0.0434 | 0.116 | 0.60 | 69.11 |
| Na2(CB9H10)(CB11H12) | 19.2 | 70 | 129 | 195 | 0.25 | 0.02 |

Geometri: [B12H12]2-: kenar 1.78 Å, R_B 1.69 Å, R_H 2.89 Å, etkin yarıçap 3.99 Å, etkin hacim 267 Å³. Süperiyonik bcc Na₂B₁₂H₁₂ kafesi a = 7.38 Å; anyon sert-küre yarıçapı 3.20 Å; tetrahedral site boşluk yarıçapı 0.93 Å (Na⁺ 1.02 Å); Na site doluluğu 0.33 → yüksek vakans oranı.

## 3. Hücre varyantları

```
== BorPil-A (Na | Na2(B12H12)(B10H10) | NVP) ==
Katot: Na3V2(PO4)3 (NASICON, NVP) | SE: Na2(B12H12)0.5(B10H10)0.5 (eş-molar kloso-borat karışımı) | Anot: Na metal
Çalışma sıcaklığı 45 °C → σ = 3.12 mS/cm, toplam ASR ≈ 29.2 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                 179.7 µm    38.96 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Katot kompozit                 179.7 µm    38.96 mg/cm²
Tekrar birimi: 536 µm, 102.4 mg/cm², 6.0 mAh/cm², 3.37 V
Yığın: 197 Wh/kg, 377 Wh/L
Hücre (100×300 mm pouch, 33 birim): 59.4 Ah, 1047 g, 594 mL → 191 Wh/kg, 337 Wh/L
Element bütçesi: B 0.95 kg/kWh, Na 1.22 kg/kWh, V 0.60 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 119 USD/kWh
```

```
== BorPil-A0 (Na | Na2(B12H12)(B10H10) | NaCrO2) — pencere içi muhafazakâr ==
Katot: NaCrO2 (O3 tabakalı oksit) | SE: Na2(B12H12)0.5(B10H10)0.5 (eş-molar kloso-borat karışımı) | Anot: Na metal
Çalışma sıcaklığı 45 °C → σ = 3.12 mS/cm, toplam ASR ≈ 24.6 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                 147.4 µm    37.27 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Katot kompozit                 147.4 µm    37.27 mg/cm²
Tekrar birimi: 472 µm, 99.0 mg/cm², 6.0 mAh/cm², 2.95 V
Yığın: 179 Wh/kg, 375 Wh/L
Hücre (100×300 mm pouch, 33 birim): 59.4 Ah, 1013 g, 524 mL → 173 Wh/kg, 335 Wh/L
Element bütçesi: B 1.05 kg/kWh, Na 1.55 kg/kWh, V 0.00 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 111 USD/kWh
```

```
== BorPil-A-Fe (Na | Na2(B12H12)(B10H10) | Na2/3Fe1/2Mn1/2O2) — vanadyumsuz düşük maliyet ==
Katot: P2-Na2/3Fe1/2Mn1/2O2 (tabakalı Fe/Mn oksit) | SE: Na2(B12H12)0.5(B10H10)0.5 (eş-molar kloso-borat karışımı) | Anot: Na metal
Çalışma sıcaklığı 45 °C → σ = 3.12 mS/cm, toplam ASR ≈ 23.1 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                 116.2 µm    28.57 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Na metal anot (şarjlı)          46.5 µm     4.51 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Katot kompozit                 116.2 µm    28.57 mg/cm²
Tekrar birimi: 409 µm, 81.6 mg/cm², 6.0 mAh/cm², 2.75 V
Yığın: 202 Wh/kg, 403 Wh/L
Hücre (100×300 mm pouch, 33 birim): 59.4 Ah, 838 g, 456 mL → 195 Wh/kg, 358 Wh/L
Element bütçesi: B 0.95 kg/kWh, Na 1.28 kg/kWh, V 0.00 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 91 USD/kWh
```

```
== BorPil-B (Na | Na2(CB9H10)(CB11H12) | NVPF) — 2. nesil yüksek performans ==
Katot: Na3V2(PO4)2F3 (NVPF) | SE: Na2(CB9H10)(CB11H12) (karışık karba-kloso-borat) | Anot: Na metal
Çalışma sıcaklığı 35 °C → σ = 95.99 mS/cm, toplam ASR ≈ 8.5 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                 237.6 µm    47.62 mg/cm²
  - SE ayırıcı                      20.0 µm     2.50 mg/cm²
  - Na metal anot (şarjlı)          45.4 µm     4.40 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Na metal anot (şarjlı)          45.4 µm     4.40 mg/cm²
  - SE ayırıcı                      20.0 µm     2.50 mg/cm²
  - Katot kompozit                 237.6 µm    47.62 mg/cm²
Tekrar birimi: 630 µm, 115.5 mg/cm², 8.0 mAh/cm², 3.90 V
Yığın: 270 Wh/kg, 495 Wh/L
Hücre (100×300 mm pouch, 25 birim): 60.0 Ah, 897 g, 530 mL → 261 Wh/kg, 442 Wh/L
Element bütçesi: B 0.65 kg/kWh, Na 0.77 kg/kWh, V 0.52 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 458 USD/kWh
```

```
== BorPil-C (Sert karbon | Na2(B12H12)(B10H10) | NVP) — dendritsiz güvenli varyant ==
Katot: Na3V2(PO4)3 (NASICON, NVP) | SE: Na2(B12H12)0.5(B10H10)0.5 (eş-molar kloso-borat karışımı) | Anot: Sert karbon (hard carbon)
Çalışma sıcaklığı 45 °C → σ = 3.12 mS/cm, toplam ASR ≈ 29.2 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                 179.7 µm    38.96 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Sert karbon (hard carbon) kompozit anot   123.5 µm    17.33 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Sert karbon (hard carbon) kompozit anot   123.5 µm    17.33 mg/cm²
  - SE ayırıcı                      30.0 µm     4.50 mg/cm²
  - Katot kompozit                 179.7 µm    38.96 mg/cm²
Tekrar birimi: 690 µm, 128.1 mg/cm², 6.0 mAh/cm², 3.17 V
Yığın: 149 Wh/kg, 276 Wh/L
Hücre (100×300 mm pouch, 33 birim): 59.4 Ah, 1306 g, 762 mL → 144 Wh/kg, 247 Wh/L
Element bütçesi: B 1.34 kg/kWh, Na 0.95 kg/kWh, V 0.64 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 161 USD/kWh
```

```
== BorPil-S (Na | Na2(CB9H10)(CB11H12) | S) — uzun vade Na-S ==
Katot: S (Na-S, Na2S'e kadar) | SE: Na2(CB9H10)(CB11H12) (karışık karba-kloso-borat) | Anot: Na metal
Çalışma sıcaklığı 60 °C → σ = 194.56 mS/cm, toplam ASR ≈ 20.1 Ω·cm²
Katmanlar (tekrar birimi):
  - Al folyo (katot)                12.0 µm     3.24 mg/cm²
  - Katot kompozit                  71.6 µm    10.00 mg/cm²
  - SE ayırıcı                      20.0 µm     2.50 mg/cm²
  - Na metal anot (şarjlı)          45.4 µm     4.40 mg/cm²
  - Al folyo (anot)                 12.0 µm     3.24 mg/cm²
  - Na metal anot (şarjlı)          45.4 µm     4.40 mg/cm²
  - SE ayırıcı                      20.0 µm     2.50 mg/cm²
  - Katot kompozit                  71.6 µm    10.00 mg/cm²
Tekrar birimi: 298 µm, 40.3 mg/cm², 8.0 mAh/cm², 1.80 V
Yığın: 357 Wh/kg, 483 Wh/L
Hücre (100×300 mm pouch, 25 birim): 60.0 Ah, 321 g, 256 mL → 336 Wh/kg, 422 Wh/L
Element bütçesi: B 0.58 kg/kWh, Na 0.74 kg/kWh, V 0.00 kg/kWh, Li 0.00 kg/kWh
Malzeme maliyeti (varsayımsal ölçek): 382 USD/kWh
```

## 4. Paket (BorPil-A, 75 kWh, 400 V)

```
== Paket: C-segment sedan/SUV — 75 kWh hedef, 400 V ==
Hücre: BorPil-A (Na | Na2(B12H12)(B10H10) | NVP)
Mimari: 119s3p = 357 hücre × 63.0 Ah, 401 V nominal
Enerji: 75.8 kWh brüt / 69.7 kWh kullanılabilir
Kütle 521 kg (145 Wh/kg), hacim 362 L (209 Wh/L)
Element bütçesi: B 72.1 kg, Na 92.7 kg, V 45.7 kg, Li 0.0 kg
Akım yoğunluğu: sürekli 3.17 mA/cm², tepe 7.92 mA/cm²
Isıl: kayıp 10.1 W/K (ΔT=40 K → 403 W); -10→25 °C ön ısıtma 5.1 kWh
Maliyet (varsayımsal ölçek): 15,652 USD → 207 USD/kWh
```

## 5. Sürüş simülasyonu (WLTP-benzeri sentetik çevrim, C-segment)

| Senaryo | Menzil (km) | Tüketim (kWh/100 km) | Paket T başlangıç→bitiş (°C) | Min hücre gerilimi (V) | Ort. I²R ısı (W) |
|---|---:|---:|---:|---:|---:|
| 20 °C, ısıtıcı yok | 489 | 14.7 | 20→28 | 3.04 | 168 |
| −10 °C, 25 °C'ye ısıtıcı (6 kW) | 443 | 16.3 | -10→25 | 2.74 | 222 |
| 35 °C | 495 | 14.5 | 35→39 | 3.10 | 83 |

Araç toplam kütlesi 2021 kg (glider + yük + paket).

## 6. Li-iyon ile karşılaştırma (75 kWh paket)

| Kimya | Wh/kg (hücre) | Wh/L (hücre) | USD/kWh (hücre, varsayım) | Li (kg/75 kWh) | B (kg) | Co (kg) | Ni (kg) | Yanıcı elektrolit | Paket kütlesi (kg) | Paket hacmi (L) |
|---|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|
| BorPil-A | 191 | 337 | 185 | 0.0 | 72.1 | 0.0 | 0.0 | hayır | 521 | 362 |
| BorPil-A0 | 173 | 335 | 172 | 0.0 | 80.0 | 0.0 | 0.0 | hayır | 576 | 365 |
| BorPil-A-Fe | 195 | 358 | 141 | 0.0 | 71.9 | 0.0 | 0.0 | hayır | 508 | 339 |
| BorPil-B | 261 | 442 | 710 | 0.0 | 48.7 | 0.0 | 0.0 | hayır | 379 | 274 |
| BorPil-C | 144 | 247 | 249 | 0.0 | 101.5 | 0.0 | 0.0 | hayır | 689 | 492 |
| BorPil-S | 336 | 422 | 593 | 0.0 | 43.7 | 0.0 | 0.0 | hayır | 292 | 285 |
| Li-iyon NMC811 (pouch, 2025 sınıfı) | 265 | 700 | 100 | 8.2 | 0.0 | 6.8 | 56.2 | evet | 393 | 179 |
| Li-iyon LFP (prizmatik, 2025 sınıfı) | 170 | 380 | 75 | 6.8 | 0.0 | 0.0 | 0.0 | evet | 613 | 329 |

## 7. Grafikler

![iletkenlik](iletkenlik_arrhenius.png)

![enerji](enerji_yogunlugu.png)

![duyarlilik](duyarlilik.png)

![guc](guc_ve_desarj.png)

![katman](katman_yigini.png)

![iko](b12h12_ikosahedron.png)
