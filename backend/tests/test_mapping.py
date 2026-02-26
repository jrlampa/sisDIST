"""Tests for mapping domain — coordinate conversion (no DB, no external APIs)."""
import pytest
from app.domains.mapping.service import MappingService
from app.domains.mapping.schemas import UTMConversionResponse


class TestCoordinateConversion:
    """Test UTM SIRGAS2000 ↔ WGS84 conversions."""

    def setup_method(self):
        self.service = MappingService()

    def test_convert_known_coordinates(self):
        """Test coordinates: UTM SIRGAS2000 zone 23S E=714316 N=7549084 → -22.15018, -42.92185"""
        result = self.service.convert_utm_to_wgs84(
            easting=714316.0,
            northing=7549084.0,
            zone=23,
            hemisphere="S",
        )
        assert isinstance(result, UTMConversionResponse)
        assert result.lat == pytest.approx(-22.15018, abs=0.02)
        assert result.lon == pytest.approx(-42.92185, abs=0.02)

    def test_returns_correct_schema(self):
        result = self.service.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "S")
        assert result.easting == 714316.0
        assert result.northing == 7549084.0
        assert result.zone == 23
        assert result.hemisphere == "S"
        assert result.epsg > 0

    def test_hemisphere_uppercase_lowercase(self):
        r1 = self.service.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "S")
        r2 = self.service.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "s")
        # Both should give the same result (case-insensitive)
        assert r1.lat == pytest.approx(r2.lat, rel=1e-3)
        assert r1.lon == pytest.approx(r2.lon, rel=1e-3)

    def test_southern_hemisphere_negative_lat(self):
        """Southern hemisphere should produce negative latitude."""
        result = self.service.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "S")
        assert result.lat < 0

    def test_rio_de_janeiro_longitude_range(self):
        """Rio de Janeiro longitudes should be in range -45 to -40."""
        result = self.service.convert_utm_to_wgs84(714316.0, 7549084.0, 23, "S")
        assert -45.0 < result.lon < -40.0
