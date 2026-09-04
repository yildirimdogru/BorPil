# BorPil EV-74 — OEM entegrasyon kılavuzu

**Belge:** BP-IG-074 · Rev A  
**Kapsam:** Standard (BP-EV74-S-404). Pro / Fe aynı arayüz, farklı kütle ve ısıl atalet.  
**Hedef okuyucu:** HV sistem, ısıl, gövde, yazılım (BMS/VCU), servis mühendisi.

Bu kılavuz, paketin araca **nasıl bağlanacağını** ve **hangi iş kurallarının zorunlu**
olduğunu anlatır. Hücre kimyası ve maden bütçesi burada tekrarlanmaz:
`BorPil-EV74_teknik_veri_formu.md`, `docs/08`.

---

## 1. Sistem mimarisi (araçta ne görürsünüz)

```
        ┌──────────── 3 bağımsız 120s dizi ────────────┐
CCS DC ─┤ Dizi 1 — akım şöntü — kontaktör — 120 hücre  │
400 V   ┤ Dizi 2 — akım şöntü — kontaktör — 120 hücre  ├── HV bus 283–452 V
        ┤ Dizi 3 — akım şöntü — kontaktör — 120 hücre  │
        └──────── paket kontaktörü + ön şarj 100 Ω ────┘
                         │
              BMS (CAN FD) + bağımsız 80 °C ısıtıcı kesici
                         │
         3 kW PTC ── ayrı kontaktör ── 12 V / şebeke (DC’de 20 kW)
         3 kW soğutma plakası ── glikol ── araç soğutma
         0,8 kW atık ısı ── termostatik vana (hedef+5 K kapanır)
```

Üç dizi **hücre-içi 3p değildir**. Her dizi kendi akım sensörü ve kontaktörüne sahiptir.
Bir dizi izole edilirse araç **2/3 güçle** gidebilir; Na dendrit yumuşak kısa, dizi
dengesizliği olarak yakalanır.

---

## 2. Mekanik montaj

| Madde | Şart |
|---|---|
| Konum | Taban / kayıkçık; ağırlık merkezi düşük tutulur (596 kg Standard) |
| Zarf | 1600 × 1200 × 270 mm (Pro aynı ayak, daha alçak yığın) |
| Pabuç | 8–12 adet M10; tork OEM şablonu (öneri 45–55 N·m, kilit somun) |
| Yığın basıncı | **Araçtan bağımsız.** Disk yay + çerçeve 1,2 ± 0,3 MPa sağlar. Gövde
  ezmesi yığını sıkıştırmamalı; 2 mm yay stroku bırakın |
| Şarj şişmesi | Hücre kalınlığı ~%10 artabilir (~1,9 mm). Çerçeve bunu yutar; tavan
  sacı yığına dayanmamalı |
| Çarpışma | Paket tepsisi yük yolundan ayrı; HV kilit (HVIL) kaput/koltuk altında değil,
  paket flanşında |

Kaldırma: yalnız işaretli kancalar. Forklift dişini taban oluklarına alın; hücre düzlemine
dik darbe yasak.

---

## 3. Yüksek gerilim

| | Değer / kural |
|---|---|
| Pencere | 283–452 V. Invertör DC-link ve şarj cihazı **500 V sınıfı** |
| Tepe akım | 495 A (200 kW / 404 V). Busbar + kontaktör + sigorta bütçesi ≈ **2 mΩ** |
| Ön şarj | 100 Ω, ~60 ms; VCU DC-link = paket gerilimi ±%5 olmadan ana kontaktör kapanmaz |
| Tab | Al, 0,3 mm × 100 mm; sürekli ≤ 2,5 A/mm² (tasarım 2,2) |
| İzolasyon | ≥ 500 Ω/V; BMS her uyanışta ölçer, altındaysa Ready yasak |
| HVIL | Seri kilit; koparsa 100 ms içinde kontaktör aç |
| Konnektör | 400 V CCS Combo DC araç prizi + paket içi 2 kutup (OEM seçimi, IP67) |

**Kısa devre — soğukta sigorta yetmez.** 45 °C’de beklenen kısa ~5 kA (Pro ~8 kA);
**−10 °C’de ~190 A** (Pro ~310 A) — sürekli çalışma akımının altında. Sigorta (≥ 16 kA
kesme, sıcak paket için) tek başına ayırt edemez.

Zorunlu VCU/BMS kuralı:

1. Paket akımı ↔ invertör/şarj cihazı akımı plausibilite (eşik OEM, öneri %15 veya 40 A).  
2. **dI/dt** eşiği: beklenmeyen yükselişte kontaktör aç (ASIL C).  
3. Soğukta “sigorta atmadı = kısa yok” **yanlış** kabul edilir.

---

## 4. Isıl entegrasyon — “sıcak batarya”

Kloso-borat 35–60 °C’de daha iletkendir. Soğuk paket **güçsüzdür**, tehlikeli değildir;
ısıtıcı takılı kalması ise **ASIL D** tehlikedir.

### 4.1 Sürüş

| | Kural |
|---|---|
| Hedef | Paket **35 °C** |
| PTC | 3 kW, yalnız paket içi plaka |
| Atık ısı | Tahrikten 0,8 kW, termostatik vana; hedef + 5 K’de kapanır |
| Soğutma | 60 °C üstünde ≥ 3 kW sıvı plaka |
| Kabin | Kabin HVAC paketi soğutmak için kullanılmaz (tersine de PTC kabini ısıtmaz) |

20 °C ortamda strateji ~2,0 kWh ısıtıcı çeker (menzil 457 km). Isıtıcısız menzil 472 km
ama 25 °C’de tepe güç ~70 kW’a düşer — müşteri şikâyeti ve yokuş/sollama riski.

### 4.2 DC şarj

| | Kural |
|---|---|
| Hedef | Paket **45 °C** |
| Şarj gücü | **75 kW tavan**; CCD/1,5. Paket **< 44 °C ise 75 kW yok** |
| Isıtıcı | **20 kW şebekeden** (istasyon veya araç içi AC→paket ısıtıcı). 3 kW PTC ile
  −10 °C’de 10→80 % 95 dk olur; 20 kW ile **54 dk** |
| Soğutma | Şarjda paket 45 → 55–57 °C; plaka açık |

VCU, CCS’ten 75 kW istemeden önce BMS `pack_T_min ≥ 44` ve `ccd_headroom` bitini bekler.

### 4.3 Park ve V2G

35 °C tutulmaz (günde 3,6–11 kWh kayıp). Paket soğur. V2G / rejen akımı `CCD(T)/1,5` ile
sınırlıdır; fazla rejen **mekanik frene** gider — fren aşınması kışın artar, bu normaldir.

### 4.4 Isıtıcı güvenlik zinciri (kesilemez iş kuralı)

Yalıtımlı pakette (UA ≈ 10 W/K) PTC **kendiliğinden sınırlanmaz**: 3 kW → +17–20 K/h;
6 kW yasak türevi +40 K/h ve ~95 dk’da Na erimesi.

| Katman | Ne | Bağımsızlık |
|---|---|---|
| BMS yazılım | 80 °C güç kes / 90 °C ayır | MCU-A |
| Donanım | **80 °C** bimetal veya termal sigorta | BMS yazılımından ayrı |
| Kontaktör | Isıtıcıya **ayrı** kontaktör (HV paket kontaktöründen ayrı) | — |
| Sıcaklık | Çift NTC, ısıtıcı plakasında; karşılaştırma | MCU-B önerilir |
| ISO 26262 | ASIL D → **B(D)+B(D)** | tek MCU yetmez |

OEM, ısıtıcıyı VCU üzerinden “sürekli açık” bırakacak bir konfor senaryosu yazamaz.

---

## 5. BMS ve yazılım arayüzü

CAN FD, 500 kbit/s varsayılan (2 Mbit/s seçenek). Döngü 10–100 ms.

### 5.1 OEM’in uyması gereken sinyaller (minimum)

| Sinyal | Yön | Anlam |
|---|---|---|
| `U_pack`, `I_pack`, `I_s1..s3` | BMS→VCU | Dizi akımları ayrı; sapma > %3 uyarı, sürekli > 50 mA denge sapması arıza |
| `T_min`, `T_max`, `T_heater` | BMS→VCU | T_heater bağımsız zincir |
| `SOC` | BMS→VCU | Coulomb sayımı birincil; OCV platosu düz (~1 mV/%SOC) — alt uçtan kalibrasyon yok |
| `SOH`, `R_pack` | BMS→VCU | dR/dT ≈ −5…−7 %/K; R sapması yumuşak kısa erken uyarı |
| `P_dch_max(T,SOC)`, `P_chg_max`, `P_regen_max` | BMS→VCU | **Harita bağlayıcıdır.** VCU bu tavanı aşamaz |
| `allow_75kW_dc` | BMS→VCU | T ≥ 44 °C ve CCD payı |
| `string_open[3]` | BMS→VCU | İzole dizi; tork 2/3 |
| `crash`, `HVIL`, `iso_fault` | ↔ | 100 ms açma |
| `heat_cmd`, `cool_cmd` | VCU→BMS | BMS reddedebilir (T, ASIL) |

SOC: her tam şarjda üst diz (> 3,5 V/hücre) yeniden kalibrasyon. Dengeleme yalnız üst
dizde, pasif 150–300 mA/kanal.

### 5.2 Güç haritası (özet)

Deşarj: 25 °C ~70 kW → 45 °C ~210 kW.  
Şarj/rejen: 25 °C ~26 kW → 45 °C ~78 kW.  
−10 °C deşarj tepe ~7 kW.  
Deşarj akım tavanı `min(CCD×2, 12 mA/cm²)`; şarj/rejen `CCD/1,5`.

VCU, soğukta “tam gaz” isteyemez; sürücü gösterge metni önerilir:
*“Batarya ısınıyor — güç sınırlı. Ön ısıtmayı prize takılıyken kullanın.”*

---

## 6. Şarj istasyonu

- CCS 400 V, cihaz tavanı 150 kW / 500 A olsa bile **paket 75 kW** ister.  
- İstasyon veya araç, DC süresince **20 kW paket ısıtıcısına** şebeke vermelidir
  (ayrı AC pin veya HV’den DC-DC — OEM seçimi, BMS `grid_heat_kW`).  
- ISO 15118: `EVSE` 75 kW’ı “yavaş” sanmasın; bu kimya tavanıdır, kablo değil.

---

## 7. Üretim hattı ve sevk (OEM montaj)

- Sevk SOC %30 ± 5.  
- Paketi açmayın; kuru oda yalnız BorPil fabrikası ve yetkili hücre servisi.  
- Montajda HV kapağı torklu; nemli bezle dış yüzey, **su jeti yasak**.  
- İlk uyanış: izolasyon, üç dizi OCV (±%1,5–2 binning), NTC, ısıtıcı kesici süreklilik.

---

## 8. Yasaklar (etiketle aynı)

1. Paketi suya daldırmayın; kaza sonrası D sınıfı / inert, **su yok**.  
2. Isıtıcıyı BMS/kesici atlatarak sürmeyin.  
3. Dizileri araç içinde paralel busbar ile “tek 3p” yapmayın.  
4. 800 V invertöre 120s paketi bağlamayın (pencere uyumsuz değil ama mimari SKU ayrı).  
5. Hücre kesmeyin, Na havaya açılır.

Kontrol listesi ve kaza prosedürü: `BorPil-EV74_guvenlik_ve_garanti.md`.
