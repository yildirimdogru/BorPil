"""
EV batarya paketi boyutlandırma: hücre → modül/CTP → paket. Kütle, hacim, gerilim
mimarisi, element bütçesi, maliyet ve ısıl ön-şartlandırma enerjisi.
"""

from __future__ import annotations

from dataclasses import dataclass

from .hucre import HucreSonucu, HucreTasarimi, hesapla


@dataclass(frozen=True)
class PaketGereksinimi:
    ad: str = "C-segment sedan/SUV"
    brut_enerji_kWh: float = 75.0
    nominal_gerilim_V: float = 400.0
    kullanilabilir_soc_penceresi: float = 0.92
    surekli_guc_kW: float = 80.0      # ~1C sürekli (otoyol tırmanış senaryosu)
    tepe_guc_kW: float = 200.0        # 10 s darbe
    hizli_sarj_kW: float = 75.0       # 1. nesil: Na kaplama kritik akım yoğunluğu ile sınırlı (~1C)
    # Elektrik mimarisi (EE incelemesi)
    invertor_dc_link_maks_V: float = 500.0   # 400 V sınıfı (750 V Si/SiC); 800 V sınıfı için 860
    sarj_cihazi_maks_V: float = 500.0        # CCS 400 V sınıfı; 800 V sınıfı için 1000
    sarj_cihazi_maks_A: float = 500.0
    busbar_kontaktor_mohm: float = 2.0       # busbar + kontaktör + sigorta toplamı
    tab_genislik_mm: float = 100.0
    tab_kalinlik_mm: float = 0.3             # Al tab (EE: 0.2 → 0.3 mm, sürekli ≤ 2.5 A/mm²)
    tab_akim_yogunlugu_surekli_maks_A_mm2: float = 2.5
    # Kütle/hacim çarpanları: CTP (cell-to-pack) mimarisi; katı hâl (yanıcı elektrolit yok)
    # → daha az yangın bariyeri, ancak yığın basıncı fikstürü (1-2 MPa), 12 mm yalıtım ve ısıtıcı
    # eklenir. Hakem önerisi aralığı: 0.65-0.72 kütle, 0.50-0.58 hacim.
    hucre_paket_kutle_orani: float = 0.72
    hucre_paket_hacim_orani: float = 0.56
    # Maliyet: hücre imalat çarpanı (malzeme → hücre) ve paket düzeyi ek maliyet
    imalat_carpani: float = 1.55
    paket_ek_usd_kWh: float = 22.0
    # Isıl
    yalitim_kalinlik_mm: float = 12.0
    yalitim_k_W_mK: float = 0.022           # aerojel keçe
    paket_yuzey_m2: float = 5.5
    paket_isi_kapasitesi_kJ_kgK: float = 1.0


@dataclass
class PaketSonucu:
    gereksinim: PaketGereksinimi
    hucre: HucreSonucu
    seri: int
    paralel: int
    hucre_sayisi: int
    gercek_enerji_kWh: float
    kullanilabilir_enerji_kWh: float
    nominal_gerilim_V: float
    paket_kutle_kg: float
    paket_hacim_L: float
    paket_wh_kg: float
    paket_wh_L: float
    bor_kg: float
    na_kg: float
    v_kg: float
    li_kg: float
    maliyet_usd: float
    maliyet_usd_kWh: float
    surekli_akim_yogunlugu_mA_cm2: float
    tepe_akim_yogunlugu_mA_cm2: float
    isi_kaybi_W_per_K: float
    on_isitma_kWh_minus10_to_25: float
    V_min_paket: float = 0.0
    V_maks_paket: float = 0.0
    tepe_akim_paket_A: float = 0.0
    tab_akim_yogunlugu_surekli_A_mm2: float = 0.0
    hizli_sarj_min_T_C: float = 0.0          # CCD/SF ile hizli_sarj_kW'a izin veren en düşük paket sıcaklığı
    kisa_devre_akimi_45C_kA: float = 0.0
    kisa_devre_akimi_m10C_A: float = 0.0
    uyarilar: list[str] = None  # type: ignore[assignment]

    def ozet(self) -> str:
        g = self.gereksinim
        return "\n".join([
            f"== Paket: {g.ad} — {g.brut_enerji_kWh:.0f} kWh hedef, {g.nominal_gerilim_V:.0f} V ==",
            f"Hücre: {self.hucre.tasarim.ad}",
            f"Mimari: {self.seri}s{self.paralel}p = {self.hucre_sayisi} hücre × {self.hucre.hucre_kapasite_Ah:.1f} Ah, "
            f"{self.nominal_gerilim_V:.0f} V nominal",
            f"Enerji: {self.gercek_enerji_kWh:.1f} kWh brüt / {self.kullanilabilir_enerji_kWh:.1f} kWh kullanılabilir",
            f"Kütle {self.paket_kutle_kg:.0f} kg ({self.paket_wh_kg:.0f} Wh/kg), hacim {self.paket_hacim_L:.0f} L ({self.paket_wh_L:.0f} Wh/L)",
            f"Element bütçesi: B {self.bor_kg:.1f} kg, Na {self.na_kg:.1f} kg, V {self.v_kg:.1f} kg, Li {self.li_kg:.1f} kg",
            f"Akım yoğunluğu: sürekli {self.surekli_akim_yogunlugu_mA_cm2:.2f} mA/cm², tepe {self.tepe_akim_yogunlugu_mA_cm2:.2f} mA/cm²",
            f"Isıl: kayıp {self.isi_kaybi_W_per_K:.1f} W/K (ΔT=40 K → {self.isi_kaybi_W_per_K*40:.0f} W); "
            f"-10→25 °C ön ısıtma {self.on_isitma_kWh_minus10_to_25:.1f} kWh",
            f"Maliyet (varsayımsal ölçek): {self.maliyet_usd:,.0f} USD → {self.maliyet_usd_kWh:.0f} USD/kWh",
            f"Elektrik: pencere {self.V_min_paket:.0f}–{self.V_maks_paket:.0f} V, tepe akım {self.tepe_akim_paket_A:.0f} A, "
            f"tab sürekli {self.tab_akim_yogunlugu_surekli_A_mm2:.1f} A/mm²; hızlı şarj ({g.hizli_sarj_kW:.0f} kW) için "
            f"paket ≥ {self.hizli_sarj_min_T_C:.0f} °C; beklenen kısa devre akımı 45 °C: {self.kisa_devre_akimi_45C_kA:.1f} kA, "
            f"−10 °C: {self.kisa_devre_akimi_m10C_A:.0f} A",
        ] + [f"  ! {u}" for u in (self.uyarilar or [])])


def boyutlandir(tasarim: HucreTasarimi, gereksinim: PaketGereksinimi = PaketGereksinimi(),
                hucre_kapasite_Ah: float = 60.0) -> PaketSonucu:
    h = hesapla(tasarim, hedef_kapasite_Ah=hucre_kapasite_Ah)
    seri = max(1, round(gereksinim.nominal_gerilim_V / h.gerilim_V))
    V_nom = seri * h.gerilim_V
    enerji_hucre_kWh = h.hucre_kapasite_Ah * h.gerilim_V / 1e3
    paralel = max(1, round(gereksinim.brut_enerji_kWh / (seri * enerji_hucre_kWh)))
    n = seri * paralel
    # Hücre kapasitesini, seri×paralel mimarisiyle hedef enerjiyi tam tutturacak şekilde yeniden boyutlandır
    hedef_hucre_Ah = gereksinim.brut_enerji_kWh * 1e3 / (n * h.gerilim_V)
    h = hesapla(tasarim, hedef_kapasite_Ah=hedef_hucre_Ah)
    enerji_hucre_kWh = h.hucre_kapasite_Ah * h.gerilim_V / 1e3
    E = n * enerji_hucre_kWh

    hucre_kutle = n * h.hucre_kutle_kg
    hucre_hacim = n * h.hucre_hacim_L
    paket_kutle = hucre_kutle / gereksinim.hucre_paket_kutle_orani
    paket_hacim = hucre_hacim / gereksinim.hucre_paket_hacim_orani

    # Toplam elektrot alanı (tek yüz eşdeğeri) → akım yoğunluğu
    alan_cm2 = h.elektrot_alani_cm2 * n
    # Hücre akımı = I_paket / paralel; hücre alanı = alan_toplam / n  →  j = I_paket · seri / alan_toplam
    I_surekli_A = gereksinim.surekli_guc_kW * 1e3 / V_nom
    j_surekli = I_surekli_A * seri / alan_cm2 * 1e3
    j_tepe = j_surekli * gereksinim.tepe_guc_kW / gereksinim.surekli_guc_kW

    UA = gereksinim.yalitim_k_W_mK * gereksinim.paket_yuzey_m2 / (gereksinim.yalitim_kalinlik_mm * 1e-3)
    on_isitma_kWh = paket_kutle * gereksinim.paket_isi_kapasitesi_kJ_kgK * 35.0 / 3600.0

    maliyet = E * (h.malzeme_usd_per_kwh * gereksinim.imalat_carpani + gereksinim.paket_ek_usd_kWh)

    # --- Elektrik mimarisi kontrolleri (EE incelemesi)
    from . import simulasyon as _sm  # döngüsel içe aktarmayı önlemek için yerel
    V_min_p = seri * _sm.v_min_hucre(h)
    V_maks_p = seri * (h.gerilim_V + 0.40)
    I_tepe = gereksinim.tepe_guc_kW * 1e3 / V_nom
    tab_alan_mm2 = gereksinim.tab_genislik_mm * gereksinim.tab_kalinlik_mm
    j_tab_surekli = (I_surekli_A / paralel) / tab_alan_mm2
    uyarilar: list[str] = []
    if V_maks_p > gereksinim.invertor_dc_link_maks_V:
        uyarilar.append(f"KRİTİK: paket üst gerilimi {V_maks_p:.0f} V invertör DC-link tavanını "
                        f"({gereksinim.invertor_dc_link_maks_V:.0f} V) aşıyor → seri sayısını azalt.")
    if V_maks_p > gereksinim.sarj_cihazi_maks_V:
        uyarilar.append(f"UYARI: paket üst gerilimi {V_maks_p:.0f} V şarj cihazı sınıfını ({gereksinim.sarj_cihazi_maks_V:.0f} V) aşıyor.")
    if j_tab_surekli > gereksinim.tab_akim_yogunlugu_surekli_maks_A_mm2:
        uyarilar.append(f"UYARI: tab sürekli akım yoğunluğu {j_tab_surekli:.1f} A/mm² > {gereksinim.tab_akim_yogunlugu_surekli_maks_A_mm2} A/mm².")
    # Hızlı şarj sıcaklık kapısı: CCD/SF · alan · n · V ≥ hizli_sarj_kW olan en düşük T
    T_kapi = 80.0
    for T_C in [x / 2 for x in range(-40, 161)]:
        if _sm.maks_sarj_gucu_kW(_p_gecici(h, n, seri, paralel), T_C) >= gereksinim.hizli_sarj_kW:
            T_kapi = T_C
            break
    if T_kapi > 45.0:
        uyarilar.append(f"UYARI: {gereksinim.hizli_sarj_kW:.0f} kW hızlı şarj için paket ≥ {T_kapi:.0f} °C gerekir (CCD/SF sınırı).")
    R_paket_45 = _sm.hucre_direnci_ohm(h, 45.0) * seri / paralel + gereksinim.busbar_kontaktor_mohm * 1e-3
    R_paket_m10 = _sm.hucre_direnci_ohm(h, -10.0) * seri / paralel + gereksinim.busbar_kontaktor_mohm * 1e-3
    I_kd_45 = V_maks_p / R_paket_45
    I_kd_m10 = V_maks_p / R_paket_m10
    if I_kd_m10 < 2 * I_surekli_A:
        uyarilar.append(f"UYARI: −10 °C'de beklenen kısa devre akımı ({I_kd_m10:.0f} A) sürekli çalışma akımının 2 katından düşük → "
                        f"sigorta soğukta kısa devreyi ayırt edemez; akım-plausibilite/dI/dt ile kontaktör açma gerekir.")

    return PaketSonucu(
        gereksinim=gereksinim, hucre=h, seri=seri, paralel=paralel, hucre_sayisi=n,
        gercek_enerji_kWh=E, kullanilabilir_enerji_kWh=E * gereksinim.kullanilabilir_soc_penceresi,
        nominal_gerilim_V=V_nom, paket_kutle_kg=paket_kutle, paket_hacim_L=paket_hacim,
        paket_wh_kg=E * 1e3 / paket_kutle, paket_wh_L=E * 1e3 / paket_hacim,
        bor_kg=h.bor_kg_per_kwh * E, na_kg=h.na_kg_per_kwh * E, v_kg=h.v_kg_per_kwh * E, li_kg=h.li_kg_per_kwh * E,
        maliyet_usd=maliyet, maliyet_usd_kWh=maliyet / E,
        surekli_akim_yogunlugu_mA_cm2=j_surekli, tepe_akim_yogunlugu_mA_cm2=j_tepe,
        isi_kaybi_W_per_K=UA, on_isitma_kWh_minus10_to_25=on_isitma_kWh,
        V_min_paket=V_min_p, V_maks_paket=V_maks_p, tepe_akim_paket_A=I_tepe,
        tab_akim_yogunlugu_surekli_A_mm2=j_tab_surekli, hizli_sarj_min_T_C=T_kapi,
        kisa_devre_akimi_45C_kA=I_kd_45 / 1e3, kisa_devre_akimi_m10C_A=I_kd_m10, uyarilar=uyarilar,
    )


class _p_gecici:
    """maks_sarj_gucu_kW için PaketSonucu'nun gerektirdiği alanları taşıyan hafif nesne."""
    def __init__(self, h, n, seri, paralel):
        self.hucre, self.hucre_sayisi, self.seri, self.paralel = h, n, seri, paralel
