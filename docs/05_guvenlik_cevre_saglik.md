# 05 — Güvenlik, Çevre ve Biyolojik Etki (A5 Biyolog/Toksikolog, A1 Kimyacı)

## 5.1 Hücre güvenliği: neden ısıl kaçak zinciri kırılır?

Li-iyon'da ısıl kaçak zinciri: SEI bozunması → ayırıcı erimesi → iç kısa devre → katot O₂
salımı → **yanıcı karbonat elektrolitin** yanması. BorPil'de:

| Halka | Li-iyon | BorPil-A |
|---|---|---|
| Elektrolit | Yanıcı organik sıvı (parlama noktası ~30 °C) | Katı kloso-borat tuzu; yanmaz, buhar basıncı yok |
| Ayırıcı | PE/PP, 130–165 °C'de erir | Elektrolit filminin kendisi; >400 °C kararlı |
| Katot O₂ salımı | NMC 200–250 °C'de O₂ | NVP (polianyon, P–O bağı) O₂ salmaz; NaCrO₂/Fe-Mn oksit sınırlı |
| Anot | Grafit/Li; Li ile elektrolit ekzotermik | Na metal — su ve hava ile reaktif (aşağıda) |

Kalan iki risk **Na metal** ve **hidrojen**dir:

- **Na metal** (şarjlı hâlde paket başına ~35 kg: 14 kg fazlalık + ~21 kg döngüsel; hücrelerde
  dağılmış, 46 µm folyo): kılıf delinmesinde hava/nem ile ekzotermik reaksiyon
  (Na + H₂O → NaOH + ½H₂). "Yanıcı elektrolit yok" ifadesi hücreyi yanmaz kılmaz: erimiş Na
  (e.n. 97.8 °C; 35–60 °C çalışma sıcaklığına marj ~40 K) + nem ciddi tehlikedir. Ancak sıvı
  elektrolit yokluğunda yayılacak yanıcı ortam yoktur; hasar yerel kalır. Pouch üstüne Al-laminat + tepside inert
  köpük dolgu ile önlem. Çarpışma testinde (UN 38.3 T6 ezme, GB 38031 delme) referans:
  Na katı hâl hücreleri için ısıl kaçak yerine yerel ısınma beklenir; doğrulanacak (docs/06).
- **Hidrojen:** kloso-boratlar hidroliz etmez (BH₄⁻'nin aksine). Yalnız > 400–500 °C'de
  bozunmada H₂ salarlar. Bu sıcaklığa hücrede ulaşılması için dış yangın gerekir; paket
  havalandırma kanalı bu senaryo için yeterlidir. DBFC modülünde ise NaBH₄ hidrolizi sürekli
  H₂ kaynağıdır → ayrı havalandırma ve H₂ sensörü zorunlu.

Yüksek çalışma sıcaklığı (35–60 °C) elektrolit açısından sorunsuzdur (ısıl kararlılık çok
üstte); tasarım sınırı Na'nın erime noktasıdır: BMS 80 °C'de gücü keser, 90 °C'de paketi ayırır.
**Nem:** Na₂B₁₂H₁₂ hidrat (·4H₂O) oluşturur; hidrat hem iletkenliği düşürür hem Na ile
reaksiyona girer → hermetik hücre, üretimde < 100 ppm H₂O (kurul P15).

**Elektrik-elektronik kaynaklı tehlikeler (kurul P3, P4):**
- *Isıtıcı takılı kalma:* yalıtımlı pakette (UA ≈ 10 W/K) ısıtıcı kendiliğinden sınırlanmaz; 3 kW'ta
  +17–20 K/h, 6 kW'ta +40 K/h ve ~95 dk'da Na erimesi. ISO 26262 tehlike sınıfı ASIL D →
  B(D)+B(D) ayrıştırma: BMS yazılım sınırı (80 °C güç kesme / 90 °C ayırma) + bağımsız donanım
  (80 °C bimetal/termal sigorta, ayrı ısıtıcı kontaktörü, ayrı MCU, çift NTC).
- *Soğukta kısa devre:* paket direnci −10 °C'de 25× büyük → kısa devre akımı 190–310 A (sürekli
  akımın altında); sigorta ayırt edemez, paket ısınır, direnç düşer, akım katlanır (pozitif geri
  besleme). Koruma: akım-plausibilite (paket ↔ invertör/şarj cihazı) + dI/dt ile kontaktör açma;
  sigorta kesme kapasitesi ≥ 16 kA (60 °C durumu).
- *Aşırı şarj:* kesim 3.77 V, pasifleşme tavanı 4.0 V (230 mV marj) → ASIL C; ölçüm ±5 mV.
- *Söndürme:* D sınıfı + inert gaz; modül düzeyinde su yasak (Na).

## 5.2 Toksikoloji

| Madde | Akut toksisite | Kronik / sınıflandırma | Değerlendirme |
|---|---|---|---|
| Borik asit / boratlar (bozunma / geri dönüşüm ürünü) | Düşük (LD₅₀ oral sıçan ~2.5–4 g/kg) | AB CLP: Repr. 1B (üreme toksisitesi, yüksek dozda) — sınıfla­ma boraks ve borik asit için | İşyeri maruziyet sınırı (ör. 2 mg/m³ B) ile yönetilir; toz kontrolü |
| Na₂B₁₂H₁₂ / Na₂B₁₀H₁₀ | Veri sınırlı; kimyasal olarak inert, çözünür tuz | Kloso-borat anyonları biyolojik ortamda kararlı; karboranlar BNCT'de (bor nötron yakalama terapisi) hasta uygulamalarında kullanılır → düşük toksisite göstergesi | REACH kayıt gerekecek; tam GLP veri seti projenin bir iş paketidir |
| Diboran, dekaboran (sentez ara ürünü) | **Yüksek** (B₂H₆ IDLH 15 ppm; B₁₀H₁₄ deri yoluyla emilir) | Nörotoksik | Yalnız kapalı sentez tesisinde; hücrede bulunmaz |
| Na metal | Kostik (NaOH oluşumu) | — | Mekanik koruma, kuru söndürücü (D sınıfı) |
| NVP (V³⁺/V⁴⁺) | Vanadyum bileşikleri: V₂O₅ toksik/solunum irritanı; NVP fosfat kafesinde düşük çözünürlük | V₂O₅ IARC 2B | Toz kontrolü; A-Fe varyantı V'yi tamamen kaldırır |
| NaCrO₂ | Cr(III) düşük; **Cr(VI)** oluşumu üretimde/oksidasyonda risk | Cr(VI) kanserojen | A0 yalnız kapalı proses ve Cr(VI) analiziyle |
| Al, C, NBR | Düşük | — | — |

Li-iyon karşılaştırması: NMC'de Ni/Co bileşikleri (Co: Carc. 1B; Ni: solunum kanserojeni)
ve LiPF₆ hidrolizinden HF. BorPil-A'nın toksikolojik profili LFP'ye yakın veya daha iyidir;
en belirgin kalem üreme toksisitesi sınıfındaki borat tozudur (deterjan/cam endüstrisinde
onlarca yıllık yönetim pratiği mevcuttur).

## 5.3 Çevre ve yaşam döngüsü

- **Madencilik:** bor açık ocak, düşük enerji yoğunluğu; sodyum tuzdan; vanadyum çelik cürufu
  yan ürünü olabilir. Li salamura buharlaştırma (su ayak izi) ve Co (etik risk) yok.
- **Üretim enerjisi:** elektrolit dolum/ıslatma/formasyon adımlarının kısalması ve düşük
  formasyon sıcaklığı Li-iyon'a göre hücre başına enerjiyi düşürür; kuru oda gereksinimi
  benzer; hidroborat sentezi (H₂ salımı, çözücü geri kazanımı) ek yük getirir. Tahmini
  hücre üretim CO₂e: LFP ile aynı mertebe (ayrıntılı LCA iş paketi).
- **Kullanım:** Yüksek sıcaklık stratejisinin ön ısıtma enerjisi (kışın 5 kWh) menzili
  ~%9 düşürür; Li-iyon'da da ön şartlandırma kaybı vardır (daha küçük).
- **Geri dönüşüm:** Hidrometalurjik yol: hücre kırma (Ar) → su ile Na sönümleme → NaOH +
  Na₂B₁₂H₁₂ çözeltisi (kloso-borat suda kararlı, **doğrudan kristalizasyonla geri kazanılır**,
  yeniden sentez gerekmez) → süzüntüde NVP/Al ayrımı (yoğunluk/flotasyon) → V asit liçi.
  Kloso-boratın kimyasal kararlılığı, geri dönüşümde Li-iyon'a göre belirgin avantajdır.
- **Uç senaryo:** yangında B₂O₃/borat + NaOH külü; HF, PF₅, Ni/Co dumanı yok.

## 5.4 Biyoloji ile bağ: neden bu ekipte bir biyolog var?

1. Bor, bitkiler için esansiyel, memeliler için muhtemelen esansiyel bir iz elementtir; doğal
   sularda mg/L düzeyinde bulunur. Sızıntı senaryosunda ekotoksisite eşiği (sucul ortamda
   ~1–10 mg B/L kronik) yönetilebilir düzeydedir; borlu tuzların geri dönüşümü ekonomik
   olduğundan sızıntı motivasyonu da düşüktür.
2. Karboran/kloso-borat kimyası tıpta (BNCT ilaçları, radyofarmasötikler) kullanılır; bu
   bileşiklerin in-vivo kararlılık verisi, elektrolit toksikoloji dosyası için hazır bir
   başlangıçtır.
3. Sürücü/servis personeli maruziyet senaryoları (toz, Na metal, H₂) risk değerlendirmesi
   biyolog tarafından yürütülür; pil söküm tesislerinde biyoizleme (idrar B) protokolü önerilir.
