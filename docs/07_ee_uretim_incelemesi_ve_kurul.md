# 07 — Elektrik-Elektronik ve Üretici İncelemeleri, Kurul Kararları (2. tur)

İki bağımsız uzman inceleme (H3: elektrik-elektronik mühendisliği; H4: EV batarya üreticisi) ve
beş üyeli disiplinler arası kurulun (elektrokimyacı, katı hâl fizikçisi, malzeme/üretim bilimci,
sistem mühendisi, güvenlik/toksikoloji) ortak kararları. Tüm sayılar güncel modelden
(`cikti/RAPOR.md`).

## 7.1 H3 — Elektrik-elektronik incelemesi: ana bulgular

Paket direnci 45 °C'de 55 mΩ, 25 °C'de 157 mΩ, −10 °C'de 1.44 Ω (dR/dT ≈ −5…−7 %/K). Bu tek
sayı bulguların çoğunun kaynağıdır:

1. **Soğukta güç modeli tutarsızdı.** Tepe güç fonksiyonu kritik akım yoğunluğunu (CCD)
   uyguluyor, sürüş simülasyonu uygulamıyordu. Düzeltme: tek `akim_siniri_A()` (deşarj CCD×2,
   ≤ 12 mA/cm²; şarj/rejen CCD/1.5) tüm modüllerde. Sonuç: −10 °C'de ısıtıcılı sürüşte ilk
   ~12 dk güç kısıtı (1.8 kWh açık) görünür hâle geldi; −20 °C ısıtıcı arızası senaryosunda
   araç çevrimi izleyemez.
2. **Isıtıcı takılı kalma = Na erimesi.** UA ≈ 10 W/K yalıtımla 6 kW ısıtıcı +41 K/h → 35 °C'den
   97.8 °C'ye ~95 dk. Li-iyon'da benzeri yok (soğutma sınırlar). ASIL D → B(D)+B(D) ayrıştırma:
   bağımsız 80 °C termal kesici + ayrı ısıtıcı kontaktörü + çift NTC. PTC 3 kW'a düşürülünce
   süre 216–248 dk'ya çıkar; kesici yine zorunlu.
3. **Sigorta soğukta kısa devreyi ayırt edemez.** Beklenen kısa devre akımı 45 °C'de 5–8 kA,
   −10 °C'de 190–310 A (sürekli çalışma akımının altında). Akım-plausibilite (paket ↔ invertör)
   ve dI/dt ile kontaktör açma gerekir; sigorta kesme kapasitesi ≥ 16 kA (60 °C).
4. **Hızlı şarj kapısında marj yoktu.** SF 1.5 ile 75 kW için paket ≥ 44–45 °C. Soğuk pakette
   şarj süresi ısıtma gücüyle belirlenir → ısıtıcı DC şarj cihazından 20 kW ile beslenir
   (−10 °C seansı 95 → 54 dk).
5. **400 V doğru; 800 V'ta 237s pencere 893 V ile SiC DC-link tavanını aşar** → ≤ 228s. Seri
   119 → 120 (10×12 kanallı AFE, 404 V). Tab 0.3 mm (sürekli 2.2 A/mm²).
6. **Darbe (AC) kendinden ısıtma** fiziksel olarak güçlü ama kendini sınırlar: −20 °C'de 42 kW,
   0 °C'de 11 kW, 25 °C'de 2.6 kW (1C rms). −20 → 0 °C **10 dk / 3.7 kWh**; tam ön ısıtma için
   şebeke gücü veya atık ısı gerekir. Na/kloso-borat arayüzünün kHz AC dayanımı deneysel
   doğrulama listesinde.
7. **Tahrik atık ısısı** (~0.8 kW sürüşte) termostatik vana ile pakete: −10 °C menzil
   431 → 455 km, ısıtıcı 9.2 → 5.7 kWh.
8. **Park/V2G:** 35 °C tutmak günde 3.6–11 kWh → parkta paket soğumaya bırakılır; V2G akımı
   CCD(T) ile kapılanır.
9. **BMS:** düz plato → coulomb sayımı + üst dizde (>3.5 V) yeniden kalibrasyon; R(T) artığı
   termometre/dendrit göstergesi; pasif dengeleme 150–300 mA; T–SOC güç/şarj haritası
   (`cikti/isitma_ve_sarj.png`).

## 7.2 H4 — Üretici incelemesi: ana bulgular

1. **Saf pouch 1–2 MPa yığın basıncını ve %10 kalınlık salınımını taşıyamaz** → pouch-in-frame
   (çerçeve + disk yay k ≈ 20 N/mm, 2 mm strok, 1.2 ± 0.3 MPa), hacim oranı 0.56 → 0.52, +12 kg.
2. **30 µm serbest hidroborat filmi ve 20 µm Na folyo bugün endüstriyel değil** → gen-1 ticari
   baz çizgisi A-alt (60 µm / 50 µm / 30 Ω·cm²); A hedef/üst bant.
3. **Verim ve maliyet:** ilk geçiş verimi gen-1 %60–75 (SE film pinhole, WIP delaminasyon);
   imalat çarpanı 1.65–1.85; paket ekleyici 28–38 USD/kWh. Model: ×1.75, %75, +32.
   120 USD/kWh mevcut malzeme karmasıyla ulaşılamaz; gerçekçi hedef bandı 165–200 USD/kWh
   (SE ≤ 25 USD/kg, verim ≥ %90, 10 GWh ölçeği).
4. **Nem birincil arıza modu:** kuru oda < 100 ppm H₂O, hat içi XRD/FTIR hidrat kontrolü,
   metalize polimer + epoksi kenar kılıf (10–15 yıl).
5. **WIP (sıcak izostatik pres) batch darboğaz** → pilotta WIP, ≥ 3 GWh'de 200 MPa kalender +
   bölgesel WIP (ASR bütçesi +3–5 Ω·cm²).
6. **Kloso-borat sentez kapasitesi** bugün < 10 t/yıl; 1 GWh için ~1400 t/yıl → tedarik zincirinin
   ana kısıtı. Vanadyum: 100k araç/yıl = 4600 t V (küresel üretimin %5–10'u) → A-Fe paralel.
7. **B-numunesi öncesi güvenlik matrisi:** UN 38.3 T1–T8 + gaz analizi (H₂, B₂H₆); ECE R100 /
   GB 38031 çivi–ezme–ısıl yayılım (8 hücreli modül); aşırı şarj 1.2×/1.5× V_maks + ARC; dış
   kısa devre 10 ms–10 s; D sınıfı + inert gaz söndürme (modül düzeyinde su yasak).
8. **A/B/C numune planı:** A 0.1–1 Ah ≥ 500 hücre (CCD ≥ 3 mA/cm² @45 °C, 500 çevrim); B 5–10 Ah,
   WIP proses, 800 çevrim, UN 38.3 ön test; C 60 Ah, 1000+ hücre, 1500 çevrim projeksiyonu,
   12'li modül, ECE R100.

## 7.3 Kurul kararları

| P# | Konu | Karar | Uygulama | Muhalif |
|---|---|---|---|---|
| P1 | Tek akım sınırı (deşarj/şarj/rejen) | Onay | `simulasyon.akim_siniri_A`; sürüşte CCD + rejen sınırı, fazla rejen mekanik frene | — |
| P2 | Hızlı şarj kapısı SF 1.5, şarj simülasyonu | Onay | 75 kW ≥ 44 °C; `sarj_simulasyonu`, ısıtıcı şebekeden 20 kW | — |
| P3 | Paket elektrik kontrolleri | Onay | gerilim penceresi/invertör/şarj cihazı, tab, kısa devre uyarısı (`paket.boyutlandir`) | — |
| P4 | Isıtıcı güvenlik zinciri | Kabul | 80 °C donanım kesici + ayrı kontaktör + çift NTC; `isitici_takili_*` analizi; ASIL D → B(D)+B(D) | — |
| P5 | Darbe (AC) ısıtma | Kabul-düzeltilmiş | Model seçeneği (`darbe_isitma_gucu_kW`); gen-1 baz değil, EIS doğrulaması sonrası; PTC 6 → 3 kW | Elektrokimyacı: EIS'siz baz olmasın (giderildi) |
| P6 | Tahrik atık ısısı | Kabul-düzeltilmiş | `atik_isi_kW = 0.8` baz, termostatik vana (hedef + 5 K) | — |
| P7 | Sıvı soğutma | Kabul-düzeltilmiş | ≥ 3 kW, 60 °C tavan (`sogutma_guc_W_per_K = 200`, tavan 3 kW) | — |
| P8 | 3 bağımsız dizi | Kabul-düzeltilmiş | `bagimsiz_dizi = True`, +225 USD; dizi akım dengesizliği = dendrit dedektörü | Üretim bilimci: 3p daha basit; güvenlik oyuyla geçti |
| P9 | 119 → 120 seri | Kabul-düzeltilmiş | 404 V nominal, 283–452 V, 10×12 kanal AFE | — |
| P10 | Pouch-in-frame | Kabul | hacim oranı 0.52, +12 kg fikstür, 1.2 ± 0.3 MPa | — |
| P11 | A-alt gen-1 ticari baz çizgisi | Kabul | Rapor/dokümanlar baz (A-alt) / hedef (A) yan yana | Sistem mühendisi: menzil rekabetçiliği; üretilebilirlik baskın |
| P12 | NVP ALD kaplama zorunlu, A0 paralel, karbon %3 → %2 | Kabul-düzeltilmiş | Reçete güncellendi; NVP maliyeti +2 USD/kg (kaplama) | — |
| P13 | Maliyet modeli | Kabul-düzeltilmiş | ×1.75, verim 0.75, +32 USD/kWh; gen-1 baz 412, hedef 358 USD/kWh; hedef bandı 165–200 | Sistem mühendisi: yatırımcı algısı; şeffaflık tercih edildi |
| P14 | Kompozitte SE %25 → %18 | Ertele (gen-2) | −12 USD/kWh'e karşı soğukta +5 Ω·cm² | — |
| P15 | Nem spesifikasyonu | Kabul | < 100 ppm H₂O, hat içi hidrat QC, güçlendirilmiş kılıf (docs/03, /05) | — |
| P16 | WIP → hibrit presleme | Kabul-düzeltilmiş | Pilot WIP; ≥ 3 GWh kalender + bölgesel WIP; ASR bütçesi +3–5 Ω·cm² | — |
| P17 | BMS spesifikasyonu | Kabul | docs/04 §4.5 | — |
| P18 | Güvenlik nitelendirme + A/B/C planı | Kabul | docs/06 §6.4 | — |
| P19 | Park/V2G politikası | Kabul | 35 °C tutma yok; CCD(T) kapılı düşük akım | — |
| P20 | Çok düğümlü ısıl model + 3p akım paylaşımı | Ertele | B-numune HIL kalibrasyonu | Katı hâl fizikçisi: kenar soğukluğu hatası; gen-1 için yeterli görüldü |

## 7.4 Kararların sonucu: 1. nesil konfigürasyon

| | Baz çizgisi (A-alt) | Hedef (A) |
|---|---:|---:|
| Hücre | 60 µm SE, 50 µm Na, 30 Ω·cm² → **177 Wh/kg, 279 Wh/L** | 30 µm, 20 µm, 15 Ω·cm² → 203 Wh/kg, 341 Wh/L |
| Paket 74 kWh, 120s3p, 3 dizi, pouch-in-frame | **596 kg / 512 L (125 Wh/kg)** | 519 kg / 418 L (143 Wh/kg) |
| Menzil (20 °C, strateji / −10 °C ön ısıtılmış) | **457 / 474 km** | 474 / 486 km |
| DC şarj 10 → 80 % (45 / 25 / −10 °C başlangıç) | **32 / 38 / 54 dk** | 34 / 39 / 53 dk |
| Maliyet (SE 50 USD/kg, verim %75) | **412 USD/kWh** | 358 USD/kWh |
| Maliyet (SE 25, verim %90, ×1.55) | 234 | 214 |
| Bor / Li | 92 kg / 0 | 70 kg / 0 |

Isıl strateji: 12 mm aerojel, sürüşte 35 °C hedef (3 kW PTC + 0.8 kW atık ısı), DC şarjda 45 °C
(20 kW şebeke ısıtıcı), 60 °C'de ≥ 3 kW soğutma, parkta ısıtma yok, 80 °C bağımsız kesici.
Darbe ısıtma yol haritasında (derin soğuktan çıkış: −20 → 0 °C, 10 dk).

## 7.5 Deneysel doğrulama planına eklenen maddeler (kurul)

1. Na | SE | Na simetrik hücrede CCD(T): 25/45/60 °C, 1 MPa; hedef ≥ 3 mA/cm² @45 °C.
2. kHz AC arayüz dayanımı (0.5–1C rms, 1–10 kHz, −20…0 °C) + EIS; kaplama/delaminasyon kriteri.
3. ALD kaplamalı / kaplamasız NVP | SE: CV 2.0–4.0 V, XPS pasif tabaka; A0 (NaCrO₂) paralel.
4. Nem/hidrat QC (< 100 ppm), 10–15 yıl nem bariyeri yaşlandırma.
5. WIP ↔ kalender ASR haritası (300–500 MPa vs 200 MPa).
6. 8 hücreli modül güvenlik matrisi (UN 38.3, ECE R100/GB 38031, ARC, H₂/B₂H₆ gaz analizi, D sınıfı söndürme).
7. 3 dizi mimarisinde yumuşak kısa devre enjeksiyonu ile erken algılama.
8. Soğuk performans paketi: −10/−20 °C, PTC 3 kW + atık ısı (+ pilot sonrası darbe ısıtma).
9. A-numune ≥ 500 çevrim @45 °C; B-numune 800 çevrim WIP proses.
10. Çok düğümlü ısıl + 3p akım paylaşımı: B-numune HIL kalibrasyonu (ertelendi).
