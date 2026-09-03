# 04 — Hücre, Paket ve Araç Entegrasyonu (A6 Sistem Mühendisi, A4 Geometri)

Tüm sayılar `python -m borpil.cli rapor` çıktısından alınmıştır (`cikti/RAPOR.md`).

## 4.1 Hücre: BorPil-A pouch, 63 Ah

Çift taraflı tekrar birimi (536 µm, 102.4 mg/cm², 6.0 mAh/cm²):

| Katman | Kalınlık (µm) | Kütle (mg/cm²) | İşlev |
|---|---:|---:|---|
| Al folyo (katot) | 12 | 3.24 | akım toplayıcı |
| NVP/SE kompozit katot | 180 | 38.96 | 3 mAh/cm², %70 NVP |
| Kloso-borat ayırıcı | 30 | 4.50 | tek iyon iletken, yalıtkan |
| Na metal (şarjlı) | 46.5 | 4.51 | 26.5 µm döngüsel + 20 µm fazla |
| Al folyo (anot) | 12 | 3.24 | paylaşımlı |
| Na metal | 46.5 | 4.51 | |
| Ayırıcı | 30 | 4.50 | |
| Katot | 180 | 38.96 | |

- Yığın: **197 Wh/kg, 377 Wh/L**. Hücre (100 × 300 mm, 35 birim, Al-laminat kılıf, tab):
  **63 Ah, ~1.1 kg, ~0.63 L → 191 Wh/kg, 337 Wh/L**, 3.37 V nominal, 2.3–3.7 V pencere.
- Element bütçesi: B 0.95, Na 1.22, V 0.60, **Li 0.00** kg/kWh.
- 45 °C'de σ = 3.1 mS/cm; ASR bütçesi: ayırıcı 1.0 + katot kompozit ~13 + arayüzler 15 ≈ 29 Ω·cm²
  → 63 Ah hücrede 1.4 mΩ; 1C'de 88 mV kayıp.
- Tasarım kaldıraçları (`cikti/duyarlilik.png`): ayırıcı 30 → 20 µm: +4 Wh/kg; yükleme
  3 → 4 mAh/cm²: +10 Wh/kg; anotsuz: +8 Wh/kg. 2. nesil hedefi 215–230 Wh/kg (NVP ile).

## 4.2 Paket: 75 kWh, 400 V, CTP (cell-to-pack)

| Parametre | Değer |
|---|---|
| Mimari | **119s3p**, 357 hücre, 401 V nominal (274–440 V) |
| Enerji | 75.8 kWh brüt, 69.7 kWh kullanılabilir (%92 SOC penceresi) |
| Kütle / hacim | **521 kg / 362 L** → 145 Wh/kg, 209 Wh/L (hücre→paket 0.76 / 0.62) |
| Sürekli güç | 80 kW (≈1C, 3.2 mA/cm²) |
| Tepe güç (10 s) | 200 kW hedef; model 45 °C'de ~250 kW, 25 °C'de ~120 kW, −10 °C'de ~20 kW |
| Hızlı şarj | 1. nesil 75 kW (1C; Na kaplama kritik akım yoğunluğu ile sınırlı) |
| Bor / Na / V | 72 / 93 / 46 kg |
| Maliyet (varsayımsal) | 15.7 kUSD → 207 USD/kWh (SE 50 USD/kg); 140 USD/kWh (SE 20 USD/kg) |

Pouch hücreler kalınlık ekseninde yığılır; her 8 hücre arasına 2 mm yaylı basınç plakası
(1–2 MPa yığın basıncı katı hâl için zorunludur). Modülsüz CTP: hücreler doğrudan
alüminyum tepsiye, altta 12 mm aerojel yalıtım, üstte kompozit kapak. 800 V varyantı:
238s… (`borpil paket A --volt 800`).

### Yığın basıncı ve geometri
Katı-katı temas için hücre başına ~1 MPa → 300 cm² hücrede 3 kN. Yaylı plaka (disk yaylar)
Na metalin döngüsel kalınlık değişimini (±26 µm/katman × 70 katman ≈ ±1.8 mm/hücre) karşılar.
Bu, tasarımın en önemli mekanik gereksinimidir ve modül-içi yay katsayısı bu strok için
seçilir.

## 4.3 Isıl yönetim: "sıcak batarya" stratejisi

Kloso-borat iletkenliği sıcaklıkla artar; hücre 45–60 °C'de en iyi çalışır ve yanıcı
elektrolit olmadığı için 60 °C güvenlik açısından sorun değildir. Bu, Li-iyon'un tam tersi
bir ısıl felsefe gerektirir:

- **Yalıtım** ön planda: 12 mm aerojel (k = 0.022 W/m·K), 5.5 m² yüzey → UA ≈ 10 W/K.
  45 °C paket, 5 °C ortamda 400 W kaybeder; sürüşte I²R ısısı (80–220 W ortalama) bunun
  yarısını karşılar; kalan PTC ısıtıcıdan (1 kW sınıfı) gelir.
- **Ön ısıtma:** −10 → 25 °C için 5.1 kWh (paket ısı kapasitesi ~1 kJ/kg·K). Şebekeye
  bağlıyken yapılır; bağlı değilse 6 kW ısıtıcı + kendi I²R ısısı ile ~30 dk içinde 25 °C.
  Simülasyon (−10 °C senaryosu): menzil 443 km (20 °C'de 489 km), min hücre gerilimi 2.74 V.
- **Soğutma:** yalnız hızlı şarjda ve >60 °C'de; düşük debili sıvı plaka. Li-iyon paketlerin
  aksine soğutma sistemi boyutlandırmada tali kalır.
- **Park:** paketin soğumasına izin verilir (kendi kendine deşarj kloso-boratta ihmal
  edilebilir; Na/SE arayüzü oda sıcaklığında kararlı).

## 4.4 Araç düzeyi sonuçlar (WLTP-benzeri sentetik çevrim)

C-segment: glider 1350 kg + 150 kg yük + 521 kg paket = 2021 kg; Cd 0.27, A 2.3 m², Crr 0.009.

| Senaryo | Menzil | Tüketim | Paket T | Min V/hücre |
|---|---:|---:|---:|---:|
| 20 °C, ısıtıcı kapalı | **489 km** | 14.7 kWh/100 km | 20 → 28 °C | 3.04 V |
| −10 °C, ısıtıcı 6 kW (hedef 25 °C) | 443 km | 16.3 | −10 → 25 °C | 2.74 V |
| 35 °C | 495 km | 14.5 | 35 → 39 °C | 3.10 V |

Not: sentetik çevrim 24.1 km / 1800 s (WLTP sınıf 3: 23.3 km / 1800 s); gerçek WLTP
noktalarıyla değiştirilebilir (`simulasyon.wltp_benzeri_cevrim`).

## 4.5 BMS ve elektrik mimarisi notları

- Düz OCV platosu (3.2–3.4 V arası %90 SOC) → SOC tahmini için coulomb sayımı + uçlardaki dik
  kollar (3.45 V üstü, 2.9 V altı) ile yeniden kalibrasyon; Li-iyon LFP ile aynı sınıf zorluk.
- Hücre dengeleme: pasif (düz platoda küçük akım yeter).
- Sıcaklık sensörü yoğunluğu Li-iyon'dan az (ısıl kaçak yok), ancak **arayüz direnci
  izleme** (EIS/DC darbe) Na dendrit erken uyarısı için eklenir.
- Tepe güç sıcaklığa çok bağımlı → BMS güç sınırı haritası T–SOC düzleminde (`simulasyon.maks_guc_kW`).
