"""
Sistem simülasyonu: eşdeğer devre (OCV(SOC) + sıcaklığa bağlı iç direnç) + toplu (lumped)
ısıl model + basit araç boyuna dinamiği ile sürüş çevrimi. Amaç: menzil, soğukta güç
yeteneği, kendi kendine ısınma ve gerilim sınırlarının doğrulanması.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .elektrolit import alan_direnci_ohm_cm2, arrhenius, kritik_akim_yogunlugu_mA_cm2
from .hucre import HucreSonucu
from .paket import PaketSonucu
from .sabitler import C_TO_K


# ---------------------------------------------------------------------------
# Elektrokimyasal eşdeğer devre
# ---------------------------------------------------------------------------

def ocv(soc: np.ndarray | float, V_ort: float) -> np.ndarray | float:
    """
    Faz-geçişli (iki fazlı) katotlar (NVP, NaCrO2) için düz platolu OCV eğrisi:
    hafif eğim + dolu/boş uçlarda dik kollar. SOC 0-1.
    """
    s = np.clip(np.asarray(soc, dtype=float), 0.0, 1.0)
    return (V_ort + 0.04 * (2 * s - 1)
            + 0.10 * np.tanh((s - 0.96) * 60)
            - 0.35 * np.exp(-s * 30))


def asr_sicaklik(h: HucreSonucu, T_C: float, Ea_arayuz_eV: float = 0.45) -> float:
    """Toplam ASR(T): ayırıcı (Arrhenius, SE) + katot kompozit (SE ile ölçekli) + arayüz (Ea_arayuz)."""
    t = h.tasarim
    T0 = t.calisma_sicakligi_C
    asr_ayirici_T0 = alan_direnci_ohm_cm2(t.elektrolit, t.ayirici_kalinlik_um, T0)
    asr_ayirici = alan_direnci_ohm_cm2(t.elektrolit, t.ayirici_kalinlik_um, T_C)
    asr_katot_T0 = h.asr_toplam_ohm_cm2 - asr_ayirici_T0 - t.arayuz_direnci_ohm_cm2
    olcek_se = asr_ayirici / asr_ayirici_T0
    asr_arayuz = t.arayuz_direnci_ohm_cm2 / float(arrhenius(1.0, Ea_arayuz_eV, T_C + C_TO_K, T0 + C_TO_K))
    return asr_ayirici + asr_katot_T0 * olcek_se + asr_arayuz


def hucre_direnci_ohm(h: HucreSonucu, T_C: float) -> float:
    alan_cm2 = (h.tasarim.pouch_en_mm * h.tasarim.pouch_boy_mm / 100.0) * 2 * h.katman_sayisi
    return asr_sicaklik(h, T_C) / alan_cm2


def maks_guc_kW(p: PaketSonucu, T_C: float, soc: float = 0.5, V_min_hucre: float = 2.3,
                j_kritik_25C_mA_cm2: float = 3.0, desarj_toleransi: float = 2.0,
                j_tavan_mA_cm2: float = 12.0) -> float:
    """
    Verilen sıcaklık ve SOC'de 10 s tepe deşarj gücü. Üç sınırın en küçüğü alınır:
      (1) omik sınır: hücre gerilimi V_min'e düşmeden çekilebilecek akım, P = V_min·(OCV − V_min)/R;
      (2) arayüz sınırı: Na soyulma/kaplama kritik akım yoğunluğu (Arrhenius ölçekli, deşarjda
          `desarj_toleransi` kat esneklik) × elektrot alanı;
      (3) katot tavanı: kompozit katotta katı hâl difüzyonu/ısıl sınır için mutlak j tavanı (~4C).
    """
    R = hucre_direnci_ohm(p.hucre, T_C)
    U = float(ocv(soc, p.hucre.gerilim_V))
    I_omik = max(0.0, (U - V_min_hucre) / R)
    alan_cm2 = (p.hucre.tasarim.pouch_en_mm * p.hucre.tasarim.pouch_boy_mm / 100.0) * 2 * p.hucre.katman_sayisi
    j_arayuz = min(kritik_akim_yogunlugu_mA_cm2(T_C, J_ref=j_kritik_25C_mA_cm2) * desarj_toleransi, j_tavan_mA_cm2)
    I_arayuz = j_arayuz * alan_cm2 / 1e3
    if I_omik <= I_arayuz:
        P_hucre = V_min_hucre * I_omik
    else:
        P_hucre = (U - I_arayuz * R) * I_arayuz
    return P_hucre * p.hucre_sayisi / 1e3


# ---------------------------------------------------------------------------
# Araç ve sürüş çevrimi
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Arac:
    ad: str = "C-segment EV"
    glider_kutle_kg: float = 1350.0     # batarya paketi hariç araç kütlesi
    yuk_kg: float = 150.0
    Cd: float = 0.27
    alan_m2: float = 2.30
    Crr: float = 0.0090
    eta_tahrik: float = 0.90            # invertör + motor + dişli (sürüş)
    eta_rejen: float = 0.65             # tekerlek → batarya
    yardimci_guc_W: float = 600.0       # HVAC hariç
    hava_yogunlugu: float = 1.20
    g: float = 9.81


def wltp_benzeri_cevrim(dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """
    WLTP sınıf-3 yapısına yakın sentetik hız profili (düşük/orta/yüksek/çok yüksek fazlar;
    ~1800 s, ~23 km). Gerçek WLTP noktaları yerine trapez segmentler kullanılır.
    Dönüş: (t [s], v [m/s]).
    """
    segmentler = []  # (hedef hız km/h, süre s)
    def faz(hiz_listesi):
        for v, s in hiz_listesi:
            segmentler.append((v, s))
    # Düşük (589 s)
    faz([(0, 10), (30, 20), (30, 40), (0, 15), (0, 10), (45, 25), (45, 60), (20, 15), (20, 30), (0, 15),
         (0, 20), (35, 20), (35, 50), (0, 20), (0, 15), (50, 30), (50, 60), (25, 20), (0, 20), (0, 94)])
    # Orta (433 s)
    faz([(50, 25), (50, 60), (70, 20), (70, 70), (40, 20), (40, 40), (76, 25), (76, 70), (30, 30), (0, 30), (0, 43)])
    # Yüksek (455 s)
    faz([(60, 25), (60, 40), (95, 25), (95, 80), (50, 25), (50, 60), (97, 25), (97, 50), (0, 45), (0, 80)])
    # Çok yüksek (323 s)
    faz([(80, 25), (80, 30), (110, 25), (110, 40), (131, 25), (131, 45), (90, 25), (90, 25), (0, 40), (0, 43)])

    v = []
    v_onceki = 0.0
    for hedef_kmh, sure in segmentler:
        hedef = hedef_kmh / 3.6
        n = max(1, int(sure / dt))
        v.extend(np.linspace(v_onceki, hedef, n, endpoint=False))
        v_onceki = hedef
    v = np.array(v)
    t = np.arange(len(v)) * dt
    return t, v


def tekerlek_gucu_W(arac: Arac, toplam_kutle: float, v: np.ndarray, a: np.ndarray) -> np.ndarray:
    F = (0.5 * arac.hava_yogunlugu * arac.Cd * arac.alan_m2 * v**2
         + arac.Crr * toplam_kutle * arac.g
         + toplam_kutle * a)
    return F * v


@dataclass
class SurusSonucu:
    menzil_km: float
    tuketim_kWh_100km: float
    T_baslangic_C: float
    T_bitis_C: float
    V_min_hucre: float
    isi_uretimi_ort_W: float
    toplam_kutle_kg: float


def surus_simulasyonu(p: PaketSonucu, arac: Arac = Arac(), T_ortam_C: float = 20.0,
                      T_baslangic_C: float | None = None, isitici_hedef_C: float | None = 25.0,
                      isitici_guc_kW: float = 3.0, soc_bitis: float = 0.05) -> SurusSonucu:
    """
    Çevrimi SOC bitene kadar tekrarlayarak menzil hesaplar. Isıl model: m·c·dT/dt = I²R + P_ısıtıcı − UA·(T−T_ortam).
    Isıtıcı: hücre sıcaklığı hedefin altındaysa (bataryadan beslenerek) çalışır — soğuk iklim senaryosu.
    """
    t, v = wltp_benzeri_cevrim()
    dt = float(t[1] - t[0])
    a = np.gradient(v, dt)
    toplam_kutle = arac.glider_kutle_kg + arac.yuk_kg + p.paket_kutle_kg
    P_teker = tekerlek_gucu_W(arac, toplam_kutle, v, a)
    P_bat_cevrim = np.where(P_teker >= 0, P_teker / arac.eta_tahrik, P_teker * arac.eta_rejen) + arac.yardimci_guc_W
    mesafe_cevrim_km = float(np.trapezoid(v, t) / 1e3)

    E_kWh = p.gercek_enerji_kWh
    soc = 1.0
    T = T_ortam_C if T_baslangic_C is None else T_baslangic_C
    C_isil = p.paket_kutle_kg * p.gereksinim.paket_isi_kapasitesi_kJ_kgK * 1e3  # J/K
    UA = p.isi_kaybi_W_per_K
    n = p.hucre_sayisi
    V_min = 10.0
    mesafe_km = 0.0
    q_toplam_J = 0.0
    sure_s = 0.0
    kapasite_As = p.hucre.hucre_kapasite_Ah * 3600.0
    bitti = False

    while not bitti and sure_s < 200 * t[-1]:
        for i in range(len(v)):
            P_bat = P_bat_cevrim[i]
            P_isitici = isitici_guc_kW * 1e3 if (isitici_hedef_C is not None and T < isitici_hedef_C) else 0.0
            R_h = hucre_direnci_ohm(p.hucre, T)
            U = float(ocv(soc, p.hucre.gerilim_V))
            P_h = (P_bat + P_isitici) / n            # hücre başına güç (seri-paralel simetrik)
            # V·I = P_h, V = U − I·R  →  R·I² − U·I + P_h = 0  (küçük kök = kararlı çözüm)
            disc = U * U - 4 * R_h * P_h
            I_h = U / (2 * R_h) if disc < 0 else (U - np.sqrt(disc)) / (2 * R_h)
            V_h = U - I_h * R_h
            if P_h > 0:
                V_min = min(V_min, V_h)
            soc -= I_h * dt / kapasite_As
            Q = I_h**2 * R_h * n
            q_toplam_J += Q * dt
            T += (Q + P_isitici - UA * (T - T_ortam_C)) * dt / C_isil
            mesafe_km += v[i] * dt / 1e3
            sure_s += dt
            if soc <= soc_bitis:
                bitti = True
                break

    kullanilan_kWh = E_kWh * (1.0 - soc)
    return SurusSonucu(
        menzil_km=mesafe_km,
        tuketim_kWh_100km=kullanilan_kWh / mesafe_km * 100.0 if mesafe_km > 0 else float("nan"),
        T_baslangic_C=T_ortam_C if T_baslangic_C is None else T_baslangic_C,
        T_bitis_C=T,
        V_min_hucre=V_min,
        isi_uretimi_ort_W=q_toplam_J / max(1.0, sure_s),
        toplam_kutle_kg=toplam_kutle,
    )


def sabit_akim_desarj(h: HucreSonucu, c_orani: float, T_C: float, n_nokta: int = 200):
    """Sabit C-hızında deşarj eğrisi: (kapasite Ah, gerilim V)."""
    R = hucre_direnci_ohm(h, T_C)
    I = c_orani * h.hucre_kapasite_Ah
    soc = np.linspace(1.0, 0.0, n_nokta)
    V = ocv(soc, h.gerilim_V) - I * R
    Ah = (1 - soc) * h.hucre_kapasite_Ah
    gecerli = V > 2.0
    return Ah[gecerli], V[gecerli]
