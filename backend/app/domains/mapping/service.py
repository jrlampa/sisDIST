"""Mapping service — orchestrates OSM fetching, elevation and coordinate conversion."""
import httpx
from app.core.config import get_settings
from app.domains.mapping.schemas import OSMResponse, ElevationResponse, UTMConversionResponse
from app.domains.mapping.osm_service import fetch_osm_data
from pyproj import Transformer

settings = get_settings()


# EPSG:31983 = SIRGAS2000 / UTM zone 23S (covers most of Rio de Janeiro)
_EPSG_SIRGAS_23S = 31983
_TRANSFORMER_TO_WGS84 = Transformer.from_crs(f"EPSG:{_EPSG_SIRGAS_23S}", "EPSG:4326", always_xy=True)


class MappingService:
    """Service for geospatial operations: OSM, elevation and coordinate conversion."""

    async def fetch_osm_data(self, lat: float, lon: float, radius: int) -> OSMResponse:
        return await fetch_osm_data(lat, lon, radius)

    async def fetch_elevation(self, lat: float, lon: float) -> ElevationResponse:
        url = f"{settings.opentopodata_url}?locations={lat},{lon}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        result = data["results"][0]
        return ElevationResponse(lat=lat, lon=lon, elevation=result["elevation"])

    def convert_utm_to_wgs84(
        self, easting: float, northing: float, zone: int, hemisphere: str
    ) -> UTMConversionResponse:
        # SIRGAS2000 UTM South: EPSG = 31960 + zone  (zone 23S → EPSG:31983)
        # SIRGAS2000 UTM North: EPSG = 31954 + zone  (zone 18N → EPSG:31972)
        if hemisphere.upper() == "S":
            epsg = 31960 + zone
        else:
            epsg = 31954 + zone
        try:
            transformer = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
        except Exception:
            transformer = _TRANSFORMER_TO_WGS84
            epsg = _EPSG_SIRGAS_23S
        lon, lat = transformer.transform(easting, northing)
        return UTMConversionResponse(
            easting=easting,
            northing=northing,
            zone=zone,
            hemisphere=hemisphere,
            lat=lat,
            lon=lon,
            epsg=epsg,
        )
