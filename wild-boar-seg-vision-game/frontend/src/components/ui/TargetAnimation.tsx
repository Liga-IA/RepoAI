'use client'

import { motion } from 'framer-motion'

interface TargetAnimationProps {
  x: number
  y: number
  type: 'lock' | 'hit' | 'miss' | 'penalty'
  onComplete?: () => void
}

export default function TargetAnimation({ x, y, type, onComplete }: TargetAnimationProps) {
  const colors = {
    lock: '#4ade80',    // Verde para alvo travado
    hit: '#22c55e',     // Verde para acerto
    miss: '#f59e0b',    // Amarelo para erro
    penalty: '#ef4444', // Vermelho para penalidade
  }

  const color = colors[type]

  return (
    <motion.div
      className="absolute pointer-events-none"
      style={{
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: 'translate(-50%, -50%)',
      }}
      initial={{ scale: 0, opacity: 1 }}
      animate={{ scale: 1.5, opacity: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      onAnimationComplete={onComplete}
    >
      <svg width="80" height="80" viewBox="0 0 80 80">
        {/* Círculo externo */}
        <motion.circle
          cx="40"
          cy="40"
          r="35"
          fill="none"
          stroke={color}
          strokeWidth="3"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.3 }}
        />

        {/* Cruz central */}
        {type === 'hit' && (
          <>
            <motion.line
              x1="20"
              y1="40"
              x2="60"
              y2="40"
              stroke={color}
              strokeWidth="3"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.2, delay: 0.1 }}
            />
            <motion.line
              x1="40"
              y1="20"
              x2="40"
              y2="60"
              stroke={color}
              strokeWidth="3"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.2, delay: 0.1 }}
            />
          </>
        )}

        {/* X para miss/penalty */}
        {(type === 'miss' || type === 'penalty') && (
          <>
            <motion.line
              x1="25"
              y1="25"
              x2="55"
              y2="55"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.2, delay: 0.1 }}
            />
            <motion.line
              x1="55"
              y1="25"
              x2="25"
              y2="55"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.2, delay: 0.1 }}
            />
          </>
        )}

        {/* Cantos do alvo */}
        {type === 'lock' && (
          <>
            {/* Superior esquerdo */}
            <motion.path
              d="M 15 25 L 15 15 L 25 15"
              fill="none"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.15 }}
            />
            {/* Superior direito */}
            <motion.path
              d="M 55 15 L 65 15 L 65 25"
              fill="none"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.15, delay: 0.05 }}
            />
            {/* Inferior esquerdo */}
            <motion.path
              d="M 15 55 L 15 65 L 25 65"
              fill="none"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.15, delay: 0.1 }}
            />
            {/* Inferior direito */}
            <motion.path
              d="M 55 65 L 65 65 L 65 55"
              fill="none"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.15, delay: 0.15 }}
            />
          </>
        )}
      </svg>
    </motion.div>
  )
}

// Componente para animação de alvo da IA
export function AITargetAnimation({ x, y, onComplete }: { x: number; y: number; onComplete?: () => void }) {
  return (
    <motion.div
      className="absolute pointer-events-none"
      style={{
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: 'translate(-50%, -50%)',
      }}
      initial={{ scale: 2, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      onAnimationComplete={onComplete}
    >
      <svg width="60" height="60" viewBox="0 0 60 60">
        {/* Círculo pulsante */}
        <motion.circle
          cx="30"
          cy="30"
          r="25"
          fill="rgba(239, 68, 68, 0.2)"
          stroke="#ef4444"
          strokeWidth="2"
          animate={{
            r: [25, 28, 25],
            strokeWidth: [2, 3, 2],
          }}
          transition={{
            duration: 0.5,
            repeat: 2,
          }}
        />

        {/* Mira interna */}
        <circle cx="30" cy="30" r="3" fill="#ef4444" />

        {/* Linhas de mira */}
        <line x1="30" y1="10" x2="30" y2="20" stroke="#ef4444" strokeWidth="2" />
        <line x1="30" y1="40" x2="30" y2="50" stroke="#ef4444" strokeWidth="2" />
        <line x1="10" y1="30" x2="20" y2="30" stroke="#ef4444" strokeWidth="2" />
        <line x1="40" y1="30" x2="50" y2="30" stroke="#ef4444" strokeWidth="2" />
      </svg>
    </motion.div>
  )
}

