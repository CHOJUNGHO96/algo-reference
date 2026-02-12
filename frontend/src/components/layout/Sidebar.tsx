import { useListCategoriesQuery } from '../../store/api/algorithmApi';
import './Sidebar.css';

interface SidebarProps {
  selectedCategory?: number;
  onCategorySelect?: (categoryId: number | undefined) => void;
}

export const Sidebar = ({ selectedCategory, onCategorySelect }: SidebarProps) => {
  const { data: categories, isLoading } = useListCategoriesQuery();

  const handleCategoryClick = (categoryId: number) => {
    if (onCategorySelect) {
      onCategorySelect(selectedCategory === categoryId ? undefined : categoryId);
    }
  };

  if (isLoading) {
    return (
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>카테고리</h2>
        </div>
        <div className="sidebar-loading">로딩 중...</div>
      </aside>
    );
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>카테고리</h2>
      </div>

      <nav className="category-nav">
        <button
          className={`category-item ${!selectedCategory ? 'active' : ''}`}
          onClick={() => onCategorySelect?.(undefined)}
        >
          <span className="category-name">모든 알고리즘</span>
        </button>

        {categories?.map((category) => (
          <button
            key={category.id}
            className={`category-item ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => handleCategoryClick(category.id)}
          >
            <span
              className="category-color"
              style={{ backgroundColor: category.color || 'var(--accent-blue)' }}
            />
            <span className="category-name">{category.name}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
};
