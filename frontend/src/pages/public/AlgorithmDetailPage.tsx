import { useParams, Link } from 'react-router-dom';
import { LeftOutlined, EyeOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { useGetAlgorithmBySlugQuery } from '../../store/api/algorithmApi';
import { CodeBlock } from '../../components/code/CodeBlock';
import './AlgorithmDetailPage.css';

export const AlgorithmDetailPage = () => {
  const { slug } = useParams<{ slug: string }>();
  const { data: algorithm, isLoading, error } = useGetAlgorithmBySlugQuery(slug!);

  if (isLoading) {
    return (
      <div className="algorithm-detail-page">
        <div className="loading-state">알고리즘 로딩 중...</div>
      </div>
    );
  }

  if (error || !algorithm) {
    return (
      <div className="algorithm-detail-page">
        <div className="error-state">
          알고리즘을 찾을 수 없습니다. <Link to="/algorithms">알고리즘 목록으로 돌아가기</Link>
        </div>
      </div>
    );
  }

  const getDifficultyClass = (difficulty: string) => {
    return `difficulty-${difficulty.toLowerCase()}`;
  };

  return (
    <div className="algorithm-detail-page">
      {/* Back button */}
      <Link to="/algorithms" className="back-link">
        <LeftOutlined /> 알고리즘 목록으로
      </Link>

      {/* Header */}
      <header className="algorithm-header">
        <div className="header-main">
          <h1 className="algorithm-title">{algorithm.title}</h1>
          <div className="header-badges">
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

        <div className="header-meta">
          <span className="meta-item">
            <EyeOutlined /> 조회수 {algorithm.view_count.toLocaleString()}
          </span>
          <span className="meta-item">
            <ClockCircleOutlined /> 업데이트 {new Date(algorithm.updated_at).toLocaleDateString('ko-KR')}
          </span>
        </div>
      </header>

      {/* Content Sections */}
      <div className="algorithm-content">
        {/* Section 1: Concept Summary */}
        <section className="content-section">
          <h2 className="section-heading">1. 개념 요약</h2>
          <p className="section-text">{algorithm.concept_summary}</p>
        </section>

        {/* Section 2: Core Formulas/Patterns */}
        {algorithm.core_formulas && algorithm.core_formulas.length > 0 && (
          <section className="content-section">
            <h2 className="section-heading">2. 핵심 공식과 패턴</h2>
            <div className="formulas-grid">
              {algorithm.core_formulas.map((formula, index) => (
                <div key={index} className="formula-card">
                  <h3 className="formula-name">{formula.name}</h3>
                  <code className="formula-code">{formula.formula}</code>
                  <p className="formula-description">{formula.description}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Section 3: Thought Process */}
        {algorithm.thought_process && (
          <section className="content-section">
            <h2 className="section-heading">3. 사고 과정</h2>
            <pre className="thought-process">{algorithm.thought_process}</pre>
          </section>
        )}

        {/* Section 4: Application Conditions */}
        {algorithm.application_conditions && (
          <section className="content-section">
            <h2 className="section-heading">4. 사용 조건</h2>
            <div className="conditions-grid">
              {algorithm.application_conditions.when_to_use && (
                <div className="condition-box use">
                  <h3 className="condition-title">✅ 사용 시기:</h3>
                  <ul className="condition-list">
                    {algorithm.application_conditions.when_to_use.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              {algorithm.application_conditions.when_not_to_use && (
                <div className="condition-box avoid">
                  <h3 className="condition-title">❌ 피해야 할 경우:</h3>
                  <ul className="condition-list">
                    {algorithm.application_conditions.when_not_to_use.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Section 5: Complexity Analysis */}
        <section className="content-section">
          <h2 className="section-heading">5. 복잡도 분석</h2>
          <div className="complexity-grid">
            <div className="complexity-box">
              <span className="complexity-label">시간 복잡도</span>
              <code className="complexity-value">{algorithm.time_complexity}</code>
            </div>
            <div className="complexity-box">
              <span className="complexity-label">공간 복잡도</span>
              <code className="complexity-value">{algorithm.space_complexity}</code>
            </div>
          </div>
        </section>

        {/* Section 6: Representative Problem Types */}
        {algorithm.problem_types && algorithm.problem_types.length > 0 && (
          <section className="content-section">
            <h2 className="section-heading">6. 대표 문제 유형</h2>
            <div className="problems-list">
              {algorithm.problem_types.map((problem, index) => (
                <div key={index} className="problem-type">
                  <h3 className="problem-type-name">{problem.type}</h3>
                  {problem.leetcode_examples && problem.leetcode_examples.length > 0 && (
                    <ul className="leetcode-examples">
                      {problem.leetcode_examples.map((example, idx) => (
                        <li key={idx} className="leetcode-example">
                          {example}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Section 7: Code Templates */}
        {algorithm.code_templates && algorithm.code_templates.length > 0 && (
          <section className="content-section">
            <h2 className="section-heading">7. 코드 템플릿</h2>
            {algorithm.code_templates.map((template) => (
              <CodeBlock
                key={template.id}
                code={template.code}
                language={template.language.prism_key}
                explanation={template.explanation}
              />
            ))}
          </section>
        )}

        {/* Section 8: Common Mistakes */}
        {algorithm.common_mistakes && (
          <section className="content-section">
            <h2 className="section-heading">8. 흔한 실수</h2>
            <pre className="common-mistakes">{algorithm.common_mistakes}</pre>
          </section>
        )}
      </div>
    </div>
  );
};
