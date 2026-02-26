"""Tests for calculation domain — pure Python, no database needed."""
import math
import pytest
from app.domains.calculations.voltage_drop import calculate_voltage_drop, _get_conductor_properties
from app.domains.calculations.mechanical_stress import calculate_mechanical_stress
from app.domains.calculations.schemas import VoltageDropRequest, MechanicalStressRequest


# ── Conductor property lookup ────────────────────────────────────────────────

class TestConductorProperties:
    def test_exact_match_ca_50(self):
        r, x = _get_conductor_properties("CA", 50)
        assert r == pytest.approx(0.641)
        assert x == pytest.approx(0.300)

    def test_exact_match_ca_95(self):
        r, x = _get_conductor_properties("CA", 95)
        assert r == pytest.approx(0.320)
        assert x == pytest.approx(0.280)

    def test_case_insensitive(self):
        r1, _ = _get_conductor_properties("ca", 50)
        r2, _ = _get_conductor_properties("CA", 50)
        assert r1 == r2

    def test_interpolation(self):
        # 60 mm² lies between 50 and 70 mm²
        r, x = _get_conductor_properties("CA", 60)
        assert 0.443 < r < 0.641
        assert 0.290 < x < 0.300

    def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="desconhecido"):
            _get_conductor_properties("UNKNOWN", 50)

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            _get_conductor_properties("CA", 1000)

    def test_caa_exact(self):
        r, x = _get_conductor_properties("CAA", 70)
        assert r == pytest.approx(0.435)

    def test_acsr_exact(self):
        r, x = _get_conductor_properties("ACSR", 120)
        assert r == pytest.approx(0.248)


# ── Voltage drop 3-phase ────────────────────────────────────────────────────

class TestVoltageDropThreePhase:
    def _req(self, **kwargs):
        defaults = dict(
            current=100.0,
            length=500.0,
            conductor_type="CA",
            cross_section=50,
            power_factor=0.92,
            phases=3,
            nominal_voltage=220.0,
            voltage_level="BT",
        )
        defaults.update(kwargs)
        return VoltageDropRequest(**defaults)

    def test_basic_calculation(self):
        """Manual: ΔV = √3 × 100 × 0.5 × (0.641×0.92 + 0.300×0.392) ≈ 64.8 V"""
        req = self._req()
        resp = calculate_voltage_drop(req)
        assert resp.voltage_drop_v > 0
        assert resp.voltage_drop_pct > 0
        assert resp.standard == "ABNT NBR 5410"

    def test_known_value(self):
        """Verify formula manually: √3 × 100 × 0.5 km × (0.641×0.92 + 0.300×sin)"""
        req = self._req()
        r, x = 0.641, 0.300
        cos_phi = 0.92
        sin_phi = math.sqrt(1 - cos_phi ** 2)
        expected = math.sqrt(3) * 100 * 0.5 * (r * cos_phi + x * sin_phi)
        resp = calculate_voltage_drop(req)
        assert resp.voltage_drop_v == pytest.approx(expected, rel=1e-3)

    def test_percentage_formula(self):
        req = self._req(nominal_voltage=220.0)
        resp = calculate_voltage_drop(req)
        expected_pct = (resp.voltage_drop_v / 220.0) * 100
        assert resp.voltage_drop_pct == pytest.approx(expected_pct, rel=1e-3)

    def test_bt_limit_is_7pct(self):
        req = self._req(voltage_level="BT")
        resp = calculate_voltage_drop(req)
        assert resp.limit_pct == pytest.approx(7.0)

    def test_mt_limit_is_5pct(self):
        req = self._req(voltage_level="MT")
        resp = calculate_voltage_drop(req)
        assert resp.limit_pct == pytest.approx(5.0)

    def test_compliant_for_short_line(self):
        req = self._req(length=10.0, current=10.0)
        resp = calculate_voltage_drop(req)
        assert resp.compliant is True

    def test_non_compliant_for_long_heavy_line(self):
        req = self._req(length=5000.0, current=200.0, cross_section=16)
        resp = calculate_voltage_drop(req)
        assert resp.compliant is False

    def test_conductor_properties_returned(self):
        req = self._req()
        resp = calculate_voltage_drop(req)
        assert resp.resistance == pytest.approx(0.641)
        assert resp.reactance == pytest.approx(0.300)


# ── Voltage drop 1-phase ────────────────────────────────────────────────────

class TestVoltageDropOnePhase:
    def _req(self, **kwargs):
        defaults = dict(
            current=50.0,
            length=200.0,
            conductor_type="CA",
            cross_section=25,
            power_factor=0.85,
            phases=1,
            nominal_voltage=127.0,
            voltage_level="BT",
        )
        defaults.update(kwargs)
        return VoltageDropRequest(**defaults)

    def test_formula_factor_is_two(self):
        req = self._req()
        r, x = 1.200, 0.320
        cos_phi = 0.85
        sin_phi = math.sqrt(1 - cos_phi ** 2)
        expected = 2 * 50.0 * 0.2 * (r * cos_phi + x * sin_phi)
        resp = calculate_voltage_drop(req)
        assert resp.voltage_drop_v == pytest.approx(expected, rel=1e-3)

    def test_single_phase_higher_than_three_phase(self):
        """Single-phase always gives higher drop than 3-phase for same params."""
        base = dict(current=50, length=200, conductor_type="CA", cross_section=25,
                    power_factor=0.85, nominal_voltage=220.0, voltage_level="BT")
        resp1 = calculate_voltage_drop(VoltageDropRequest(phases=1, **base))
        resp3 = calculate_voltage_drop(VoltageDropRequest(phases=3, **base))
        assert resp1.voltage_drop_v > resp3.voltage_drop_v


# ── Mechanical stress ────────────────────────────────────────────────────────

class TestMechanicalStress:
    def _req(self, **kwargs):
        defaults = dict(
            wind_speed=25.0,
            conductor_diameter=14.4,
            span_length=60.0,
            conductor_weight=407.0,
            conductor_tension=5000.0,
            pole_height=11.0,
            attachment_height=10.0,
            num_conductors=3,
        )
        defaults.update(kwargs)
        return MechanicalStressRequest(**defaults)

    def test_returns_positive_values(self):
        req = self._req()
        resp = calculate_mechanical_stress(req)
        assert resp.wind_load_per_conductor_n > 0
        assert resp.weight_load_per_conductor_n > 0
        assert resp.tension_load_n > 0
        assert resp.total_resultant_n > 0
        assert resp.moment_nm > 0

    def test_wind_load_formula(self):
        """Fw = 1.2 × q × d × L, q = 0.613 × V²"""
        req = self._req(wind_speed=25.0, conductor_diameter=14.4, span_length=60.0, num_conductors=1)
        q = 0.613 * 25.0 ** 2
        d_m = 14.4 / 1000.0
        expected_fw = 1.2 * q * d_m * 60.0
        resp = calculate_mechanical_stress(req)
        assert resp.wind_load_per_conductor_n == pytest.approx(expected_fw, rel=1e-3)

    def test_weight_load_formula(self):
        """Wc = (weight_kg_per_km / 1000) × span × g"""
        req = self._req(conductor_weight=407.0, span_length=60.0)
        expected_wc = (407.0 / 1000.0) * 60.0 * 9.80665
        resp = calculate_mechanical_stress(req)
        assert resp.weight_load_per_conductor_n == pytest.approx(expected_wc, rel=1e-3)

    def test_moment_formula(self):
        """M = total_horizontal × attachment_height"""
        req = self._req(attachment_height=10.0)
        resp = calculate_mechanical_stress(req)
        assert resp.moment_nm > 0
        # moment should scale with attachment height
        req2 = self._req(attachment_height=5.0)
        resp2 = calculate_mechanical_stress(req2)
        assert resp.moment_nm == pytest.approx(resp2.moment_nm * 2, rel=1e-2)

    def test_more_conductors_higher_load(self):
        req3 = self._req(num_conductors=3)
        req1 = self._req(num_conductors=1)
        resp3 = calculate_mechanical_stress(req3)
        resp1 = calculate_mechanical_stress(req1)
        assert resp3.total_resultant_n > resp1.total_resultant_n

    def test_standard_label(self):
        req = self._req()
        resp = calculate_mechanical_stress(req)
        assert resp.standard == "ABNT NBR 8458/8798"

    def test_safety_factor_field(self):
        req = self._req()
        resp = calculate_mechanical_stress(req)
        assert resp.safety_factor_required == pytest.approx(2.5)

    def test_higher_wind_higher_load(self):
        req_low = self._req(wind_speed=10.0)
        req_high = self._req(wind_speed=40.0)
        resp_low = calculate_mechanical_stress(req_low)
        resp_high = calculate_mechanical_stress(req_high)
        assert resp_high.wind_load_per_conductor_n > resp_low.wind_load_per_conductor_n
