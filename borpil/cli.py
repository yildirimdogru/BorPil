"""Komut satırı arayüzü: `python -m borpil.cli ...` veya kurulu ise `borpil ...`."""

from __future__ import annotations

import argparse
import sys

from . import hucre as hc
from . import paket as pk
from . import rapor
from . import simulasyon as sm
from . import termodinamik as td


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="borpil", description="BorPil bor esaslı EV bataryası tasarım araçları")
    alt = p.add_subparsers(dest="komut", required=True)

    h = alt.add_parser("hucre", help="hücre yığın modeli özeti")
    h.add_argument("varyant", nargs="?", default="A", choices=list(hc.VARYANTLAR))
    h.add_argument("--ah", type=float, default=60.0, help="hedef hücre kapasitesi (Ah)")
    h.add_argument("--sicaklik", type=float, default=None, help="çalışma sıcaklığı (°C)")
    h.add_argument("--ayirici", type=float, default=None, help="SE ayırıcı kalınlığı (µm)")
    h.add_argument("--alan-kapasitesi", type=float, default=None, help="tek yüz alan kapasitesi (mAh/cm²)")

    pa = alt.add_parser("paket", help="EV paketi boyutlandırma")
    pa.add_argument("varyant", nargs="?", default="A", choices=list(hc.VARYANTLAR))
    pa.add_argument("--kwh", type=float, default=75.0)
    pa.add_argument("--volt", type=float, default=400.0)

    su = alt.add_parser("surus", help="sürüş çevrimi / menzil simülasyonu")
    su.add_argument("varyant", nargs="?", default="A", choices=list(hc.VARYANTLAR))
    su.add_argument("--kwh", type=float, default=75.0)
    su.add_argument("--ortam", type=float, default=20.0, help="ortam sıcaklığı (°C)")
    su.add_argument("--isitici", type=float, default=None, help="ısıtıcı hedef sıcaklığı (°C); yoksa kapalı")

    alt.add_parser("termo", help="teorik termodinamik sınırlar")

    r = alt.add_parser("rapor", help="tam rapor + grafikler üret")
    r.add_argument("--cikti", default="cikti")
    r.add_argument("--grafiksiz", action="store_true")

    a = p.parse_args(argv)

    if a.komut == "hucre":
        import dataclasses
        t = hc.VARYANTLAR[a.varyant]
        degisiklik = {}
        if a.sicaklik is not None:
            degisiklik["calisma_sicakligi_C"] = a.sicaklik
        if a.ayirici is not None:
            degisiklik["ayirici_kalinlik_um"] = a.ayirici
        if a.alan_kapasitesi is not None:
            degisiklik["alan_kapasitesi_mAh_cm2"] = a.alan_kapasitesi
        t = dataclasses.replace(t, **degisiklik)
        print(hc.hesapla(t, hedef_kapasite_Ah=a.ah).ozet())
    elif a.komut == "paket":
        g = pk.PaketGereksinimi(brut_enerji_kWh=a.kwh, nominal_gerilim_V=a.volt)
        print(pk.boyutlandir(hc.VARYANTLAR[a.varyant], g).ozet())
    elif a.komut == "surus":
        g = pk.PaketGereksinimi(brut_enerji_kWh=a.kwh)
        pkt = pk.boyutlandir(hc.VARYANTLAR[a.varyant], g)
        s = sm.surus_simulasyonu(pkt, T_ortam_C=a.ortam, isitici_hedef_C=a.isitici)
        print(f"Menzil {s.menzil_km:.0f} km, tüketim {s.tuketim_kWh_100km:.1f} kWh/100 km, "
              f"paket T {s.T_baslangic_C:.0f}→{s.T_bitis_C:.0f} °C, min hücre gerilimi {s.V_min_hucre:.2f} V, "
              f"araç kütlesi {s.toplam_kutle_kg:.0f} kg")
    elif a.komut == "termo":
        for k in td.metal_hava_kiyas() + [td.dbfc()]:
            print(f"{k.ad:<40s} {k.reaksiyon:<22s} E°={k.E0_V:.3f} V  {k.kapasite_mah_g:6.0f} mAh/g  "
                  f"{k.enerji_wh_kg_reaktan:6.0f} Wh/kg (reaktan)  {k.enerji_wh_kg_urun:5.0f} Wh/kg (ürün)")
        d = td.dbfc_gidis_donus()
        print(f"DBFC gidiş-dönüş verimi: %{d['gidis_donus_verimi']*100:.0f}")
    elif a.komut == "rapor":
        yol = rapor.uret(a.cikti, grafikler=not a.grafiksiz)
        print(f"Rapor yazıldı: {yol}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
