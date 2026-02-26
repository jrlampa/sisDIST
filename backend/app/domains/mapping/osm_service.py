"""OSM / Overpass API data fetching."""
import httpx
from app.core.config import get_settings
from app.domains.mapping.schemas import OSMResponse, OSMNode, OSMWay

settings = get_settings()

_OVERPASS_QUERY = """
[out:json][timeout:30];
(
  node["power"="pole"](around:{radius},{lat},{lon});
  node["power"="tower"](around:{radius},{lat},{lon});
  way["power"~"line|minor_line"](around:{radius},{lat},{lon});
  node["power"="substation"](around:{radius},{lat},{lon});
  node["power"="transformer"](around:{radius},{lat},{lon});
);
out body geom;
"""


async def fetch_osm_data(lat: float, lon: float, radius: int) -> OSMResponse:
    """Fetch electrical infrastructure data from OpenStreetMap Overpass API."""
    query = _OVERPASS_QUERY.format(lat=lat, lon=lon, radius=radius)
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(settings.overpass_url, data={"data": query})
        resp.raise_for_status()
        data = resp.json()

    elements = data.get("elements", [])
    poles: list[OSMNode] = []
    towers: list[OSMNode] = []
    power_lines: list[OSMWay] = []
    substations: list[OSMNode] = []

    for el in elements:
        tags = el.get("tags", {})
        power_tag = tags.get("power", "")

        if el["type"] == "node":
            node = OSMNode(osm_id=el["id"], lat=el["lat"], lon=el["lon"], tags=tags)
            if power_tag == "pole":
                poles.append(node)
            elif power_tag == "tower":
                towers.append(node)
            elif power_tag in ("substation", "transformer"):
                substations.append(node)
        elif el["type"] == "way":
            geometry = [{"lat": p["lat"], "lon": p["lon"]} for p in el.get("geometry", [])]
            way = OSMWay(osm_id=el["id"], nodes=el.get("nodes", []), tags=tags, geometry=geometry)
            power_lines.append(way)

    return OSMResponse(
        poles=poles,
        towers=towers,
        power_lines=power_lines,
        substations=substations,
        total_elements=len(elements),
    )
