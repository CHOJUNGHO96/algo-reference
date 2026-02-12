import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for Algorithm Reference Platform E2E tests
 *
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  // Test directory
  testDir: './specs',

  // Maximum time one test can run for
  timeout: 30 * 1000,

  // Test execution settings
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Reporter configuration
  reporter: process.env.CI
    ? [['html'], ['github']]
    : [['html'], ['list']],

  // Shared settings for all projects
  use: {
    // Base URL for tests
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Collect trace when retrying failed tests
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'retain-on-failure',

    // Default timeout for actions
    actionTimeout: 10 * 1000,

    // Default timeout for navigation
    navigationTimeout: 30 * 1000,
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile viewports
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },

    // Tablet viewports
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] },
    },
  ],

  // Web server configuration (optional - for local development)
  webServer: process.env.CI
    ? undefined
    : {
        command: 'npm run dev',
        cwd: '../../frontend',
        url: 'http://localhost:3000',
        reuseExistingServer: !process.env.CI,
        timeout: 120 * 1000,
      },

  // Output directory for test artifacts
  outputDir: 'test-results/',
});
