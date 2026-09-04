"""
Yaşayan ısıl sistem (YIS, kurul P27): paket kendi sıcaklığını tutar; yaşam payı
kullanıcının enerjisinden kesilir. TMS ölürse veya çekirdek T_ölüm altına inerse
paket 'ölü'dür (Ready yok). Amaç: kullanıcı LFP/NMC gibi binsin — ön ısıtma ritüeli yok.

Isıl denklem parkta: m·c·dT/dt = P_ısıtıcı − P_soğutma_ısıl − UA·(T−T_ortam).
Soğutmanın paketten çektiği elektrik ≈ P_soğutma_ısıl / COP.
Prizde ısıtma/soğutma şebekeden (SOC değişmez); prizsiz yaşam payından (SOC→0 olunca ısı durur).

P19 (parkta ısı yok) gen-1 varsayılan SKU olarak durur. YIS paralel işletim modudur.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import hucre as hc
from . import paket as pk
from . import simulasyon as sm


@dataclass(frozen=True)
class YasayanIsil:
    """Kurul P27 varsayılanları."""
    tutma_C: float = 35.0          # üst histerezis / prizde sıkı hedef
    tutma_alt_C: float = 25.0      # alt histerezis — 24/7 35 °C prizsiz rezervi yer
    sogutma_C: float = 55.0        # bundan sonra sıvı plaka
    olum_C: float = 10.0           # altında Ready yok (CCD/kullanıcı eşiği)
    tavan_C: float = 60.0
    yasam_payi: float = 0.08       # brüt SOC'den kullanıcıya görünmeyen pay
    kullanici_tavani: float = 0.96
    isitici_kW: float = 3.0
    sogutma_maks_kW: float = 3.0
    sogutma_COP: float = 2.5
    fabrika_soc: float = 1.0
    fabrika_T_C: float = 35.0
    kesici_C: float = 80.0         # P4 donanım kesici — ısıtıcıyı keser, sistemi 'ölü' saymaz


@dataclass
class YasamDurumu:
    soc: float
    T_C: float
    tms_ok: bool
    prize: bool
    yasayan: YasayanIsil
    paket: pk.PaketSonucu
    isitma_acik: bool = False
    sogutma_acik: bool = False
    kwh_yasam_harcanan: float = 0.0
    kwh_sebeke: float = 0.0

    @property
    def canli(self) -> bool:
        return self.tms_ok and self.T_C >= self.yasayan.olum_C and self.soc > 0.0

    @property
    def rezerv_soc(self) -> float:
        y = self.yasayan
        return max(0.0, min(self.soc, y.yasam_payi))

    @property
    def kullanici_gostergesi(self) -> float:
        """0–100, LFP gibi; yaşam payı ve üst tavan gizlenir."""
        y = self.yasayan
        span = y.kullanici_tavani - y.yasam_payi
        if span <= 0:
            return 0.0
        return float(np.clip((self.soc - y.yasam_payi) / span, 0.0, 1.0) * 100.0)

    @property
    def kullanici_kWh(self) -> float:
        y = self.yasayan
        return max(0.0, (min(self.soc, y.kullanici_tavani) - y.yasam_payi) * self.paket.gercek_enerji_kWh)


def dogum(p: pk.PaketSonucu | None = None, y: YasayanIsil | None = None) -> YasamDurumu:
    """Fabrika: full SOC, 35 °C, TMS sağ — sistem yaşamaya başlar."""
    if p is None:
        p = pk.boyutlandir(hc.BORPIL_A_ALT)
    if y is None:
        y = YasayanIsil()
    return YasamDurumu(soc=y.fabrika_soc, T_C=y.fabrika_T_C, tms_ok=True, prize=False,
                       yasayan=y, paket=p)


def rezerv_kWh(p: pk.PaketSonucu | None = None, y: YasayanIsil | None = None) -> float:
    if p is None:
        p = pk.boyutlandir(hc.BORPIL_A_ALT)
    if y is None:
        y = YasayanIsil()
    return y.yasam_payi * p.gercek_enerji_kWh


def _denetle(durum: YasamDurumu, T_ortam_C: float, prize: bool) -> None:
    """Histerezis mandalı: prizde 35 °C sıkı; prizsiz 25–35 °C."""
    y = durum.yasayan
    T = durum.T_C
    if not durum.tms_ok:
        durum.isitma_acik = False
        durum.sogutma_acik = False
        return
    if prize:
        if T < y.tutma_C - 0.3:
            durum.isitma_acik = True
        if T >= y.tutma_C + 0.3:
            durum.isitma_acik = False
    else:
        if T <= y.tutma_alt_C:
            durum.isitma_acik = True
        if T >= y.tutma_C:
            durum.isitma_acik = False
    if T >= y.sogutma_C:
        durum.sogutma_acik = True
    if T <= y.sogutma_C - 3.0:
        durum.sogutma_acik = False
    if T >= y.kesici_C:
        durum.isitma_acik = False


def _adim_isil(durum: YasamDurumu, T_ortam_C: float, dt: float, prize: bool) -> tuple[float, float, float, float]:
    """Bir dt: (T, soc, P_isitici_W, P_sogutma_isil_W). Durumu mandal ve kWh sayaçlarıyla günceller."""
    y, p = durum.yasayan, durum.paket
    T, soc = durum.T_C, durum.soc
    UA = p.isi_kaybi_W_per_K
    C = p.paket_kutle_kg * p.gereksinim.paket_isi_kapasitesi_kJ_kgK * 1e3
    _denetle(durum, T_ortam_C, prize)
    P_isi = y.isitici_kW * 1e3 if durum.isitma_acik else 0.0
    if durum.sogutma_acik:
        P_sog = min(y.sogutma_maks_kW * 1e3, max(200.0 * (T - y.sogutma_C), 400.0))
    else:
        P_sog = 0.0
    P_elek = P_isi + (P_sog / y.sogutma_COP if P_sog > 0 else 0.0)
    if prize:
        durum.kwh_sebeke += P_elek * dt / 3.6e6
    elif P_elek > 0 and soc > 0:
        d_soc = P_elek * dt / (p.gercek_enerji_kWh * 3.6e6)
        if d_soc >= soc:
            olcek = soc / max(d_soc, 1e-18)
            P_isi *= olcek
            P_sog *= olcek
            P_elek = soc * p.gercek_enerji_kWh * 3.6e6 / dt
            durum.kwh_yasam_harcanan += soc * p.gercek_enerji_kWh
            soc = 0.0
            durum.isitma_acik = False
            durum.sogutma_acik = False
        else:
            soc -= d_soc
            durum.kwh_yasam_harcanan += P_elek * dt / 3.6e6
    T += (P_isi - P_sog - UA * (T - T_ortam_C)) * dt / C
    return T, soc, P_isi, P_sog


def park_tutma(durum: YasamDurumu, T_ortam_C: float, sure_h: float, prize: bool = False,
               dt: float = 60.0) -> tuple[YasamDurumu, dict]:
    """Park: prizli şebeke, prizsiz yaşam payı. Histerezis 25–35 °C (prizde 35 °C sıkı)."""
    d = YasamDurumu(
        durum.soc, durum.T_C, durum.tms_ok, prize, durum.yasayan, durum.paket,
        durum.isitma_acik, durum.sogutma_acik, durum.kwh_yasam_harcanan, durum.kwh_sebeke,
    )
    isi_J = sog_J = 0.0
    n = max(1, int(round(sure_h * 3600 / dt)))
    for _ in range(n):
        T, soc, Pi, Ps = _adim_isil(d, T_ortam_C, dt, prize)
        d.T_C, d.soc = T, soc
        isi_J += Pi * dt
        sog_J += Ps * dt
    d.prize = prize
    ozet = {
        "sure_h": sure_h,
        "prize": prize,
        "T_bitis_C": d.T_C,
        "soc_bitis": d.soc,
        "isitici_kWh": isi_J / 3.6e6,
        "sogutma_kWh_isil": sog_J / 3.6e6,
        "yasam_kWh": d.kwh_yasam_harcanan,
        "sebeke_kWh": d.kwh_sebeke,
        "canli": d.canli,
        "gostergesi": d.kullanici_gostergesi,
        "kullanici_kWh": d.kullanici_kWh,
    }
    return d, ozet


def park_iz(durum: YasamDurumu, T_ortam_C: float, sure_h: float, prize: bool = False,
            dt: float = 120.0) -> dict:
    """Park zaman serisi (grafik / simülasyon çıktısı)."""
    d = YasamDurumu(
        durum.soc, durum.T_C, durum.tms_ok, prize, durum.yasayan, durum.paket,
        durum.isitma_acik, durum.sogutma_acik, durum.kwh_yasam_harcanan, durum.kwh_sebeke,
    )
    n = max(1, int(round(sure_h * 3600 / dt)))
    t = np.zeros(n + 1)
    T = np.zeros(n + 1)
    soc = np.zeros(n + 1)
    gosterge = np.zeros(n + 1)
    T[0], soc[0], gosterge[0] = d.T_C, d.soc, d.kullanici_gostergesi
    for i in range(n):
        Tn, sn, _, _ = _adim_isil(d, T_ortam_C, dt, prize)
        d.T_C, d.soc = Tn, sn
        t[i + 1] = (i + 1) * dt / 3600.0
        T[i + 1], soc[i + 1] = Tn, sn
        gosterge[i + 1] = d.kullanici_gostergesi
    d.prize = prize
    return {"t_h": t, "T_C": T, "soc": soc, "gosterge": gosterge, "durum": d,
            "prize": prize, "T_ortam_C": T_ortam_C}


def kullanici_surusu(durum: YasamDurumu, T_ortam_C: float) -> tuple[YasamDurumu, sm.SurusSonucu | None]:
    """LFP gibi: hazır değilse sürme. Hazırsa T zaten tutma bandında; ısıtıcı sürüşte atık ısı + PTC."""
    if not durum.canli:
        return durum, None
    y = durum.yasayan
    s = sm.surus_simulasyonu(
        durum.paket, T_ortam_C=T_ortam_C, T_baslangic_C=durum.T_C,
        isitici_hedef_C=y.tutma_C, isitici_guc_kW=y.isitici_kW,
        soc_bitis=y.yasam_payi,
    )
    kullanilan = s.tuketim_kWh_100km / 100.0 * s.menzil_km
    if kullanilan != kullanilan:  # NaN
        kullanilan = 0.0
    yeni_soc = max(y.yasam_payi, durum.soc - kullanilan / durum.paket.gercek_enerji_kWh)
    yeni = YasamDurumu(yeni_soc, s.T_bitis_C, durum.tms_ok, False, y, durum.paket)
    return yeni, s


def dc_sarj_canli(durum: YasamDurumu, T_ortam_C: float, soc_hedef: float = 0.80) -> sm.SarjSonucu:
    """Canlı paket zaten sıcak → 75 kW kapısı daha erken açılır. Ölü paket ortamdan ısınır (şebeke)."""
    T0 = durum.T_C if durum.canli else T_ortam_C
    return sm.sarj_simulasyonu(
        durum.paket, T_ortam_C=T_ortam_C, T_baslangic_C=T0,
        soc_baslangic=min(max(durum.soc, 0.10), 0.80), soc_hedef=soc_hedef,
        isitici_hedef_C=45.0, isitici_guc_kW=20.0,
    )


def tms_oldur(durum: YasamDurumu) -> YasamDurumu:
    """TMS arızası: paket ölü kabul (Ready yok). Kullanıcı önerisi — sistem ölürse paket ölür."""
    return YasamDurumu(durum.soc, durum.T_C, False, durum.prize, durum.yasayan, durum.paket)


def karsilastir_lfp_gibi(T_ortam_C: float = -10.0, park_h: float = 12.0,
                         varyant: str = "A-alt") -> dict:
    """Gen-1 (parkta ısı yok) vs YIS prizsiz vs YIS prizli — aynı gece, sonra sürüş ve 10→80 % şarj."""
    p = pk.boyutlandir(hc.VARYANTLAR[varyant])
    y = YasayanIsil()
    dog = dogum(p, y)

    g1_park_T = T_ortam_C  # UA≈10 W/K, 12 h ≫ zaman sabiti
    g1_surus = sm.surus_simulasyonu(p, T_ortam_C=T_ortam_C, T_baslangic_C=g1_park_T, isitici_hedef_C=35.0)
    g1_sarj = sm.sarj_simulasyonu(p, T_ortam_C=T_ortam_C, T_baslangic_C=g1_park_T)

    d_y, o_y = park_tutma(dog, T_ortam_C, park_h, prize=False)
    _, s_y = kullanici_surusu(d_y, T_ortam_C)
    sj_y = sm.sarj_simulasyonu(
        p, T_ortam_C=T_ortam_C,
        T_baslangic_C=d_y.T_C if d_y.canli else T_ortam_C,
    )

    d_p, o_p = park_tutma(dogum(p, y), T_ortam_C, park_h, prize=True)
    _, s_p = kullanici_surusu(d_p, T_ortam_C)
    sj_p = sm.sarj_simulasyonu(
        p, T_ortam_C=T_ortam_C,
        T_baslangic_C=d_p.T_C if d_p.canli else T_ortam_C,
    )

    olu = tms_oldur(dogum(p, y))
    _, s_olu = kullanici_surusu(olu, T_ortam_C)

    def _surus(s: sm.SurusSonucu | None) -> dict:
        if s is None:
            return {"hazir": False, "menzil_km": 0.0, "guc_kisiti_s": 0.0, "acik_kWh": 0.0, "T0": None}
        return {"hazir": True, "menzil_km": s.menzil_km, "guc_kisiti_s": s.guc_kisiti_s,
                "acik_kWh": s.guc_acigi_kWh, "T0": s.T_baslangic_C, "T1": s.T_bitis_C}

    return {
        "ortam_C": T_ortam_C, "park_h": park_h,
        "ua_W_K": p.isi_kaybi_W_per_K,
        "rezerv_kWh": rezerv_kWh(p, y),
        "gen1": {"park_T": g1_park_T, "surus": _surus(g1_surus),
                 "sarj_dk": g1_sarj.sure_dk, "sarj_isitici_kWh": g1_sarj.isitici_kWh},
        "yis_prizsiz": {"park": o_y, "surus": _surus(s_y),
                        "sarj_dk": sj_y.sure_dk, "sarj_isitici_kWh": sj_y.isitici_kWh},
        "yis_prizli": {"park": o_p, "surus": _surus(s_p),
                       "sarj_dk": sj_p.sure_dk, "sarj_isitici_kWh": sj_p.isitici_kWh},
        "tms_olu": {"canli": olu.canli, "surus": _surus(s_olu)},
        "kullanici_kWh_dogum": dog.kullanici_kWh,
        "brut_kWh": p.gercek_enerji_kWh,
    }


def ozet_metin(k: dict | None = None) -> str:
    if k is None:
        k = karsilastir_lfp_gibi()
    g1, ys, yp = k["gen1"], k["yis_prizsiz"], k["yis_prizli"]
    satir = [
        f"== Yaşayan ısıl sistem — {k['park_h']:.0f} h park, ortam {k['ortam_C']:.0f} °C ==",
        f"Doğumda kullanıcıya görünen enerji: {k['kullanici_kWh_dogum']:.1f} kWh / {k['brut_kWh']:.1f} kWh brüt "
        f"(yaşam payı {k['rezerv_kWh']:.1f} kWh gizlenir; UA {k['ua_W_K']:.1f} W/K).",
        f"Gen-1 (parkta ısı yok): kalkış T={g1['park_T']:.0f} °C, menzil {g1['surus']['menzil_km']:.0f} km, "
        f"güç kısıtı {g1['surus']['guc_kisiti_s']:.0f} s, 10→80 % {g1['sarj_dk']:.0f} dk.",
        f"YIS prizsiz: T={ys['park']['T_bitis_C']:.1f} °C, canli={ys['park']['canli']}, "
        f"gösterge %{ys['park']['gostergesi']:.0f}, ısıtıcı {ys['park']['isitici_kWh']:.2f} kWh. "
        f"Sürüş hazır={ys['surus']['hazir']}, menzil {ys['surus']['menzil_km']:.0f} km, "
        f"kısıt {ys['surus']['guc_kisiti_s']:.0f} s, şarj {ys['sarj_dk']:.0f} dk.",
        f"YIS prizli: T={yp['park']['T_bitis_C']:.1f} °C, canli={yp['park']['canli']}, "
        f"gösterge %{yp['park']['gostergesi']:.0f}, şebeke {yp['park']['sebeke_kWh']:.2f} kWh. "
        f"Sürüş kısıt {yp['surus']['guc_kisiti_s']:.0f} s, şarj {yp['sarj_dk']:.0f} dk — LFP gibi hedef.",
        f"TMS ölü: Ready={k['tms_olu']['canli']}, sürüş yasak={not k['tms_olu']['surus']['hazir']}.",
    ]
    return "\n".join(satir)


def markdown_bolum() -> str:
    sag = karsilastir_lfp_gibi(-10.0, 12.0)
    yazi = karsilastir_lfp_gibi(40.0, 12.0)
    k48 = karsilastir_lfp_gibi(-10.0, 48.0)

    def satir(ad, k, kol):
        if kol == "gen1":
            s = k["gen1"]["surus"]
            return (f"| {ad} | {k['gen1']['park_T']:.0f} | evet | {s['menzil_km']:.0f} | "
                    f"{s['guc_kisiti_s']:.0f} | {k['gen1']['sarj_dk']:.0f} |")
        blok = k[kol]
        park = blok["park"]
        s = blok["surus"]
        return (f"| {ad} | {park['T_bitis_C']:.1f} | {str(park['canli']).lower()} | "
                f"{s['menzil_km']:.0f} | {s['guc_kisiti_s']:.0f} | {blok['sarj_dk']:.0f} |")

    return "\n".join([
        "## 13. Yaşayan ısıl sistem (YIS, kurul P27)\n",
        ozet_metin(sag) + "\n",
        "| Senaryo | Kalkış T °C | Canlı | Menzil km | Güç kısıtı s | 10→80 % dk |\n|---|---:|:---:|---:|---:|---:|",
        satir("Gen-1, −10 °C 12 h", sag, "gen1"),
        satir("YIS prizsiz, −10 °C 12 h", sag, "yis_prizsiz"),
        satir("YIS prizli, −10 °C 12 h", sag, "yis_prizli"),
        satir("YIS prizsiz, −10 °C 48 h", k48, "yis_prizsiz"),
        satir("YIS prizli, 40 °C 12 h", yazi, "yis_prizli"),
        "",
        "Kullanıcı 0–100 gösterge yaşam payını gizler. TMS arızası veya T < 10 °C → Ready yok "
        "(paket ölü; şebekeden diriltme ayrı). P19 (parkta ısı yok) varsayılan SKU olarak durur; "
        "YIS paralel işletim modudur. Ayrıntı: `docs/11_yasayan_isil_sistem.md`.\n",
    ])
