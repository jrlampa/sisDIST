interface MaterialItem {
  codigo: string
  descricao: string
  unidade: string
  quantidade: number
}

interface Props {
  projectName: string
  concessionaire: string
  items: MaterialItem[]
}

export default function MaterialList({ projectName, concessionaire, items }: Props) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="font-bold text-gray-800 mb-1">Lista de Material</h2>
      <p className="text-sm text-gray-500 mb-3">{projectName} — {concessionaire}</p>
      {items.length === 0 ? (
        <p className="text-gray-400 text-sm">Nenhum item na lista.</p>
      ) : (
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="text-left px-3 py-2 border">Código</th>
              <th className="text-left px-3 py-2 border">Descrição</th>
              <th className="text-left px-3 py-2 border">Un.</th>
              <th className="text-right px-3 py-2 border">Qtd.</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="px-3 py-2 border font-mono text-xs">{item.codigo}</td>
                <td className="px-3 py-2 border">{item.descricao}</td>
                <td className="px-3 py-2 border">{item.unidade}</td>
                <td className="px-3 py-2 border text-right">{item.quantidade}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
