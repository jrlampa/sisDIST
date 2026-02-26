import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || ''

export const apiClient = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
})

// ── Types ────────────────────────────────────────────────────────────────────

export interface Pole {
  id: number
  code: string
  project_id?: number
  latitude?: number
  longitude?: number
  elevation?: number
  pole_type: string
  pole_height?: number
  pole_class?: string
  owner?: string
  observations?: string
  created_at?: string
}

export interface Conductor {
  id: number
  project_id?: number
  pole_from_id?: number
  pole_to_id?: number
  conductor_type: string
  cross_section: number
  voltage_level: string
  phases: number
  length?: number
  observations?: string
  created_at?: string
}

export interface Project {
  id: number
  name: string
  description?: string
  concessionaire: string
  area_wkt?: string
  created_at?: string
  updated_at?: string
}

export interface VoltageDropRequest {
  current: number
  length: number
  conductor_type: string
  cross_section: number
  power_factor: number
  phases: 1 | 3
  nominal_voltage: number
  voltage_level: string
}

export interface VoltageDropResponse {
  voltage_drop_v: number
  voltage_drop_pct: number
  limit_pct: number
  compliant: boolean
  resistance: number
  reactance: number
  standard: string
}

export interface MechanicalStressRequest {
  wind_speed: number
  conductor_diameter: number
  span_length: number
  conductor_weight: number
  conductor_tension: number
  pole_height: number
  attachment_height: number
  num_conductors: number
}

export interface MechanicalStressResponse {
  wind_load_per_conductor_n: number
  weight_load_per_conductor_n: number
  tension_load_n: number
  total_resultant_n: number
  moment_nm: number
  safety_factor_required: number
  standard: string
}

// ── API calls ────────────────────────────────────────────────────────────────

export const polesApi = {
  list: (projectId?: number) =>
    apiClient.get<Pole[]>('/infrastructure/poles', { params: { project_id: projectId } }).then(r => r.data),
  create: (data: Omit<Pole, 'id'>) =>
    apiClient.post<Pole>('/infrastructure/poles', data).then(r => r.data),
  update: (id: number, data: Partial<Pole>) =>
    apiClient.put<Pole>(`/infrastructure/poles/${id}`, data).then(r => r.data),
  delete: (id: number) =>
    apiClient.delete(`/infrastructure/poles/${id}`),
}

export const conductorsApi = {
  list: (projectId?: number) =>
    apiClient.get<Conductor[]>('/infrastructure/conductors', { params: { project_id: projectId } }).then(r => r.data),
  create: (data: Omit<Conductor, 'id'>) =>
    apiClient.post<Conductor>('/infrastructure/conductors', data).then(r => r.data),
  update: (id: number, data: Partial<Conductor>) =>
    apiClient.put<Conductor>(`/infrastructure/conductors/${id}`, data).then(r => r.data),
  delete: (id: number) =>
    apiClient.delete(`/infrastructure/conductors/${id}`),
}

export const projectsApi = {
  list: () =>
    apiClient.get<Project[]>('/projects/').then(r => r.data),
  create: (data: Omit<Project, 'id'>) =>
    apiClient.post<Project>('/projects/', data).then(r => r.data),
  update: (id: number, data: Partial<Project>) =>
    apiClient.put<Project>(`/projects/${id}`, data).then(r => r.data),
  delete: (id: number) =>
    apiClient.delete(`/projects/${id}`),
  materialList: (id: number) =>
    apiClient.get(`/projects/${id}/material-list`).then(r => r.data),
}

export const calculationsApi = {
  voltageDrop: (data: VoltageDropRequest) =>
    apiClient.post<VoltageDropResponse>('/calculations/voltage-drop', data).then(r => r.data),
  mechanicalStress: (data: MechanicalStressRequest) =>
    apiClient.post<MechanicalStressResponse>('/calculations/mechanical-stress', data).then(r => r.data),
}

export const mappingApi = {
  osm: (lat: number, lon: number, radius = 500) =>
    apiClient.get('/mapping/osm', { params: { lat, lon, radius } }).then(r => r.data),
  elevation: (lat: number, lon: number) =>
    apiClient.get('/mapping/elevation', { params: { lat, lon } }).then(r => r.data),
  convertUtm: (easting: number, northing: number, zone = 23, hemisphere = 'S') =>
    apiClient.get('/mapping/convert-utm', { params: { easting, northing, zone, hemisphere } }).then(r => r.data),
}
