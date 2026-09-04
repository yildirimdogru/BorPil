# BorPil EV-74

**Lityumsuz. Yanıcı sıvı yok. Bor, iyonun otoyolu.**

Tamamen katı hâl çekiş bataryası — C-segment binek ve hafif SUV.

---

## Bir bakışta

| | EV-74 Standard | EV-74 Pro |
|---|---:|---:|
| Enerji | **74,2 kWh** brüt / **68,3 kWh** net | aynı |
| Paket | **596 kg · 512 L · 125 Wh/kg** | 519 kg · 418 L · 143 Wh/kg |
| Mimari | 404 V · 120s3p · **3 bağımsız dizi** | aynı zarf |
| Menzil* | **457 km** (20 °C, ısıl strateji) | 474 km |
| DC 10→80 % | **32 dk** (paket 45 °C) | 34 dk |
| Lityum / kobalt / nikel / bakır (hücre) | **0** | 0 |
| Bor | **92 kg** | 70 kg |

\*C-segment referans: 1350 kg glider + 150 kg yük, WLTP-benzeri çevrim, ısıtıcı dâhil.

---

## Neden BorPil?

**Bor katkı değil, iletimin kendisi.**  
[B₁₂H₁₂]²⁻ ve [B₁₀H₁₀]²⁻ kafes anyonları oda sıcaklığında dönen, geniş boşluklu bir
kristal kurar. Na⁺ bu yolda düşük engelle (Ea ≈ 0,4 eV) gider. Li-iyon’daki yanıcı
organik elektrolitin yerini **katı kloso-borat tuzu** alır.

**Isıl kaçak zinciri kırılır.**  
Yanıcı buhar yok. NVP katot O₂ salmaz. Ayırıcı 130 °C’de eriyen poliolefin değil.
Kalan riskler yönetilir: sodyum metal, nem, ısıtıcı — bağımsız 80 °C donanım kesici,
üç dizi, soğukta akım-plausibilite.

**Kritik metal yok.**  
Hücrede lityum, kobalt, nikel, bakır yok. Sodyum tuzdan, bor Türkiye rezervinden,
vanadyum fosfat kafesinde (Fe SKU’da vanadyum da yok). Paket başına maden bütçesi:
`docs/08`.

**Sıcak çalışır, soğukta ısınır.**  
35–60 °C bu kimyanın verimli bandıdır. 3 kW PTC + tahrik atık ısısı sürüşte hedefi tutar;
DC istasyonda 20 kW şebeke ısıtıcı 75 kW şarj kapısını açar. Kışın prize takılı ön ısıtma
−10 °C menzilini **474 km**’ye çıkarır.

**Bir dizi gider, iki dizi kalır.**  
Üç bağımsız 120s dizi: yumuşak kısa bir dizide yakalanır, araç 2/3 güçle eve döner.

---

## Kimya, bir cümle

```
Al | Na₃V₂(PO₄)₃ (ALD) + kloso-borat | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ | Na metal | Al
```

Katot kütlece %71 NVP, %25 katı elektrolit, %2 karbon, %2 bağlayıcı. Her iki tarafta
alüminyum folyo — bakır yok.

---

## Filo ve OEM için üç karar noktası

1. **Güvenlik dosyası.** Yanıcı elektrolit kalemi kapanır; Na ve ısıtıcı kalemleri açılır.
   Entegrasyon kılavuzu bu kalemleri ASIL ile bağlar — atlanan montaj “yanmaz” iddiasını
   düşürür.  
2. **Şarj hikâyesi.** 75 kW kimya tavanıdır, kablo değil. Müşteriye “32 dk / 45 °C paket”
   denir; soğuk pakette istasyon önce ısıtır (54 dk @ −10 °C, 20 kW şebeke).  
3. **Tedarik.** 92 kg bor / paket yerli cevherle ölçeklenir; kısıt cevher değil hidroborat
   sentezidir. Geri dönüşümde kloso-borat suda kristalleşir, yeniden sentez gerekmez.

---

## Ürün ailesi

| SKU | Kimin için |
|---|---|
| **EV-74 Standard** | Hacim C-segment; bugünün üretim kalınlıkları (60 µm SE, 50 µm Na) |
| **EV-74 Pro** | Aynı enerji, 77 kg daha hafif paket, daha yüksek Wh/L |
| **EV-74 Fe** | Vanadyum istemeyen pazar ve maliyet hattı |

Garanti (ürün şartnamesi): **8 yıl / 160 000 km**, kullanılabilir enerji ≥ %70.
Soğukta güç sınırı arıza değildir; ön ısıtma kullanımın parçasıdır.

---

## Teknik kutu (Standard)

- 74,2 / 68,3 kWh · 404 V (283–452 V) · 360 hücre  
- 80 kW sürekli · ~210 kW tepe @ 45 °C · ~7 kW tepe @ −10 °C  
- 75 kW DC, paket ≥ 44 °C  
- Pouch-in-frame, 1,2 MPa yığın, 12 mm aerojel  
- 3 kW PTC · 0,8 kW atık ısı · ≥ 3 kW soğutma @ 60 °C  
- Söndürme: D sınıfı / inert — **modüle su yok**

Tam tablo: `BorPil-EV74_teknik_veri_formu.md`  
Montaj: `BorPil-EV74_entegrasyon_kilavuzu.md`  
Güvenlik / garanti: `BorPil-EV74_guvenlik_ve_garanti.md`

---

## English (one page)

**BorPil EV-74** — lithium-free all-solid-state traction battery. Boron is the ionic
highway (closo-borate SE), not a boron anode. **74.2 kWh**, 404 V, 596 kg, **457 km**
WLTP-like in a C-segment car at 20 °C. **No Li, Co, Ni or Cu in the cell.** 92 kg of
boron per pack. No flammable liquid electrolyte. DC charge 75 kW once the pack is warm
(32 min 10→80 % at 45 °C). Three independent strings. Independent 80 °C heater cut-off.
Class D extinguishing; no water on modules. Warranty 8 years / 160 000 km to 70 %
usable energy.

---

*BorPil — bor esaslı, lityumsuz katı hâl.*  
Teknik sayılar tasarım modelinden (`borpil`, `cikti/RAPOR.md`). Belge seti:
`docs/urun/00_urun_belge_seti.md`.
