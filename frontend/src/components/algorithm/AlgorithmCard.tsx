import { Link } from 'react-router-dom';
import { EyeOutlined } from '@ant-design/icons';
import type { AlgorithmList } from '../../types/api';
import './AlgorithmCard.css';

interface AlgorithmCardProps {
  algorithm: AlgorithmList;
}

export const AlgorithmCard = ({ algorithm }: AlgorithmCardProps) => {
  const getDifficultyClass = (difficulty: string) => {
    return `difficulty-${difficulty.toLowerCase()}`;
  };

  const truncateSummary = (text: string, maxLength: number = 120) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength).trim() + '...';
  };

  return (
    <Link to={`/algorithms/${algorithm.slug}`} className="algorithm-card-link">
      <article className="algorithm-card">
        {/* Header */}
        <div className="card-header">
          <h3 className="card-title">{algorithm.title}</h3>
          <div className="card-badges">
            <span
              className="category-badge"
              style={{ backgroundColor: algorithm.category.color || 'var(--accent-blue)' }}
            >
              {algorithm.category.name}
            </span>
            <span className={`difficulty-badge ${getDifficultyClass(algorithm.difficulty.name)}`}>
              {algorithm.difficulty.name}
            </span>
          </div>
        </div>

        {/* Content */}
        <div className="card-content">
          <p className="card-summary">{truncateSummary(algorithm.concept_summary)}</p>
        </div>

        {/* Footer */}
        <div className="card-footer">
          <div className="complexity-badges">
            <span className="complexity-badge" title="시간 복잡도">
              <span className="complexity-label">시간:</span>
              <code className="complexity-value">{algorithm.time_complexity}</code>
            </span>
            <span className="complexity-badge" title="공간 복잡도">
              <span className="complexity-label">공간:</span>
              <code className="complexity-value">{algorithm.space_complexity}</code>
            </span>
          </div>

          <div className="view-count">
            <EyeOutlined />
            <span>{algorithm.view_count.toLocaleString()}</span>
          </div>
        </div>
      </article>
    </Link>
  );
};
