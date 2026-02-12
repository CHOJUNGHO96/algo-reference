import { useState, useCallback } from 'react';
import { Input, Select, Pagination } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { Sidebar } from '../../components/layout/Sidebar';
import { AlgorithmList } from '../../components/algorithm/AlgorithmList';
import { useListAlgorithmsQuery, useListCategoriesQuery } from '../../store/api/algorithmApi';
import './AlgorithmListPage.css';

// Debounce utility
function useDebounce<T extends (...args: never[]) => void>(
  callback: T,
  delay: number
): (...args: Parameters<T>) => void {
  const [timeoutId, setTimeoutId] = useState<ReturnType<typeof setTimeout> | null>(null);

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutId) clearTimeout(timeoutId);
      const newTimeoutId = setTimeout(() => callback(...args), delay);
      setTimeoutId(newTimeoutId);
    },
    [callback, delay, timeoutId]
  );
}

const { Option } = Select;

export const AlgorithmListPage = () => {
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [selectedDifficulty, setSelectedDifficulty] = useState<number | undefined>();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [debouncedSearch, setDebouncedSearch] = useState<string>('');
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(12);

  const { data: categories } = useListCategoriesQuery();

  const { data, isLoading, error } = useListAlgorithmsQuery({
    page: currentPage,
    size: pageSize,
    category_id: selectedCategory,
    difficulty_id: selectedDifficulty,
    search: debouncedSearch || undefined,
    sort_by: 'created_at',
    order: 'desc',
  });

  // Debounced search handler
  const debouncedSetSearch = useDebounce((value: string) => {
    setDebouncedSearch(value);
    setCurrentPage(1); // Reset to first page on search
  }, 300);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    debouncedSetSearch(value);
  };

  const handleCategorySelect = (categoryId: number | undefined) => {
    setSelectedCategory(categoryId);
    setCurrentPage(1); // Reset to first page when category changes
  };

  const handleDifficultyChange = (difficultyId: number | undefined) => {
    setSelectedDifficulty(difficultyId);
    setCurrentPage(1);
  };

  const handlePageChange = (page: number, size: number) => {
    setCurrentPage(page);
    setPageSize(size);
  };

  const getFilterSummary = () => {
    const filters: string[] = [];
    if (selectedCategory) {
      const category = categories?.find((c) => c.id === selectedCategory);
      if (category) filters.push(category.name);
    }
    if (selectedDifficulty) {
      const difficultyNames = ['쉬움', '보통', '어려움'];
      filters.push(difficultyNames[selectedDifficulty - 1] || '');
    }
    if (debouncedSearch) filters.push(`"${debouncedSearch}"`);

    return filters.length > 0 ? `필터: ${filters.join(', ')}` : '';
  };

  return (
    <div className="algorithm-list-page">
      <Sidebar
        selectedCategory={selectedCategory}
        onCategorySelect={handleCategorySelect}
      />

      <main className="algorithm-list-content">
        {/* Filter Controls */}
        <div className="content-header">
          <div className="header-top">
            <h1 className="page-title">알고리즘 목록</h1>
            {data && (
              <p className="result-count">
                {data.total}개의 알고리즘
              </p>
            )}
          </div>

          <div className="filter-controls">
            {/* Search Bar */}
            <Input
              placeholder="알고리즘 검색..."
              prefix={<SearchOutlined />}
              value={searchQuery}
              onChange={handleSearchChange}
              className="search-input"
              allowClear
            />

            {/* Difficulty Filter */}
            <Select
              placeholder="모든 난이도"
              value={selectedDifficulty}
              onChange={handleDifficultyChange}
              className="difficulty-select"
              allowClear
              style={{ width: 180 }}
            >
              <Option value={1}>쉬움</Option>
              <Option value={2}>보통</Option>
              <Option value={3}>어려움</Option>
            </Select>

            {/* Page Size Selector */}
            <Select
              value={pageSize}
              onChange={(value) => {
                setPageSize(value);
                setCurrentPage(1);
              }}
              className="page-size-select"
              style={{ width: 120 }}
            >
              <Option value={12}>12개씩 보기</Option>
              <Option value={24}>24개씩 보기</Option>
              <Option value={48}>48개씩 보기</Option>
            </Select>
          </div>

          {/* Active Filters Summary */}
          {getFilterSummary() && (
            <p className="filter-summary">{getFilterSummary()}</p>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            알고리즘을 불러오는데 실패했습니다. 나중에 다시 시도해주세요.
          </div>
        )}

        {/* Algorithm Grid */}
        <AlgorithmList algorithms={data?.items || []} loading={isLoading} />

        {/* Empty State */}
        {!isLoading && data?.items.length === 0 && (
          <div className="empty-state">
            <p>검색 조건에 맞는 알고리즘이 없습니다.</p>
            <button
              onClick={() => {
                setSelectedCategory(undefined);
                setSelectedDifficulty(undefined);
                setSearchQuery('');
                setDebouncedSearch('');
              }}
              className="reset-filters-button"
            >
              필터 초기화
            </button>
          </div>
        )}

        {/* Pagination */}
        {data && data.pages > 1 && (
          <div className="pagination-container">
            <Pagination
              current={currentPage}
              total={data.total}
              pageSize={pageSize}
              onChange={handlePageChange}
              showSizeChanger={false}
              showTotal={(total, range) => `전체 ${total}개 중 ${range[0]}-${range[1]}`}
            />
          </div>
        )}
      </main>
    </div>
  );
};
