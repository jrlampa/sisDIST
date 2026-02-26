/**
 * Unit tests for calculation-related utilities.
 * These test pure functions that mirror the backend calculation logic.
 */
import { describe, it, expect } from 'vitest'

// ── Voltage drop formula (mirrors backend Python logic) ──────────────────────

const CONDUCTOR_TABLE: Record<string, Record<number, [number, number]>> = {
  CA: {
    16:  [1.915, 0.335],
    25:  [1.200, 0.320],
    35:  [0.868, 0.310],
    50:  [0.641, 0.300],
    70:  [0.443, 0.290],
    95:  [0.320, 0.280],
    120: [0.253, 0.275],
    150: [0.206, 0.270],
    185: [0.164, 0.265],
    240: [0.125, 0.260],
  },
}

function calculateVoltageDrop(
  current: number,
  lengthM: number,
  conductorType: string,
  crossSection: number,
  powerFactor: number,
  phases: 1 | 3,
  nominalVoltage: number
): { dropV: number; dropPct: number } {
  const table = CONDUCTOR_TABLE[conductorType]
  if (!table) throw new Error('Tipo de condutor desconhecido')
  const props = table[crossSection]
  if (!props) throw new Error('Seção não encontrada')
  const [r, x] = props
  const sinPhi = Math.sqrt(Math.max(0, 1 - powerFactor ** 2))
  const lengthKm = lengthM / 1000
  const factor = phases === 3 ? Math.sqrt(3) : 2
  const dropV = factor * current * lengthKm * (r * powerFactor + x * sinPhi)
  const dropPct = (dropV / nominalVoltage) * 100
  return { dropV, dropPct }
}

describe('Voltage Drop Calculation', () => {
  it('calculates 3-phase voltage drop correctly', () => {
    const { dropV, dropPct } = calculateVoltageDrop(100, 500, 'CA', 50, 0.92, 3, 220)
    expect(dropV).toBeGreaterThan(0)
    expect(dropPct).toBeGreaterThan(0)
    // Manual: √3 × 100 × 0.5 × (0.641×0.92 + 0.300×sin)
    const sinPhi = Math.sqrt(1 - 0.92 ** 2)
    const expected = Math.sqrt(3) * 100 * 0.5 * (0.641 * 0.92 + 0.300 * sinPhi)
    expect(dropV).toBeCloseTo(expected, 3)
  })

  it('calculates 1-phase voltage drop with factor 2', () => {
    const { dropV } = calculateVoltageDrop(50, 200, 'CA', 25, 0.85, 1, 127)
    const sinPhi = Math.sqrt(1 - 0.85 ** 2)
    const expected = 2 * 50 * 0.2 * (1.200 * 0.85 + 0.320 * sinPhi)
    expect(dropV).toBeCloseTo(expected, 3)
  })

  it('1-phase drop is higher than 3-phase for same parameters', () => {
    const r1 = calculateVoltageDrop(100, 500, 'CA', 50, 0.92, 1, 220)
    const r3 = calculateVoltageDrop(100, 500, 'CA', 50, 0.92, 3, 220)
    expect(r1.dropV).toBeGreaterThan(r3.dropV)
  })

  it('larger cross section gives lower voltage drop', () => {
    const r50 = calculateVoltageDrop(100, 500, 'CA', 50, 0.92, 3, 220)
    const r150 = calculateVoltageDrop(100, 500, 'CA', 150, 0.92, 3, 220)
    expect(r150.dropV).toBeLessThan(r50.dropV)
  })

  it('percentage equals absolute drop divided by nominal voltage × 100', () => {
    const { dropV, dropPct } = calculateVoltageDrop(100, 500, 'CA', 50, 0.92, 3, 220)
    expect(dropPct).toBeCloseTo((dropV / 220) * 100, 5)
  })

  it('zero length gives zero drop', () => {
    const { dropV } = calculateVoltageDrop(100, 0, 'CA', 50, 0.92, 3, 220)
    expect(dropV).toBe(0)
  })

  it('throws for unknown conductor type', () => {
    expect(() => calculateVoltageDrop(100, 500, 'UNKNOWN', 50, 0.92, 3, 220)).toThrow()
  })
})
