/**
 * Unit tests for AlgorithmCard component
 *
 * Tests component rendering, content display, and user interactions.
 */

import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { AlgorithmCard } from '../algorithm/AlgorithmCard';
import type { AlgorithmList } from '../../types/api';

// Helper function to render component with Router
const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

// Mock algorithm data
const mockAlgorithm: AlgorithmList = {
  id: 1,
  title: 'Two Pointer Technique',
  slug: 'two-pointer-technique',
  category: {
    id: 1,
    name: 'Two Pointer',
    slug: 'two-pointer',
    color: '#0969da',
    description: 'Two pointer algorithms',
  },
  difficulty: {
    id: 2,
    name: 'Medium',
    color: '#d29922',
  },
  concept_summary: 'The two pointer technique uses two indices to traverse data structures efficiently.',
  time_complexity: 'O(n)',
  space_complexity: 'O(1)',
  view_count: 1250,
  is_published: true,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

describe('AlgorithmCard', () => {
  it('renders algorithm title', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    expect(screen.getByText('Two Pointer Technique')).toBeInTheDocument();
  });

  it('renders category badge with correct name', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const categoryBadge = screen.getByText('Two Pointer');
    expect(categoryBadge).toBeInTheDocument();
  });

  it('applies category color to badge', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const categoryBadge = screen.getByText('Two Pointer');
    expect(categoryBadge).toHaveStyle({ backgroundColor: '#0969da' });
  });

  it('renders difficulty badge with correct name', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const difficultyBadge = screen.getByText('Medium');
    expect(difficultyBadge).toBeInTheDocument();
    expect(difficultyBadge).toHaveClass('difficulty-badge');
  });

  it('applies difficulty-specific CSS class', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const difficultyBadge = screen.getByText('Medium');
    expect(difficultyBadge).toHaveClass('difficulty-medium');
  });

  it('displays time complexity', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    expect(screen.getByText('Time:')).toBeInTheDocument();
    expect(screen.getByText('O(n)')).toBeInTheDocument();
  });

  it('displays space complexity', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    expect(screen.getByText('Space:')).toBeInTheDocument();
    expect(screen.getByText('O(1)')).toBeInTheDocument();
  });

  it('displays view count with formatting', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    // 1250 should be formatted as "1,250"
    expect(screen.getByText('1,250')).toBeInTheDocument();
  });

  it('truncates long concept summary', () => {
    const longAlgorithm = {
      ...mockAlgorithm,
      concept_summary: 'A'.repeat(200), // 200 characters
    };
    renderWithRouter(<AlgorithmCard algorithm={longAlgorithm} />);
    const summary = screen.getByText(/A+\.\.\./);
    expect(summary.textContent?.length).toBeLessThan(200);
    expect(summary.textContent).toMatch(/\.\.\.$/);
  });

  it('does not truncate short concept summary', () => {
    const shortAlgorithm = {
      ...mockAlgorithm,
      concept_summary: 'Short summary',
    };
    renderWithRouter(<AlgorithmCard algorithm={shortAlgorithm} />);
    const summary = screen.getByText('Short summary');
    expect(summary.textContent).not.toMatch(/\.\.\.$/);
  });

  it('navigates to correct algorithm detail page', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/algorithms/two-pointer-technique');
  });

  it('renders as article element for semantic HTML', () => {
    const { container } = renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    const article = container.querySelector('article');
    expect(article).toBeInTheDocument();
    expect(article).toHaveClass('algorithm-card');
  });

  it('displays view count icon', () => {
    renderWithRouter(<AlgorithmCard algorithm={mockAlgorithm} />);
    // EyeOutlined icon from Ant Design should be present
    const viewCountSection = screen.getByText('1,250').parentElement;
    expect(viewCountSection).toBeInTheDocument();
  });

  it('handles algorithm with zero views', () => {
    const noViewsAlgorithm = {
      ...mockAlgorithm,
      view_count: 0,
    };
    renderWithRouter(<AlgorithmCard algorithm={noViewsAlgorithm} />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  it('handles algorithm with large view count', () => {
    const popularAlgorithm = {
      ...mockAlgorithm,
      view_count: 1234567,
    };
    renderWithRouter(<AlgorithmCard algorithm={popularAlgorithm} />);
    // Should format with commas: 1,234,567
    expect(screen.getByText('1,234,567')).toBeInTheDocument();
  });

  it('handles different difficulty levels correctly', () => {
    const easyAlgorithm = {
      ...mockAlgorithm,
      difficulty: { id: 1, name: 'Easy', color: '#00ff00' },
    };
    renderWithRouter(<AlgorithmCard algorithm={easyAlgorithm} />);
    const difficultyBadge = screen.getByText('Easy');
    expect(difficultyBadge).toHaveClass('difficulty-easy');
  });

  it('truncates at exactly 120 characters', () => {
    const exactLengthSummary = 'A'.repeat(120);
    const algorithm = {
      ...mockAlgorithm,
      concept_summary: exactLengthSummary,
    };
    renderWithRouter(<AlgorithmCard algorithm={algorithm} />);
    const summary = screen.getByText(exactLengthSummary);
    expect(summary.textContent).not.toMatch(/\.\.\.$/);
  });

  it('truncates at 121 characters', () => {
    const longSummary = 'A'.repeat(121);
    const algorithm = {
      ...mockAlgorithm,
      concept_summary: longSummary,
    };
    renderWithRouter(<AlgorithmCard algorithm={algorithm} />);
    const summaryText = screen.getByText(/A+\.\.\./);
    expect(summaryText.textContent).toMatch(/\.\.\.$/);
    expect(summaryText.textContent?.length).toBe(123); // 120 + '...'
  });
});
