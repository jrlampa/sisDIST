import { useState } from 'react'

interface Props {
  center: { lat: number; lon: number }
  loading: boolean
  onFetch: (lat: number, lon: number, radius: number) => void
}

export default function MapControls({ center, loading, onFetch }: Props) {
  const [lat, setLat] = useState(center.lat.toString())
  const [lon, setLon] = useState(center.lon.toString())
  const [radius, setRadius] = useState('500')

  const handleSearch = () => {
    const latN = parseFloat(lat)
    const lonN = parseFloat(lon)
    const radN = parseInt(radius, 10)
    if (isNaN(latN) || isNaN(lonN) || isNaN(radN)) return
    onFetch(latN, lonN, radN)
  }

  return (
    <div className="flex flex-wrap gap-3 items-end bg-white p-4 rounded-lg shadow border">
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Latitude</label>
        <input
          type="number"
          value={lat}
          onChange={(e) => setLat(e.target.value)}
          className="border rounded px-2 py-1 text-sm w-32"
          step="0.00001"
        />
      </div>
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Longitude</label>
        <input
          type="number"
          value={lon}
          onChange={(e) => setLon(e.target.value)}
          className="border rounded px-2 py-1 text-sm w-32"
          step="0.00001"
        />
      </div>
      <div>
        <label className="block text-xs font-medium text-gray-600 mb-1">Raio (m)</label>
        <select
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value="100">100m</option>
          <option value="500">500m</option>
          <option value="1000">1 km</option>
          <option value="2000">2 km</option>
          <option value="5000">5 km</option>
        </select>
      </div>
      <button
        onClick={handleSearch}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 text-sm"
      >
        {loading ? 'Buscando...' : 'Buscar OSM'}
      </button>
    </div>
  )
}
