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
from . import kimya_sicaklik as ky
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
    ax.axvspan(1000 / (60 + 273.15), 1000 / (25 + 273.15), color="0.9", label="Gen-1 pencere 25-60 °C")
    ax.axvspan(1000 / (45 + 273.15), 1000 / (10 + 273.15), color="#bbdefb", alpha=0.45, label="Hedef 10-45 °C")
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

    fiyatlar = np.array([10, 20, 30, 50, 75, 100, 150, 200])
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
    axes[1].set_xscale("log")
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
    axes[0].set_xlabel("Paket sıcaklığı (°C)"); axes[0].set_ylabel(f"10 s tepe güç (kW), V_min = {sm.v_min_hucre(p.hucre):.2f} V/hücre")
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


def grafik_isitma_ve_sarj(cikti: Path, p: pk.PaketSonucu) -> Path:
    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    T = np.linspace(-20, 60, 41)
    axes[0].plot(T, [sm.maks_sarj_gucu_kW(p, t) for t in T], label="Azami şarj/rejen gücü (CCD/1.5)")
    axes[0].plot(T, [sm.maks_guc_kW(p, t) for t in T], label="10 s tepe deşarj gücü")
    axes[0].plot(T, [sm.darbe_isitma_gucu_kW(p, t, 1.0) for t in T], "--", label="Darbe ısıtma gücü (1C rms)")
    axes[0].axhline(p.gereksinim.hizli_sarj_kW, ls=":", c="k", lw=0.8)
    axes[0].text(-18, p.gereksinim.hizli_sarj_kW * 1.05, f"Hızlı şarj hedefi {p.gereksinim.hizli_sarj_kW:.0f} kW", fontsize=7)
    axes[0].set_xlabel("Paket sıcaklığı (°C)"); axes[0].set_ylabel("kW"); axes[0].set_ylim(0, 300)
    axes[0].set_title("Güç haritaları — sıcaklık (BMS sınır haritası)"); axes[0].legend(fontsize=7); axes[0].grid(alpha=0.3)
    T0s = [-20, -10, 0, 10, 25, 35, 45]
    sureler = [sm.sarj_simulasyonu(p, T_baslangic_C=t).sure_dk for t in T0s]
    isitici = [sm.sarj_simulasyonu(p, T_baslangic_C=t).isitici_kWh for t in T0s]
    ax2 = axes[1]
    ax2.bar(T0s, sureler, width=6, color="#5c6bc0", label="10→80 % süre (dk)")
    ax2.set_xlabel("Paket başlangıç sıcaklığı (°C)"); ax2.set_ylabel("Şarj süresi (dk)")
    ax3 = ax2.twinx(); ax3.plot(T0s, isitici, "o-", c="#ffb300", label="Isıtıcı enerjisi (kWh, şebekeden)")
    ax3.set_ylabel("kWh")
    ax2.set_title("DC hızlı şarj (150 kW cihaz, 20 kW şebeke ısıtıcı)")
    h1, l1 = ax2.get_legend_handles_labels(); h2, l2 = ax3.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper right"); ax2.grid(alpha=0.3)
    yol = cikti / "isitma_ve_sarj.png"
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
    # Kurul P11: 1. nesil ticari baz çizgisi A-alt; A hedef/üst bant
    pB = pk.boyutlandir(hc.BORPIL_A_ALT, g)   # baz
    pA = pk.boyutlandir(hc.BORPIL_A, g)       # hedef
    senaryolar = [
        ("20 °C, ısıtıcı 35 °C + 0.8 kW atık ısı (strateji)", dict(T_ortam_C=20.0, isitici_hedef_C=35.0)),
        ("20 °C, ısıtıcı kapalı", dict(T_ortam_C=20.0, isitici_hedef_C=None)),
        ("−10 °C, ısıtıcı 35 °C (3 kW PTC + atık ısı)", dict(T_ortam_C=-10.0, isitici_hedef_C=35.0)),
        ("−10 °C, şebekeden 35 °C'ye ön ısıtılmış", dict(T_ortam_C=-10.0, T_baslangic_C=35.0, isitici_hedef_C=35.0)),
        ("−20 °C, ısıtıcı arızalı (stres)", dict(T_ortam_C=-20.0, isitici_hedef_C=None)),
        ("35 °C", dict(T_ortam_C=35.0, isitici_hedef_C=35.0)),
        ("40 °C, otoyol 130 km/h", dict(T_ortam_C=40.0, isitici_hedef_C=35.0, cevrim=sm.sabit_hiz_cevrimi(130))),
    ]
    surusler = {ad: (sm.surus_simulasyonu(pB, **kw), sm.surus_simulasyonu(pA, **kw)) for ad, kw in senaryolar}
    sarjlar = {T0: (sm.sarj_simulasyonu(pB, T_baslangic_C=T0), sm.sarj_simulasyonu(pA, T_baslangic_C=T0)) for T0 in (45, 25, 0, -10)}

    yollar = {}
    if grafikler:
        yollar["iletkenlik"] = grafik_iletkenlik(cikti)
        yollar["enerji"] = grafik_enerji_yogunlugu(cikti, satirlar)
        yollar["duyarlilik"] = grafik_duyarlilik(cikti, hc.BORPIL_A)
        yollar["guc"] = grafik_guc_ve_desarj(cikti, pB)
        yollar["katman"] = grafik_katmanlar(cikti, pB.hucre)
        yollar["iko"] = grafik_ikosahedron(cikti)
        yollar["isitma"] = grafik_isitma_ve_sarj(cikti, pB)

    md = []
    md.append("# BorPil — Hesaplanmış Tasarım Raporu (otomatik üretildi)\n")
    md.append("Bu dosya `borpil rapor` komutuyla üretilir; tüm sayılar `borpil` paketindeki modellerden gelir. "
              "Kurul kararı (docs/07): 1. nesil ticari **baz çizgisi BorPil-A-alt**, **hedef/üst bant BorPil-A**; "
              "her iki konfigürasyon yan yana raporlanır.\n")

    md.append("## 1. Teorik sınırlar (termodinamik)\n")
    md.append("| Kimya | Reaksiyon | E° (V) | Kapasite (mAh/g reaktan) | Wh/kg reaktan | Wh/kg ürün (O₂ dâhil) |\n|---|---|---:|---:|---:|---:|")
    for k in td.metal_hava_kiyas() + [td.dbfc()]:
        md.append(f"| {k.ad} | {k.reaksiyon} | {k.E0_V:.3f} | {k.kapasite_mah_g:.0f} | {k.enerji_wh_kg_reaktan:.0f} | {k.enerji_wh_kg_urun:.0f} |")
    dp = td.dbfc_pratik(); dr = td.dbfc_gidis_donus()
    md.append("")
    md.append(f"DBFC pratik tahmin: %20 NaBH₄ çözeltisi, 0.85 V, %65 yakıt kullanımı → "
              f"{dp['pratik_wh_kg_cozelti']:.0f} Wh/kg çözelti, {dp['pratik_wh_kg_sistem']:.0f} Wh/kg sistem; "
              f"NaBO₂→NaBH₄ rejenerasyonu dâhil gidiş-dönüş verimi **%{dr['gidis_donus_verimi']*100:.0f}** "
              f"(rejenerasyon verimi %30 varsayımı). Sonuç: DBFC ana depolama değil, menzil uzatıcı/yakıt yoludur.\n")
    mu = td.dbfc_menzil_uzatici()
    md.append(f"DBFC menzil uzatıcı örneği: 40 kg çözelti (8 kg NaBH₄) + 15 kW yığın + tank/BOP = {mu['sistem_kutle_kg']:.0f} kg → "
              f"{mu['enerji_kWh']:.0f} kWh, **+{mu['ek_menzil_km']:.0f} km** ({mu['sistem_wh_kg']:.0f} Wh/kg sistem), "
              f"~{mu['dolum_suresi_dk']:.0f} dk sıvı dolum.\n")

    md.append("## 2. Elektrolit: kloso-borat iletkenliği\n")
    md.append("| Elektrolit | σ(−10 °C) mS/cm | σ(25 °C) | σ(45 °C) | σ(60 °C) | Ea (eV) | ASR 30 µm @45 °C (Ω·cm²) |\n|---|---:|---:|---:|---:|---:|---:|")
    for ad, se in mz.KATI_ELEKTROLITLER.items():
        s = [float(el.iletkenlik_C(se, T)) * 1e3 for T in (-10, 25, 45, 60)]
        md.append(f"| {ad} | {s[0]:.3g} | {s[1]:.3g} | {s[2]:.3g} | {s[3]:.3g} | {se.Ea:.2f} | {el.alan_direnci_ohm_cm2(se, 30, 45):.3g} |")
    geo = ge.b12h12_geometrisi(); bos = ge.na_bosluk_analizi(mz.NA2B12H12.yogunluk, mz.NA2B12H12.molar_kutle)
    md.append("")
    md.append(f"Geometri: {geo}. Süperiyonik bcc Na₂B₁₂H₁₂ kafesi a = {bos['kafes_a_A']:.2f} Å; anyon sert-küre yarıçapı "
              f"{bos['anyon_sert_kure_yaricap_A']:.2f} Å; tetrahedral site boşluk yarıçapı {bos['tetrahedral_bosluk_yaricap_A']:.2f} Å "
              f"(Na⁺ {bos['Na_yaricap_A']:.2f} Å); Na site doluluğu {bos['na_site_doluluk']:.2f} → yüksek vakans oranı.\n")

    md.append("## 3. Hücre varyantları\n")
    for anahtar, t in hc.VARYANTLAR.items():
        md.append("```\n" + hc.hesapla(t).ozet() + "\n```\n")

    md.append("## 4. Paket (75 kWh, 120s3p, 3 bağımsız dizi, pouch-in-frame)\n")
    md.append("### 4a. Baz çizgisi — BorPil-A-alt\n```\n" + pB.ozet() + "\n```\n")
    md.append("### 4b. Hedef — BorPil-A\n```\n" + pA.ozet() + "\n```\n")

    md.append("## 5. Sürüş simülasyonu (WLTP-benzeri sentetik çevrim, C-segment) — baz / hedef\n")
    md.append("Akım sınırları tüm modüllerde ortaktır (deşarj CCD×2, rejen CCD/1.5); güç kısıtında araç kalan güçle "
              "ulaşabildiği hıza düşer, fazla rejen mekanik frene gider.\n")
    md.append("| Senaryo | Menzil km (baz / hedef) | Tüketim kWh/100 km | Paket T (°C) | Isıtıcı kWh | Güç kısıtı s / açık kWh | Rejen kaybı kWh | Ort. hız km/h |\n|---|---:|---:|---:|---:|---:|---:|---:|")
    for ad, (b, a) in surusler.items():
        md.append(f"| {ad} | **{b.menzil_km:.0f}** / {a.menzil_km:.0f} | {b.tuketim_kWh_100km:.1f} / {a.tuketim_kWh_100km:.1f} | "
                  f"{b.T_baslangic_C:.0f}→{b.T_bitis_C:.0f} (maks {b.T_maks_C:.0f}) | {b.isitici_kWh:.1f} | {b.guc_kisiti_s:.0f} / {b.guc_acigi_kWh:.1f} | "
                  f"{b.rejen_kaybi_kWh:.1f} | {b.ort_hiz_kmh:.0f} |")
    b20 = surusler[senaryolar[0][0]][0]
    md.append("")
    md.append(f"Araç toplam kütlesi {b20.toplam_kutle_kg:.0f} kg (baz; glider + yük + paket). Tüketim bataryadan çekilen toplam enerjidir "
              f"(ısıtıcı dâhil, şebeke şarj kayıpları hariç). −20 °C 'ısıtıcı arızalı' satırı: araç çevrimi izleyemez (güç kısıtı süresi ve "
              f"açık büyük); menzil değeri düşük hızda sürüşe karşılık gelir ve operasyonel bir vaat değildir.\n")

    md.append("## 6. DC hızlı şarj (10 → 80 % SOC, 150 kW cihaz, şebekeden 20 kW ısıtıcı) — baz / hedef\n")
    md.append("| Paket başlangıç T | Süre dk | Ortalama / tepe güç kW | Isıtıcı kWh | I²R kWh | Bitiş T °C | Sınırlayıcı (süre kesri) |\n|---:|---:|---:|---:|---:|---:|---|")
    for T0, (b, a) in sarjlar.items():
        sinir = ", ".join(f"{k} %{v*100:.0f}" for k, v in b.sinir_dagilimi.items() if v > 0.005)
        md.append(f"| {T0} °C | **{b.sure_dk:.0f}** / {a.sure_dk:.0f} | {b.ort_guc_kW:.0f} / {b.tepe_guc_kW:.0f} | {b.isitici_kWh:.1f} | "
                  f"{b.kayip_I2R_kWh:.2f} | {b.T_bitis_C:.0f} | {sinir} |")
    md.append("")
    md.append(f"Hızlı şarj sıcaklık kapısı: {g.hizli_sarj_kW:.0f} kW için paket ≥ {pB.hizli_sarj_min_T_C:.0f} °C (CCD/1.5). "
              "Soğuk pakette şarj süresi ısıtma gücüyle belirlenir; bu yüzden ısıtıcı DC şarj cihazından 20 kW ile beslenir.\n")

    md.append("## 7. Isıtma seçenekleri (−10 °C → 45 °C ön ısıtma; kurul P5/P6)\n")
    md.append("| Yöntem | Süre dk | Enerji kWh | Not |\n|---|---:|---:|---|")
    for ad, kw in (("PTC 3 kW (park, paketten)", dict(ptc_kW=3)), ("PTC 6 kW", dict(ptc_kW=6)),
                   ("Şebekeden 20 kW (DC şarj istasyonu)", dict(ptc_kW=20)),
                   ("Darbe (AC) ısıtma 1C rms, tek başına", dict(darbe_c_orani=1.0)),
                   ("Darbe 1C + PTC 3 kW", dict(ptc_kW=3, darbe_c_orani=1.0))):
        sure, E = sm.on_isitma_suresi_dk(pB, -10, 45, **kw)
        md.append(f"| {ad} | {sure:.0f} | {E:.1f} | |")
    sure0, E0 = sm.on_isitma_suresi_dk(pB, -20, 0, darbe_c_orani=1.0)
    md.append("")
    md.append(f"Darbe ısıtma −20 °C'de {sm.darbe_isitma_gucu_kW(pB, -20, 1.0):.0f} kW, 0 °C'de {sm.darbe_isitma_gucu_kW(pB, 0, 1.0):.0f} kW, "
              f"25 °C'de {sm.darbe_isitma_gucu_kW(pB, 25, 1.0):.1f} kW üretir (direnç ısındıkça düşer → kendini sınırlar): "
              f"−20 → 0 °C **{sure0:.0f} dk / {E0:.1f} kWh**. Sonuç: darbe ısıtma derin soğuktan çıkış aracı, tam ön ısıtma için "
              "şebeke gücü veya atık ısı gerekir. Na/kloso-borat arayüzünün kHz AC dayanımı deneysel doğrulama planındadır.\n")

    md.append("## 8. Elektrik mimarisi ve güvenlik kontrolleri (baz paket)\n")
    md.append(f"- Gerilim penceresi {pB.V_min_paket:.0f}–{pB.V_maks_paket:.0f} V (invertör DC-link tavanı {g.invertor_dc_link_maks_V:.0f} V, "
              f"şarj cihazı {g.sarj_cihazi_maks_V:.0f} V sınıfı); tepe akım {pB.tepe_akim_paket_A:.0f} A; tab sürekli {pB.tab_akim_yogunlugu_surekli_A_mm2:.1f} A/mm².")
    md.append(f"- Beklenen kısa devre akımı: 45 °C'de {pB.kisa_devre_akimi_45C_kA:.1f} kA, −10 °C'de {pB.kisa_devre_akimi_m10C_A:.0f} A "
              f"(sürekli akımın 2 katından düşük → sigorta soğukta ayırt edemez; akım-plausibilite + dI/dt ile kontaktör açma).")
    md.append(f"- Isıtıcı takılı kalma: +{pB.isitici_takili_isinma_K_per_h:.0f} K/h, 35 °C'den Na erimesine {pB.isitici_takili_na_erime_dk:.0f} dk "
              f"(3 kW PTC ile); bağımsız donanım kesici {g.isitici_donanim_kesici_C:.0f} °C + ayrı ısıtıcı kontaktörü + çift NTC (ASIL D → B(D)+B(D)).")
    md.append(f"- {pB.paralel} bağımsız {pB.seri}s dizi: dizi akım dengesizliği = Na dendrit yumuşak kısa devre dedektörü; 2/3 güçle hata toleransı.")
    for u in pB.uyarilar:
        md.append(f"- ! {u}")
    md.append("")

    md.append("## 9. Maliyet (gen-1 gerçekçi model: imalat ×1.75, ilk geçiş verimi %75, paket +32 USD/kWh)\n")
    md.append("| SE fiyatı USD/kg | Verim | Baz (A-alt) paket USD/kWh | Hedef (A) paket USD/kWh |\n|---:|---:|---:|---:|")
    for fiyat, verim in ((50, 0.75), (50, 0.90), (25, 0.90), (15, 0.95)):
        satir = []
        for t in (hc.BORPIL_A_ALT, hc.BORPIL_A):
            se = dataclasses.replace(t.elektrolit, maliyet_usd_kg=fiyat)
            gg = dataclasses.replace(g, ilk_gecis_verimi=verim, imalat_carpani=1.75 if verim < 0.9 else 1.55)
            satir.append(pk.boyutlandir(dataclasses.replace(t, elektrolit=se), gg).maliyet_usd_kWh)
        md.append(f"| {fiyat} | %{verim*100:.0f} | {satir[0]:.0f} | {satir[1]:.0f} |")
    md.append("")
    md.append("Ekonomik hedef bandı (165–200 USD/kWh) için SE ≤ 25 USD/kg **ve** verim ≥ %90 **ve** imalat çarpanı ≤ 1.55 (10 GWh ölçeği) gerekir; "
              "120 USD/kWh mevcut malzeme karmasıyla ulaşılabilir değildir (SE ≤ 15 USD/kg + kompozitte SE %18 + A-Fe katot gen-2).\n")

    md.append(ky.markdown_bolum())

    md.append("## 11. Li-iyon ile karşılaştırma (75 kWh paket)\n")
    md.append(ks.markdown_tablo(satirlar, g.brut_enerji_kWh))

    if grafikler:
        md.append("## 12. Grafikler\n")
        for ad, yol in yollar.items():
            md.append(f"![{ad}]({yol.name})\n")

    rapor_yolu = cikti / "RAPOR.md"
    rapor_yolu.write_text("\n".join(md), encoding="utf-8")
    return rapor_yolu
