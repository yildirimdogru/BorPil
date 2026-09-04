# BorPil EV-74 — Güvenlik, servis ve garanti

**Belge:** BP-SG-074 · Rev A  
**Birlikte okuyun:** teknik veri formu, entegrasyon kılavuzu, `docs/05`.

---

## 1. Ürün tehlikeleri (özet SDS)

| Madde | Nerede | Tehlike | Normal kullanımda maruziyet |
|---|---|---|---|
| Na metal | Anot, şarjlı hücrede dağılmış folyo | Su/hava ile kostik + H₂; e.n. 97,8 °C | Hermetik pouch; yok |
| Kloso-borat tuzu | SE + katot kompozit | Toz: borat CLP Repr. 1B (yüksek doz, işyeri) | Hücre kapalı; sızıntıda ıslak temizlik değil, vakum + PPE |
| NVP (V³⁺/V⁴⁺) | Katot | V₂O₅ tozu irritan (üretim); kafeste düşük çözünürlük | Serviste kırma yoksa yok |
| Al, C, NBR | Folyo, karbon, bağlayıcı | Düşük | — |
| Diboran / dekaboran | **Yalnız sentez tesisi** | Yüksek toksisite | Hücrede **yok** |

**Yok:** LiPF₆, HF, Co, Ni, yanıcı karbonat elektrolit, H₂S (sülfür SE değil).

Yangın uç ürünü: B₂O₃/borat + NaOH külü. HF / PF₅ / Ni-Co dumanı beklenmez.

### 1.1 Söndürme ve kaza

- Sınıf: **D** (metal) + inert gaz (Ar/N₂).  
- **Modül ve açık hücreye su, köpük, CO₂ karı yasak** (Na + su). Dış muhafaza yangınında
  itfaiye suyu yalnız **komşu araç / yapı** için; paket tepsi drenajı NaOH’u kanalizasyona
  vermemeli (toplama).  
- Havalandırma: >400–500 °C dış yangında kloso-borat H₂ salabilir — paket tahliye kanalını
  tıkamayın.  
- Kaza sonrası: HVIL kopuk, 60 dk bekleme, IR kamera, yetkili servis. Paketi delmeyin.

### 1.2 İşyeri (servis / geri dönüşüm)

- Kuru oda veya Ar eldiven kutu: açık hücre.  
- Toz: 2 mg/m³ B mertebesi işyeri sınırı (yerel mevzuat).  
- Biyoizleme (söküm tesisi): idrar B, `docs/05 §5.4`.  
- Fe SKU: vanadyum liçi yok; Standard/Pro sökümünde V asit liçi ayrı hat.

---

## 2. Isıl kaçak neden “yok” denir — ve ne kalır

Li-iyon zinciri (SEI → ayırıcı erimesi → O₂ + yanıcı buhar) bu kimyada kırılır: katı
kloso-borat yanmaz, NVP O₂ salmaz, ayırıcı 130 °C PE değildir.

Kalan riskler:

1. **Na + nem** — yerel ekzoterm, yayılacak yanıcı ortam yok.  
2. **Isıtıcı takılı kalma** — yalıtım + PTC, Na erimesine götürür.  
3. **Soğuk kısa** — sigorta kör, paket ısınır, akım katlanır.  
4. **Aşırı şarj** — kesim 3,77 V, pasifleşme tavanı 4,0 V (230 mV); ASIL C.

Bu dört risk entegrasyon kılavuzundaki donanım/yazılım kurallarıyla yönetilir; atlanırsa
ürün “yanmaz batarya” iddiası geçersizdir.

---

## 3. Servis

| İş | Kim | Not |
|---|---|---|
| Dış temizlik, konnektör, yazılım | Yetkili bayi | Su jeti yok |
| Dizi kontaktörü, BMS kutusu | Yetkili HV teknisyen | SOC %30, HV kilit |
| Hücre / yığın | Yalnız BorPil veya sözleşmeli söküm | Kuru oda |
| Isıtıcı kesici, çift NTC | HV + ısıl | ASIL parça; eşdeğer yedek |
| Soğutma plakası kaçak | ısıl | Glikol; pakete su girişi = hurda adayı |

**Yedek parça:** paket tamir kiti (kontaktör, BMS, NTC, kesici, yay). Hücre SKU’su
sahada değişmez; dizi arızasında paket değişimi veya fabrika.

Arıza kodları (örnek): `E-HT-80` donanım kesici, `E-SC-COLD` soğuk kısa şüphesi,
`E-STR-IMB` dizi dengesizliği, `E-ISO` izolasyon, `E-CCD` şarj T kapısı.

---

## 4. Taşıma ve depolama

- UN 38.3 testli; sınıf 9, sodyum metal içeren katı hâl hücre (etiket OEM lojistik
  şablonu).  
- Sevk %30 SOC.  
- İstifleme: palet etiketi; 2 kasa yüksekliği (şablon).  
- Depo: kuru, −20…+45 °C, HV kapakları kilitli.  
- Hasarlı paket: kırmızı kasa, kum/inert yatak, su yok.

---

## 5. Geri dönüşüm (satışa hazır üründe taahhüt)

1. Ar altında kırma.  
2. Su ile kontrollü Na sönümleme (kapalı reaktör, H₂ yakma).  
3. Na₂B₁₂H₁₂ / B₁₀H₁₀ **doğrudan kristalizasyon** — yeniden sentez gerekmez.  
4. NVP / Al yoğunluk veya flotasyon.  
5. V asit liçi (Standard / Pro). Fe SKU’da Fe/Mn oksit hat.

Bu yol, Li-iyon’daki LiPF₆ / NMC ayrımına göre kloso-borat kararlılığı avantajı taşır.
Filo iade: paket başına ~92 kg B (Standard) ekonomik geri kazanım kalemidir.

---

## 6. Garanti (ürün-formu şartname)

Geçerli: ilk son kullanıcı veya filo, kayıtlı OEM aracında, entegrasyon kılavuzuna uygun montaj.

| Kalem | Şart |
|---|---|
| Süre | **8 yıl veya 160 000 km** (hangisi önce) |
| Enerji | Kullanılabilir kapasite ≥ **%70** (23 ± 5 °C, 0,3C, BMS kalibrasyonlu) |
| Dizi | Tek dizi kalıcı açık → paket değişimi veya eşdeğer onarım |
| Isıl | Donanım kesici ve çift NTC arızası kapsamdadır |
| Hariç | Su ile söndürme / daldırma, ısıtıcı atlatma, açılmış pouch, kaza,
  SOC’nin sürekli %5–95 dışı (BMS izin vermezse zaten), yetkisiz yazılım |
| Soğuk güç | −10 °C’de ~7 kW **arıza değildir**; ön ısıtma kullanıcı/filo yükümlülüğü |
| 75 kW şarj | Paket < 44 °C iken 75 kW yokluğu arıza değildir |

Çevrim hedefi 1500–3000 (tasarım KPI). Garanti enerji ile ölçülür, çevrim sayacı ile değil.

---

## 7. Sürücüye / filoya kısa uyarılar (kullanım kılavuzu metni)

1. Kışın aracı prize takılı bırakın; “ön ısıtma” menzil ve gücü geri verir (−10 °C’de
   440 → **474 km** Standard).  
2. Gösterge “güç sınırlı / ısınıyor” derse yokuşta sollamayın.  
3. DC istasyonda 30–55 dk 10→80 % **normaldir** (kimya tavanı 75 kW).  
4. Kaza: sarı HV etiket, yaklaşmayın, su sıkmayın, 112’ye “sodyum metal katı hâl paket”
   deyin.  
5. Paketi evde sökmeyin.

---

## 8. English safety box

No flammable liquid electrolyte. Remaining hazards: **Na metal + moisture**, **stuck
heater** (independent 80 °C cut-off required), **cold short** (fuse blind — use
plausibility + dI/dt). Extinguish with **Class D / inert gas; no water on modules**.
Warranty 8 yr / 160 000 km to 70 % usable energy. Cold power limit is specified
behaviour, not a defect.
