"""BorPil varyantlarının Li-iyon referanslarıyla hücre ve paket düzeyinde karşılaştırılması."""

from __future__ import annotations

from dataclasses import dataclass

from . import malzemeler as mz
from .hucre import HucreTasarimi, hesapla
from .paket import PaketGereksinimi, boyutlandir


@dataclass
class Satir:
    ad: str
    wh_kg: float
    wh_L: float
    usd_kwh_hucre: float
    li_kg: float
    bor_kg: float
    co_kg: float
    ni_kg: float
    yanici: str
    paket_kutle_kg: float
    paket_hacim_L: float


def _li_referans_satiri(r: mz.ReferansHucre, g: PaketGereksinimi) -> Satir:
    E = g.brut_enerji_kWh
    hucre_kutle = E * 1e3 / r.wh_kg
    hucre_hacim = E * 1e3 / r.wh_L
    # Li-iyon paketlerde yanıcı elektrolit nedeniyle ek yangın bariyeri; hücre→paket kütle oranı ~0.72
    return Satir(r.ad, r.wh_kg, r.wh_L, r.usd_kwh, r.li_kg_per_kwh * E, 0.0, r.co_kg_per_kwh * E,
                 r.ni_kg_per_kwh * E, "evet" if r.yanici_elektrolit else "hayır",
                 hucre_kutle / 0.72, hucre_hacim / 0.60)


def tablo(varyantlar: dict[str, HucreTasarimi], g: PaketGereksinimi = PaketGereksinimi()) -> list[Satir]:
    satirlar = []
    for anahtar, t in varyantlar.items():
        p = boyutlandir(t, g)
        h = p.hucre  # paket için yeniden boyutlanmış hücre (tutarlılık)
        satirlar.append(Satir(
            f"BorPil-{anahtar}", h.hucre_wh_kg, h.hucre_wh_L,
            h.malzeme_usd_per_kwh * g.imalat_carpani, p.li_kg, p.bor_kg, 0.0, 0.0, "hayır",
            p.paket_kutle_kg, p.paket_hacim_L,
        ))
    for r in mz.REFERANSLAR.values():
        satirlar.append(_li_referans_satiri(r, g))
    return satirlar


def markdown_tablo(satirlar: list[Satir], E_kWh: float) -> str:
    bas = (f"| Kimya | Wh/kg (hücre) | Wh/L (hücre) | USD/kWh (hücre, varsayım) | Li (kg/{E_kWh:.0f} kWh) "
           f"| B (kg) | Co (kg) | Ni (kg) | Yanıcı elektrolit | Paket kütlesi (kg) | Paket hacmi (L) |\n")
    bas += "|---|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|\n"
    for s in satirlar:
        bas += (f"| {s.ad} | {s.wh_kg:.0f} | {s.wh_L:.0f} | {s.usd_kwh_hucre:.0f} | {s.li_kg:.1f} | {s.bor_kg:.1f} "
                f"| {s.co_kg:.1f} | {s.ni_kg:.1f} | {s.yanici} | {s.paket_kutle_kg:.0f} | {s.paket_hacim_L:.0f} |\n")
    return bas
