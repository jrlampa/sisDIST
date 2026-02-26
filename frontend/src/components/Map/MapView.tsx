import { MapContainer, TileLayer } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import PoleMarker from './PoleMarker'
import ConductorLine from './ConductorLine'

interface Props {
  center: { lat: number; lon: number }
  zoom: number
  osmData?: any
  onCenterChange?: (c: { lat: number; lon: number }) => void
}

export default function MapView({ center, zoom, osmData }: Props) {
  const poles = osmData?.poles ?? []
  const towers = osmData?.towers ?? []
  const lines = osmData?.power_lines ?? []

  return (
    <MapContainer
      center={[center.lat, center.lon]}
      zoom={zoom}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {poles.map((p: any) => (
        <PoleMarker key={`pole-${p.osm_id}`} lat={p.lat} lon={p.lon} type="pole" tags={p.tags} />
      ))}
      {towers.map((t: any) => (
        <PoleMarker key={`tower-${t.osm_id}`} lat={t.lat} lon={t.lon} type="tower" tags={t.tags} />
      ))}
      {lines.map((l: any) => (
        <ConductorLine key={`line-${l.osm_id}`} geometry={l.geometry} tags={l.tags} />
      ))}
    </MapContainer>
  )
}
