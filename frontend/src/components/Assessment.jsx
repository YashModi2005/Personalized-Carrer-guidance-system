import React, { useState } from 'react';
import {
    User, Brain, Target, Wrench, Lightbulb, Sparkles,
    MoveRight, GraduationCap, Zap, Heart, ChevronLeft,
    ChevronRight, Award, BookOpen, Activity, AlertCircle
} from 'lucide-react';
import Toast from './Toast';

/* ── Step definitions ───────────────────────────────────── */
const STEPS = [
    { id: 1, label: 'Identity', icon: User, desc: 'Tell us about yourself' },
    { id: 2, label: 'Skills', icon: Wrench, desc: 'Your strengths & expertise' },
    { id: 3, label: 'Extras', icon: Lightbulb, desc: 'Interests & activities' },
];

/* ── Step progress bar ──────────────────────────────────── */
const StepBar = ({ current }) => (
    <div style={{ marginBottom: '2.5rem' }}>
        {/* Step dots + connector */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0, marginBottom: '0.75rem' }}>
            {STEPS.map((step, idx) => {
                const done = current > step.id;
                const active = current === step.id;
                const Icon = step.icon;
                return (
                    <React.Fragment key={step.id}>
                        {/* Dot */}
                        <div style={{
                            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.35rem',
                            position: 'relative', zIndex: 1
                        }}>
                            <div style={{
                                width: 44, height: 44, borderRadius: '50%',
                                background: done ? '#0d9488' : active ? '#1e3a5f' : 'rgba(30,58,95,0.08)',
                                border: active ? '2.5px solid #2563eb' : done ? '2.5px solid #0d9488' : '2px solid rgba(30,58,95,0.18)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                transition: 'all 0.35s cubic-bezier(0.4,0,0.2,1)',
                                boxShadow: active ? '0 0 0 4px rgba(37,99,235,0.15)' : done ? '0 0 0 3px rgba(13,148,136,0.12)' : 'none'
                            }}>
                                {done
                                    ? <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8l4 4 6-7" stroke="white" strokeWidth="2" strokeLinecap="round" /></svg>
                                    : <Icon size={18} color={active ? 'white' : '#94a3b8'} />
                                }
                            </div>
                            <span style={{
                                fontSize: '0.68rem', fontWeight: active || done ? 700 : 500,
                                color: active ? '#1e3a5f' : done ? '#0d9488' : '#94a3b8',
                                letterSpacing: '0.05em', textTransform: 'uppercase',
                                transition: 'color 0.3s'
                            }}>{step.label}</span>
                        </div>
                        {/* Connector line */}
                        {idx < STEPS.length - 1 && (
                            <div style={{
                                flex: 1, height: '2px', margin: '0 0.5rem',
                                marginBottom: '1.25rem',
                                background: current > step.id
                                    ? 'linear-gradient(90deg, #0d9488, #2563eb)'
                                    : 'rgba(30,58,95,0.12)',
                                transition: 'background 0.5s ease',
                                borderRadius: '2px'
                            }} />
                        )}
                    </React.Fragment>
                );
            })}
        </div>

        {/* Step counter text */}
        <p style={{ textAlign: 'center', fontSize: '0.8rem', color: '#94a3b8', fontWeight: 500 }}>
            Step <strong style={{ color: '#1e3a5f' }}>{current}</strong> of {STEPS.length} — {STEPS[current - 1].desc}
        </p>
    </div>
);

/* ── Field label with icon ──────────────────────────────── */
const FieldLabel = ({ icon: Icon, children, accent = '#1e3a5f' }) => (
    <label style={{
        display: 'flex', alignItems: 'center', gap: '0.5rem',
        fontSize: '0.75rem', fontWeight: 800,
        color: accent,
        textTransform: 'uppercase', letterSpacing: '0.15em',
        marginBottom: '0.75rem'
    }}>
        <span style={{
            width: 20, height: 20, borderRadius: '5px',
            background: `${accent}14`, display: 'flex',
            alignItems: 'center', justifyContent: 'center', flexShrink: 0
        }}>
            <Icon size={12} color={accent} />
        </span>
        {children}
    </label>
);

/* ════════════════════════════════════════════════════════════
   MAIN COMPONENT
═══════════════════════════════════════════════════════════ */
const Assessment = ({ onComplete, onBack, apiBaseUrl, apiHeaders }) => {
    const [step, setStep] = useState(1);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [loadingMsg, setLoadingMsg] = useState("Initializing Engine...");
    const [toast, setToast] = useState(null);
    const [validationError, setValidationError] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        academic_percentage: 85,
        interests: '',
        tech_skills: '',
        soft_skills: '',
        extracurriculars: ''
    });

    const updateField = (field, value) =>
        setFormData(prev => ({ ...prev, [field]: value }));

    /* Validation per step */
    const isValidContent = (text) => {
        if (!text) return false;
        const clean = text.trim();
        
        // 1. Min length check (Allow 2-char terms like AI, ML, UI if they are purely letters)
        if (clean.length < 2) return false;
        if (clean.length === 2) return /^[a-zA-Z]+$/.test(clean);
        
        // 2. Reject pure numbers
        if (/^\d+$/.test(clean)) return false;

        // 3. Reject repetitive junk (e.g. "aaaaa")
        if (clean.length > 5 && /(.)\1{4,}/.test(clean.toLowerCase())) return false;

        // 4. Alphabet ratio check (require at least 50% letters for longer terms)
        const letters = [...clean].filter(char => /[a-zA-Z]/.test(char)).length;
        if (letters / clean.length < 0.5) return false;

        // 5. Numeric density check
        const digits = [...clean].filter(char => /[0-9]/.test(char)).length;
        if (digits > 3 && !clean.includes(' ')) {
            if (clean.length > 10) return false;
        }

        // 6. Special character density check
        const specialChars = [...clean].filter(char => !/[a-zA-Z0-9\s]/.test(char)).length;
        if (specialChars / clean.length > 0.5) return false;
        
        return true;
    };

    const canNext = () => {
        if (step === 1) {
            return formData.name.trim().length > 0 && isValidContent(formData.interests);
        }
        if (step === 2) {
            return isValidContent(formData.tech_skills) && isValidContent(formData.soft_skills);
        }
        return true;
    };

    const handleNext = () => {
        setValidationError(null);
        if (step === 1 && !isValidContent(formData.interests)) {
            setValidationError("Please provide a more descriptive interest (no excessive symbols).");
            return;
        }
        if (step === 2 && (!isValidContent(formData.tech_skills) || !isValidContent(formData.soft_skills))) {
            setValidationError("Please describe your skills using real words and avoid excessive symbols.");
            return;
        }

        if (step < 3 && canNext()) setStep(s => s + 1);
    };
    const handlePrev = () => { if (step > 1) setStep(s => s - 1); };

    const handleSubmit = async (e) => {
        if (e) e.preventDefault();
        if (!canNext()) return;

        setIsSubmitting(true);
        const messages = [
            "Analyzing Interest Patterns...",
            "Contextualizing Skill Gradients...",
            "Mapping Core Aptitudes...",
            "Finalizing Recommendations..."
        ];
        let i = 0;
        const interval = setInterval(() => {
            setLoadingMsg(messages[i % messages.length]);
            i++;
        }, 1500);

        try {
            const response = await fetch(`${apiBaseUrl}/recommend`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...apiHeaders },
                body: JSON.stringify(formData),
            });
            if (!response.ok) throw new Error('API Sync Failed');
            const data = await response.json();
            clearInterval(interval);
            
            if (data.is_valid === false) {
                setValidationError(data.validation_message || "Invalid input detected. Please refine your skills.");
                setIsSubmitting(false);
                return;
            }
            
            onComplete(formData, data);
        } catch (err) {
            console.error(err);
            clearInterval(interval);
            setToast({ message: "Neural Engine Sync Failed. Please retry.", type: 'error' });
            setLoadingMsg("Engine Error. Retrying connection...");
            setTimeout(() => setIsSubmitting(false), 2000);
        }
    };

    /* ── Loading screen ───────────────────────────────────── */
    if (isSubmitting) {
        return (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
                <div style={{ position: 'relative', display: 'inline-block', marginBottom: '3rem' }}>
                    <div className="progress-ring" style={{ width: '120px', height: '120px', borderWidth: '2px' }}></div>
                    <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
                        <Brain size={48} className="text-primary" />
                    </div>
                </div>
                <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Processing Future</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', letterSpacing: '0.05em' }}>{loadingMsg}</p>
            </div>
        );
    }

    /* ── Form ─────────────────────────────────────────────── */
    return (
        <div className="assessment-wrapper">
            {/* Inline slider CSS */}
            <style>{`
                .navy-slider {
                    -webkit-appearance: none;
                    appearance: none;
                    width: 100%;
                    height: 6px;
                    border-radius: 3px;
                    background: linear-gradient(
                        to right,
                        #1e3a5f 0%,
                        #2563eb calc(${((formData.academic_percentage - 50) / 50) * 100}%),
                        rgba(30,58,95,0.15) calc(${((formData.academic_percentage - 50) / 50) * 100}%)
                    );
                    outline: none;
                    cursor: pointer;
                    margin: 0.75rem 0;
                }
                .navy-slider::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    appearance: none;
                    width: 20px; height: 20px;
                    border-radius: 50%;
                    background: #1e3a5f;
                    border: 3px solid white;
                    box-shadow: 0 2px 8px rgba(30,58,95,0.4);
                    cursor: pointer;
                    transition: transform 0.15s, box-shadow 0.15s;
                }
                .navy-slider::-webkit-slider-thumb:hover {
                    transform: scale(1.2);
                    box-shadow: 0 4px 16px rgba(30,58,95,0.5);
                }
                .navy-slider::-moz-range-thumb {
                    width: 20px; height: 20px;
                    border-radius: 50%;
                    background: #1e3a5f;
                    border: 3px solid white;
                    box-shadow: 0 2px 8px rgba(30,58,95,0.4);
                    cursor: pointer;
                }
                .step-fade-in {
                    animation: stepIn 0.35s cubic-bezier(0.4,0,0.2,1) both;
                }
                @keyframes stepIn {
                    from { opacity: 0; transform: translateX(20px); }
                    to   { opacity: 1; transform: translateX(0);     }
                }
                .btn-press:active { transform: scale(0.97) !important; }
            `}</style>

            {/* Header */}
            <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
                <h2 className="gradient-text" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Career Assessment</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem' }}>Your personalized AI career blueprint</p>
            </div>

            {/* Step progress bar */}
            <StepBar current={step} />

            {/* Validation Error Banner */}
            {validationError && (
                <div style={{
                    background: 'rgba(239, 68, 68, 0.08)',
                    border: '1px solid rgba(239, 68, 68, 0.25)',
                    borderRadius: '12px',
                    padding: '1rem 1.5rem',
                    marginBottom: '1.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    animation: 'fadeUp 0.3s both'
                }}>
                    <AlertCircle size={20} style={{ color: '#ef4444', flexShrink: 0 }} />
                    <div style={{ flex: 1 }}>
                        <h4 style={{ margin: 0, fontSize: '0.9rem', fontWeight: 800, color: '#b91c1c' }}>Analysis Blocked</h4>
                        <p style={{ margin: '0.1rem 0 0', fontSize: '0.8rem', color: '#dc2626', fontWeight: 500 }}>
                            {validationError}
                        </p>
                    </div>
                    <button 
                        onClick={() => setValidationError(null)}
                        style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontWeight: 800, fontSize: '0.75rem' }}
                    >
                        DISMISS
                    </button>
                </div>
            )}

            <form onSubmit={handleSubmit}>
                {/* ── STEP 1: Identity ──────────────────────────── */}
                {step === 1 && (
                    <div className="assessment-grid step-fade-in">
                        <div className="input-group">
                            <FieldLabel icon={User} accent="#1e3a5f">Your Name</FieldLabel>
                            <input
                                className="input-vibrance"
                                placeholder="e.g. Alex Johnson"
                                value={formData.name}
                                onChange={(e) => updateField('name', e.target.value)}
                                required
                                autoFocus
                            />
                        </div>

                        <div className="input-group">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                                <FieldLabel icon={GraduationCap} accent="#2563eb">Academic Score</FieldLabel>
                                <span style={{
                                    background: '#1e3a5f', color: 'white',
                                    fontWeight: 800, fontSize: '0.85rem',
                                    padding: '0.2rem 0.7rem', borderRadius: '8px'
                                }}>{formData.academic_percentage}%</span>
                            </div>
                            <input
                                type="range"
                                min="50" max="100"
                                className="navy-slider"
                                value={formData.academic_percentage}
                                onChange={(e) => updateField('academic_percentage', parseInt(e.target.value))}
                            />
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.3rem' }}>
                                <span>50% (Pass)</span><span>75% (Merit)</span><span>100% (Distinction)</span>
                            </div>
                        </div>

                        <div className="input-group full-width">
                            <FieldLabel icon={Heart} accent="#7c3aed">Primary Interests</FieldLabel>
                            <input
                                className="input-vibrance"
                                placeholder="e.g. Artificial Intelligence, Music Production, Space Exploration"
                                value={formData.interests}
                                onChange={(e) => updateField('interests', e.target.value)}
                                required
                            />
                        </div>
                    </div>
                )}

                {/* ── STEP 2: Skills ────────────────────────────── */}
                {step === 2 && (
                    <div className="assessment-grid step-fade-in">
                        <div className="input-group">
                            <FieldLabel icon={Wrench} accent="#2563eb">Technical Skills</FieldLabel>
                            <textarea
                                className="input-vibrance"
                                placeholder="e.g. Python, Adobe Suite, React, UI Design"
                                value={formData.tech_skills}
                                onChange={(e) => updateField('tech_skills', e.target.value)}
                                required
                            />
                        </div>

                        <div className="input-group">
                            <FieldLabel icon={Brain} accent="#0d9488">Soft Skills</FieldLabel>
                            <textarea
                                className="input-vibrance"
                                placeholder="e.g. Leadership, Strategic Thinking, Creative Problem Solving"
                                value={formData.soft_skills}
                                onChange={(e) => updateField('soft_skills', e.target.value)}
                                required
                            />
                        </div>
                    </div>
                )}

                {/* ── STEP 3: Extras ────────────────────────────── */}
                {step === 3 && (
                    <div className="assessment-grid step-fade-in">
                        <div className="input-group full-width">
                            <FieldLabel icon={Lightbulb} accent="#1e3a5f">Extracurricular Activities</FieldLabel>
                            <input
                                className="input-vibrance"
                                placeholder="e.g. Hackathons, Competitive Sports, Open Source Contribution"
                                value={formData.extracurriculars}
                                onChange={(e) => updateField('extracurriculars', e.target.value)}
                            />
                        </div>

                        {/* Summary preview */}
                        <div className="input-group full-width" style={{
                            background: 'rgba(37,99,235,0.04)',
                            border: '1px solid rgba(37,99,235,0.14)',
                            borderRadius: '16px', padding: '1.5rem'
                        }}>
                            <p style={{ fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.15em', color: '#1e3a5f', marginBottom: '1rem' }}>
                                📋 Your Profile Summary
                            </p>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.88rem' }}>
                                {[
                                    { key: 'Name', val: formData.name || '—' },
                                    { key: 'Score', val: `${formData.academic_percentage}%` },
                                    { key: 'Interests', val: formData.interests || '—' },
                                    { key: 'Tech', val: formData.tech_skills || '—' },
                                ].map(({ key, val }) => (
                                    <div key={key}>
                                        <span style={{ color: '#94a3b8', fontWeight: 600 }}>{key}: </span>
                                        <span style={{ color: '#1e293b', fontWeight: 500 }}
                                            title={val}>{val.length > 35 ? val.slice(0, 35) + '…' : val}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* ── Navigation buttons ───────────────────────── */}
                <div style={{
                    marginTop: '2rem', display: 'flex', justifyContent: 'space-between', gap: '1rem',
                    borderTop: '1px solid rgba(30,58,95,0.09)', paddingTop: '2rem'
                }}>
                    {/* Left: Back */}
                    {step === 1 ? (
                        <button type="button" onClick={onBack} className="btn-outline btn-press">
                            <ChevronLeft size={18} />
                            Back
                        </button>
                    ) : (
                        <button type="button" onClick={handlePrev} className="btn-outline btn-press">
                            <ChevronLeft size={18} />
                            Previous
                        </button>
                    )}

                    {/* Right: Next or Submit */}
                    {step < 3 ? (
                        <button
                            type="button"
                            onClick={handleNext}
                            className="btn-vibrance btn-press"
                            style={{ flex: 1, justifyContent: 'center', opacity: canNext() ? 1 : 0.5 }}
                            disabled={!canNext()}
                        >
                            Next Step
                            <ChevronRight size={18} />
                        </button>
                    ) : (
                        <button
                            type="submit"
                            className="btn-vibrance btn-press"
                            style={{ flex: 1, justifyContent: 'center' }}
                        >
                            <Sparkles size={18} />
                            Launch Analysis
                        </button>
                    )}
                </div>
            </form>

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

export default Assessment;
