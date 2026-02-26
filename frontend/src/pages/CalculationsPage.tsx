import { useState } from 'react'
import VoltageDropForm from '../components/Calculations/VoltageDropForm'
import MechanicalForm from '../components/Calculations/MechanicalForm'

type Tab = 'voltage' | 'mechanical'

export default function CalculationsPage() {
  const [tab, setTab] = useState<Tab>('voltage')

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-800 mb-4">Cálculos de Engenharia</h1>
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setTab('voltage')}
          className={`px-4 py-2 rounded font-medium ${tab === 'voltage' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
        >
          Queda de Tensão
        </button>
        <button
          onClick={() => setTab('mechanical')}
          className={`px-4 py-2 rounded font-medium ${tab === 'mechanical' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
        >
          Esforço Mecânico
        </button>
      </div>
      {tab === 'voltage' ? <VoltageDropForm /> : <MechanicalForm />}
    </div>
  )
}
