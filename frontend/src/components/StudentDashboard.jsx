import React, { useState, useEffect } from 'react';
import {
    History,
    MessageSquare,
    ChevronRight,
    Calendar,
    Sparkles,
    Briefcase,
    Brain,
    Clock
} from 'lucide-react';

const StudentDashboard = ({ apiBaseUrl, apiHeaders, onDetailView }) => {
    const [history, setHistory] = useState([]);
    const [chats, setChats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('assessments');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const [histRes, chatRes] = await Promise.all([
                fetch(`${apiBaseUrl}/student/history`, { headers: apiHeaders }),
                fetch(`${apiBaseUrl}/student/chats`, { headers: apiHeaders })
            ]);

            if (!histRes.ok || !chatRes.ok) {
                const errorData = await histRes.json();
                throw new Error(errorData.detail || 'Neural History Sync Interrupted');
            }

            const histData = await histRes.json();
            const chatData = await chatRes.json();

            setHistory(histData.recommendations || []);
            setChats(chatData.chats || []);
        } catch (err) {
            console.error("Nexus History Sync Failed:", err);
            // Optionally set an error state here if needed
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <div className="progress-ring"></div>
            </div>
        );
    }

    return (
        <div className="student-dashboard" style={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
            <header style={{ marginBottom: '2.5rem', textAlign: 'center', position: 'relative' }}>
                <h1 className="gradient-text" style={{ fontSize: '3.2rem', fontWeight: 900, marginBottom: '0.5rem', letterSpacing: '-0.03em' }}>Personal Journey</h1>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
                    <div className="pulse-dot" style={{ width: 8, height: 8, borderRadius: '50%', background: '#10b981', boxShadow: '0 0 12px #10b981' }}></div>
                    <p style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.15em', margin: 0 }}>
                        NEURAL TRAJECTORY ARCHIVE • {history.length} SYNCED SESSIONS
                    </p>
                </div>
            </header>

            {/* NEURAL GROWTH PANEL - DYNAMIC STATS */}
            {activeTab === 'assessments' && history.length > 0 && (
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                    gap: '1.25rem', 
                    marginBottom: '3rem',
                    animation: 'fadeUp 0.6s ease'
                }}>
                    <div style={growthMetricStyle}>
                        <div style={metricIconStyle('#2563eb')}><Brain size={20} /></div>
                        <div>
                            <p style={metricLabelStyle}>Neural Fidelity</p>
                            <h4 style={metricValueStyle}>{(history[0]?.match_score * 100).toFixed(1)}%</h4>
                        </div>
                    </div>
                    <div style={growthMetricStyle}>
                        <div style={metricIconStyle('#7c3aed')}><History size={20} /></div>
                        <div>
                            <p style={metricLabelStyle}>Career Velocity</p>
                            <h4 style={metricValueStyle}>High Match</h4>
                        </div>
                    </div>
                    <div style={growthMetricStyle}>
                        <div style={metricIconStyle('#0d9488')}><Sparkles size={20} /></div>
                        <div>
                            <p style={metricLabelStyle}>Trajectory Hub</p>
                            <h4 style={metricValueStyle}>{history[0]?.predicted_career?.split(' ')[0]}</h4>
                        </div>
                    </div>
                </div>
            )}

            <div className="tab-switcher" style={{
                display: 'flex',
                gap: '0.4rem',
                marginBottom: '2.5rem',
                justifyContent: 'center',
                background: 'rgba(255,255,255,0.88)',
                border: '1px solid rgba(30,58,95,0.09)',
                padding: '0.4rem',
                borderRadius: '16px',
                width: 'fit-content',
                margin: '0 auto 2.5rem',
                boxShadow: '0 2px 10px rgba(30,58,95,0.06)'
            }}>
                <button
                    onClick={() => setActiveTab('assessments')}
                    className={`nav-btn ${activeTab === 'assessments' ? 'active' : ''}`}
                    style={activeTab === 'assessments' ? activeTabStyle : inactiveTabStyle}
                >
                    <History size={18} />
                    <span>Assessments ({history.length})</span>
                </button>
                <button
                    onClick={() => setActiveTab('chats')}
                    className={`nav-btn ${activeTab === 'chats' ? 'active' : ''}`}
                    style={activeTab === 'chats' ? activeTabStyle : inactiveTabStyle}
                >
                    <MessageSquare size={18} />
                    <span>Coach Logs</span>
                </button>
            </div>

            <main className="history-content">
                {activeTab === 'assessments' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        {history.length === 0 ? (
                            <div style={emptyStateStyle}>
                                <Brain size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
                                <p>No trajectories mapped yet. Launch your first analysis to begin.</p>
                            </div>
                        ) : (
                            <div style={{ position: 'relative', paddingLeft: '40px' }}>
                                {/* VERTICAL TIMELINE CONNECTOR */}
                                <div style={{ 
                                    position: 'absolute', 
                                    left: '18px', 
                                    top: '20px', 
                                    bottom: '20px', 
                                    width: '2px', 
                                    background: 'linear-gradient(to bottom, #2563eb, rgba(37,99,235,0.05))',
                                    zIndex: 0
                                }}></div>

                                {history.map((reg, idx) => (
                                    <div key={reg.id} style={{ position: 'relative', marginBottom: '2rem' }}>
                                        {/* TIMELINE NODE */}
                                        <div style={{ 
                                            position: 'absolute', 
                                            left: '-26px', 
                                            top: '24px', 
                                            width: '10px', 
                                            height: '10px', 
                                            borderRadius: '50%', 
                                            background: idx === 0 ? '#2563eb' : '#cbd5e1', 
                                            border: '3px solid white',
                                            boxShadow: idx === 0 ? '0 0 10px rgba(37,99,235,0.4)' : 'none',
                                            zIndex: 1 
                                        }}></div>

                                        <div className="vibrance-card history-card" style={cardStyle}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                                                    <div style={iconBoxStyle}>
                                                        <Briefcase className="text-primary" size={24} />
                                                    </div>
                                                    <div>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                                            <h3 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 800, color: '#0f172a' }}>{reg.predicted_career}</h3>
                                                            <span style={{ fontSize: '0.65rem', fontWeight: 800, background: 'rgba(30,58,95,0.05)', color: '#475569', padding: '2px 8px', borderRadius: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                                                ENTRY #{history.length - idx}
                                                            </span>
                                                        </div>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.25rem', color: '#64748b', fontSize: '0.85rem', fontWeight: 600 }}>
                                                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                                                                <Calendar size={14} /> {new Date(reg.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                                                            </span>
                                                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#2563eb' }}>
                                                                <Sparkles size={14} /> {(reg.match_score * 100).toFixed(0)}% Match
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                                <button
                                                    className="btn-outline"
                                                    style={{ 
                                                        padding: '0.6rem 1.2rem', 
                                                        borderRadius: '12px', 
                                                        background: 'white', 
                                                        border: '1px solid #e2e8f0',
                                                        fontWeight: 700,
                                                        fontSize: '0.85rem'
                                                    }}
                                                    onClick={() => {
                                                        if (reg.full_json) {
                                                            try {
                                                                const results = JSON.parse(reg.full_json);
                                                                const userData = {
                                                                    name: reg.name,
                                                                    academic_percentage: reg.academic_percentage,
                                                                    interests: reg.interests,
                                                                    tech_skills: reg.tech_skills,
                                                                    soft_skills: reg.soft_skills,
                                                                    extracurriculars: reg.extracurriculars
                                                                };
                                                                onDetailView(userData, results);
                                                            } catch (e) {
                                                                console.error("Neural Decode Failed:", e);
                                                            }
                                                        } else {
                                                            const partialResults = {
                                                                career_details: [{
                                                                    career_title: reg.predicted_career,
                                                                    match_score: reg.match_score,
                                                                    description: "Legacy Data Snapshot: This trajectory was mapped before the Deep Persistence upgrade. Detailed neural insights are generated from existing telemetry.",
                                                                    salary_range: "$85k - $160k",
                                                                    growth_outlook: "Stable Growth",
                                                                    entry_difficulty: "Strategic Access",
                                                                    work_life_balance: "High Flexibility",
                                                                    top_employers: ["Fortune 500 Companies", "Dynamic Startups"],
                                                                    tech_stack: ["Analytical Tools", "Industry Platforms"]
                                                                }]
                                                            };
                                                            const userData = {
                                                                name: reg.name,
                                                                academic_percentage: reg.academic_percentage,
                                                                interests: reg.interests,
                                                                tech_skills: reg.tech_skills,
                                                                soft_skills: reg.soft_skills,
                                                                extracurriculars: reg.extracurriculars
                                                            };
                                                            onDetailView(userData, partialResults);
                                                        }
                                                    }}
                                                >
                                                    <span>View Details</span>
                                                    <ChevronRight size={16} />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'chats' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
                        {chats.length === 0 ? (
                            <div style={emptyStateStyle}>
                                <MessageSquare size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
                                <p>No conversation logs found. Consult your Neural Coach to start a dialogue.</p>
                            </div>
                        ) : (
                            Object.entries(
                                chats.reduce((acc, chat) => {
                                    const sid = chat.session_id || 'Legacy Archive';
                                    if (!acc[sid]) acc[sid] = [];
                                    acc[sid].push(chat);
                                    return acc;
                                }, {})
                            ).reverse().map(([sessionId, sessionChats]) => (
                                <div key={sessionId} style={{ position: 'relative' }}>
                                    <div style={{ 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        gap: '0.75rem', 
                                        marginBottom: '1rem',
                                        paddingLeft: '0.5rem'
                                    }}>
                                        <div style={{ width: 8, height: 8, borderRadius: '50%', background: sessionId === 'Legacy Archive' ? '#94a3b8' : '#2563eb' }}></div>
                                        <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
                                            {sessionId === 'Legacy Archive' ? 'Legacy Data Stream' : `Neural Session: ${sessionId.slice(0, 12)}...`}
                                        </span>
                                        <span style={{ fontSize: '0.65rem', color: '#94a3b8' }}>• {sessionChats.length} Messages</span>
                                    </div>
                                    
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                        {sessionChats.map((chat) => (
                                            <div key={chat.id} className="vibrance-card chat-log-card" style={cardStyle}>
                                                <div style={{ display: 'flex', gap: '1.25rem' }}>
                                                    <div style={chatIconStyle}>
                                                        <Clock size={16} />
                                                    </div>
                                                    <div style={{ flex: 1 }}>
                                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                                                            <span style={{ fontSize: '0.65rem', color: '#94a3b8', fontWeight: 600 }}>
                                                                {new Date(chat.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                            </span>
                                                        </div>
                                                        <div style={{ marginBottom: '1rem' }}>
                                                            <p style={{ color: '#94a3b8', fontSize: '0.7rem', marginBottom: '0.25rem', fontWeight: 800 }}>USER INPUT</p>
                                                            <p style={{ margin: 0, fontSize: '0.9rem', color: '#1e293b' }}>{chat.message}</p>
                                                        </div>
                                                        <div style={{ paddingLeft: '1rem', borderLeft: '2px solid #e2e8f0' }}>
                                                            <p style={{ color: '#2563eb', fontSize: '0.7rem', marginBottom: '0.25rem', fontWeight: 800 }}>NEURAL RESPONSE</p>
                                                            <p style={{ margin: 0, fontSize: '0.9rem', color: '#334155' }}>{chat.response.length > 200 ? chat.response.substring(0, 200) + "..." : chat.response}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </main>
        </div>
    );
};

const activeTabStyle = {
    background: '#1e3a5f',
    border: '1px solid #1e3a5f',
    color: 'white',
    padding: '0.65rem 1.25rem',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    cursor: 'pointer',
    fontWeight: 700,
    fontSize: '0.875rem',
    boxShadow: '0 4px 16px rgba(30,58,95,0.3)',
    transition: 'all 0.2s ease'
};

const inactiveTabStyle = {
    background: 'transparent',
    border: '1px solid transparent',
    color: '#475569',
    padding: '0.65rem 1.25rem',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    cursor: 'pointer',
    fontWeight: 500,
    fontSize: '0.875rem',
    transition: 'all 0.2s ease'
};

const cardStyle = {
    padding: '1.5rem 2rem',
    borderRadius: '20px',
    background: 'white',
    border: '1px solid #e2e8f0',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 4px 12px rgba(30,58,95,0.04)',
    cursor: 'default'
};

const growthMetricStyle = {
    background: 'white',
    padding: '1.5rem',
    borderRadius: '20px',
    border: '1px solid #e2e8f0',
    display: 'flex',
    alignItems: 'center',
    gap: '1.25rem',
    boxShadow: '0 4px 20px rgba(30,58,95,0.05)'
};

const metricIconStyle = (color) => ({
    width: '48px',
    height: '48px',
    borderRadius: '14px',
    background: `${color}10`,
    color: color,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0
});

const metricLabelStyle = {
    margin: 0,
    fontSize: '0.7rem',
    fontWeight: 800,
    color: '#94a3b8',
    textTransform: 'uppercase',
    letterSpacing: '0.05em'
};

const metricValueStyle = {
    margin: 0,
    fontSize: '1.2rem',
    fontWeight: 900,
    color: '#0f172a'
};

const iconBoxStyle = {
    width: '56px',
    height: '56px',
    borderRadius: '14px',
    background: 'rgba(37,99,235,0.08)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    border: '1px solid rgba(37,99,235,0.15)'
};

const chatIconStyle = {
    color: 'var(--primary-light)',
    marginTop: '0.25rem'
};

const emptyStateStyle = {
    textAlign: 'center',
    padding: '5rem 2rem',
    color: '#94a3b8',
    background: 'rgba(248,250,252,0.8)',
    borderRadius: '24px',
    border: '1px dashed rgba(30,58,95,0.18)'
};

export default StudentDashboard;
