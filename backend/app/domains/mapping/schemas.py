"""Mapping domain schemas."""
from pydantic import BaseModel, Field
from typing import Any


class OSMNode(BaseModel):
    osm_id: int
    lat: float
    lon: float
    tags: dict[str, Any] = {}


class OSMWay(BaseModel):
    osm_id: int
    nodes: list[int]
    tags: dict[str, Any] = {}
    geometry: list[dict[str, float]] = []


class OSMResponse(BaseModel):
    poles: list[OSMNode] = []
    towers: list[OSMNode] = []
    power_lines: list[OSMWay] = []
    substations: list[OSMNode] = []
    total_elements: int = 0


class ElevationResponse(BaseModel):
    lat: float
    lon: float
    elevation: float = Field(..., description="Altitude em metros (SRTM 90m)")
    dataset: str = "srtm90m"


class UTMConversionResponse(BaseModel):
    easting: float
    northing: float
    zone: int
    hemisphere: str
    lat: float = Field(..., description="Latitude WGS84")
    lon: float = Field(..., description="Longitude WGS84")
    epsg: int = Field(..., description="Código EPSG da projeção de entrada")
