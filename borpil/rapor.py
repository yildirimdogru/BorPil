"""
Tüm hesapları çalıştırır; Markdown rapor + grafikler üretir (varsayılan çıktı dizini: cikti/).
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import numpy as np

from . import elektrolit as el
from . import geometri as ge
from . import hucre as hc
from . import karsilastirma as ks
from . import malzemeler as mz
from . import paket as pk
from . import simulasyon as sm
from . import termodinamik as td


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "figure.dpi": 130})
    return plt


# ---------------------------------------------------------------------------
# Grafikler
# ---------------------------------------------------------------------------

def grafik_iletkenlik(cikti: Path) -> Path:
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for ad, se in mz.KATI_ELEKTROLITLER.items():
        T_C, sig = el.sicaklik_tarama(se, -30, 150, 361)
        ax.semilogy(1000 / (T_C + 273.15), sig, label=ad)
    ax.axvspan(1000 / (60 + 273.15), 1000 / (25 + 273.15), color="0.9", label="Çalışma penceresi 25-60 °C")
    ax.axhline(1e-3, ls=":", c="k", lw=0.8)
    ax.text(3.9, 1.2e-3, "1 mS/cm (EV eşiği)", fontsize=8)
    ax.set_xlabel("1000/T (1/K)")
    ax.set_ylabel("İyonik iletkenlik σ (S/cm)")
    sec = ax.secondary_xaxis("top", functions=(lambda x: 1000 / x - 273.15, lambda c: 1000 / (c + 273.15)))
    sec.set_xlabel("T (°C)")
    ax.set_title("Kloso-borat katı elektrolitler — Arrhenius modeli")
    ax.legend(fontsize=7, loc="lower left")
    ax.grid(alpha=0.3, which="both")
    yol = cikti / "iletkenlik_arrhenius.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


def grafik_enerji_yogunlugu(cikti: Path, satirlar: list[ks.Satir]) -> Path:
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    adlar = [s.ad.replace("Li-iyon ", "").split(" (")[0] for s in satirlar]
    x = np.arange(len(satirlar))
    ax.bar(x - 0.2, [s.wh_kg for s in satirlar], 0.4, label="Wh/kg (hücre)")
    ax.bar(x + 0.2, [s.wh_L for s in satirlar], 0.4, label="Wh/L (hücre)")
    ax.set_xticks(x); ax.set_xticklabels(adlar, rotation=20, ha="right")
    ax.set_ylabel("Enerji yoğunluğu")
    ax.set_title("Hücre düzeyi enerji yoğunluğu: BorPil varyantları ve Li-iyon referansları")
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    yol = cikti / "enerji_yogunlugu.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


def grafik_duyarlilik(cikti: Path, temel: hc.HucreTasarimi) -> Path:
    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    kalinliklar = np.array([10, 20, 30, 50, 80, 120])
    for q in (2.0, 3.0, 4.0, 5.0):
        whkg = [hc.hesapla(dataclasses.replace(temel, ayirici_kalinlik_um=k, alan_kapasitesi_mAh_cm2=q)).hucre_wh_kg
                for k in kalinliklar]
        axes[0].plot(kalinliklar, whkg, "o-", label=f"{q:.0f} mAh/cm²")
    axes[0].set_xlabel("SE ayırıcı kalınlığı (µm)"); axes[0].set_ylabel("Hücre Wh/kg")
    axes[0].set_title("Enerji yoğunluğu duyarlılığı"); axes[0].legend(fontsize=7); axes[0].grid(alpha=0.3)

    fiyatlar = np.linspace(10, 120, 12)
    for anahtar in ("A", "A-Fe", "A0"):
        t = hc.VARYANTLAR[anahtar]
        maliyetler = []
        for f in fiyatlar:
            se = dataclasses.replace(t.elektrolit, maliyet_usd_kg=f)
            maliyetler.append(hc.hesapla(dataclasses.replace(t, elektrolit=se)).malzeme_usd_per_kwh)
        axes[1].plot(fiyatlar, maliyetler, "s-", label=f"BorPil-{anahtar}")
    axes[1].axhline(55, ls="--", c="gray"); axes[1].text(12, 57, "LFP malzeme maliyeti (~55 USD/kWh)", fontsize=7)
    axes[1].set_xlabel("Kloso-borat elektrolit fiyatı (USD/kg)"); axes[1].set_ylabel("Hücre malzeme maliyeti (USD/kWh)")
    axes[1].set_title("Maliyet duyarlılığı"); axes[1].legend(fontsize=7); axes[1].grid(alpha=0.3)
    yol = cikti / "duyarlilik.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


def grafik_guc_ve_desarj(cikti: Path, p: pk.PaketSonucu) -> Path:
    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    T = np.linspace(-20, 70, 46)
    for soc in (0.8, 0.5, 0.2):
        axes[0].plot(T, [sm.maks_guc_kW(p, t, soc) for t in T], label=f"SOC {soc:.0%}")
    axes[0].axhline(p.gereksinim.tepe_guc_kW, ls="--", c="k", lw=0.8)
    axes[0].text(-18, p.gereksinim.tepe_guc_kW * 1.03, f"Hedef tepe güç {p.gereksinim.tepe_guc_kW:.0f} kW", fontsize=7)
    axes[0].set_xlabel("Paket sıcaklığı (°C)"); axes[0].set_ylabel("10 s tepe güç (kW), V_min = 2.3 V/hücre")
    axes[0].set_title("Güç yeteneği — sıcaklık (omik ∧ kritik akım sınırı)"); axes[0].legend(fontsize=7)
    axes[0].grid(alpha=0.3); axes[0].set_ylim(0, None)

    for c, T_C in ((0.2, 45), (1.0, 45), (2.0, 45), (1.0, 20), (0.5, 0), (0.2, -10)):
        Ah, V = sm.sabit_akim_desarj(p.hucre, c, T_C)
        axes[1].plot(Ah, V, label=f"{c:g}C, {T_C:+d} °C")
    axes[1].set_xlabel("Deşarj kapasitesi (Ah)"); axes[1].set_ylabel("Hücre gerilimi (V)")
    axes[1].set_title(f"Deşarj eğrileri — {p.hucre.hucre_kapasite_Ah:.0f} Ah pouch"); axes[1].legend(fontsize=7)
    axes[1].grid(alpha=0.3)
    yol = cikti / "guc_ve_desarj.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


def grafik_katmanlar(cikti: Path, h: hc.HucreSonucu) -> Path:
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    renk = {"Al": "#9e9e9e", "Katot": "#5c6bc0", "SE": "#26a69a", "Na": "#ffb300", "Sert": "#8d6e63"}
    y = 0
    for k in h.katmanlar:
        r = next((v for anahtar, v in renk.items() if k.ad.startswith(anahtar)), "#cccccc")
        ax.barh(0, k.kalinlik_um, left=y, color=r, edgecolor="k", lw=0.4)
        if k.kalinlik_um > 25:
            ax.text(y + k.kalinlik_um / 2, 0, k.ad.split(" (")[0].split(" anot")[0].split(" kompozit")[0],
                    ha="center", va="center", fontsize=7, rotation=90)
        y += k.kalinlik_um
    ax.set_xlim(0, y); ax.set_yticks([]); ax.set_xlabel("Kalınlık (µm)")
    ax.set_title(f"Çift taraflı tekrar birimi — {h.tekrar_kalinlik_um:.0f} µm, {h.tekrar_kapasite_mAh_cm2:.0f} mAh/cm²")
    yol = cikti / "katman_yigini.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


def grafik_ikosahedron(cikti: Path) -> Path:
    plt = _plt()
    v = ge.ikosahedron_koseleri()
    fig = plt.figure(figsize=(4.2, 4.2))
    ax = fig.add_subplot(111, projection="3d")
    for i in range(12):
        for j in range(i + 1, 12):
            if abs(np.linalg.norm(v[i] - v[j]) - ge.B_B_BAG) < 1e-6:
                ax.plot(*zip(v[i], v[j]), c="#5c6bc0", lw=1.2)
    ax.scatter(*v.T, s=60, c="#3949ab", depthshade=False)
    h = v / np.linalg.norm(v, axis=1, keepdims=True) * (np.linalg.norm(v[0]) + ge.B_H_BAG)
    for b, hh in zip(v, h):
        ax.plot(*zip(b, hh), c="0.6", lw=0.8)
    ax.scatter(*h.T, s=15, c="0.5")
    ax.set_box_aspect([1, 1, 1]); ax.set_axis_off()
    ax.set_title("[B12H12]2- ikosahedronu\n(B–B 1.78 Å, B–H 1.20 Å)", fontsize=9)
    yol = cikti / "b12h12_ikosahedron.png"
    fig.tight_layout(); fig.savefig(yol); plt.close(fig)
    return yol


# ---------------------------------------------------------------------------
# Rapor
# ---------------------------------------------------------------------------

def uret(cikti_dizini: str | Path = "cikti", grafikler: bool = True) -> Path:
    cikti = Path(cikti_dizini)
    cikti.mkdir(parents=True, exist_ok=True)

    g = pk.PaketGereksinimi()
    satirlar = ks.tablo(hc.VARYANTLAR, g)
    hA = hc.hesapla(hc.BORPIL_A)
    pA = pk.boyutlandir(hc.BORPIL_A, g)
    surus_20 = sm.surus_simulasyonu(pA, T_ortam_C=20.0, isitici_hedef_C=None)
    surus_m10 = sm.surus_simulasyonu(pA, T_ortam_C=-10.0, isitici_hedef_C=25.0, isitici_guc_kW=6.0)
    surus_35 = sm.surus_simulasyonu(pA, T_ortam_C=35.0, isitici_hedef_C=None)

    yollar = {}
    if grafikler:
        yollar["iletkenlik"] = grafik_iletkenlik(cikti)
        yollar["enerji"] = grafik_enerji_yogunlugu(cikti, satirlar)
        yollar["duyarlilik"] = grafik_duyarlilik(cikti, hc.BORPIL_A)
        yollar["guc"] = grafik_guc_ve_desarj(cikti, pA)
        yollar["katman"] = grafik_katmanlar(cikti, pA.hucre)
        yollar["iko"] = grafik_ikosahedron(cikti)

    md = []
    md.append("# BorPil — Hesaplanmış Tasarım Raporu (otomatik üretildi)\n")
    md.append("Bu dosya `borpil rapor` komutuyla üretilir; tüm sayılar `borpil` paketindeki modellerden gelir.\n")

    md.append("## 1. Teorik sınırlar (termodinamik)\n")
    md.append("| Kimya | Reaksiyon | E° (V) | Kapasite (mAh/g reaktan) | Wh/kg reaktan | Wh/kg ürün (O₂ dâhil) |\n|---|---|---:|---:|---:|---:|")
    for k in td.metal_hava_kiyas() + [td.dbfc()]:
        md.append(f"| {k.ad} | {k.reaksiyon} | {k.E0_V:.3f} | {k.kapasite_mah_g:.0f} | {k.enerji_wh_kg_reaktan:.0f} | {k.enerji_wh_kg_urun:.0f} |")
    dp = td.dbfc_pratik(); dr = td.dbfc_gidis_donus()
    md.append("")
    md.append(f"DBFC pratik tahmin: %20 NaBH₄ çözeltisi, 1.0 V, %75 yakıt kullanımı → "
              f"{dp['pratik_wh_kg_cozelti']:.0f} Wh/kg çözelti, {dp['pratik_wh_kg_sistem']:.0f} Wh/kg sistem; "
              f"NaBO₂→NaBH₄ rejenerasyonu dâhil gidiş-dönüş verimi **%{dr['gidis_donus_verimi']*100:.0f}** "
              f"(rejenerasyon verimi %35 varsayımı). Sonuç: DBFC ana depolama değil, menzil uzatıcı/yakıt yoludur.\n")
    mu = td.dbfc_menzil_uzatici()
    md.append(f"DBFC menzil uzatıcı örneği: 40 kg çözelti (8 kg NaBH₄) + 15 kW yığın + tank/BOP = {mu['sistem_kutle_kg']:.0f} kg → "
              f"{mu['enerji_kWh']:.0f} kWh, **+{mu['ek_menzil_km']:.0f} km** ({mu['sistem_wh_kg']:.0f} Wh/kg sistem), "
              f"~{mu['dolum_suresi_dk']:.0f} dk sıvı dolum.\n")

    md.append("## 2. Elektrolit: kloso-borat iletkenliği\n")
    md.append("| Elektrolit | σ(−10 °C) mS/cm | σ(25 °C) | σ(45 °C) | σ(60 °C) | Ea (eV) | ASR 30 µm @45 °C (Ω·cm²) |\n|---|---:|---:|---:|---:|---:|---:|")
    for ad, se in mz.KATI_ELEKTROLITLER.items():
        s = [float(el.iletkenlik_C(se, T)) * 1e3 for T in (-10, 25, 45, 60)]
        md.append(f"| {ad} | {s[0]:.3g} | {s[1]:.3g} | {s[2]:.3g} | {s[3]:.3g} | {se.Ea:.2f} | {el.alan_direnci_ohm_cm2(se, 30, 45):.2f} |")
    geo = ge.b12h12_geometrisi(); bos = ge.na_bosluk_analizi(mz.NA2B12H12.yogunluk, mz.NA2B12H12.molar_kutle)
    md.append("")
    md.append(f"Geometri: {geo}. Süperiyonik bcc Na₂B₁₂H₁₂ kafesi a = {bos['kafes_a_A']:.2f} Å; anyon sert-küre yarıçapı "
              f"{bos['anyon_sert_kure_yaricap_A']:.2f} Å; tetrahedral site boşluk yarıçapı {bos['tetrahedral_bosluk_yaricap_A']:.2f} Å "
              f"(Na⁺ {bos['Na_yaricap_A']:.2f} Å); Na site doluluğu {bos['na_site_doluluk']:.2f} → yüksek vakans oranı.\n")

    md.append("## 3. Hücre varyantları\n")
    for anahtar, t in hc.VARYANTLAR.items():
        md.append("```\n" + hc.hesapla(t).ozet() + "\n```\n")

    md.append("## 4. Paket (BorPil-A, 75 kWh, 400 V)\n")
    md.append("```\n" + pA.ozet() + "\n```\n")

    md.append("## 5. Sürüş simülasyonu (WLTP-benzeri sentetik çevrim, C-segment)\n")
    md.append("| Senaryo | Menzil (km) | Tüketim (kWh/100 km) | Paket T başlangıç→bitiş (°C) | Min hücre gerilimi (V) | Ort. I²R ısı (W) |\n|---|---:|---:|---:|---:|---:|")
    for ad, s in (("20 °C, ısıtıcı yok", surus_20), ("−10 °C, 25 °C'ye ısıtıcı (6 kW)", surus_m10), ("35 °C", surus_35)):
        md.append(f"| {ad} | {s.menzil_km:.0f} | {s.tuketim_kWh_100km:.1f} | {s.T_baslangic_C:.0f}→{s.T_bitis_C:.0f} | {s.V_min_hucre:.2f} | {s.isi_uretimi_ort_W:.0f} |")
    md.append("")
    md.append(f"Araç toplam kütlesi {surus_20.toplam_kutle_kg:.0f} kg (glider + yük + paket).\n")

    md.append("## 6. Li-iyon ile karşılaştırma (75 kWh paket)\n")
    md.append(ks.markdown_tablo(satirlar, g.brut_enerji_kWh))

    if grafikler:
        md.append("## 7. Grafikler\n")
        for ad, yol in yollar.items():
            md.append(f"![{ad}]({yol.name})\n")

    rapor_yolu = cikti / "RAPOR.md"
    rapor_yolu.write_text("\n".join(md), encoding="utf-8")
    return rapor_yolu
