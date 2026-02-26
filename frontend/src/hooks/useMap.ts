import { useState, useCallback } from 'react'
import { mappingApi } from '../services/api'
import { DEFAULT_CENTER } from '../services/mapService'

export function useMap() {
  const [center, setCenter] = useState(DEFAULT_CENTER)
  const [zoom, setZoom] = useState(13)
  const [osmData, setOsmData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchOsm = useCallback(async (lat: number, lon: number, radius = 500) => {
    setLoading(true)
    setError(null)
    try {
      const data = await mappingApi.osm(lat, lon, radius)
      setOsmData(data)
    } catch (err: any) {
      setError(err?.message || 'Erro ao buscar dados OSM')
    } finally {
      setLoading(false)
    }
  }, [])

  return { center, setCenter, zoom, setZoom, osmData, loading, error, fetchOsm }
}
