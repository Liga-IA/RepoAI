'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Target, Brain, Crosshair, Trophy, Info, Play, Zap } from 'lucide-react'
import { useGameStore } from '@/store/gameStore'
import DualArena from '@/components/game/DualArena'
import GameResults from '@/components/game/GameResults'
import HowToPlay from '@/components/ui/HowToPlay'
import CustomCursor from '@/components/ui/CustomCursor'

export default function Home() {
  // Usa o store completo para garantir reatividade
  const { 
    gameStatus, 
    startGame, 
    setPlayerName 
  } = useGameStore()
  
  const [showHowToPlay, setShowHowToPlay] = useState(false)
  const [nameInput, setNameInput] = useState('')

  // Debug: monitora mudanças no gameStatus
  useEffect(() => {
    console.log('📊 gameStatus mudou para:', gameStatus)
  }, [gameStatus])

  const handleStartGame = () => {
    console.log('🚀 Iniciando jogo...', { nameInput, gameStatus })
    try {
      if (nameInput.trim()) {
        setPlayerName(nameInput.trim())
      }
      console.log('📞 Chamando startGame()...')
      startGame()
      console.log('✅ startGame() executado')
    } catch (error) {
      console.error('❌ Erro ao iniciar jogo:', error)
    }
  }

  return (
    <>
      {/* <CustomCursor /> */}
      
      <main className="relative min-h-screen z-10 bg-forest-950" style={{ minHeight: '100vh', backgroundColor: '#0a1a0f' }}>
        <AnimatePresence mode="wait">
          {gameStatus === 'idle' && (
            <motion.div
              key="menu"
              initial={false}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, y: -20 }}
              className="min-h-screen flex flex-col items-center justify-center p-8 text-white relative z-10"
              style={{ opacity: 1 }}
            >
              {/* Logo e Título */}
              <motion.div
                initial={false}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2, type: 'spring' }}
                className="text-center mb-12"
                style={{ opacity: 1 }}
              >
                <div className="flex items-center justify-center gap-4 mb-4">
                  <motion.div
                    animate={{ rotate: [0, -10, 10, 0] }}
                    transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
                  >
                    <Target className="w-16 h-16 text-forest-400" />
                  </motion.div>
                  <h1 className="font-display text-7xl md:text-8xl text-white tracking-wider">
                    JAVALI
                    <span className="text-forest-400"> HUNTER</span>
                  </h1>
                  <motion.div
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    <Crosshair className="w-16 h-16 text-danger-400" />
                  </motion.div>
                </div>
                
                <motion.p
                  initial={false}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                  className="text-earth-300 text-xl max-w-2xl mx-auto"
                  style={{ opacity: 1 }}
                >
                  Teste suas habilidades contra uma IA de visão computacional.
                  Quem consegue identificar mais javalis? 🐗
                </motion.p>
              </motion.div>

              {/* Card principal */}
              <motion.div
                initial={false}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.4, type: 'spring' }}
                className="card-glow p-8 w-full max-w-lg"
                style={{ opacity: 1 }}
              >
                {/* VS Display */}
                <div className="flex items-center justify-center gap-8 mb-8">
                  <div className="flex flex-col items-center">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-forest-600 to-forest-800 
                                    flex items-center justify-center border-2 border-forest-500 shadow-lg">
                      <span className="text-4xl">🧑</span>
                    </div>
                    <span className="mt-2 text-earth-300 font-medium">VOCÊ</span>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <motion.span 
                      className="text-5xl font-display text-warning-400"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1, repeat: Infinity }}
                    >
                      VS
                    </motion.span>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-danger-600 to-danger-800 
                                    flex items-center justify-center border-2 border-danger-500 shadow-lg">
                      <Brain className="w-10 h-10 text-white" />
                    </div>
                    <span className="mt-2 text-earth-300 font-medium">IA</span>
                  </div>
                </div>

                {/* Input de nome */}
                <div className="mb-6">
                  <label className="block text-earth-400 text-sm mb-2 uppercase tracking-wider">
                    Seu nome de caçador
                  </label>
                  <input
                    type="text"
                    value={nameInput}
                    onChange={(e) => setNameInput(e.target.value)}
                    placeholder="Digite seu nome..."
                    className="w-full px-4 py-3 bg-earth-900/50 border border-earth-700 rounded-lg
                             text-white placeholder-earth-500 focus:border-forest-500 
                             focus:ring-2 focus:ring-forest-500/30 transition-all outline-none"
                    maxLength={20}
                  />
                </div>

                {/* Botões */}
                <div className="space-y-4">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={(e) => {
                      e.preventDefault()
                      e.stopPropagation()
                      console.log('🔘 Botão clicado!')
                      handleStartGame()
                    }}
                    className="btn-primary w-full flex items-center justify-center gap-3"
                    type="button"
                  >
                    <Play className="w-6 h-6" />
                    INICIAR CAÇADA
                  </motion.button>

                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setShowHowToPlay(true)}
                    className="btn-secondary w-full flex items-center justify-center gap-2"
                  >
                    <Info className="w-5 h-5" />
                    Como Jogar
                  </motion.button>
                </div>
              </motion.div>

              {/* Features */}
              <motion.div
                initial={false}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 max-w-4xl w-full"
                style={{ opacity: 1 }}
              >
                <FeatureCard
                  icon={<Target className="w-8 h-8 text-forest-400" />}
                  title="Detecção em Tempo Real"
                  description="IA analisa imagens usando YOLOv8 para identificar javalis"
                />
                <FeatureCard
                  icon={<Zap className="w-8 h-8 text-warning-400" />}
                  title="Competição Intensa"
                  description="Veja quem é mais rápido e preciso: você ou a máquina"
                />
                <FeatureCard
                  icon={<Brain className="w-8 h-8 text-danger-400" />}
                  title="IA Adaptativa"
                  description="A IA aprende com seus acertos e erros para melhorar"
                />
              </motion.div>

              {/* Footer */}
              <motion.footer
                initial={false}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="mt-16 text-center text-earth-500 text-sm"
                style={{ opacity: 1 }}
              >
                <p>Desenvolvido para detecção de espécies invasoras (Sus scrofa)</p>
                <p className="mt-1">UFSC - Tópicos Avançados em IA</p>
              </motion.footer>
            </motion.div>
          )}

          {gameStatus === 'playing' && (
            <motion.div
              key="game"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="min-h-screen"
            >
              <div className="container mx-auto px-4 py-6 max-w-7xl">
                <DualArena />
              </div>
            </motion.div>
          )}

          {gameStatus === 'finished' && (
            <motion.div
              key="results"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="min-h-screen flex items-center justify-center p-8"
            >
              <GameResults />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Modal Como Jogar */}
        <AnimatePresence>
          {showHowToPlay && (
            <HowToPlay onClose={() => setShowHowToPlay(false)} />
          )}
        </AnimatePresence>
      </main>
    </>
  )
}

function FeatureCard({ 
  icon, 
  title, 
  description 
}: { 
  icon: React.ReactNode
  title: string
  description: string 
}) {
  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="card p-6 text-center"
    >
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-white font-semibold mb-2">{title}</h3>
      <p className="text-earth-400 text-sm">{description}</p>
    </motion.div>
  )
}

