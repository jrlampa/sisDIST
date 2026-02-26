"""Voltage drop calculation — ABNT NBR 5410.

Formula:
    3-phase: ΔV = (√3 × I × L × (R·cosφ + X·sinφ)) / 1000
    1-phase: ΔV = (2 × I × L × (R·cosφ + X·sinφ)) / 1000
    ΔV%     = (ΔV / Vn) × 100
Limit:
    BT: 7% (NBR 5410) — 5% for service entrance
    MT: 5% (Prodist)
"""
import math
from app.domains.calculations.schemas import VoltageDropRequest, VoltageDropResponse

# Conductor properties table — resistance (Ω/km) and reactance (Ω/km)
# Source: ABNT NBR 5410 / manufacturer datasheets
_CONDUCTOR_TABLE: dict[str, dict[float, tuple[float, float]]] = {
    "CA": {
        16:  (1.915, 0.335),
        25:  (1.200, 0.320),
        35:  (0.868, 0.310),
        50:  (0.641, 0.300),
        70:  (0.443, 0.290),
        95:  (0.320, 0.280),
        120: (0.253, 0.275),
        150: (0.206, 0.270),
        185: (0.164, 0.265),
        240: (0.125, 0.260),
    },
    "CAA": {
        16:  (1.900, 0.340),
        25:  (1.190, 0.325),
        35:  (0.860, 0.315),
        50:  (0.630, 0.305),
        70:  (0.435, 0.295),
        95:  (0.315, 0.285),
        120: (0.248, 0.278),
        150: (0.200, 0.272),
        185: (0.160, 0.268),
        240: (0.122, 0.262),
    },
    "ACSR": {
        16:  (1.900, 0.340),
        25:  (1.190, 0.325),
        35:  (0.860, 0.315),
        50:  (0.630, 0.305),
        70:  (0.435, 0.295),
        95:  (0.315, 0.285),
        120: (0.248, 0.278),
        150: (0.200, 0.272),
        185: (0.160, 0.268),
        240: (0.122, 0.262),
    },
}

_VOLTAGE_LIMITS: dict[str, float] = {
    "BT": 7.0,
    "MT": 5.0,
    "AT": 3.0,
}


def _get_conductor_properties(conductor_type: str, cross_section: float) -> tuple[float, float]:
    """Return (resistance Ω/km, reactance Ω/km) for the given conductor."""
    table = _CONDUCTOR_TABLE.get(conductor_type.upper())
    if table is None:
        raise ValueError(f"Tipo de condutor desconhecido: {conductor_type}. Use CA, CAA ou ACSR.")

    # Exact match
    if cross_section in table:
        return table[cross_section]

    # Interpolate between nearest values
    sections = sorted(table.keys())
    if cross_section < sections[0] or cross_section > sections[-1]:
        raise ValueError(
            f"Seção {cross_section} mm² fora do intervalo suportado ({sections[0]}–{sections[-1]} mm²)."
        )
    for i in range(len(sections) - 1):
        s_lo, s_hi = sections[i], sections[i + 1]
        if s_lo <= cross_section <= s_hi:
            t = (cross_section - s_lo) / (s_hi - s_lo)
            r = table[s_lo][0] + t * (table[s_hi][0] - table[s_lo][0])
            x = table[s_lo][1] + t * (table[s_hi][1] - table[s_lo][1])
            return r, x
    raise ValueError(f"Não foi possível interpolar para seção {cross_section} mm².")


def calculate_voltage_drop(request: VoltageDropRequest) -> VoltageDropResponse:
    """Calculate voltage drop per ABNT NBR 5410."""
    resistance, reactance = _get_conductor_properties(request.conductor_type, request.cross_section)

    cos_phi = request.power_factor
    sin_phi = math.sqrt(max(0.0, 1.0 - cos_phi ** 2))
    length_km = request.length / 1000.0

    impedance_factor = resistance * cos_phi + reactance * sin_phi

    if request.phases == 3:
        delta_v = math.sqrt(3) * request.current * length_km * impedance_factor
    else:
        delta_v = 2.0 * request.current * length_km * impedance_factor

    pct = (delta_v / request.nominal_voltage) * 100.0
    limit = _VOLTAGE_LIMITS.get(request.voltage_level.upper(), 7.0)

    return VoltageDropResponse(
        voltage_drop_v=round(delta_v, 4),
        voltage_drop_pct=round(pct, 4),
        limit_pct=limit,
        compliant=pct <= limit,
        resistance=resistance,
        reactance=reactance,
    )
