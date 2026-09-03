# 02 — Kimya ve Termodinamik (A1 Elektrokimyacı, A2 Fizikçi)

## 2.1 Bor neden batarya elementi olabilir — ve neden "bor anot" değil?

Bor (Z=5, 10.81 g/mol) hafiftir ve üç değerliklidir; oksidasyonu çok ekzotermiktir:

    4 B + 3 O₂ → 2 B₂O₃      ΔG° = −2388.6 kJ  →  E° = 2.063 V, 7438 mAh/g B, **15.3 kWh/kg B**

Bu teorik değer Li-hava'nın (11.2 kWh/kg Li) üzerindedir. Ancak bu enerji **elektrokimyasal
olarak tersinir biçimde** kullanılamaz: B₂O₃/borat ürünü yalıtkan ve pasifleştiricidir, oda
sıcaklığında B'nin anodik çözünmesi kinetik olarak bloke olur, tersine B kaplama sulu ya da
organik ortamda mümkün değildir (B³⁺ çok küçük, çok sert bir katyondur; kovalent bağ yapar).
Dolayısıyla bor, alkali metaller gibi bir "kaplanan/sökülen anot" olamaz.

Borun bataryadaki gerçek gücü başka yerdedir: **bor-hidrojen kafes anyonları**. Aşağıdaki
dört yol tarandı:

| Yol | Reaksiyon / bileşen | E° veya σ | Değerlendirme |
|---|---|---|---|
| Bor-hava (birincil) | 4B + 3O₂ → 2B₂O₃ | 2.06 V, 15.3 kWh/kg | Tersinir değil; pasivasyon. **Ret** (referans). |
| DBFC | NaBH₄ + 2O₂ → NaBO₂ + 2H₂O | 1.65 V, 9.3 kWh/kg NaBH₄ | Yakıt pili; rejenerasyon verimi düşük (gidiş-dönüş ~%16). **Menzil uzatıcı**. |
| Mg / Mg(CB₁₁H₁₂)₂ | Mg metal + karborat sıvı elektrolit | 3 V pencere, ~1 mS/cm | Mg katot kinetiği zayıf (Chevrel 1.1 V); enerji düşük. **İzleme**. |
| **Na / Na-kloso-borat katı** | Na | Na₂(B₁₂H₁₂)(B₁₀H₁₀) | NVP | ~1 mS/cm @ 20 °C, Na'ya kararlı | **Ana yol.** |

## 2.2 Kloso-borat anyonları: yapı ve kararlılık

- **[B₁₂H₁₂]²⁻**: 12 bor atomu düzgün bir **ikosahedron** oluşturur (B–B 1.78 Å, çevrel yarıçap
  1.69 Å, H dâhil ~2.9 Å, vdW ile ~4.0 Å; bkz. `geometri.py`). 26 iskelet elektronu (Wade
  kuralı, n+1 = 13 bağ çifti) kafes içinde üç boyutlu delokalizedir → "üç boyutlu aromatiklik".
  Sonuç: sıcak suda, asit/bazda, havada kararlı; termal bozunma > 500 °C.
- **[B₁₀H₁₀]²⁻**: iki başlıklı kare antiprizma (D₄d). Daha az simetrik → kafeste daha kolay
  düzensizleşir; saf Na₂B₁₀H₁₀ ~360 K'de süperiyonik faza geçer.
- **[CB₁₁H₁₂]⁻, [CB₉H₁₀]⁻**: bir B'nin C ile değiştirilmesi yükü −1'e düşürür → Na⁺-anyon
  etkileşimi zayıflar, iletkenlik artar (70 mS/cm sınıfı), ancak karboran sentezi pahalıdır.

### İletim mekanizması

Yüksek sıcaklık (veya anyon karışımıyla frustrasyona uğratılmış) fazda anyonlar bcc/fcc
kafeste yerlerinde **hızla yeniden yönelir** (ps ölçeği). Na⁺ iyonları, 4 Na için 12 site
(bcc Im-3m, 12d) gibi **düşük dolulukta** (1/3) tetrahedral sitelerde bulunur;
`geometri.na_bosluk_analizi` ölçülen yüksek-T kafesi (a = 7.9 Å; geçişte ~%15 hacim
genleşmesi) için bu sitelerde ~1.00 Å boşluk yarıçapı verir — Na⁺ (1.02 Å) ile neredeyse
birebir: iyon siteye tam oturur ama sıkışmaz, 2/3'ü boş komşu sitelere düşük engelle geçer. Anyon dönmesi komşu siteler
arasındaki engeli anlık olarak düşürür ("paddle-wheel"). Ea ≈ 0.2–0.4 eV.

Eş-molar **Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅** karışımı (Duchêne 2017), iki anyonun boyut/şekil
uyumsuzluğuyla düzenli fazı bastırır; oda sıcaklığında ~0.9 mS/cm, 60 °C'de ~6 mS/cm
(model: `elektrolit.iletkenlik_C`).

## 2.3 Elektrokimyasal kararlılık penceresi

| Sınır | Değer (vs Na⁺/Na) | Not |
|---|---|---|
| Katodik (indirgenme) | 0 V — Na metaline karşı termodinamik kararlı | Hidroboratlar zaten indirgenmiş; Na ile reaksiyon yok. Ana avantaj. |
| Anodik, termodinamik | ~3.0 V (B₁₂H₁₂²⁻ → B₁₂H₁₂⁻ oksidasyonu) | NaCrO₂ (2.95 V ort., 3.5 V kesim) bu sınırda güvenli çalışır. |
| Anodik, kinetik (pasifleşme) | ~4 V | Asakura 2020: ince oksidasyon ürünü tabakası iyonik iletken, elektronik yalıtkan → NVP (3.37 V) ve hatta NVPF (3.9 V) kararlı çevrim. |

Tasarım kararı: BorPil-A (NVP) pasifleştirici arayüz varsayımıyla; **doğrulanamazsa A0
(NaCrO₂) devreye girer**. Bu, projenin en önemli kimyasal riskidir ve deney planında ilk
sıradadır (`docs/06`).

## 2.4 Katot ve anot yarı reaksiyonları (BorPil-A)

    Katot:  Na₃V₂(PO₄)₃ ⇌ NaV₂(PO₄)₃ + 2Na⁺ + 2e⁻       E ≈ 3.37 V (V³⁺/V⁴⁺), 117.6 mAh/g teorik
    Anot:   Na⁺ + e⁻ ⇌ Na(s)                             E = 0 V, 1166 mAh/g
    Hücre:  ~3.37 V, aktif madde bazında 1/(1/110 + 1/1166) × 3.37 ≈ 339 Wh/kg (aktif)

Hücre düzeyinde (folyo, elektrolit, kılıf dâhil) model **191 Wh/kg** verir (`hucre.py`).

## 2.5 DBFC termodinamiği (menzil uzatıcı)

    Anot:   BH₄⁻ + 8OH⁻ → BO₂⁻ + 6H₂O + 8e⁻     E° = −1.24 V
    Katot:  2O₂ + 4H₂O + 8e⁻ → 8OH⁻              E° = +0.40 V
    Toplam: NaBH₄ + 2O₂ → NaBO₂ + 2H₂O           E° = 1.64 V  (model: 1.647 V, ΔG°f'lerden)

Teorik 5668 mAh/g, 9.3 kWh/kg NaBH₄. Pratik: %20 NaBH₄ / %10 NaOH çözeltisi, yük altında
0.85 V (0.7–0.9), %65 faradaik kullanım (%50–75) → ~630 Wh/kg çözelti, ~390 Wh/kg sistem
(tank+yığın). Yan reaksiyon (hidroliz, BH₄⁻ + 2H₂O → BO₂⁻ + 4H₂) hem yakıt kaybı hem H₂
güvenlik konusudur; alkali pH ve Au/Pd-Ni anot katalizörleriyle bastırılır. **NaBO₂ → NaBH₄
rejenerasyonu** (Mg veya elektrokimyasal indirgeme) teorik 9.3 kWh/kg, pratik verim %15–35
(ABD DOE'nin 2007 "no-go" kararının gerekçesi) → gidiş-dönüş ~%10.
Sonuç: DBFC, elektrik depolamak için değil, **yerli bor yakıtıyla menzil uzatmak** için.
Örnek boyutlandırma (`termodinamik.dbfc_menzil_uzatici`): 40 kg çözelti (8 kg NaBH₄) + 15 kW
yığın + tank/BOP ≈ 160 kg → 25 kWh, **+167 km**, 3 dakikalık sıvı dolum; harcanan NaBO₂
istasyonda toplanıp rejenerasyona gönderilir (kapalı bor döngüsü).

## 2.6 Isıl davranış ve Nernst etkisi

- OCV sıcaklık katsayısı NVP için küçüktür (|dE/dT| < 0.3 mV/K; düz plato, faz geçişli
  reaksiyon). Isıl model bu yüzden yalnız I²R (Joule) terimini alır; entropik ısı ihmal edilir.
- Hücre tasarım noktası 45 °C'dir: σ 3.1 mS/cm, 30 µm ayırıcı ASR ≈ 1 Ω·cm², toplam ASR
  (arayüzler dâhil) ≈ 29 Ω·cm²; 25 °C'de 83, −10 °C'de ~760 Ω·cm². Soğukta arayüz direnci
  (Ea ~0.45 eV) baskındır; bu yüzden paket ısıtıcıyla ≥ 35 °C'de tutulur (`docs/04`).
- Karışık karba-kloso-borat için tabloda 25 °C üstü değerler Arrhenius **ekstrapolasyonu**dur
  (195 mS/cm @ 60 °C ölçüm değil).

## 2.7 Kaynaklar (seçilmiş)

- Udovic, T. J. ve ark. *Chem. Commun.* **50**, 3750 (2014) — Na₂B₁₂H₁₂ süperiyonik iletim.
- Udovic, T. J. ve ark. *Adv. Mater.* **26**, 7622 (2014) — Na₂B₁₀H₁₀.
- Tang, W. S. ve ark. *Energy Environ. Sci.* **8**, 3637 (2015) — NaCB₁₁H₁₂ / LiCB₁₁H₁₂.
- Tang, W. S. ve ark. *Adv. Energy Mater.* **6**, 1502237 (2016) — NaCB₉H₁₀ / LiCB₉H₁₀ "sıvı benzeri" iletkenlik.
- Tang, W. S. ve ark. *ACS Energy Lett.* **1**, 659 (2016) — karışık anyon karba-kloso-borat katı çözeltisi, oda sıcaklığında ~70 mS/cm.
- Asakura, R. ve ark. *ACS Appl. Energy Mater.* **2**, 6924 (2019) — hidroborat oksidasyonu ve karbonun etkisi.
- Yabuuchi, N. ve ark. *Nat. Mater.* **11**, 512 (2012) — P2-Na₂/₃Fe₁/₂Mn₁/₂O₂.
- Duchêne, L. ve ark. *Chem. Commun.* **53**, 4195 (2017) — Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ elektroliti.
- Duchêne, L. ve ark. *Energy Environ. Sci.* **10**, 2609 (2017) — 3 V tamamen katı hâl Na hücresi (NaCrO₂).
- Asakura, R. ve ark. *Energy Environ. Sci.* **13**, 5048 (2020) — 4 V pasifleştirici arayüz.
- Duchêne, L., Remhof, A., Hagemann, H., Battaglia, C. *Energy Storage Mater.* **25**, 782 (2020) — hidroborat elektrolitler derlemesi.
- Brighi, M., Murgia, F., Černý, R. *Cell Rep. Phys. Sci.* **1**, 100217 (2020) — kloso-hidroborat Na tuzları derlemesi.
- Tutusaus, O. ve ark. *Angew. Chem. Int. Ed.* **54**, 7900 (2015) — Mg(CB₁₁H₁₂)₂ elektroliti.
- Jian, Z. ve ark. *Adv. Energy Mater.* **3**, 156 (2013) — Na₃V₂(PO₄)₃ katot.
- Amendola, S. C. ve ark. *J. Power Sources* **84**, 130 (1999); Ma, J. ve ark. *Renew. Sustain. Energy Rev.* **14**, 183 (2010) — DBFC.
- NIST-JANAF Termokimyasal Tablolar; CRC Handbook — ΔG°f değerleri.
