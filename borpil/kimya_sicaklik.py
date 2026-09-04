"""
10–45 °C çalışma penceresi için kimya taraması (A1).

Soru: gen-1 kloso-borat karışımının 35–60 °C bandını kimya ile 10–45 °C'ye çekmek
soğuk UX sorununu çözer mi?

Cevap üç katmana ayrılır (bulk σ, arayüz ASR, Na kaplama CCD). Bulk, ölçülmüş
karba-kloso-boratla 10 °C'de zaten yeterlidir; CCD/arayüz aynı Arrhenius eğimiyle
kalırsa pencere tek başına sorunu kapatmaz.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import elektrolit as el
from . import malzemeler as mz
from .sabitler import C_TO_K, K_BOLTZMANN_EV

# Gen-1 tasarım noktasındaki bulk iletkenlik (A, 45 °C) — 10 °C'de yakalanacak hedef.
SIGMA_TASARIM_45C_S_CM = float(el.iletkenlik_C(mz.NA2_B12_B10, 45.0))  # ≈ 3.12e-3
CCD_TASARIM_45C = el.kritik_akim_yogunlugu_mA_cm2(45.0)                 # ≈ 4.49
# Sürekli 80 kW / tepe 200 kW için kaba j (3 mAh/cm², 360 hücre, 404 V) burada kullanılmaz;
# tarama CCD ve σ eşikleriyle yapılır.


def _arrhenius_carpan(T_C: float, T_ref_C: float, Ea_eV: float) -> float:
    T = T_C + C_TO_K
    T0 = T_ref_C + C_TO_K
    return float(np.exp(-(Ea_eV / K_BOLTZMANN_EV) * (1.0 / T - 1.0 / T0)))


def sigma_25_icin_hedef(hedef_sigma_10C: float, Ea_eV: float) -> float:
    """10 °C'de hedef σ için gereken σ(25 °C)."""
    return hedef_sigma_10C / _arrhenius_carpan(10.0, 25.0, Ea_eV)


def ea_icin_j25(hedef_ccd_10C: float, Ea_eV: float) -> float:
    """10 °C'de hedef CCD için gereken J_kritik(25 °C)."""
    return hedef_ccd_10C / _arrhenius_carpan(10.0, 25.0, Ea_eV)


def ccd_ea_icin_sabit_j25(hedef_ccd_10C: float, J_25: float = el.J_KRITIK_25C_MA_CM2) -> float:
    """J_25 sabitken 10 °C hedef CCD için gereken arayüz Ea (eV).

    hedef ≥ J_25 ise soğuyunca artan CCD gerekir → pozitif Ea ile imkânsız (inf).
    Ea→0 iken CCD(10 °C) → J_25; 4,5 mA/cm² @45 °C eşleşmesi için Ea düşürmek yetmez.
    """
    d = 1.0 / (10.0 + C_TO_K) - 1.0 / (25.0 + C_TO_K)
    oran = hedef_ccd_10C / J_25
    if oran >= 1.0:
        return float("inf")
    return float(-K_BOLTZMANN_EV * np.log(oran) / d)


@dataclass(frozen=True)
class ElektrolitTarama:
    ad: str
    ea_eV: float
    sigma_10: float
    sigma_25: float
    sigma_45: float
    asr30_10: float
    bulk_10C_yeterli: bool
    olcum: bool
    notlar: str


def elektrolit_taramasi() -> list[ElektrolitTarama]:
    hedef = SIGMA_TASARIM_45C_S_CM
    satirlar = []
    for ad, se in mz.KATI_ELEKTROLITLER.items():
        s10 = float(el.iletkenlik_C(se, 10.0))
        s25 = float(el.iletkenlik_C(se, 25.0))
        s45 = float(el.iletkenlik_C(se, 45.0))
        satirlar.append(ElektrolitTarama(
            ad=ad, ea_eV=se.Ea,
            sigma_10=s10, sigma_25=s25, sigma_45=s45,
            asr30_10=el.alan_direnci_ohm_cm2(se, 30.0, 10.0),
            bulk_10C_yeterli=s10 >= hedef,
            olcum=se.T_gecis is None or ad.startswith("Na2(B12"),
            notlar=se.notlar[:80] if se.notlar else se.kaynak[:80],
        ))
    return satirlar


@dataclass(frozen=True)
class SentezHedefi:
    """Ölçülmemiş tarama hedefi — sentez KPI'sı, malzeme veri tabanına konmaz."""
    ad: str
    ea_eV: float
    sigma_25_S_cm: float
    j25_mA_cm2: float
    ea_ccd_eV: float

    def sigma_C(self, T_C: float) -> float:
        return self.sigma_25_S_cm * _arrhenius_carpan(T_C, 25.0, self.ea_eV)

    def ccd_C(self, T_C: float) -> float:
        return self.j25_mA_cm2 * _arrhenius_carpan(T_C, 25.0, self.ea_ccd_eV)


# Bulk: 10 °C'de gen-1'in 45 °C σ'sı. CCD: 10 °C'de bugünkü 45 °C CCD'si (tam eşleşme).
HEDEF_BULK = SentezHedefi("Bulk-yalnız (CCD aynı)", 0.30, sigma_25_icin_hedef(SIGMA_TASARIM_45C_S_CM, 0.30),
                          el.J_KRITIK_25C_MA_CM2, el.EA_ARAYUZ_EV)
HEDEF_TAM = SentezHedefi("Bulk+CCD (10 °C ≈ bugünkü 45 °C)", 0.25, sigma_25_icin_hedef(SIGMA_TASARIM_45C_S_CM, 0.25),
                         ea_icin_j25(CCD_TASARIM_45C, 0.22), 0.22)
HEDEF_YUMUSAK = SentezHedefi("Yumuşak (10 °C'de 80 kW sınıfı, CCD×2 ≥ 3 mA/cm²)", 0.28,
                             sigma_25_icin_hedef(1e-3, 0.28),  # 1 mS/cm @10 °C
                             ea_icin_j25(1.5, 0.30), 0.30)


def sentez_hedefleri() -> list[SentezHedefi]:
    return [HEDEF_BULK, HEDEF_YUMUSAK, HEDEF_TAM]


def ccd_tablosu(sicakliklar: tuple[float, ...] = (-10, 0, 10, 25, 35, 45)) -> list[dict]:
    satir = []
    for T in sicakliklar:
        satir.append({
            "T_C": T,
            "ccd_gen1": el.kritik_akim_yogunlugu_mA_cm2(T),
            "ccd_ea022": el.kritik_akim_yogunlugu_mA_cm2(T, Ea_eV=0.22),
            "ccd_j25_4": el.kritik_akim_yogunlugu_mA_cm2(T, J_ref=4.0),
            "desarj_j_gen1": min(el.kritik_akim_yogunlugu_mA_cm2(T) * 2.0, 12.0),
        })
    return satir


def ozet_metin() -> str:
    s10_a = float(el.iletkenlik_C(mz.NA2_B12_B10, 10.0)) * 1e3
    s10_b = float(el.iletkenlik_C(mz.NA2_CB9_CB11, 10.0)) * 1e3
    s45_a = SIGMA_TASARIM_45C_S_CM * 1e3
    j10 = el.kritik_akim_yogunlugu_mA_cm2(10.0)
    j25_gerek = ea_icin_j25(CCD_TASARIM_45C, el.EA_ARAYUZ_EV)
    return "\n".join([
        "== Kimya taraması: 10–45 °C penceresi ==",
        f"Gen-1 B12/B10: σ(10 °C)={s10_a:.2f} mS/cm vs σ(45 °C)={s45_a:.2f} mS/cm (bulk {s45_a/s10_a:.1f}× zayıf).",
        f"Karba-kloso Na2(CB9H10)(CB11H12): σ(10 °C)={s10_b:.1f} mS/cm — bulk eşiği ({s45_a:.2f}) AŞILIR.",
        f"CCD gen-1 (Ea=0.45 eV): {j10:.2f} mA/cm² @10 °C vs {CCD_TASARIM_45C:.2f} @45 °C ({CCD_TASARIM_45C/j10:.1f}×).",
        f"10 °C'de bugünkü 45 °C CCD için J_25={j25_gerek:.1f} mA/cm² zorunlu (Ea düşürmek yetmez: "
        f"Ea→0 iken CCD(10)→{el.J_KRITIK_25C_MA_CM2} mA/cm² < {CCD_TASARIM_45C:.1f}).",
        "Sonuç: yalnız elektrolit bulk'ını değiştirmek 10–45 °C'yi açmaz; Na/SE arayüz CCD'si birincil kilit.",
        "BorPil-LT = NVP + ölçülmüş karba-kloso (4 V katot yok). BorPil-B = aynı SE + NVPF (oksidasyon riski).",
    ])


def guc_karsilastirma(anahtarlar: tuple[str, ...] = ("A-alt", "A", "LT", "B", "C")) -> list[dict]:
    """Paket tepe deşarj ve şarj gücü (°C). CCD modeli tümünde Na-metal (C için muhafazakâr)."""
    from . import hucre as hc
    from . import paket as pk
    from . import simulasyon as sm
    satir = []
    for k in anahtarlar:
        p = pk.boyutlandir(hc.VARYANTLAR[k])
        satir.append({
            "ad": k,
            "wh_kg": p.hucre.hucre_wh_kg,
            "P10": sm.maks_guc_kW(p, 10.0),
            "P25": sm.maks_guc_kW(p, 25.0),
            "P45": sm.maks_guc_kW(p, 45.0),
            "chg10": sm.maks_sarj_gucu_kW(p, 10.0),
            "chg25": sm.maks_sarj_gucu_kW(p, 25.0),
            "chg45": sm.maks_sarj_gucu_kW(p, 45.0),
            "T75kW": p.hizli_sarj_min_T_C,
            "usd": p.maliyet_usd_kWh,
        })
    return satir


def markdown_bolum() -> str:
    satirlar = [
        "## 10. Kimya taraması: 10–45 °C penceresi (A1)\n",
        ozet_metin() + "\n",
        "| Elektrolit | Ea eV | σ(10) mS/cm | σ(25) | σ(45) | ASR 30 µm @10 °C | Bulk 10 °C ≥ gen-1@45 °C |\n"
        "|---|---:|---:|---:|---:|---:|:---:|",
    ]
    for t in elektrolit_taramasi():
        evet = "evet" if t.bulk_10C_yeterli else "hayır"
        satirlar.append(
            f"| {t.ad} | {t.ea_eV:.2f} | {t.sigma_10*1e3:.3g} | {t.sigma_25*1e3:.3g} | "
            f"{t.sigma_45*1e3:.3g} | {t.asr30_10:.2g} | {evet} |"
        )
    satirlar.append("")
    satirlar.append("| T °C | CCD gen-1 mA/cm² | deşarj j (CCD×2) | CCD Ea=0.22 | CCD J_25=4 |\n|---:|---:|---:|---:|---:|")
    for r in ccd_tablosu():
        satirlar.append(
            f"| {r['T_C']:.0f} | {r['ccd_gen1']:.2f} | {r['desarj_j_gen1']:.2f} | "
            f"{r['ccd_ea022']:.2f} | {r['ccd_j25_4']:.2f} |"
        )
    satirlar.append("")
    satirlar.append("| Sentez hedefi | Ea bulk | σ(25) mS/cm | σ(10) | J_25 | Ea CCD | CCD(10) |\n|---|---:|---:|---:|---:|---:|---:|")
    for h in sentez_hedefleri():
        satirlar.append(
            f"| {h.ad} | {h.ea_eV:.2f} | {h.sigma_25_S_cm*1e3:.2f} | {h.sigma_C(10)*1e3:.2f} | "
            f"{h.j25_mA_cm2:.2f} | {h.ea_ccd_eV:.2f} | {h.ccd_C(10):.2f} |"
        )
    satirlar.append("")
    satirlar.append("| Varyant | Wh/kg hücre | P_dch 10/25/45 °C kW | P_chg 10/25/45 °C kW | 75 kW için min T | USD/kWh |\n"
                    "|---|---:|---:|---:|---:|---:|")
    for g in guc_karsilastirma():
        satirlar.append(
            f"| {g['ad']} | {g['wh_kg']:.0f} | {g['P10']:.0f} / {g['P25']:.0f} / {g['P45']:.0f} | "
            f"{g['chg10']:.0f} / {g['chg25']:.0f} / {g['chg45']:.0f} | {g['T75kW']:.0f} | {g['usd']:.0f} |"
        )
    satirlar.append("")
    satirlar.append(
        "Yorum: LT ve B, karba-kloso ile omik kaybı 10 °C'de düşürür; **tepe güç hâlâ CCD** "
        "(10 °C satırları A-alt ile aynı mertebede kalır). 75 kW kapısı ~44 °C'den inmez. "
        "Ayrıntı ve kimya rotaları: `docs/10_kimya_10_45C.md`.\n"
    )
    return "\n".join(satirlar)
