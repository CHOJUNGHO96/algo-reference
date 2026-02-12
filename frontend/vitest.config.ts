import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    // Test environment
    environment: 'jsdom',

    // Setup files
    setupFiles: ['./src/setupTests.ts'],

    // Global test utilities
    globals: true,

    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json', 'lcov'],
      exclude: [
        'node_modules/',
        'src/setupTests.ts',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData/',
        'dist/',
      ],
      // Coverage thresholds
      lines: 75,
      functions: 75,
      branches: 75,
      statements: 75,
    },

    // Test file patterns
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],

    // Reporter configuration
    reporters: ['verbose'],

    // Mock CSS modules
    css: {
      modules: {
        classNameStrategy: 'non-scoped',
      },
    },
  },

  // Path resolution (match vite.config.ts)
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
