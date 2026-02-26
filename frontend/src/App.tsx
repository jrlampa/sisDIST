import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Dashboard from './pages/Dashboard'
import MapPage from './pages/MapPage'
import CalculationsPage from './pages/CalculationsPage'
import ProjectsPage from './pages/ProjectsPage'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-blue-700 text-white px-6 py-3 flex gap-6 items-center shadow">
            <span className="font-bold text-lg">sisDIST</span>
            <NavLink to="/" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Painel
            </NavLink>
            <NavLink to="/map" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Mapa
            </NavLink>
            <NavLink to="/calculations" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Cálculos
            </NavLink>
            <NavLink to="/projects" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Projetos
            </NavLink>
          </nav>
          <main className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/calculations" element={<CalculationsPage />} />
              <Route path="/projects" element={<ProjectsPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
