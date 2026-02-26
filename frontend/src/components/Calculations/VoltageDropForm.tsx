import { useState } from 'react'
import { calculationsApi, VoltageDropRequest, VoltageDropResponse } from '../../services/api'

const CONDUCTOR_TYPES = ['CA', 'CAA', 'ACSR']
const CROSS_SECTIONS = [16, 25, 35, 50, 70, 95, 120, 150, 185, 240]

export default function VoltageDropForm() {
  const [form, setForm] = useState<VoltageDropRequest>({
    current: 100,
    length: 500,
    conductor_type: 'CA',
    cross_section: 50,
    power_factor: 0.92,
    phases: 3,
    nominal_voltage: 220,
    voltage_level: 'BT',
  })
  const [result, setResult] = useState<VoltageDropResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const set = (k: keyof VoltageDropRequest, v: any) => setForm((f) => ({ ...f, [k]: v }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await calculationsApi.voltageDrop(form)
      setResult(res)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Erro no cálculo')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-xl">
      <h2 className="text-lg font-semibold text-gray-700 mb-4">Queda de Tensão — ABNT NBR 5410</h2>
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Corrente (A)</span>
            <input type="number" value={form.current} min={0.1} step={0.1}
              onChange={(e) => set('current', parseFloat(e.target.value))}
              className="mt-1 w-full border rounded px-2 py-1 text-sm" />
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Comprimento (m)</span>
            <input type="number" value={form.length} min={1} step={1}
              onChange={(e) => set('length', parseFloat(e.target.value))}
              className="mt-1 w-full border rounded px-2 py-1 text-sm" />
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Tipo de Condutor</span>
            <select value={form.conductor_type} onChange={(e) => set('conductor_type', e.target.value)}
              className="mt-1 w-full border rounded px-2 py-1 text-sm">
              {CONDUCTOR_TYPES.map((t) => <option key={t}>{t}</option>)}
            </select>
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Seção (mm²)</span>
            <select value={form.cross_section} onChange={(e) => set('cross_section', parseFloat(e.target.value))}
              className="mt-1 w-full border rounded px-2 py-1 text-sm">
              {CROSS_SECTIONS.map((s) => <option key={s}>{s}</option>)}
            </select>
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Fator de Potência</span>
            <input type="number" value={form.power_factor} min={0} max={1} step={0.01}
              onChange={(e) => set('power_factor', parseFloat(e.target.value))}
              className="mt-1 w-full border rounded px-2 py-1 text-sm" />
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Fases</span>
            <select value={form.phases} onChange={(e) => set('phases', parseInt(e.target.value) as 1 | 3)}
              className="mt-1 w-full border rounded px-2 py-1 text-sm">
              <option value={1}>Monofásico (1F)</option>
              <option value={3}>Trifásico (3F)</option>
            </select>
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Tensão Nominal (V)</span>
            <input type="number" value={form.nominal_voltage} min={1}
              onChange={(e) => set('nominal_voltage', parseFloat(e.target.value))}
              className="mt-1 w-full border rounded px-2 py-1 text-sm" />
          </label>
          <label className="block">
            <span className="text-xs font-medium text-gray-600">Nível de Tensão</span>
            <select value={form.voltage_level} onChange={(e) => set('voltage_level', e.target.value)}
              className="mt-1 w-full border rounded px-2 py-1 text-sm">
              <option value="BT">BT — Baixa Tensão</option>
              <option value="MT">MT — Média Tensão</option>
            </select>
          </label>
        </div>
        <button type="submit" disabled={loading}
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 font-medium">
          {loading ? 'Calculando...' : 'Calcular'}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600">{error}</p>}

      {result && (
        <div className={`mt-4 p-4 rounded-lg border-2 ${result.compliant ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50'}`}>
          <h3 className="font-semibold mb-2">{result.compliant ? '✅ Conforme' : '❌ Não Conforme'}</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <span className="text-gray-600">Queda de Tensão:</span>
            <span className="font-mono">{result.voltage_drop_v.toFixed(2)} V ({result.voltage_drop_pct.toFixed(2)}%)</span>
            <span className="text-gray-600">Limite:</span>
            <span className="font-mono">{result.limit_pct.toFixed(1)}%</span>
            <span className="text-gray-600">Resistência:</span>
            <span className="font-mono">{result.resistance} Ω/km</span>
            <span className="text-gray-600">Reatância:</span>
            <span className="font-mono">{result.reactance} Ω/km</span>
            <span className="text-gray-500 col-span-2 text-xs">{result.standard}</span>
          </div>
        </div>
      )}
    </div>
  )
}
