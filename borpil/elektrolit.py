"""
Kloso-borat katı elektrolitlerin iyon taşınımı.

Model: σ(T) = σ_ref · exp[-(Ea/k)(1/T - 1/T_ref)]  (Arrhenius; σT ~ ön çarpanı ihmal edilmiştir,
50 K'lik pencerelerde hata < %15). Düzen-düzensizlik geçişi olan tuzlarda geçişin üstünde
ikinci bir Arrhenius kolu kullanılır.

Fiziksel arka plan: [B12H12]2-/[B10H10]2- anyonları yüksek sıcaklıkta (veya karışımla
frustrasyona uğratılmış kafeste oda sıcaklığında) hızlı yeniden yönelim yapar; büyük,
yumuşak, tek yüklü/çift yüklü anyonların oluşturduğu geniş boşluklu kafes Na+ için düşük
enerjili göç yolları açar ("paddle-wheel" mekanizması). Bu yüzden Ea ~0.2-0.4 eV gibi düşüktür.
"""

from __future__ import annotations

import numpy as np

from .malzemeler import KatiElektrolit
from .sabitler import C_TO_K, K_BOLTZMANN_EV


def arrhenius(sigma_ref: float, Ea_eV: float, T: np.ndarray | float, T_ref: float) -> np.ndarray | float:
    return sigma_ref * np.exp(-(Ea_eV / K_BOLTZMANN_EV) * (1.0 / np.asarray(T, dtype=float) - 1.0 / T_ref))


def iletkenlik(se: KatiElektrolit, T_K: np.ndarray | float) -> np.ndarray | float:
    """İyonik iletkenlik (S/cm) — faz geçişi varsa iki kollu model."""
    T = np.asarray(T_K, dtype=float)
    dusuk = arrhenius(se.sigma_ref, se.Ea, T, se.T_ref)
    if se.T_gecis is None or se.sigma_gecis_ust is None:
        return dusuk
    Ea_ust = se.Ea_ust if se.Ea_ust is not None else se.Ea
    yuksek = arrhenius(se.sigma_gecis_ust, Ea_ust, T, se.T_gecis)
    return np.where(T >= se.T_gecis, yuksek, dusuk)


def iletkenlik_C(se: KatiElektrolit, T_C: np.ndarray | float) -> np.ndarray | float:
    return iletkenlik(se, np.asarray(T_C, dtype=float) + C_TO_K)


def alan_direnci_ohm_cm2(se: KatiElektrolit, kalinlik_um: float, T_C: float) -> float:
    """Ayırıcı katmanın alan-özgül direnci: ASR = L / σ  (Ω·cm²)."""
    L_cm = kalinlik_um * 1e-4
    return L_cm / float(iletkenlik_C(se, T_C))


def bruggeman_etkin_iletkenlik(sigma: float, hacim_kesri: float, alfa: float = 1.5) -> float:
    """Kompozit katot içindeki elektrolit fazının etkin iletkenliği: σ_eff = σ·ε^α."""
    return sigma * hacim_kesri**alfa


def hedef_kalinlik_um(se: KatiElektrolit, T_C: float, hedef_asr_ohm_cm2: float = 10.0,
                      min_mekanik_um: float = 20.0) -> float:
    """
    Verilen ASR hedefi için gereken ayırıcı kalınlığı; mekanik/dendrit alt sınırıyla kırpılır.
    (Katı hâl hücrelerde ~10 Ω·cm² ASR, 3 mA/cm²'de ~30 mV kayıp demektir.)
    """
    L_cm = hedef_asr_ohm_cm2 * float(iletkenlik_C(se, T_C))
    return max(L_cm * 1e4, min_mekanik_um)


# Na | kloso-borat arayüzi için 25 °C'de kaplama yönünde kritik akım yoğunluğu (mA/cm²).
# Literatür (basınç altında, oda sıcaklığı): 0.5-2 mA/cm²; merkezî tasarım değeri 1.5.
J_KRITIK_25C_MA_CM2 = 1.5
EA_ARAYUZ_EV = 0.45


def kritik_akim_yogunlugu_mA_cm2(T_C: float, J_ref: float = J_KRITIK_25C_MA_CM2, T_ref_C: float = 25.0,
                                 Ea_eV: float = EA_ARAYUZ_EV) -> float:
    """
    Na-metal/kloso-borat arayüzünde dendritsiz çalışabilen kritik akım yoğunluğu için
    ampirik Arrhenius ölçekleme (T_ref'te J_ref). Sıcaklık artınca Na sürünmesi (creep) ve
    iyonik iletkenlik artar, boşluk oluşumu azalır → J_kritik artar. Tüm modüller bu tek
    tanımı kullanır (tutarlılık için).
    """
    T = T_C + C_TO_K
    T0 = T_ref_C + C_TO_K
    return J_ref * float(np.exp(-(Ea_eV / K_BOLTZMANN_EV) * (1.0 / T - 1.0 / T0)))


def sicaklik_tarama(se: KatiElektrolit, T_C_min: float = -30, T_C_max: float = 120, n: int = 151):
    T_C = np.linspace(T_C_min, T_C_max, n)
    return T_C, iletkenlik_C(se, T_C)
