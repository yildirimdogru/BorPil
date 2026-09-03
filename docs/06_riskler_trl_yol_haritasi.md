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
| **BorPil-A sistem** | **3–4** | Bu çalışma: modelle boyutlandırılmış, deneysel doğrulama bekliyor |

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

## 6.3 Hakem bulguları (H1, H2)

Bağımsız inceleme bulguları ve yapılan düzeltmeler bu bölümde tutulur:

- Paket akım yoğunluğu formülünde hücre alanı/paralel kol karışıklığı → `j = I_paket · seri / A_toplam`
  olarak düzeltildi (paket.py).
- Tepe güç modeli salt omik iken 60 °C'de fiziksel olmayan >1 MW değerler veriyordu →
  Na soyulma kritik akım sınırı (Arrhenius) ve katot difüzyon tavanı (12 mA/cm²) eklendi.
- Kafes boşluk analizinde vdW yarıçapı kullanımı >%100 dolgu veriyordu → sert küre yarıçapı
  kafes temasından (a√3/4) türetildi; vdW yarıçapı ayrıca raporlanıyor.
- Hücre kapasitesi, seri×paralel mimarisiyle hedef enerjiyi tam tutturacak şekilde yeniden
  boyutlandırılıyor (önceden 71.5 kWh çıkıyordu).

## 6.4 Doğrulama planı (deneysel)

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
| Hücre Wh/kg / Wh/L | 190 / 340 | 260 / 440 |
| Paket Wh/kg | 145 | 195 |
| Çevrim ömrü (%80 EOL) | 1500 | 2500 |
| Hızlı şarj (10→80 %) | 45 dk (1C) | 25 dk |
| Çalışma sıcaklığı | 25–60 °C (−20 °C'de sınırlı güç) | 10–70 °C |
| Hücre maliyeti | 185 → 120 USD/kWh (SE fiyatına bağlı) | < 100 USD/kWh |
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
