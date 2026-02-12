import { Link } from 'react-router-dom';
import { RocketOutlined, BookOutlined, ThunderboltOutlined } from '@ant-design/icons';
import './HomePage.css';

export const HomePage = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            패턴 기반 학습으로
            <span className="gradient-text"> 알고리즘 마스터하기</span>
          </h1>
          <p className="hero-subtitle">
            공식과 패턴별로 정리된 종합 알고리즘 참고서.
            체계적인 구조와 코드 템플릿으로 더 빠르게 학습하세요.
          </p>
          <Link to="/algorithms" className="cta-button">
            <RocketOutlined /> 알고리즘 탐색
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">AlgoRef를 선택하는 이유</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <BookOutlined />
            </div>
            <h3 className="feature-title">8가지 구조화</h3>
            <p className="feature-description">
              모든 알고리즘은 일관된 8가지 섹션(개념, 공식, 사고 과정, 복잡도, 예제 등)으로
              구성되어 있습니다.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <ThunderboltOutlined />
            </div>
            <h3 className="feature-title">패턴 기반</h3>
            <p className="feature-description">
              핵심 공식과 패턴(투 포인터, 슬라이딩 윈도우 등)별로 정리되어
              더 빠른 패턴 인식이 가능합니다.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <RocketOutlined />
            </div>
            <h3 className="feature-title">코드 템플릿</h3>
            <p className="feature-description">
              다양한 프로그래밍 언어의 코드 템플릿을 문법 강조와 복사 기능과 함께
              제공합니다.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2 className="cta-title">실력을 향상시킬 준비가 되셨나요?</h2>
        <p className="cta-subtitle">
          패턴과 공식별로 정리된 알고리즘을 지금 바로 탐색해보세요
        </p>
        <Link to="/algorithms" className="cta-button secondary">
          모든 알고리즘 둘러보기
        </Link>
      </section>
    </div>
  );
};
