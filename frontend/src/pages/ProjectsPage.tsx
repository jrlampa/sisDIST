import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { projectsApi, Project } from '../services/api'
import ProjectList from '../components/Projects/ProjectList'

export default function ProjectsPage() {
  const qc = useQueryClient()
  const { data: projects = [], isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: projectsApi.list,
  })

  const createMutation = useMutation({
    mutationFn: (data: Omit<Project, 'id'>) => projectsApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['projects'] }),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => projectsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['projects'] }),
  })

  if (isLoading) return <p>Carregando...</p>
  if (error) return <p className="text-red-600">Erro ao carregar projetos.</p>

  return (
    <div>
      <h1 className="text-xl font-bold text-gray-800 mb-4">Projetos</h1>
      <button
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={() =>
          createMutation.mutate({
            name: `Projeto ${new Date().toLocaleDateString('pt-BR')}`,
            concessionaire: 'Enel-RJ',
          })
        }
      >
        + Novo Projeto
      </button>
      <ProjectList projects={projects} onDelete={(id) => deleteMutation.mutate(id)} />
    </div>
  )
}
