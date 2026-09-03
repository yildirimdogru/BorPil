"""
Malzeme veri tabanı.

Sayısal değerler açık literatürden derlenmiş yaklaşık mühendislik değerleridir (kaynak
notları docs/02_kimya_ve_termodinamik.md içindedir). Maliyetler ölçekli üretim
varsayımıdır ve `maliyet_varsayim` alanında açıkça işaretlenmiştir.

Birimler: yoğunluk g/cm³, kapasite mAh/g, potansiyel V (Na+/Na veya belirtilen
referansa karşı), iletkenlik S/cm, aktivasyon enerjisi eV, maliyet USD/kg.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .sabitler import kutle_kesri, molar_kutle, teorik_kapasite_mah_g


@dataclass(frozen=True, eq=False)
class Malzeme:
    ad: str
    formul: dict[str, float]
    yogunluk: float                   # g/cm³
    maliyet_usd_kg: float             # USD/kg (ölçekli üretim varsayımı)
    maliyet_varsayim: str = ""        # maliyetin dayanağı / belirsizlik notu
    notlar: str = ""

    @property
    def molar_kutle(self) -> float:
        return molar_kutle(self.formul)

    def bor_kesri(self) -> float:
        return kutle_kesri(self.formul, "B")

    def lityum_kesri(self) -> float:
        return kutle_kesri(self.formul, "Li")


@dataclass(frozen=True, eq=False)
class Elektrot(Malzeme):
    kapasite_teorik: float = 0.0      # mAh/g (aktif madde)
    kapasite_pratik: float = 0.0      # mAh/g (ilk döngülerde ulaşılabilir)
    potansiyel_ort: float = 0.0       # V, ortalama çalışma potansiyeli (Na+/Na'ya karşı)
    rol: str = "katot"                # "katot" | "anot"
    metalik: bool = False             # True: kaplanan/soyulan metal anot (kompozit değil)


@dataclass(frozen=True, eq=False)
class KatiElektrolit(Malzeme):
    """
    Kloso-borat katı elektrolit. İletkenlik iki fazlı Arrhenius modeliyle tanımlanır:
    düzenli (düşük sıcaklık) faz ve düzensiz/süperiyonik (yüksek sıcaklık) faz.
    Faz geçişi olmayan (oda sıcaklığında zaten düzensiz) tuzlarda T_gecis = None.
    """
    sigma_ref: float = 0.0            # S/cm, T_ref'te ölçülmüş iletkenlik
    T_ref: float = 298.15             # K
    Ea: float = 0.4                   # eV, T_ref'in bulunduğu fazın aktivasyon enerjisi
    T_gecis: float | None = None      # K, düzen-düzensizlik geçiş sıcaklığı
    sigma_gecis_ust: float | None = None  # S/cm, geçişin hemen üstündeki iletkenlik
    Ea_ust: float | None = None       # eV, süperiyonik fazın aktivasyon enerjisi
    oksidasyon_siniri_V: float = 3.0  # V vs Na+/Na, termodinamik anodik sınır (yaklaşık)
    oksidasyon_pasif_V: float = 4.0   # V, pasifleştirici arayüzle kinetik olarak ulaşılan sınır
    na_sayisi: float = 2.0            # formül birimi başına taşınan Na+
    kaynak: str = ""


@dataclass(frozen=True, eq=False)
class Folyo(Malzeme):
    kalinlik_um: float = 12.0


# ---------------------------------------------------------------------------
# Katı elektrolitler (kloso-boratlar ve karba-kloso-boratlar)
# ---------------------------------------------------------------------------

NA2B12H12 = KatiElektrolit(
    ad="Na2B12H12 (dodekahidro-kloso-dodekaborat)",
    formul={"Na": 2, "B": 12, "H": 12},
    yogunluk=1.46,
    maliyet_usd_kg=45.0,
    maliyet_varsayim="NaBH4 + B2H6 ölçekli rota; bugünkü laboratuvar fiyatının ~1/50'i",
    sigma_ref=1e-5, T_ref=500.0, Ea=0.8,
    T_gecis=529.0, sigma_gecis_ust=0.1, Ea_ust=0.2,
    oksidasyon_siniri_V=3.0, oksidasyon_pasif_V=4.0,
    kaynak="Udovic ve ark., Chem. Commun. 2014; Verdal ve ark. 2014",
    notlar="Saf hâlde oda sıcaklığında yalıtkan (~1e-11 S/cm); 529 K'de ~10^3 kat sıçrayarak süperiyonik bcc faza geçer (a ≈ 7.9 Å). Anyon karışımıyla geçiş oda sıcaklığına çekilir.",
)

NA2B10H10 = KatiElektrolit(
    ad="Na2B10H10 (dekahidro-kloso-dekaborat)",
    formul={"Na": 2, "B": 10, "H": 10},
    yogunluk=1.45,
    maliyet_usd_kg=55.0,
    maliyet_varsayim="dekaboran rotası; Na2B12H12'den biraz pahalı",
    sigma_ref=1e-6, T_ref=298.15, Ea=0.7,
    T_gecis=360.0, sigma_gecis_ust=0.01, Ea_ust=0.2,
    oksidasyon_siniri_V=2.9, oksidasyon_pasif_V=3.8,
    kaynak="Udovic ve ark., Adv. Mater. 2014",
)

# Temel tasarım elektroliti: eş-molar B12/B10 karışımı, oda sıcaklığında düzensiz faz
NA2_B12_B10 = KatiElektrolit(
    ad="Na2(B12H12)0.5(B10H10)0.5 (eş-molar kloso-borat karışımı)",
    formul={"Na": 2, "B": 11, "H": 11},
    yogunluk=1.50,
    maliyet_usd_kg=50.0,
    maliyet_varsayim="iki tuzun ağırlıklı ortalaması + bilyalı öğütme",
    sigma_ref=9e-4, T_ref=293.15, Ea=0.40,
    T_gecis=None,
    oksidasyon_siniri_V=3.0, oksidasyon_pasif_V=4.0,
    kaynak="Duchêne ve ark., Chem. Commun. 2017 (elektrolit) ve Energy Environ. Sci. 2017 (3 V tam hücre); Asakura ve ark., EES 2020 (4 V pasifleşme)",
    notlar="Oda sıcaklığında ~1 mS/cm; 60 °C'de ~5 mS/cm. Na metaline karşı kararlı, soğuk preslenebilir.",
)

NACB11H12 = KatiElektrolit(
    ad="NaCB11H12 (karba-kloso-dodekaborat)",
    formul={"Na": 1, "C": 1, "B": 11, "H": 12},
    yogunluk=1.30,
    maliyet_usd_kg=400.0,
    maliyet_varsayim="karboran sentezi pahalı; niş ölçek",
    sigma_ref=1e-5, T_ref=298.15, Ea=0.6,
    T_gecis=380.0, sigma_gecis_ust=0.12, Ea_ust=0.15,
    oksidasyon_siniri_V=3.5, oksidasyon_pasif_V=4.2,
    na_sayisi=1.0,
    kaynak="Tang ve ark., Energy Environ. Sci. 2015",
)

NA2_CB9_CB11 = KatiElektrolit(
    ad="Na2(CB9H10)(CB11H12) (karışık karba-kloso-borat)",
    formul={"Na": 2, "C": 2, "B": 20, "H": 22},
    yogunluk=1.25,
    maliyet_usd_kg=450.0,
    maliyet_varsayim="karboran sentezi; yalnız premium hücreler için",
    sigma_ref=0.07, T_ref=298.15, Ea=0.25,
    T_gecis=None,
    oksidasyon_siniri_V=3.3, oksidasyon_pasif_V=4.2,
    kaynak="Tang ve ark., ACS Energy Lett. 2016 (karışık anyon katı çözeltisi, ~70 mS/cm @ oda sıcaklığı); NaCB9H10 için Tang ve ark., Adv. Energy Mater. 2016",
    notlar="Bilinen en iletken Na katı elektrolitlerinden biri; maliyet kısıtı nedeniyle 2. nesil. 25 °C üstü değerler Arrhenius ekstrapolasyonudur (ölçüm değil).",
)

KATI_ELEKTROLITLER = {
    "Na2B12H12": NA2B12H12,
    "Na2B10H10": NA2B10H10,
    "Na2(B12H12)(B10H10)": NA2_B12_B10,
    "NaCB11H12": NACB11H12,
    "Na2(CB9H10)(CB11H12)": NA2_CB9_CB11,
}

# ---------------------------------------------------------------------------
# Katotlar (Na+/Na'ya karşı)
# ---------------------------------------------------------------------------

_nvp_formul = {"Na": 3, "V": 2, "P": 3, "O": 12}
NVP = Elektrot(
    ad="Na3V2(PO4)3 (NASICON, NVP)",
    formul=_nvp_formul,
    yogunluk=3.17,
    maliyet_usd_kg=22.0,
    maliyet_varsayim="V2O5 ~12 USD/kg × 0.40 kg/kg + sol-jel/karbon kaplama; aralık 18-30",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_nvp_formul), 2),  # ≈117.6
    kapasite_pratik=110.0,
    potansiyel_ort=3.37,
    notlar="Düz plato (V3+/V4+), yapısal olarak çok kararlı, düşük hacim değişimi (%8).",
)

_nacro2_formul = {"Na": 1, "Cr": 1, "O": 2}
NACRO2 = Elektrot(
    ad="NaCrO2 (O3 tabakalı oksit)",
    formul=_nacro2_formul,
    yogunluk=4.36,
    maliyet_usd_kg=9.0,
    maliyet_varsayim="Cr2O3 + Na2CO3 katı hâl sentezi",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_nacro2_formul), 1),  # ≈250
    kapasite_pratik=115.0,   # 0.5 Na ile tersinir
    potansiyel_ort=2.95,
    notlar="Kloso-borat penceresi içinde; Duchêne 2017 tam hücre gösterimi. Cr(VI) riski üretimde yönetilir.",
)

_nvpf_formul = {"Na": 3, "V": 2, "P": 2, "O": 8, "F": 3}
NVPF = Elektrot(
    ad="Na3V2(PO4)2F3 (NVPF)",
    formul=_nvpf_formul,
    yogunluk=3.15,
    maliyet_usd_kg=18.0,
    maliyet_varsayim="NVP + florür kaynağı",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_nvpf_formul), 2),  # ≈128
    kapasite_pratik=120.0,
    potansiyel_ort=3.90,
    notlar="4 V sınıfı; yalnızca pasifleştirici arayüzle (Asakura 2020) kloso-boratla uyumlu. 2. nesil.",
)

_s_formul = {"S": 1}
KUKURT = Elektrot(
    ad="S (Na-S, Na2S'e kadar)",
    formul=_s_formul,
    yogunluk=2.07,
    maliyet_usd_kg=0.5,
    maliyet_varsayim="petrokimya yan ürünü",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_s_formul), 2),  # ≈1672
    kapasite_pratik=800.0,
    potansiyel_ort=1.80,
    notlar="Uzun vade; hacim değişimi ve polisülfür kinetiği katı hâlde zor.",
)

_nfm_formul = {"Na": 0.667, "Fe": 0.5, "Mn": 0.5, "O": 2}
NA_FE_MN = Elektrot(
    ad="P2-Na2/3Fe1/2Mn1/2O2 (tabakalı Fe/Mn oksit)",
    formul=_nfm_formul,
    yogunluk=4.10,
    maliyet_usd_kg=6.0,
    maliyet_varsayim="Fe2O3 + Mn2O3 + Na2CO3 katı hâl sentezi; kritik metal yok",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_nfm_formul), 0.667),  # ≈175 (0.67 Na)
    kapasite_pratik=120.0,   # 4.0 V tavanı ile (P2→O2/'Z' geçişi önlenerek); 1.5-4.3 V'ta 190
    potansiyel_ort=2.75,
    notlar="Vanadyumsuz, en düşük maliyetli katot; nem hassasiyeti ve faz geçişi kaynaklı sönüm yönetilmeli.",
)

_pw_formul = {"Na": 2, "Fe": 2, "C": 6, "N": 6}
PRUSYA_BEYAZI = Elektrot(
    ad="Na2Fe[Fe(CN)6] (Prusya beyazı)",
    formul=_pw_formul,
    yogunluk=1.90,
    maliyet_usd_kg=5.0,
    maliyet_varsayim="sulu çöktürme; FeSO4 + Na4Fe(CN)6",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_pw_formul), 2),  # ≈171
    kapasite_pratik=150.0,
    potansiyel_ort=3.10,
    notlar="Ucuz, Fe bazlı; düşük yoğunluk → Wh/L zayıf, kristal suyu kontrolü şart.",
)

KATOTLAR = {"NVP": NVP, "NaCrO2": NACRO2, "NVPF": NVPF, "S": KUKURT,
            "NaFeMnO2": NA_FE_MN, "PrusyaBeyazi": PRUSYA_BEYAZI}

# ---------------------------------------------------------------------------
# Anotlar
# ---------------------------------------------------------------------------

_na_formul = {"Na": 1}
NA_METAL = Elektrot(
    ad="Na metal",
    formul=_na_formul,
    yogunluk=0.97,
    maliyet_usd_kg=3.0,
    maliyet_varsayim="Downs hücresi, ticari",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_na_formul), 1),  # ≈1166
    kapasite_pratik=teorik_kapasite_mah_g(molar_kutle(_na_formul), 1),
    potansiyel_ort=0.0,
    rol="anot",
    metalik=True,
    notlar="Kloso-boratlar Na metaline karşı termodinamik olarak kararlı; yumuşak metal → iyi katı-katı temas. Erime noktası 97.8 °C.",
)

SERT_KARBON = Elektrot(
    ad="Sert karbon (hard carbon)",
    formul={"C": 1},
    yogunluk=1.55,
    maliyet_usd_kg=8.0,
    maliyet_varsayim="biyokütle/asfalt öncülü",
    kapasite_teorik=300.0,   # ampirik üst değer (kristalografik teorik kapasite tanımlı değil)
    kapasite_pratik=280.0,
    potansiyel_ort=0.20,
    rol="anot",
    notlar="Muhafazakâr alternatif: Na dendriti riski yok, enerji yoğunluğu düşer. İlk çevrim tersinmez kaybı (%10-20) np_orani ile karşılanır.",
)

_mg_formul = {"Mg": 1}
MG_METAL = Elektrot(
    ad="Mg metal",
    formul=_mg_formul,
    yogunluk=1.74,
    maliyet_usd_kg=4.0,
    maliyet_varsayim="ticari",
    kapasite_teorik=teorik_kapasite_mah_g(molar_kutle(_mg_formul), 2),  # ≈2205
    kapasite_pratik=2000.0,
    potansiyel_ort=0.34,  # Mg2+/Mg, Na+/Na'ya karşı (yalnız Mg-elektrolitli ayrı bir hücrede anlamlı)
    rol="anot",
    metalik=True,
    notlar="Na kloso-borat SE ile uyumsuz; yalnız Mg(CB11H12)2 tipi Mg elektrolitli izleme yolu için veri.",
)

ANOTLAR = {"Na": NA_METAL, "sert_karbon": SERT_KARBON, "Mg": MG_METAL}

# ---------------------------------------------------------------------------
# Yardımcı malzemeler
# ---------------------------------------------------------------------------

AL_FOLYO = Folyo(ad="Al folyo", formul={"Al": 1}, yogunluk=2.70, maliyet_usd_kg=5.0,
                 maliyet_varsayim="ticari batarya folyosu", kalinlik_um=12.0,
                 notlar="Na ile alaşım yapmaz → her iki elektrotta Al kullanılabilir (Cu'ya gerek yok).")
CU_FOLYO = Folyo(ad="Cu folyo", formul={"Cu": 1}, yogunluk=8.96, maliyet_usd_kg=12.0,
                 maliyet_varsayim="ticari", kalinlik_um=8.0)
KARBON_ILETKEN = Malzeme(ad="İletken karbon (CNT/CB)", formul={"C": 1}, yogunluk=2.0,
                         maliyet_usd_kg=15.0, maliyet_varsayim="karbon siyahı + az CNT")
BAGLAYICI = Malzeme(ad="Bağlayıcı (NBR/PIB)", formul={"C": 4, "H": 8}, yogunluk=0.92,
                    maliyet_usd_kg=10.0, maliyet_varsayim="ticari elastomer")

# ---------------------------------------------------------------------------
# Li-iyon referans hücreleri (paket düzeyinde karşılaştırma için)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReferansHucre:
    ad: str
    wh_kg: float
    wh_L: float
    usd_kwh: float
    li_kg_per_kwh: float
    co_kg_per_kwh: float
    ni_kg_per_kwh: float
    yanici_elektrolit: bool
    cevrim_omru: int
    notlar: str = ""


NMC811 = ReferansHucre("Li-iyon NMC811 (pouch, 2025 sınıfı)", 265, 700, 100, 0.11, 0.09, 0.75,
                       True, 1500, "Yüksek enerji, termal kaçak riski, Co/Ni bağımlılığı")
LFP = ReferansHucre("Li-iyon LFP (prizmatik, 2025 sınıfı)", 170, 380, 75, 0.09, 0.0, 0.0,
                    True, 3500, "Düşük maliyet, uzun ömür, soğukta zayıf")

REFERANSLAR = {"NMC811": NMC811, "LFP": LFP}
