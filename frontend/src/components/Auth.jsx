import React, { useState } from 'react';
import { Shield, User, Lock, ArrowRight, UserPlus, LogIn, Sparkles, Globe, Cpu } from 'lucide-react';
import Toast from './Toast';

const Auth = ({ onLogin, apiBaseUrl }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        role: 'student',
        secretKey: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [toast, setToast] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const endpoint = isLogin ? '/auth/login' : '/auth/signup';

        try {
            let body;
            let headers = {};

            if (isLogin) {
                body = new URLSearchParams();
                body.append('username', formData.username);
                body.append('password', formData.password);
                if (formData.role === 'counselor') {
                    body.append('secret_key', formData.secretKey);
                }
                headers['Content-Type'] = 'application/x-www-form-urlencoded';
            } else {
                const signupData = {
                    username: formData.username,
                    password: formData.password,
                    role: formData.role,
                    secret_key: formData.role === 'counselor' ? formData.secretKey : undefined
                };
                body = JSON.stringify(signupData);
                headers['Content-Type'] = 'application/json';
            }

            const res = await fetch(`${apiBaseUrl}${endpoint}`, {
                method: 'POST',
                headers,
                body
            });

            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || 'Authentication failed');

            if (isLogin) {
                onLogin(data.access_token, data.role);
            } else {
                setToast({ message: "Account created! Please log in.", type: 'success' });
                setIsLogin(true);
            }
        } catch (err) {
            setToast({ message: err.message, type: 'error' });
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page-wrapper">
            <div className="auth-side-branding">
                <div className="branding-content">
                    <div className="branding-logo">
                        <Cpu size={40} color="white" />
                    </div>
                    <h1 className="branding-title">
                        Navigate Your <br /> 
                        <span style={{ color: '#60a5fa' }}>Future Self</span>
                    </h1>
                    <p className="branding-subtitle">
                        Experience the world's most advanced autonomous career guidance engine. 
                        Powered by neural intelligence, designed for your unique trajectory.
                    </p>
                    
                    <div style={{ marginTop: '4rem', display: 'flex', gap: '2rem', justifyContent: 'center', opacity: 0.6 }}>
                        <div style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>98%</div>
                            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase' }}>Precision</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>15k+</div>
                            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase' }}>Trajectories</div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '1.5rem', fontWeight: '800' }}>24/7</div>
                            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase' }}>Neural Sync</div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="auth-side-form">
                <div className="premium-glass-card">
                    <div style={{ marginBottom: '2.5rem' }}>
                        <h2 className="gradient-text" style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                            {isLogin ? 'Welcome Back' : 'Get Started'}
                        </h2>
                        <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>
                            {isLogin ? 'Enter your credentials to access the engine' : 'Create your neural profile to begin your journey'}
                        </p>
                    </div>

                    <div className="auth-mode-toggle">
                        <button 
                            className={`mode-btn ${isLogin ? 'active' : ''}`}
                            onClick={() => setIsLogin(true)}
                        >
                            Sign In
                        </button>
                        <button 
                            className={`mode-btn ${!isLogin ? 'active' : ''}`}
                            onClick={() => setIsLogin(false)}
                        >
                            Create Account
                        </button>
                    </div>

                    <form onSubmit={handleSubmit}>
                        <div className="input-premium-group">
                            <input
                                className="input-premium"
                                type="text"
                                required
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                placeholder="Username"
                            />
                            <div className="input-icon">
                                <User size={18} />
                            </div>
                        </div>

                        <div className="input-premium-group">
                            <input
                                className="input-premium"
                                type="password"
                                required
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                placeholder="Password"
                            />
                            <div className="input-icon">
                                <Lock size={18} />
                            </div>
                        </div>

                        <div className="input-premium-group">
                            <select
                                className="input-premium"
                                value={formData.role}
                                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                                style={{ appearance: 'none' }}
                            >
                                <option value="student">User Account</option>
                                <option value="counselor">Admin</option>
                            </select>
                            <div className="input-icon">
                                <Shield size={18} />
                            </div>
                        </div>

                        {formData.role === 'counselor' && (
                            <div className="input-premium-group animate-fade-in" style={{ marginTop: '1rem' }}>
                                <input
                                    className="input-premium"
                                    type="password"
                                    required
                                    value={formData.secretKey}
                                    onChange={(e) => setFormData({ ...formData, secretKey: e.target.value })}
                                    placeholder="Enter Admin Secret Key"
                                />
                                <div className="input-icon">
                                    <Sparkles size={18} color="#60a5fa" />
                                </div>
                            </div>
                        )}

                        <button 
                            className="btn-vibrance" 
                            style={{ width: '100%', marginTop: '1.5rem', justifyContent: 'center' }} 
                            disabled={loading}
                        >
                            {loading ? 'Synchronizing...' : (
                                <>
                                    {isLogin ? 'Authorize Access' : 'Initialize Profile'}
                                    <ArrowRight size={18} />
                                </>
                            )}
                        </button>
                    </form>

                    <div style={{ marginTop: '2.5rem', textAlign: 'center' }}>
                        <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
                            Secure environment. AES-256 Neural Encryption active.
                        </p>
                    </div>
                </div>
            </div>

            {toast && (
                <Toast
                    message={toast.message}
                    type={toast.type}
                    onClose={() => setToast(null)}
                />
            )}
        </div>
    );
};

export default Auth;
