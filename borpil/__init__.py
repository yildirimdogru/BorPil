"""
BorPil — elektrikli araçlar için lityumsuz, bor esaslı batarya tasarım ve simülasyon paketi.

Ana kimya: Na-metal anot | Na kloso-borat katı elektrolit | Na3V2(PO4)3 (NVP) katot.
Yardımcı yollar: Mg / Mg(CB11H12)2, doğrudan borhidrür yakıt pili (DBFC), teorik bor-hava sınırı.

Modüller
--------
sabitler      : fiziksel sabitler
malzemeler    : malzeme veri tabanı (yoğunluk, kapasite, potansiyel, maliyet, bor içeriği)
termodinamik  : Gibbs/Nernst, teorik kapasite ve enerji yoğunluğu hesapları
elektrolit    : kloso-borat iyonik iletkenliğinin Arrhenius modeli ve faz geçişleri
kimya_sicaklik: 10–45 °C penceresi taraması (bulk σ vs CCD/arayüz)
geometri      : [B12H12]2- ikosahedronu ve anyon boyutu; hücre/paket paketleme geometrisi
hucre         : katman yığını (stack) modeli → Wh/kg, Wh/L, bor kütlesi
paket         : EV paket boyutlandırma (enerji, gerilim, kütle, hacim, maliyet)
simulasyon    : eşdeğer devre + termal toplu model ile deşarj ve sürüş çevrimi simülasyonu
karsilastirma : Li-iyon (NMC811, LFP) ile karşılaştırma tablosu
rapor         : tüm hesapları çalıştırıp Markdown rapor ve grafikler üretir
"""

from . import (
    sabitler,
    malzemeler,
    termodinamik,
    elektrolit,
    geometri,
    hucre,
    paket,
    simulasyon,
    karsilastirma,
    kimya_sicaklik,
)

__all__ = [
    "sabitler",
    "malzemeler",
    "termodinamik",
    "elektrolit",
    "geometri",
    "hucre",
    "paket",
    "simulasyon",
    "karsilastirma",
    "kimya_sicaklik",
]

__version__ = "0.1.0"
