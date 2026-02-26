import { useState } from 'react'
import { useCreatePole } from '../../hooks/useInfrastructure'

export default function PoleForm({ projectId, onCreated }: { projectId?: number; onCreated?: () => void }) {
  const [code, setCode] = useState('')
  const [poleType, setPoleType] = useState('concreto')
  const [lat, setLat] = useState('')
  const [lon, setLon] = useState('')
  const [elevation, setElevation] = useState('')
  const [height, setHeight] = useState('')
  const createMutation = useCreatePole()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!code.trim()) return
    createMutation.mutate(
      {
        code: code.trim(),
        pole_type: poleType,
        project_id: projectId,
        latitude: lat ? parseFloat(lat) : undefined,
        longitude: lon ? parseFloat(lon) : undefined,
        elevation: elevation ? parseFloat(elevation) : undefined,
        pole_height: height ? parseFloat(height) : undefined,
      },
      { onSuccess: () => { setCode(''); onCreated?.() } }
    )
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
      <label className="col-span-2 block">
        <span className="text-xs font-medium text-gray-600">Código *</span>
        <input value={code} onChange={(e) => setCode(e.target.value)} required
          className="mt-1 w-full border rounded px-2 py-1 text-sm" placeholder="P-001" />
      </label>
      <label className="block">
        <span className="text-xs font-medium text-gray-600">Tipo</span>
        <select value={poleType} onChange={(e) => setPoleType(e.target.value)}
          className="mt-1 w-full border rounded px-2 py-1 text-sm">
          <option value="concreto">Concreto</option>
          <option value="madeira">Madeira</option>
          <option value="aço">Aço</option>
        </select>
      </label>
      <label className="block">
        <span className="text-xs font-medium text-gray-600">Altura (m)</span>
        <input type="number" value={height} onChange={(e) => setHeight(e.target.value)} step={0.5}
          className="mt-1 w-full border rounded px-2 py-1 text-sm" placeholder="11.0" />
      </label>
      <label className="block">
        <span className="text-xs font-medium text-gray-600">Latitude</span>
        <input type="number" value={lat} onChange={(e) => setLat(e.target.value)} step={0.00001}
          className="mt-1 w-full border rounded px-2 py-1 text-sm" placeholder="-22.15018" />
      </label>
      <label className="block">
        <span className="text-xs font-medium text-gray-600">Longitude</span>
        <input type="number" value={lon} onChange={(e) => setLon(e.target.value)} step={0.00001}
          className="mt-1 w-full border rounded px-2 py-1 text-sm" placeholder="-42.92185" />
      </label>
      <label className="block">
        <span className="text-xs font-medium text-gray-600">Altitude (m)</span>
        <input type="number" value={elevation} onChange={(e) => setElevation(e.target.value)} step={0.1}
          className="mt-1 w-full border rounded px-2 py-1 text-sm" placeholder="850.0" />
      </label>
      <button type="submit" disabled={createMutation.isPending}
        className="col-span-2 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 text-sm font-medium">
        {createMutation.isPending ? 'Salvando...' : 'Cadastrar Poste'}
      </button>
      {createMutation.isError && <p className="col-span-2 text-red-600 text-sm">Erro ao salvar poste.</p>}
    </form>
  )
}
