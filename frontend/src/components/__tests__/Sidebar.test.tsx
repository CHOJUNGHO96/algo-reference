/**
 * Unit tests for Sidebar component
 *
 * Tests category list rendering, filtering, and active state.
 */

import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Sidebar } from '../layout/Sidebar';

// Mock the RTK Query hook
vi.mock('../../store/api/algorithmApi', () => ({
  useListCategoriesQuery: vi.fn(),
}));

import { useListCategoriesQuery } from '../../store/api/algorithmApi';

// Mock categories data
const mockCategories = [
  { id: 1, name: 'Two Pointer', slug: 'two-pointer', color: '#0969da', description: 'Two pointer algorithms' },
  { id: 2, name: 'Sliding Window', slug: 'sliding-window', color: '#1f883d', description: 'Sliding window algorithms' },
  { id: 3, name: 'Binary Search', slug: 'binary-search', color: '#d29922', description: 'Binary search algorithms' },
];

describe('Sidebar', () => {
  beforeEach(() => {
    // Default mock implementation
    vi.mocked(useListCategoriesQuery).mockReturnValue({
      data: mockCategories,
      isLoading: false,
      isError: false,
      error: undefined,
      refetch: vi.fn(),
    } as any);
  });

  it('renders sidebar with categories header', () => {
    render(<Sidebar />);
    expect(screen.getByText('Categories')).toBeInTheDocument();
  });

  it('shows loading state while fetching categories', () => {
    vi.mocked(useListCategoriesQuery).mockReturnValue({
      data: undefined,
      isLoading: true,
      isError: false,
      error: undefined,
      refetch: vi.fn(),
    } as any);

    render(<Sidebar />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders "All Algorithms" button', () => {
    render(<Sidebar />);
    expect(screen.getByText('All Algorithms')).toBeInTheDocument();
  });

  it('renders all category items', () => {
    render(<Sidebar />);

    expect(screen.getByText('Two Pointer')).toBeInTheDocument();
    expect(screen.getByText('Sliding Window')).toBeInTheDocument();
    expect(screen.getByText('Binary Search')).toBeInTheDocument();
  });

  it('applies active class to selected category', () => {
    render(<Sidebar selectedCategory={1} />);

    const twoPointerButton = screen.getByText('Two Pointer').closest('button');
    expect(twoPointerButton).toHaveClass('active');
  });

  it('applies active class to "All Algorithms" when no category selected', () => {
    render(<Sidebar selectedCategory={undefined} />);

    const allButton = screen.getByText('All Algorithms').closest('button');
    expect(allButton).toHaveClass('active');
  });

  it('calls onCategorySelect when category is clicked', () => {
    const onCategorySelect = vi.fn();
    render(<Sidebar onCategorySelect={onCategorySelect} />);

    const twoPointerButton = screen.getByText('Two Pointer').closest('button');
    fireEvent.click(twoPointerButton!);

    expect(onCategorySelect).toHaveBeenCalledWith(1);
  });

  it('calls onCategorySelect with undefined when "All Algorithms" is clicked', () => {
    const onCategorySelect = vi.fn();
    render(<Sidebar selectedCategory={1} onCategorySelect={onCategorySelect} />);

    const allButton = screen.getByText('All Algorithms').closest('button');
    fireEvent.click(allButton!);

    expect(onCategorySelect).toHaveBeenCalledWith(undefined);
  });

  it('toggles category selection when same category is clicked again', () => {
    const onCategorySelect = vi.fn();
    render(<Sidebar selectedCategory={1} onCategorySelect={onCategorySelect} />);

    const twoPointerButton = screen.getByText('Two Pointer').closest('button');
    fireEvent.click(twoPointerButton!);

    // Should deselect (set to undefined) when clicking already selected category
    expect(onCategorySelect).toHaveBeenCalledWith(undefined);
  });

  it('applies category color to color indicator', () => {
    const { container } = render(<Sidebar />);

    const colorIndicators = container.querySelectorAll('.category-color');
    expect(colorIndicators).toHaveLength(3); // One for each category

    // Check first category has correct color
    expect(colorIndicators[0]).toHaveStyle({ backgroundColor: '#0969da' });
  });

  it('uses fallback color when category color is missing', () => {
    vi.mocked(useListCategoriesQuery).mockReturnValue({
      data: [{ id: 1, name: 'Test Category', slug: 'test', color: null, description: 'Test' }],
      isLoading: false,
      isError: false,
      error: undefined,
      refetch: vi.fn(),
    } as any);

    const { container } = render(<Sidebar />);

    const colorIndicator = container.querySelector('.category-color');
    // Should use CSS variable as fallback
    expect(colorIndicator).toHaveStyle({ backgroundColor: 'var(--accent-blue)' });
  });

  it('renders as aside element for semantic HTML', () => {
    const { container} = render(<Sidebar />);

    const aside = container.querySelector('aside.sidebar');
    expect(aside).toBeInTheDocument();
  });

  it('renders nav element for accessibility', () => {
    const { container } = render(<Sidebar />);

    const nav = container.querySelector('nav.category-nav');
    expect(nav).toBeInTheDocument();
  });

  it('handles empty categories array', () => {
    vi.mocked(useListCategoriesQuery).mockReturnValue({
      data: [],
      isLoading: false,
      isError: false,
      error: undefined,
      refetch: vi.fn(),
    } as any);

    render(<Sidebar />);

    // Should still show "All Algorithms" button
    expect(screen.getByText('All Algorithms')).toBeInTheDocument();

    // But no category items
    expect(screen.queryByText('Two Pointer')).not.toBeInTheDocument();
  });

  it('does not call onCategorySelect when prop is undefined', () => {
    render(<Sidebar />);

    const twoPointerButton = screen.getByText('Two Pointer').closest('button');

    // Should not throw error when onCategorySelect is undefined
    expect(() => fireEvent.click(twoPointerButton!)).not.toThrow();
  });

  it('renders category items as buttons for accessibility', () => {
    render(<Sidebar />);

    const buttons = screen.getAllByRole('button');
    // Should have 4 buttons: "All Algorithms" + 3 categories
    expect(buttons).toHaveLength(4);
  });

  it('maintains active state correctly when switching categories', () => {
    const { rerender } = render(<Sidebar selectedCategory={1} />);

    let twoPointerButton = screen.getByText('Two Pointer').closest('button');
    expect(twoPointerButton).toHaveClass('active');

    // Rerender with different selected category
    rerender(<Sidebar selectedCategory={2} />);

    twoPointerButton = screen.getByText('Two Pointer').closest('button');
    const slidingWindowButton = screen.getByText('Sliding Window').closest('button');

    expect(twoPointerButton).not.toHaveClass('active');
    expect(slidingWindowButton).toHaveClass('active');
  });
});
