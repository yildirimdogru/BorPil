# 08 — Paket maden ve element bütçesi

Bu belge, tasarlanan **74 kWh BorPil** paketinde tipik olarak bulunan maden / malzeme /
element oranlarını kayıt altına alır. Sayılar `borpil` yığın modelinden üretilir
(`python -m borpil.cli paket A-alt` ve `hucre.py` tekrar birimi); kılıf, tab ve paket
donanımı (çerçeve, yay, yalıtım, BMS, ısıtıcı) element tablosuna **dahil değildir**
aksi belirtilmedikçe.

Kaynak: hücre reçetesi `KompozitRecete` (%71 NVP / %25 SE / %2 C+CNT / %2 NBR),
elektrolit `Na₂(B₁₂H₁₂)₀.₅(B₁₀H₁₀)₀.₅`, anot Na metal fazlası, her iki tarafta Al folyo.
Karşılaştırma: `docs/01`, `docs/03 §3.6`, `cikti/RAPOR.md`.

## 8.1 Ürün satırı

| SKU (ürün formu) | Tasarım | 74 kWh paket | Hücre |
|---|---|---|---|
| **BorPil EV-74 Standard** | BorPil-A-alt (60 µm SE, 50 µm Na, 30 Ω·cm²) | **596 kg / 512 L**, 125 Wh/kg | 177 Wh/kg, 279 Wh/L |
| BorPil EV-74 Pro | BorPil-A (30 µm / 20 µm / 15 Ω·cm²) | 519 kg / 418 L, 143 Wh/kg | 203 Wh/kg, 341 Wh/L |
| BorPil EV-74 Fe | BorPil-A-Fe (Na-Fe-Mn oksit katot) | ~592 kg | 178 Wh/kg; V = 0 |

Aşağıdaki ayrıntılı bütçe **Standard (A-alt)** içindir; Pro ve Fe özet satırları §8.4’tedir.

## 8.2 Element bütçesi (yığın, 74,2 kWh)

Yığın tekrarı (A-alt): 111,0 mg/cm², 650 µm, 6,0 mAh/cm², 3,37 V.
Hücreler paketin ~%71’i (~420 kg); kalan ~176 kg çerçeve, yay, yalıtım, BMS, ısıtıcı
(+12 kg basınç fikstürü).

| Element | kg / paket | kg/kWh | Yığın kütlesinin ~ | Paket kütlesinin ~ | Not |
|---|---:|---:|---:|---:|---|
| **Sodyum (Na)** | **102** | 1,37 | %25 | %17 | katot + SE + Na fazlası |
| **Bor (B)** | **92** | 1,24 | %23 | %16 | yalnız kloso-borat; hücre kütlesinin ~%20–25’i B |
| **Oksijen (O)** | 84 | 1,14 | %21 | %14 | NVP fosfat kafesi (cevher oksijeni) |
| **Vanadyum (V)** | **45** | 0,60 | %11 | %7,5 | NVP; katot yüklemesine bağlı, SE incelince değişmez |
| **Fosfor (P)** | 41 | 0,55 | %10 | %7 | NVP |
| **Alüminyum (Al)** | 24 | 0,32 | %6 | %4 | yalnız akım toplayıcı folyo; kılıf/çerçeve hariç |
| **Karbon (C)** | 11 | 0,14 | %3 | %2 | iletken karbon + bağlayıcı |
| **Hidrojen (H)** | 9 | 0,13 | %2 | %2 | kloso-borat kafesi + bağlayıcı |
| **Lityum (Li)** | **0** | 0 | 0 | 0 | — |
| **Kobalt / nikel / bakır** | **0** | 0 | 0 | 0 | Na, Al ile alaşım yapmaz → Cu folyo yok |

Hücre kütlesinin kabaca **%20–25’i bordur**; pakette bu oran donanım yüzünden **~%14–16**’ya iner.

## 8.3 Bileşik / “maden” olarak ne girer?

**Baz çizgisi (A-alt), 74,2 kWh:**

| Malzeme | ~kg / paket | Yığındaki pay | Formüldeki kütle kesirleri | Cevher / kaynak |
|---|---:|---:|---|---|
| **NVP** — Na₃V₂(PO₄)₃ | ~200 | ~%49 | O %42, V %22, P %20, Na %15 | V₂O₅ (cüruf/yan ürün olabilir) + fosfat + soda |
| **Kloso-borat SE** | ~137 | ~%34 | **B %68**, Na %26, H %6 | tinkal / kolemanit → boraks / H₃BO₃ → NaBH₄ → hidroborat |
| **Na metal** (yalnız fazlalık) | ~36 | ~%9 | Na %100 | tuz (Downs hücresi). Döngüsel Na NVP formülünde sayılır |
| **Al folyo** | ~24 | ~%6 | Al %100 | boksit; her iki elektrot |
| Karbon + bağlayıcı (NBR) | ~11 | ~%3 | C, H | — |

Katot kompozit reçetesi (kütle): **%71 NVP / %25 SE / %2 C+CNT / %2 NBR**; gözenek ≤ %8.
Ayırıcı: eş-molar Na₂B₁₂H₁₂ + Na₂B₁₀H₁₀ karışımı (saf Na₂B₁₂H₁₂ kütlece %69 B).

Cevher dilinde paket **bor cevheri + tuz + vanadyum + fosfat + alüminyum** taşır;
**lityum, kobalt, nikel, bakır yoktur**.

## 8.4 Hedef (Pro) ve vanadyumsuz (Fe) satırlar

| | Standard (A-alt) | Pro (A) | Fe (A-Fe) |
|---|---:|---:|---:|
| Bor | 92 kg (1,24 kg/kWh) | **70 kg** (0,94) | 81 kg (1,09) |
| Sodyum | 102 kg (1,37) | **72 kg** (0,97) | 82 kg (1,11) |
| Vanadyum | 45 kg (0,60) | 45 kg | **0** |
| Demir / manganez | 0 | 0 | ~61 / 60 kg |
| Kloso-borat SE | ~137 kg | ~104 kg | ~ benzer Pro |
| NVP / aktif katot | ~200 kg NVP | ~200 kg NVP | ~185 kg Na-Fe-Mn oksit |
| Na fazlası | ~36 kg | ~14 kg | ~14 kg (hedef kalınlık) |
| Al folyo | ~24 kg | ~24 kg | ~29 kg (Wh başına biraz daha fazla) |

Pro’da elektrolit ve Na fazlası inceldiği için B ve Na düşer; vanadyum katot yüklemesine
bağlıdır, değişmez. Fe satırı V riskini sıfırlar, yerine yaygın Fe/Mn oksitleri koyar.

`docs/03` tablo 3.6 (hedef A, 75 kWh yuvarlak): SE ~107 kg, NVP ~205 kg, Na fazlası ~14 kg,
Al ~23 kg, karbon/bağlayıcı ~14 kg — modelle uyumlu (Pro satırı).

## 8.5 Tedarik ve ölçek notu

- 1 GWh/yıl hücre ≈ **~1400 t/yıl kloso-borat**, **~960 t/yıl bor içeriği**.
- Türkiye bor ürünü (B₂O₃ bazında Mt mertebesi) yanında cevher kısıtı yoktur; kısıt
  **hidroborat sentez kapasitesi**dir (`docs/03 §3.1`, `docs/06`).
- Vanadyum **45 kg/araç** → A-Fe yolu paralel nitelendirme hattıdır.
- Geri dönüşüm: kloso-borat suda kararlı, **doğrudan kristalizasyonla** geri kazanılır;
  NVP/Al yoğunluk ayrımı, V asit liçi (`docs/05 §5.3`).

## 8.6 Model sınırı

Element kg/kWh yığın (elektrot + SE + folyo) içindir. Pouch Al-laminat kılıf, ultrasonik
tab, çelik/kompozit çerçeve, disk yay, aerojel, sıvı soğutma plakası ve bakır busbar
**ayrı kütle kalemleridir** (~176 kg Standard pakette). Busbar bakırı hücre kimyasında
yoktur; paket elektrik donanımındadır.
