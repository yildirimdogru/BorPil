# 00 — Bilim Ekibi, Roller ve Yöntem

BorPil projesi tek bir uzmanın değil, disiplinler arası bir ekibin ürünüdür. Bu depo, ekibin
kararlarını yalnızca metin olarak değil, **çalıştırılabilir modeller** (`borpil/` paketi) ve
**otomatik üretilen rapor** (`cikti/RAPOR.md`) olarak kayıt altına alır. Her sayısal iddia
koda bağlıdır; kod değişirse rapor değişir.

## Ekip (ajanlar) ve sorumluluk alanları

| Ajan | Disiplin | Sorumluluk | Deponun ilgili kısmı |
|---|---|---|---|
| **A1 — Elektrokimyacı** | Kimya | Reaksiyonlar, Gibbs enerjileri, hücre potansiyelleri, kararlılık pencereleri, elektrolit kimyası | `termodinamik.py`, `malzemeler.py`, `docs/02` |
| **A2 — Katı hâl fizikçisi** | Fizik | İyon taşınımı (Arrhenius, faz geçişleri), arayüz direnci, kritik akım yoğunluğu, ısıl model | `elektrolit.py`, `simulasyon.py` |
| **A3 — Malzeme bilimci** | Malzeme bilimi | Sentez rotaları, folyo/kompozit reçeteleri, üretim prosesi, tedarik zinciri (Türkiye boru), maden bütçesi | `hucre.py` reçeteler, `docs/03`, `docs/08` |
| **A4 — Matematikçi / geometrici** | Matematik, geometri | [B12H12]²⁻ ikosahedronu, kafes boşluk analizi, paketleme geometrisi, sayısal çözümler | `geometri.py`, `simulasyon.py` çözücü |
| **A5 — Biyolog / toksikolog** | Biyoloji, çevre | Bor, sodyum, vanadyum toksikolojisi; hidrojen salımı; yaşam döngüsü ve geri dönüşüm | `docs/05` |
| **A6 — Sistem mühendisi** | Otomotiv | Paket mimarisi, gerilim, güç, ısıl yönetim, sürüş çevrimi, maliyet; ürün formu belgeler | `paket.py`, `karsilastirma.py`, `docs/04`, `docs/08`, `docs/urun/` |
| **H1, H2 — Bağımsız hakemler (1. tur)** | Kimya/fizik; sayısal model | Kör inceleme: sabitler, literatür uyumu, birim hataları | `docs/06 §6.3` |
| **H3, H4 — Bağımsız uzmanlar (2. tur)** | Elektrik-elektronik; EV batarya üretimi | Mimari, BMS, ısıl-elektrik, güvenlik; format, proses, verim, maliyet, nitelendirme | `docs/07` |
| **Kurul (5 üye)** | Tüm disiplinler | H3/H4 önerilerini oylar, ödünleşimleri karara bağlar | `docs/07 §7.3` |

## Yöntem

1. **Problem tanımı.** Lityum ağırlıklı kimyaların yerine, birincil enerji taşıyıcısı olarak
   *bor içeren* ve elektrikli araçta (EV) kullanılabilecek bir batarya. Kısıtlar: Li içermemek,
   EV paket ölçeğinde üretilebilirlik, güvenlik, bor açısından yerli tedarik.
2. **Aday kimyaların taranması** (A1, A2): bor-hava, doğrudan borhidrür yakıt pili (DBFC),
   Mg / karba-kloso-borat, Na / kloso-borat katı elektrolit, Li-borhidrür (elendi: Li içerir).
   Termodinamik üst sınırlar `borpil termo` ile hesaplanır; seçim ölçütleri `docs/02`.
3. **Seçim.** Ana yol: **Na-metal | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ | Na₃V₂(PO₄)₃** tamamen katı hâl
   hücre (BorPil-A). Bor, hücrenin iyonik omurgasını (elektrolit + katot kompozitinin
   iyonik fazı) oluşturur; hücre kütlesinin ~%19'u bordur. Yedek/alt varyantlar: A0 (NaCrO₂),
   A-Fe (vanadyumsuz), B (karba-kloso-borat, 4 V), C (sert karbon anot), S (Na-S).
   DBFC menzil uzatıcı olarak ikincil yol.
4. **Parametrik modelleme** (A3, A4, A6): katman yığını → hücre → paket → araç. Her seviye
   ayrı modül; varsayımlar veri sınıflarında açık alanlar olarak tutulur.
5. **Doğrulama** (H1, H2): birim testleri (`tests/`), literatürle çapraz kontrol, bağımsız
   el hesabı. İki hakem ajan kör inceleme yaptı; 10 "düzeltilmesi gereken" ve 4 "kesin hata"
   bulgusu kodda giderildi, sorgulanabilir varsayımlar band/duyarlılık olarak rapora işlendi.
   Bulgular ve düzeltmeler `docs/06 §6.3`'te kayıt altındadır.
6. **Dürüstlük ilkesi.** Maliyet ve ömür gibi henüz kanıtlanmamış büyüklükler "varsayım"
   olarak işaretlenir (`maliyet_varsayim` alanı). Rapor, üstünlükleri kadar sınırları da yazar.

## Karar günlüğü (özet)

| # | Karar | Gerekçe |
|---|---|---|
| K1 | Bor-hava birincil kimya olarak **reddedildi** | Teorik 15 kWh/kg (B başına) cazip; ancak B₂O₃/borat pasivasyonu, tersinirsizlik ve oda sıcaklığında B oksidasyon kinetiği çözülmemiş. Yalnızca teorik referans. |
| K2 | DBFC ana depolama olarak **reddedildi**, menzil uzatıcı olarak **tutuldu** | NaBO₂→NaBH₄ rejenerasyonu dâhil gidiş-dönüş verimi ~%16; elektrik→elektrik depolama için uygun değil. Yakıt olarak bor (NaBH₄) yerli ve yüksek enerjili. |
| K3 | Na / kloso-borat katı hâl **ana yol** | Oda sıcaklığında >1 mS/cm, Na metaline karşı termodinamik kararlılık, yanıcı değil, soğuk preslenebilir, Li içermez, bor ağırlıklı (kütlece %69 B). |
| K4 | Katot: NVP (ana), NaCrO₂ (muhafazakâr), Na-Fe-Mn oksit (düşük maliyet) | NVP: düz 3.37 V platosu, düşük hacim değişimi; NaCrO₂: kloso-borat penceresinde kanıtlanmış tam hücre; Fe/Mn: vanadyum riskini sıfırlar. |
| K5 | Anot: Na metal (ana), sert karbon (güvenli varyant) | Na metal en yüksek enerji; kloso-borat Na'ya kararlı. Sert karbon dendrit riskini kaldırır, %25 enerji kaybı. |
| K6 | Al akım toplayıcı her iki tarafta | Na, Al ile alaşım yapmaz → Cu gereksiz (maliyet, kütle). |
| K7 | Çalışma penceresi 35–60 °C (ısıtıcı hedefi 35 °C), hücre tasarım noktası 45 °C | Kloso-borat iletkenliği sıcaklıkla artar (Ea ≈ 0.4 eV); yanıcı elektrolit olmadığı için ısıl kaçak riski yok, yalıtım + ısıtıcı ile yönetim. Isıtıcı %3 menzil karşılığında tepe gücü 3× artırır. |
| K8 | Sonuçlar tasarım noktası + muhafazakâr alt tahmin (A-alt) olarak **band** hâlinde raporlanır | Hakem H1 bulgusu: 30 µm SE / 20 µm Na / 15 Ω·cm² varsayımları üst sınırdır; 60 µm / 50 µm / 30 Ω·cm² ile 177 Wh/kg. |
| K9 | **A-alt 1. nesil ticari baz çizgisi**, A hedef (kurul P11) | 30 µm serbest film ve 20 µm Na folyo bugün endüstriyel değil; üretilebilirlik > enerji yoğunluğu. |
| K10 | 120s3p, **3 bağımsız dizi**, pouch-in-frame, 80 °C ısıtıcı kesici, 20 kW şebeke ısıtıcı, 0.8 kW atık ısı, parkta ısıtma yok (kurul P4–P10, P19) | Elektrik-elektronik ve üretici incelemeleri; güvenlik oyları baskın. |
| K11 | Maliyet modeli gen-1 gerçekçi: ×1.75, verim %75, +32 USD/kWh (kurul P13) | Şeffaflık; 120 USD/kWh iddiasından vazgeçildi, hedef bandı 165–200. |

## Ürün formu belgeler

Tasarım satışa hazır bir SKU olsaydı OEM ve pazara verilecek set `docs/urun/` altındadır
(EV-74 veri formu, entegrasyon, güvenlik/garanti, broşür). Maden/element bütçesi
`docs/08`. Sayılar `borpil` modeline bağlı kalır; sertifika numaraları şablondur.
