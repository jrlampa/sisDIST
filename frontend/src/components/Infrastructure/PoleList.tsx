import { useState } from 'react'
import { usePoles, useCreatePole, useDeletePole } from '../../hooks/useInfrastructure'

export default function PoleList({ projectId }: { projectId?: number }) {
  const { data: poles = [], isLoading } = usePoles(projectId)
  const createMutation = useCreatePole()
  const deleteMutation = useDeletePole()
  const [newCode, setNewCode] = useState('')

  if (isLoading) return <p className="text-gray-500">Carregando postes...</p>

  return (
    <div>
      <div className="flex gap-2 mb-3">
        <input
          value={newCode}
          onChange={(e) => setNewCode(e.target.value)}
          placeholder="Código do poste (ex: P-001)"
          className="border rounded px-2 py-1 text-sm flex-1"
        />
        <button
          onClick={() => {
            if (!newCode.trim()) return
            createMutation.mutate({ code: newCode.trim(), pole_type: 'concreto' })
            setNewCode('')
          }}
          className="px-3 py-1 bg-blue-600 text-white rounded text-sm"
        >
          Adicionar
        </button>
      </div>
      {poles.length === 0 ? (
        <p className="text-gray-400 text-sm">Nenhum poste cadastrado.</p>
      ) : (
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="text-left px-3 py-2 border">Código</th>
              <th className="text-left px-3 py-2 border">Tipo</th>
              <th className="text-left px-3 py-2 border">Altitude (m)</th>
              <th className="text-left px-3 py-2 border">Lat</th>
              <th className="text-left px-3 py-2 border">Lon</th>
              <th className="px-3 py-2 border"></th>
            </tr>
          </thead>
          <tbody>
            {poles.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-3 py-2 border font-mono">{p.code}</td>
                <td className="px-3 py-2 border">{p.pole_type}</td>
                <td className="px-3 py-2 border">{p.elevation ?? '—'}</td>
                <td className="px-3 py-2 border">{p.latitude?.toFixed(5) ?? '—'}</td>
                <td className="px-3 py-2 border">{p.longitude?.toFixed(5) ?? '—'}</td>
                <td className="px-3 py-2 border text-center">
                  <button
                    onClick={() => deleteMutation.mutate(p.id)}
                    className="text-red-600 hover:underline text-xs"
                  >
                    Remover
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
