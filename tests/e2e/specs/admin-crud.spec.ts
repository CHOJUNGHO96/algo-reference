/**
 * E2E Test: Admin CRUD Operations
 *
 * Tests admin authentication and algorithm CRUD operations:
 * 1. Admin login
 * 2. Create new algorithm
 * 3. Edit existing algorithm
 * 4. Delete algorithm
 */

import { test, expect } from '@playwright/test';
import { testAdmin, newAlgorithm } from '../fixtures/test-data';

test.describe('Admin CRUD Operations', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to admin login
    await page.goto('/admin/login');
  });

  test('admin can login with valid credentials', async ({ page }) => {
    // Fill login form
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', testAdmin.password);

    // Submit form
    await page.click('[data-testid="login-button"]');

    // Wait for redirect to admin dashboard
    await expect(page).toHaveURL('/admin/dashboard', { timeout: 5000 });

    // Verify admin dashboard elements present
    await expect(page.locator('text=Admin Dashboard')).toBeVisible();
    await expect(page.locator('text=Create Algorithm')).toBeVisible();
  });

  test('admin login fails with invalid credentials', async ({ page }) => {
    // Fill login form with wrong password
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', 'wrongpassword');

    // Submit form
    await page.click('[data-testid="login-button"]');

    // Verify error message appears
    await expect(page.locator('text=Invalid credentials')).toBeVisible({ timeout: 3000 });

    // Should stay on login page
    await expect(page).toHaveURL('/admin/login');
  });

  test('admin can create new algorithm with all 8 sections', async ({ page }) => {
    // Login first
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', testAdmin.password);
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to create algorithm page
    await page.click('text=Create Algorithm');
    await expect(page).toHaveURL('/admin/algorithms/create');

    // Fill all 8 sections
    await page.fill('[data-testid="title-input"]', newAlgorithm.title);

    // Select category from dropdown
    await page.click('[data-testid="category-select"]');
    await page.click(`text=${newAlgorithm.category}`);

    // Select difficulty from dropdown
    await page.click('[data-testid="difficulty-select"]');
    await page.click(`text=${newAlgorithm.difficulty}`);

    // Fill text sections
    await page.fill('[data-testid="concept-summary-input"]', newAlgorithm.conceptSummary);
    await page.fill('[data-testid="core-formulas-input"]', newAlgorithm.coreFormulas);
    await page.fill('[data-testid="thought-process-input"]', newAlgorithm.thoughtProcess);
    await page.fill('[data-testid="application-conditions-input"]', newAlgorithm.applicationConditions);
    await page.fill('[data-testid="time-complexity-input"]', newAlgorithm.timeComplexity);
    await page.fill('[data-testid="space-complexity-input"]', newAlgorithm.spaceComplexity);
    await page.fill('[data-testid="problem-types-input"]', newAlgorithm.problemTypes);
    await page.fill('[data-testid="common-mistakes-input"]', newAlgorithm.commonMistakes);

    // Add code template
    await page.fill('[data-testid="code-template-input"]', newAlgorithm.codeTemplate);

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Wait for success message
    await expect(page.locator('text=Algorithm created successfully')).toBeVisible({ timeout: 5000 });

    // Verify redirect to algorithm detail page
    await expect(page).toHaveURL(/\/algorithms\/binary-search/);

    // Verify all sections are displayed
    await expect(page.locator('h1')).toContainText('Binary Search');
    await expect(page.locator('text=Easy')).toBeVisible();
  });

  test('admin can edit existing algorithm', async ({ page }) => {
    // Login
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', testAdmin.password);
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to algorithm detail
    await page.goto('/algorithms/two-pointer-technique');

    // Click edit button (visible only for admins)
    await page.click('[data-testid="edit-button"]');

    // Wait for edit page
    await expect(page).toHaveURL('/admin/algorithms/two-pointer-technique/edit');

    // Modify title
    const titleInput = page.locator('[data-testid="title-input"]');
    await titleInput.clear();
    await titleInput.fill('Updated Two Pointer Technique');

    // Modify concept summary
    const conceptInput = page.locator('[data-testid="concept-summary-input"]');
    await conceptInput.clear();
    await conceptInput.fill('Updated concept summary with more details...');

    // Save changes
    await page.click('[data-testid="save-button"]');

    // Verify success message
    await expect(page.locator('text=Algorithm updated successfully')).toBeVisible();

    // Verify changes reflected on detail page
    await expect(page.locator('h1')).toContainText('Updated Two Pointer Technique');
    await expect(page.locator('text=Updated concept summary')).toBeVisible();
  });

  test('admin can delete algorithm', async ({ page }) => {
    // Login
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', testAdmin.password);
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to algorithm detail
    await page.goto('/algorithms/binary-search');

    // Click delete button
    await page.click('[data-testid="delete-button"]');

    // Confirm deletion in dialog
    await page.click('[data-testid="confirm-delete-button"]');

    // Wait for redirect to list page
    await expect(page).toHaveURL('/');

    // Verify success message
    await expect(page.locator('text=Algorithm deleted successfully')).toBeVisible();

    // Verify algorithm no longer exists
    await page.goto('/algorithms/binary-search');
    await expect(page.locator('text=404')).toBeVisible();
  });

  test('form validation prevents submission with incomplete data', async ({ page }) => {
    // Login
    await page.fill('[data-testid="email-input"]', testAdmin.email);
    await page.fill('[data-testid="password-input"]', testAdmin.password);
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/admin/dashboard');

    // Navigate to create algorithm page
    await page.click('text=Create Algorithm');

    // Try to submit with only title (missing required fields)
    await page.fill('[data-testid="title-input"]', 'Incomplete Algorithm');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify validation error messages appear
    await expect(page.locator('text=Category is required')).toBeVisible();
    await expect(page.locator('text=Difficulty is required')).toBeVisible();
    await expect(page.locator('text=Concept summary is required')).toBeVisible();

    // Should stay on create page
    await expect(page).toHaveURL('/admin/algorithms/create');
  });

  test('non-admin user cannot access admin pages', async ({ page }) => {
    // Try to access admin dashboard without login
    await page.goto('/admin/dashboard');

    // Should redirect to login page
    await expect(page).toHaveURL('/admin/login');

    // Try to access create page
    await page.goto('/admin/algorithms/create');

    // Should redirect to login page
    await expect(page).toHaveURL('/admin/login');
  });
});
