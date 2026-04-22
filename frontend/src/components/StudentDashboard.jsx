import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    History,
    MessageSquare,
    ChevronRight,
    Calendar,
    Sparkles,
    Briefcase,
    Brain,
    Clock,
    TrendingUp,
    Target,
    Zap,
    Cpu
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
                throw new Error('Neural History Sync Interrupted');
            }

            const histData = await histRes.json();
            const chatData = await chatRes.json();

            setHistory(histData.recommendations || []);
            setChats(chatData.chats || []);
        } catch (err) {
            console.error("Nexus History Sync Failed:", err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="nexus-loader">
                <motion.div 
                    animate={{ 
                        scale: [1, 1.2, 1],
                        rotate: [0, 180, 360],
                        opacity: [0.5, 1, 0.5]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="loader-ring"
                >
                    <Cpu size={48} color="#6366f1" />
                </motion.div>
                <p>Syncing Neural History...</p>
            </div>
        );
    }

    return (
        <div className="nexus-dashboard">
            {/* --- DASHBOARD HEADER --- */}
            <motion.header 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="nexus-header"
            >
                <div className="header-content">
                    <div className="title-section">
                        <span className="badge-neon">Personal Nexus</span>
                        <h1>Neural Trajectory <span className="text-glow">Archive</span></h1>
                    </div>
                    <div className="stats-mini">
                        <div className="stat-pill">
                            <Zap size={14} className="text-cyan" />
                            <span>{history.length} Projections</span>
                        </div>
                        <div className="stat-pill">
                            <MessageSquare size={14} className="text-purple" />
                            <span>{chats.length} Coach Logs</span>
                        </div>
                    </div>
                </div>
            </motion.header>

            {/* --- CORE METRICS PANEL --- */}
            <AnimatePresence mode="wait">
                {activeTab === 'assessments' && history.length > 0 && (
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="metrics-grid"
                    >
                        <MetricCard 
                            icon={<Brain size={24} />} 
                            label="Cognitive Alignment" 
                            value={`${(history[0]?.match_score * 100).toFixed(1)}%`}
                            trend="+4.2%"
                            color="indigo"
                        />
                        <MetricCard 
                            icon={<Target size={24} />} 
                            label="Primary Target" 
                            value={history[0]?.predicted_career?.split(' ')[0]}
                            trend="High Match"
                            color="cyan"
                        />
                        <MetricCard 
                            icon={<TrendingUp size={24} />} 
                            label="Market Readiness" 
                            value="Expert Level"
                            trend="Rising"
                            color="purple"
                        />
                    </motion.div>
                )}
            </AnimatePresence>

            {/* --- NAVIGATION TABS --- */}
            <div className="nexus-tabs">
                <button 
                    className={`nexus-tab ${activeTab === 'assessments' ? 'active' : ''}`}
                    onClick={() => setActiveTab('assessments')}
                >
                    <History size={18} />
                    <span>Neural History</span>
                    {activeTab === 'assessments' && <motion.div layoutId="tab-underline" className="tab-underline" />}
                </button>
                <button 
                    className={`nexus-tab ${activeTab === 'chats' ? 'active' : ''}`}
                    onClick={() => setActiveTab('chats')}
                >
                    <MessageSquare size={18} />
                    <span>Coach Consults</span>
                    {activeTab === 'chats' && <motion.div layoutId="tab-underline" className="tab-underline" />}
                </button>
            </div>

            {/* --- MAIN CONTENT AREA --- */}
            <main className="nexus-content">
                <AnimatePresence mode="wait">
                    {activeTab === 'assessments' ? (
                        <motion.div 
                            key="assessments"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="trajectory-list"
                        >
                            {history.length === 0 ? (
                                <EmptyState icon={<Brain size={64} />} text="No neural trajectories mapped yet." />
                            ) : (
                                history.map((reg, idx) => (
                                    <TrajectoryCard 
                                        key={reg.id} 
                                        reg={reg} 
                                        idx={history.length - idx}
                                        onView={() => {
                                            const results = reg.full_json ? JSON.parse(reg.full_json) : {
                                                career_details: [{
                                                    career_title: reg.predicted_career,
                                                    match_score: reg.match_score,
                                                    description: "Legacy Neural Snapshot.",
                                                    salary_range: "Market Leading",
                                                    growth_outlook: "High"
                                                }]
                                            };
                                            onDetailView(reg, results);
                                        }}
                                    />
                                ))
                            )}
                        </motion.div>
                    ) : (
                        <motion.div 
                            key="chats"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="chat-log-list"
                        >
                            {chats.length === 0 ? (
                                <EmptyState icon={<MessageSquare size={64} />} text="No conversation logs synced." />
                            ) : (
                                <ChatLogs chats={chats} />
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
};

/* --- SUB-COMPONENTS --- */

const MetricCard = ({ icon, label, value, trend, color }) => (
    <div className={`metric-card glass-glow ${color}`}>
        <div className="metric-icon">{icon}</div>
        <div className="metric-info">
            <p className="metric-label">{label}</p>
            <h3 className="metric-value">{value}</h3>
            <span className="metric-trend">{trend}</span>
        </div>
        <div className="card-flare"></div>
    </div>
);

const TrajectoryCard = ({ reg, idx, onView }) => (
    <motion.div 
        whileHover={{ scale: 1.02, x: 5 }}
        className="trajectory-card glass-card"
    >
        <div className="card-main">
            <div className="card-icon-wrapper">
                <Briefcase size={24} />
            </div>
            <div className="card-body">
                <div className="card-header-row">
                    <h3>{reg.predicted_career}</h3>
                    <span className="idx-tag">#{idx}</span>
                </div>
                <div className="card-meta">
                    <span><Calendar size={14} /> {new Date(reg.created_at).toLocaleDateString()}</span>
                    <span className="match-tag"><Sparkles size={14} /> {(reg.match_score * 100).toFixed(0)}% Match</span>
                </div>
            </div>
        </div>
        <button className="nexus-btn-sm" onClick={onView}>
            <span>Analyze</span>
            <ChevronRight size={16} />
        </button>
    </motion.div>
);

const ChatLogs = ({ chats }) => {
    const sessions = chats.reduce((acc, chat) => {
        const sid = chat.session_id || 'Legacy Archive';
        if (!acc[sid]) acc[sid] = [];
        acc[sid].push(chat);
        return acc;
    }, {});

    return Object.entries(sessions).reverse().map(([sid, sessionChats]) => (
        <div key={sid} className="chat-session-group">
            <div className="session-divider">
                <div className="divider-line"></div>
                <span>Session: {sid.slice(0, 8)}</span>
                <div className="divider-line"></div>
            </div>
            {sessionChats.map(chat => (
                <div key={chat.id} className="chat-log-item glass-card">
                    <div className="log-time"><Clock size={12} /> {new Date(chat.created_at).toLocaleTimeString()}</div>
                    <div className="log-content">
                        <div className="user-query">
                            <label>Query</label>
                            <p>{chat.message}</p>
                        </div>
                        <div className="coach-reply">
                            <label>Response</label>
                            <p>{chat.response}</p>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    ));
};

const EmptyState = ({ icon, text }) => (
    <div className="nexus-empty">
        <div className="empty-icon">{icon}</div>
        <p>{text}</p>
        <button className="btn-vibrance sm">Initialize Analysis</button>
    </div>
);

export default StudentDashboard;

