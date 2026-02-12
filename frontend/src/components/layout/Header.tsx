import { Link } from 'react-router-dom';
import { SearchOutlined, LoginOutlined, GithubOutlined } from '@ant-design/icons';
import './Header.css';

export const Header = () => {
  return (
    <header className="app-header">
      <div className="header-container">
        {/* Logo */}
        <Link to="/" className="header-logo">
          <span className="logo-text">AlgoRef</span>
        </Link>

        {/* Search (placeholder for now) */}
        <div className="header-search">
          <SearchOutlined className="search-icon" />
          <input
            type="text"
            placeholder="알고리즘 검색..."
            className="search-input"
          />
        </div>

        {/* Navigation */}
        <nav className="header-nav">
          <Link to="/algorithms" className="nav-link">
            알고리즘
          </Link>
          <a
            href="https://github.com/CHOJUNGHO96/algo-reference"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-link"
            title="GitHub 저장소"
          >
            <GithubOutlined />
          </a>
          <Link to="/admin" className="nav-link admin-link">
            <LoginOutlined /> 관리자
          </Link>
        </nav>
      </div>
    </header>
  );
};
