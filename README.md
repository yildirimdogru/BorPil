# BorPil — Bor Esaslı, Lityumsuz Elektrikli Araç Bataryası

Lityum ağırlıklı pil kimyalarına alternatif olarak, **bor** içeren ve elektrikli araçlarda
kullanılabilecek bir batarya tasarımı: disiplinler arası bir bilim ekibinin (kimya, fizik,
malzeme bilimi, matematik/geometri, biyoloji, sistem mühendisliği) kararları, hesapları ve
simülasyonları.

**Ana tasarım (BorPil-A):** Na-metal anot | Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅ kloso-borat katı
elektrolit | Na₃V₂(PO₄)₃ katot — tamamen katı hâl, yanmaz, Li/Co/Ni/Cu içermez; hücre
kütlesinin ~%19'u bor.

| | BorPil-A (model) | LFP | NMC811 |
|---|---:|---:|---:|
| Hücre | 191 Wh/kg, 337 Wh/L | 170 / 380 | 265 / 700 |
| 75 kWh paket | 521 kg, 0 kg Li, 72 kg B | 613 kg, 6.8 kg Li | 393 kg, 8.2 kg Li, 56 kg Ni |
| WLTP-benzeri menzil (C-segment) | ~490 km | | |
| Yanıcı elektrolit | yok | var | var |

## Depo yapısı

```
borpil/            Python paketi (modeller)
  sabitler.py        fiziksel sabitler, molar kütleler
  malzemeler.py      malzeme veri tabanı (elektrolitler, katotlar, anotlar, Li-iyon referansları)
  termodinamik.py    Gibbs → E°, Nernst, bor-hava & DBFC teorik sınırları
  elektrolit.py      kloso-borat iletkenliği (Arrhenius, faz geçişi), ASR, kritik akım
  geometri.py        [B12H12]2- ikosahedronu, kafes boşluk analizi, pouch/paket geometrisi
  hucre.py           katman yığını → Wh/kg, Wh/L, element bütçesi, maliyet (varyantlar A, A0, A-Fe, B, C, S)
  paket.py           EV paketi boyutlandırma (seri/paralel, kütle, hacim, ısıl, maliyet)
  simulasyon.py      OCV+R eşdeğer devre, toplu ısıl model, WLTP-benzeri sürüş çevrimi, güç haritası
  karsilastirma.py   Li-iyon ile karşılaştırma tablosu
  rapor.py, cli.py   rapor + grafik üretimi, komut satırı
docs/              tasarım dokümanları (Türkçe)
  00_ekip_ve_yontem.md            ekip rolleri, yöntem, karar günlüğü
  01_tasarim_ozeti.md             yönetici özeti
  02_kimya_ve_termodinamik.md     neden bor, aday kimyalar, kloso-borat mekanizması, kaynaklar
  03_malzeme_ve_uretim.md         sentez rotaları, reçeteler, proses akışı, maliyet
  04_hucre_ve_paket_tasarimi.md   hücre/paket/araç sayıları, ısıl strateji, BMS
  05_guvenlik_cevre_saglik.md     güvenlik, toksikoloji, yaşam döngüsü
  06_riskler_trl_yol_haritasi.md  TRL, risk kaydı, hakem bulguları, doğrulama planı, KPI
cikti/             otomatik üretilen rapor (RAPOR.md) ve grafikler
tests/             birim testleri
```

## Kurulum ve kullanım

```bash
pip install -r requirements.txt
python -m borpil.cli termo                 # teorik sınırlar (bor-hava, DBFC, metal-hava kıyas)
python -m borpil.cli hucre A               # hücre yığın modeli (A, A0, A-Fe, B, C, S)
python -m borpil.cli hucre A --ayirici 20 --alan-kapasitesi 4 --sicaklik 60
python -m borpil.cli paket A --kwh 75 --volt 400
python -m borpil.cli surus A --ortam -10 --isitici 25
python -m borpil.cli rapor                 # cikti/RAPOR.md + grafikler
python -m pytest -q
```

Tüm sayısal iddialar koddan üretilir; varsayımlar (özellikle maliyetler) veri sınıflarında
açıkça işaretlenmiştir (`maliyet_varsayim`). Sınırlar ve riskler `docs/01` ve `docs/06`'da
açıkça yazılıdır: hızlı şarj (~1C), hidroborat oksidasyon penceresi, soğuk performans,
kloso-borat maliyeti.
