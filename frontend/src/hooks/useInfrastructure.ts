import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { polesApi, conductorsApi, Pole, Conductor } from '../services/api'

export function usePoles(projectId?: number) {
  return useQuery({
    queryKey: ['poles', projectId],
    queryFn: () => polesApi.list(projectId),
  })
}

export function useCreatePole() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: Omit<Pole, 'id'>) => polesApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['poles'] }),
  })
}

export function useDeletePole() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => polesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['poles'] }),
  })
}

export function useConductors(projectId?: number) {
  return useQuery({
    queryKey: ['conductors', projectId],
    queryFn: () => conductorsApi.list(projectId),
  })
}

export function useCreateConductor() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: Omit<Conductor, 'id'>) => conductorsApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['conductors'] }),
  })
}
