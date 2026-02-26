import { Project } from '../../services/api'

interface Props {
  projects: Project[]
  onDelete: (id: number) => void
}

export default function ProjectList({ projects, onDelete }: Props) {
  if (projects.length === 0) {
    return <p className="text-gray-400 text-sm">Nenhum projeto encontrado.</p>
  }

  return (
    <div className="space-y-3">
      {projects.map((p) => (
        <div key={p.id} className="bg-white rounded-lg shadow p-4 flex justify-between items-start">
          <div>
            <h3 className="font-semibold text-gray-800">{p.name}</h3>
            {p.description && <p className="text-sm text-gray-500 mt-1">{p.description}</p>}
            <span className="inline-block mt-2 text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
              {p.concessionaire}
            </span>
            {p.created_at && (
              <span className="ml-2 text-xs text-gray-400">
                {new Date(p.created_at).toLocaleDateString('pt-BR')}
              </span>
            )}
          </div>
          <div className="flex gap-2">
            <a
              href={`/api/v1/projects/${p.id}/material-list`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:underline"
            >
              Lista de Material
            </a>
            <button
              onClick={() => onDelete(p.id)}
              className="text-sm text-red-500 hover:underline"
            >
              Excluir
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
