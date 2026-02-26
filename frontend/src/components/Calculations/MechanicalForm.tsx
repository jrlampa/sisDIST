import { useState } from 'react'
import { calculationsApi, MechanicalStressRequest, MechanicalStressResponse } from '../../services/api'

export default function MechanicalForm() {
  const [form, setForm] = useState<MechanicalStressRequest>({
    wind_speed: 25,
    conductor_diameter: 14.4,
    span_length: 60,
    conductor_weight: 407,
    conductor_tension: 5000,
    pole_height: 11,
    attachment_height: 10,
    num_conductors: 3,
  })
  const [result, setResult] = useState<MechanicalStressResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const set = (k: keyof MechanicalStressRequest, v: number) => setForm((f) => ({ ...f, [k]: v }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await calculationsApi.mechanicalStress(form)
      setResult(res)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Erro no cálculo')
    } finally {
      setLoading(false)
    }
  }

  const fields: { key: keyof MechanicalStressRequest; label: string; step: number }[] = [
    { key: 'wind_speed', label: 'Velocidade do Vento (m/s)', step: 0.5 },
    { key: 'conductor_diameter', label: 'Diâmetro do Condutor (mm)', step: 0.1 },
    { key: 'span_length', label: 'Vão (m)', step: 1 },
    { key: 'conductor_weight', label: 'Peso do Condutor (kg/km)', step: 1 },
    { key: 'conductor_tension', label: 'Tensão Mecânica (N)', step: 100 },
    { key: 'pole_height', label: 'Altura do Poste (m)', step: 0.5 },
    { key: 'attachment_height', label: 'Altura do Ponto de Fixação (m)', step: 0.5 },
    { key: 'num_conductors', label: 'Número de Condutores', step: 1 },
  ]

  return (
    <div className="max-w-xl">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">Esforço Mecânico — ABNT NBR 8458/8798</h2>
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-3">
        <div className="grid grid-cols-2 gap-4">
          {fields.map(({ key, label, step }) => (
            <label key={key} className="block">
              <span className="text-xs font-medium text-gray-600">{label}</span>
              <input
                type="number"
                value={form[key]}
                min={0.1}
                step={step}
                onChange={(e) => set(key, parseFloat(e.target.value))}
                className="mt-1 w-full border rounded px-2 py-1 text-sm"
              />
            </label>
          ))}
        </div>
        <button type="submit" disabled={loading}
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 font-medium">
          {loading ? 'Calculando...' : 'Calcular'}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600">{error}</p>}

      {result && (
        <div className="mt-4 p-4 rounded-lg border-2 border-yellow-400 bg-yellow-50">
          <h3 className="font-semibold mb-2">Resultado do Esforço Mecânico</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <span className="text-gray-600">Carga de Vento/Condutor:</span>
            <span className="font-mono">{result.wind_load_per_conductor_n.toFixed(1)} N</span>
            <span className="text-gray-600">Carga de Peso/Condutor:</span>
            <span className="font-mono">{result.weight_load_per_conductor_n.toFixed(1)} N</span>
            <span className="text-gray-600">Carga de Tração:</span>
            <span className="font-mono">{result.tension_load_n.toFixed(1)} N</span>
            <span className="text-gray-600">Resultante Total:</span>
            <span className="font-mono font-bold">{result.total_resultant_n.toFixed(1)} N</span>
            <span className="text-gray-600">Momento Fletor:</span>
            <span className="font-mono font-bold">{result.moment_nm.toFixed(1)} N·m</span>
            <span className="text-gray-600">Coef. Segurança Mín.:</span>
            <span className="font-mono">{result.safety_factor_required}</span>
            <span className="text-gray-500 col-span-2 text-xs">{result.standard}</span>
          </div>
        </div>
      )}
    </div>
  )
}
