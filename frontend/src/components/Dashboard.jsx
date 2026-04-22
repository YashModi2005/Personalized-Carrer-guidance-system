import React, { useState, useEffect, useRef } from 'react';
import Chat from './Chat';
import {
    Trophy, TrendingUp, AlertCircle, Activity, Award,
    Briefcase, MessageSquare, Sparkles, DollarSign,
    Building2, Zap, Target, RefreshCw, ChevronRight,
    Star, Clock, ArrowRight, Shield, BookOpen, Users,
    MapPin, BarChart2, CheckCircle, XCircle
} from 'lucide-react';

/* ─── tiny helpers ─────────────────────────────────────── */
const pct = (s) => `${(s * 100).toFixed(1)}%`;
const getMatchLabel = (s) => {
    if (s >= 0.93) return "Excellent Career Fit";
    if (s >= 0.85) return "Strong Potential Match";
    if (s >= 0.75) return "Steady Growth Path";
    return "Exploration Match";
};

/* ─── HighlightText ────────────────────────────────────── */
const HighlightText = ({ text, userData }) => {
    if (!text || !userData) return text;
    
    // Collect all unique keywords from skills and interests
    const skills = [
        ...(typeof userData.tech_skills === 'string' ? userData.tech_skills.split(',') : []),
        ...(typeof userData.soft_skills === 'string' ? userData.soft_skills.split(',') : []),
        ...(typeof userData.interests === 'string' ? userData.interests.split(',') : [])
    ].map(s => s.trim().toLowerCase()).filter(s => s.length > 2);

    if (skills.length === 0) return text;

    // Create a regex to match any of the keywords (case insensitive)
    const pattern = new RegExp(`(${skills.join('|')})`, 'gi');
    const parts = text.split(pattern);

    return (
        <span>
            {parts.map((part, i) => {
                // Improved matching: ignore case and extra whitespace
                const cleanPart = part.trim().toLowerCase();
                const isMatch = skills.some(s => s === cleanPart);
                return isMatch ? (
                    <strong key={i} style={{ 
                        color: '#1e40af', 
                        fontWeight: 800, 
                        background: 'rgba(37,99,235,0.12)',
                        padding: '1px 6px',
                        borderRadius: '6px',
                        display: 'inline-block',
                        margin: '0 1px'
                    }}>
                        {part}
                    </strong>
                ) : part;
            })}
        </span>
    );
};

/* ─── MatchSignals ──────────────────────────────────────── */
const MatchSignals = ({ text, userData }) => {
    if (!text || !userData) return null;
    const skills = [
        ...(typeof userData.tech_skills === 'string' ? userData.tech_skills.split(',') : []),
        ...(typeof userData.soft_skills === 'string' ? userData.soft_skills.split(',') : []),
        ...(typeof userData.interests === 'string' ? userData.interests.split(',') : [])
    ].map(s => s.trim()).filter(s => s.length > 2);

    const found = skills.filter(s => {
        const sLower = s.toLowerCase();
        const tLower = text.toLowerCase();
        // Match either the whole phrase OR individual significant words
        const words = sLower.split(' ').filter(w => w.length > 3);
        return tLower.includes(sLower) || words.some(w => tLower.includes(w));
    });

    if (found.length === 0) return null;

    return (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.45rem', marginTop: '1rem' }}>
            {found.map((s, i) => (
                <div key={i} style={{ 
                    display: 'flex', alignItems: 'center', gap: '0.3rem',
                    fontSize: '0.65rem', fontWeight: 800, 
                    color: '#0d9488', background: 'rgba(13,148,136,0.08)',
                    border: '1px solid rgba(13,148,136,0.15)',
                    borderRadius: '8px', padding: '3px 10px',
                    textTransform: 'uppercase', letterSpacing: '0.05em'
                }}>
                    <Target size={10} />
                    Input Signal: {s}
                </div>
            ))}
        </div>
    );
};

/* ─── LogicTable ────────────────────────────────────────── */
const LogicTable = ({ userData, topMatch }) => {
    if (!userData || !topMatch) return null;

    const sections = [
        { label: "Technical Skills", data: userData.tech_skills, reason: "Core Proficiency", stars: "★★★", rank: "High" },
        { label: "Professional Passions", data: userData.interests, reason: "Strategic Alignment", stars: "★★★", rank: "High" },
        { label: "Soft Skills", data: userData.soft_skills, reason: "Cultural & Team Fit", stars: "★★☆", rank: "Medium" }
    ];

    // Only show rows that have matches in the description or 'why' text
    const rows = sections.filter(s => {
        if (!s.data) return false;
        const words = s.data.split(/[ ,]+/).filter(w => w.length >= 2);
        const fullText = (topMatch.description + " " + topMatch.why_it_matches).toLowerCase();
        return words.some(w => fullText.includes(w.toLowerCase()));
    });

    if (rows.length === 0) return null;

    return (
        <div style={{ 
            marginTop: '1.5rem', 
            background: 'white', 
            border: '1px solid #e2e8f0', 
            borderRadius: '16px', 
            overflow: 'hidden',
            boxShadow: '0 4px 12px rgba(0,0,0,0.03)'
        }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                    <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0' }}>
                        <th style={{ padding: '0.85rem 1.25rem', fontSize: '0.7rem', fontWeight: 800, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.1em' }}>What You Typed</th>
                        <th style={{ padding: '0.85rem 1.25rem', fontSize: '0.7rem', fontWeight: 800, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Why It Matched</th>
                        <th style={{ padding: '0.85rem 1.25rem', fontSize: '0.7rem', fontWeight: 800, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Importance</th>
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, i) => (
                        <tr key={i} style={{ borderBottom: i === rows.length - 1 ? 'none' : '1px solid #f1f5f9' }}>
                            <td style={{ padding: '1rem 1.25rem' }}>
                                <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#1e293b' }}>{row.data}</div>
                                <div style={{ fontSize: '0.65rem', color: '#94a3b8', fontWeight: 600 }}>Source: {row.label}</div>
                            </td>
                            <td style={{ padding: '1rem 1.25rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <div style={{ width: 6, height: 6, borderRadius: '50%', background: row.rank === 'High' ? '#2563eb' : '#0d9488' }} />
                                    <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>{row.reason}</span>
                                </div>
                                <div style={{ fontSize: '0.65rem', color: '#94a3b8', paddingLeft: '0.85rem' }}>Mapping Logic: Contextual Similarity</div>
                            </td>
                            <td style={{ padding: '1rem 1.25rem' }}>
                                <div style={{ fontSize: '0.9rem', color: '#2563eb', letterSpacing: '1px', fontWeight: 800 }}>{row.stars}</div>
                                <div style={{ fontSize: '0.65rem', color: row.rank === 'High' ? '#2563eb' : '#0d9488', fontWeight: 800, textTransform: 'uppercase' }}>{row.rank}</div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};
const GaugeSVG = ({ score, size = 200 }) => {
    const r = size / 2 - 14;
    const circ = 2 * Math.PI * r;
    const [dash, setDash] = useState(circ);
    useEffect(() => {
        const t = setTimeout(() => setDash(circ * (1 - score)), 100);
        return () => clearTimeout(t);
    }, [score, circ]);

    const color =
        score >= 0.9 ? '#2563eb' :
            score >= 0.75 ? '#0d9488' : '#7c3aed';

    return (
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
            style={{ transform: 'rotate(-90deg)' }}>
            <circle cx={size / 2} cy={size / 2} r={r}
                fill="none" stroke="rgba(30,58,95,0.08)" strokeWidth="10" />
            <circle cx={size / 2} cy={size / 2} r={r}
                fill="none" stroke={color} strokeWidth="10"
                strokeDasharray={circ}
                strokeDashoffset={dash}
                strokeLinecap="round"
                style={{
                    transition: 'stroke-dashoffset 2.2s cubic-bezier(0.4,0,0.2,1)',
                    filter: `drop-shadow(0 0 8px ${color}60)`
                }} />
        </svg>
    );
};

/* ─── ScoreBadge ────────────────────────────────────────── */
const ScoreBadge = ({ score }) => {
    const val = (score * 100).toFixed(0);
    const color = score >= 0.9 ? '#2563eb' : score >= 0.75 ? '#0d9488' : '#7c3aed';
    return (
        <span style={{
            fontFamily: 'Space Grotesk, sans-serif', fontWeight: 800,
            fontSize: '1rem', color,
            background: `${color}14`,
            border: `1px solid ${color}35`,
            borderRadius: '8px', padding: '3px 10px'
        }}>{(score * 100).toFixed(1)}%</span>
    );
};

/* ─── StatCard ──────────────────────────────────────────── */
const StatCard = ({ label, value, accent, icon: Icon, delay = 0 }) => (
    <div style={{
        background: '#ffffff',
        border: `1px solid rgba(30,58,95,0.09)`,
        borderTop: `3px solid ${accent}`,
        borderRadius: '16px',
        padding: '1.4rem 1.6rem',
        position: 'relative',
        overflow: 'hidden',
        animation: `fadeUp 0.6s ${delay}s both`,
        transition: 'transform 0.25s, box-shadow 0.25s',
        boxShadow: '0 2px 12px rgba(30,58,95,0.06)'
    }}
        onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.boxShadow = `0 16px 40px -10px ${accent}30`; }}
        onMouseLeave={e => { e.currentTarget.style.transform = ''; e.currentTarget.style.boxShadow = '0 2px 12px rgba(30,58,95,0.06)'; }}
    >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.6rem' }}>
            {Icon && <Icon size={14} style={{ color: accent }} />}
            <span style={{ fontSize: '0.65rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.18em', color: '#94a3b8' }}>{label}</span>
        </div>
        <div style={{ fontSize: '1.05rem', fontWeight: 700, color: accent, lineHeight: 1.3 }}>{value}</div>
    </div>
);

/* ─── RadarChart ────────────────────────────────────────── */
const RadarChart = ({ data, size = 300 }) => {
    if (!data) return null;
    const dimensions = ["Engineering", "Analytical", "Creative", "Strategy", "Security"];
    const count = dimensions.length;
    const center = size / 2;
    const radius = size * 0.35;

    // Calculate polygon points
    const points = dimensions.map((dim, i) => {
        const angle = (Math.PI * 2 * i) / count - Math.PI / 2;
        const value = (data[dim] || 5) / 10; // Normalized 0-1, default to 5
        return {
            x: center + radius * value * Math.cos(angle),
            y: center + radius * value * Math.sin(angle),
            labelX: center + (radius + 25) * Math.cos(angle),
            labelY: center + (radius + 20) * Math.sin(angle),
            dim
        };
    });

    const polygonPath = points.map(p => `${p.x},${p.y}`).join(' ');

    // Grid circles
    const gridLevels = [0.2, 0.4, 0.6, 0.8, 1];

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '1rem' }}>
            <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
                {/* Grid */}
                {gridLevels.map(level => (
                    <polygon
                        key={level}
                        points={dimensions.map((_, i) => {
                            const angle = (Math.PI * 2 * i) / count - Math.PI / 2;
                            return `${center + radius * level * Math.cos(angle)},${center + radius * level * Math.sin(angle)}`;
                        }).join(' ')}
                        fill="none"
                        stroke="rgba(30,58,95,0.06)"
                        strokeWidth="1"
                    />
                ))}
                {/* Spoke lines */}
                {dimensions.map((_, i) => {
                    const angle = (Math.PI * 2 * i) / count - Math.PI / 2;
                    return (
                        <line
                            key={i}
                            x1={center} y1={center}
                            x2={center + radius * Math.cos(angle)}
                            y2={center + radius * Math.sin(angle)}
                            stroke="rgba(30,58,95,0.06)"
                            strokeWidth="1"
                        />
                    );
                })}
                {/* Data Polygon */}
                <polygon
                    points={polygonPath}
                    fill="rgba(37, 99, 235, 0.15)"
                    stroke="#2563eb"
                    strokeWidth="2.5"
                    strokeLinejoin="round"
                    style={{ filter: 'drop-shadow(0 0 12px rgba(37,99,235,0.2))' }}
                />
                {/* Labels */}
                {points.map((p, i) => (
                    <text
                        key={i}
                        x={p.labelX}
                        y={p.labelY}
                        textAnchor="middle"
                        style={{
                            fontSize: '0.65rem',
                            fontWeight: 800,
                            fill: '#1e3a5f',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em'
                        }}
                    >
                        {p.dim}
                    </text>
                ))}
            </svg>
        </div>
    );
};

/* ─── ResourceCard ────────────────────────────────────────── */
const ResourceCard = ({ title, platform, url }) => {
    const iconColor = platform === 'YouTube' ? '#ef4444' : platform === 'Coursera' ? '#2563eb' : '#0d9488';
    return (
        <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="resource-card"
            style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
                padding: '1.25rem',
                background: 'white',
                border: '1px solid rgba(30,58,95,0.08)',
                borderRadius: '14px',
                textDecoration: 'none',
                transition: 'all 0.25s',
                marginBottom: '1rem'
            }}
        >
            <div style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: `${iconColor}12`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                <BookOpen size={20} style={{ color: iconColor }} />
            </div>
            <div style={{ flex: 1 }}>
                <h5 style={{ fontSize: '0.9rem', fontWeight: 800, color: '#1e3a5f', marginBottom: '0.2rem' }}>{title}</h5>
                <p style={{ fontSize: '0.75rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{platform}</p>
            </div>
            <ChevronRight size={18} style={{ color: '#94a3b8' }} />
        </a>
    );
};

/* ─── RoadmapStep ───────────────────────────────────────── */
const RoadmapStep = ({ step, idx, total }) => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: '28px' }}>
            <div style={{
                width: 28, height: 28, borderRadius: '50%',
                background: 'linear-gradient(135deg, #1e3a5f, #2563eb)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '0.7rem', fontWeight: 800, color: 'white',
                boxShadow: '0 0 10px rgba(37,99,235,0.35)',
                flexShrink: 0
            }}>{idx + 1}</div>
            {idx < total - 1 && (
                <div style={{ width: 1, flex: 1, minHeight: 20, background: 'rgba(37,99,235,0.2)', marginTop: 4 }} />
            )}
        </div>
        <div style={{ paddingBottom: idx < total - 1 ? '1rem' : 0 }}>
            <p style={{ fontSize: '0.95rem', fontWeight: 500, color: '#1e293b', lineHeight: 1.4 }}>{step}</p>
        </div>
    </div>
);

// ─── AlternativeCard ─────────────────────────────────────
const AlternativeCard = ({ rec, idx, userData }) => (
    <div style={{
        background: '#ffffff',
        border: '1px solid rgba(30,58,95,0.09)',
        borderTop: '3px solid #2563eb',
        borderRadius: '20px',
        padding: '2rem',
        animation: `fadeUp 0.5s ${0.1 * idx + 0.3}s both`,
        transition: 'transform 0.3s, box-shadow 0.3s',
        position: 'relative', overflow: 'hidden',
        boxShadow: '0 2px 12px rgba(30,58,95,0.06)'
    }}
        onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-6px)'; e.currentTarget.style.boxShadow = '0 16px 40px rgba(30,58,95,0.12)'; }}
        onMouseLeave={e => { e.currentTarget.style.transform = ''; e.currentTarget.style.boxShadow = '0 2px 12px rgba(30,58,95,0.06)'; }}
    >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
            <h4 style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.02em', lineHeight: 1.2, flex: 1, marginRight: '0.75rem', color: '#0f172a' }}>
                {rec.career_title}
            </h4>
            <ScoreBadge score={rec.match_score} />
        </div>
        <p style={{ color: '#64748b', fontSize: '0.9rem', lineHeight: 1.6, marginBottom: '1rem' }}>
            {rec.description}
        </p>
        
        {/* IMPROVED WHY MATCHES - ALTERNATIVE CARD */}
        <div style={{ 
            background: 'rgba(37,99,235,0.05)', 
            borderLeft: '3px solid #2563eb',
            borderRadius: '12px', 
            padding: '0.85rem 1rem', 
            marginBottom: '1rem'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginBottom: '0.35rem' }}>
                <Sparkles size={11} style={{ color: '#2563eb' }} />
                <span style={{ fontSize: '0.6rem', fontWeight: 900, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#1e3a5f', opacity: 0.8 }}>Why This Matches</span>
            </div>
            <p style={{ color: '#1e3a5f', fontSize: '0.82rem', fontWeight: 600, margin: 0, lineHeight: 1.5 }}>
                <HighlightText 
                    text={(rec.why_it_matches || "Aligned with your profile structure.").replace(/\s+\./g, '.').replace(/\s+/g, ' ')} 
                    userData={userData} 
                />
            </p>
        </div>

        {/* PRECISE INSIGHT TAGS - OPTION 1 Combined */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#2563eb', background: 'rgba(37,99,235,0.08)', borderRadius: '6px', padding: '2px 8px', border: '1px solid rgba(37,99,235,0.1)' }}>
                Skill-Led Fit
            </span>
            <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#0d9488', background: 'rgba(13,148,136,0.08)', borderRadius: '6px', padding: '2px 8px', border: '1px solid rgba(13,148,136,0.1)' }}>
                Passion Match
            </span>
            <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#7c3aed', background: 'rgba(124,58,237,0.08)', borderRadius: '6px', padding: '2px 8px', border: '1px solid rgba(124,58,237,0.1)' }}>
                High Growth
            </span>
        </div>

        {/* AI ANALYSIS LINE - OPTION 2 Combined */}
        <div style={{ 
            marginBottom: '1.25rem',
            padding: '0.75rem',
            background: '#f8fafc',
            borderRadius: '10px',
            border: '1px solid #e2e8f0'
        }}>
            <p style={{ fontSize: '0.75rem', color: '#475569', margin: 0, lineHeight: 1.4 }}>
                <strong style={{ color: '#1e293b' }}>AI Analysis:</strong> Matches your proficiency in <span style={{ color: '#2563eb' }}>{userData?.skills?.split(',')[0] || "core skills"}</span> and leverages your unique talents.
            </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#0d9488', background: 'rgba(13,148,136,0.08)', border: '1px solid rgba(13,148,136,0.2)', borderRadius: '8px', padding: '3px 10px' }}>
                {rec.salary_range}
            </span>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#475569', background: 'rgba(71,85,105,0.07)', border: '1px solid rgba(71,85,105,0.15)', borderRadius: '8px', padding: '3px 10px' }}>
                {rec.entry_difficulty}
            </span>
        </div>
    </div>
);

// ─── InputReflectionCard ───────────────────────────────────
const InputReflectionCard = ({ userData, topMatch }) => !userData ? null : (
    <div style={{
        background: 'linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)',
        borderRadius: '24px',
        padding: '2.5rem',
        color: 'white',
        boxShadow: '0 12px 32px rgba(30,58,95,0.25)',
        position: 'relative',
        overflow: 'hidden',
        marginBottom: '1.5rem',
        border: '1px solid rgba(255,255,255,0.1)',
        animation: 'fadeUp 0.6s 0.3s both'
    }}>
        <div style={{ position: 'absolute', right: -30, top: -30, opacity: 0.1, color: 'white' }}>
            <Sparkles size={180} />
        </div>

        <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
                <div style={{ padding: '0.5rem', background: 'rgba(255,255,255,0.15)', borderRadius: '12px', backdropFilter: 'blur(4px)' }}>
                    <Zap size={20} />
                </div>
                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, margin: 0, letterSpacing: '0.02em' }}>Your AI Career Insight</h3>
            </div>

            <p style={{ fontSize: '1.2rem', lineHeight: 1.8, fontWeight: 500, margin: 0, maxWidth: '1000px' }}>
                {(() => {
                    const highlightColor = '#22d3ee'; // Vibrant Neon Cyan
                    const highlight = {
                        color: highlightColor,
                        fontWeight: 900,
                        textShadow: `0 0 15px ${highlightColor}44`,
                        margin: '0 1px',
                        letterSpacing: '0.01em'
                    };
                    const careerStyle = {
                        color: highlightColor,
                        fontWeight: 900,
                        textTransform: 'uppercase',
                        letterSpacing: '0.06em',
                        fontSize: '1.25rem',
                        textShadow: `0 0 20px ${highlightColor}66`
                    };
                    return (
                        <>
                            "Hello <span style={highlight}>{userData.name || 'User'}</span>, our analysis has synchronized your technical expertise in <span style={highlight}>{userData.tech_skills}</span> with your exceptional <span style={highlight}>{userData.soft_skills}</span>.
                            By combining these with your deep interest in <span style={highlight}>{userData.interests}</span>
                            {userData.extracurriculars ? <> and your background in <span style={highlight}>{userData.extracurriculars}</span></> : ''},
                            your growth trajectory is uniquely optimized for the <span style={careerStyle}>{topMatch.career_title}</span> path."
                        </>
                    );
                })()}
            </p>

            <div style={{ display: 'flex', gap: '2.5rem', marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                <div>
                    <p style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.15em', opacity: 0.7, marginBottom: '0.4rem', fontWeight: 700 }}>Analysis Depth</p>
                    <p style={{ fontSize: '1rem', fontWeight: 800 }}>
                        {typeof userData.tech_skills === 'string'
                            ? userData.tech_skills.split(',').filter(s => s.trim()).length
                            : (Array.isArray(userData.tech_skills) ? userData.tech_skills.length : 0)} Proven Skills
                    </p>
                </div>
                <div>
                    <p style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.15em', opacity: 0.7, marginBottom: '0.4rem', fontWeight: 700 }}>Academic Record</p>
                    <p style={{ fontSize: '1rem', fontWeight: 800 }}>{userData.academic_percentage}% Proficiency</p>
                </div>
                <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.5rem', opacity: 0.8 }}>
                    <Target size={14} />
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Neural Sync Active</span>
                </div>
            </div>
        </div>
    </div>
);

/* ════════════════════════════════════════════════════════════
   MAIN DASHBOARD
═══════════════════════════════════════════════════════════ */
const Dashboard = ({ results, userData, onReset }) => {
    const [showChat, setShowChat] = useState(false);
    const [activeTab, setActiveTab] = useState('overview');
    const contentRef = useRef(null);
    const chatRef = useRef(null);
    
    const switchTab = (id) => { 
        setActiveTab(id);
    };

    useEffect(() => {
        if (activeTab === 'coach' && chatRef.current) {
            chatRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }, [activeTab]);

    if (!results) return null;

    const recommendations = results.career_details || [];
    const topMatch = recommendations[0];
    const otherMatches = recommendations.slice(1);

    const isLowConfidence = topMatch && topMatch.match_score < 0.4;
    const isTrashData = !topMatch || topMatch.match_score < 0.2;

    if (isTrashData) return (
        <div style={{ 
            display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '80vh',
            animation: 'fadeUp 0.6s both'
        }}>
            <div style={{ 
                textAlign: 'center', maxWidth: '500px', padding: '3rem', 
                background: 'white', borderRadius: '32px', 
                boxShadow: '0 20px 50px -10px rgba(30,58,95,0.15)',
                border: '1px solid rgba(30,58,95,0.05)'
            }}>
                <div style={{ 
                    width: 80, height: 80, borderRadius: '24px', background: 'rgba(239, 68, 68, 0.08)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 2.5rem'
                }}>
                    <Shield size={40} style={{ color: '#ef4444' }} />
                </div>
                <h2 style={{ fontSize: '2.2rem', fontWeight: 900, marginBottom: '1rem', color: '#0f172a', letterSpacing: '-0.02em' }}>Signal Quality Too Low</h2>
                <p style={{ color: '#64748b', marginBottom: '2.5rem', lineHeight: 1.6, fontSize: '1.05rem' }}>
                    The AI Engine detected insufficient or non-standard signals in your assessment. To protect analysis integrity, we cannot generate a roadmap for this data.
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    <button onClick={onReset} className="btn-vibrance" style={{ width: '100%', padding: '1rem' }}>
                        <RefreshCw size={18} />
                        Refine My Assessment
                    </button>
                    <p style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600, marginTop: '1rem' }}>
                        TIP: Use real technical terms and descriptive interests.
                    </p>
                </div>
            </div>
        </div>
    );

    const tabs = [
        { id: 'overview', label: 'Overview', icon: Target },
        { id: 'roadmap', label: 'Roadmap', icon: MapPin },
        { id: 'alternatives', label: `Other Paths (${otherMatches.length})`, icon: BarChart2 },
        { id: 'coach', label: 'AI Coach', icon: MessageSquare },
    ];

    return (
        <div style={{ width: '100%', maxWidth: '1280px', margin: '0 auto', padding: '2rem 1.5rem 6rem' }}>
            <style>{`
                @keyframes fadeUp {
                    from { opacity: 0; transform: translateY(24px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes pulseGlow {
                    0%,100% { box-shadow: 0 0 0 0 rgba(37,99,235,0); }
                    50% { box-shadow: 0 0 0 8px rgba(37,99,235,0.10); }
                }
            `}</style>

            {/* ── LOW CONFIDENCE WARNING ─────────────────────── */}
            {isLowConfidence && (
                <div style={{
                    background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(251, 191, 36, 0.05) 100%)',
                    border: '1px solid rgba(245, 158, 11, 0.2)',
                    borderRadius: '20px',
                    padding: '1.5rem 2.5rem',
                    marginBottom: '2.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1.5rem',
                    animation: 'fadeUp 0.6s both',
                    boxShadow: '0 10px 30px -10px rgba(245, 158, 11, 0.1)'
                }}>
                    <div style={{ 
                        width: 48, height: 48, borderRadius: '14px', 
                        background: 'rgba(245, 158, 11, 0.15)', 
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        flexShrink: 0 
                    }}>
                        <Shield size={24} style={{ color: '#d97706' }} />
                    </div>
                    <div style={{ flex: 1 }}>
                        <h4 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 800, color: '#92400e' }}>Precision Alert: Inconclusive Data</h4>
                        <p style={{ margin: '0.4rem 0 0', fontSize: '0.9rem', color: '#b45309', fontWeight: 500, lineHeight: 1.5 }}>
                            The AI Engine detected non-standard input which impacted analysis depth. The roadmap below is a <strong>low-confidence projection</strong>. 
                        </p>
                    </div>
                    <button 
                        onClick={onReset}
                        className="btn-outline"
                        style={{ 
                            padding: '0.75rem 1.5rem', 
                            borderColor: 'rgba(245, 158, 11, 0.4)',
                            color: '#92400e',
                            background: 'white',
                            fontSize: '0.85rem',
                            fontWeight: 800
                        }}
                    >
                        <RefreshCw size={14} style={{ marginRight: 8 }} />
                        REFINE INPUT
                    </button>
                </div>
            )}

            {/* ── HERO ─────────────────────────────────────────── */}
            <div style={{
                background: 'transparent',
                border: '1px solid rgba(30,58,95,0.08)',
                borderTop: '3px solid #1e3a5f',
                borderRadius: '28px',
                padding: '3rem',
                marginBottom: '2rem',
                position: 'relative',
                overflow: 'hidden',
                animation: 'fadeUp 0.6s both',
                boxShadow: '0 4px 24px rgba(30,58,95,0.08)'
            }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1fr) auto', gap: '3rem', alignItems: 'center', position: 'relative', zIndex: 1 }}>
                    {/* Left col */}
                    <div>
                        {/* Status pill */}
                        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(37,99,235,0.08)', border: '1px solid rgba(37,99,235,0.2)', borderRadius: '100px', padding: '0.35rem 1rem', marginBottom: '1.25rem' }}>
                            <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#2563eb', animation: 'pulseGlow 2s infinite' }} />
                            <span style={{ fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.2em', color: '#1e3a5f' }}>
                                Primary Career Match
                            </span>
                        </div>

                        <h1 style={{
                            fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
                            fontWeight: 900,
                            letterSpacing: '-0.04em',
                            lineHeight: 1,
                            marginBottom: '1.25rem',
                            color: '#0f172a',
                        }}>
                            {topMatch.career_title}
                        </h1>

                        <p style={{ fontSize: '1.05rem', color: '#475569', lineHeight: 1.65, maxWidth: '600px', marginBottom: '1.5rem', paddingLeft: '1rem', borderLeft: '2px solid #2563eb' }}>
                            {topMatch.description}
                        </p>

                        {/* WHY THIS MATCHES - PRIMARY */}
                        <div style={{ 
                            background: 'rgba(37,99,235,0.04)', 
                            border: '1px dashed rgba(37,99,235,0.2)', 
                            borderRadius: '16px', 
                            padding: '1.25rem 1.5rem', 
                            marginBottom: '2rem',
                            maxWidth: '650px'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.5rem' }}>
                                <Sparkles size={14} style={{ color: '#2563eb' }} />
                                <span style={{ fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.12em', color: '#2563eb' }}>Why This Matches Your Profile</span>
                            </div>
                            <p style={{ color: '#1e3a5f', fontSize: '0.95rem', fontWeight: 600, margin: 0, lineHeight: 1.5 }}>
                                <HighlightText text={topMatch.why_it_matches} userData={userData} />
                            </p>
                        </div>

                        {/* OPTION 1: LOGIC TABLE */}
                        <LogicTable userData={userData} topMatch={topMatch} />

                        <div style={{ marginBottom: '2.5rem' }} />

                        {/* 3-stat row */}
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
                            <StatCard label="Est. Salary" value={topMatch.salary_range} accent="#0d9488" icon={DollarSign} delay={0.1} />
                            <StatCard label="Growth Vector" value={topMatch.growth_outlook} accent="#2563eb" icon={TrendingUp} delay={0.2} />
                            <StatCard label="Entry Level" value={topMatch.entry_difficulty} accent="#7c3aed" icon={Shield} delay={0.3} />
                        </div>
                    </div>

                    {/* Right — gauge */}
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem', minWidth: 200 }}>
                        <div style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                            <GaugeSVG score={topMatch.match_score} size={200} />
                            <div style={{ position: 'absolute', textAlign: 'center' }}>
                                <div style={{
                                    fontSize: '3rem', fontWeight: 900, lineHeight: 1,
                                    color: '#1e3a5f'
                                }}>
                                    {pct(topMatch.match_score)}
                                </div>
                                <div style={{ fontSize: '0.6rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.25em', color: '#94a3b8', marginTop: '0.3rem' }}>
                                    Match Quality
                                </div>
                            </div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '1.1rem', fontWeight: 900, color: '#1e3a5f', letterSpacing: '-0.02em' }}>
                                {getMatchLabel(topMatch.match_score)}
                            </div>
                            <div style={{ fontSize: '0.65rem', color: '#64748b', fontWeight: 500, marginTop: '2px' }}>
                                Human-verified career alignment
                            </div>
                        </div>
                        <div style={{ background: 'rgba(37,99,235,0.08)', border: '1px solid rgba(37,99,235,0.2)', borderRadius: '10px', padding: '0.5rem 1.2rem', textAlign: 'center' }}>
                            <Sparkles size={12} style={{ color: '#2563eb', marginRight: 5, verticalAlign: 'middle' }} />
                            <span style={{ fontSize: '0.7rem', fontWeight: 700, color: '#1e3a5f', textTransform: 'uppercase', letterSpacing: '0.12em' }}>AI ANALYZED</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* ── TABS ─────────────────────────────────────────── */}
            <div ref={contentRef} style={{
                display: 'flex', gap: '0.4rem', marginBottom: '2rem',
                scrollMarginTop: '100px', /* Ensure it doesn't hidden under navbar */
                background: 'transparent', 
            }}>
                {tabs.map(t => {
                    const Icon = t.icon;
                    const active = activeTab === t.id;
                    return (
                        <button key={t.id} type="button" onClick={() => switchTab(t.id)} style={{
                            display: 'flex', alignItems: 'center', gap: '0.5rem',
                            padding: '0.65rem 1.25rem', borderRadius: '12px',
                            border: 'none', cursor: 'pointer', whiteSpace: 'nowrap',
                            fontSize: '0.875rem', fontWeight: active ? 700 : 500,
                            fontFamily: 'Plus Jakarta Sans, sans-serif',
                            background: active ? 'rgba(255, 255, 255, 0.4)' : 'transparent', /* Subtle glass blend */
                            backdropFilter: active ? 'blur(10px)' : 'none',
                            color: active ? '#1e3a5f' : '#475569',
                            transition: 'all 0.2s',
                            boxShadow: active ? '0 4px 12px rgba(30,58,95,0.04)' : 'none'
                        }}>
                            <Icon size={15} />
                            {t.label}
                        </button>
                    );
                })}
            </div>

            {/* ── TAB: OVERVIEW ─────────────────────────────────── */}
            {activeTab === 'overview' && (
                <div style={{ animation: 'fadeUp 0.45s both' }}>
                    {/* Personalized Input Reflection Card */}
                    <InputReflectionCard userData={userData} topMatch={topMatch} />

                    <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '1.5rem' }}>
                        {/* Neural Analysis */}
                        <div style={{
                            background: '#ffffff',
                            border: '1px solid rgba(30,58,95,0.09)',
                            borderLeft: '3px solid #2563eb',
                            borderRadius: '24px', padding: '2rem',
                            boxShadow: '0 2px 16px rgba(30,58,95,0.07)'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                                <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(37,99,235,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(37,99,235,0.15)' }}>
                                    <Activity size={18} style={{ color: '#2563eb' }} />
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Neural Analysis</h3>
                                    <p style={{ fontSize: '0.7rem', color: '#94a3b8', margin: 0 }}>AI-Generated Reasoning</p>
                                </div>
                            </div>
                            <p style={{ fontSize: '1rem', lineHeight: 1.75, color: '#334155', marginBottom: '1.75rem' }}>
                                {results.explanation || topMatch.why_it_matches}
                            </p>
                            {results.top_features?.length > 0 && (
                                <div>
                                    <p style={{ fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.15em', color: '#94a3b8', marginBottom: '0.75rem' }}>Key Signals</p>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        {results.top_features.map((f, i) => {
                                            const name = typeof f === 'object' ? (f.name || f.feature || '') : f;
                                            return (
                                                <span key={i} style={{
                                                    padding: '0.3rem 0.8rem', background: 'rgba(37,99,235,0.07)',
                                                    border: '1px solid rgba(37,99,235,0.18)', borderRadius: '8px',
                                                    fontSize: '0.78rem', fontWeight: 600, color: '#1e3a5f'
                                                }}>
                                                    {name.replace(/_/g, ' ')}
                                                </span>
                                            );
                                        })}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Right column — Employers + Skill Gap */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                            {/* Top employers */}
                            <div style={{
                                background: '#ffffff',
                                border: '1px solid rgba(30,58,95,0.09)',
                                borderLeft: '3px solid #0d9488',
                                borderRadius: '24px', padding: '2rem', flex: 1,
                                boxShadow: '0 2px 16px rgba(30,58,95,0.07)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
                                    <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(13,148,136,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(13,148,136,0.15)' }}>
                                        <Building2 size={18} style={{ color: '#0d9488' }} />
                                    </div>
                                    <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Who is Hiring?</h3>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                                    {topMatch.top_employers?.map((emp, i) => (
                                        <div key={i} style={{
                                            display: 'flex', alignItems: 'center', gap: '0.75rem',
                                            padding: '0.7rem 0.9rem',
                                            background: 'rgba(248,250,252,0.9)',
                                            border: '1px solid rgba(30,58,95,0.08)',
                                            borderRadius: '12px'
                                        }}>
                                            <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#0d9488', flexShrink: 0 }} />
                                            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#1e293b' }}>{emp}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Work-life balance */}
                            <div style={{
                                background: 'rgba(13,148,136,0.04)', border: '1px solid rgba(13,148,136,0.15)',
                                borderRadius: '24px', padding: '1.75rem'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.6rem' }}>
                                    <Clock size={16} style={{ color: '#0d9488' }} />
                                    <span style={{ fontSize: '0.7rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.15em', color: '#94a3b8' }}>Daily Life Balance</span>
                                </div>
                                <p style={{ fontSize: '0.95rem', fontWeight: 600, color: '#0d9488' }}>{topMatch.work_life_balance}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* ── TAB: ROADMAP ─────────────────────────────────── */}
            {activeTab === 'roadmap' && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', animation: 'fadeUp 0.45s both' }}>
                    {/* Learning path */}
                    <div style={{ background: '#ffffff', border: '1px solid rgba(30,58,95,0.09)', borderLeft: '3px solid #2563eb', borderRadius: '24px', padding: '2rem', boxShadow: '0 2px 16px rgba(30,58,95,0.07)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.75rem' }}>
                            <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(37,99,235,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(37,99,235,0.15)' }}>
                                <BookOpen size={18} style={{ color: '#2563eb' }} />
                            </div>
                            <div>
                                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Success Blueprint</h3>
                                <p style={{ fontSize: '0.7rem', color: '#94a3b8', margin: 0 }}>Step-by-step path to your future</p>
                            </div>
                        </div>
                        {topMatch.learning_roadmap?.map((step, i) => (
                            <RoadmapStep key={i} step={step} idx={i} total={topMatch.learning_roadmap.length} />
                        ))}
                    </div>

                    {/* Recommended skills + core challenges */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div style={{ background: '#ffffff', border: '1px solid rgba(30,58,95,0.09)', borderLeft: '3px solid #0d9488', borderRadius: '24px', padding: '2rem', flex: 1, boxShadow: '0 2px 16px rgba(30,58,95,0.07)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
                                <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(13,148,136,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(13,148,136,0.15)' }}>
                                    <Trophy size={18} style={{ color: '#0d9488' }} />
                                </div>
                                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Recommended Skills</h3>
                            </div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {topMatch.recommended_skills?.map((s, i) => (
                                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.4rem 0.9rem', background: 'rgba(13,148,136,0.07)', border: '1px solid rgba(13,148,136,0.18)', borderRadius: '10px' }}>
                                        <CheckCircle size={12} style={{ color: '#0d9488', flexShrink: 0 }} />
                                        <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#0d9488' }}>{s}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div style={{ background: 'rgba(124,58,237,0.04)', border: '1px solid rgba(124,58,237,0.14)', borderRadius: '24px', padding: '2rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                                <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(124,58,237,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(124,58,237,0.15)' }}>
                                    <XCircle size={18} style={{ color: '#7c3aed' }} />
                                </div>
                                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Core Challenges</h3>
                            </div>
                            <p style={{ fontSize: '0.95rem', color: '#475569', lineHeight: 1.65 }}>
                                {topMatch.core_challenges}
                            </p>
                        </div>

                        {/* Potential jobs */}
                        <div style={{ background: 'rgba(13,148,136,0.04)', border: '1px solid rgba(13,148,136,0.15)', borderRadius: '24px', padding: '2rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                                <div style={{ width: 36, height: 36, borderRadius: '10px', background: 'rgba(13,148,136,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid rgba(13,148,136,0.15)' }}>
                                    <Briefcase size={18} style={{ color: '#0d9488' }} />
                                </div>
                                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Potential Roles</h3>
                            </div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {topMatch.potential_jobs?.map((j, i) => (
                                    <span key={i} style={{ padding: '0.35rem 0.85rem', background: 'rgba(13,148,136,0.07)', border: '1px solid rgba(13,148,136,0.18)', borderRadius: '10px', fontSize: '0.82rem', fontWeight: 600, color: '#0d9488' }}>
                                        {j}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* ── TAB: ALTERNATIVES ────────────────────────────── */}
            {activeTab === 'alternatives' && (
                <div style={{ animation: 'fadeUp 0.45s both' }}>
                    {otherMatches.length === 0 ? (
                        <div style={{ textAlign: 'center', padding: '4rem', color: '#94a3b8' }}>
                            <Briefcase size={48} style={{ marginBottom: '1rem', opacity: 0.3 }} />
                            <p>No alternative trajectories available.</p>
                        </div>
                    ) : (
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.25rem' }}>
                            {otherMatches.map((rec, idx) => <AlternativeCard key={idx} rec={rec} idx={idx} userData={userData} />)}
                        </div>
                    )}
                </div>
            )}

            {/* ── TAB: AI COACH ─────────────────────────────────── */}
            {activeTab === 'coach' && (
                <div ref={chatRef} style={{ animation: 'fadeUp 0.45s both' }}>
                    {!showChat ? (
                        <div style={{
                            background: 'linear-gradient(135deg, rgba(37,99,235,0.06), rgba(30,58,95,0.04))',
                            border: '1px solid rgba(37,99,235,0.15)',
                            borderTop: '3px solid #1e3a5f',
                            borderRadius: '28px', padding: '5rem 3rem',
                            textAlign: 'center',
                            boxShadow: '0 4px 24px rgba(30,58,95,0.08)'
                        }}>
                            <div style={{ width: 80, height: 80, borderRadius: '24px', background: 'linear-gradient(135deg, #0f2444, #2563eb)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 2rem', boxShadow: '0 16px 40px -10px rgba(30,58,95,0.4)' }}>
                                <MessageSquare size={36} style={{ color: 'white' }} />
                            </div>
                            <h2 style={{ fontSize: '2.5rem', fontWeight: 900, letterSpacing: '-0.04em', marginBottom: '1rem', color: '#0f172a' }}>Your AI Career Coach</h2>
                            <p style={{ color: '#475569', fontSize: '1.05rem', maxWidth: '540px', margin: '0 auto 2.5rem', lineHeight: 1.65 }}>
                                Get personalised advice, deep career insights, and a custom action plan from your AI coach — trained on your unique profile.
                            </p>
                            <button
                                onClick={() => { setShowChat(true); }}
                                className="btn-vibrance"
                                style={{ padding: '1.1rem 3rem', fontSize: '1rem' }}
                            >
                                <Sparkles size={18} />
                                Start Coaching Session
                            </button>
                        </div>
                    ) : (
                        <div className="chat-wrapper-integrated" style={{ animation: 'fadeUp 0.45s both' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem', padding: '0 1rem' }}>
                                <div style={{ width: 44, height: 44, borderRadius: '14px', background: 'linear-gradient(135deg, #0f2444, #2563eb)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 20px rgba(30,58,95,0.2)' }}>
                                    <Activity size={22} style={{ color: 'white' }} />
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '1.25rem', fontWeight: 800, margin: 0, color: '#0f172a' }}>Coach Nexus</h3>
                                    <div style={{ fontSize: '0.7rem', color: '#0d9488', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em' }}>● Live Session Active</div>
                                </div>
                            </div>
                            <Chat assessmentData={userData} />
                        </div>
                    )}
                </div>
            )}

            {/* ── BOTTOM ACTIONS ────────────────────────────────── */}
            <div style={{
                marginTop: '3rem', display: 'flex', justifyContent: 'center', gap: '1rem',
                paddingTop: '2rem', borderTop: '1px solid rgba(30,58,95,0.09)',
                animation: 'fadeUp 0.6s 0.4s both'
            }}>
                <button onClick={onReset} className="btn-vibrance" style={{ padding: '1rem 2.5rem', fontSize: '0.95rem' }}>
                    <RefreshCw size={16} />
                    New Assessment
                </button>
                <button 
                    onClick={() => {
                        setActiveTab('coach');
                        setShowChat(true); // Jump straight to chat
                    }} 
                    className="btn-outline" 
                    style={{ padding: '1rem 2.5rem', fontSize: '0.95rem' }}
                >
                    <MessageSquare size={16} />
                    Talk to Coach
                </button>
            </div>
        </div>
    );
};

export default Dashboard;
