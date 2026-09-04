# 11 — Kurul oturumu: yaşayan ısıl sistem (soğukta sürmek ve şarj)

**Tür:** tüm ekipler toplantısı + çalıştırılabilir model  
**Gündem sahibi:** proje sahibi — “Arabayı soğukta sürebilmek ve şarj edebilmek.” Öneri: batarya
paketi için **tam bir ısıtma–soğutma sistemi**; kendi kendini ısıtan ve soğutan **canlı** bir
organizma. Sistem ölürse paket de ölü kabul. Fabrikada full SOC ile doğar; yaşamı için
kullanıcının enerjisinden her zaman bir pay keser. Mükemmelleşince son kullanıcı LFP/NMC gibi
biner — ön ısıtma ritüeli yok.  
**Sayılar:** `python -m borpil.cli yasam` ve `cikti/RAPOR.md §13` (`borpil/yasayan_isil.py`).  
**Kimya notu:** `docs/10` soğuk gücü tuz formülüyle çözmez (CCD kilit). Bu oturum kimyayı
değiştirmez; **ısıl yaşamı** ürünün içine alır.

**Katılanlar (masa):** A1 elektrokimya · A2 katı hâl fiziği · A3 malzeme/üretim · A4 sayısal/ısıl
geometri · A5 güvenlik/toksikoloji · A6 sistem/ürün · H3 elektrik-elektronik · H4 batarya üreticisi ·
konuk: iklim (TR) · konuk: güç elektroniği (e-aks) · kurul (5).

P19 (parkta 35 °C tutma yok) **iptal edilmez.** YIS, P19’un yanındaki **işletim modudur.**

---

## 0. Proje sahibinin sözü (aynen, sonra mühendislik diline)

1. Tam ısıtma **ve** soğutma. Tek yönlü PTC yetmez.
2. Sistem **yaşayan** olsun: kendini ısıtsın, kendini soğutsun.
3. Bu sistem ölürse **batarya paketi de ölür** — kabul.
4. Fabrika: ilk üretimde **full batarya**, sistem canlı doğar.
5. Yaşam payı: kullanıcı enerjisinden **her zaman** bir dilim kesilir; gösterge LFP gibi 0–100.
6. Mükemmelleşince kullanıcı NMC/LFP alışkanlığıyla binsin.

Kurul bu altıyı ayrı oylar; “kimya 10 °C’de CCD açsın” ile karıştırmaz (`docs/10` duruyor).

---

## 1. Fizik masası — neden “canlı” olmak zorunda?

### A2 — Katı hâl fizikçisi

Gen-1 kloso-borat **hücre çekirdeğinde 35–60 °C** ister. Hava 35 °C değil. Tepe güç modelde
~210 kW @45 °C, ~70 kW @25 °C, **~7 kW @−10 °C**. 75 kW DC kapısı paket **≥ 44–45 °C**.
CCD 1,5 mA/cm² @25 °C, Ea 0,45 eV. Kimya hattı (LT) bulk σ’yu 10 °C’de açar, CCD’yi açmaz.

Dolayısıyla soğuk araba iki iştir:

| İş | Kimya (docs/10) | YIS (bu belge) |
|---|---|---|
| −10 °C’de tork | CCD yükselt (gen-2, yapılmadı) | Paketi **zaten 25–35 °C**’de tut |
| 10→80 % DC | aynı CCD kilidi | Kalkış T yüksek → 20 kW şebeke ısıtıcı 45 °C’ye daha kısa |

YIS kimyayı 10 °C’de “LFP yapmaz”. YIS, kullanıcının **paketi soğuk görmemesini** sağlar.

### A4 — Isıl denklem (kodda aynı)

Parkta tek havuz:

```
m · c · dT/dt = P_ısıtıcı − P_soğutma − UA · (T − T_ortam)
```

A-alt paket: m ≈ 596 kg, c = 1 kJ/kg·K, UA ≈ **10,1 W/K** (12 mm aerojel, 5,5 m²).
Zaman sabiti τ = m·c/UA ≈ **16 h**. −10 °C’de 35 °C tutmak ≈ **450 W** sürekli;
25 °C tutmak ≈ **350 W**. Yaşam payı %8 × 74 kWh ≈ **5,9 kWh** → 35 °C’yi **sıkı** tutarak
prizsiz ≈ **13 h**; 25–35 °C histerezisle bir kış gecesi (12 h) yaşar, 48 h hâlâ canlı kalır
(rezerv + kullanıcının üst SOC’si). Bu sayı bir bug değil: **prizsiz LFP-gibi UX yalıtım ve
priz olmadan sonsuz değildir.**

### Konuk — iklim (TR)

| Park | Priz | YIS ne yapar |
|---|---|---|
| İstanbul gecesi, −2 °C, 10 h | evde | 35 °C sıkı; kullanıcı sabah LFP gibi |
| Ankara, −10 °C, 12 h | yok | histerezis 25–35 °C; tork var, 75 kW DC yok (45 °C kapısı) |
| Erzurum, −20 °C, 48 h, priz yok | yok | rezerv biter → T→10 °C → **Ready yok** (kabul edilen ölüm) |
| Adana, 40 °C, 12 h | evde | soğutma 55 °C’de devreye; 12 h’de tavan aşılmaz |

---

## 2. Tasarım — yaşayan paket

### A6 — Sistem (ürün sözleşmesi)

```
Fabrika doğumu: SOC = 1.00, T = 35 °C, TMS = sağ  →  canli = True
Kullanıcı göstergesi 0–100:  SOC_görünür = clip((SOC − 0.08) / (0.96 − 0.08), 0, 1)
Çekiş SOC tabanı = yaşam payı (0.08); TMS prizsiz bu tabanın altına inebilir (ölene kadar)
Ready = TMS_ok ∧ T ≥ 10 °C ∧ SOC > 0
TMS arızası veya T < 10 °C  →  Ready yok, çekiş yok  (paket ölü)
```

Kullanıcı %100 gördüğünde brüt ~%96’dadır (üst tavan, ömür); %0 gördüğünde hâlâ %8 yaşam payı
vardır. Bu, LFP’nin “gösterge 0 = boş” alışkanlığına **ters** durur gibi görünür; aslında LFP
BMS’i de alt tampon bırakır. Fark: bizim tampon **ısıtıcıyı hayatta tutmak** içindir.

### A3 — Donanım

Mevcut gen-1 parçalar yeter, yeni kimya yok:

- 3 kW PTC (P5) + 80 °C bağımsız kesici (P4)
- ≥ 3 kW sıvı plaka, COP ≈ 2,5 (yazın e-aks ısısını **pakete basmamak**)
- 12 mm aerojel (UA ≈ 10 W/K) — prizsiz ömrü uzatmanın asıl kolu yalıtım kalınlığıdır
- BMS: yaşam payı coulomb sayımında ayrı kova; gösterge kovayı gizler

İsteğe bağlı gen-1,5: yalıtım 20 mm → UA ~6 W/K → prizsiz 35 °C tutma ~1,7× uzar.

### H3 — Elektrik-elektronik (uyarı, kabul ile)

Yaşayan sistem = parkta ısıtıcı **silahlı**. P4 zinciri durur (kesici, ayrı kontaktör, çift NTC).
P19’un gerekçesi buydu: 35 °C 24/7, günde 3,6–11 kWh **ve** takılı-kalma riski.
Kurul şimdi riski **ürün kararı** olarak alıyor: sistem ölürse paket ölür; o yüzden TMS
ASIL hedefi **yükselir**, düşmez. Fail-operational değil, **fail-dead** — sahip bunu istedi.

Parkta priz yokken ısıtıcı paketten; prizde şebekeden (V2H/V2G değil, TMS öncelikli).

### H4 — Üretici (doğum prosedürü)

Hat sonu: paket 35 °C fırın / sıvı döngüde, SOC 100 %, TMS self-test geçmeden sevkiyat yok.
Soğuk depo sevkiyatı: yaşam payı + yalıtım + mümkünse 48 V bakım prizi. “Ölü paket” servis
modu: şebekeden 20 kW ile 10 °C üstüne diriltme — **ayrı prosedür**, Ready değil.

### A1 — Elektrokimyacı

YIS, 35–60 °C bandını **gizler**, iptal etmez. LT hattı hâlâ gen-2. 10 °C’de CCD ile 75 kW
beklemeyin; canlı paket 25–35 °C’de sürülür, DC’de şebeke 45 °C’ye taşır.

### A5 — Güvenlik

Fail-dead: sürücü −20 °C’de yolda TMS kaybederse araç **derhal** güçsüzleşir (T düşmese bile
Ready kesilir). Bu, “ısınarak evine dön”den kötü. Kurul: TMS yedek (2. NTC hattı + 2. kontaktör)
**P4’te zaten var**; yazılım Ready’yi TMS_ok’a bağlar. Na erimesi hâlâ kesici işi, YIS ölümü değil.

### Konuk — e-aks

Soğutma döngüsü yazın paket tavanını, kışın atık ısıyı paylaşır (P6/P22). YIS soğutmayı
“canlılığın diğer yarısı” yapar: T > 55 °C → plaka. 40 °C Adana parkı 12 h modelde soğutma
tetiklemez (UA küçük, iç üretim yok); otoyol + DC şarj tetikler.

---

## 3. Simülasyon — ne çıktı?

Komut: `python -m borpil.cli yasam --ortam -10 --park-saat 12`  
Kod: `borpil/yasayan_isil.py`. P19 varsayılan `PaketGereksinimi` değişmez.

Özet (A-alt, model; rapor §13 güncel sayıyı basar):

- Doğumda kullanıcı **~65 kWh** görür / **~74 kWh** brüt (%8 yaşam + %4 üst tavan).
- **Gen-1** −10 °C 12 h: kalkış T = −10 °C, güç kısıtı büyük, 10→80 % uzun (paket soğuk).
- **YIS prizsiz** 12 h: T histerezis bandında (25–35 °C), canlı, gösterge hâlâ yüksek;
  sürüş kısıtı gen-1’in **çok altında**; DC hâlâ 45 °C kapısı için şebeke ısıtıcı kullanır
  ama −10 °C’den değil 25–35 °C’den çıkar.
- **YIS prizli** 12 h: T ≈ 35 °C, SOC değişmez, şebeke ~5 kWh (450 W × 12 h); LFP-gibi hedef.
- **TMS ölü:** Ready yok, `kullanici_surusu` → `None`.
- **48 h prizsiz −10 °C:** model canlı kalır (histerezis + brüt SOC); **sürekli 35 °C**
  istenirse rezerv ~13 h’de biter — bu yüzden alt eşik 25 °C.

Dürüst cümle: **LFP-gibi sabah, priz veya kısa park veya daha kalın yalıtım ister.**
Prizsiz Doğu kışı 48 h “sonsuz canlı organizma” değildir; ölen sistem / ölen pakettir.

---

## 4. Kurul kararları (P27–P32)

| P# | Konu | Karar | Not |
|---|---|---|---|
| P27 | Yaşayan ısıl sistem | **Kabul, paralel mod** | P19 SKU varsayılanı durur; YIS `yasam` işletim modu / gen-1,5 ürün |
| P28 | Fail-dead | **Kabul** | TMS arızası veya T < 10 °C veya SOC = 0 → Ready yok; paket ölü |
| P29 | Fabrika doğumu | **Kabul** | Sevkiyat: SOC 100 %, T 35 °C, TMS self-test |
| P30 | Yaşam payı | **%8 brüt + %4 üst tavan** | Gösterge gizler; çekiş tabanı %8; TMS prizsiz tabanın altına inebilir |
| P31 | Prizsiz UX sınırı | **Kabul, iddia yok** | 12 h −10 °C canlı; 24/7 35 °C prizsiz vaat **yok** (UA fiziği) |
| P32 | Isıtma + soğutma | **Tek canlı döngü** | Isıt 25–35 °C (priz 35), soğut ≥ 55 °C, kesici 80 °C |

Muhalif kayıt: H3 “parkta silahlı PTC ASIL’i yükseltir” (P4 zinciri + fail-dead ile geçti);
H4 “doğum fırını hat maliyeti” (P29 prosedür, SKU opsiyonu); A6 “P19’u kaldırmayın, iki SKU
tutun” (kabul — P27 paralel).

---

## 5. Çalışma grubu (sinerji, kapanış)

Grup adı: **YIS — yaşayan paket.** Sahip: A6. Fizik: A2/A4. Donanım: A3/H4. Güvenlik: H3/A5.
Kimya izleme: A1 (`docs/10`, CCD). İklim senaryoları: konuk iklim → `cli yasam --ortam`.

Sonraki iş (bu oturumda yok): yalıtım 20 mm duyarlılığı; 48 V bakım prizi; TMS yedek
kanıtı (HIL); şebekeden diriltme prosedürü. Kimya CCD’si ayrı hat.

Proje sahibine doğrudan: öneriniz **kabul ve kodlandı.** Organizma metaförü fiziğe oturuyor —
enerji yemeden ısınan cisim yok; pay kesiliyor; ölünce Ready yok. Mükemmel LFP taklidi
**prizde** bugün modelde var; prizsizde histerezis ve dürüst menzil/güç. Bu, soğuk sorununun
çözüm sözleşmesidir, mucize tuz değil.
