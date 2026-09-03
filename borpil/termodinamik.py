"""
Elektrokimyasal termodinamik: Gibbs enerjisinden hücre potansiyeli, Nernst düzeltmesi,
teorik kapasite/enerji yoğunluğu ve bor esaslı alternatif kimyaların (bor-hava, doğrudan
borhidrür yakıt pili) teorik sınırları.

Standart oluşum Gibbs enerjileri (kJ/mol, 298 K) NIST-JANAF / CRC değerleridir.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .sabitler import FARADAY, FARADAY_MAH, M, R_GAZ, T_ODA, molar_kutle

# ΔG°f (kJ/mol), 298.15 K
DG_F = {
    "B2O3(s)": -1194.3,
    "H2O(l)": -237.13,
    "NaBH4(s)": -123.9,
    "NaBO2(s)": -920.7,
    "Na2O(s)": -375.5,
    "MgO(s)": -569.3,
    "Li2O(s)": -561.2,
    "O2(g)": 0.0,
    "B(s)": 0.0,
    "Na(s)": 0.0,
    "Mg(s)": 0.0,
    "Li(s)": 0.0,
}


def hucre_potansiyeli(dG_kJ_mol: float, n_elektron: float) -> float:
    """E° = -ΔG / (nF). ΔG kJ/mol cinsinden (reaksiyon başına), sonuç V."""
    return -dG_kJ_mol * 1000.0 / (n_elektron * FARADAY)


def nernst(E0: float, n: float, T: float = T_ODA, aktivite_orani: float = 1.0) -> float:
    """E = E° - (RT/nF)·ln(Q). aktivite_orani = Q (ürünler/reaktanlar)."""
    return E0 - (R_GAZ * T / (n * FARADAY)) * np.log(aktivite_orani)


def sicaklik_katsayisi_duzeltme(E0: float, dS_J_molK: float, n: float, T: float) -> float:
    """dE/dT = ΔS/(nF) ile E(T) ≈ E°(298) + (ΔS/nF)(T-298)."""
    return E0 + dS_J_molK / (n * FARADAY) * (T - T_ODA)


@dataclass(frozen=True)
class TeorikKimya:
    ad: str
    reaksiyon: str
    E0_V: float
    n_elektron: float
    kutle_reaktan_g: float        # oksijen HARİÇ, taşınan aktif kütle (g / reaksiyon)
    kutle_urun_g: float           # O2 dâhil toplam ürün kütlesi (g / reaksiyon)

    @property
    def kapasite_mah_g(self) -> float:
        """Taşınan reaktan başına teorik kapasite (mAh/g)."""
        return self.n_elektron * FARADAY_MAH / self.kutle_reaktan_g

    @property
    def enerji_wh_kg_reaktan(self) -> float:
        return self.kapasite_mah_g * self.E0_V  # mAh/g·V = mWh/g = Wh/kg

    @property
    def enerji_wh_kg_urun(self) -> float:
        """Havadan alınan oksijen de dâhil (deşarj sonu kütlesi) — hava pillerinde adil kıyas."""
        return self.n_elektron * FARADAY_MAH / self.kutle_urun_g * self.E0_V


def bor_hava() -> TeorikKimya:
    """4B + 3O2 → 2B2O3. Teorik üst sınır; tersinir değil, pasivasyon nedeniyle pratik değil."""
    dG = 2 * DG_F["B2O3(s)"]
    n = 12  # 4 B × 3 e
    return TeorikKimya(
        ad="Bor-hava (teorik)",
        reaksiyon="4B + 3O2 → 2B2O3",
        E0_V=hucre_potansiyeli(dG, n),
        n_elektron=n,
        kutle_reaktan_g=4 * M["B"],
        kutle_urun_g=2 * molar_kutle({"B": 2, "O": 3}),
    )


def dbfc() -> TeorikKimya:
    """
    Doğrudan borhidrür yakıt pili: NaBH4 + 2O2 → NaBO2 + 2H2O (8 e-).
    Alkali ortamda BH4- + 8OH- → BO2- + 6H2O + 8e- (E° ≈ -1.24 V) ve O2 katodu (+0.40 V).
    """
    dG = DG_F["NaBO2(s)"] + 2 * DG_F["H2O(l)"] - DG_F["NaBH4(s)"]
    n = 8
    return TeorikKimya(
        ad="Doğrudan borhidrür yakıt pili (DBFC, teorik)",
        reaksiyon="NaBH4 + 2O2 → NaBO2 + 2H2O",
        E0_V=hucre_potansiyeli(dG, n),
        n_elektron=n,
        kutle_reaktan_g=molar_kutle({"Na": 1, "B": 1, "H": 4}),
        kutle_urun_g=molar_kutle({"Na": 1, "B": 1, "O": 2}) + 2 * molar_kutle({"H": 2, "O": 1}),
    )


def dbfc_pratik(
    nabh4_kutle_kesri: float = 0.20,
    calisma_gerilimi_V: float = 1.0,
    yakit_kullanimi: float = 0.75,
    sistem_kutle_carpani: float = 1.6,
) -> dict[str, float]:
    """
    Alkali sulu NaBH4 çözeltisiyle (ör. %20 NaBH4 / %10 NaOH) pratik enerji yoğunluğu tahmini.
    yakit_kullanimi: hidroliz kaynaklı BH4- kaybı sonrası faradaik kullanım oranı.
    sistem_kutle_carpani: yığın + tank + pompa + BOP dâhil kütle çarpanı (yakıt kütlesine oranla).
    """
    t = dbfc()
    wh_kg_yakit = t.kapasite_mah_g * calisma_gerilimi_V * yakit_kullanimi  # saf NaBH4 başına
    wh_kg_cozelti = wh_kg_yakit * nabh4_kutle_kesri
    return {
        "E0_V": t.E0_V,
        "teorik_wh_kg_nabh4": t.enerji_wh_kg_reaktan,
        "pratik_wh_kg_nabh4": wh_kg_yakit,
        "pratik_wh_kg_cozelti": wh_kg_cozelti,
        "pratik_wh_kg_sistem": wh_kg_cozelti / sistem_kutle_carpani,
    }


def dbfc_gidis_donus(rejenerasyon_verimi: float = 0.35, **pratik_kwargs) -> dict[str, float]:
    """
    NaBO2 → NaBH4 rejenerasyonu (elektrokimyasal/hidrojenle indirgeme) dâhil gidiş-dönüş verimi.
    Rejenerasyonun teorik enerji girdisi = -ΔG_rxn (9.33 kWh/kg NaBH4); pratik verim
    (rejenerasyon_verimi) literatürde %20-40 arasındadır. Sonuç: pil olarak kullanılırsa
    elektrik→elektrik verimi. Bu, DBFC'nin ana depolama yerine yakıt/menzil uzatıcı olarak
    konumlandırılmasının nicel gerekçesidir.
    """
    p = dbfc_pratik(**pratik_kwargs)
    girdi = p["teorik_wh_kg_nabh4"] / rejenerasyon_verimi
    return {
        "rejenerasyon_girdisi_kwh_per_kg_nabh4": girdi / 1e3,
        "cikti_kwh_per_kg_nabh4": p["pratik_wh_kg_nabh4"] / 1e3,
        "gidis_donus_verimi": p["pratik_wh_kg_nabh4"] / girdi,
    }


def dbfc_menzil_uzatici(
    cozelti_kutle_kg: float = 40.0,
    tuketim_kWh_100km: float = 15.0,
    yigin_guc_kW: float = 15.0,
    yigin_ozgul_guc_W_kg: float = 150.0,
    tank_bop_kutle_kg: float = 20.0,
    **pratik_kwargs,
) -> dict[str, float]:
    """
    Araca eklenen bir DBFC menzil uzatıcının kaba boyutlandırması: NaBH₄ çözeltisi tankı
    (harcanan çözelti NaBO₂ olarak tankta kalır; kütle sabit), yığın ve yardımcı ekipman.
    Yığın ortalama seyir gücünü (~15 kW) karşılar; tepe güç bataryadan gelir (hibrit).
    """
    p = dbfc_pratik(**pratik_kwargs)
    enerji_kWh = p["pratik_wh_kg_cozelti"] * cozelti_kutle_kg / 1e3
    yigin_kg = yigin_guc_kW * 1e3 / yigin_ozgul_guc_W_kg
    toplam_kg = cozelti_kutle_kg + yigin_kg + tank_bop_kutle_kg
    return {
        "enerji_kWh": enerji_kWh,
        "ek_menzil_km": enerji_kWh / tuketim_kWh_100km * 100.0,
        "sistem_kutle_kg": toplam_kg,
        "sistem_wh_kg": enerji_kWh * 1e3 / toplam_kg,
        "nabh4_kg": cozelti_kutle_kg * pratik_kwargs.get("nabh4_kutle_kesri", 0.20),
        "dolum_suresi_dk": 3.0,  # sıvı yakıt dolumu; şarj değil
    }


def metal_hava_kiyas() -> list[TeorikKimya]:
    """Bor-hava'yı Li-, Na-, Mg-hava teorik değerleriyle aynı yöntemle kıyaslar."""
    liste = [bor_hava()]
    for ad, rxn, dg, n, reak, urun in [
        ("Li-hava (Li2O)", "4Li + O2 → 2Li2O", 2 * DG_F["Li2O(s)"], 4, 4 * M["Li"], 2 * molar_kutle({"Li": 2, "O": 1})),
        ("Na-hava (Na2O)", "4Na + O2 → 2Na2O", 2 * DG_F["Na2O(s)"], 4, 4 * M["Na"], 2 * molar_kutle({"Na": 2, "O": 1})),
        ("Mg-hava (MgO)", "2Mg + O2 → 2MgO", 2 * DG_F["MgO(s)"], 4, 2 * M["Mg"], 2 * molar_kutle({"Mg": 1, "O": 1})),
    ]:
        liste.append(TeorikKimya(ad, rxn, hucre_potansiyeli(dg, n), n, reak, urun))
    return liste


def elektrot_cifti_teorik_enerji(
    q_katot_mah_g: float, q_anot_mah_g: float, V_ort: float
) -> dict[str, float]:
    """
    Yalnızca aktif maddeler üzerinden teorik enerji yoğunluğu.
    Toplam aktif kütle başına kapasite: 1/(1/Qc + 1/Qa).
    """
    q_cift = 1.0 / (1.0 / q_katot_mah_g + 1.0 / q_anot_mah_g)
    return {
        "kapasite_mah_g_aktif": q_cift,
        "enerji_wh_kg_aktif": q_cift * V_ort,
        "katot_kutle_orani": q_cift / q_katot_mah_g,
    }
