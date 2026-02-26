"""Mechanical stress calculation for poles — ABNT NBR 8458/8798.

Loads considered:
    - Wind load on conductors: Fw = Cf × q × d × L
      where q = 0.613 × V² (dynamic pressure, Pa), Cf = 1.2 (drag), d = diameter (m), L = span (m)
    - Weight load on conductors: Wc = (weight_kg_per_km / 1000) × span × g
    - Tension load: from cable tension at the attachment point
    - Moment at base: M = resultant × attachment_height
Safety factor requirement: ≥ 2.5 (NBR 8458/8798)
"""
import math
from app.domains.calculations.schemas import MechanicalStressRequest, MechanicalStressResponse

_GRAVITY = 9.80665  # m/s²
_DRAG_COEFF = 1.2   # Cf for cylindrical conductor
_AIR_DENSITY_FACTOR = 0.613  # ½ρ for standard air density (ρ=1.225 kg/m³)


def calculate_mechanical_stress(request: MechanicalStressRequest) -> MechanicalStressResponse:
    """Calculate mechanical stress on a pole per ABNT NBR 8458/8798."""
    # Dynamic wind pressure (Pa)
    q = _AIR_DENSITY_FACTOR * request.wind_speed ** 2

    # Conductor diameter in meters
    d_m = request.conductor_diameter / 1000.0

    # Wind load per conductor (N) — acts horizontally
    fw = _DRAG_COEFF * q * d_m * request.span_length
    fw = max(fw, 0.0)

    # Weight load per conductor (N) — acts vertically
    weight_n_per_m = (request.conductor_weight / 1000.0) * _GRAVITY  # N/m
    wc = weight_n_per_m * request.span_length

    # Tension load: horizontal component from cable tension (N)
    # Simplified: at a deviation point assume full tension on each side cancel,
    # but at a dead-end or angle pole the resultant tension is the cable tension itself.
    # Here we model the horizontal pull at attachment as the given tension.
    tension_h = request.conductor_tension  # N

    # Total horizontal force per conductor at attachment
    horizontal_per_conductor = math.sqrt(fw ** 2 + tension_h ** 2)

    # Total forces for all conductors
    total_horizontal = horizontal_per_conductor * request.num_conductors
    total_vertical = wc * request.num_conductors

    # Total resultant force at attachment (N)
    total_resultant = math.sqrt(total_horizontal ** 2 + total_vertical ** 2)

    # Bending moment at base (N·m) — using attachment height
    moment = total_horizontal * request.attachment_height

    return MechanicalStressResponse(
        wind_load_per_conductor_n=round(fw, 2),
        weight_load_per_conductor_n=round(wc, 2),
        tension_load_n=round(tension_h, 2),
        total_resultant_n=round(total_resultant, 2),
        moment_nm=round(moment, 2),
    )
