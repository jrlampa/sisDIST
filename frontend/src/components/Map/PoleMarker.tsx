import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'

const poleIcon = L.divIcon({
  className: '',
  html: '<div style="width:10px;height:10px;background:#2563eb;border:2px solid white;border-radius:50%;"></div>',
  iconSize: [10, 10],
  iconAnchor: [5, 5],
})

const towerIcon = L.divIcon({
  className: '',
  html: '<div style="width:12px;height:12px;background:#dc2626;border:2px solid white;transform:rotate(45deg);"></div>',
  iconSize: [12, 12],
  iconAnchor: [6, 6],
})

interface Props {
  lat: number
  lon: number
  type: 'pole' | 'tower'
  tags?: Record<string, string>
}

export default function PoleMarker({ lat, lon, type, tags = {} }: Props) {
  const icon = type === 'pole' ? poleIcon : towerIcon
  const label = type === 'pole' ? 'Poste' : 'Torre'
  return (
    <Marker position={[lat, lon]} icon={icon}>
      <Popup>
        <strong>{label}</strong>
        <br />
        {tags.ref && <span>Ref: {tags.ref}<br /></span>}
        {tags.height && <span>Altura: {tags.height}m<br /></span>}
        {tags.material && <span>Material: {tags.material}<br /></span>}
        <small>
          {lat.toFixed(5)}, {lon.toFixed(5)}
        </small>
      </Popup>
    </Marker>
  )
}
