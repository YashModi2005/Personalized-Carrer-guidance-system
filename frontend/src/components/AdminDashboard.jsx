import React, { useState, useEffect } from 'react';
import {
    Users,
    Database,
    Activity,
    FileText,
    Upload,
    TrendingUp,
    Search,
    Eye,
    X,
    ChevronRight,
    CheckCircle2,
    AlertCircle,
    History
} from 'lucide-react';
import Toast from './Toast';

export default function AdminDashboard({ apiBaseUrl, apiHeaders }) {
    const [activeTab, setActiveTab] = useState('students');
    const [registrations, setRegistrations] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [toast, setToast] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [uploadStatus, setUploadStatus] = useState(null);
    const [selectedDossier, setSelectedDossier] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [regRes, statsRes] = await Promise.all([
                fetch(`${apiBaseUrl}/admin/recommendations`, { headers: apiHeaders }),
                fetch(`${apiBaseUrl}/admin/stats`, { headers: apiHeaders })
            ]);

            if (!regRes.ok || !statsRes.ok) {
                const errorData = await regRes.json();
                throw new Error(errorData.detail || 'Neural Sync Failed');
            }

            const regData = await regRes.json();
            const statsData = await statsRes.json();

            setRegistrations(regData?.recommendations || []);
            setStats(statsData);
        } catch (err) {
            console.error("Dashboard Sync Failed:", err);
            setToast({ type: 'error', message: `Sync Interrupted: ${err.message}` });
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setUploadStatus({ type: 'loading', message: 'Uploading vectorizing assets...' });

        try {
            const res = await fetch(`${apiBaseUrl}/admin/upload-dataset`, {
                method: 'POST',
                headers: apiHeaders,
                body: formData
            });
            const data = await res.json();
            setToast({ type: 'success', message: data.message });
        } catch (err) {
            setToast({ type: 'error', message: 'Nexus Sync Interrupted.' });
        }
    };

    const filteredRegistrations = (registrations || []).filter(r =>
        (r?.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
        (r?.predicted_career || "").toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <div className="progress-ring"></div>
            </div>
        );
    }

    return (
        <div className="admin-layout anim-slide-up">
            {/* Sidebar */}
            <aside className="admin-sidebar">
                <div style={{ marginBottom: '2.5rem' }}>
                    <h3 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#1e3a5f', marginBottom: '0.25rem', letterSpacing: '-0.02em' }}>NeuroControl</h3>
                    <p style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.15em', fontWeight: 700, opacity: 0.8 }}>Counselor Nexus v2.0</p>
                </div>

                <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <TabButton
                        active={activeTab === 'students'}
                        onClick={() => setActiveTab('students')}
                        icon={<Users size={20} />}
                        label="Student Database"
                    />
                    <TabButton
                        active={activeTab === 'analytics'}
                        onClick={() => setActiveTab('analytics')}
                        icon={<Activity size={20} />}
                        label="Neural Analytics"
                    />
                    {/* Temporarily hidden: Dossier Payloads */}
                    {/* <TabButton
                        active={activeTab === 'datasets'}
                        onClick={() => setActiveTab('datasets')}
                        icon={<Database size={20} />}
                        label="Dossier Payloads"
                    /> */}
                    <TabButton
                        active={activeTab === 'inventory'}
                        onClick={() => setActiveTab('inventory')}
                        icon={<History size={20} />}
                        label="Dossier Inventory"
                    />
                </nav>

                <div className="section-divider"></div>

                <div style={{ padding: '0 0.5rem', marginTop: 'auto' }}>
                    <div className="admin-status-node">
                        <span style={{ fontSize: '0.65rem', color: '#1e3a5f', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.15em', opacity: 0.6 }}>System Health</span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <div className="pulse-green" style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%' }}></div>
                            <span style={{ fontSize: '0.85rem', fontWeight: 800, color: '#1e3a5f' }}>OPERATIONAL</span>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Area */}
            <main className="admin-main">
                {activeTab === 'students' && (
                    <div className="admin-card">
                        <div className="admin-card-header">
                            <div>
                                <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.25rem' }}>Voyager Records</h2>
                                <p style={{ color: 'var(--text-muted)' }}>Telemetry from active career assessments</p>
                            </div>
                            <div className="admin-search-wrapper">
                                <Search className="admin-search-icon" size={20} />
                                <input
                                    className="input-vibrance admin-search-input"
                                    placeholder="Locate student or trajectory..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                            </div>
                        </div>

                        <div style={{ overflowX: 'auto' }}>
                            <table className="admin-table">
                                <thead>
                                    <tr>
                                        <th>Voyager Identity</th>
                                        <th>Target Trajectory</th>
                                        <th>Neural Affinity</th>
                                        <th>Sync Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredRegistrations.map((reg) => (
                                        <tr key={reg.id} className="admin-table-row">
                                            <td>
                                                <div style={{ fontWeight: 800, fontSize: '1.1rem' }}>{reg.name}</div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>{reg.academic_percentage}% Proficiency</div>
                                            </td>
                                            <td>
                                                <span className="badge-neural" style={{ margin: 0, padding: '0.4rem 1rem' }}>{reg.predicted_career}</span>
                                            </td>
                                            <td>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                                    <div className="resonance-bar-bg" style={{ width: '80px' }}>
                                                        <div className="resonance-bar-fill" style={{ width: `${reg.match_score * 100}%` }}></div>
                                                    </div>
                                                    <span style={{ fontWeight: 900, color: 'var(--primary-light)' }}>{(reg.match_score * 100).toFixed(0)}%</span>
                                                </div>
                                            </td>
                                            <td style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{new Date(reg.created_at).toLocaleDateString()}</td>
                                            <td>
                                                <button
                                                    className="btn-outline"
                                                    style={{ padding: '0.6rem', borderRadius: '12px', border: '1px solid var(--glass-border)' }}
                                                    onClick={() => setSelectedDossier(reg)}
                                                >
                                                    <Eye size={18} color="var(--primary-light)" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {activeTab === 'analytics' && stats && (
                    <div className="admin-stat-grid">
                        <div className="admin-stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                                <div className="profile-badge">
                                    <TrendingUp color="var(--primary-light)" size={24} />
                                </div>
                                <h3 style={{ fontSize: '1.5rem', fontWeight: 800 }}>Trajectory Density</h3>
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxHeight: '420px', overflowY: 'auto', paddingRight: '0.5rem' }} className="custom-scrollbar">
                                {stats.top_career_trends.map((item, i) => (
                                    <div key={i} className="resonance-item">
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
                                            <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>{item.career}</span>
                                            <span style={{ color: 'var(--primary-light)', fontWeight: 800 }}>{item.count} Sessions</span>
                                        </div>
                                        <div className="resonance-bar-bg">
                                            <div className="resonance-bar-fill" style={{ width: `${(item.count / stats.total_sessions) * 100}%` }}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="admin-stat-card">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                                <div className="profile-badge" style={{ background: 'rgba(14, 165, 233, 0.1)', borderColor: 'rgba(14, 165, 233, 0.2)' }}>
                                    <Activity color="var(--secondary)" size={24} />
                                </div>
                                <h3 style={{ fontSize: '1.5rem', fontWeight: 800 }}>Engine Efficacy</h3>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem 0 2rem' }}>
                                <div style={{ fontSize: '4.5rem', fontWeight: 900 }} className="gradient-text">{stats.average_match_score}%</div>
                                <p style={{ color: 'var(--text-muted)', letterSpacing: '0.2em', textTransform: 'uppercase', fontSize: '0.75rem' }}>Neural Confidence Mean</p>
                            </div>
                            <div className="section-divider"></div>
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <div>
                                    <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>Total Sessions</p>
                                    <p style={{ fontSize: '1.75rem', fontWeight: 900 }}>{stats.total_sessions}</p>
                                </div>
                                <div>
                                    <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>Unique Voyagers</p>
                                    <p style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--primary-light)' }}>{stats.total_users}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'inventory' && (
                    <div className="admin-card">
                        <div className="admin-card-header" style={{ marginBottom: '2.5rem' }}>
                            <div>
                                <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.25rem' }}>Dossier Inventory</h2>
                                <p style={{ color: 'var(--text-muted)' }}>Aggregate telemetry archives by unique voyager identity</p>
                            </div>
                        </div>

                        <div style={{ overflowX: 'auto' }}>
                            <table className="admin-table">
                                <thead>
                                    <tr>
                                        <th>Voyager Identity</th>
                                        <th>Assessment Volume</th>
                                        <th>Last Archive Date</th>
                                        <th>Neural Link</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.values(registrations.reduce((acc, reg) => {
                                        const key = `${reg.name}_${reg.user_id || 'GUEST'}`;
                                        if (!acc[key]) {
                                            acc[key] = reg;
                                        }
                                        return acc;
                                    }, {})).map((user) => (
                                        <tr key={user.id} className="admin-table-row">
                                            <td>
                                                <div style={{ fontWeight: 800, fontSize: '1.1rem' }}>{user.name}</div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>ID: {user.user_id || 'GUEST_VECT'}</div>
                                            </td>
                                            <td>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                                    <div style={{
                                                        padding: '0.4rem 1rem',
                                                        background: 'rgba(124, 58, 237, 0.2)',
                                                        color: 'var(--primary-light)',
                                                        borderRadius: '8px',
                                                        fontWeight: 900,
                                                        fontSize: '1rem'
                                                    }}>
                                                        {user.assessment_count}
                                                    </div>
                                                    <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }}>SESSIONS</span>
                                                </div>
                                            </td>
                                            <td style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>
                                                {new Date(user.created_at).toLocaleDateString()}
                                            </td>
                                            <td>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#10b981', fontSize: '0.8rem', fontWeight: 800 }}>
                                                    <div className="pulse-green" style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%' }}></div>
                                                    SYNCED
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )
                }
            </main >
            {toast && (
                <Toast
                    message={toast.message}
                    type={toast.type}
                    onClose={() => setToast(null)}
                />
            )}

            {
                selectedDossier && (
                    <DossierModal
                        data={selectedDossier}
                        onClose={() => setSelectedDossier(null)}
                    />
                )
            }
        </div >
    );
}

const TabButton = ({ active, onClick, icon, label }) => (
    <button
        onClick={onClick}
        className={`admin-nav-item ${active ? 'active' : ''}`}
        style={{ width: '100%', border: 'none' }}
    >
        {icon}
        <span style={{ fontSize: '1rem' }}>{label}</span>
        {active && <ChevronRight size={16} style={{ marginLeft: 'auto', color: 'white' }} />}
    </button>
);

function DossierModal({ data, onClose }) {
    if (!data) return null;

    return (
        <div className="modal-overlay anim-fade-in" onClick={onClose} style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(30, 58, 95, 0.7)',
            backdropFilter: 'blur(8px)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem'
        }}>
            <div className="custom-scrollbar" onClick={e => e.stopPropagation()} style={{
                maxWidth: '800px',
                width: '95%',
                maxHeight: '90vh',
                overflowY: 'auto',
                position: 'relative',
                border: '1px solid rgba(30,58,95,0.1)',
                background: 'white',
                padding: '3rem',
                borderRadius: '24px',
                boxShadow: '0 25px 50px -12px rgba(30,58,95,0.25)',
                zIndex: 1001
            }}>
                <button
                    onClick={onClose}
                    style={{
                        position: 'absolute',
                        top: '1.5rem',
                        right: '1.5rem',
                        background: 'rgba(30,58,95,0.05)',
                        border: '1px solid rgba(30,58,95,0.1)',
                        borderRadius: '50%',
                        padding: '0.5rem',
                        cursor: 'pointer',
                        color: '#1e3a5f',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    <X size={20} />
                </button>

                <div style={{ marginBottom: '3rem' }}>
                    <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Voyager Dossier</h2>
                    <p style={{ color: '#64748b', letterSpacing: '0.1em', textTransform: 'uppercase', fontSize: '0.8rem', fontWeight: 600 }}>Telemetry Archive for {data.name}</p>
                </div>

                <div className="admin-stat-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '3rem', width: '100%' }}>
                    <div className="vibrance-card" style={{ padding: '1.5rem', background: '#f8fafc' }}>
                        <p style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.05em', fontWeight: 700 }}>Predicted Career</p>
                        <p style={{ fontSize: '1.4rem', fontWeight: 800, color: '#1e3a5f' }}>{data.predicted_career || 'Unknown'}</p>
                    </div>
                    <div className="vibrance-card" style={{ padding: '1.5rem', background: '#f8fafc' }}>
                        <p style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.05em', fontWeight: 700 }}>Neural Affinity</p>
                        <p style={{ fontSize: '1.4rem', fontWeight: 800, color: '#2563eb' }}>{data.match_score ? (data.match_score * 100).toFixed(1) : '0.0'}%</p>
                    </div>
                    <div className="vibrance-card" style={{ padding: '1.5rem', background: '#f8fafc' }}>
                        <p style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', marginBottom: '0.75rem', letterSpacing: '0.05em', fontWeight: 700 }}>Academic Vector</p>
                        <p style={{ fontSize: '1.4rem', fontWeight: 800, color: '#1e3a5f' }}>{data.academic_percentage || '0'}%</p>
                    </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
                    <DossierSection title="Neural Interests" content={data.interests} color="var(--primary-light)" />
                    <DossierSection title="Technical Capabilities" content={data.tech_skills} color="var(--secondary)" />
                    <DossierSection title="Cognitive Soft Skills" content={data.soft_skills} color="var(--accent)" />
                    <DossierSection title="Extracurricular Trajectory" content={data.extracurriculars} color="var(--aurora-1)" />
                </div>

                <div className="section-divider" style={{ margin: '4rem 0 2rem' }}></div>

                <div style={{ textAlign: 'right' }}>
                    <button className="btn-vibrance" onClick={onClose} style={{ padding: '1rem 2.5rem', borderRadius: '14px' }}>Close Dossier</button>
                </div>
            </div>
        </div>
    );
};

function DossierSection({ title, content, color }) {
    return (
        <div className="anim-fade-in" style={{ animationDelay: '0.2s' }}>
            <h4 style={{ color: color, fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.2em', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem', fontWeight: 800 }}>
                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: color, boxShadow: `0 0 10px ${color}` }}></div>
                {title}
            </h4>
            <div className="vibrance-card" style={{ background: '#f8fafc', border: '1px solid rgba(30,58,95,0.08)', padding: '1.5rem', borderRadius: '18px' }}>
                <p style={{ lineHeight: 1.7, color: '#1e3a5f', fontWeight: 500, opacity: 0.9, fontSize: '1rem' }}>{content || 'No telemetry recorded for this vector.'}</p>
            </div>
        </div>
    );
}

