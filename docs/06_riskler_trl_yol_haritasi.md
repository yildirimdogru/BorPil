# 06 — Riskler, Olgunluk (TRL), Doğrulama Planı ve Yol Haritası

## 6.1 Teknoloji olgunluğu (bugün)

| Bileşen | TRL | Dayanak |
|---|---|---|
| Kloso-borat Na katı elektrolit (oda sıc. ~1 mS/cm) | 4 | Çok sayıda laboratuvar, gram ölçeği; 100 mAh sınıfı hücreler |
| Na / kloso-borat / NaCrO₂ tam hücre | 4 | 3 V, 250 çevrim, 60 °C (Duchêne 2017) |
| Na / hidroborat / 4 V katot (pasifleşme) | 3 | Asakura 2020 |
| NVP katot (sıvı elektrolit Na-iyon) | 8–9 | Ticari Na-iyon hücrelerde kullanılıyor |
| Na metal anot, katı hâl, >3 mA/cm² | 3 | Kritik akım yoğunluğu çalışmaları |
| Pouch ölçekli katı hâl imalatı (sülfür analoglarından transfer) | 5–6 | Sektörde pilot hatlar |
| DBFC yığın | 4–5 | Prototip sistemler (kW sınıfı) |
| Darbe (AC) kendinden ısıtma, Na/kloso-borat arayüzü | 2–3 | Li-iyon'da ticari; hidroborat arayüzünde kHz dayanım verisi yok |
| **BorPil-A sistem** | **3–4** | Bu çalışma: modelle boyutlandırılmış, iki tur bağımsız inceleme; deneysel doğrulama bekliyor |

## 6.2 Risk kaydı

| # | Risk | Olasılık | Etki | Azaltma / B planı |
|---|---|---|---|---|
| R1 | NVP (3.37 V) ile hidroborat oksidasyonu pasifleşmez, kapasite sönümü | Orta | Yüksek | Katot kaplama (NaNbO₃/Na₃PO₄); karba-kloso-borat katkısı; **A0: NaCrO₂** (2.95 V) |
| R2 | Na dendriti / boşluk oluşumu; kritik akım yoğunluğu < 3 mA/cm² | Orta | Yüksek | 45–60 °C çalışma (Na sürünmesi ↑); 1–2 MPa yığın basıncı; Al/C ara tabaka; **C: sert karbon** |
| R3 | Kloso-borat maliyeti 20–25 USD/kg'a inmez | Orta | Orta | NaBH₄→B₁₀H₁₄ rotası, çözücü geri kazanımı; ayırıcı 20 µm; kompozitte SE %25 → %18 |
| R4 | Vanadyum fiyat/tedarik | Düşük-Orta | Orta | **A-Fe** (Fe/Mn oksit) veya Prusya beyazı; V geri dönüşümü |
| R5 | Soğuk iklim güç yetersizliği | Yüksek | Orta | Ön ısıtma stratejisi; arayüz Ea düşürme (kaplama); kışın güç sınırı haritası (BMS) |
| R6 | Çevrim ömrü < 1500 | Orta | Yüksek | Formasyon protokolü; katot hacim değişimi küçük (NVP %8); Na fazlası 20 µm |
| R7 | Kompozit katotta SE-katot arayüz kimyasal reaksiyonu (yüksek T) | Düşük | Orta | 60 °C kalorimetri; kaplama |
| R8 | Kılıf delinmesinde Na metal reaksiyonu | Düşük | Orta | İnert dolgu, sert tepsi; UN 38.3 / GB 38031 testleri |
| R9 | Hidroborat sentezi (B₂H₆) endüstriyel güvenlik | Orta | Orta | Kapalı, sürekli akış reaktörü; borhidrür endüstrisi pratiği |
| R10 | Rakip: sıvı elektrolitli Na-iyon veya sülfür katı hâl Na | Yüksek | Orta | Bor içeriği + yanmazlık + Na-metal enerji yoğunluğu ile farklılaşma |
| R11 | Nem: Na₂B₁₂H₁₂·4H₂O hidratı iletkenliği düşürür, Na ile reaksiyona girer | Orta | Orta | Hermetik hücre; üretimde <%1 RH; hidrat XRD kontrolü |
| R12 | Na erime noktası (97.8 °C) ile çalışma sıcaklığı marjı | Düşük | Yüksek | BMS 80 °C güç kesme / 90 °C ayırma; yalıtım tasarımı aşırı ısınmayı da yavaşlatır → aktif izleme |
| R13 | İletken karbonun hidroborat oksidasyonunu hızlandırması | Orta | Orta | Katot kaplama (zorunlu, kurul P12); karbon payı %3 → %2, CNT ile |
| R14 | Isıtıcı takılı kalma → Na erimesi (yalıtımlı pakette kendiliğinden sınırlanmaz) | Düşük | Çok yüksek | Bağımsız 80 °C termal kesici + ayrı kontaktör + çift NTC; ASIL D → B(D)+B(D) (docs/07 P4) |
| R15 | Soğukta kısa devre akımı sürekli akımın altında → sigorta ayırt edemez | Orta | Yüksek | Akım-plausibilite + dI/dt kontaktör açma; ≥ 16 kA kesme kapasiteli sigorta (P3) |
| R16 | Saf pouch 1–2 MPa basıncı ve %10 kalınlık salınımını taşıyamaz | Yüksek | Yüksek | Pouch-in-frame, disk yaylı plaka, 1.2 ± 0.3 MPa (P10) |
| R17 | Gen-1 verim %60–75 (SE film pinhole, WIP delaminasyon) → maliyet | Yüksek | Orta | Hat içi kalınlık/EIS QC, 60 µm fallback spesifikasyonu, WIP → kalender geçişi (P13, P16) |
| R18 | Kloso-borat sentez kapasitesi (< 10 t/yıl) | Yüksek | Yüksek | NaBH₄ → B₁₀H₁₄ kapalı akış reaktörü; 5 yıllık ölçekleme planı; ikinci tedarikçi |

## 6.3 Hakem bulguları (H1 kimya/fizik, H2 sayısal model) ve yapılan düzeltmeler

İki bağımsız hakem ajan, kodu ve raporu kör olarak inceledi. Bulgular ve işlem:

| # | Bulgu | Kaynak | İşlem |
|---|---|---|---|
| 1 | Döngüye giren Na hem katot formülünde hem şarjlı anot kütlesinde sayılıyordu (%5 kütle, Na bütçesi %21 fazla) | H1, H2 | Anot kütlesi yalnız fazlalık Na; kalınlık şarjlı hâl. Hücre 191 → **201 Wh/kg**, Na 1.22 → 0.97 kg/kWh. Test eklendi. |
| 2 | OCV eğrisinin SOC ortalaması nominalin 0.10 V altındaydı → tüketim ~%3 şişkin | H1, H2 | Şekil fonksiyonu analitik ofsetle nominale kalibre edildi; ∫OCV = V_ort testi eklendi. |
| 3 | Güç talebi karşılanamayınca akım kırpılıyor ama mesafe/açık kaydedilmiyordu | H2 | Kesim gerilimi sınırı + `guc_kisiti_s`, `guc_acigi_kWh` alanları; kısıtlı adımlarda mesafe güç oranıyla ölçeklenir. −20 °C stres testi eklendi. |
| 4 | Kritik akım yoğunluğu için iki farklı varsayılan (1.0 ve 3.0 mA/cm²) | H1 | Tek merkezî sabit `J_KRITIK_25C_MA_CM2 = 1.5` (literatür 0.5–2); tüm modüller bunu kullanır. |
| 5 | Elektrolit oksidasyon penceresi katot potansiyeliyle hiç karşılaştırılmıyordu | H1, H2 | `hesapla` kesim potansiyelini termodinamik/pasifleşme sınırlarıyla kıyaslar, UYARI/KRİTİK üretir. |
| 6 | Na₂B₁₂H₁₂ düzenli faz iletkenliği ~3 mertebe yüksek (geçişte sıçrama kaybolmuştu) | H1 | Referans 500 K / 1e-5 S/cm; 529 K'de ~10³ sıçrama; 25 °C'de ~3e-8 S/cm. |
| 7 | bcc kafes parametresi oda sıcaklığı yoğunluğundan (a=7.38 Å) türetiliyordu; ölçüm 7.9 Å | H1 | Ölçülen a = 7.9 Å varsayılan; tetrahedral boşluk 0.93 → **1.00 Å** (Na⁺ 1.02 Å). Yoğunluk 1.55 → 1.46. |
| 8 | Anot dalı `is` kimlik kontrolüyle seçiliyordu; `replace` edilmiş Na anot kompozit dala düşüyordu | H2 | `Elektrot.metalik` alanı; test eklendi. |
| 9 | `frozen` dataclass + dict alan → hash hatası | H2 | `eq=False`. |
| 10 | Menzil %95 SOC ile, paket %92 ile hesaplanıyordu | H1 | Simülasyon SOC penceresini paketten alır. |
| 11 | Kaynak atıfları: 70 mS/cm → ACS Energy Lett. 2016; eş-molar karışım → Chem. Commun. 2017 (+EES 2017 tam hücre) | H1 | Düzeltildi. |
| 12 | Tepe güç salt omik (60 °C'de >1 MW) | H1 | CCD (Arrhenius) ve 12 mA/cm² katot tavanı; kesim gerilimi nominalin %70'i (Na-S için de çalışır). |
| 13 | Paket akım yoğunluğu formülü | H2 doğruladı | `j = I_paket·seri/A_toplam` ✓ (bağımsız el hesabıyla test). |
| 14 | Wh/kg, Wh/L, USD/kWh, bor bütçesi birim dönüşümleri | H2 doğruladı | El hesabı 191.1 / 337.0 / 119.0 ile birebir (Na düzeltmesi öncesi). |
| 15 | NaFeMnO₂ pratik kapasite 150 → 120 mAh/g (≤ 4.0 V tavanı) | H1 | Güncellendi; A-Fe 195 → 176 Wh/kg. |
| 16 | 30 µm SE, 20 µm Na, 15 Ω·cm² üst sınır varsayımları | H1 | **A-alt** varyantı (60 µm, 50 µm, 30 Ω·cm²) eklendi: 175 Wh/kg; sonuçlar band olarak raporlanır. |
| 17 | Hücre→paket oranları 0.76/0.62 iyimser (basınç fikstürü, 66 L yalıtım) | H1 | 0.72 / 0.56. |
| 18 | DBFC 1.0 V, %75 kullanım, %35 rejenerasyon iyimser | H1 | 0.85 V, %65, %30 → gidiş-dönüş %10; menzil uzatıcı +227 → +167 km. |
| 19 | NVP maliyeti 16 → 22 USD/kg; SE duyarlılığı 200 USD/kg'a kadar | H1 | Güncellendi; paket 230 USD/kWh (SE 50). |
| 20 | 45 °C tasarım noktası ısıtıcısız sürdürülemez | H1 | Isıtıcı hedefi 35 °C "sıcak batarya" stratejisi; ısıtıcı enerjisi raporda ayrı sütun. |
| 21 | Totolojik testler (kütle toplamı, akım formülü, ikosahedron assert) | H2 | Bağımsız el hesabı/özdeşlik tabanlı testlerle değiştirildi; toplam 39 test. |

Kabul edilen ama modele alınmayan notlar: sert karbon ilk çevrim kaybı (N/P ile örtük), rejen
akım sınırı (BMS notu, `docs/04`), gerçek WLTC hız noktaları (sentetik çevrim 24.1 km yeterli).

2. tur (elektrik-elektronik + üretici) bulguları ve kurul kararları: `docs/07`.

## 6.4 Doğrulama planı (deneysel)

Kurulun 2. turda eklediği maddeler (kHz AC arayüz dayanımı, ALD kaplama CV/XPS, nem < 100 ppm QC,
WIP ↔ kalender ASR haritası, 8 hücreli modül güvenlik matrisi, 3 dizi yumuşak kısa devre enjeksiyonu,
A/B/C numune hacimleri) `docs/07 §7.5`'tedir; aşağıdaki fazlara dağıtılır.

**Faz 0 — Malzeme (gram ölçeği)**
- Na₂B₁₂H₁₂, Na₂B₁₀H₁₀ sentezi (yerli NaBH₄'ten), eş-molar öğütme; XRD (bcc/fcc düzensiz faz),
  EIS −30…+100 °C (Arrhenius; hedef ≥ 0.8 mS/cm @ 25 °C, Ea ≤ 0.45 eV).
- Na | SE | Na simetrik hücre: kritik akım yoğunluğu 25/45/60 °C'de, 1 MPa (hedef ≥ 3 mA/cm² @ 45 °C).
- SE | NVP arayüz: CV 2.0–4.0 V, kaplamalı/kaplamasız; XPS ile pasif tabaka.

**Faz 1 — Hücre (0.1 → 1 Ah)**
- Kompozit katot reçetesi optimizasyonu (SE %18–30), ayırıcı film 30 µm döküm.
- 1 Ah pouch: 45 °C, 0.5C/0.5C, 500 çevrim; hedef ≥ %90 kapasite; 0 °C'de 0.2C deşarj.
- Güvenlik ön testi: çivi, ezme, 150 °C fırın (ARC kalorimetri).

**Faz 2 — Otomotiv hücresi (60 Ah) ve modül**
- 100 × 300 mm, 35 birim; WIP proses; ≥ 185 Wh/kg hedefi; 1500 çevrim projeksiyonu.
- 12 hücreli modül: yaylı basınç plakası, ısıtıcı, yalıtım; IEC 62660-2/-3, UN 38.3.
- Sürüş çevrimi profil testi (bu depodaki güç profiliyle HIL).

**Faz 3 — Paket ve araç**
- 75 kWh, 400 V, CTP; GB 38031 / ECE R100; kış testi (−20 °C ön ısıtma), yaz (50 °C ortam).

## 6.5 Hedef KPI'ler

| KPI | 1. nesil (A) | 2. nesil (B) |
|---|---|---|
| Hücre Wh/kg / Wh/L | 177 / 279 (baz A-alt); 203 / 341 (hedef A) | 260 / 440 |
| Paket Wh/kg | 125 (baz) / 143 (hedef) | 195 |
| Çevrim ömrü (%80 EOL) | 1500 | 2500 |
| Hızlı şarj (10→80 %) | 32 dk (45 °C paket) / 54 dk (−10 °C, şebeke ısıtıcı ile) | 25 dk |
| Çalışma sıcaklığı | 35–60 °C (ısıl strateji; −20 °C'de darbe ısıtma ile çıkış) | 10–70 °C |
| Paket maliyeti | 412 → 234 USD/kWh (SE 50 → 25 USD/kg, verim %75 → %90) | < 180 USD/kWh |
| Li / Co / Ni | 0 / 0 / 0 | 0 / 0 / 0 |
| Bor içeriği | ~%19 hücre kütlesi | ~%13 |

## 6.6 Açık bilimsel sorular

1. Hidroborat oksidasyon ürününün (B₁₂H₁₂⁻ radikali → B₂₄H₂₃³⁻ dimeri?) yapısı ve iyonik
   iletkenliği — pasifleşmenin fiziği.
2. Anyon karışım oranının (B₁₂:B₁₀) ve az miktarda karba-anyon katkısının iletkenlik/kararlılık
   dengesi; 0.5:0.5 optimum mu?
3. Na/kloso-borat arayüzünde boşluk oluşumu kinetiği; Na sürünme hızı ile kritik akım ilişkisi
   (sıcaklık + basınç haritası).
4. Kloso-borat elektrolitin uzun süreli (10 yıl) kimyasal/mekanik yaşlanması, kaplama
   tabakalarının delaminasyonu.
5. DBFC için NaBO₂ rejenerasyon verimini %50'ye çıkaran elektrokimyasal/hidrojenle indirgeme
   yolları (yerli bor yakıtı döngüsü).
