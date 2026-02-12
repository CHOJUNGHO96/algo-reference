/**
 * Test data fixtures for E2E tests
 *
 * Provides reusable test data for algorithm entities.
 */

export const testAlgorithm = {
  title: 'Two Pointer Technique',
  slug: 'two-pointer-technique',
  category: 'Two Pointer',
  difficulty: 'Medium',
  conceptSummary: 'The two pointer technique uses two indices to traverse data structures efficiently.',
  timeComplexity: 'O(n)',
  spaceComplexity: 'O(1)',
};

export const testAdmin = {
  email: 'admin@test.com',
  password: 'adminpass123',
};

export const newAlgorithm = {
  title: 'Binary Search',
  category: 'Binary Search',
  difficulty: 'Easy',
  conceptSummary: 'Binary search is a divide-and-conquer algorithm for finding elements in sorted arrays.',
  coreFormulas: 'mid = (left + right) // 2',
  thoughtProcess: '1. Find middle element\n2. Compare with target\n3. Narrow search space',
  applicationConditions: 'Array must be sorted',
  timeComplexity: 'O(log n)',
  spaceComplexity: 'O(1)',
  problemTypes: 'Search in sorted array, find first/last occurrence',
  commonMistakes: 'Integer overflow in mid calculation, off-by-one errors',
  codeTemplate: `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1`,
};

export const categories = [
  { name: 'Two Pointer', slug: 'two-pointer', color: '#0969da' },
  { name: 'Binary Search', slug: 'binary-search', color: '#6f42c1' },
  { name: 'Sliding Window', slug: 'sliding-window', color: '#22863a' },
];

export const difficulties = [
  { name: 'Easy', color: '#22863a' },
  { name: 'Medium', color: '#d29922' },
  { name: 'Hard', color: '#cf222e' },
];
