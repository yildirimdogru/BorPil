# 03 — Malzemeler, Sentez Rotaları ve Üretim (A3 Malzeme Bilimci)

## 3.1 Bor tedarik zinciri (cevherden elektrolite)

```
Tinkal / kolemanit (Kırka, Emet, Bigadiç)
   → Boraks / borik asit (H₃BO₃)                      [mevcut endüstri]
   → Bor oksit / boratlar → NaBH₄ (Brown-Schlesinger: NaH + B(OCH₃)₃ veya Bayer rotası)
                                                       [Türkiye'de pilot/endüstriyel NaBH₄ üretimi mevcut]
   → B₂H₆ (NaBH₄ + BF₃·OEt₂ veya H₂SO₄) ──┐
   → B₁₀H₁₄ (dekaboran; B₂H₆ pirolizi)    ├─→ Na₂B₁₂H₁₂ , Na₂B₁₀H₁₀
                                           ┘
```

- **Na₂B₁₂H₁₂:** 2 NaBH₄ + 5 B₂H₆ → Na₂B₁₂H₁₂ + 13 H₂ (diglim, 180 °C). Endüstriyel
  alternatif: NaBH₄ + B₁₀H₁₄ → Na₂B₁₂H₁₂ (piroliz, 150–200 °C). Hidratlı ürün 200 °C vakumda
  kurutulur (kristal suyu iletkenliği bozar).
- **Na₂B₁₀H₁₀:** B₁₀H₁₄ + 2 Et₃N → (Et₃NH)₂B₁₀H₁₀ → NaOH ile iyon değişimi. Diboran/dekaboran
  toksik ve piroforiktir; kapalı, azot altında proses. Tüm bu adımlar borhidrür kimyasında
  bilinen, ölçeklenmiş birim işlemlerdir; yeni olan **tonaj**dır (75 kWh'lik paket başına
  ~105 kg kloso-borat tuzu ≈ 72 kg B).
- **Eş-molar karışım:** Na₂B₁₂H₁₂ + Na₂B₁₀H₁₀ (1:1 mol) yüksek enerjili bilyalı öğütme
  (2–4 saat, Ar) → katı çözelti; alternatif: sulu ortak çözeltiden kurutma. Nem < 10 ppm
  ortamda (kuru oda) işlenir; kloso-boratlar hidroliz etmez ama hidrat oluşturur.

Ölçek hedefi: 1 GWh/yıl hücre → ~1400 t/yıl kloso-borat, ~960 t/yıl bor içeriği. Türkiye'nin
yıllık bor ürünü üretimi (B₂O₃ bazında milyon ton mertebesi) yanında ihmal edilebilir;
kısıt cevher değil, **hidroborat sentez kapasitesi**dir.

## 3.2 Katot malzemeleri

| Malzeme | Sentez | Pratik | Not |
|---|---|---|---|
| **Na₃V₂(PO₄)₃/C (NVP)** | Sol-jel veya katı hâl; V₂O₅ + NaH₂PO₄ + sitrik asit, 750–800 °C Ar | 110 mAh/g, 3.37 V | Karbon kaplı (in-situ) parçacık, D50 ~2–5 µm. Hücrede 2.7 kg/kWh NVP, 0.6 kg/kWh V. Kompozitteki iletken karbon hidroborat oksidasyonunu hızlandırır → kaplama şart. |
| NaCrO₂ | Cr₂O₃ + Na₂CO₃, 900 °C Ar | 115 mAh/g, 2.95 V | Cr(VI) oluşumunu önlemek için inert atmosfer; nem hassas. |
| P2-Na₂/₃Fe₁/₂Mn₁/₂O₂ | Fe₂O₃ + Mn₂O₃ + Na₂CO₃, 900 °C hava | 120 mAh/g (≤ 4.0 V), 2.75 V | Ucuz, kritik metalsiz; 4.3 V'a kadar 190 mAh/g ama P2→O2/"Z" geçişi ve elektrolit penceresi 4.0 V tavanı zorlar; havada Na kaybı → kuru oda. |
| Na₃V₂(PO₄)₂F₃ (2. nesil) | NVP + NaF, hidrotermal/katı hâl | 120 mAh/g, 3.9 V | Yalnız karba-kloso-borat + pasifleştirici arayüzle. |

### Katot kompozit reçetesi (kütle)
%71 aktif (karbon + ALD NaNbO₃/Na₃PO₄ kaplı), %25 kloso-borat SE, %2 iletken karbon (CB + CNT;
karbon hidroborat oksidasyonunu hızlandırdığı için azaltıldı), %2 elastomer bağlayıcı (NBR, ksilen içinde). Gözeneklilik hedefi ≤ %8 (izostatik pres sonrası).
Yükleme 3 mAh/cm² (tek yüz) → 39 mg/cm², ~180 µm.

**Arayüz kaplaması (kritik):** NVP parçacıkları üzerine 5–10 nm NaNbO₃ veya Na₃PO₄ tabakası
(ALD veya ıslak kimya). Amaç: yüksek SOC'de SE oksidasyonunu kontrollü, kendi kendini
sınırlayan bir pasif tabakaya dönüştürmek.

## 3.3 Ayırıcı (katı elektrolit filmi)

- **Yaş proses:** SE tozu + %2–3 NBR, ksilen/toluen; Mylar taşıyıcı üzerine slot-die döküm,
  80 °C kurutma. **Kalınlık hedefi 30 µm** (tasarım noktası); literatürde kendi başına duran
  hidroborat filmleri henüz 50–100 µm sınıfındadır, bu yüzden alt tahmin varyantı 60 µm ile
  hesaplanır (175 Wh/kg). 30 µm, sülfür katı hâl hatlarında ulaşılmış bir değerdir. Sıvı bazlı ince film, katı hâl
  sülfür pillerden aktarılan olgun bir yöntemdir.
- **Kuru proses (alternatif):** SE + %0.5 PTFE lif oluşturma → kalender (Maxwell tipi); çözücü
  yok, daha yüksek yoğunluk.
- Kloso-boratlar **yumuşaktır** (Young modülü ~5–15 GPa mertebesi, Vickers sertliği düşük):
  soğuk presle %95+ yoğunluk. Oksitlerden farklı olarak sinterleme yok; sülfürlerden farklı
  olarak H₂S yok.

## 3.4 Anot

- **Na metal (1. nesil):** 20 µm "fazla" Na, Al folyo üzerine ekstrüzyon/hadde ile lamine
  (Na Al ile alaşım yapmaz; erime noktası 97.8 °C → sıcak lamine kolay). Deşarj sonu bile
  Al'de %100 sıyırma olmaz (fazla Na); şarjda katottan gelen Na (26 µm eşdeğeri) kaplanır.
  20 µm Na folyo üretimi ölçekli değildir; alt tahmin varyantı 50 µm ile hesaplanır.
  Kütle muhasebesi: döngüsel Na katot formülünde (Na₃V₂(PO₄)₃) sayılır, anot kütlesine yalnız
  fazlalık eklenir (kütle korunumu); kalınlıkta şarjlı (maksimum) hâl alınır.
- **Anotsuz (2. nesil):** Al üzerine ~1 µm karbon/Ag tohum tabakası; ilk şarjda Na oluşur.
  Enerji yoğunluğu %8 artar; kritik akım yoğunluğu doğrulaması gerekir.
- **Sert karbon (varyant C):** biyokütle/asfalt öncülü, 1300 °C; %68 aktif + %27 SE kompozit.

## 3.5 Hücre montajı — proses akışı

Kurul kararları (docs/07): format **pouch-in-frame** (çelik/kompozit çerçeve + disk yay, 1.2 ± 0.3 MPa);
kuru oda **< 100 ppm H₂O** + hat içi XRD/FTIR hidrat kontrolü; kılıf metalize polimer + epoksi kenar;
pilotta batch WIP, ≥ 3 GWh'de 200 MPa kalender + bölgesel WIP; gen-1 ilk geçiş verimi %60–75 (SE film
pinhole ve WIP delaminasyonu ana kayıp), ±1.5–2 % kapasite eşleştirme.

1. Katot kompozit döküm (çift taraflı Al, slot-die) → kurutma → kalender.
2. SE filmi Mylar'dan katot üzerine transfer-laminasyon (60 °C, 50 MPa hadde).
3. Na/Al anot folyosu laminasyonu.
4. Z-katlama veya yığma (33 tekrar birimi, 100 × 300 mm).
5. **Sıcak izostatik pres (WIP):** 80 °C, 300–500 MPa, 10 dk — katı-katı temasın anahtarı.
6. Tab kaynağı (Al-Al ultrasonik; iki tarafta da Al → tek tip kaynak), pouch kılıf, vakum
   kapama. **Elektrolit dolum ve ıslatma adımı yok** → Li-iyon'a göre 2 adım eksik.
7. Formasyon: 45 °C, 0.1C × 2 çevrim; yığın basıncı 1–2 MPa (modül düzeyinde yaylı plaka).
8. Yaşlandırma/OCV kontrolü; sızıntı ve delaminasyon için ultrason.

Tüm hat kuru oda (< −40 °C çiğ noktası) gerektirir; Na metal için ek olarak Ar kapalı kutu
yalnız laminasyon istasyonunda.

## 3.6 Element bütçesi ve maliyet (BorPil-A, 75 kWh)

| Element/malzeme | kg / paket | USD/kg (varsayım) | Not |
|---|---:|---:|---|
| Kloso-borat SE (B %68) | ~107 | 50 (hedef 20; bugün >1000) | Maliyet belirleyici; ölçek ve rota |
| NVP | ~205 | 22 (aralık 18–30) | V₂O₅ fiyatına duyarlı; 46 kg V |
| Na metal (yalnız fazlalık; döngüsel Na katotta) | ~14 | 3 | Toplam Na (SE + katot + fazla) 73 kg |
| Al folyo | ~23 | 5 | Cu yok |
| Karbon, bağlayıcı | ~14 | 10–15 | |

Model (kurul P13, gen-1 gerçekçi): malzeme / ilk geçiş verimi (%75) × imalat çarpanı (1.75) + paket
ekleyici (32 USD/kWh) + 3 dizi donanımı. Hedef A: 136 USD/kWh malzeme → **358 USD/kWh** paket; baz
A-alt: 162 → **412 USD/kWh** (SE 50 USD/kg). Ölçek senaryosu (SE 25, verim %90, ×1.55): 214 / 234.
SE tek başına malzeme maliyetinin ~%55'idir (1.4–1.9 kg SE/kWh). Ekonomik hedef bandı 165–200 USD/kWh
için SE ≤ 25 USD/kg **ve** verim ≥ %90 **ve** 10 GWh ölçeği birlikte gerekir; 120 USD/kWh mevcut karma
ile ulaşılamaz (gen-2: SE %18, A-Fe katot, SE ≤ 15 USD/kg). Grafik: `cikti/duyarlilik.png`, tablo:
`cikti/RAPOR.md §9`.
