import { Navigate } from 'react-router-dom';
import { useGetCurrentUserQuery } from '../../store/api/algorithmApi';
import { Spin } from 'antd';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const token = localStorage.getItem('access_token');

  // Verify token with backend (always call hooks unconditionally)
  const { isLoading, error } = useGetCurrentUserQuery(undefined, {
    skip: !token, // Skip query if no token
  });

  // If no token, redirect to login
  if (!token) {
    return <Navigate to="/admin" replace />;
  }

  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '400px'
      }}>
        <Spin size="large" tip="Verifying authentication..." />
      </div>
    );
  }

  // If token is invalid, redirect to login
  if (error) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return <Navigate to="/admin" replace />;
  }

  // Token is valid, render protected content
  return <>{children}</>;
};
