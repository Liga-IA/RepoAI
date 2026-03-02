'use client'

import { motion } from 'framer-motion'
import { useGameStore } from '@/store/gameStore'
import { User, Brain, Target, AlertTriangle, Crosshair, Eye, EyeOff } from 'lucide-react'

export default function Scoreboard() {
  const {
    playerName,
    playerScore,
    playerHits,
    playerMisses,
    playerHumanHits,
    aiScore,
    aiHits,
    aiMisses,
    aiHumanHits,
    showDetections,
    toggleDetections,
  } = useGameStore()

  const playerLeading = playerScore > aiScore
  const aiLeading = aiScore > playerScore

  return (
    <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-stretch">
      {/* Placar do Jogador */}
      <motion.div
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className={`card p-4 ${playerLeading ? 'ring-2 ring-forest-500/50' : ''}`}
      >
        <div className="flex items-center gap-3 mb-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-forest-600 to-forest-800 
                          flex items-center justify-center border-2 border-forest-500">
            <User className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="text-earth-400 text-xs uppercase tracking-wider">Jogador</p>
            <p className="text-white font-semibold truncate max-w-[120px]">{playerName}</p>
          </div>
          {playerLeading && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="ml-auto text-forest-400 text-sm font-medium px-2 py-1 bg-forest-900/50 rounded"
            >
              Liderando!
            </motion.span>
          )}
        </div>

        <div className="flex items-baseline gap-2">
          <motion.span
            key={playerScore}
            initial={{ scale: 1.2, color: playerScore > 0 ? '#4ade80' : '#f87171' }}
            animate={{ scale: 1, color: '#ffffff' }}
            className="score-display text-white"
          >
            {playerScore}
          </motion.span>
          <span className="text-earth-500 text-sm">pts</span>
        </div>

        <div className="grid grid-cols-3 gap-2 mt-3">
          <StatMini icon={<Target className="w-4 h-4" />} value={playerHits} label="Acertos" positive />
          <StatMini icon={<Crosshair className="w-4 h-4" />} value={playerMisses} label="Erros" />
          <StatMini 
            icon={<AlertTriangle className="w-4 h-4" />} 
            value={playerHumanHits} 
            label="Humanos" 
            danger 
          />
        </div>
      </motion.div>

      {/* Centro - VS e controles */}
      <div className="flex flex-col items-center justify-center gap-2">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', delay: 0.2 }}
          className="relative"
        >
          <span className="font-display text-4xl text-warning-400">VS</span>
          
          {/* Indicador de diferença */}
          <motion.div
            key={`${playerScore}-${aiScore}`}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`absolute -bottom-6 left-1/2 -translate-x-1/2 text-sm font-mono ${
              playerScore > aiScore 
                ? 'text-forest-400' 
                : playerScore < aiScore 
                  ? 'text-danger-400' 
                  : 'text-earth-400'
            }`}
          >
            {playerScore !== aiScore && (
              <>
                {playerScore > aiScore ? '+' : '-'}
                {Math.abs(playerScore - aiScore)}
              </>
            )}
          </motion.div>
        </motion.div>

        {/* Toggle de detecções (debug) */}
        <button
          onClick={toggleDetections}
          className={`mt-6 p-2 rounded-lg transition-all ${
            showDetections 
              ? 'bg-forest-600/30 text-forest-400' 
              : 'bg-earth-800/50 text-earth-500 hover:text-earth-300'
          }`}
          title={showDetections ? 'Esconder detecções' : 'Mostrar detecções'}
        >
          {showDetections ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
        </button>
      </div>

      {/* Placar da IA */}
      <motion.div
        initial={{ x: 50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className={`card p-4 ${aiLeading ? 'ring-2 ring-danger-500/50' : ''}`}
      >
        <div className="flex items-center gap-3 mb-3">
          {aiLeading && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="text-danger-400 text-sm font-medium px-2 py-1 bg-danger-900/50 rounded"
            >
              Liderando!
            </motion.span>
          )}
          <div className="ml-auto text-right">
            <p className="text-earth-400 text-xs uppercase tracking-wider">Inteligência Artificial</p>
            <p className="text-white font-semibold">YOLOv8 Bot</p>
          </div>
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-danger-600 to-danger-800 
                          flex items-center justify-center border-2 border-danger-500">
            <Brain className="w-6 h-6 text-white" />
          </div>
        </div>

        <div className="flex items-baseline gap-2 justify-end">
          <span className="text-earth-500 text-sm">pts</span>
          <motion.span
            key={aiScore}
            initial={{ scale: 1.2, color: aiScore > 0 ? '#4ade80' : '#f87171' }}
            animate={{ scale: 1, color: '#ffffff' }}
            className="score-display text-white"
          >
            {aiScore}
          </motion.span>
        </div>

        <div className="grid grid-cols-3 gap-2 mt-3">
          <StatMini icon={<Target className="w-4 h-4" />} value={aiHits} label="Acertos" positive />
          <StatMini icon={<Crosshair className="w-4 h-4" />} value={aiMisses} label="Erros" />
          <StatMini 
            icon={<AlertTriangle className="w-4 h-4" />} 
            value={aiHumanHits} 
            label="Humanos" 
            danger 
          />
        </div>
      </motion.div>
    </div>
  )
}

function StatMini({ 
  icon, 
  value, 
  label, 
  positive = false,
  danger = false 
}: { 
  icon: React.ReactNode
  value: number
  label: string
  positive?: boolean
  danger?: boolean
}) {
  return (
    <div className="bg-earth-900/30 rounded px-2 py-1.5 text-center">
      <div className={`flex items-center justify-center gap-1 ${
        danger 
          ? 'text-danger-400' 
          : positive 
            ? 'text-forest-400' 
            : 'text-earth-400'
      }`}>
        {icon}
        <span className="font-mono text-sm font-bold">{value}</span>
      </div>
      <span className="text-earth-500 text-[10px] uppercase">{label}</span>
    </div>
  )
}

