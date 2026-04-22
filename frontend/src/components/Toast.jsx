import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertTriangle, Info, X } from 'lucide-react';

const Toast = ({ message, type = 'success', onClose, duration = 5000 }) => {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        setIsVisible(true);
        const timer = setTimeout(() => {
            handleClose();
        }, duration);
        return () => clearTimeout(timer);
    }, [duration]);

    const handleClose = () => {
        setIsVisible(false);
        setTimeout(onClose, 300); // Wait for fade out animation
    };

    const icons = {
        success: <CheckCircle size={20} color="#10b981" />,
        error: <AlertTriangle size={20} color="#ef4444" />,
        info: <Info size={20} color="#3b82f6" />
    };

    const colors = {
        success: 'rgba(16, 185, 129, 0.1)',
        error: 'rgba(239, 68, 68, 0.1)',
        info: 'rgba(59, 130, 246, 0.1)'
    };

    const borders = {
        success: '1px solid rgba(16, 185, 129, 0.2)',
        error: '1px solid rgba(239, 68, 68, 0.2)',
        info: '1px solid rgba(59, 130, 246, 0.2)'
    };

    return (
        <div style={{
            position: 'fixed',
            top: '2rem',
            right: '2rem',
            zIndex: 9999,
            transform: isVisible ? 'translateX(0)' : 'translateX(120%)',
            opacity: isVisible ? 1 : 0,
            transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem',
            padding: '1rem 1.5rem',
            background: 'rgba(15, 23, 42, 0.8)',
            backdropFilter: 'blur(12px)',
            borderRadius: '16px',
            border: borders[type],
            boxShadow: '0 20px 40px rgba(0,0,0,0.4)',
            color: 'white',
            minWidth: '300px'
        }}>
            <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: colors[type],
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}>
                {icons[type]}
            </div>
            <div style={{ flex: 1 }}>
                <p style={{ margin: 0, fontSize: '0.9rem', fontWeight: 500 }}>{message}</p>
            </div>
            <button
                onClick={handleClose}
                style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--text-dim)',
                    cursor: 'pointer',
                    padding: '4px',
                    display: 'flex'
                }}
            >
                <X size={16} />
            </button>

            {/* Progress Bar */}
            <div style={{
                position: 'absolute',
                bottom: 0,
                left: 0,
                height: '3px',
                background: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6',
                width: isVisible ? '100%' : '0%',
                transition: `width ${duration}ms linear`,
                borderRadius: '0 0 16px 16px',
                boxShadow: `0 -2px 10px ${type === 'success' ? 'rgba(16, 185, 129, 0.4)' : type === 'error' ? 'rgba(239, 68, 68, 0.4)' : 'rgba(59, 130, 246, 0.4)'}`
            }} />
        </div>
    );
};

export default Toast;
