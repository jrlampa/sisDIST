"""Mapping API endpoints — OSM, elevation, coordinate conversion."""
from fastapi import APIRouter, Query, HTTPException
from app.domains.mapping.service import MappingService
from app.domains.mapping.schemas import OSMResponse, ElevationResponse, UTMConversionResponse

router = APIRouter()
_service = MappingService()


@router.get("/osm", response_model=OSMResponse, summary="Buscar dados OSM ao redor de coordenadas")
async def get_osm_data(
    lat: float = Query(..., description="Latitude WGS84"),
    lon: float = Query(..., description="Longitude WGS84"),
    radius: int = Query(500, ge=50, le=5000, description="Raio em metros"),
):
    """Busca postes, linhas e subestações do OpenStreetMap via Overpass API."""
    try:
        return await _service.fetch_osm_data(lat, lon, radius)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erro ao consultar OSM: {exc}") from exc


@router.get("/elevation", response_model=ElevationResponse, summary="Obter elevação de coordenadas")
async def get_elevation(
    lat: float = Query(..., description="Latitude WGS84"),
    lon: float = Query(..., description="Longitude WGS84"),
):
    """Obtém altitude via OpenTopoData (SRTM 90m)."""
    try:
        return await _service.fetch_elevation(lat, lon)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erro ao obter elevação: {exc}") from exc


@router.get(
    "/convert-utm",
    response_model=UTMConversionResponse,
    summary="Converter coordenadas UTM SIRGAS2000 para WGS84",
)
async def convert_utm(
    easting: float = Query(..., description="Coordenada Leste (E) em metros"),
    northing: float = Query(..., description="Coordenada Norte (N) em metros"),
    zone: int = Query(23, description="Fuso UTM"),
    hemisphere: str = Query("S", description="Hemisfério: N ou S"),
):
    """Converte coordenadas UTM SIRGAS2000 (EPSG:31983) para WGS84."""
    try:
        return _service.convert_utm_to_wgs84(easting, northing, zone, hemisphere)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Erro na conversão: {exc}") from exc
