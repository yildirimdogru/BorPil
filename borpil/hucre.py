"""
Katman yığını (stack) modeli: bir çift taraflı tekrar biriminden hücre düzeyinde
enerji yoğunluğu (Wh/kg, Wh/L), element bütçesi (bor, sodyum, vanadyum) ve malzeme
maliyeti hesaplar.

Tekrar birimi (çift taraflı katot):
    Al(katot) | katot kompozit | SE ayırıcı | Na anot | Al(anot) | Na anot | SE ayırıcı | katot kompozit
Bir sonraki birim yine Al(katot) ile başlar; dolayısıyla birim başına 1 katot folyosu,
1 anot folyosu, 2 katot, 2 SE, 2 anot katmanı düşer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import malzemeler as mz
from .elektrolit import alan_direnci_ohm_cm2, bruggeman_etkin_iletkenlik, iletkenlik_C
from .sabitler import kutle_kesri


@dataclass(frozen=True)
class KompozitRecete:
    """Kütle kesirleri (toplam 1.0) ve gözeneklilik."""
    aktif: float = 0.70
    elektrolit: float = 0.25
    karbon: float = 0.03
    baglayici: float = 0.02
    gozeneklilik: float = 0.08

    def __post_init__(self):
        toplam = self.aktif + self.elektrolit + self.karbon + self.baglayici
        if abs(toplam - 1.0) > 1e-6:
            raise ValueError(f"Kütle kesirleri 1.0 olmalı, {toplam:.4f} verildi")


@dataclass(frozen=True)
class HucreTasarimi:
    ad: str = "BorPil-A (Na | Na2(B12H12)(B10H10) | NVP)"
    katot: mz.Elektrot = mz.NVP
    katot_recete: KompozitRecete = field(default_factory=KompozitRecete)
    alan_kapasitesi_mAh_cm2: float = 3.0       # tek yüz, katot pratik kapasitesine göre
    elektrolit: mz.KatiElektrolit = mz.NA2_B12_B10
    ayirici_kalinlik_um: float = 30.0
    anot: mz.Elektrot = mz.NA_METAL
    anot_fazlasi_um: float = 20.0              # Na metal için başlangıç fazlası (anotsuz tasarımda 0)
    anot_recete: KompozitRecete = field(default_factory=lambda: KompozitRecete(0.68, 0.27, 0.03, 0.02, 0.08))
    np_orani: float = 1.10                     # sert karbon anot için N/P
    katot_folyo: mz.Folyo = mz.AL_FOLYO
    anot_folyo: mz.Folyo = mz.AL_FOLYO
    pouch_en_mm: float = 100.0
    pouch_boy_mm: float = 300.0
    kilif_g_cm2: float = 0.018                 # Al-laminat kılıf, tek yüz
    kilif_kalinlik_um: float = 150.0
    tab_kutle_orani: float = 0.02              # hücre kütlesine oranla tab/izolasyon
    calisma_sicakligi_C: float = 45.0
    arayuz_direnci_ohm_cm2: float = 15.0       # katot/SE + Na/SE arayüz ASR toplamı (ölçekli hedef)


@dataclass
class KatmanSonucu:
    ad: str
    kalinlik_um: float
    kutle_mg_cm2: float
    bor_mg_cm2: float = 0.0
    maliyet_usd_m2: float = 0.0


def _kompozit_yogunluk(recete: KompozitRecete, aktif: mz.Elektrot, se: mz.KatiElektrolit) -> float:
    hacim_g = (recete.aktif / aktif.yogunluk + recete.elektrolit / se.yogunluk
               + recete.karbon / mz.KARBON_ILETKEN.yogunluk + recete.baglayici / mz.BAGLAYICI.yogunluk)
    return (1.0 - recete.gozeneklilik) / hacim_g


def _kompozit_katman(ad: str, recete: KompozitRecete, aktif: mz.Elektrot, se: mz.KatiElektrolit,
                     aktif_mg_cm2: float) -> KatmanSonucu:
    toplam_mg = aktif_mg_cm2 / recete.aktif
    rho = _kompozit_yogunluk(recete, aktif, se)
    kalinlik_um = toplam_mg * 1e-3 / rho * 1e4
    se_mg = toplam_mg * recete.elektrolit
    bor = se_mg * se.bor_kesri() + aktif_mg_cm2 * aktif.bor_kesri()
    maliyet = (aktif_mg_cm2 * aktif.maliyet_usd_kg + se_mg * se.maliyet_usd_kg
               + toplam_mg * recete.karbon * mz.KARBON_ILETKEN.maliyet_usd_kg
               + toplam_mg * recete.baglayici * mz.BAGLAYICI.maliyet_usd_kg) * 1e-6 * 1e4  # mg/cm² → kg/m²
    return KatmanSonucu(ad, kalinlik_um, toplam_mg, bor, maliyet)


@dataclass
class HucreSonucu:
    tasarim: HucreTasarimi
    katmanlar: list[KatmanSonucu]
    tekrar_kalinlik_um: float
    tekrar_kutle_mg_cm2: float
    tekrar_kapasite_mAh_cm2: float
    gerilim_V: float
    stack_wh_kg: float
    stack_wh_L: float
    hucre_wh_kg: float
    hucre_wh_L: float
    hucre_kapasite_Ah: float
    hucre_kutle_kg: float
    hucre_hacim_L: float
    katman_sayisi: int
    bor_kg_per_kwh: float
    na_kg_per_kwh: float
    v_kg_per_kwh: float
    li_kg_per_kwh: float
    malzeme_usd_per_kwh: float
    asr_toplam_ohm_cm2: float
    sigma_S_cm: float
    elektrot_alani_cm2: float          # hücre başına toplam tek-yüz katot alanı
    uyarilar: list[str]

    def ozet(self) -> str:
        t = self.tasarim
        satirlar = [
            f"== {t.ad} ==",
            f"Katot: {t.katot.ad} | SE: {t.elektrolit.ad} | Anot: {t.anot.ad}",
            f"Çalışma sıcaklığı {t.calisma_sicakligi_C:.0f} °C → σ = {self.sigma_S_cm*1e3:.2f} mS/cm, "
            f"toplam ASR ≈ {self.asr_toplam_ohm_cm2:.1f} Ω·cm²",
            "Katmanlar (tekrar birimi):",
        ]
        for k in self.katmanlar:
            satirlar.append(f"  - {k.ad:<28s} {k.kalinlik_um:7.1f} µm  {k.kutle_mg_cm2:7.2f} mg/cm²")
        satirlar += [
            f"Tekrar birimi: {self.tekrar_kalinlik_um:.0f} µm, {self.tekrar_kutle_mg_cm2:.1f} mg/cm², "
            f"{self.tekrar_kapasite_mAh_cm2:.1f} mAh/cm², {self.gerilim_V:.2f} V",
            f"Yığın: {self.stack_wh_kg:.0f} Wh/kg, {self.stack_wh_L:.0f} Wh/L",
            f"Hücre ({t.pouch_en_mm:.0f}×{t.pouch_boy_mm:.0f} mm pouch, {self.katman_sayisi} birim): "
            f"{self.hucre_kapasite_Ah:.1f} Ah, {self.hucre_kutle_kg*1e3:.0f} g, {self.hucre_hacim_L*1e3:.0f} mL "
            f"→ {self.hucre_wh_kg:.0f} Wh/kg, {self.hucre_wh_L:.0f} Wh/L",
            f"Element bütçesi: B {self.bor_kg_per_kwh:.2f} kg/kWh, Na {self.na_kg_per_kwh:.2f} kg/kWh, "
            f"V {self.v_kg_per_kwh:.2f} kg/kWh, Li {self.li_kg_per_kwh:.2f} kg/kWh",
            f"Malzeme maliyeti (varsayımsal ölçek): {self.malzeme_usd_per_kwh:.0f} USD/kWh",
        ]
        satirlar += [f"  ! {u}" for u in self.uyarilar]
        return "\n".join(satirlar)


def hesapla(t: HucreTasarimi, hedef_kapasite_Ah: float = 60.0) -> HucreSonucu:
    se = t.elektrolit
    katot = t.katot
    q_c = t.alan_kapasitesi_mAh_cm2

    # --- Katot kompozit (tek yüz)
    katot_aktif_mg = q_c / katot.kapasite_pratik * 1e3
    kat = _kompozit_katman("Katot kompozit", t.katot_recete, katot, se, katot_aktif_mg)

    # --- Ayırıcı
    se_mg = t.ayirici_kalinlik_um * 1e-4 * se.yogunluk * 1e3
    ayirici = KatmanSonucu("SE ayırıcı", t.ayirici_kalinlik_um, se_mg, se_mg * se.bor_kesri(),
                           se_mg * 1e-6 * 1e4 * se.maliyet_usd_kg)

    # --- Anot (tek yüz)
    if t.anot.rol != "anot":
        raise ValueError("anot rolü 'anot' olmalı")
    metalik = t.anot.metalik
    if metalik:
        # Kütle korunumu: döngüye giren Na zaten katot formülünde (Na3V2(PO4)3, deşarjlı hâl)
        # sayılmıştır; anot kütlesine yalnız fazlalık eklenir. Kalınlık için şarjlı (maksimum) hâl alınır.
        kaplanan_mg = q_c / t.anot.kapasite_pratik * 1e3
        fazla_mg = t.anot_fazlasi_um * 1e-4 * t.anot.yogunluk * 1e3
        kalinlik = (kaplanan_mg + fazla_mg) * 1e-3 / t.anot.yogunluk * 1e4
        anot = KatmanSonucu(f"{t.anot.ad} anot (fazlalık; şarjlı kalınlık)", kalinlik, fazla_mg, 0.0,
                            fazla_mg * 1e-6 * 1e4 * t.anot.maliyet_usd_kg)
        anot_potansiyel = t.anot.potansiyel_ort
    else:
        aktif_mg = q_c * t.np_orani / t.anot.kapasite_pratik * 1e3
        anot = _kompozit_katman(f"{t.anot.ad} kompozit anot", t.anot_recete, t.anot, se, aktif_mg)
        anot_potansiyel = t.anot.potansiyel_ort

    # --- Folyolar
    def folyo(f: mz.Folyo, ad: str) -> KatmanSonucu:
        mg = f.kalinlik_um * 1e-4 * f.yogunluk * 1e3
        return KatmanSonucu(ad, f.kalinlik_um, mg, 0.0, mg * 1e-6 * 1e4 * f.maliyet_usd_kg)

    fk = folyo(t.katot_folyo, f"{t.katot_folyo.ad} (katot)")
    fa = folyo(t.anot_folyo, f"{t.anot_folyo.ad} (anot)")

    katmanlar = [fk, kat, ayirici, anot, fa, anot, ayirici, kat]
    tekrar_kalinlik = sum(k.kalinlik_um for k in katmanlar)
    tekrar_kutle = sum(k.kutle_mg_cm2 for k in katmanlar)
    tekrar_bor = sum(k.bor_mg_cm2 for k in katmanlar)
    tekrar_maliyet = sum(k.maliyet_usd_m2 for k in katmanlar)
    tekrar_kapasite = 2 * q_c
    V = katot.potansiyel_ort - anot_potansiyel
    enerji_mWh_cm2 = tekrar_kapasite * V

    stack_wh_kg = enerji_mWh_cm2 / tekrar_kutle * 1e3          # mWh/mg → Wh/kg
    stack_wh_L = enerji_mWh_cm2 / (tekrar_kalinlik * 1e-4) * 1e-3 * 1e3  # mWh/cm³ → Wh/L

    # --- Hücre (pouch)
    alan_cm2 = t.pouch_en_mm * t.pouch_boy_mm / 100.0
    n = max(1, round(hedef_kapasite_Ah * 1e3 / (tekrar_kapasite * alan_cm2)))
    kapasite_Ah = n * tekrar_kapasite * alan_cm2 / 1e3
    yigin_kutle_g = n * tekrar_kutle * alan_cm2 * 1e-3
    kilif_g = 2 * t.kilif_g_cm2 * alan_cm2 * 1.15   # %15 kenar payı
    hucre_kutle_g = (yigin_kutle_g + kilif_g) / (1.0 - t.tab_kutle_orani)
    hucre_kalinlik_mm = (n * tekrar_kalinlik + 2 * t.kilif_kalinlik_um) / 1e3
    hucre_hacim_L = alan_cm2 * 1.10 * hucre_kalinlik_mm * 0.1 / 1e3  # %10 kenar/tab hacmi
    enerji_Wh = kapasite_Ah * V

    # --- Element bütçesi (kg/kWh)
    def element_kg_per_kwh(el: str) -> float:
        mg = 0.0
        # aktif katot
        mg += 2 * katot_aktif_mg * kutle_kesri(katot.formul, el)
        # SE (ayırıcı + kompozitlerdeki)
        se_toplam_mg = 2 * se_mg + 2 * kat.kutle_mg_cm2 * t.katot_recete.elektrolit
        if not metalik:
            se_toplam_mg += 2 * anot.kutle_mg_cm2 * t.anot_recete.elektrolit
        mg += se_toplam_mg * kutle_kesri(se.formul, el)
        # anot (metalikte yalnız fazlalık; döngüsel Na katot formülünde sayılı)
        if metalik:
            mg += 2 * anot.kutle_mg_cm2 * kutle_kesri(t.anot.formul, el)
        else:
            mg += 2 * anot.kutle_mg_cm2 * t.anot_recete.aktif * kutle_kesri(t.anot.formul, el)
        return mg / enerji_mWh_cm2  # mg/mWh = kg/kWh

    # --- Direnç
    sigma = float(iletkenlik_C(se, t.calisma_sicakligi_C))
    asr_ayirici = alan_direnci_ohm_cm2(se, t.ayirici_kalinlik_um, t.calisma_sicakligi_C)
    se_hacim_kesri = (t.katot_recete.elektrolit / se.yogunluk) / (
        t.katot_recete.aktif / katot.yogunluk + t.katot_recete.elektrolit / se.yogunluk
        + t.katot_recete.karbon / mz.KARBON_ILETKEN.yogunluk + t.katot_recete.baglayici / mz.BAGLAYICI.yogunluk
    ) * (1 - t.katot_recete.gozeneklilik)
    sigma_eff = bruggeman_etkin_iletkenlik(sigma, se_hacim_kesri)
    # kompozit katotta iyonik yol ~ kalınlığın yarısı (dağıtılmış reaksiyon)
    asr_katot = (kat.kalinlik_um * 1e-4 / 2) / sigma_eff
    asr_toplam = asr_ayirici + asr_katot + t.arayuz_direnci_ohm_cm2

    # --- Kararlılık penceresi kontrolü (şarj kesim potansiyeli ≈ ortalama + 0.4 V)
    uyarilar: list[str] = []
    kesim_V = katot.potansiyel_ort + 0.4
    if kesim_V > se.oksidasyon_pasif_V:
        uyarilar.append(f"KRİTİK: katot kesim potansiyeli ~{kesim_V:.1f} V, elektrolitin pasifleşmeyle "
                        f"ulaştığı sınırı ({se.oksidasyon_pasif_V:.1f} V) aşıyor.")
    elif kesim_V > se.oksidasyon_siniri_V:
        uyarilar.append(f"UYARI: katot kesim potansiyeli ~{kesim_V:.1f} V termodinamik oksidasyon sınırının "
                        f"({se.oksidasyon_siniri_V:.1f} V) üstünde; çalışma pasifleştirici arayüze (kaplama) dayanır.")
    if metalik and t.anot is mz.MG_METAL:
        uyarilar.append("KRİTİK: Mg anot Na⁺ iletken kloso-borat ile uyumsuz; yalnız Mg elektrolitli hücrede anlamlı.")

    return HucreSonucu(
        tasarim=t,
        katmanlar=katmanlar,
        tekrar_kalinlik_um=tekrar_kalinlik,
        tekrar_kutle_mg_cm2=tekrar_kutle,
        tekrar_kapasite_mAh_cm2=tekrar_kapasite,
        gerilim_V=V,
        stack_wh_kg=stack_wh_kg,
        stack_wh_L=stack_wh_L,
        hucre_wh_kg=enerji_Wh / (hucre_kutle_g / 1e3),
        hucre_wh_L=enerji_Wh / hucre_hacim_L,
        hucre_kapasite_Ah=kapasite_Ah,
        hucre_kutle_kg=hucre_kutle_g / 1e3,
        hucre_hacim_L=hucre_hacim_L,
        katman_sayisi=n,
        bor_kg_per_kwh=tekrar_bor / enerji_mWh_cm2,
        na_kg_per_kwh=element_kg_per_kwh("Na"),
        v_kg_per_kwh=element_kg_per_kwh("V"),
        li_kg_per_kwh=element_kg_per_kwh("Li"),
        malzeme_usd_per_kwh=tekrar_maliyet / (enerji_mWh_cm2 * 1e-3 * 1e4) * 1e3,  # USD/m² ÷ Wh/m² → USD/Wh → USD/kWh
        asr_toplam_ohm_cm2=asr_toplam,
        sigma_S_cm=sigma,
        elektrot_alani_cm2=alan_cm2 * 2 * n,
        uyarilar=uyarilar,
    )


# ---------------------------------------------------------------------------
# Hazır tasarım varyantları
# ---------------------------------------------------------------------------

BORPIL_A = HucreTasarimi()  # temel: Na | B12/B10 | NVP, 45 °C

BORPIL_A_MUHAFAZAKAR = HucreTasarimi(
    ad="BorPil-A0 (Na | Na2(B12H12)(B10H10) | NaCrO2) — pencere içi muhafazakâr",
    katot=mz.NACRO2,
)

BORPIL_B = HucreTasarimi(
    ad="BorPil-B (Na | Na2(CB9H10)(CB11H12) | NVPF) — 2. nesil yüksek performans",
    katot=mz.NVPF,
    elektrolit=mz.NA2_CB9_CB11,
    ayirici_kalinlik_um=20.0,
    alan_kapasitesi_mAh_cm2=4.0,
    anot_fazlasi_um=10.0,
    calisma_sicakligi_C=35.0,
    arayuz_direnci_ohm_cm2=8.0,
)

BORPIL_C = HucreTasarimi(
    ad="BorPil-C (Sert karbon | Na2(B12H12)(B10H10) | NVP) — dendritsiz güvenli varyant",
    anot=mz.SERT_KARBON,
)

BORPIL_S = HucreTasarimi(
    ad="BorPil-S (Na | Na2(CB9H10)(CB11H12) | S) — uzun vade Na-S",
    katot=mz.KUKURT,
    katot_recete=KompozitRecete(0.50, 0.35, 0.13, 0.02, 0.15),
    elektrolit=mz.NA2_CB9_CB11,
    ayirici_kalinlik_um=20.0,
    alan_kapasitesi_mAh_cm2=4.0,
    anot_fazlasi_um=10.0,
    calisma_sicakligi_C=60.0,
    arayuz_direnci_ohm_cm2=20.0,
)

BORPIL_A_ALT = HucreTasarimi(
    ad="BorPil-A-alt (Na | Na2(B12H12)(B10H10) | NVP) — muhafazakâr alt tahmin (60 µm SE, 50 µm Na, 30 Ω·cm²)",
    ayirici_kalinlik_um=60.0,
    anot_fazlasi_um=50.0,
    arayuz_direnci_ohm_cm2=30.0,
)

BORPIL_A_FE = HucreTasarimi(
    ad="BorPil-A-Fe (Na | Na2(B12H12)(B10H10) | Na2/3Fe1/2Mn1/2O2) — vanadyumsuz düşük maliyet",
    katot=mz.NA_FE_MN,
)

VARYANTLAR = {
    "A": BORPIL_A,
    "A-alt": BORPIL_A_ALT,
    "A0": BORPIL_A_MUHAFAZAKAR,
    "A-Fe": BORPIL_A_FE,
    "B": BORPIL_B,
    "C": BORPIL_C,
    "S": BORPIL_S,
}
