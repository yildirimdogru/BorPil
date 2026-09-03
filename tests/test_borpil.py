import dataclasses
import math

import numpy as np
import pytest

from borpil import elektrolit as el
from borpil import geometri as ge
from borpil import hucre as hc
from borpil import karsilastirma as ks
from borpil import malzemeler as mz
from borpil import paket as pk
from borpil import simulasyon as sm
from borpil import termodinamik as td
from borpil.sabitler import FARADAY_MAH, molar_kutle, teorik_kapasite_mah_g


# --- Sabitler / temel formüller -------------------------------------------------

def test_faraday_mah():
    assert FARADAY_MAH == pytest.approx(26801.5, rel=1e-4)


def test_teorik_kapasiteler_literatur():
    # Klasik referans değerler: Na metal 1166 mAh/g, NVP 117.6 mAh/g, S 1672 mAh/g
    assert mz.NA_METAL.kapasite_teorik == pytest.approx(1166, abs=1)
    assert mz.NVP.kapasite_teorik == pytest.approx(117.6, abs=0.3)
    assert mz.KUKURT.kapasite_teorik == pytest.approx(1672, abs=2)
    assert teorik_kapasite_mah_g(molar_kutle({"Li": 1}), 1) == pytest.approx(3861, abs=2)


def test_bor_kesri_na2b12h12():
    # 12·10.81 / 187.8 ≈ 0.69
    assert mz.NA2B12H12.bor_kesri() == pytest.approx(0.69, abs=0.01)
    assert mz.NVP.lityum_kesri() == 0.0


# --- Termodinamik ---------------------------------------------------------------

def test_dbfc_potansiyeli_literaturle_uyumlu():
    # Literatür: E° ≈ 1.64 V (BH4-/BO2- −1.24 V, O2/OH- +0.40 V)
    d = td.dbfc()
    assert d.E0_V == pytest.approx(1.64, abs=0.02)
    assert d.kapasite_mah_g == pytest.approx(5668, rel=0.01)


def test_bor_hava_teorik():
    b = td.bor_hava()
    assert b.E0_V == pytest.approx(2.06, abs=0.02)
    assert b.enerji_wh_kg_reaktan > 15000
    # Li-hava'dan (reaktan bazlı) daha yüksek, ürün bazlı daha düşük
    li = td.metal_hava_kiyas()[1]
    assert b.enerji_wh_kg_reaktan > li.enerji_wh_kg_reaktan
    assert b.enerji_wh_kg_urun < li.enerji_wh_kg_urun


def test_dbfc_gidis_donus_dusuk():
    r = td.dbfc_gidis_donus()
    assert 0.05 < r["gidis_donus_verimi"] < 0.30


def test_nernst_standart_kosul():
    assert td.nernst(1.0, 1, aktivite_orani=1.0) == pytest.approx(1.0)


# --- Elektrolit -----------------------------------------------------------------

def test_arrhenius_referans_noktasi():
    se = mz.NA2_B12_B10
    assert float(el.iletkenlik(se, se.T_ref)) == pytest.approx(se.sigma_ref)


def test_iletkenlik_sicaklikla_artar():
    T = np.array([250.0, 300.0, 350.0])
    s = el.iletkenlik(mz.NA2_B12_B10, T)
    assert np.all(np.diff(s) > 0)


def test_faz_gecisi_sicramasi():
    se = mz.NA2B10H10
    alt = float(el.iletkenlik(se, se.T_gecis - 1))
    ust = float(el.iletkenlik(se, se.T_gecis + 1))
    assert ust / alt > 100


def test_asr_kalinlikla_dogru_orantili():
    a = el.alan_direnci_ohm_cm2(mz.NA2_B12_B10, 30, 45)
    b = el.alan_direnci_ohm_cm2(mz.NA2_B12_B10, 60, 45)
    assert b == pytest.approx(2 * a)


def test_hedef_kalinlik_mekanik_alt_sinir():
    # 45 °C'de 3 mS/cm ile 10 Ω·cm² için gereken kalınlık 300 µm; mekanik sınır 20 µm'nin üstünde kalır
    k = el.hedef_kalinlik_um(mz.NA2_B12_B10, 45, hedef_asr_ohm_cm2=10.0)
    assert k > 20
    k2 = el.hedef_kalinlik_um(mz.NA2_CB9_CB11, 25, hedef_asr_ohm_cm2=0.01)
    assert k2 == 20.0


# --- Geometri -------------------------------------------------------------------

def test_ikosahedron_12_kose_30_kenar():
    v = ge.ikosahedron_koseleri()
    assert v.shape == (12, 3)
    d = np.linalg.norm(v[:, None, :] - v[None, :, :], axis=-1)
    kenar_sayisi = int(np.sum(np.abs(d - ge.B_B_BAG) < 1e-9) // 2)
    assert kenar_sayisi == 30
    # her köşenin 5 komşusu
    assert np.all(np.sum(np.abs(d - ge.B_B_BAG) < 1e-9, axis=1) == 5)


def test_b12h12_yaricap():
    g = ge.b12h12_geometrisi()
    assert g.cevrel_yaricap_B_A == pytest.approx(1.78 * math.sin(2 * math.pi / 5), abs=1e-9)
    assert 3.5 < g.etkin_yaricap_A < 4.5


def test_na_bosluk_analizi_makul():
    b = ge.na_bosluk_analizi(mz.NA2B12H12.yogunluk, mz.NA2B12H12.molar_kutle)
    assert 7.0 < b["kafes_a_A"] < 8.0
    assert b["na_site_doluluk"] == pytest.approx(1 / 3)
    assert 0.6 < b["anyon_hacim_kesri_sert"] < 0.7   # bcc sert küre paketleme = 0.68


def test_pouch_boyutlandir():
    g = ge.pouch_boyutlandir(60.0, 6.0, 536.0)
    assert g.katman_sayisi == 34
    assert 18 < g.kalinlik_mm < 20
    assert ge.kutu_icine_paketle(g, (2000, 1400, 120)) > 100


# --- Hücre ----------------------------------------------------------------------

def test_kompozit_recete_toplam_kontrolu():
    with pytest.raises(ValueError):
        hc.KompozitRecete(0.5, 0.5, 0.1, 0.0)


def test_hucre_temel_tasarim_araligi():
    h = hc.hesapla(hc.BORPIL_A)
    assert 170 < h.hucre_wh_kg < 220
    assert 300 < h.hucre_wh_L < 400
    assert h.li_kg_per_kwh == 0.0
    assert 0.8 < h.bor_kg_per_kwh < 1.2
    assert h.gerilim_V == pytest.approx(3.37)
    assert h.tekrar_kapasite_mAh_cm2 == pytest.approx(6.0)


def test_kutle_dengesi_katmanlar():
    h = hc.hesapla(hc.BORPIL_A)
    assert sum(k.kutle_mg_cm2 for k in h.katmanlar) == pytest.approx(h.tekrar_kutle_mg_cm2)
    assert sum(k.kalinlik_um for k in h.katmanlar) == pytest.approx(h.tekrar_kalinlik_um)


def test_incelme_enerji_yogunlugunu_artirir():
    kalin = hc.hesapla(dataclasses.replace(hc.BORPIL_A, ayirici_kalinlik_um=80))
    ince = hc.hesapla(dataclasses.replace(hc.BORPIL_A, ayirici_kalinlik_um=20))
    assert ince.hucre_wh_kg > kalin.hucre_wh_kg
    assert ince.hucre_wh_L > kalin.hucre_wh_L


def test_sert_karbon_varyanti_dusuk_enerji():
    a = hc.hesapla(hc.BORPIL_A)
    c = hc.hesapla(hc.BORPIL_C)
    assert c.hucre_wh_kg < a.hucre_wh_kg
    assert c.gerilim_V == pytest.approx(3.37 - 0.20)


def test_stack_hucreden_buyuk():
    for t in hc.VARYANTLAR.values():
        h = hc.hesapla(t)
        assert h.stack_wh_kg > h.hucre_wh_kg
        assert h.stack_wh_L > h.hucre_wh_L


# --- Paket ----------------------------------------------------------------------

def test_paket_hedef_enerjiyi_tutturur():
    p = pk.boyutlandir(hc.BORPIL_A)
    assert p.gercek_enerji_kWh == pytest.approx(75.0, rel=0.02)
    assert abs(p.nominal_gerilim_V - 400) < 5
    assert p.hucre_sayisi == p.seri * p.paralel
    assert p.li_kg == 0.0
    assert 50 < p.bor_kg < 100


def test_paket_800V():
    g = pk.PaketGereksinimi(nominal_gerilim_V=800.0)
    p = pk.boyutlandir(hc.BORPIL_A, g)
    assert abs(p.nominal_gerilim_V - 800) < 5
    assert p.seri > 200


def test_akim_yogunlugu_olcekleme():
    p = pk.boyutlandir(hc.BORPIL_A)
    # 1C'ye yakın sürekli güçte j ≈ alan kapasitesi (3 mAh/cm²) mertebesinde olmalı
    assert 2.0 < p.surekli_akim_yogunlugu_mA_cm2 < 4.5
    assert p.tepe_akim_yogunlugu_mA_cm2 == pytest.approx(
        p.surekli_akim_yogunlugu_mA_cm2 * p.gereksinim.tepe_guc_kW / p.gereksinim.surekli_guc_kW)


# --- Simülasyon -----------------------------------------------------------------

def test_ocv_monoton_ve_aralikta():
    s = np.linspace(0, 1, 101)
    V = sm.ocv(s, 3.37)
    assert np.all(np.diff(V) > 0)
    assert 2.7 < V[0] < 3.2 and 3.4 < V[-1] < 3.6


def test_direnc_sogukta_artar():
    p = pk.boyutlandir(hc.BORPIL_A)
    assert sm.hucre_direnci_ohm(p.hucre, -10) > sm.hucre_direnci_ohm(p.hucre, 25) > sm.hucre_direnci_ohm(p.hucre, 60)


def test_asr_referans_sicaklikta_tutarli():
    h = hc.hesapla(hc.BORPIL_A)
    assert sm.asr_sicaklik(h, h.tasarim.calisma_sicakligi_C) == pytest.approx(h.asr_toplam_ohm_cm2, rel=1e-6)


def test_maks_guc_sicaklikla_artar_ve_tavanlanir():
    p = pk.boyutlandir(hc.BORPIL_A)
    P = [sm.maks_guc_kW(p, T) for T in (-10, 10, 30, 50, 70)]
    assert all(b >= a for a, b in zip(P, P[1:]))
    assert P[-1] < 400  # kritik akım tavanı devrede


def test_cevrim_wltp_benzeri():
    t, v = sm.wltp_benzeri_cevrim()
    mesafe = np.trapezoid(v, t) / 1e3
    assert 1700 < t[-1] < 1900
    assert 22 < mesafe < 26
    assert v.max() * 3.6 == pytest.approx(131, abs=1)


def test_surus_menzil_makul():
    p = pk.boyutlandir(hc.BORPIL_A)
    s = sm.surus_simulasyonu(p, T_ortam_C=20, isitici_hedef_C=None)
    assert 350 < s.menzil_km < 600
    assert 12 < s.tuketim_kWh_100km < 20
    assert s.T_bitis_C > s.T_baslangic_C  # I²R ile kendi kendine ısınma
    soguk = sm.surus_simulasyonu(p, T_ortam_C=-10, isitici_hedef_C=25, isitici_guc_kW=6)
    assert soguk.menzil_km < s.menzil_km
    assert soguk.V_min_hucre > 2.0


# --- Karşılaştırma --------------------------------------------------------------

def test_karsilastirma_tablosu():
    satirlar = ks.tablo(hc.VARYANTLAR)
    assert len(satirlar) == len(hc.VARYANTLAR) + len(mz.REFERANSLAR)
    bor = [s for s in satirlar if s.ad.startswith("BorPil")]
    assert all(s.li_kg == 0.0 and s.yanici == "hayır" for s in bor)
    md = ks.markdown_tablo(satirlar, 75)
    assert md.count("\n") == len(satirlar) + 2
