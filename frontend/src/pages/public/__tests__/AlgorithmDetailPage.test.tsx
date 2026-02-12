import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AlgorithmDetailPage } from '../AlgorithmDetailPage';
import { useGetAlgorithmBySlugQuery } from '../../../store/api/algorithmApi';

// Mock the RTK Query hook
vi.mock('../../../store/api/algorithmApi', () => ({
  useGetAlgorithmBySlugQuery: vi.fn(),
}));

// Mock CodeBlock component
vi.mock('../../../components/code/CodeBlock', () => ({
  CodeBlock: ({ code, language, explanation }: { code: string; language: string; explanation?: string }) => (
    <div data-testid="code-block">
      <div data-testid="code-language">{language}</div>
      <div data-testid="code-content">{code}</div>
      {explanation && <div data-testid="code-explanation">{explanation}</div>}
    </div>
  ),
}));

const mockAlgorithm = {
  id: 1,
  title: 'Two Pointer Technique',
  slug: 'two-pointer-technique',
  category: {
    id: 1,
    name: 'Two Pointer',
    slug: 'two-pointer',
    color: '#0969da',
  },
  difficulty: {
    id: 1,
    name: 'Easy',
  },
  concept_summary: 'A technique that uses two pointers to solve problems efficiently.',
  core_formulas: [
    {
      name: 'Basic Two Pointer',
      formula: 'left = 0, right = n-1',
      description: 'Start from both ends',
    },
  ],
  thought_process: 'Step 1: Initialize two pointers\nStep 2: Move pointers based on condition',
  application_conditions: {
    when_to_use: ['Sorted arrays', 'Searching pairs'],
    when_not_to_use: ['Unsorted data', 'Single pointer sufficient'],
  },
  time_complexity: 'O(n)',
  space_complexity: 'O(1)',
  problem_types: [
    {
      type: 'Container With Most Water',
      leetcode_examples: ['LC 11 - Container With Most Water', 'LC 42 - Trapping Rain Water'],
    },
  ],
  code_templates: [
    {
      id: 1,
      language: { prism_key: 'python' },
      code: 'def twoPointer(arr):\n    left, right = 0, len(arr) - 1',
      explanation: 'Basic Python implementation',
    },
    {
      id: 2,
      language: { prism_key: 'javascript' },
      code: 'function twoPointer(arr) {\n    let left = 0, right = arr.length - 1;',
      explanation: 'JavaScript version',
    },
  ],
  common_mistakes: 'Mistake 1: Not checking array bounds\nMistake 2: Incorrect pointer movement',
  view_count: 1250,
  updated_at: '2024-01-15T10:30:00Z',
};

const renderWithRouter = (slug = 'two-pointer-technique') => {
  return render(
    <BrowserRouter>
      <Routes>
        <Route path="/algorithms/:slug" element={<AlgorithmDetailPage />} />
      </Routes>
    </BrowserRouter>,
    { wrapper: ({ children }) => <BrowserRouter><Routes><Route path="*" element={<div>{children}</div>} /></Routes></BrowserRouter> }
  );
};

const renderWithPath = (slug: string) => {
  window.history.pushState({}, '', `/algorithms/${slug}`);
  return render(
    <BrowserRouter>
      <Routes>
        <Route path="/algorithms/:slug" element={<AlgorithmDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
};

describe('AlgorithmDetailPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
      data: mockAlgorithm,
      isLoading: false,
      error: undefined,
    } as never);
  });

  describe('Loading State', () => {
    it('shows loading message while fetching', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: undefined,
        isLoading: true,
        error: undefined,
      } as never);
      renderWithPath('two-pointer-technique');
      expect(screen.getByText('Loading algorithm...')).toBeInTheDocument();
    });

    it('does not show content while loading', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: undefined,
        isLoading: true,
        error: undefined,
      } as never);
      renderWithPath('two-pointer-technique');
      expect(screen.queryByText('Two Pointer Technique')).not.toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('shows error message when algorithm not found', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: undefined,
        isLoading: false,
        error: { status: 404, data: 'Not found' },
      } as never);
      renderWithPath('nonexistent');
      expect(screen.getByText(/Algorithm not found/)).toBeInTheDocument();
    });

    it('shows back link in error state', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: undefined,
        isLoading: false,
        error: { status: 404, data: 'Not found' },
      } as never);
      renderWithPath('nonexistent');
      expect(screen.getByText(/Back to algorithms/)).toBeInTheDocument();
    });

    it('shows error when data is null', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: null,
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('null-data');
      expect(screen.getByText(/Algorithm not found/)).toBeInTheDocument();
    });
  });

  describe('Header Section', () => {
    beforeEach(() => {
      renderWithPath('two-pointer-technique');
    });

    it('renders algorithm title', () => {
      expect(screen.getByText('Two Pointer Technique')).toBeInTheDocument();
    });

    it('renders category badge with name', () => {
      expect(screen.getByText('Two Pointer')).toBeInTheDocument();
    });

    it('renders difficulty badge', () => {
      expect(screen.getByText('Easy')).toBeInTheDocument();
    });

    it('applies correct difficulty class', () => {
      const difficultyBadge = screen.getByText('Easy').closest('.difficulty-badge');
      expect(difficultyBadge).toHaveClass('difficulty-easy');
    });

    it('displays view count with formatting', () => {
      expect(screen.getByText(/1,250 views/)).toBeInTheDocument();
    });

    it('displays updated date', () => {
      expect(screen.getByText(/Updated/)).toBeInTheDocument();
    });

    it('renders back to algorithms link', () => {
      expect(screen.getByText(/Back to Algorithms/)).toBeInTheDocument();
    });
  });

  describe('Content Sections', () => {
    beforeEach(() => {
      renderWithPath('two-pointer-technique');
    });

    it('renders section 1: Concept Summary', () => {
      expect(screen.getByText('1. Concept Summary')).toBeInTheDocument();
      expect(screen.getByText(/A technique that uses two pointers/)).toBeInTheDocument();
    });

    it('renders section 2: Core Formulas', () => {
      expect(screen.getByText('2. Core Formulas & Patterns')).toBeInTheDocument();
      expect(screen.getByText('Basic Two Pointer')).toBeInTheDocument();
      expect(screen.getByText('left = 0, right = n-1')).toBeInTheDocument();
      expect(screen.getByText('Start from both ends')).toBeInTheDocument();
    });

    it('renders section 3: Thought Process', () => {
      expect(screen.getByText('3. Thought Process')).toBeInTheDocument();
      expect(screen.getByText(/Step 1: Initialize two pointers/)).toBeInTheDocument();
    });

    it('renders section 4: Application Conditions - Use when', () => {
      expect(screen.getByText('4. When to Use')).toBeInTheDocument();
      expect(screen.getByText(/Use when:/)).toBeInTheDocument();
      expect(screen.getByText('Sorted arrays')).toBeInTheDocument();
      expect(screen.getByText('Searching pairs')).toBeInTheDocument();
    });

    it('renders section 4: Application Conditions - Avoid when', () => {
      expect(screen.getByText(/Avoid when:/)).toBeInTheDocument();
      expect(screen.getByText('Unsorted data')).toBeInTheDocument();
      expect(screen.getByText('Single pointer sufficient')).toBeInTheDocument();
    });

    it('renders section 5: Complexity Analysis', () => {
      expect(screen.getByText('5. Complexity Analysis')).toBeInTheDocument();
      expect(screen.getByText('Time Complexity')).toBeInTheDocument();
      expect(screen.getByText('O(n)')).toBeInTheDocument();
      expect(screen.getByText('Space Complexity')).toBeInTheDocument();
      expect(screen.getByText('O(1)')).toBeInTheDocument();
    });

    it('renders section 6: Representative Problems', () => {
      expect(screen.getByText('6. Representative Problems')).toBeInTheDocument();
      expect(screen.getByText('Container With Most Water')).toBeInTheDocument();
      expect(screen.getByText(/LC 11 - Container With Most Water/)).toBeInTheDocument();
      expect(screen.getByText(/LC 42 - Trapping Rain Water/)).toBeInTheDocument();
    });

    it('renders section 7: Code Templates', () => {
      expect(screen.getByText('7. Code Templates')).toBeInTheDocument();
      const codeBlocks = screen.getAllByTestId('code-block');
      expect(codeBlocks).toHaveLength(2);
    });

    it('renders code templates with correct languages', () => {
      const languages = screen.getAllByTestId('code-language');
      expect(languages[0]).toHaveTextContent('python');
      expect(languages[1]).toHaveTextContent('javascript');
    });

    it('renders code templates with content', () => {
      const codeContents = screen.getAllByTestId('code-content');
      expect(codeContents[0]).toHaveTextContent('def twoPointer(arr)');
      expect(codeContents[1]).toHaveTextContent('function twoPointer(arr)');
    });

    it('renders code templates with explanations', () => {
      const explanations = screen.getAllByTestId('code-explanation');
      expect(explanations[0]).toHaveTextContent('Basic Python implementation');
      expect(explanations[1]).toHaveTextContent('JavaScript version');
    });

    it('renders section 8: Common Mistakes', () => {
      expect(screen.getByText('8. Common Mistakes')).toBeInTheDocument();
      expect(screen.getByText(/Mistake 1: Not checking array bounds/)).toBeInTheDocument();
    });
  });

  describe('Conditional Rendering', () => {
    it('does not render core formulas section when empty', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, core_formulas: [] },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('2. Core Formulas & Patterns')).not.toBeInTheDocument();
    });

    it('does not render core formulas section when null', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, core_formulas: null },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('2. Core Formulas & Patterns')).not.toBeInTheDocument();
    });

    it('does not render thought process when null', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, thought_process: null },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('3. Thought Process')).not.toBeInTheDocument();
    });

    it('does not render application conditions when null', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, application_conditions: null },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('4. When to Use')).not.toBeInTheDocument();
    });

    it('does not render problem types when empty', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, problem_types: [] },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('6. Representative Problems')).not.toBeInTheDocument();
    });

    it('does not render code templates when empty', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, code_templates: [] },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('7. Code Templates')).not.toBeInTheDocument();
    });

    it('does not render common mistakes when null', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, common_mistakes: null },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText('8. Common Mistakes')).not.toBeInTheDocument();
    });
  });

  describe('Difficulty Class Mapping', () => {
    it('applies correct class for Medium difficulty', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, difficulty: { id: 2, name: 'Medium' } },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      const difficultyBadge = screen.getByText('Medium').closest('.difficulty-badge');
      expect(difficultyBadge).toHaveClass('difficulty-medium');
    });

    it('applies correct class for Hard difficulty', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, difficulty: { id: 3, name: 'Hard' } },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      const difficultyBadge = screen.getByText('Hard').closest('.difficulty-badge');
      expect(difficultyBadge).toHaveClass('difficulty-hard');
    });
  });

  describe('Edge Cases', () => {
    it('handles missing category color with fallback', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, category: { ...mockAlgorithm.category, color: undefined } },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      // Component should still render without error
      expect(screen.getByText('Two Pointer')).toBeInTheDocument();
    });

    it('handles zero views', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, view_count: 0 },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.getByText(/0 views/)).toBeInTheDocument();
    });

    it('handles large view counts with formatting', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: { ...mockAlgorithm, view_count: 1234567 },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.getByText(/1,234,567 views/)).toBeInTheDocument();
    });

    it('renders when application_conditions has only when_to_use', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: {
          ...mockAlgorithm,
          application_conditions: { when_to_use: ['Use case 1'], when_not_to_use: null },
        },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.getByText(/Use when:/)).toBeInTheDocument();
      expect(screen.queryByText(/Avoid when:/)).not.toBeInTheDocument();
    });

    it('renders when application_conditions has only when_not_to_use', () => {
      vi.mocked(useGetAlgorithmBySlugQuery).mockReturnValue({
        data: {
          ...mockAlgorithm,
          application_conditions: { when_to_use: null, when_not_to_use: ['Avoid case 1'] },
        },
        isLoading: false,
        error: undefined,
      } as never);
      renderWithPath('test');
      expect(screen.queryByText(/Use when:/)).not.toBeInTheDocument();
      expect(screen.getByText(/Avoid when:/)).toBeInTheDocument();
    });
  });
});
