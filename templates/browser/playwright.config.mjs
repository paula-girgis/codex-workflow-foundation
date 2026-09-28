import { defineConfig, devices } from '@playwright/test';

// Adapt this file in the target project. Adoption does not install packages or browsers.
// Start with one browser; add projects only when their checks actually run.
export default defineConfig({
  testDir: './tests/playwright',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  failOnFlakyTests: true,
  retries: 0,
  workers: process.env.CI ? 1 : undefined,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  outputDir: 'test-results',
  reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }], ['json', { outputFile: 'test-results.json' }]],
  use: {
    baseURL: process.env.BASE_URL || 'http://127.0.0.1:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'off',
    ...devices['Desktop Chrome'],
  },
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }],
  // Add a reviewed project-local server command, for example:
  // webServer: { command: 'npm run start:test', url: 'http://127.0.0.1:3000', reuseExistingServer: false },
});
