import { test, expect } from '@playwright/test'

test.describe('sisDIST Application', () => {
  test('homepage shows sisDIST title', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('text=sisDIST')).toBeVisible()
  })

  test('navigation links are present', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('text=Mapa')).toBeVisible()
    await expect(page.locator('text=Cálculos')).toBeVisible()
    await expect(page.locator('text=Projetos')).toBeVisible()
  })

  test('dashboard shows ABNT standards', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('text=ABNT')).toBeVisible()
  })

  test('calculations page shows voltage drop form', async ({ page }) => {
    await page.goto('/calculations')
    await expect(page.locator('text=Queda de Tensão')).toBeVisible()
  })

  test('projects page loads', async ({ page }) => {
    await page.goto('/projects')
    await expect(page.locator('text=Projetos')).toBeVisible()
  })
})
