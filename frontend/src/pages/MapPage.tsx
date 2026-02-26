import MapView from '../components/Map/MapView'
import MapControls from '../components/Map/MapControls'
import { useMap } from '../hooks/useMap'

export default function MapPage() {
  const { center, setCenter, zoom, osmData, loading, error, fetchOsm } = useMap()

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-800 mb-4">Mapa de Infraestrutura</h1>
      <MapControls onFetch={fetchOsm} center={center} loading={loading} />
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <div className="mt-4 rounded-lg overflow-hidden shadow" style={{ height: '65vh' }}>
        <MapView center={center} zoom={zoom} osmData={osmData} onCenterChange={setCenter} />
      </div>
      {osmData && (
        <div className="mt-2 text-sm text-gray-500">
          {osmData.total_elements} elementos encontrados —{' '}
          {osmData.poles?.length ?? 0} postes, {osmData.power_lines?.length ?? 0} linhas
        </div>
      )}
    </div>
  )
}
