import { describe, it, expect } from 'vitest'
import {
  haversineDistance,
  formatCoords,
  isWithinBrazil,
  DEFAULT_CENTER,
} from '../../src/services/mapService'

describe('haversineDistance', () => {
  it('returns 0 for same point', () => {
    expect(haversineDistance(DEFAULT_CENTER, DEFAULT_CENTER)).toBe(0)
  })

  it('calculates distance between two points approximately', () => {
    // Rio de Janeiro to São Paulo is roughly 360km
    const rj = { lat: -22.9068, lon: -43.1729 }
    const sp = { lat: -23.5505, lon: -46.6333 }
    const dist = haversineDistance(rj, sp)
    expect(dist).toBeGreaterThan(350_000)
    expect(dist).toBeLessThan(420_000)
  })

  it('is symmetric', () => {
    const a = { lat: -22.15, lon: -42.92 }
    const b = { lat: -22.20, lon: -42.95 }
    expect(haversineDistance(a, b)).toBeCloseTo(haversineDistance(b, a), 3)
  })

  it('increases with distance', () => {
    const origin = { lat: -22.15, lon: -42.92 }
    const near = { lat: -22.151, lon: -42.921 }
    const far = { lat: -22.2, lon: -43.0 }
    expect(haversineDistance(origin, far)).toBeGreaterThan(haversineDistance(origin, near))
  })
})

describe('formatCoords', () => {
  it('formats southern negative latitude with S indicator', () => {
    const result = formatCoords(-22.15018, -42.92185)
    expect(result).toContain('S')
    expect(result).toContain('O')
    expect(result).toContain('22.15018')
  })

  it('formats northern positive latitude with N indicator', () => {
    const result = formatCoords(5.0, -60.0)
    expect(result).toContain('N')
  })

  it('formats eastern longitude with L indicator', () => {
    const result = formatCoords(0, 10.0)
    expect(result).toContain('L')
  })
})

describe('isWithinBrazil', () => {
  it('returns true for Rio de Janeiro coordinates', () => {
    expect(isWithinBrazil(-22.15018, -42.92185)).toBe(true)
  })

  it('returns true for São Paulo', () => {
    expect(isWithinBrazil(-23.5505, -46.6333)).toBe(true)
  })

  it('returns false for Paris', () => {
    expect(isWithinBrazil(48.8566, 2.3522)).toBe(false)
  })

  it('returns false for Buenos Aires', () => {
    expect(isWithinBrazil(-34.6037, -58.3816)).toBe(false)
  })

  it('returns false for New York', () => {
    expect(isWithinBrazil(40.7128, -74.0060)).toBe(false)
  })
})

describe('DEFAULT_CENTER', () => {
  it('is within Brazil', () => {
    expect(isWithinBrazil(DEFAULT_CENTER.lat, DEFAULT_CENTER.lon)).toBe(true)
  })

  it('has correct test coordinates for Rio de Janeiro region', () => {
    expect(DEFAULT_CENTER.lat).toBeCloseTo(-22.15018, 3)
    expect(DEFAULT_CENTER.lon).toBeCloseTo(-42.92185, 3)
  })
})
