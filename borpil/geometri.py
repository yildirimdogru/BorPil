"""
Geometri: (1) [B12H12]2- anyonunun ikosahedral yapısı ve etkin boyutu — iletkenlik
mekanizmasının (büyük, küresel, dönen anyon kafesi) geometrik temeli; (2) kafes ve boşluk
tahmini; (3) hücre/modül/paket paketleme geometrisi.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np

from .sabitler import AVOGADRO

# Bağ uzunlukları (Å) — nötron/X-ışını kırınımı ortalamaları
B_B_BAG = 1.78
B_H_BAG = 1.20
H_VDW = 1.10  # hidrojenin van der Waals yarıçapı
NA_IYON_YARICAP = 1.02  # Shannon, KS=6


def ikosahedron_koseleri(kenar: float = B_B_BAG) -> np.ndarray:
    """Kenar uzunluğu `kenar` olan düzgün ikosahedronun 12 köşesi (merkez orijinde)."""
    phi = (1 + 5**0.5) / 2
    ham = []
    for (a, b) in product((-1, 1), repeat=2):
        ham += [(0, a, b * phi), (a, b * phi, 0), (b * phi, 0, a)]
    ham = np.array(ham, dtype=float)
    # (0, ±1, ±φ) tipi köşelerde kenar uzunluğu 2 → ölçekle
    return ham * (kenar / 2.0)


@dataclass(frozen=True)
class AnyonGeometrisi:
    kose_sayisi: int
    kenar_A: float
    cevrel_yaricap_B_A: float     # B atomları küresinin yarıçapı
    cevrel_yaricap_H_A: float     # H atomları küresinin yarıçapı
    etkin_yaricap_A: float        # H vdW yarıçapı dâhil "sert küre" yarıçapı
    etkin_hacim_A3: float

    def __str__(self) -> str:
        return (f"[B12H12]2-: kenar {self.kenar_A:.2f} Å, R_B {self.cevrel_yaricap_B_A:.2f} Å, "
                f"R_H {self.cevrel_yaricap_H_A:.2f} Å, etkin yarıçap {self.etkin_yaricap_A:.2f} Å, "
                f"etkin hacim {self.etkin_hacim_A3:.0f} Å³")


def b12h12_geometrisi() -> AnyonGeometrisi:
    v = ikosahedron_koseleri()
    R_B = float(np.linalg.norm(v, axis=1).mean())
    # Düzgün ikosahedron çevrel yarıçapı: a·sin(2π/5) — sayısal sonuçla doğrulama için
    assert abs(R_B - B_B_BAG * np.sin(2 * np.pi / 5)) < 1e-9
    R_H = R_B + B_H_BAG
    R_etkin = R_H + H_VDW
    return AnyonGeometrisi(
        kose_sayisi=len(v),
        kenar_A=B_B_BAG,
        cevrel_yaricap_B_A=R_B,
        cevrel_yaricap_H_A=R_H,
        etkin_yaricap_A=R_etkin,
        etkin_hacim_A3=4 / 3 * np.pi * R_etkin**3,
    )


def bcc_kafes_parametresi_A(yogunluk_g_cm3: float, molar_kutle: float, formul_birimi_hucre: int = 2) -> float:
    """Yoğunluk ve molar kütleden kübik hücre kenarı (Å). Yüksek-T Na2B12H12 fazı bcc (Im-3m), Z=2."""
    hacim_formul_A3 = molar_kutle / (yogunluk_g_cm3 * AVOGADRO) * 1e24
    return (hacim_formul_A3 * formul_birimi_hucre) ** (1 / 3)


A_BCC_NA2B12H12_A = 7.9  # Å, süperiyonik bcc fazın ölçülen kafes parametresi (Udovic/Verdal 2014)


def na_bosluk_analizi(yogunluk_g_cm3: float | None = None, molar_kutle: float | None = None,
                      a_bcc_A: float | None = A_BCC_NA2B12H12_A) -> dict[str, float]:
    """
    Yüksek-T (süperiyonik) Na2B12H12 fazı: anyonlar bcc kafeste (Im-3m, Z=2), Na+ iyonları
    12d tetrahedral-benzeri sitelerde. Hücrede 4 Na+ için 12 site → 2/3 boşluk (vakans);
    bu yüksek boş-site oranı + anyonların hızlı yeniden yönelimi düşük göç engelinin
    (Ea ~0.2-0.4 eV) yapısal kaynağıdır.

    Kafes parametresi varsayılan olarak ölçülen yüksek-T değeridir (7.9 Å; geçişte ~%15 hacim
    genleşmesi olduğu için oda sıcaklığı yoğunluğundan türetilmez). a_bcc_A=None verilirse
    yoğunluk ve molar kütleden hesaplanır.

    Anyon "sert küre" yarıçapı, birbirine değen anyonlar varsayımıyla kafesten türetilir
    (R = a√3/4). vdW dâhil geometrik yarıçap (b12h12_geometrisi) ayrıca raporlanır; ikisi
    arasındaki fark H...H temaslarının iç içe geçmesini (yumuşak anyon) gösterir.
    """
    if a_bcc_A is None:
        if yogunluk_g_cm3 is None or molar_kutle is None:
            raise ValueError("a_bcc_A verilmezse yoğunluk ve molar kütle gerekir")
        a = bcc_kafes_parametresi_A(yogunluk_g_cm3, molar_kutle)
    else:
        a = a_bcc_A
    R_sert = a * 3**0.5 / 4                       # bcc'de en yakın komşu a√3/2 → yarıçap a√3/4
    R_vdw = b12h12_geometrisi().etkin_yaricap_A
    d_tet = a * 5**0.5 / 4                        # (1/2,1/4,0) tipi tetrahedral site → anyona uzaklık
    d_okt = a / 2                                 # (1/2,0,0) tipi oktahedral site (bcc'de basık)
    na_site_sayisi = 12                           # 12d
    na_sayisi = 4                                 # Z=2 × 2 Na
    return {
        "kafes_a_A": a,
        "anyon_anyon_A": 2 * R_sert,
        "anyon_sert_kure_yaricap_A": R_sert,
        "anyon_vdw_yaricap_A": R_vdw,
        "tetrahedral_bosluk_yaricap_A": d_tet - R_sert,
        "oktahedral_bosluk_yaricap_A": d_okt - R_sert,
        "Na_yaricap_A": NA_IYON_YARICAP,
        "na_site_doluluk": na_sayisi / na_site_sayisi,
        "anyon_hacim_kesri_sert": 2 * (4 / 3 * np.pi * R_sert**3) / a**3,
    }


# ---------------------------------------------------------------------------
# Paketleme geometrisi
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PouchGeometrisi:
    en_mm: float
    boy_mm: float
    kalinlik_mm: float
    katman_sayisi: int

    @property
    def hacim_L(self) -> float:
        return self.en_mm * self.boy_mm * self.kalinlik_mm * 1e-6


def pouch_boyutlandir(kapasite_Ah: float, alan_kapasitesi_mAh_cm2_cift: float, tekrar_kalinlik_um: float,
                      en_mm: float = 100.0, boy_mm: float = 300.0, kilif_um: float = 300.0) -> PouchGeometrisi:
    """
    Hedef Ah için gereken çift taraflı tekrar biriminin sayısını ve pouch kalınlığını verir.
    alan_kapasitesi_mAh_cm2_cift: bir tekrar biriminin (iki katot yüzü) alan kapasitesi.
    """
    alan_cm2 = en_mm * boy_mm / 100.0
    kapasite_birim_Ah = alan_cm2 * alan_kapasitesi_mAh_cm2_cift / 1000.0
    n = int(np.ceil(kapasite_Ah / kapasite_birim_Ah))
    kalinlik_mm = (n * tekrar_kalinlik_um + 2 * kilif_um) / 1000.0
    return PouchGeometrisi(en_mm, boy_mm, kalinlik_mm, n)


def kutu_icine_paketle(hucre: PouchGeometrisi, kutu_mm: tuple[float, float, float],
                       doluluk: float = 0.80) -> int:
    """
    Basit dikdörtgen paketleme: hücreler kalınlık ekseninde yığılır; hücre başına bir ara
    plaka/köpük payı için doluluk katsayısı uygulanır. Sonuç: kutuya sığan hücre sayısı.
    """
    L, W, H = kutu_mm
    en_boyunca = int(L // hucre.boy_mm)
    yan_boyunca = int(W // hucre.en_mm)
    kalinlik_boyunca = int(H * doluluk // hucre.kalinlik_mm)
    return en_boyunca * yan_boyunca * kalinlik_boyunca
