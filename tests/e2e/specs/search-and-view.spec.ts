/**
 * E2E Test: Search and View Algorithm Flow
 *
 * Critical user journey:
 * 1. User types in search bar
 * 2. Results appear with filtering
 * 3. Click on algorithm card
 * 4. View all 8 sections
 * 5. Copy code snippet
 * 6. Navigate back to list
 */

import { test, expect } from '@playwright/test';

test.describe('Algorithm Search and View Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');

    // Wait for initial page load
    await page.waitForLoadState('networkidle');
  });

  test('user can search and view algorithm details', async ({ page }) => {
    // Step 1: Type in search bar
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('Two Pointer');

    // Wait for search results to appear
    await page.waitForSelector('[data-testid="algorithm-card"]', { timeout: 5000 });

    // Verify search results appear
    const algorithmCards = page.locator('[data-testid="algorithm-card"]');
    await expect(algorithmCards).toHaveCount(1, { timeout: 5000 });

    // Step 2: Click on first result
    await algorithmCards.first().click();

    // Step 3: Verify we're on detail page
    await expect(page).toHaveURL(/\/algorithms\/two-pointer-technique/);
    await expect(page.locator('h1')).toContainText('Two Pointer Technique');

    // Step 4: Verify all 8 sections are present and visible
    const sections = [
      'Concept Summary',
      'Core Formulas',
      'Thought Process',
      'Application Conditions',
      'Time Complexity',
      'Problem Types',
      'Code Templates',
      'Common Mistakes',
    ];

    for (const section of sections) {
      await expect(page.getByText(section)).toBeVisible();
    }

    // Step 5: Verify code block present
    const codeBlock = page.locator('[data-testid="code-block"]');
    await expect(codeBlock).toBeVisible();

    // Step 6: Test copy button
    const copyButton = page.locator('[data-testid="copy-code-button"]').first();
    await copyButton.click();

    // Verify copy confirmation appears
    await expect(page.locator('text=Copied!')).toBeVisible({ timeout: 2000 });

    // Step 7: Navigate back to list
    await page.goBack();

    // Verify we're back on the list page
    await expect(page).toHaveURL('/');
    await expect(searchInput).toBeVisible();
  });

  test('search returns no results for invalid query', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('NonExistentAlgorithm12345');

    // Wait a moment for search to complete
    await page.waitForTimeout(1000);

    // Verify no results message
    await expect(page.locator('text=No algorithms found')).toBeVisible();
  });

  test('algorithm detail page displays complexity badges', async ({ page }) => {
    // Navigate directly to algorithm detail
    await page.goto('/algorithms/two-pointer-technique');

    // Verify time complexity badge
    const timeComplexity = page.locator('text=Time:').locator('..').locator('code');
    await expect(timeComplexity).toContainText('O(n)');

    // Verify space complexity badge
    const spaceComplexity = page.locator('text=Space:').locator('..').locator('code');
    await expect(spaceComplexity).toContainText('O(1)');
  });

  test('algorithm detail page displays category and difficulty', async ({ page }) => {
    await page.goto('/algorithms/two-pointer-technique');

    // Verify category badge
    await expect(page.locator('.category-badge')).toContainText('Two Pointer');

    // Verify difficulty badge
    await expect(page.locator('.difficulty-badge')).toContainText('Medium');
  });

  test('view count increments on algorithm view', async ({ page }) => {
    // First view
    await page.goto('/algorithms/two-pointer-technique');

    // Get initial view count
    const viewCountElement = page.locator('[data-testid="view-count"]');
    const initialViewCount = await viewCountElement.textContent();

    // Navigate away and back
    await page.goto('/');
    await page.goto('/algorithms/two-pointer-technique');

    // Get updated view count
    const updatedViewCount = await viewCountElement.textContent();

    // View count should have increased
    expect(updatedViewCount).not.toBe(initialViewCount);
  });

  test('mobile responsive - search and view on small screen', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Navigate to homepage
    await page.goto('/');

    // Search should work on mobile
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('Two Pointer');

    // Results should appear
    await expect(page.locator('[data-testid="algorithm-card"]').first()).toBeVisible();

    // Click and navigate
    await page.locator('[data-testid="algorithm-card"]').first().click();

    // Detail page should render properly
    await expect(page.locator('h1')).toContainText('Two Pointer');

    // Code block should be horizontally scrollable on mobile
    const codeBlock = page.locator('[data-testid="code-block"]');
    await expect(codeBlock).toBeVisible();
  });
});
