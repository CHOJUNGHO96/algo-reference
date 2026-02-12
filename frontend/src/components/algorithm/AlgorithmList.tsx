import { AlgorithmCard } from './AlgorithmCard';
import type { AlgorithmList as AlgorithmListType } from '../../types/api';
import './AlgorithmList.css';

interface AlgorithmListProps {
  algorithms: AlgorithmListType[];
  loading?: boolean;
}

export const AlgorithmList = ({ algorithms, loading = false }: AlgorithmListProps) => {
  if (loading) {
    return (
      <div className="algorithm-grid">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="algorithm-card-skeleton" />
        ))}
      </div>
    );
  }

  if (algorithms.length === 0) {
    return (
      <div className="empty-state">
        <p>알고리즘이 없습니다</p>
      </div>
    );
  }

  return (
    <div className="algorithm-grid">
      {algorithms.map((algorithm) => (
        <AlgorithmCard key={algorithm.id} algorithm={algorithm} />
      ))}
    </div>
  );
};
