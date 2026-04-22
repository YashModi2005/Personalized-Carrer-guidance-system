import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Assessment from './components/Assessment';
import Chat from './components/Chat';
import Dashboard from './components/Dashboard';
import AdminDashboard from './components/AdminDashboard';
import StudentDashboard from './components/StudentDashboard';
import Auth from './components/Auth';

const BACKEND_URL = 'http://localhost:8000';

const App = () => {
  const [view, setView] = useState('home'); // 'home', 'assessment', 'dashboard', 'admin'
  const [userData, setUserData] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Auth State
  const [token, setToken] = useState(sessionStorage.getItem('cp_token'));
  const [userRole, setUserRole] = useState(sessionStorage.getItem('cp_role'));

  const handleLogin = (newToken, role) => {
    setToken(newToken);
    setUserRole(role);
    sessionStorage.setItem('cp_token', newToken);
    sessionStorage.setItem('cp_role', role);
  };

  const handleLogout = () => {
    setToken(null);
    setUserRole(null);
    sessionStorage.removeItem('cp_token');
    sessionStorage.removeItem('cp_role');
    setView('home');
  };

  const apiHeaders = {
    'Authorization': `Bearer ${token}`
  };

  const handleStart = () => {
    setError(null);
    setView('assessment');
  };

  const handleComplete = (formData, apiResponse) => {
    setUserData(formData);
    setResults(apiResponse);
    setView('dashboard');
  };

  const handleReset = () => {
    setUserData(null);
    setResults(null);
    setError(null);
    setView('home');
  };

  return (
    <div className="app-wrapper">
      <div className="bg-canvas"></div>

      {token ? (
        <>
          <Navbar
            onViewChange={setView}
            currentView={view}
            userRole={userRole}
            onLogout={handleLogout}
          />

          <main className="main-content">
            {view === 'home' ? (
              <Home onStart={handleStart} />
            ) : (
              <div className={(view === 'dashboard' || view === 'admin') ? 'dashboard-wrapper' : 'vibrance-card'}>
                {view === 'assessment' && (
                  <Assessment
                    onComplete={handleComplete}
                    onBack={handleReset}
                    apiBaseUrl={BACKEND_URL}
                    apiHeaders={apiHeaders}
                  />
                )}

                {view === 'dashboard' && (
                  <Dashboard results={results} userData={userData} onReset={handleReset} />
                )}

                {view === 'admin' && (
                  <AdminDashboard apiBaseUrl={BACKEND_URL} apiHeaders={apiHeaders} />
                )}

                {view === 'history' && (
                  <StudentDashboard
                    apiBaseUrl={BACKEND_URL}
                    apiHeaders={apiHeaders}
                    onDetailView={handleComplete}
                  />
                )}
              </div>
            )}
          </main>
        </>
      ) : (
        <Auth onLogin={handleLogin} apiBaseUrl={BACKEND_URL} />
      )}

      <footer className="footer" style={{
        textAlign: 'center',
        padding: '2rem',
        color: 'var(--text-dim)',
        fontSize: '0.75rem',
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        opacity: 0.5
      }}>
        © 2026 AI Career Pilot • Autonomous Career Coach • Global Neural Engine
      </footer>
    </div>
  );
};

export default App;
