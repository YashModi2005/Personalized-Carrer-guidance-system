import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Zap, Compass, Target, Sparkles, MoveRight,
  ChevronRight, PieChart, ShieldCheck,
  Globe, Brain, Cpu, Layers, Activity,
  Terminal, BarChart3
} from 'lucide-react';

const Home = ({ onStart }) => {
  const [feedItems, setFeedItems] = useState([
    "Neural Engine Initialized...",
    "Market Data Synced: 12.4k Job Patterns",
    "Personality Model Calibrated",
    "V3.4 Nexus Core Online"
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      const logs = [
        "Analyzing Skill Trends in Cloud Engineering...",
        "Updating Salary Indices: +2.4% for AI Engineers",
        "New Roadmap Generated for Fullstack Devs",
        "Global Career Trajectories Updated",
        "Predicting Market Shift: DevOps 2026",
        "Cross-Referencing Tech Stack Requirements..."
      ];
      const randomLog = logs[Math.floor(Math.random() * logs.length)];
      setFeedItems(prev => [randomLog, ...prev.slice(0, 3)]);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.15 } }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
  };

  return (
    <motion.div
      className="nexus-home"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* --- HERO SECTION --- */}
      <section className="hero-nexus">
        <div className="hero-grid">
          <motion.div className="hero-left" variants={itemVariants}>
            <div className="badge-glow">
              <Activity size={14} className="pulse-slow" />
              <span>System Status: Optimal</span>
            </div>
            <h1 className="hero-title-mega">
              Pilot Your <br />
              <span className="text-gradient-nexus">Trajectory</span>
            </h1>
            <p className="hero-desc-nexus">
              The world's first autonomous career architect. We don't just predict jobs; we engineer your professional future using high-fidelity neural mapping.
            </p>
            <div className="hero-actions-nexus">
              <button onClick={onStart} className="btn-nexus-main">
                <span>Start Neural Scan</span>
                <MoveRight size={20} />
              </button>
              <div className="user-proof">
                <div className="avatars-group">
                  <div className="avatar">YM</div>
                  <div className="avatar">JD</div>
                  <div className="avatar">AS</div>
                </div>
                <span>12k+ Analyzed</span>
              </div>
            </div>
          </motion.div>

          {/* --- NEURAL FEED (RIGHT SIDE) --- */}
          <motion.div className="hero-right" variants={itemVariants}>
            <div className="intelligence-terminal glass-dark">
              <div className="terminal-header">
                <div className="terminal-dots">
                  <span></span><span></span><span></span>
                </div>
                <span className="terminal-title">LIVE_INTELLIGENCE_FEED</span>
              </div>
              <div className="terminal-body">
                <AnimatePresence mode="popLayout">
                  {feedItems.map((item, i) => (
                    <motion.div
                      key={item}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      className="feed-line"
                    >
                      <span className="line-prefix">>></span>
                      <span className="line-text">{item}</span>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
              <div className="terminal-footer">
                <Terminal size={14} />
                <span>ACTIVE_NEXUS_CORE_V3.4</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* --- FLOATING COSMIC BACKGROUND --- */}
        <div className="cosmic-bg">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
        </div>
      </section>

      {/* --- FEATURE GRID --- */}
      <section className="nexus-features">
        <div className="features-container">
          <div className="features-intro">
            <h2 className="section-title-nexus">The Architecture</h2>
            <p>Our multi-layer neural network analyzes thousands of data points to ensure your career success.</p>
          </div>
          <div className="nexus-grid">
            <FeatureCard 
              icon={<Brain />} 
              title="Cognitive Engine" 
              desc="Maps your unique psychology to elite career domains." 
              color="indigo"
            />
            <FeatureCard 
              icon={<Cpu />} 
              title="Explainable AI" 
              desc="Transparency at every step. Understand every 'Why'." 
              color="cyan"
            />
            <FeatureCard 
              icon={<Globe />} 
              title="Market IQ" 
              desc="Real-time global salary and growth telemetry." 
              color="purple"
            />
            <FeatureCard 
              icon={<BarChart3 />} 
              title="Skill Atlas" 
              desc="Automated roadmap generation to bridge gaps." 
              color="blue"
            />
          </div>
        </div>
      </section>

      {/* --- FOOTER CTA --- */}
      <section className="nexus-footer-cta">
        <motion.div whileHover={{ scale: 1.01 }} className="cta-glass-card">
          <h2>Ready to Evolve?</h2>
          <p>Join the next generation of professionals guided by neural intelligence.</p>
          <button onClick={onStart} className="btn-nexus-main lg">
            <span>Initialize Mapping</span>
            <Sparkles size={20} />
          </button>
        </motion.div>
      </section>
    </motion.div>
  );
};

const FeatureCard = ({ icon, title, desc, color }) => (
  <motion.div 
    whileHover={{ y: -10 }}
    className={`nexus-feature-card ${color}`}
  >
    <div className="feature-icon-wrapper">{icon}</div>
    <h3>{title}</h3>
    <p>{desc}</p>
  </motion.div>
);

export default Home;

