"""Tests for security utilities and OSM service (mocked)."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.security import generate_secret_key, hash_string


class TestSecurity:
    """Test cryptographic utilities."""

    def test_generate_secret_key_default_length(self):
        key = generate_secret_key()
        # token_hex(32) → 64 hex chars
        assert len(key) == 64

    def test_generate_secret_key_custom_length(self):
        key = generate_secret_key(16)
        assert len(key) == 32

    def test_generate_secret_key_is_hex(self):
        key = generate_secret_key()
        int(key, 16)  # raises ValueError if not valid hex

    def test_generate_secret_key_unique(self):
        k1 = generate_secret_key()
        k2 = generate_secret_key()
        assert k1 != k2

    def test_hash_string_known_value(self):
        """SHA-256 of 'hello' is well-known."""
        result = hash_string("hello")
        assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    def test_hash_string_is_lowercase_hex(self):
        result = hash_string("test")
        assert result == result.lower()
        assert all(c in "0123456789abcdef" for c in result)

    def test_hash_string_length(self):
        result = hash_string("any string")
        assert len(result) == 64

    def test_hash_string_deterministic(self):
        assert hash_string("abc") == hash_string("abc")

    def test_hash_string_different_inputs(self):
        assert hash_string("abc") != hash_string("abd")


class TestOSMService:
    """Test OSM/Overpass service with mocked HTTP client."""

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_data_poles(self):
        from app.domains.mapping.osm_service import fetch_osm_data

        fake_response = {
            "elements": [
                {"type": "node", "id": 1, "lat": -22.15, "lon": -42.92, "tags": {"power": "pole"}},
                {"type": "node", "id": 2, "lat": -22.16, "lon": -42.93, "tags": {"power": "tower"}},
            ]
        }
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_response

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.osm_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await fetch_osm_data(-22.15018, -42.92185, 500)

        assert len(result.poles) == 1
        assert result.poles[0].osm_id == 1
        assert len(result.towers) == 1
        assert result.towers[0].osm_id == 2
        assert result.total_elements == 2

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_data_power_lines(self):
        from app.domains.mapping.osm_service import fetch_osm_data

        fake_response = {
            "elements": [
                {
                    "type": "way",
                    "id": 100,
                    "nodes": [1, 2],
                    "tags": {"power": "line"},
                    "geometry": [
                        {"lat": -22.15, "lon": -42.92},
                        {"lat": -22.16, "lon": -42.93},
                    ],
                }
            ]
        }
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_response

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.osm_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await fetch_osm_data(-22.15018, -42.92185, 100)

        assert len(result.power_lines) == 1
        assert result.power_lines[0].osm_id == 100
        assert len(result.power_lines[0].geometry) == 2

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_data_substations(self):
        from app.domains.mapping.osm_service import fetch_osm_data

        fake_response = {
            "elements": [
                {"type": "node", "id": 99, "lat": -22.15, "lon": -42.92, "tags": {"power": "substation"}},
                {"type": "node", "id": 98, "lat": -22.16, "lon": -42.93, "tags": {"power": "transformer"}},
            ]
        }
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_response

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.osm_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await fetch_osm_data(-22.15018, -42.92185, 1000)

        assert len(result.substations) == 2

    @pytest.mark.asyncio(mode="auto")
    async def test_fetch_osm_data_empty(self):
        from app.domains.mapping.osm_service import fetch_osm_data

        fake_response = {"elements": []}
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = fake_response

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_resp)

        with patch("app.domains.mapping.osm_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
            mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await fetch_osm_data(-22.15018, -42.92185, 500)

        assert result.total_elements == 0
        assert result.poles == []
        assert result.power_lines == []
        assert result.substations == []
