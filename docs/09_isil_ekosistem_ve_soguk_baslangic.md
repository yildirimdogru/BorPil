# 09 — Kurul oturumu: 35–60 °C bandı, atık ısı ekosistemi, zincirleme ısınma ve “katalizör”

**Tür:** 3. tur beyin fırtınası / karar oturumu (tutanak)  
**Gündem sahibi:** proje sahibi — “35–60 °C gerçek hayatta ağır dezavantaj; Türkiye’de ölü doğar mı;
atık ısıyı avantaja çevirmek; düşük akımla başlayan zincirleme ısınma; süperkapasitör katalizörü;
Mars/uzay.”  
**Sayılar:** `cikti/RAPOR.md`, `docs/04`, `docs/07` (P4–P7, P19). Yeni kod yok; bu belge karar ve
yol haritasıdır.

**Katılanlar (masa):** A1 elektrokimya · A2 katı hâl fiziği · A3 malzeme/üretim · A4 sayısal/ısıl
geometri · A5 güvenlik/toksikoloji · A6 sistem/ürün · H3 elektrik-elektronik · H4 batarya üreticisi ·
konuk: güç elektroniği (e-aks) · konuk: ultrakapasitör / hibrit ESS · konuk: iklim (TR) · konuk:
uzay güç sistemleri · kurul (5).

---

## 0. Proje sahibinin sözü (gündem, özet)

1. Pil 35–60 °C çekirdekte verimli. Bunu sahada tutmak kolay değil. Li-iyon da soğukta düşer ama
   bizim aralık daha kötü. Çöl şartı bir yana, **Türkiye kışı** projeyi ölü doğurur gibi duruyor.
   Belki Mars gibi “sıcak gezegen” / uzay daha uygun pazar.
2. Şarj + deşarj + motor sürücü kayıplarını paketi ısıtmaya çeviren **kompakt ekosistem** iyi fikir;
   adil puan istiyorum (10 üzerinden).
3. Gerçek kullanımda akım bir anda maksimuma çıkmaz: araç 0’dan 100’e atlamaz, şarj da rampelenir.
   Motor çalıştıkça ısınır → pil ısınır → performans artar; şarj başlar → ısınır → daha iyi şarj.
   Bu zinciri **kullanıcının fark etmeyeceği** süreye nasıl çekeriz? Aklımdaki katalizör:
   kompakt sisteme **süperkapasitör**.

Kurul bu dört iddiayı ayrı notlar; birbirine karıştırmaz.

---

## 1. Notlar, adil (10 üzerinden)

| İddia | Kurul notu | Ne anlama gelir |
|---|---:|---|
| “35–60 °C Türkiye’de projeyi öldürür” | **5 / 10** | Teşhis abartılı; **1 numaralı ürün riski** olduğu doğru (o ayrı, **8 / 10**) |
| Atık ısıyı ekosistem ürünü yapmak | **8 / 10** | Mimari olarak güçlü; soğuk uyanışı tek başına çözmez (**5 / 10**) |
| “Düşük akımla başlarız, zincirleme yeter” | **6 / 10** | Fizik doğru, tavan yanlış: −10 °C’de tepe **~7 kW** — birçok gerçek manevra bunun üstünde |
| Süperkapasitör = katalizör | **7,5 / 10** | Konfor tamponu ve darbe-ısıtma kaynağı olarak evet; paketi ısıtan şey olarak **4 / 10** |
| “Mars sıcak, orada daha avantajlı” | **3 / 10** | Mars **soğuk** (ortalama ≈ −60 °C). RTG’li uzay nişi ayrı, **6 / 10** |

---

## 2. “35–60 °C ölü doğum mu?” — uzman turu

### A2 — Katı hâl fizikçisi

Band hava sıcaklığı değil, **hücre içi** 35–60 °C. Kloso-borat σ(T) Arrhenius (Ea ≈ 0,4 eV);
CCD aynı aileden. Li-iyon LFP da −10 °C’de zayıf ama 25 °C’de “yeterli araba”dır. Bizde 25 °C
tepe güç **~70 kW**, 45 °C **~210 kW**, −10 °C **~7 kW**. Bu, LFP’den kötü bir *eğim*; 20 °C
ortamda ısıl stratejiyle menzil hâlâ **457 km**. Ölü doğum 20 °C İstanbul trafiği değil;
**prizsiz Erzurum sabahı + hemen çevre yolu**.

### Konuk — iklim (Türkiye)

Türkiye tek iklim değil.

| Bölge | Kış | Yaz | BorPil için asıl iş |
|---|---|---|---|
| İstanbul / Ege kıyı | nadiren −5, çoğu gün > 0 | 30–35 | Ön ısıtma + atık ısı yeter; 3 kW PTC |
| Ankara / İç Anadolu | −10 olası | 35 | Priz alışkanlığı veya tampon şart |
| Doğu (Kars, Erzurum) | −20…−30 | ılık yaz | Prizsiz “hemen gaza” **ölü** — katalizör veya darbe ısıtma olmadan satılmaz |
| Çukurova / Güneydoğu | ılık | **40–45 hava** | Ters problem: 60 °C tavan, ≥ 3 kW soğutma, invertör ısısını pakete basmamak |

“Çöl ülkesi değiliz o yüzden tamam” yanlış. Yazın Adana’da soğutma, kışın Doğu’da ısıtma —
**iki uç da Türkiye**. Ürünü öldüren şey bandın varlığı değil, **kullanıcının ilk 60 saniyede
ICE/LFP torku beklemesi**.

### A6 — Sistem

ICE de soğukta kördür; kimse “dizel Anadolu’da ölü” demedi çünkü ısınma *beklenen* bir ritüeldi.
EV müşterisi ritüel kabul etmez. Bu yüzden 35–60 **mühendislik olarak yaşar, ürün olarak
ancak gizlenirse yaşar.** Gizlemek = priz + zincir + tampon (aşağıda). Pivottan (yalnız uzay)
önce bu üçlüyü dene.

### A1 — Elektrokimyacı

Bandı 10–45 °C’ye çekmek = başka elektrolit (karba-kloso, gen-2 B) veya sıvı katkı. Gen-1
kloso-borat karışımının Ea’sı bu. “Daha soğukta çalışan BorPil” ayrı kimya projesi; bu oturumun
konusu değil. Na e.n. 97,8 °C üst bandı da sıkı tutar — 70 °C hava + yalıtım + takılı ısıtıcı
yine ASIL D.

### Kurul ara kararı (P21)

35–60 °C **Türkiye pazarını kapatmaz**; **Doğu kışı + prizsiz anında tam güç** senaryosunu
kapatır. Birincil pazar C-segment TR/AB, uzay değil. KPI: “anahtar çevirince ilk 20 s’de
kullanıcının hissettiği güç ≥ 50 kW” (ortam −10 °C, ön ısıtmasız) — bugünkü kimya tek başına
bunu vermez; tampon veya darbe ısıtma gerekir.

---

## 3. Atık ısı ekosistemi — puan **8 / 10**

### H3 — Elektrik-elektronik

P6 zaten 0,8 kW tahrik atık ısısı; DC’de 20 kW şebeke. Önerilen “paket + şarj + sürücü tek
ısıl ürün” bunu **SKU’laştırır**. 8 veriyorum çünkü:

- Sürüşte 35 °C’yi *tutmak* için doğru yer (PTC 2,0 kWh → daha az).
- DC’de 75 kW kapısı 44 °C; istasyon ısısı + 20 kW bunun parçası.

2 puan kırıyorum: atık ısı **güç varken** gelir. Parktan uyanışta invertör soğuk. OBC kaybı
yavaş şarjda çoğu zaman < 1 kW.

### Konuk — güç elektroniği

Kompakt e-aks + paket glikol döngüsü OEM’lere satılır bir “ısıl alan”dır. Ek hızlandırıcı
(zinciri ilk 30 s’de tutuşturmak): **kontak açık, hareket yokken** invertörde bilinçli kayıp
modüasyonu (loss heating) — sargı ve modül 2–5 kW ısı üretir, vana pakete basar. Gürültü ve
EMC var; 30–60 s rölanti ısınması. PTC’ye paralel, ASIL’de ayrı kanal değil (aynı glikol).
Vane yapışması hâlâ ortak arıza → 80 °C kesici durur.

### H4 — Üretici

Üç kutuyu (paket, OBC, invertör) tek tesisten satmak Tesla/BYD entegasyonu. BorPil Tier-2
ise satılacak şey **paket + ısıl kontrol ünitesi + flanş şartnamesi** (0,8 / 20 kW kapıları).
8/10 mimari, 6/10 iş modeli.

### A5 — Güvenlik

Isıyı pakete *bilerek* almak, takılı-kalma yüzeyini büyütür. Yazın 40 °C otoyolda invertör
ısısını pakete basmak 80 °C’ye yürür. Ekosistem **ısıtıcı ve soğutucu aynı vanada** olmak
zorunda; “sadece ısıt” kutusu yok.

### Kurul (P22)

Atık ısı ekosistemi **kabul, not 8/10**. Ürün adı taslağı: *BorPil Isıl Alan* (paket + vana
+ şarj ısıtma portu). Soğuk uyanış vaadi bu SKU’nun üzerine yazılmaz.

---

## 4. Zincirleme reaksiyon — “yavaş başlar, ısındıkça açılır”

### A4 — Sayısal

Paket 596 kg, c ≈ 1 kJ/kgK, UA ≈ 10 W/K.

| Kaynak | Yaklaşık net ısı | −10 → 35 °C (45 K) |
|---|---|---|
| PTC 3 kW (kayıp düşülmüş) | ~2,5 kW | **~3 saat** mertebesi (park) |
| Şebeke 20 kW | ~19 kW | **~25–30 dk** (RAPOR: −10→45 °C 28 dk) |
| Atık ısı 0,8 kW | 0,8 kW | tek başına pratik değil; *tutma* |
| Darbe 1C, −20 °C | **42 kW** (sonra düşer) | −20→0 °C **10 dk / 3,7 kWh** |
| I²R deşarj −10 °C, 7 kW tavan | küçük | tavan ısınmayı da boğar |

Tavuk–yumurta: soğukta **az akım çekebilirsin** → az I²R → yavaş ısınma. Zincir *pozitif
geri besleme* ancak CCD’nin izin verdiği akım ısınmayı besleyecek kadar büyükse çalışır.
−10 °C’de 7 kW’lık tavan, 596 kg’ı hızla ısıtmaz. 20 °C’de 70→210 kW eğrisi zinciri
**besler** — İstanbul kışının çoğu günü bu. Kars sabahı beslemez.

### A6

“Kullanıcı 100 km/h’ye anında çıkmaz” şehir içi doğrudur; **yokuş + sollama + çevre yolu
rampası** 10 saniye 80–150 kW ister. İlk 12 dk −10 °C sürüşte model zaten güç kısıtı yazıyor
(1,8 kWh açık). Zinciri merkeze almak doğru kontrol yasasıdır (`P_dch_max(T)` zaten var);
**konfor şartı değildir**.

### H3

Şarj tarafı zinciri daha temiz: istasyon 20 kW ile ısıtırken akım CCD ile rampelenir;
10→80 % −10 °C’de 54 dk, bunun ~%23’ü ön ısıtma. Kullanıcı “yavaş şarj”ı 54 dk’da zaten
hisseder — şarjda katalizör, süperkap’tan çok **20 kW şebeke**dir.

### Kurul (P23)

Rampeli zincir **kontrol yasası olarak onay** (zaten harita). Tek başına UX çözümü **değil**.
Hızlandırmak = tavanı (CCD×ısı) büyütmek veya tavanın altını **başka bir güç kaynağıyla**
doldurmak.

---

## 5. Süperkapasitör “katalizör mü?”

Katalizör metaforu kurulda şöyle düzeltildi: denge hâlâ 35–45 °C’dir (75 kW / 200 kW orada).
Kapasitör dengeyi değiştirmez; **aktivasyon bariyerini** (kullanıcının ilk 10–20 s’de duyduğu
güç açığını) düşürür.

### Konuk — ultrakapasitör

| Rol | İşe yarar mı | Not |
|---|---|---|
| Paketi kendi I²R’si ile ısıtmak | Zayıf | 0,2 kWh’lik kap, 3 kW PTC’nin 4 dakikasına denk; 596 kg’ı ısıtmaz |
| Çekiş tamponu (soğuk açık güç) | **Güçlü** | 10 s × 80 kW ≈ 0,22 kWh; EDLC ~6 Wh/kg → **~35 kg**, kaba maliyet 3–5 bin USD |
| Darbe (AC) ısıtmaya akım kaynağı | **Güçlü** | Soğuk paket CCD yüzünden DC veremez; ortalama sıfır AC’yi kap + invertör verebilir (P5, EIS) |
| Rejen yutma soğukta | Orta | CCD/1,5 rejen tavanı; fazlası zaten mekanik fren — kap freni kurtarır |

EDLC lityum içermez — marka ile uyumlu. **Ama** tipik asetonitril/organik elektrolit **yanıcıdır**.
“Pakette yanıcı sıvı yok” broşürü, kap kutusunda yanıcı sıvı varsa yırtılır. İyonik sıvı /
kuru kap: daha pahalı, daha zayıf güç.

Aynı kimyadan **2–4 kWh’lik “pilot” yığın** (küçük kütle, sürekli 35 °C, küçük PTC): lityumsuz,
yanıcı kap yok, hem kalkış gücü hem glikole tohum ısı. Üretimde ikinci format. Kurul ikisini
rakip değil **sıra** görür.

### A3 — Malzeme

35 kg kap + kutu, 596 kg pakette %6. Wh/kg düşer (125 → ~118). Maliyet 412 USD/kWh üzerine
~50 USD/kWh ekleyici — gen-1 zaten pahalı. Hacim ürününe gen-1’de koyma; **kış paketi /
Doğu SKU / filo** olarak opsiyon.

### A1

Na | kloso-borat üzerine kHz AC, P5’te EIS’siz baz yasak. Kap + invertör bu deneyi *kolaylaştırır*
(paketi DC ile zorlamadan). Sıra: EIS → darbe ısıtma → kapı isteğe bağlı kap kaynağı.

### A5

İki enerji deposu = iki yangın modeli. Kap kutusu paket tepsisinden ısıl ve sızdırmaz ayrı;
söndürme sınıfı farklı olabilir (organik kap ≠ D sınıfı Na).

### Kurul (P24)

Süperkapasitör **gen-1 baz değil** (maliyet, yanıcı kap elektroliti, kütle).  
**Gen-1,5 / kış opsiyonu** olarak kavramsal kabul: 0,15–0,25 kWh EDLC veya 2 kWh aynı kimya
pilot yığın; amaç kullanıcıya −10 °C’de ilk 15–20 s ≥ 50–80 kW.  
Darbe ısıtmanın akım kaynağı olarak kap, EIS sonrası P5’e bağlanır.

---

## 6. Zinciri hızlandırmak — ne yapabiliriz? (öncelik sırası)

Kullanıcının fark etmemesi = **hissettiği güç ve şarj süresi**, paket termometresi değil.

| # | Aksiyon | Etki | Süre / enerji | Engel | Kurul |
|---|---|---|---|---|---|
| 1 | Takvim / priz ön ısıtma (şebeke) | Uyanışta zincir gerekmez | −10→45 °C ~28 dk, ~9 kWh şebeke | Evde priz yoksa sıfır | **Gen-1 zorunlu UX** (yazılım + kılavuz) |
| 2 | Kontakta invertör kayıp ısıtması 2–5 kW | Zinciri tutuşturur, hareket yok | 1–3 dk “hazır” lambası | EMC, gürültü, 80 °C kesici | **P25a** kavram, e-aks ile |
| 3 | Atık ısı vanası (P6) + 20 kW DC (P2) | Tutma + şarj zinciri | modelde var | Yazın soğutma | **Duruyor, SKU’laştır (P22)** |
| 4 | Darbe AC 1C (P5) | Derin soğuktan çıkış | −20→0 °C 10 dk | EIS, Na arayüz | **Pilot sonrası baz adayı** |
| 5 | Çekiş tamponu (kap veya pilot yığın) | İlk 10–20 s güç açığını gizler | 0,2 kWh / ~35 kg veya 2 kWh Na | maliyet, yanıcı kap | **P24 opsiyon** |
| 6 | 40–45 °C faz değişim (PCM) ceketi | 30–90 dk park sonrası sıcak kal | kütle + sızıntı | geceyi kurtarmaz | **İzleme, gen-2** |
| 7 | PTC’yi 6 kW’a çekmek | Park süresini ~2× kısaltır | 95 dk Na erimesi (takılı) | ASIL, P4/P5’te 3 kW’a inildi | **Red; kesici olmadan asla** |
| 8 | Kimyayı 10–45 °C’ye çekmek (B, karba-kloso) | Bandı yumuşatır | maliyet, tedarik, CCD kilit | gen-2 LT | **A1 raporu `docs/10`; bu oturumda yoktu** |

“Katalizör” pratikte tek parça değil: **(1) priz + (2) kayıp ısıtma + (4) darbe + (5) tampon**.
(1) ve (3) bugün var. (2)(4)(5) kullanıcı farkını kapatan katmanlar.

### Şarj zincirini hızlandırmak

DC’de darboğaz CCD değil ısınmaysa (RAPOR: −10 °C sürenin %23’ü ön ısıtma): 20 kW’ı **30 kW**
istasyon opsiyonu (kablo/istasyon); pakette I²R’yi CCD içinde tut. Süperkap şarjı hızlandırmaz
(enerjisi kWh cinsinden yok). Şarj katalizörü **şebeke ısıtıcı gücü**.

### Deşarj zincirini hızlandırmak

İlk 20 s tampon (5) + eşzamanlı (2) veya (4). Tampon bitmeden paket 5–10 K ısınırsa CCD
yükselir, tampon doldurulabilir (rejen / yavaş DC). Bu, istenen pozitif geri beslemedir —
**kapasitör ısınmanın yerine geçmez, ısınmaya zaman satın alır.**

---

## 7. Uzay ve Mars — kısa ve net

### Konuk — uzay güç sistemleri

Mars yüzey ortalama ≈ **−60 °C**, gece −120 °C civarı; ekvator öğleni nadiren 20 °C.
“Sıcak gezegen” **Venüs** (~460 °C) veya Merkür gündüzüdür; ikisi de Na e.n. 97,8 °C’nin
üzerinde — bu hücre orada durmaz.

BorPil’in uzayda *gerçek* avantajı sıcak gezegen değil: **vakumda konveksiyon yok**, RTG/RHU
zaten atık ısı verir, 35–60 °C’yi tutmak gezegen yüzeyinden kolay olabilir; yanıcı elektrolit
yokluğu mürettebat/rover için değerli. Bu **niş** (kg ve rad dayanımı ayrı iş). C-segment
TR pazarının plan B’si değil.

### Kurul (P26)

Pazar pivotu yok. Uzay: izleme notu, RTG atık ısı + vakum yalıtımı. Mars “sıcak” gerekçesi
**redd** (olgu hatası).

---

## 8. Kurul kararları (P21–P26)

| P# | Konu | Karar | Not |
|---|---|---|---|
| P21 | 35–60 °C Türkiye’yi öldürür mı | **Öldürmez; 1. UX riski** | KPI: −10 °C ön ısıtmasız ilk 20 s ≥ 50 kW (tampon/darbe ile) |
| P22 | Atık ısı ekosistemi | **8/10, SKU’laştır** | *Isıl Alan*; soğuk uyanış vaadi yok |
| P23 | Rampeli zincir | **Kontrol yasası evet, UX hayır** | Harita durur; tavanı dolduracak katman şart |
| P24 | Süperkapasitör katalizör | **Gen-1 baz değil; 1,5 opsiyon** | 0,15–0,25 kWh EDLC veya 2 kWh pilot Na yığın; yanıcı kap elektroliti broşür riski |
| P25 | Hızlandırma yığını | **1→2→4→5 sırası** | Priz zorunlu UX; kayıp ısıtma kavram; darbe EIS sonrası; tampon opsiyon; PTC 6 kW yok |
| P26 | Mars/uzay pivot | **Yok** | Mars soğuk; uzay niş izleme |

Muhalifler (kayıt): sistem mühendisi P24’te “kış SKU’suz Doğu’da satışa çıkmayın” (kabul notu);
üretici P24 maliyetine karşı (opsiyon olduğu için geçti); elektrokimyacı P5/P25 darbe sırasını
EIS’siz öne almaya karşı (sıraya uyuldu).

---

## 9. Toplantı kapanışı — proje sahibine doğrudan

35–60 °C **kabul edilmesi gereken bir maliyet**; çöl masalı değil, Türkiye’nin iki ucu da
(Doğu kışı, güney yazı) bunu zorlar. Li-iyon’dan kötü eğim gerçek. Ölü doğum değil —
**gizlenmeyen soğuk tork** ölü doğum.

Atık ısı ekosistemi **8/10**: doğru ticari çerçeve; zinciri *tutarsın*, *tutuşturmazsın*.

Düşük akımla başlayan zincir **6/10**: İstanbul’da çoğu gün çalışır; −10 °C’de 7 kW tavan
zinciri boğar.

Süperkapasitör **katalizör olarak 7,5/10** eğer onu ısıtıcı sanmazsak: kullanıcıya zaman
satın alır; paketi 35 °C’ye o getirmez. Asıl hızlandırıcılar sırayla **priz, invertör kayıp
ısısı, darbe AC (EIS), sonra tampon**.

Mars’a taşımak **kaçış değil**; orası daha soğuk. Isıyı evde, istasyonda ve e-aksta evcilleştirmek
bu kimyanın ev ödevi.

Sonraki iş paketleri (kod/deney, bu tutanakta model değişmedi): e-aks kayıp-ısıtma kavramı;
P24 tampon kütle-maliyet bandı; P5 EIS kapısı; iklim KPI’sinin `surus` senaryosuna eklenmesi
ayrı görev.
