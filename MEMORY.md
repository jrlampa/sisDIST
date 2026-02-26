# sisDIST — Project Memory (RAG/Context File)

## 1. Mission
sisDIST é uma ferramenta enterprise para engenheiros elétricos brasileiros realizar:
- Cálculos elétricos (queda de tensão — ABNT NBR 5410)
- Cálculos mecânicos (esforço mecânico em postes — ABNT NBR 8458/8798)
- Listas de material para redes de distribuição aérea
- Levantamento topográfico com APIs públicas gratuitas (OSM, OpenTopoData)
- Gêmeo digital da infraestrutura (postes, estruturas MT/BT, condutores, equipamentos)
- Suporte às concessionárias Enel-RJ e Light
- Georeferenciamento no sistema SIRGAS2000 UTM

## 2. Architecture
- **Pattern**: DDD (Domain Driven Design) — thin frontend, smart backend
- **Docker first**: all services containerized
- **Languages**: Python 3.12 (backend), TypeScript/React 18 (frontend)
- **Database**: PostgreSQL 15 + PostGIS (EPSG:31983 — SIRGAS2000 UTM Zone 23S)
- **Cache**: Redis
- **Proxy**: Nginx
- **Zero cost**: only free/public APIs

## 3. Domain Model

### Project
- Represents a distribution network engineering project
- Has a name, description, concessionaire (Enel-RJ or Light), and geographic area (Polygon)
- Contains poles, conductors, and equipment

### Pole (Poste)
- Code, location (PostGIS Point), elevation, pole_type, pole_height, pole_class
- Types: concrete (concreto), wood (madeira), steel (aço)
- Classes: as per NBR specification

### Conductor (Condutor)
- Connects two poles (pole_from_id → pole_to_id)
- Types: CA (All Aluminum), CAA (Aluminum-Steel), ACSR
- Cross sections: 16, 25, 35, 50, 70, 95, 120, 150, 185, 240 mm²
- Voltage levels: BT (baixa tensão), MT (média tensão)

### Equipment (Equipamento)
- Attached to a pole
- Types: transformer (transformador), capacitor, lightning_arrester (para-raios), fuse, insulator

## 4. Key Algorithms

### Voltage Drop (Queda de Tensão) — ABNT NBR 5410
- 3-phase: ΔV = (√3 × I × L × (R×cosφ + X×sinφ)) / 1000
- 1-phase: ΔV = (2 × I × L × (R×cosφ + X×sinφ)) / 1000
- Percentage: ΔV% = (ΔV / Vn) × 100
- Limit BT: 7% (NBR 5410), 5% for service entrance

### Mechanical Stress — ABNT NBR 8458/8798
- Wind load: Fw = Cf × q × d × L (Cf=1.2 drag coeff, q=dynamic pressure Pa)
- Wind pressure: q = 0.613 × V² (V in m/s)
- Weight load: Wc = ρ × A × L × g
- Tension force: T = weight_span × Wc / (2 × sag)
- Total resultant: Fr = √(Fw² + T²) per attachment
- Safety factor (coef. segurança): ≥ 2.5

### Conductor Properties (ABNT NBR tables)
| Cross Section (mm²) | Type | R (Ω/km) | X (Ω/km) |
|---------------------|------|-----------|-----------|
| 16  | CA  | 1.915 | 0.335 |
| 25  | CA  | 1.200 | 0.320 |
| 35  | CA  | 0.868 | 0.310 |
| 50  | CA  | 0.641 | 0.300 |
| 70  | CA  | 0.443 | 0.290 |
| 95  | CA  | 0.320 | 0.280 |
| 120 | CA  | 0.253 | 0.275 |
| 150 | CA  | 0.206 | 0.270 |
| 185 | CA  | 0.164 | 0.265 |
| 240 | CA  | 0.125 | 0.260 |

## 5. API Integrations

### Overpass API (OSM)
- URL: https://overpass-api.de/api/interpreter
- Query poles: node["power"="pole"](around:RADIUS,LAT,LON)
- Query lines: way["power"~"line|minor_line"](around:RADIUS,LAT,LON)
- No authentication needed
- Rate limit: be respectful, cache responses in Redis

### OpenTopoData Elevation API
- URL: https://api.opentopodata.org/v1/srtm90m
- Query: GET ?locations=LAT,LON
- Returns elevation in meters (SRTM 90m resolution)
- No authentication needed

## 6. Coordinate Systems

### SIRGAS2000 UTM Zone 23S
- EPSG: 31983
- Used for all storage and calculations
- Zone 23K covers most of Rio de Janeiro state

### WGS84 (GPS / Leaflet maps)
- EPSG: 4326
- Used for frontend display and OSM API calls

### Conversion (pyproj)
```python
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)
lon, lat = transformer.transform(easting, northing)
```

## 7. Test Coordinates
- UTM SIRGAS2000 Zone 23S (EPSG:31983): Easting=714316, Northing=7549084
- Decimal degrees: lat=-22.15018, lon=-42.92185
- Location: Região Serrana do Rio de Janeiro
- Test radii: 100m, 500m, 1km
- Note: The zone letter "K" in "23K" denotes the latitude band (MGRS notation); the EPSG for zone 23S is 31983.

## 8. Standards Reference
- ABNT NBR 5410:2004 — Instalações elétricas de baixa tensão
- ABNT NBR 8458:1984 — Postes de madeira para redes de distribuição
- ABNT NBR 8798:1985 — Instalação de postes de concreto
- Aneel Prodist Módulo 8 — Qualidade de energia elétrica (limites de tensão)
- Aneel Resolução 414/2010 — Condições gerais de fornecimento
