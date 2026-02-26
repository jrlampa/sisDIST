import { Polyline, Popup } from 'react-leaflet'

interface Coord { lat: number; lon: number }

interface Props {
  geometry: Coord[]
  tags?: Record<string, string>
}

export default function ConductorLine({ geometry, tags = {} }: Props) {
  if (geometry.length < 2) return null
  const positions = geometry.map((c) => [c.lat, c.lon] as [number, number])
  const color = tags.voltage ? '#dc2626' : '#2563eb'

  return (
    <Polyline positions={positions} color={color} weight={2} opacity={0.8}>
      <Popup>
        <strong>Linha de Energia</strong>
        <br />
        {tags.voltage && <span>Tensão: {tags.voltage}<br /></span>}
        {tags.cables && <span>Cabos: {tags.cables}<br /></span>}
        {tags.name && <span>{tags.name}<br /></span>}
      </Popup>
    </Polyline>
  )
}
