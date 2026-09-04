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
        ])


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

    return PaketSonucu(
        gereksinim=gereksinim, hucre=h, seri=seri, paralel=paralel, hucre_sayisi=n,
        gercek_enerji_kWh=E, kullanilabilir_enerji_kWh=E * gereksinim.kullanilabilir_soc_penceresi,
        nominal_gerilim_V=V_nom, paket_kutle_kg=paket_kutle, paket_hacim_L=paket_hacim,
        paket_wh_kg=E * 1e3 / paket_kutle, paket_wh_L=E * 1e3 / paket_hacim,
        bor_kg=h.bor_kg_per_kwh * E, na_kg=h.na_kg_per_kwh * E, v_kg=h.v_kg_per_kwh * E, li_kg=h.li_kg_per_kwh * E,
        maliyet_usd=maliyet, maliyet_usd_kWh=maliyet / E,
        surekli_akim_yogunlugu_mA_cm2=j_surekli, tepe_akim_yogunlugu_mA_cm2=j_tepe,
        isi_kaybi_W_per_K=UA, on_isitma_kWh_minus10_to_25=on_isitma_kWh,
    )
