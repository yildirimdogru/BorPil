# 04 — Hücre, Paket ve Araç Entegrasyonu (A6 Sistem Mühendisi, A4 Geometri)

Tüm sayılar `python -m borpil.cli rapor` çıktısından alınmıştır (`cikti/RAPOR.md`).

## 4.1 Hücre: BorPil-A pouch, 63 Ah

Çift taraflı tekrar birimi (536 µm, 97.3 mg/cm², 6.0 mAh/cm²):

| Katman | Kalınlık (µm) | Kütle (mg/cm²) | İşlev |
|---|---:|---:|---|
| Al folyo (katot) | 12 | 3.24 | akım toplayıcı |
| NVP/SE kompozit katot | 180 | 38.96 | 3 mAh/cm², %70 NVP (Na₃V₂(PO₄)₃, deşarjlı hâl) |
| Kloso-borat ayırıcı | 30 | 4.50 | tek iyon iletken, yalıtkan |
| Na metal (fazlalık) | 46.5 (şarjlı) | 1.94 | 20 µm fazla; döngüsel 26.5 µm Na katot formülünde sayılı |
| Al folyo (anot) | 12 | 3.24 | paylaşımlı |
| Na metal | 46.5 | 1.94 | |
| Ayırıcı | 30 | 4.50 | |
| Katot | 180 | 38.96 | |

- Yığın: **208 Wh/kg, 377 Wh/L**. Hücre (100 × 300 mm, 35 birim, Al-laminat kılıf, tab):
  **63 Ah, 1.06 kg, 0.63 L → 201 Wh/kg, 337 Wh/L**, 3.37 V nominal, 2.36–3.77 V pencere.
- Alt tahmin (A-alt: 60 µm ayırıcı, 50 µm Na, 30 Ω·cm² arayüz): **175 Wh/kg, 276 Wh/L**.
  1. nesil için savunulabilir band 175–201 Wh/kg.
- Element bütçesi: B 0.95, Na 0.97, V 0.60, **Li 0.00** kg/kWh.
- 45 °C'de σ = 3.1 mS/cm; ASR bütçesi: ayırıcı 1.0 + katot kompozit ~13 + arayüzler 15 ≈ 29 Ω·cm²
  → 63 Ah hücrede 1.4 mΩ; 1C'de 88 mV kayıp. 25 °C'de 83 Ω·cm², −10 °C'de ~760 Ω·cm².
- Model uyarısı: NVP kesim potansiyeli (~3.8 V) hidroboratın termodinamik oksidasyon sınırının
  (3.0 V) üstünde → çalışma pasifleştirici arayüze dayanır (`hucre.hesapla` bunu bayraklar).
- Tasarım kaldıraçları (`cikti/duyarlilik.png`): ayırıcı 30 → 20 µm: +4 Wh/kg; yükleme
  3 → 4 mAh/cm²: +10 Wh/kg; anotsuz: +8 Wh/kg. 2. nesil hedefi 215–230 Wh/kg (NVP ile).

## 4.2 Paket: 75 kWh, 400 V, CTP (cell-to-pack)

| Parametre | Değer |
|---|---|
| Mimari | **119s3p**, 357 hücre, 401 V nominal (281–449 V) |
| Enerji | 75.8 kWh brüt, 69.7 kWh kullanılabilir (%92 SOC penceresi) |
| Kütle / hacim | **523 kg / 401 L** → 145 Wh/kg, 189 Wh/L (hücre→paket 0.72 / 0.56; basınç fikstürü + 12 mm yalıtım dâhil) |
| Sürekli güç | 80 kW (≈1C, 3.2 mA/cm²) |
| Tepe güç (10 s, V_min = 2.36 V, CCD ve 12 mA/cm² tavanı ile) | 200 kW hedef; model 45 °C'de ~210 kW, 25 °C'de ~70 kW, −10 °C'de ~7 kW |
| Hızlı şarj | 1. nesil 75 kW (1C = 3.2 mA/cm²), yalnız paket ≥ 40 °C iken (CCD 45 °C'de 4.5 mA/cm²; 25 °C'de 1.5) |
| Bor / Na / V | 72 / 73 / 46 kg |
| Maliyet (varsayımsal) | 17.5 kUSD → 230 USD/kWh (SE 50 USD/kg); 165 USD/kWh (SE 20 USD/kg) |

Pouch hücreler kalınlık ekseninde yığılır; her 8 hücre arasına yaylı basınç plakası
(1–2 MPa yığın basıncı katı hâl için zorunludur). Modülsüz CTP: hücreler doğrudan
alüminyum tepsiye, altta 12 mm aerojel yalıtım (≈66 L, paket hacminin %16'sı), üstte kompozit
kapak. 800 V varyantı: 237s2p, 47 Ah hücre (`borpil paket A --volt 800`).

### Yığın basıncı ve geometri
Katı-katı temas için hücre başına ~1 MPa → 300 cm² hücrede 3 kN. Şarjda hücre kalınlığı
35 × 2 × 26.5 µm ≈ 1.9 mm (%10) artar; disk yaylı plaka bu stroku karşılar. Bu, tasarımın
en önemli mekanik gereksinimidir ve paket kütle/hacim oranlarının Li-iyon CTP'den (0.78/0.65)
düşük alınmasının nedenidir.

## 4.3 Isıl yönetim: "sıcak batarya" stratejisi

Kloso-borat iletkenliği sıcaklıkla artar; hücre 35–60 °C'de en iyi çalışır ve yanıcı
elektrolit olmadığı için 60 °C güvenlik açısından sorun değildir (Na e.n. 97.8 °C'ye
marj korunur). Bu, Li-iyon'un tam tersi bir ısıl felsefe gerektirir:

- **Yalıtım** ön planda: 12 mm aerojel (k = 0.022 W/m·K), 5.5 m² yüzey → UA ≈ 10 W/K.
  35 °C paket, 20 °C ortamda 150 W kaybeder; sürüşte I²R ısısı (80–160 W ortalama) bunun
  büyük kısmını karşılar; kalan PTC ısıtıcıdan gelir.
- **Isıtıcı hedefi 35 °C.** Simülasyon: 20 °C ortamda ısıtıcı toplam 2.7 kWh çeker
  (menzil 476 km; ısıtıcısız 490 km ama tepe güç 52 kW'a düşer). Bu **%3 menzil karşılığında
  güç yeteneğinin 3 katına çıkması** demektir — tasarım tercihi.
- **Ön ısıtma:** −10 → 35 °C için 6.5 kWh (paket ısı kapasitesi ~1 kJ/kg·K). Şebekeye
  bağlıyken yapılır; bağlı değilse 6 kW ısıtıcı + I²R ile ~40 dk. Simülasyon (−10 °C, ısıtıcı
  sürüş boyunca 9.0 kWh): menzil 428 km, min hücre gerilimi 2.87 V, güç kısıtı yok.
- **Stres senaryosu** (−20 °C, ısıtıcı arızalı): ilk ~7 dakika (427 s) güç talebi
  karşılanamaz (açık 1.07 kWh; araç yavaşlar), paket yüksek I²R ile kendini 12 °C'ye ısıtır,
  menzil 454 km. Araç çalışır ama performans düşer — BMS bu durumu sürücüye bildirir.
- **Soğutma:** yalnız hızlı şarjda ve >60 °C'de; düşük debili sıvı plaka. Li-iyon paketlerin
  aksine soğutma sistemi boyutlandırmada tali kalır.
- **Park:** paketin soğumasına izin verilir (kendi kendine deşarj kloso-boratta ihmal
  edilebilir; Na/SE arayüzü oda sıcaklığında kararlı). Nem: Na₂B₁₂H₁₂ hidrat oluşturur
  (·4H₂O) → hücre hermetik, paket kuru hava/N₂ ile şartlanmış.

## 4.4 Araç düzeyi sonuçlar (WLTP-benzeri sentetik çevrim)

C-segment: glider 1350 kg + 150 kg yük + 523 kg paket = 2023 kg; Cd 0.27, A 2.3 m², Crr 0.009.
Tüketim bataryadan çekilen enerjidir (ısıtıcı dâhil, şebeke şarj kayıpları hariç; gerçek
homologasyon değerleri +%10–15 olur).

| Senaryo | Menzil | Tüketim | Paket T | Min V/hücre | Isıtıcı | Güç kısıtı |
|---|---:|---:|---:|---:|---:|---:|
| 20 °C, ısıtıcı hedef 35 °C (strateji) | **476 km** | 14.7 kWh/100 km | 20 → 35 °C | 3.22 V | 2.7 kWh | — |
| 20 °C, ısıtıcı kapalı | 490 km | 14.2 | 20 → 28 °C | 3.17 V | 0 | — |
| −10 °C, ısıtıcı hedef 35 °C | 428 km | 16.3 | −10 → 35 °C | 2.87 V | 9.0 kWh | — |
| −20 °C, ısıtıcı kapalı (stres) | 454 km | 15.4 | −20 → 12 °C | 2.36 V (kesim) | 0 | 427 s / 1.07 kWh |
| 35 °C | 495 km | 14.1 | 35 → 39 °C | 3.25 V | 0 | — |

Enerji dengesi (20 °C): kullanılan 69.7 kWh = uç enerjisi 69.1 kWh + I²R 0.6 kWh; OCV eğrisinin
SOC ortalaması tam nominal gerilime (3.37 V) kalibrelidir. Sentetik çevrim 24.1 km / 1800 s
(WLTP sınıf 3: 23.3 km); gerçek WLTC noktalarıyla değiştirilebilir (`simulasyon.wltp_benzeri_cevrim`).

## 4.5 BMS ve elektrik mimarisi notları

- Düz OCV platosu (3.2–3.4 V arası %90 SOC) → SOC tahmini için coulomb sayımı + uçlardaki dik
  kollar (3.5 V üstü, 3.0 V altı) ile yeniden kalibrasyon; Li-iyon LFP ile aynı sınıf zorluk.
- Hücre dengeleme: pasif (düz platoda küçük akım yeter).
- Sıcaklık sensörü yoğunluğu Li-iyon'dan az (ısıl kaçak yok), ancak **arayüz direnci
  izleme** (EIS/DC darbe) Na dendrit erken uyarısı için eklenir.
- Tepe güç ve şarj akımı sıcaklığa çok bağımlı → BMS güç/şarj sınırı haritası T–SOC
  düzleminde (`simulasyon.maks_guc_kW`, `elektrolit.kritik_akim_yogunlugu_mA_cm2`).
- Rejeneratif frenleme şarj yönündedir (Na kaplama): soğuk pakette rejen akımı CCD ile
  sınırlandırılır, fark mekanik frene aktarılır.
