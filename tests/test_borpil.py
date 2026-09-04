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


def test_dbfc_menzil_uzatici_tutarli():
    m = td.dbfc_menzil_uzatici(cozelti_kutle_kg=40, tuketim_kWh_100km=15)
    assert m["nabh4_kg"] == pytest.approx(8.0)
    assert m["ek_menzil_km"] == pytest.approx(m["enerji_kWh"] / 15 * 100)
    assert 100 < m["sistem_wh_kg"] < 400


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
    for se in (mz.NA2B10H10, mz.NA2B12H12):
        alt = float(el.iletkenlik(se, se.T_gecis - 1))
        ust = float(el.iletkenlik(se, se.T_gecis + 1))
        assert ust / alt > 30, se.ad
    # Na2B12H12 düzenli fazı oda sıcaklığında yalıtkan (< 1e-9 S/cm)
    assert float(el.iletkenlik_C(mz.NA2B12H12, 25)) < 1e-9


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
    # ikosahedron çevrel yarıçapı: a·√(φ√5)/2 = a·0.9511 (altın oran özdeşliği ile bağımsız kontrol)
    phi = (1 + 5**0.5) / 2
    assert g.cevrel_yaricap_B_A == pytest.approx(1.78 * math.sqrt(phi * 5**0.5) / 2, abs=1e-9)
    assert g.cevrel_yaricap_H_A == pytest.approx(g.cevrel_yaricap_B_A + 1.20)
    assert 3.5 < g.etkin_yaricap_A < 4.5


def test_na_bosluk_analizi_makul():
    b = ge.na_bosluk_analizi()
    assert b["kafes_a_A"] == pytest.approx(7.9)
    assert b["na_site_doluluk"] == pytest.approx(1 / 3)
    # 12d tetrahedral site boşluğu Na+ yarıçapıyla (1.02 Å) uyumlu olmalı
    assert 0.9 < b["tetrahedral_bosluk_yaricap_A"] < 1.1
    # yoğunluktan türetilen (oda sıcaklığı) kafes, yüksek-T ölçümünden ~%15 hacim küçük
    b_rho = ge.na_bosluk_analizi(mz.NA2B12H12.yogunluk, mz.NA2B12H12.molar_kutle, a_bcc_A=None)
    assert 0.80 < (b_rho["kafes_a_A"] / 7.9) ** 3 < 0.95


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


def test_kutle_dengesi_bagimsiz_el_hesabi():
    """Hakem el hesabı (BorPil-A): katot 27.27/38.96 mg/cm², SE 4.50, Na fazlası 1.94, Al 3.24 ×2."""
    h = hc.hesapla(hc.BORPIL_A)
    katot = 3.0 / 110.0 * 1e3 / 0.70
    se = 30e-4 * 1.50 * 1e3
    na_fazla = 20e-4 * 0.97 * 1e3
    al = 12e-4 * 2.70 * 1e3
    beklenen = 2 * (katot + se + na_fazla) + 2 * al
    assert h.tekrar_kutle_mg_cm2 == pytest.approx(beklenen, rel=1e-6)
    assert h.stack_wh_kg == pytest.approx(6.0 * 3.37 / beklenen * 1e3, rel=1e-6)


def test_na_cift_sayim_yok():
    """Döngüye giren Na katot formülünde sayılır; anot kütlesi yalnız fazlalık Na'dır (kütle korunumu)."""
    h = hc.hesapla(hc.BORPIL_A)
    anot = [k for k in h.katmanlar if "Na metal" in k.ad][0]
    assert anot.kutle_mg_cm2 == pytest.approx(20e-4 * 0.97 * 1e3)
    # kalınlık ise şarjlı hâl: fazlalık + kaplanan (3 mAh/cm² / 1166 mAh/g / 0.97 g/cm³)
    assert anot.kalinlik_um == pytest.approx(20 + 3.0 / 1166 / 0.97 * 1e4, rel=1e-3)
    sifir_fazla = hc.hesapla(dataclasses.replace(hc.BORPIL_A, anot_fazlasi_um=0.0))
    assert sifir_fazla.na_kg_per_kwh < h.na_kg_per_kwh


def test_replace_edilmis_na_anot_metalik_kalir():
    """Kimlik (is) yerine `metalik` alanı kullanılır; dataclasses.replace edilmiş Na anot kompozit dala düşmez."""
    na2 = dataclasses.replace(mz.NA_METAL, maliyet_usd_kg=3.5)
    h = hc.hesapla(dataclasses.replace(hc.BORPIL_A, anot=na2))
    assert all("kompozit anot" not in k.ad for k in h.katmanlar)
    assert h.hucre_wh_kg == pytest.approx(hc.hesapla(hc.BORPIL_A).hucre_wh_kg, rel=1e-6)


def test_oksidasyon_uyarisi():
    assert any("oksidasyon" in u for u in hc.hesapla(hc.BORPIL_A).uyarilar)       # NVP 3.37 V > 3.0 V
    assert not any("KRİTİK" in u for u in hc.hesapla(hc.BORPIL_A).uyarilar)
    assert hc.hesapla(hc.BORPIL_A_MUHAFAZAKAR).uyarilar[0].startswith("UYARI")     # NaCrO2 kesim 3.35 V
    mg = dataclasses.replace(hc.BORPIL_A, anot=mz.MG_METAL)
    assert any("KRİTİK" in u for u in hc.hesapla(mg).uyarilar)


def test_malzeme_hashlenebilir():
    assert len({mz.NVP, mz.NACRO2, mz.NA2_B12_B10}) == 3


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


def test_akim_yogunlugu_bagimsiz_hesap():
    """Hücre akımı = I_paket/paralel; hücre alanı = 2 × katman × pouch alanı."""
    p = pk.boyutlandir(hc.BORPIL_A)
    I_paket = p.gereksinim.surekli_guc_kW * 1e3 / p.nominal_gerilim_V
    I_hucre = I_paket / p.paralel
    alan_hucre = 2 * p.hucre.katman_sayisi * (100 * 300 / 100.0)
    assert p.surekli_akim_yogunlugu_mA_cm2 == pytest.approx(I_hucre / alan_hucre * 1e3, rel=1e-9)
    # ~1C sürekli güçte j, alan kapasitesi (3 mAh/cm²) mertebesinde
    assert 2.0 < p.surekli_akim_yogunlugu_mA_cm2 < 4.5


# --- Simülasyon -----------------------------------------------------------------

def test_ocv_monoton_ve_ortalamasi_nominal():
    s = np.linspace(0, 1, 100001)
    V = sm.ocv(s, 3.37)
    assert np.all(np.diff(V) > 0)
    assert float(np.trapezoid(V, s)) == pytest.approx(3.37, abs=1e-4)   # enerji tutarlılığı
    assert V[0] < 3.1 and V[-1] > 3.5


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
    # 70 °C'de j tavanı (12 mA/cm²) devrede: P ≤ tavan akımı × OCV × hücre sayısı
    I_tavan = 12.0 * p.hucre.elektrot_alani_cm2 / 1e3
    assert P[-1] <= I_tavan * float(sm.ocv(0.5, p.hucre.gerilim_V)) * p.hucre_sayisi / 1e3
    assert P[-1] > 0.8 * I_tavan * sm.v_min_hucre(p.hucre) * p.hucre_sayisi / 1e3


def test_cevrim_wltp_benzeri():
    t, v = sm.wltp_benzeri_cevrim()
    mesafe = np.trapezoid(v, t) / 1e3
    assert 1700 < t[-1] < 1900
    assert 22 < mesafe < 26
    assert v.max() * 3.6 == pytest.approx(131, abs=1)


def test_surus_menzil_makul_ve_enerji_tutarli():
    p = pk.boyutlandir(hc.BORPIL_A)
    s = sm.surus_simulasyonu(p, T_ortam_C=20, isitici_hedef_C=None)
    assert 350 < s.menzil_km < 600
    assert 12 < s.tuketim_kWh_100km < 20
    assert s.T_bitis_C > s.T_baslangic_C  # I²R ile kendi kendine ısınma
    assert s.guc_kisiti_s == 0
    # Enerji dengesi: kullanılan (E·Δsoc) = uç enerjisi + I²R kaybı (±%1)
    kullanilan = p.gercek_enerji_kWh * p.gereksinim.kullanilabilir_soc_penceresi
    assert s.terminal_enerji_kWh < kullanilan
    assert (kullanilan - s.terminal_enerji_kWh) / kullanilan < 0.06
    soguk = sm.surus_simulasyonu(p, T_ortam_C=-10, isitici_hedef_C=35, isitici_guc_kW=6)
    assert soguk.menzil_km < s.menzil_km
    assert soguk.isitici_kWh > 3.0
    assert soguk.V_min_hucre >= sm.v_min_hucre(p.hucre) - 1e-6


def test_soguk_guc_acigi_kaydedilir():
    p = pk.boyutlandir(hc.BORPIL_A)
    s = sm.surus_simulasyonu(p, T_ortam_C=-20, isitici_hedef_C=None)
    # Soğukta deşarj CCD sınırı devrede: çevrimin büyük kısmı kısıtlı, araç yavaşlar, rejen mekanik frene gider
    assert s.guc_kisiti_s > 0.2 * s.sure_h * 3600 and s.guc_acigi_kWh > 10
    assert s.ort_hiz_kmh < 46
    assert s.rejen_kaybi_kWh > 1.0


def test_akim_siniri_ortak_ve_yonlu():
    p = pk.boyutlandir(hc.BORPIL_A)
    h = p.hucre
    I_d = sm.akim_siniri_A(h, 25, "desarj")
    I_s = sm.akim_siniri_A(h, 25, "sarj")
    j = 1.5 * h.elektrot_alani_cm2 / 1e3
    assert I_d == pytest.approx(j * sm.DESARJ_TOLERANSI)
    assert I_s == pytest.approx(j / sm.SARJ_GUVENLIK_KATSAYISI)
    # tepe güç fonksiyonu ile sürüş simülasyonu aynı sınırı kullanır: −10 °C'de tepe güç < 10 kW
    assert sm.maks_guc_kW(p, -10) < 10
    assert sm.maks_sarj_gucu_kW(p, 45) >= 75 > sm.maks_sarj_gucu_kW(p, 35)


def test_sarj_simulasyonu_tutarli():
    p = pk.boyutlandir(hc.BORPIL_A)
    s45 = sm.sarj_simulasyonu(p, T_baslangic_C=45)
    s25 = sm.sarj_simulasyonu(p, T_baslangic_C=25)
    sm10 = sm.sarj_simulasyonu(p, T_baslangic_C=-10)
    assert s45.sure_dk < s25.sure_dk < sm10.sure_dk
    assert s45.enerji_hucre_kWh == pytest.approx(0.70 * p.gercek_enerji_kWh, rel=0.02)
    assert s45.enerji_sebeke_kWh > s45.enerji_hucre_kWh            # I²R + ısıtıcı
    assert s45.v_maks_hucre <= p.hucre.gerilim_V + 0.40 + 1e-6
    assert sm10.sinir_dagilimi["on_isitma"] > 0.2
    assert s45.T_bitis_C <= 61.0                                    # soğutma tavanı


def test_paket_elektrik_kontrolleri():
    p = pk.boyutlandir(hc.BORPIL_A)
    assert p.V_min_paket == pytest.approx(p.seri * sm.v_min_hucre(p.hucre))
    assert p.V_maks_paket < p.gereksinim.invertor_dc_link_maks_V
    assert p.tab_akim_yogunlugu_surekli_A_mm2 < 2.5
    assert 40 <= p.hizli_sarj_min_T_C <= 46
    assert p.kisa_devre_akimi_45C_kA > 5 and p.kisa_devre_akimi_m10C_A < 400
    g800 = pk.PaketGereksinimi(nominal_gerilim_V=800.0)
    assert any("KRİTİK" in u for u in pk.boyutlandir(hc.BORPIL_A, g800).uyarilar)


def test_dusuk_gerilimli_kimyada_guc_ve_desarj_calisir():
    p = pk.boyutlandir(hc.BORPIL_S)
    assert sm.maks_guc_kW(p, 60) > 0
    Ah, V = sm.sabit_akim_desarj(p.hucre, 0.5, 60)
    assert len(Ah) > 10


# --- Karşılaştırma --------------------------------------------------------------

def test_karsilastirma_tablosu():
    satirlar = ks.tablo(hc.VARYANTLAR)
    assert len(satirlar) == len(hc.VARYANTLAR) + len(mz.REFERANSLAR)
    bor = [s for s in satirlar if s.ad.startswith("BorPil")]
    assert all(s.li_kg == 0.0 and s.yanici == "hayır" for s in bor)
    md = ks.markdown_tablo(satirlar, 75)
    assert md.count("\n") == len(satirlar) + 2
