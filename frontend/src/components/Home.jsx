import React from 'react';
import { motion } from 'framer-motion';
import {
  Zap, Compass, Target, Sparkles, MoveRight,
  ChevronRight, PieChart, ShieldCheck,
  Globe, Brain, Cpu, Layers
} from 'lucide-react';

const Home = ({ onStart }) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
  };

  return (
    <motion.div
      className="home-page-v3"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {/* 1. HERO SECTION */}
      {/* hero decorative glow removed for consistency */}
      <section className="landing-section hero-v3">

        <motion.div variants={itemVariants} className="badge-neural">
          <Sparkles size={14} className="text-secondary" />
          <span>Universe 3.0 • Neural Core v3.4</span>
        </motion.div>

        <motion.h1
          variants={itemVariants}
          className="gradient-text hero-title"
          style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', textAlign: 'center', lineHeight: 0.95 }}
        >
          Pilot Your<br />Infinite Potential
        </motion.h1>

        <motion.p variants={itemVariants} className="hero-subtitle">
          Experience the world's most advanced autonomous career coach.
          Powered by 528k neural data points and real-time market IQ.
        </motion.p>

        <motion.div variants={itemVariants} className="hero-actions">
          <button onClick={onStart} className="btn-vibrance lg">
            <span>Launch Analysis</span>
            <MoveRight size={22} />
          </button>
        </motion.div>

        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 3, repeat: Infinity }}
          className="scroll-indicator"
        >
          <ChevronRight size={32} style={{ transform: 'rotate(90deg)' }} />
        </motion.div>
      </section>

      {/* 2. THE NEURAL ENGINE GRID */}
      <section className="compact-section features-v3">
        <div className="section-header">
          <h2 className="gradient-text">The Neural Backbone</h2>
          <p>Cutting-edge technologies working in perfect harmony.</p>
        </div>

        <div className="features-grid-v3">
          <motion.div variants={itemVariants} className="feature-card-v3">
            <div className="icon-box"><Brain className="text-primary" /></div>
            <h3>Cognitive Matching</h3>
            <p>Our ML engine maps your unique psychological markers to 48+ elite career domains.</p>
          </motion.div>

          <motion.div variants={itemVariants} className="feature-card-v3">
            <div className="icon-box"><Cpu className="text-secondary" /></div>
            <h3>SHAP Reasoning</h3>
            <p>Transparency is core. See exactly why the AI made every single recommendation.</p>
          </motion.div>

          <motion.div variants={itemVariants} className="feature-card-v3">
            <div className="icon-box"><Globe className="text-accent" /></div>
            <h3>Global Market IQ</h3>
            <p>Real-time salary and outlook data fetched from the world's leading job indices.</p>
          </motion.div>

          <motion.div variants={itemVariants} className="feature-card-v3">
            <div className="icon-box"><Layers className="text-primary" /></div>
            <h3>Skill Gap Atlas</h3>
            <p>Automated roadmap generation to bridge the distance between you and your dream role.</p>
          </motion.div>
        </div>
      </section>

      {/* 3. CTA FOOTER */}
      <section className="compact-section cta-v3">
        <div className="vibrance-card cta-card-v3">
          <h2 className="gradient-text">Ready to launch?</h2>
          <p>Join 12,000+ professionals navigating their future with CareerPilot.</p>
          <button onClick={onStart} className="btn-vibrance">
            <span>Begin Neural Mapping</span>
            <Sparkles size={18} />
          </button>
        </div>
      </section>
    </motion.div>
  );
};

export default Home;
