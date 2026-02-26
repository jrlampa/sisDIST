/** Utility functions for map operations. */

export interface LatLon {
  lat: number
  lon: number
}

/** Calculate distance between two points in meters (Haversine formula). */
export function haversineDistance(a: LatLon, b: LatLon): number {
  const R = 6371000 // Earth radius in meters
  const phi1 = (a.lat * Math.PI) / 180
  const phi2 = (b.lat * Math.PI) / 180
  const dphi = ((b.lat - a.lat) * Math.PI) / 180
  const dlambda = ((b.lon - a.lon) * Math.PI) / 180
  const x = Math.sin(dphi / 2) ** 2 + Math.cos(phi1) * Math.cos(phi2) * Math.sin(dlambda / 2) ** 2
  return 2 * R * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x))
}

/** Format coordinates for display. */
export function formatCoords(lat: number, lon: number): string {
  const latDir = lat >= 0 ? 'N' : 'S'
  const lonDir = lon >= 0 ? 'L' : 'O'
  return `${Math.abs(lat).toFixed(5)}°${latDir} ${Math.abs(lon).toFixed(5)}°${lonDir}`
}

/** Check if coordinates are within Brazil's bounding box. */
export function isWithinBrazil(lat: number, lon: number): boolean {
  return lat >= -33.75 && lat <= 5.27 && lon >= -73.99 && lon <= -28.85
}

/** Default map center — Rio de Janeiro region. */
export const DEFAULT_CENTER: LatLon = { lat: -22.15018, lon: -42.92185 }
export const DEFAULT_ZOOM = 13
