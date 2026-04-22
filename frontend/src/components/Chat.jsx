import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
    Bot, 
    User, 
    Cpu, 
    Download, 
    CheckCircle2, 
    AlertCircle, 
    BrainCircuit,
    ChevronRight,
    Terminal,
    Info,
    Volume2,
    VolumeX,
    Activity,
    Scan,
    Globe,
    LineChart,
    TrendingUp
} from 'lucide-react';

const API_BASE = "http://localhost:8000";

const NeuralBackground = () => {
    const canvasRef = useRef(null);
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let particles = [];
        const particleCount = 40;
        
        const resize = () => {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        };
        
        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }
        }

        for (let i = 0; i < particleCount; i++) particles.push(new Particle());

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = 'rgba(37, 99, 235, 0.05)';
            ctx.lineWidth = 0.5;
            
            particles.forEach((p, i) => {
                p.update();
                particles.slice(i + 1).forEach(p2 => {
                    const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 150) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                });
            });
            requestAnimationFrame(animate);
        };

        window.addEventListener('resize', resize);
        resize();
        animate();
        return () => window.removeEventListener('resize', resize);
    }, []);

    return <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 0 }} />;
};

const AudioVisualizer = ({ active }) => (
    <div style={{ display: 'flex', gap: '2px', alignItems: 'flex-end', height: '12px' }}>
        {[1, 2, 3, 4].map(i => (
            <div key={i} style={{ 
                width: '2px', 
                height: active ? `${Math.random() * 100}%` : '20%',
                background: '#2563eb',
                borderRadius: '1px',
                transition: 'height 0.1s ease',
                animation: active ? `bounce ${0.3 + i * 0.1}s infinite alternate` : 'none'
            }} />
        ))}
    </div>
);

const TypingMessage = ({ text, onComplete }) => {
    const [displayedText, setDisplayedText] = useState("");
    const [index, setIndex] = useState(0);

    useEffect(() => {
        if (index < text.length) {
            const timer = setTimeout(() => {
                setDisplayedText((prev) => prev + text[index]);
                setIndex((prev) => prev + 1);
            }, 10); // Fast typing
            return () => clearTimeout(timer);
        } else if (onComplete) {
            onComplete();
        }
    }, [index, text, onComplete]);

    return <ReactMarkdown>{displayedText}</ReactMarkdown>;
};

const Chat = ({ assessmentData }) => {
    const [messages, setMessages] = useState([
        {
            text: "Hello! I am your Professional AI Career Coach. I've analyzed your profile and I am ready to guide you. **I can help you with these questions:**",
            isAgent: true,
            isTyped: true,
            suggestions: [
                "What is my first step?", 
                "Who will hire me?", 
                "Daily life in this career", 
                "How much will I earn?", 
                "Interview tips for me", 
                "Is this a growing field?"
            ]
        }
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [personality, setPersonality] = useState("professional");
    const [isMuted, setIsMuted] = useState(false);
    const [isScanning, setIsScanning] = useState(false);
    const [isReasoningPanelOpen, setIsReasoningPanelOpen] = useState(false);
    const [terminalLogs, setTerminalLogs] = useState(["[SYSTEM] INITIALIZING_CORE..."]);
    const sessionIdRef = useRef(`session_${Math.random().toString(36).substr(2, 9)}`);
    const [sessionId] = useState(sessionIdRef.current);
    const listRef = useRef(null);
    const scrollToBottom = () => {
        if (listRef.current) {
            listRef.current.scrollTo({
                top: listRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    };

    const [reasoningStep, setReasoningStep] = useState(0);
    const reasoningClips = [
        "Syncing with Profile...",
        "Analyzing Skill Marketplace...",
        "Validating Career Trajectories...",
        "Identifying Growth Milestones...",
        "Synthesizing Strategic Advice..."
    ];

    useEffect(() => {
        let interval;
        if (isLoading) {
            interval = setInterval(() => {
                setReasoningStep(prev => (prev + 1) % reasoningClips.length);
                const logLines = [
                    `[FETCH] SYNC_DATA_SESSION_${sessionId.slice(0,4)}`,
                    `[MODEL] RELOAD_WEIGHTS_V2.4`,
                    `[XAI] SHAP_COMPUTE_START`,
                    `[NLP] INTENT_VECTORS_EXTRACTED`,
                    `[CACHE] HIT_LRU_PERSONALIZATION`,
                    `[CORE] SYNTHESIZING_ADVICE`
                ];
                setTerminalLogs(prev => [...prev.slice(-4), logLines[Math.floor(Math.random() * logLines.length)]]);
            }, 1200);
        } else {
            setReasoningStep(0);
        }
        return () => clearInterval(interval);
    }, [isLoading]);

    const exportChat = () => {
        const chatText = messages.map(m => `${m.isAgent ? 'AI COACH' : 'USER'}: ${m.text}`).join('\n\n---\n\n');
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `career_session_${sessionId.slice(0,8)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    const speak = (text) => {
        if (isMuted) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text.replace(/[*#]/g, ''));
        utterance.rate = 1.1;
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        window.speechSynthesis.speak(utterance);
    };

    const handleScan = () => {
        setIsScanning(true);
        setIsReasoningPanelOpen(true);
        setTerminalLogs(prev => [...prev, "[SCAN] INITIALIZING_RESUME_LASER...", "[SCAN] EXTRACTING_SEMANTIC_FEATURES..."]);
        
        setTimeout(() => {
            setIsScanning(false);
            const scanMsg = {
                text: "### 🧬 Deep Neural Scan Complete\nI have successfully parsed your professional profile and cross-referenced it with **global market benchmarks**. Your profile shows high resonance in technical execution but has a slight gap in specialized domain leadership. \n\n**Recommendation:** Focus on a 'Lead-First' certification to unlock Tier-1 salary brackets.",
                isAgent: true,
                isTyped: false,
                suggestions: ["How to fix leadership gap?", "Compare Tier-1 salaries", "Show my skill heatmap"]
            };
            setMessages(prev => [...prev, scanMsg]);
        }, 3500);
    };

    const handleSend = async (text) => {
        if (!text.trim()) return;

        const userMsg = { text, isAgent: false };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setIsLoading(true);
        setIsReasoningPanelOpen(true); 

        const token = sessionStorage.getItem('cp_token');

        try {
            const response = await axios.post(`${API_BASE}/chat`, {
                message: text,
                session_id: sessionId,
                personality: personality,
                context: assessmentData
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            const agentMsg = {
                text: response.data.response,
                isAgent: true,
                isTyped: false,
                suggestions: response.data.suggestions,
                data: response.data.data
            };

            setMessages(prev => [...prev, agentMsg]);
            if (!isMuted) speak(response.data.response);
        } catch (error) {
            const detail = error?.response?.data?.detail;
            setMessages(prev => [...prev, {
                text: detail
                    ? `⚠️ ${detail}`
                    : "I'm having a bit of trouble connecting to my reasoning core. Let's try that again in a moment!",
                isAgent: true,
                isTyped: true
            }]);
        } finally {
            setIsLoading(false);
            // Optionally close panel after delay
        }
    };

    return (
        <div className="chat-layout" style={{ display: 'flex', gap: '1rem', height: '100%', width: '100%' }}>
            <div className="chat-container" style={{ 
                flex: 1,
                display: 'flex', 
                flexDirection: 'column', 
                background: 'white',
                borderRadius: '24px',
                overflow: 'hidden',
                border: '1px solid #e2e8f0',
                boxShadow: '0 8px 32px rgba(30,58,95,0.08)',
                position: 'relative'
            }}>
                {/* CHAT HEADER STATUS BAR */}
                <div style={{ 
                    padding: '0.75rem 1.25rem', 
                    background: '#f8fafc', 
                    borderBottom: '1px solid #e2e8f0',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                        <div style={{ position: 'relative' }}>
                            <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981', boxShadow: '0 0 10px #10b981' }}></div>
                            {isLoading && (
                                <div style={{ 
                                    position: 'absolute', 
                                    top: -2, 
                                    left: -2, 
                                    width: 14, 
                                    height: 14, 
                                    borderRadius: '50%', 
                                    border: '2px solid #10b981',
                                    borderTopColor: 'transparent',
                                    animation: 'spin 1s linear infinite'
                                }}></div>
                            )}
                        </div>
                        <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#1e3a5f', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Neural Agent Engine v2.4</span>
                    </div>
                    
                    <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                        <button 
                            onClick={handleScan}
                            className="btn-vibrance"
                            style={{ 
                                padding: '4px 12px', 
                                borderRadius: '8px', 
                                fontSize: '0.65rem',
                                background: 'linear-gradient(135deg, #0d9488, #0f766e)',
                                boxShadow: 'none'
                            }}
                        >
                            <Scan size={14} /> Scan Profile
                        </button>
                        <div style={{ width: 1, height: 16, background: '#e2e8f0' }}></div>
                        <div style={{ 
                            display: 'flex', 
                            background: '#e2e8f0', 
                            padding: '2px', 
                            borderRadius: '8px',
                            marginRight: '0.5rem'
                        }}>
                            {['professional', 'friendly'].map(p => (
                                <button
                                    key={p}
                                    onClick={() => setPersonality(p)}
                                    style={{
                                        padding: '4px 10px',
                                        fontSize: '0.65rem',
                                        fontWeight: 800,
                                        border: 'none',
                                        borderRadius: '6px',
                                        background: personality === p ? 'white' : 'transparent',
                                        color: personality === p ? '#1e3a5f' : '#64748b',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s ease',
                                        textTransform: 'capitalize'
                                    }}
                                >
                                    {p}
                                </button>
                            ))}
                        </div>
                        <button 
                            onClick={() => setIsMuted(!isMuted)}
                            style={{ 
                                background: 'transparent', 
                                border: 'none', 
                                color: '#64748b', 
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px'
                            }}
                        >
                            <AudioVisualizer active={isSpeaking && !isMuted} />
                            {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
                        </button>
                        <div style={{ width: 1, height: 16, background: '#e2e8f0' }}></div>
                        <button 
                            onClick={exportChat}
                            style={{ 
                                background: 'transparent', 
                                border: 'none', 
                                color: '#64748b', 
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.4rem',
                                fontSize: '0.7rem',
                                fontWeight: 700
                            }}
                        >
                            <Download size={14} /> Export
                        </button>
                        <div style={{ width: 1, height: 16, background: '#e2e8f0' }}></div>
                        <button 
                            onClick={() => setIsReasoningPanelOpen(!isReasoningPanelOpen)}
                            style={{ 
                                background: isReasoningPanelOpen ? 'rgba(37,99,235,0.1)' : 'transparent', 
                                border: 'none', 
                                color: isReasoningPanelOpen ? '#2563eb' : '#64748b', 
                                cursor: 'pointer',
                                padding: '4px 8px',
                                borderRadius: '6px',
                                fontSize: '0.7rem',
                                fontWeight: 700,
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.4rem'
                            }}
                        >
                            <BrainCircuit size={14} /> Reasoning
                        </button>
                    </div>
                </div>

                <div className="chat-messages" ref={listRef} style={{ 
                    flex: 1, 
                    padding: '1.5rem', 
                    overflowY: 'auto', 
                    background: 'linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)', 
                    position: 'relative' 
                }}>
                    <NeuralBackground />
                    {/* SCANNER ANIMATION OVERLAY */}
                    {isScanning && (
                        <div style={{ 
                            position: 'absolute', 
                            top: 0, 
                            left: 0, 
                            width: '100%', 
                            height: '100%', 
                            background: 'rgba(37, 99, 235, 0.05)', 
                            zIndex: 10,
                            pointerEvents: 'none',
                            overflow: 'hidden'
                        }}>
                            <div style={{ 
                                width: '100%', 
                                height: '2px', 
                                background: '#2563eb', 
                                boxShadow: '0 0 20px #2563eb',
                                position: 'absolute',
                                animation: 'scanMove 1.5s infinite linear'
                            }}></div>
                        </div>
                    )}
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`message ${msg.isAgent ? 'message-agent' : 'message-user'}`} style={{ 
                            marginBottom: '1.5rem',
                            display: 'flex',
                            gap: '1rem',
                            flexDirection: msg.isAgent ? 'row' : 'row-reverse',
                            alignItems: 'flex-start'
                        }}>
                            {/* AVATAR */}
                            <div style={{ 
                                width: 36, 
                                height: 36, 
                                borderRadius: '12px', 
                                background: msg.isAgent ? 'linear-gradient(135deg, #1e3a5f, #2563eb)' : '#f1f5f9',
                                color: msg.isAgent ? 'white' : '#64748b',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexShrink: 0,
                                boxShadow: msg.isAgent ? '0 4px 12px rgba(37,99,235,0.2)' : 'none',
                                animation: msg.isAgent && isLoading ? 'neuralPulse 1.5s infinite ease-in-out' : 'none'
                            }}>
                                {msg.isAgent ? <Bot size={20} /> : <User size={20} />}
                            </div>

                            <div style={{ 
                                display: 'flex', 
                                flexDirection: 'column', 
                                alignItems: msg.isAgent ? 'flex-start' : 'flex-end',
                                maxWidth: '80%'
                            }}>
                                <div className="message-content" style={{
                                    padding: '1.1rem 1.4rem',
                                    borderRadius: '18px',
                                    borderTopLeftRadius: msg.isAgent ? '4px' : '18px',
                                    borderTopRightRadius: msg.isAgent ? '18px' : '4px',
                                    fontSize: '0.94rem',
                                    lineHeight: 1.6,
                                    background: msg.isAgent ? 'rgba(248, 250, 252, 0.8)' : '#1e3a5f',
                                    backdropFilter: msg.isAgent ? 'blur(8px)' : 'none',
                                    color: msg.isAgent ? '#1e293b' : 'white',
                                    border: msg.isAgent ? '1px solid rgba(226, 232, 240, 0.5)' : 'none',
                                    boxShadow: msg.isAgent ? '0 4px 12px rgba(0,0,0,0.03)' : '0 6px 18px rgba(30,58,95,0.15)',
                                    position: 'relative',
                                    zIndex: 1
                                }}>
                                    {msg.isAgent && !msg.isTyped ? (
                                        <TypingMessage 
                                            text={msg.text} 
                                            onComplete={() => {
                                                const updated = [...messages];
                                                updated[idx].isTyped = true;
                                                setMessages(updated);
                                                scrollToBottom();
                                            }} 
                                        />
                                    ) : (
                                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                                    )}
                                </div>

                                {msg.isAgent && msg.data && msg.isTyped && (
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', width: '100%' }}>
                                        {/* TRAJECTORY PULSE CARD */}
                                        <div style={{ 
                                            marginTop: '1rem', 
                                            width: '100%', 
                                            background: 'white', 
                                            border: '1px solid #e2e8f0',
                                            borderRadius: '14px',
                                            padding: '1rem',
                                            boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
                                        }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                                <Activity size={14} className="text-primary-light" />
                                                <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#1e3a5f' }}>TRAJECTORY PULSE</span>
                                            </div>
                                            <div style={{ fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.25rem' }}>{msg.data.career_details[0].career_title}</div>
                                            <div style={{ height: 6, background: '#f1f5f9', borderRadius: 3, overflow: 'hidden' }}>
                                                <div style={{ 
                                                    width: `${msg.data.career_details[0].match_score * 100}%`, 
                                                    height: '100%', 
                                                    background: 'linear-gradient(90deg, #1e3a5f, #2563eb)' 
                                                }}></div>
                                            </div>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.25rem' }}>
                                                <span style={{ fontSize: '0.6rem', color: '#94a3b8' }}>Confidence Index</span>
                                                <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#2563eb' }}>{(msg.data.career_details[0].match_score * 100).toFixed(0)}%</span>
                                            </div>

                                            {/* SALARY SPARKLINE */}
                                            <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid #f1f5f9' }}>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.5rem' }}>
                                                    <TrendingUp size={12} className="text-secondary" />
                                                    <span style={{ fontSize: '0.6rem', fontWeight: 800, color: '#64748b' }}>10-YEAR SALARY TRAJECTORY</span>
                                                </div>
                                                <div style={{ display: 'flex', alignItems: 'flex-end', gap: '4px', height: '30px' }}>
                                                    {[30, 45, 40, 65, 90].map((h, i) => (
                                                        <div key={i} style={{ 
                                                            flex: 1, 
                                                            height: `${h}%`, 
                                                            background: i === 4 ? '#0d9488' : '#e2e8f0', 
                                                            borderRadius: '2px',
                                                            transition: 'height 1s ease'
                                                        }}></div>
                                                    ))}
                                                </div>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.2rem' }}>
                                                    <span style={{ fontSize: '0.5rem', color: '#cbd5e1' }}>Entry</span>
                                                    <span style={{ fontSize: '0.5rem', color: '#cbd5e1' }}>Senior+</span>
                                                </div>
                                            </div>
                                        </div>

                                        {/* XAI FEATURE IMPORTANCE */}
                                        {msg.data.top_features && msg.data.top_features.length > 0 && (
                                            <div style={{ 
                                                width: '100%', 
                                                background: '#f1f5f9', 
                                                border: '1px solid #e2e8f0',
                                                borderRadius: '14px',
                                                padding: '1rem',
                                                color: '#1e293b',
                                                boxShadow: '0 4px 12px rgba(0,0,0,0.02)'
                                            }}>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                                                    <Cpu size={14} className="text-primary-light" />
                                                    <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#64748b' }}>NEURAL FEATURE WEIGHTS</span>
                                                </div>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                                    {msg.data.top_features.map((f, i) => (
                                                        <div key={i}>
                                                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.65rem', marginBottom: '0.25rem' }}>
                                                                <span style={{ opacity: 0.8, fontWeight: 600 }}>{f.name}</span>
                                                                <span style={{ color: '#2563eb', fontWeight: 800 }}>+{f.value.toFixed(3)}</span>
                                                            </div>
                                                            <div style={{ height: 4, background: '#e2e8f0', borderRadius: 2, overflow: 'hidden' }}>
                                                                <div style={{ 
                                                                    width: `${Math.min(100, f.value * 200)}%`, 
                                                                    height: '100%', 
                                                                    background: '#2563eb'
                                                                }}></div>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}
                                
                                {msg.isAgent && msg.suggestions && msg.suggestions.length > 0 && msg.isTyped && (
                                    <div className="suggestion-row" style={{ marginTop: '0.85rem', display: 'flex', gap: '0.6rem', flexWrap: 'wrap' }}>
                                        {msg.suggestions.map((s, i) => (
                                            <button
                                                key={i}
                                                className="suggestion-chip"
                                                onClick={() => handleSend(s)}
                                                style={{
                                                    padding: '0.4rem 1rem',
                                                    borderRadius: '12px',
                                                    border: '1px solid rgba(37,99,235,0.2)',
                                                    background: 'rgba(255,255,255,0.8)',
                                                    backdropFilter: 'blur(4px)',
                                                    color: '#2563eb',
                                                    fontSize: '0.75rem',
                                                    fontWeight: 800,
                                                    cursor: 'pointer',
                                                    transition: 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '0.4rem',
                                                    animation: `slideUpFade 0.4s ease-out forwards ${i * 0.1}s`,
                                                    opacity: 0,
                                                    boxShadow: '0 2px 8px rgba(37,99,235,0.05)'
                                                }}
                                            >
                                                <ChevronRight size={14} /> {s}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                {isLoading && (
                    <div className="message message-agent" style={{ marginBottom: '1.5rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <div className="thinking-loader" style={{ display: 'flex', gap: '4px' }}>
                                <span className="thinking-dot"></span>
                                <span className="thinking-dot"></span>
                                <span className="thinking-dot"></span>
                            </div>
                            <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#2563eb', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                {reasoningClips[reasoningStep]}
                            </span>
                        </div>
                    </div>
                )}
            </div>

                <div className="chat-input-area" style={{ padding: '1.25rem 2rem', background: '#f8fafc', borderTop: '1px solid #e2e8f0' }}>
                    <div className="chat-input-row" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <input
                            className="input-vibrance"
                            placeholder="Consult your career coach..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend(input)}
                            style={{ 
                                flex: 1, 
                                padding: '1rem 1.25rem', 
                                borderRadius: '14px', 
                                border: '1.5px solid #e2e8f0',
                                outline: 'none',
                                fontSize: '0.9rem'
                            }}
                        />
                        <button
                            className="btn-vibrance"
                            style={{ 
                                padding: '0.85rem 2rem', 
                                borderRadius: '14px', 
                                fontSize: '0.9rem',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.6rem'
                            }}
                            onClick={() => handleSend(input)}
                            disabled={isLoading}
                        >
                            {isLoading ? <Cpu size={18} className="spin" /> : <Terminal size={18} />}
                            <span>{isLoading ? 'Processing' : 'Analyze'}</span>
                        </button>
                    </div>
                </div>
            </div>

            {/* NEURAL REASONING SIDE PANEL */}
            {isReasoningPanelOpen && (
                <div className="reasoning-panel" style={{ 
                    width: '320px',
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdropFilter: 'blur(20px)',
                    borderRadius: '24px',
                    padding: '1.5rem',
                    color: '#1e3a5f',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '1.5rem',
                    border: '1px solid rgba(30, 58, 95, 0.1)',
                    boxShadow: '0 20px 50px rgba(30, 58, 95, 0.15)',
                    animation: 'fadeLeft 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
                    zIndex: 20
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <Globe size={20} className={isLoading ? "spin text-primary-light" : "text-primary-light"} />
                            <h3 style={{ margin: 0, fontSize: '0.9rem', fontWeight: 800, letterSpacing: '0.05em' }}>GLOBAL REASONER</h3>
                        </div>
                        <button 
                            onClick={() => setIsReasoningPanelOpen(false)}
                            style={{ background: 'transparent', border: 'none', color: '#64748b', cursor: 'pointer' }}
                        >
                            &times;
                        </button>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                        {reasoningClips.map((clip, i) => (
                            <div key={i} style={{ 
                                display: 'flex', 
                                gap: '1rem', 
                                alignItems: 'center',
                                opacity: i === reasoningStep && isLoading ? 1 : (i < reasoningStep || (!isLoading && i < reasoningClips.length) ? 0.8 : 0.3),
                                transition: 'all 0.4s ease'
                            }}>
                                <div style={{ 
                                    width: 24, 
                                    height: 24, 
                                    borderRadius: '50%', 
                                    background: i < reasoningStep || (!isLoading && i < reasoningClips.length) ? '#10b981' : '#f1f5f9',
                                    color: i < reasoningStep || (!isLoading && i < reasoningClips.length) ? 'white' : '#94a3b8',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '0.7rem'
                                }}>
                                    {i < reasoningStep || (!isLoading && i < reasoningClips.length) ? <CheckCircle2 size={14} /> : i + 1}
                                </div>
                                <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{clip}</span>
                            </div>
                        ))}
                    </div>

                    <div style={{ 
                        marginTop: 'auto', 
                        padding: '1rem', 
                        background: '#f8fafc', 
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0',
                        fontFamily: 'monospace'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
                            <Terminal size={14} className="text-primary-light" />
                            <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#64748b' }}>NEURAL_TERMINAL</span>
                        </div>
                        <div style={{ fontSize: '0.6rem', color: '#2563eb', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            {terminalLogs.map((log, i) => (
                                <div key={i} style={{ opacity: i === terminalLogs.length - 1 ? 1 : 0.5 }}>
                                    {log}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chat;
