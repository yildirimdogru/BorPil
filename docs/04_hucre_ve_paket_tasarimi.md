# 04 — Hücre, Paket ve Araç Entegrasyonu (A6 Sistem Mühendisi, A4 Geometri)

Tüm sayılar `python -m borpil.cli rapor` çıktısından alınmıştır (`cikti/RAPOR.md`). Kurul kararı
(docs/07): 1. nesil **ticari baz çizgisi BorPil-A-alt**, **hedef/üst bant BorPil-A**; ikisi yan yana verilir.

## 4.1 Hücre

Çift taraflı tekrar birimi (hedef A: 530 µm, 96.2 mg/cm²; baz A-alt: 650 µm, 111 mg/cm²; 6.0 mAh/cm²):

| Katman | Hedef A | Baz A-alt | İşlev |
|---|---:|---:|---|
| Al folyo (katot) | 12 µm | 12 µm | akım toplayıcı |
| NVP/SE kompozit katot (%71 NVP, %25 SE, %2 C+CNT, %2 NBR; ALD kaplamalı NVP) | 180 µm | 180 µm | 3 mAh/cm² |
| Kloso-borat ayırıcı | 30 µm | **60 µm** | tek iyon iletken |
| Na metal fazlası (şarjlı kalınlık) | 20 µm (46.5) | **50 µm** (76.5) | döngüsel Na katot formülünde |
| Al folyo (anot) | 12 µm | 12 µm | paylaşımlı |
| Arayüz ASR (45 °C) | 15 Ω·cm² | **30 Ω·cm²** | |

- **Hedef A:** yığın 210 Wh/kg / 382 Wh/L; hücre **203 Wh/kg, 341 Wh/L**.
- **Baz A-alt:** yığın 182 / 311; hücre **177 Wh/kg, 279 Wh/L** (61 Ah, 1.13 kg pouch-in-frame öncesi).
- Element bütçesi (A / A-alt): B 0.95 / 1.25, Na 0.97 / 1.37, V 0.60 / 0.60, **Li 0** kg/kWh.
- 45 °C'de σ = 3.1 mS/cm; toplam ASR A: 29 Ω·cm² (1.4 mΩ/hücre), A-alt: 45 Ω·cm². 25 °C'de ~82 / 130,
  −10 °C'de ~760 / 1240 Ω·cm² (arayüz Ea 0.45 eV baskın).
- Model uyarısı: NVP kesim potansiyeli (~3.8 V) hidroboratın termodinamik oksidasyon sınırının (3.0 V)
  üstünde → çalışma **zorunlu ALD kaplama** (NaNbO₃/Na₃PO₄, 5–10 nm) ile pasifleştirici arayüze dayanır;
  A0 (NaCrO₂) paralel nitelendirme hattı.
- **Format (kurul P10):** pouch-in-frame — çelik/kompozit çerçeve + disk yay (k ≈ 20 N/mm, 2 mm strok,
  her 8 hücre), 1.2 ± 0.3 MPa; şarjda hücre kalınlığı ~1.9 mm (%10) artar. Al–Al ultrasonik tab, 0.3 mm
  (sürekli 2.2 A/mm²).

## 4.2 Paket: 74–76 kWh, 120s3p, 3 bağımsız dizi

| Parametre | Baz A-alt | Hedef A |
|---|---:|---:|
| Mimari | **120s3p**, 360 hücre × 61 Ah, 404 V nominal (283–452 V); **3 bağımsız 120s dizi** (dizi akım sensörü + kontaktör) | aynı |
| Enerji | 74.2 kWh brüt / 68.3 kWh kullanılabilir (%92) | aynı |
| Kütle / hacim | **596 kg / 512 L → 125 Wh/kg, 145 Wh/L** | 519 kg / 418 L → 143 Wh/kg, 177 Wh/L |
| Sürekli / tepe güç | 80 kW (3.2 mA/cm²) / 200 kW hedef — model 45 °C'de ~210, 25 °C'de ~70, −10 °C'de ~7 kW | aynı |
| Hızlı şarj | 75 kW, paket ≥ 44 °C (CCD/1.5); DC şarjda 20 kW şebeke ısıtıcı | ≥ 45 °C |
| Bor / Na / V | 92 / 102 / 45 kg | 70 / 72 / 45 kg |
| Maliyet (SE 50 USD/kg, verim %75, ×1.75, +32) | **412 USD/kWh** | 358 USD/kWh |
| Maliyet (SE 25, verim %90, ×1.55) | 234 | 214 |

Hücre→paket oranları 0.72 (kütle) / 0.52 (hacim) + 12 kg basınç fikstürü; 12 mm aerojel (≈66 L);
modülsüz CTP, disk yaylı plakalar. 800 V sınıfı: ≤ 228s (`borpil paket A --volt 770`); 237s pencere
893 V ile 1200 V SiC DC-link tavanını (860 V) aşar — model KRİTİK uyarı verir.

### Elektrik mimarisi ve koruma (kurul P3, P4, P8, P9)
- Tepe akım ~495 A; busbar + kontaktör + sigorta ≈ 2 mΩ; ön şarj 100 Ω / ~60 ms; izolasyon ≥ 500 Ω/V.
- **Kısa devre akımı sıcaklığa 25× bağımlı:** 45 °C'de 5–8 kA, −10 °C'de 190–310 A (sürekli akımın
  altında). Sigorta (≥ 16 kA kesme) tek başına yetmez → akım-plausibilite (paket ↔ invertör/şarj) ve
  dI/dt ile kontaktör açma (ASIL C).
- **Isıtıcı güvenlik zinciri:** ısıtıcı takılı kalırsa +17–20 K/h (3 kW), 6 kW'ta +40 K/h ve ~95 dk'da
  Na erimesi → bağımsız 80 °C termal kesici + ayrı ısıtıcı kontaktörü + çift NTC; ISO 26262 ASIL D
  → B(D)+B(D) ayrıştırma. BMS yazılım sınırları 80 °C güç kesme / 90 °C ayırma.
- **3 bağımsız dizi:** dizi akım dengesizliği Na dendrit yumuşak kısa devre dedektörü; arızalı dizi
  izole edilir, 2/3 güçle sürüş. Ek maliyet ~225 USD.

## 4.3 Isıl yönetim: "sıcak batarya" stratejisi (kurul P5–P7, P19)

Kloso-borat iletkenliği sıcaklıkla artar; hücre 35–60 °C'de en iyi çalışır; yanıcı elektrolit yok.
Sınır Na'nın erime noktasıdır (97.8 °C).

- **Sürüşte hedef 35 °C:** 3 kW PTC + **0.8 kW tahrik atık ısısı** (termostatik vana, hedef + 5 K'de
  kapanır). 20 °C ortamda ısıtıcı 2.0 kWh çeker (menzil 457 km; ısıtıcısız 472 km ama 25 °C'de tepe güç
  70 kW'a düşer). −10 °C'de atık ısı ısıtıcı enerjisini 9.2 → 5.7 kWh'ye indirir.
- **DC şarjda hedef 45 °C, ısıtıcı şebekeden 20 kW:** −10 °C'den 10 → 80 % SOC **54 dk** (6 kW paket
  ısıtıcısıyla 95 dk olurdu). Şebekeden ön ısıtılmış pakette −10 °C menzili 474 km (ısıtıcısız soğuk
  başlangıçta 440 km).
- **Darbe (AC) ısıtma (yol haritası):** invertör/motor üzerinden kHz akımla hücrenin kendi bulk
  direnci ısıtılır; −20 °C'de 42 kW, ısındıkça kendini sınırlar (25 °C'de 2.6 kW). **−20 → 0 °C 10 dk /
  3.7 kWh** — derin soğuktan çıkış aracı. Na/SE arayüzünün kHz dayanımı EIS ile doğrulanacak; gen-1
  baz değil.
- **Soğutma:** 60 °C üstünde ≥ 3 kW sıvı plaka; hızlı şarjda paket 45 → 55–57 °C.
- **Park / V2G:** 35 °C tutulmaz (günde 3.6–11 kWh); paket soğur, V2G akımı CCD(T) ile kapılanır.
- **Stres senaryosu** (−20 °C, PTC arızalı): araç çevrimi izleyemez (güç kısıtı ~1.6 saat, 16 kWh açık,
  1.8 kWh rejen mekanik frene); atık ısı ile paket zamanla 31 °C'ye çıkar. BMS sürücüyü bilgilendirir.

## 4.4 Araç düzeyi sonuçlar (WLTP-benzeri sentetik çevrim)

C-segment: glider 1350 kg + 150 kg yük + paket (596 / 519 kg) = 2096 / 2019 kg; Cd 0.27, A 2.3 m²,
Crr 0.009. Tüketim bataryadan çekilen enerjidir (ısıtıcı dâhil, şebeke şarj kayıpları hariç).

| Senaryo | Menzil baz / hedef | Tüketim (baz) | Paket T | Isıtıcı | Güç kısıtı |
|---|---:|---:|---:|---:|---:|
| 20 °C, ısıtıcı 35 °C + atık ısı (strateji) | **457 / 474 km** | 15.0 kWh/100 km | 20 → 40 °C | 2.0 kWh | — |
| 20 °C, ısıtıcı kapalı | 472 / 485 | 14.5 | 20 → 40 | 0 | — |
| −10 °C, soğuk başlangıç, ısıtıcı 35 °C | 440 / 454 | 15.5 | −10 → 40 | 5.7 | 759 s / 1.8 kWh |
| −10 °C, şebekeden 35 °C'ye ön ısıtılmış | **474 / 486** | 14.4 | 35 → 40 | 0 | — |
| −20 °C, PTC arızalı (stres) | çevrim izlenemez | — | −20 → 31 | 0 | 5781 s / 16.5 kWh |
| 35 °C | 475 / 486 | 14.4 | 35 → 42 | 0 | — |
| 40 °C, otoyol 130 km/h | 309 / 315 | 22.1 | 40 → 47 | 0 | — |

DC hızlı şarj 10 → 80 % (150 kW cihaz, 20 kW şebeke ısıtıcı), baz: 45 °C **32 dk**, 25 °C 38 dk,
0 °C 49 dk, −10 °C 54 dk; sınırlayıcı her durumda CCD (şarj cihazı değil).

## 4.5 BMS ve elektrik mimarisi notları (kurul P17)

- **SOC:** düz OCV platosu (%10–90 arası ~1 mV/%SOC modelde; gerçek NVP daha düz) → coulomb sayımı
  birincil (%0.1 şönt), her tam şarjda üst dizde (>3.5 V) yeniden kalibrasyon; alt uçtan kalibrasyon
  pratikte yok.
- **R(T) artığı:** dR/dT ≈ −5…−7 %/K → direnç ölçümü ±0.5 K hassasiyetinde termometre; kalıcı
  R_ölç/R_model sapması arayüz değişimi/yumuşak kısa erken uyarısı (EIS yetenekli AFE).
- **Dengeleme:** pasif 150–300 mA/kanal, yalnız üst dizde; >50 mA sürekli sapma = arıza.
- **Sensörler:** gerilim ±2 mV, akım ±%0.5 (ofset ≤ 20 mA), NTC ≥ 1/6 hücre + ısıtıcı plakasında çift.
- **Güç/şarj haritası (T–SOC):** deşarj 25 °C 70 kW → 45 °C 210 kW; şarj/rejen 25 °C 26 kW → 45 °C
  78 kW (`cikti/isitma_ve_sarj.png`). Soğukta rejen fazlası mekanik frene.
- **Hücre eşleştirme:** ±1.5–2 % kapasite binning (3p dizi dengesizliği < %3).
