import React from 'react';
import { Compass, LayoutDashboard, ClipboardList, History, Shield, LogOut } from 'lucide-react';

const Navbar = ({ onViewChange, currentView, userRole, onLogout }) => {

    const navItems = [
        { key: 'home', label: 'Home', icon: LayoutDashboard, show: true },
        { key: 'assessment', label: 'Career Assessment', icon: ClipboardList, show: true },
        { key: 'admin', label: 'Admin Panel', icon: Shield, show: userRole === 'counselor' },
        { key: 'history', label: 'My Journey', icon: History, show: userRole === 'student' },
    ].filter(item => item.show);

    return (
        <nav className="nav-glass">
            {/* ── Logo ── */}
            <div className="nav-logo-section" onClick={() => onViewChange('home')}>
                <div className="nav-logo-icon">
                    <Compass size={22} color="white" />
                </div>
                <div className="nav-logo-text-group">
                    <h2 className="nav-logo-title">
                        Career<span style={{ color: 'var(--primary-light)' }}>Pilot</span>
                    </h2>
                    <span className="nav-logo-subtitle">
                        {userRole ? `${userRole} · AI Engine` : 'AI Career Engine'}
                    </span>
                </div>
            </div>

            {/* ── Nav Links ── */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div className="nav-links-container">
                    {navItems.map(({ key, label, icon: Icon }) => (
                        <button
                            key={key}
                            onClick={() => onViewChange(key)}
                            className={`nav-link-item ${currentView === key ? 'active' : ''}`}
                        >
                            <Icon size={16} />
                            {label}
                        </button>
                    ))}
                </div>

                <div className="nav-divider" />

                <button className="nav-logout-btn" onClick={onLogout}>
                    <LogOut size={16} />
                    Logout
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
