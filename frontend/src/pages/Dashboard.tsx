export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-2">
        Bem-vindo ao sisDIST
      </h1>
      <p className="text-gray-600 mb-6">
        Sistema de Distribuição Elétrica — Ferramenta para engenheiros elétricos (Enel-RJ e Light)
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Mapa de Infraestrutura', desc: 'Visualize postes, condutores e equipamentos', href: '/map', color: 'bg-blue-600' },
          { label: 'Cálculos Elétricos', desc: 'Queda de tensão (NBR 5410)', href: '/calculations', color: 'bg-green-600' },
          { label: 'Esforço Mecânico', desc: 'Análise de postes (NBR 8458/8798)', href: '/calculations', color: 'bg-yellow-600' },
          { label: 'Projetos', desc: 'Gerencie projetos e listas de material', href: '/projects', color: 'bg-purple-600' },
        ].map((card) => (
          <a
            key={card.label}
            href={card.href}
            className="block rounded-lg shadow p-5 bg-white border-l-4 hover:shadow-md transition"
          >
            <div className={`inline-block px-2 py-1 rounded text-white text-xs mb-2 ${card.color}`}>
              {card.label}
            </div>
            <p className="text-sm text-gray-600">{card.desc}</p>
          </a>
        ))}
      </div>
      <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h2 className="font-semibold text-blue-800 mb-1">Padrões aplicados</h2>
        <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
          <li>ABNT NBR 5410:2004 — Instalações elétricas de baixa tensão</li>
          <li>ABNT NBR 8458/8798 — Postes de distribuição</li>
          <li>Aneel Prodist Módulo 8 — Qualidade de energia elétrica</li>
          <li>SIRGAS2000 UTM — Sistema de referência cartográfico</li>
        </ul>
      </div>
    </div>
  )
}
