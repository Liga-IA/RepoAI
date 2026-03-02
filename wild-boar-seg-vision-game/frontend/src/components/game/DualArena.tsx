'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useGameStore, Detection, SegmentationPoint } from '@/store/gameStore'
import { Loader2, Timer, User, Brain, Target, Crosshair, AlertTriangle } from 'lucide-react'
import { AIDetectionOverlay } from './SegmentationOverlay'
import api from '@/services/api'
import { AI_CONFIG, COUNTDOWN_SECONDS } from '@/constants'

interface ArenaProps {
  isPlayer: boolean
  image: string | null
  detections: Detection[]
  onImageClick?: (x: number, y: number) => void
  hitMarkers: Array<{ id: string; x: number; y: number; success: boolean; points: number }>
  score: number
  hits: number
  misses: number
  humanHits: number
  showDetections: boolean
  showSegmentation: boolean // Mostrar contornos de segmentação da IA
  aiTargets?: Array<{ x: number; y: number; active: boolean }>
}

// Componente de Arena Individual (uma para cada competidor)
function SingleArena({
  isPlayer,
  image,
  detections,
  onImageClick,
  hitMarkers,
  score,
  hits,
  misses,
  humanHits,
  showDetections,
  showSegmentation,
  aiTargets = [],
}: ArenaProps) {
  const arenaRef = useRef<HTMLDivElement>(null)

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isPlayer || !onImageClick) return
    
    const rect = arenaRef.current?.getBoundingClientRect()
    if (!rect) return

    const x = (e.clientX - rect.left) / rect.width
    const y = (e.clientY - rect.top) / rect.height
    
    onImageClick(x, y)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header do competidor */}
      <div className={`flex items-center justify-between p-3 rounded-t-xl ${
        isPlayer 
          ? 'bg-gradient-to-r from-forest-800 to-forest-900' 
          : 'bg-gradient-to-r from-danger-900 to-danger-950'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
            isPlayer 
              ? 'bg-forest-600' 
              : 'bg-danger-600'
          }`}>
            {isPlayer ? <User className="w-5 h-5 text-white" /> : <Brain className="w-5 h-5 text-white" />}
          </div>
          <div>
            <p className="text-white font-semibold">
              {isPlayer ? 'VOCÊ' : 'INTELIGÊNCIA ARTIFICIAL'}
            </p>
            <p className="text-xs text-gray-400">
              {isPlayer ? 'Clique nos javalis!' : 'YOLOv8 Bot'}
            </p>
          </div>
        </div>
        
        <div className="text-right">
          <p className={`text-3xl font-display ${
            isPlayer ? 'text-forest-400' : 'text-danger-400'
          }`}>
            {score}
          </p>
          <p className="text-xs text-gray-400">pontos</p>
        </div>
      </div>

      {/* Área da imagem */}
      <div
        ref={arenaRef}
        onClick={handleClick}
        className={`relative flex-1 overflow-hidden ${
          isPlayer ? 'cursor-crosshair' : 'cursor-default'
        }`}
        style={{ minHeight: '300px' }}
      >
        {/* Imagem */}
        {image ? (
          <img
            src={image.startsWith('data:') ? image : `data:image/jpeg;base64,${image}`}
            alt={`Área de ${isPlayer ? 'caça' : 'análise'}`}
            className="w-full h-full object-cover"
            draggable={false}
          />
        ) : (
          <div className="w-full h-full bg-earth-900 flex items-center justify-center">
            <Loader2 className="w-8 h-8 text-gray-500 animate-spin" />
          </div>
        )}

        {/* Overlay de detecções (apenas debug) */}
        {showDetections && detections.map((detection, index) => (
          <DetectionOverlay key={index} detection={detection} />
        ))}

        {/* Contornos de segmentação da IA - sempre visível na arena da IA */}
        {!isPlayer && showSegmentation && (
          <AIDetectionOverlay 
            detections={detections} 
            showLabels={true}
            animate={true}
          />
        )}

        {/* Hit markers do jogador */}
        {isPlayer && (
          <AnimatePresence>
            {hitMarkers.map((marker) => (
              <HitMarker key={marker.id} {...marker} />
            ))}
          </AnimatePresence>
        )}

        {/* Mira da IA */}
        {!isPlayer && (
          <AnimatePresence>
            {aiTargets.filter(t => t.active).map((target, index) => (
              <AITargetMarker key={index} x={target.x} y={target.y} />
            ))}
          </AnimatePresence>
        )}

        {/* Label do competidor */}
        <div className={`absolute top-2 left-2 px-2 py-1 rounded text-xs font-bold ${
          isPlayer 
            ? 'bg-forest-600 text-white' 
            : 'bg-danger-600 text-white'
        }`}>
          {isPlayer ? '🎯 JOGADOR' : '🤖 IA'}
        </div>
      </div>

      {/* Stats do competidor */}
      <div className={`grid grid-cols-3 gap-2 p-3 rounded-b-xl ${
        isPlayer 
          ? 'bg-forest-950/50' 
          : 'bg-danger-950/50'
      }`}>
        <StatBox 
          icon={<Target className="w-4 h-4" />} 
          value={hits} 
          label="Acertos" 
          color="green" 
        />
        <StatBox 
          icon={<Crosshair className="w-4 h-4" />} 
          value={misses} 
          label="Erros" 
          color="yellow" 
        />
        <StatBox 
          icon={<AlertTriangle className="w-4 h-4" />} 
          value={humanHits} 
          label="Humanos" 
          color="red" 
        />
      </div>
    </div>
  )
}

// Componente de estatística
function StatBox({ 
  icon, 
  value, 
  label, 
  color 
}: { 
  icon: React.ReactNode
  value: number
  label: string
  color: 'green' | 'yellow' | 'red'
}) {
  const colors = {
    green: 'text-forest-400',
    yellow: 'text-warning-400',
    red: 'text-danger-400',
  }

  return (
    <div className="bg-earth-900/50 rounded px-2 py-1.5 text-center">
      <div className={`flex items-center justify-center gap-1 ${colors[color]}`}>
        {icon}
        <span className="font-mono text-lg font-bold">{value}</span>
      </div>
      <span className="text-earth-500 text-[10px] uppercase">{label}</span>
    </div>
  )
}

// Overlay de detecção
function DetectionOverlay({ detection }: { detection: Detection }) {
  const { bbox, class_name, confidence, is_target } = detection
  
  const colorClass = is_target 
    ? 'border-forest-400 bg-forest-400/10' 
    : class_name === 'human' 
      ? 'border-danger-500 bg-danger-500/10' 
      : 'border-warning-400 bg-warning-400/10'

  return (
    <div
      className={`absolute border-2 rounded ${colorClass}`}
      style={{
        left: `${(bbox.x - bbox.width / 2) * 100}%`,
        top: `${(bbox.y - bbox.height / 2) * 100}%`,
        width: `${bbox.width * 100}%`,
        height: `${bbox.height * 100}%`,
      }}
    >
      <span className={`absolute -top-5 left-0 px-1 text-[10px] font-bold rounded ${
        is_target ? 'bg-forest-600' : class_name === 'human' ? 'bg-danger-600' : 'bg-warning-500'
      } text-white`}>
        {class_name} ({(confidence * 100).toFixed(0)}%)
      </span>
    </div>
  )
}

// Marcador de hit
function HitMarker({ x, y, success, points }: { x: number; y: number; success: boolean; points: number }) {
  return (
    <motion.div
      initial={{ scale: 0, opacity: 1 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      className="absolute pointer-events-none"
      style={{
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: 'translate(-50%, -50%)',
      }}
    >
      {/* Marcador X ou ✓ */}
      <div className={`w-8 h-8 flex items-center justify-center ${
        success ? 'text-forest-400' : 'text-danger-400'
      }`}>
        {success ? (
          <svg viewBox="0 0 24 24" className="w-full h-full">
            <path
              fill="currentColor"
              d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"
            />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" className="w-full h-full">
            <path
              fill="currentColor"
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"
            />
          </svg>
        )}
      </div>

      {/* Pontos flutuantes */}
      <motion.div
        initial={{ y: 0, opacity: 1 }}
        animate={{ y: -40, opacity: 0 }}
        transition={{ duration: 0.8 }}
        className={`absolute top-0 left-1/2 -translate-x-1/2 font-display text-lg font-bold whitespace-nowrap ${
          points > 0 ? 'text-forest-400' : points < 0 ? 'text-danger-400' : 'text-gray-400'
        }`}
      >
        {points > 0 ? '+' : ''}{points}
      </motion.div>
    </motion.div>
  )
}

// Marcador de mira da IA
function AITargetMarker({ x, y }: { x: number; y: number }) {
  return (
    <motion.div
      initial={{ scale: 2, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.5, opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="absolute pointer-events-none"
      style={{
        left: `${x * 100}%`,
        top: `${y * 100}%`,
        transform: 'translate(-50%, -50%)',
      }}
    >
      <div className="w-12 h-12 relative">
        {/* Círculo externo pulsante */}
        <motion.div
          className="absolute inset-0 border-2 border-danger-400 rounded-full"
          animate={{ scale: [1, 1.2, 1], opacity: [1, 0.5, 1] }}
          transition={{ duration: 0.5, repeat: 2 }}
        />
        
        {/* Cruz central */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-full h-0.5 bg-danger-400" />
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-full w-0.5 bg-danger-400" />
        </div>
        
        {/* Ponto central */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-danger-500 rounded-full" />
      </div>
    </motion.div>
  )
}

// Componente principal com duas arenas
export default function DualArena() {
  const {
    currentRound,
    totalRounds,
    roundTimeLeft,
    roundDuration,
    currentImage,
    detections,
    hitMarkers,
    showDetections,
    playerScore,
    playerHits,
    playerMisses,
    playerHumanHits,
    aiScore,
    aiHits,
    aiMisses,
    aiHumanHits,
    setCurrentImage,
    setDetections,
    registerPlayerHit,
    registerAIHit,
    updateTime,
    nextRound,
    endGame,
  } = useGameStore()

  const [loading, setLoading] = useState(true)
  const [countdown, setCountdown] = useState(3)
  const [roundStarted, setRoundStarted] = useState(false)
  const [aiTargets, setAiTargets] = useState<Array<{ x: number; y: number; active: boolean }>>([])
  const [apiError, setApiError] = useState<string | null>(null)
  
  const timerRef = useRef<NodeJS.Timeout | null>(null)
  const roundEndingRef = useRef(false) // Previne múltiplas chamadas de handleRoundEnd

  // Carrega imagem da rodada do dataset Agriculture via API
  const loadRoundImage = useCallback(async () => {
    setLoading(true)
    setRoundStarted(false)
    setCountdown(COUNTDOWN_SECONDS)
    setAiTargets([])
    setApiError(null)
    roundEndingRef.current = false // Reset flag
    
    try {
      // Busca imagem aleatória do dataset Agriculture já analisada
      const result = await api.getRandomAnalyzedImage('test')
      
      // Define a imagem (será prefixada com data:image/jpeg;base64, no render)
      setCurrentImage(result.image_base64)
      
      // Converte detecções da API para o formato do store
      const gameDetections: Detection[] = result.analysis.detections.map(d => ({
        class_name: d.class_name === 'boar' || d.class_name === 'wild-boar' ? 'boar' : 
                   d.class_name === 'person' ? 'human' : 'other',
        confidence: d.confidence,
        bbox: d.bbox,
        is_target: d.is_target,
        segmentation: d.segmentation,
      }))
      
      setDetections(gameDetections)
      console.log(`🖼️ Imagem ${result.filename}: ${gameDetections.length} detecções`)
      
    } catch (error) {
      console.error('Erro ao carregar imagem do dataset Agriculture:', error)
      setApiError('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
      setCurrentImage('')
      setDetections([])
    } finally {
      setLoading(false)
    }
  }, [currentRound, setCurrentImage, setDetections])

  // Countdown inicial
  useEffect(() => {
    if (!loading && countdown > 0) {
      const timer = setTimeout(() => setCountdown(c => c - 1), 1000)
      return () => clearTimeout(timer)
    }
    if (countdown === 0 && !roundStarted) {
      setRoundStarted(true)
    }
  }, [loading, countdown, roundStarted])

  // Timer da rodada - usando useRef para evitar problemas de closure
  useEffect(() => {
    if (!roundStarted) return
    
    const startTime = Date.now()
    const initialTime = roundTimeLeft
    
    timerRef.current = setInterval(() => {
      const elapsed = (Date.now() - startTime) / 1000
      const newTime = Math.max(0, initialTime - elapsed)
      updateTime(newTime)
      
      // Verifica fim do tempo
      if (newTime <= 0 && !roundEndingRef.current) {
        roundEndingRef.current = true
        if (timerRef.current) {
          clearInterval(timerRef.current)
          timerRef.current = null
        }
        handleRoundEnd()
      }
    }, 100)
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
        timerRef.current = null
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roundStarted])

  // Carrega imagem quando rodada muda
  useEffect(() => {
    loadRoundImage()
  }, [currentRound, loadRoundImage])

  // IA joga automaticamente
  useEffect(() => {
    if (!roundStarted || detections.length === 0) return

    detections.forEach((detection, index) => {
      // IA decide se vai "clicar" baseado nas configurações
      const shouldClick = detection.is_target 
        ? Math.random() < AI_CONFIG.BOAR_HIT_CHANCE
        : detection.class_name === 'human'
          ? Math.random() < AI_CONFIG.HUMAN_HIT_CHANCE
          : Math.random() < AI_CONFIG.OTHER_HIT_CHANCE

      if (shouldClick) {
        const delay = AI_CONFIG.BASE_REACTION_TIME + Math.random() * AI_CONFIG.REACTION_VARIANCE + index * 500
        
        setTimeout(() => {
          if (useGameStore.getState().roundTimeLeft > 0) {
            // Mostra mira da IA
            setAiTargets(prev => [...prev, { x: detection.bbox.x, y: detection.bbox.y, active: true }])
            
            setTimeout(() => {
              registerAIHit(detection)
              setAiTargets(prev => prev.map(t => 
                t.x === detection.bbox.x && t.y === detection.bbox.y 
                  ? { ...t, active: false } 
                  : t
              ))
            }, 500)
          }
        }, delay)
      }
    })
  }, [roundStarted, detections, registerAIHit])

  // Handler de clique do jogador
  const handlePlayerClick = (x: number, y: number) => {
    if (!roundStarted || roundTimeLeft <= 0) return

    const hitDetection = detections.find(d => {
      const bbox = d.bbox
      const tolerance = 0.04
      return x >= bbox.x - bbox.width/2 - tolerance && 
             x <= bbox.x + bbox.width/2 + tolerance &&
             y >= bbox.y - bbox.height/2 - tolerance && 
             y <= bbox.y + bbox.height/2 + tolerance
    })

    registerPlayerHit(hitDetection || null, x, y)
  }

  // Finaliza rodada
  const handleRoundEnd = useCallback(() => {
    if (roundEndingRef.current && !roundStarted) return // Já está finalizando
    
    roundEndingRef.current = true
    setRoundStarted(false)
    
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
    
    console.log(`🏁 Rodada ${currentRound}/${totalRounds} finalizada`)
    
    if (currentRound >= totalRounds) {
      console.log('🎮 Jogo finalizado!')
      endGame()
    } else {
      // Aguarda um momento antes de ir para próxima rodada
      setTimeout(() => {
        nextRound()
      }, 1500)
    }
  }, [currentRound, totalRounds, endGame, nextRound, roundStarted])

  const timePercentage = (roundTimeLeft / roundDuration) * 100

  return (
    <div className="space-y-4">
      {/* Header da rodada */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="text-earth-400 text-sm uppercase tracking-wider">Rodada</span>
          <span className="font-display text-3xl text-white">{currentRound}/{totalRounds}</span>
        </div>

        <div className="flex items-center gap-4">
          <Timer className="w-5 h-5 text-earth-400" />
          <span className={`font-mono text-2xl font-bold ${
            roundTimeLeft <= 5 ? 'text-danger-400 animate-pulse' : 'text-white'
          }`}>
            {roundTimeLeft.toFixed(1)}s
          </span>
        </div>
      </div>

      {/* Barra de tempo */}
      <div className="h-2 rounded-full bg-earth-900 overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          style={{
            width: `${timePercentage}%`,
            background: timePercentage > 60 ? '#22c55e' : timePercentage > 30 ? '#f59e0b' : '#ef4444'
          }}
        />
      </div>

      {/* Overlay de Loading/Countdown */}
      <AnimatePresence>
        {(loading || countdown > 0) && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
          >
            {loading ? (
              <div className="text-center">
                <Loader2 className="w-16 h-16 text-forest-400 animate-spin mx-auto mb-4" />
                <p className="text-earth-300 text-xl">Carregando imagem...</p>
              </div>
            ) : (
              <motion.div
                key={countdown}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 2, opacity: 0 }}
                className="text-center"
              >
                <span className="font-display text-9xl text-forest-400">{countdown}</span>
                <p className="text-earth-300 text-xl mt-4">Prepare-se!</p>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Duas arenas lado a lado */}
      <div className="grid grid-cols-2 gap-4">
        {/* Arena do Jogador */}
        <div className="card overflow-hidden">
          <SingleArena
            isPlayer={true}
            image={currentImage}
            detections={detections}
            onImageClick={handlePlayerClick}
            hitMarkers={hitMarkers}
            score={playerScore}
            hits={playerHits}
            misses={playerMisses}
            humanHits={playerHumanHits}
            showDetections={showDetections}
            showSegmentation={false}
          />
        </div>

        {/* Arena da IA */}
        <div className="card overflow-hidden">
          <SingleArena
            isPlayer={false}
            image={currentImage}
            detections={detections}
            hitMarkers={[]}
            score={aiScore}
            hits={aiHits}
            misses={aiMisses}
            humanHits={aiHumanHits}
            showDetections={showDetections}
            showSegmentation={true}
            aiTargets={aiTargets}
          />
        </div>
      </div>

      {/* Legenda */}
      <div className="flex items-center justify-center gap-8 text-sm">
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

