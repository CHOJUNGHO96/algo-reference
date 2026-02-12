import { GithubOutlined, HeartFilled } from '@ant-design/icons';
import './Footer.css';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="app-footer">
      <div className="footer-container">
        <div className="footer-content">
          <p className="footer-text">
            알고리즘 학습자들을 위해 <HeartFilled className="heart-icon" />로 제작
          </p>
          <p className="footer-copyright">
            © {currentYear} AlgoRef. 모든 권리 보유.
          </p>
        </div>

        <div className="footer-links">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            <GithubOutlined /> GitHub
          </a>
        </div>
      </div>
    </footer>
  );
};
