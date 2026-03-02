'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useGameStore } from '@/store/gameStore'
import { Trophy, Medal, RotateCcw, Home, Share2, Target, AlertTriangle, Brain, User } from 'lucide-react'
import confetti from 'canvas-confetti'

export default function GameResults() {
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
    totalRounds,
    roundHistory,
    resetGame,
  } = useGameStore()

  const [showStats, setShowStats] = useState(false)

  const playerWon = playerScore > aiScore
  const tie = playerScore === aiScore

  // Calcula estatísticas
  const playerAccuracy = playerHits + playerMisses > 0 
    ? ((playerHits / (playerHits + playerMisses)) * 100).toFixed(1)
    : '0.0'
  
  const aiAccuracy = aiHits + aiMisses > 0
    ? ((aiHits / (aiHits + aiMisses)) * 100).toFixed(1)
    : '0.0'

  // Efeito de confetti para o vencedor
  useEffect(() => {
    if (playerWon) {
      const duration = 3000
      const end = Date.now() + duration

      const colors = ['#22c55e', '#4ade80', '#86efac']

      const frame = () => {
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: colors
        })
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: colors
        })

        if (Date.now() < end) {
          requestAnimationFrame(frame)
        }
      }
      frame()
    }

    // Mostra estatísticas após animação
    setTimeout(() => setShowStats(true), 500)
  }, [playerWon])

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="card-glow p-8 max-w-2xl w-full"
    >
      {/* Cabeçalho do resultado */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-center mb-8"
      >
        <motion.div
          animate={{ rotate: [0, -10, 10, 0] }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="inline-block mb-4"
        >
          {playerWon ? (
            <Trophy className="w-20 h-20 text-warning-400" />
          ) : tie ? (
            <Medal className="w-20 h-20 text-earth-400" />
          ) : (
            <Brain className="w-20 h-20 text-danger-400" />
          )}
        </motion.div>

        <h1 className="font-display text-5xl md:text-6xl text-white mb-2">
          {playerWon ? 'VITÓRIA!' : tie ? 'EMPATE!' : 'DERROTA'}
        </h1>
        
        <p className="text-earth-300 text-lg">
          {playerWon 
            ? 'Você foi mais rápido que a IA!' 
            : tie 
              ? 'Vocês estão empatados!' 
              : 'A IA foi mais precisa dessa vez.'}
        </p>
      </motion.div>

      {/* Placares finais */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-[1fr_auto_1fr] gap-4 mb-8"
      >
        {/* Jogador */}
        <div className={`text-center p-4 rounded-xl ${
          playerWon ? 'bg-forest-900/30 ring-2 ring-forest-500/50' : 'bg-earth-900/30'
        }`}>
          <div className="flex items-center justify-center gap-2 mb-2">
            <User className="w-5 h-5 text-forest-400" />
            <span className="text-earth-300 text-sm">{playerName}</span>
          </div>
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', delay: 0.5 }}
            className={`font-display text-5xl ${playerWon ? 'text-forest-400' : 'text-white'}`}
          >
            {playerScore}
          </motion.span>
          <p className="text-earth-500 text-sm mt-1">pontos</p>
        </div>

        {/* VS */}
        <div className="flex items-center">
          <span className="font-display text-3xl text-earth-600">VS</span>
        </div>

        {/* IA */}
        <div className={`text-center p-4 rounded-xl ${
          !playerWon && !tie ? 'bg-danger-900/30 ring-2 ring-danger-500/50' : 'bg-earth-900/30'
        }`}>
          <div className="flex items-center justify-center gap-2 mb-2">
            <Brain className="w-5 h-5 text-danger-400" />
            <span className="text-earth-300 text-sm">IA</span>
          </div>
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', delay: 0.5 }}
            className={`font-display text-5xl ${!playerWon && !tie ? 'text-danger-400' : 'text-white'}`}
          >
            {aiScore}
          </motion.span>
          <p className="text-earth-500 text-sm mt-1">pontos</p>
        </div>
      </motion.div>

      {/* Estatísticas detalhadas */}
      {showStats && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          className="border-t border-earth-800 pt-6 mb-8"
        >
          <h3 className="text-earth-400 text-sm uppercase tracking-wider mb-4 text-center">
            Estatísticas Detalhadas
          </h3>

          <div className="grid grid-cols-2 gap-6">
            {/* Stats do Jogador */}
            <div className="space-y-3">
              <h4 className="text-forest-400 font-semibold flex items-center gap-2">
                <User className="w-4 h-4" /> {playerName}
              </h4>
              <StatRow label="Precisão" value={`${playerAccuracy}%`} />
              <StatRow label="Javalis detectados" value={playerHits} positive />
              <StatRow label="Erros" value={playerMisses} />
              <StatRow label="Humanos atingidos" value={playerHumanHits} danger />
            </div>

            {/* Stats da IA */}
            <div className="space-y-3">
              <h4 className="text-danger-400 font-semibold flex items-center gap-2">
                <Brain className="w-4 h-4" /> Inteligência Artificial
              </h4>
              <StatRow label="Precisão" value={`${aiAccuracy}%`} />
              <StatRow label="Javalis detectados" value={aiHits} positive />
              <StatRow label="Erros" value={aiMisses} />
              <StatRow label="Humanos atingidos" value={aiHumanHits} danger />
            </div>
          </div>

          {/* Mensagem sobre humanos */}
          {(playerHumanHits > 0 || aiHumanHits > 0) && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 p-3 bg-danger-900/20 border border-danger-800/30 rounded-lg flex items-start gap-3"
            >
              <AlertTriangle className="w-5 h-5 text-danger-400 flex-shrink-0 mt-0.5" />
              <p className="text-danger-300 text-sm">
                Atenção: Acertar humanos resulta em penalidade severa (-200 pts).
                Em sistemas reais, a segurança é prioridade absoluta.
              </p>
            </motion.div>
          )}
        </motion.div>
      )}

      {/* Botões de ação */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="flex flex-col sm:flex-row gap-4"
      >
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={resetGame}
          className="btn-primary flex-1 flex items-center justify-center gap-2"
        >
          <RotateCcw className="w-5 h-5" />
          Jogar Novamente
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={resetGame}
          className="btn-secondary flex-1 flex items-center justify-center gap-2"
        >
          <Home className="w-5 h-5" />
          Menu Principal
        </motion.button>
      </motion.div>

      {/* Info do projeto */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="text-center text-earth-600 text-xs mt-6"
      >
        Sistema de detecção de javalis (Sus scrofa) via visão computacional
        <br />
        UFSC - Tópicos Avançados em Inteligência Artificial
      </motion.p>
    </motion.div>
  )
}

function StatRow({ 
  label, 
  value, 
  positive = false, 
  danger = false 
}: { 
  label: string
  value: string | number
  positive?: boolean
  danger?: boolean
}) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-earth-400 text-sm">{label}</span>
      <span className={`font-mono font-bold ${
        danger 
          ? 'text-danger-400' 
          : positive 
            ? 'text-forest-400' 
            : 'text-white'
      }`}>
        {value}
      </span>
    </div>
  )
}

