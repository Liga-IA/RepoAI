'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useGameStore, Detection } from '@/store/gameStore'
import { api } from '@/services/api'
import { Loader2, AlertTriangle, Timer, Crosshair } from 'lucide-react'

export default function GameArena() {
  const {
    currentRound,
    totalRounds,
    roundTimeLeft,
    roundDuration,
    currentImage,
    detections,
    hitMarkers,
    showDetections,
    revealedDetections,
    setCurrentImage,
    setDetections,
    registerPlayerHit,
    registerAIHit,
    updateTime,
    nextRound,
    endGame,
  } = useGameStore()

  const [loading, setLoading] = useState(true)
  const [aiThinking, setAiThinking] = useState(false)
  const [roundStarted, setRoundStarted] = useState(false)
  const [countdown, setCountdown] = useState(3)
  
  const arenaRef = useRef<HTMLDivElement>(null)
  const timerRef = useRef<NodeJS.Timeout | null>(null)
  const aiTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Seed para geração de imagem (baseado na rodada e timestamp)
  const [imageSeed, setImageSeed] = useState(Date.now())
  const [imageBase64, setImageBase64] = useState<string | null>(null)
  const [imageFilename, setImageFilename] = useState<string>('')
  const [apiError, setApiError] = useState<string | null>(null)

  // Carrega nova imagem para a rodada do dataset Agriculture
  const loadRoundImage = useCallback(async () => {
    setLoading(true)
    setRoundStarted(false)
    setCountdown(3)
    setApiError(null)
    
    try {
      // Busca imagem aleatória do dataset Agriculture já analisada
      const result = await api.getRandomAnalyzedImage('test')
      
      setImageFilename(result.filename)
      setImageBase64(result.image_base64)
      setCurrentImage(result.filename)
      
      // Converte detecções da API para o formato do store
      const gameDetections: Detection[] = result.analysis.detections.map(d => ({
        class_name: d.animal_class === 'boar' ? 'boar' : 
                   d.animal_class === 'human' ? 'human' : 'other',
        confidence: d.confidence,
        bbox: {
          x: (d.bounding_box.x_min + d.bounding_box.x_max) / 2,
          y: (d.bounding_box.y_min + d.bounding_box.y_max) / 2,
          width: d.bounding_box.x_max - d.bounding_box.x_min,
          height: d.bounding_box.y_max - d.bounding_box.y_min,
        },
        is_target: d.animal_class === 'boar',
        segmentation: d.segmentation,
      }))
      
      setDetections(gameDetections)
      console.log(`🖼️ Imagem ${result.filename}: ${gameDetections.length} detecções`)
      
    } catch (error) {
      console.error('Erro ao carregar imagem do dataset Agriculture:', error)
      setApiError('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
      setImageBase64(null)
      setDetections([])
    } finally {
      setLoading(false)
    }
  }, [currentRound, setCurrentImage, setDetections])

  // Inicia rodada após countdown
  useEffect(() => {
    if (!loading && countdown > 0) {
      const timer = setTimeout(() => {
        setCountdown(c => c - 1)
      }, 1000)
      return () => clearTimeout(timer)
    }
    
    if (countdown === 0 && !roundStarted) {
      setRoundStarted(true)
    }
  }, [loading, countdown, roundStarted])

  // Timer da rodada
  useEffect(() => {
    if (!roundStarted) return

    timerRef.current = setInterval(() => {
      updateTime(roundTimeLeft - 0.1)
    }, 100)

    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [roundStarted, roundTimeLeft, updateTime])

  // Verifica fim do tempo
  useEffect(() => {
    if (roundTimeLeft <= 0 && roundStarted) {
      handleRoundEnd()
    }
  }, [roundTimeLeft, roundStarted])

  // Carrega imagem quando rodada muda
  useEffect(() => {
    loadRoundImage()
  }, [currentRound, loadRoundImage])

  // IA joga automaticamente
  useEffect(() => {
    if (!roundStarted || detections.length === 0) return

    // IA "pensa" e clica com delay variável
    detections.forEach((detection, index) => {
      if (detection.is_target || Math.random() < 0.2) {
        // Delay baseado na confiança e posição
        const baseDelay = 1500 + Math.random() * 2000
        const confidenceBonus = (1 - detection.confidence) * 1000
        const delay = baseDelay + confidenceBonus + index * 500

        aiTimerRef.current = setTimeout(() => {
          if (useGameStore.getState().roundTimeLeft > 0) {
            setAiThinking(true)
            
            setTimeout(() => {
              registerAIHit(detection)
              setAiThinking(false)
            }, 300)
          }
        }, delay)
      }
    })

    return () => {
      if (aiTimerRef.current) clearTimeout(aiTimerRef.current)
    }
  }, [roundStarted, detections, registerAIHit])

  // Handler de clique do jogador
  const handleArenaClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!roundStarted || roundTimeLeft <= 0) return

    const rect = arenaRef.current?.getBoundingClientRect()
    if (!rect) return

    const x = (e.clientX - rect.left) / rect.width
    const y = (e.clientY - rect.top) / rect.height

    // Verifica se clicou em alguma detecção
    const hitDetection = detections.find(d => {
      const bbox = d.bbox
      const left = bbox.x - bbox.width / 2
      const right = bbox.x + bbox.width / 2
      const top = bbox.y - bbox.height / 2
      const bottom = bbox.y + bbox.height / 2
      
      const tolerance = 0.03
      return x >= left - tolerance && x <= right + tolerance &&
             y >= top - tolerance && y <= bottom + tolerance
    })

    registerPlayerHit(hitDetection || null, x, y)
  }

  // Finaliza rodada
  const handleRoundEnd = () => {
    setRoundStarted(false)
    
    if (currentRound >= totalRounds) {
      endGame()
    } else {
      // Pequeno delay antes da próxima rodada
      setTimeout(() => {
        nextRound()
      }, 1500)
    }
  }

  // Pula para próxima rodada
  const handleSkipRound = () => {
    if (timerRef.current) clearInterval(timerRef.current)
    handleRoundEnd()
  }

  const timePercentage = (roundTimeLeft / roundDuration) * 100

  return (
    <div className="mt-6">
      {/* Header da rodada */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4">
          <span className="text-earth-400 text-sm uppercase tracking-wider">
            Rodada
          </span>
          <span className="font-display text-3xl text-white">
            {currentRound}/{totalRounds}
          </span>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Timer className="w-5 h-5 text-earth-400" />
            <span className={`font-mono text-2xl font-bold ${
              roundTimeLeft <= 5 ? 'text-danger-400 animate-pulse' : 'text-white'
            }`}>
              {roundTimeLeft.toFixed(1)}s
            </span>
          </div>
          
          <button
            onClick={handleSkipRound}
            className="btn-secondary text-sm"
            disabled={!roundStarted}
          >
            Pular Rodada
          </button>
        </div>
      </div>

      {/* Barra de tempo */}
      <div className="time-bar mb-4">
        <motion.div
          className="time-bar-fill"
          initial={{ width: '100%' }}
          animate={{ width: `${timePercentage}%` }}
          transition={{ duration: 0.1 }}
          style={{
            background: timePercentage > 60 
              ? '#22c55e' 
              : timePercentage > 30 
                ? '#f59e0b' 
                : '#ef4444'
          }}
        />
      </div>

      {/* Arena de jogo */}
      <div
        ref={arenaRef}
        onClick={handleArenaClick}
        className="target-area relative"
      >
        {/* Loading */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 flex items-center justify-center bg-earth-950/90 z-30"
            >
              <div className="text-center">
                <Loader2 className="w-12 h-12 text-forest-400 animate-spin mx-auto mb-4" />
                <p className="text-earth-300">Carregando imagem...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Countdown */}
        <AnimatePresence>
          {!loading && countdown > 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.5 }}
              className="absolute inset-0 flex items-center justify-center bg-earth-950/80 z-20"
            >
              <motion.div
                key={countdown}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 2, opacity: 0 }}
                className="text-center"
              >
                <span className="font-display text-9xl text-forest-400">
                  {countdown}
                </span>
                <p className="text-earth-300 text-xl mt-4">Prepare-se!</p>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Erro de conexão com API */}
        {apiError && (
          <div className="absolute inset-0 flex items-center justify-center bg-earth-950/90 z-30">
            <div className="text-center p-8 bg-earth-900 rounded-lg border border-danger-500/50 max-w-md">
              <AlertTriangle className="w-16 h-16 text-danger-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-danger-400 mb-2">Erro de Conexão</h3>
              <p className="text-earth-300 mb-4">{apiError}</p>
              <button
                onClick={loadRoundImage}
                className="px-6 py-2 bg-forest-600 hover:bg-forest-500 text-white rounded-lg transition-colors"
              >
                Tentar Novamente
              </button>
            </div>
          </div>
        )}

        {/* Imagem do dataset Agriculture */}
        {imageBase64 && (
          <img 
            src={`data:image/jpeg;base64,${imageBase64}`}
            alt={`Imagem ${imageFilename}`}
            className="w-full h-full object-cover"
            draggable={false}
          />
        )}

        {/* Overlay de segmentação para detecções */}
        {detections.map((detection, index) => {
          if (!detection.segmentation || detection.segmentation.length < 3) return null
          
          return (
            <svg
              key={`seg-${index}`}
              className="absolute inset-0 w-full h-full pointer-events-none z-5"
              viewBox="0 0 100 100"
              preserveAspectRatio="none"
            >
              <polygon
                points={detection.segmentation.map(p => `${p.x * 100},${p.y * 100}`).join(' ')}
                fill={detection.is_target ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)'}
                stroke={detection.is_target ? '#22c55e' : '#ef4444'}
                strokeWidth="0.3"
                strokeDasharray={detection.is_target ? '0' : '2,2'}
              />
            </svg>
          )
        })}

        {/* Bounding boxes (debug ou após acerto) */}
        {(showDetections || revealedDetections.length > 0) && detections.map((detection, index) => {
          const isRevealed = revealedDetections.includes(
            `${detection.bbox.x}-${detection.bbox.y}`
          )
          
          if (!showDetections && !isRevealed) return null
          
          return (
            <DetectionBox key={index} detection={detection} revealed={isRevealed} />
          )
        })}

        {/* Hit markers */}
        <AnimatePresence>
          {hitMarkers.map((marker) => (
            <motion.div
              key={marker.id}
              initial={{ scale: 0, opacity: 1 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              style={{
                left: `${marker.x * 100}%`,
                top: `${marker.y * 100}%`,
              }}
              className="absolute pointer-events-none z-20"
            >
              <div className={`hit-marker ${marker.success ? 'success' : 'fail'} animate-hit-marker`} />
              
              {/* Pontos flutuantes */}
              <motion.div
                initial={{ y: 0, opacity: 1 }}
                animate={{ y: -60, opacity: 0 }}
                transition={{ duration: 1 }}
                className={`absolute left-1/2 -translate-x-1/2 font-display text-2xl font-bold whitespace-nowrap ${
                  marker.points > 0 
                    ? 'text-forest-400' 
                    : marker.points < 0 
                      ? 'text-danger-400' 
                      : 'text-earth-400'
                }`}
              >
                {marker.points > 0 ? '+' : ''}{marker.points}
              </motion.div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Indicador IA pensando */}
        <AnimatePresence>
          {aiThinking && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="absolute top-4 right-4 bg-danger-600/90 px-4 py-2 rounded-lg flex items-center gap-2 z-20"
            >
              <Crosshair className="w-5 h-5 text-white animate-pulse" />
              <span className="text-white font-medium">IA Mirando...</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Overlay de fim de rodada */}
        <AnimatePresence>
          {roundTimeLeft <= 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="absolute inset-0 bg-earth-950/80 flex items-center justify-center z-30"
            >
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring' }}
                >
                  <h2 className="font-display text-5xl text-white mb-4">
                    TEMPO ESGOTADO!
                  </h2>
                  <p className="text-earth-300">
                    {currentRound >= totalRounds 
                      ? 'Calculando resultado final...' 
                      : 'Preparando próxima rodada...'}
                  </p>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Legenda */}
      <div className="mt-4 flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-forest-400 rounded" />
          <span className="text-earth-400">Javali (+100pts)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-warning-400 rounded" />
          <span className="text-earth-400">Outro Animal (-30pts)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-danger-500 rounded" />
          <span className="text-earth-400">Humano (-200pts)</span>
        </div>
      </div>
    </div>
  )
}

// Componente de bounding box
function DetectionBox({ detection, revealed }: { detection: Detection; revealed: boolean }) {
  const { bbox, class_name, confidence, is_target } = detection
  
  const colorClass = is_target 
    ? 'boar' 
    : class_name === 'human' 
      ? 'human' 
      : 'other'
  
  const label = {
    boar: '🐗 Javali',
    pig: '🐷 Porco',
    deer: '🦌 Veado',
    human: '⚠️ Humano',
    other: '🐾 Animal',
  }[class_name]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`detection-box ${colorClass}`}
      style={{
        left: `${(bbox.x - bbox.width / 2) * 100}%`,
        top: `${(bbox.y - bbox.height / 2) * 100}%`,
        width: `${bbox.width * 100}%`,
        height: `${bbox.height * 100}%`,
      }}
    >
      <span 
        className={`detection-label ${
          is_target 
            ? 'bg-forest-600 text-white' 
            : class_name === 'human'
              ? 'bg-danger-600 text-white'
              : 'bg-warning-500 text-earth-900'
        }`}
      >
        {label} ({(confidence * 100).toFixed(0)}%)
      </span>
    </motion.div>
  )
}

