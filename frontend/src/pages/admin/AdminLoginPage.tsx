import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { useLoginMutation } from '../../store/api/algorithmApi';
import './AdminLoginPage.css';

export const AdminLoginPage = () => {
  const navigate = useNavigate();
  const [login, { isLoading, error }] = useLoginMutation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const result = await login({ email, password }).unwrap();
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);
      navigate('/admin/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div className="admin-login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>관리자 로그인</h1>
          <p>관리자 패널에 접근하려면 인증 정보를 입력하세요</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">
              <UserOutlined /> 이메일
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@algoref.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <LockOutlined /> 비밀번호
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <div className="error-message">
              잘못된 인증 정보입니다. 다시 시도해주세요.
            </div>
          )}

          <button type="submit" className="login-button" disabled={isLoading}>
            {isLoading ? '로그인 중...' : '로그인'}
          </button>
        </form>
      </div>
    </div>
  );
};
