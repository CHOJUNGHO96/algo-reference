import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { HomePage } from './pages/public/HomePage';
import { AlgorithmListPage } from './pages/public/AlgorithmListPage';
import { AlgorithmDetailPage } from './pages/public/AlgorithmDetailPage';
import { AdminLoginPage } from './pages/admin/AdminLoginPage';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AlgorithmEditor } from './pages/admin/AlgorithmEditor';
import './styles/theme.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Header />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/algorithms" element={<AlgorithmListPage />} />
          <Route path="/algorithms/:slug" element={<AlgorithmDetailPage />} />

          {/* Admin Routes */}
          <Route path="/admin" element={<AdminLoginPage />} />
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/algorithms/new"
            element={
              <ProtectedRoute>
                <AlgorithmEditor />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/algorithms/:id/edit"
            element={
              <ProtectedRoute>
                <AlgorithmEditor />
              </ProtectedRoute>
            }
          />
        </Routes>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
