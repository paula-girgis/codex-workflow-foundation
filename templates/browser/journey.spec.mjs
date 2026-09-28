import { test, expect } from '@playwright/test';

/*
 * Adapt this representative template to the product contract before enabling it.
 * It is intentionally not a passing product test: placeholders must not be mistaken
 * for evidence. Use roles/labels/owned test IDs and deterministic fixtures.
 */
test('replace with a critical user journey', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/replace with product title/i);
  // Example shape:
  // await page.getByRole('button', { name: 'Create item' }).click();
  // await page.getByLabel('Name').fill('A deterministic fixture');
  // await page.getByRole('button', { name: 'Save' }).click();
  // await expect(page.getByRole('status')).toHaveText('Saved');
  // await page.reload();
  // await expect(page.getByText('A deterministic fixture', { exact: true })).toBeVisible();
  throw new Error('Adapt templates/browser/journey.spec.mjs to the agreed project contract before running it.');
});

test('replace with a scoped responsive or visual review', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page.locator('body')).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath('running-app.png'), fullPage: true });
  // Keep this capture distinct from wireframes, polished designs and approved snapshots.
  test.skip(true, 'Replace with an approved visual assertion and viewport contract.');
});
