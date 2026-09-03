"""Fiziksel sabitler (SI) ve sık kullanılan dönüşümler."""

FARADAY = 96485.33212        # C/mol
R_GAZ = 8.314462618          # J/(mol·K)
K_BOLTZMANN_EV = 8.617333262e-5  # eV/K
AVOGADRO = 6.02214076e23     # 1/mol
E_YUK = 1.602176634e-19      # C

T_ODA = 298.15               # K
C_TO_K = 273.15

# Faraday sabitinin mAh/mol karşılığı: 96485 C/mol / 3.6 C/mAh
FARADAY_MAH = FARADAY / 3.6  # ≈ 26801 mAh/mol

# Molar kütleler (g/mol)
M = {
    "H": 1.008,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "V": 50.942,
    "Cr": 51.996,
    "Mn": 54.938,
    "Fe": 55.845,
    "Co": 58.933,
    "Ni": 58.693,
    "Cu": 63.546,
    "Li": 6.94,
    "Mo": 95.95,
}


def molar_kutle(formul: dict[str, float]) -> float:
    """{'Na': 2, 'B': 12, 'H': 12} biçimindeki bir sözlükten molar kütle (g/mol)."""
    return sum(M[el] * n for el, n in formul.items())


def kutle_kesri(formul: dict[str, float], element: str) -> float:
    """Bileşikteki bir elementin kütle kesri (0-1)."""
    return M[element] * formul.get(element, 0.0) / molar_kutle(formul)


def teorik_kapasite_mah_g(molar_kutle_g: float, n_elektron: float) -> float:
    """Teorik özgül kapasite (mAh/g): n·F / M."""
    return n_elektron * FARADAY_MAH / molar_kutle_g
