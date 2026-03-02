import { create } from 'zustand'
import { ROUND_DURATION, TOTAL_ROUNDS, POINTS } from '@/constants'

// Ponto de um polígono de segmentação (coordenadas normalizadas 0-1)
export interface SegmentationPoint {
  x: number
  y: number
}

export interface Detection {
  class_name: 'boar' | 'pig' | 'deer' | 'human' | 'other'
  confidence: number
  bbox: {
    x: number
    y: number
    width: number
    height: number
  }
  is_target: boolean
  // Polígono de segmentação (contorno do animal)
  segmentation?: SegmentationPoint[]
}

export interface HitMarker {
  id: string
  x: number
  y: number
  success: boolean
  points: number
  timestamp: number
}

export interface GameState {
  // Status do jogo
  gameStatus: 'idle' | 'playing' | 'finished'
  sessionId: string | null
  
  // Jogador
  playerName: string
  playerScore: number
  playerHits: number
  playerMisses: number
  playerHumanHits: number
  
  // IA
  aiScore: number
  aiHits: number
  aiMisses: number
  aiHumanHits: number
  
  // Rodada atual
  currentRound: number
  totalRounds: number
  roundTimeLeft: number
  roundDuration: number
  
  // Imagem e detecções
  currentImage: string | null
  detections: Detection[]
  revealedDetections: string[] // IDs das detecções já reveladas
  
  // Hit markers para animação
  hitMarkers: HitMarker[]
  
  // Histórico
  roundHistory: Array<{
    round: number
    playerPoints: number
    aiPoints: number
    boarsFound: number
  }>
  
  // Configurações
  showDetections: boolean // Debug: mostrar boxes de detecção
  soundEnabled: boolean
  
  // Actions
  setPlayerName: (name: string) => void
  startGame: () => void
  endGame: () => void
  resetGame: () => void
  
  setCurrentImage: (image: string) => void
  setDetections: (detections: Detection[]) => void
  
  registerPlayerHit: (detection: Detection | null, x: number, y: number) => void
  registerAIHit: (detection: Detection) => void
  
  updateTime: (time: number) => void
  nextRound: () => void
  
  addHitMarker: (marker: Omit<HitMarker, 'id' | 'timestamp'>) => void
  removeHitMarker: (id: string) => void
  
  toggleDetections: () => void
  toggleSound: () => void
}

export const useGameStore = create<GameState>((set, get) => ({
  // Estado inicial
  gameStatus: 'idle',
  sessionId: null,
  
  playerName: 'Caçador',
  playerScore: 0,
  playerHits: 0,
  playerMisses: 0,
  playerHumanHits: 0,
  
  aiScore: 0,
  aiHits: 0,
  aiMisses: 0,
  aiHumanHits: 0,
  
  currentRound: 0,
  totalRounds: TOTAL_ROUNDS,
  roundTimeLeft: ROUND_DURATION,
  roundDuration: ROUND_DURATION,
  
  currentImage: null,
  detections: [],
  revealedDetections: [],
  
  hitMarkers: [],
  roundHistory: [],
  
  showDetections: false,
  soundEnabled: true,
  
  // Actions
  setPlayerName: (name) => set({ playerName: name }),
  
  startGame: () => {
    const sessionId = `session_${Date.now()}`
    set({
      gameStatus: 'playing',
      sessionId,
      playerScore: 0,
      playerHits: 0,
      playerMisses: 0,
      playerHumanHits: 0,
      aiScore: 0,
      aiHits: 0,
      aiMisses: 0,
      aiHumanHits: 0,
      currentRound: 1,
      roundTimeLeft: ROUND_DURATION,
      roundHistory: [],
      hitMarkers: [],
      revealedDetections: [],
    })
  },
  
  endGame: () => set({ gameStatus: 'finished' }),
  
  resetGame: () => set({
    gameStatus: 'idle',
    sessionId: null,
    playerScore: 0,
    playerHits: 0,
    playerMisses: 0,
    playerHumanHits: 0,
    aiScore: 0,
    aiHits: 0,
    aiMisses: 0,
    aiHumanHits: 0,
    currentRound: 0,
    roundTimeLeft: ROUND_DURATION,
    currentImage: null,
    detections: [],
    revealedDetections: [],
    hitMarkers: [],
    roundHistory: [],
  }),
  
  setCurrentImage: (image) => set({ 
    currentImage: image,
    revealedDetections: [],
  }),
  
  setDetections: (detections) => set({ detections }),
  
  registerPlayerHit: (detection, x, y) => {
    const state = get()
    let points = POINTS.MISS
    let success = false
    
    if (detection) {
      if (detection.is_target) {
        // Acertou javali!
        points = POINTS.BOAR_HIT
        // Bônus por tempo restante (quanto mais rápido, mais pontos)
        const timeBonus = Math.floor((state.roundTimeLeft / state.roundDuration) * 50)
        points += timeBonus
        success = true
        
        set((state) => ({
          playerScore: state.playerScore + points,
          playerHits: state.playerHits + 1,
          revealedDetections: [...state.revealedDetections, `${detection.bbox.x}-${detection.bbox.y}`],
        }))
      } else if (detection.class_name === 'human') {
        // Acertou humano - penalidade severa
        points = POINTS.HUMAN_HIT
        set((state) => ({
          playerScore: state.playerScore + points,
          playerHumanHits: state.playerHumanHits + 1,
          playerMisses: state.playerMisses + 1,
        }))
      } else {
        // Acertou outro animal
        points = POINTS.WRONG_ANIMAL
        set((state) => ({
          playerScore: state.playerScore + points,
          playerMisses: state.playerMisses + 1,
        }))
      }
    } else {
      // Não acertou nada
      set((state) => ({
        playerMisses: state.playerMisses + 1,
      }))
    }
    
    // Adiciona hit marker
    get().addHitMarker({ x, y, success, points })
  },
  
  registerAIHit: (detection) => {
    let points = 0
    
    if (detection.is_target) {
      points = POINTS.BOAR_HIT
      set((state) => ({
        aiScore: state.aiScore + points,
        aiHits: state.aiHits + 1,
      }))
    } else if (detection.class_name === 'human') {
      points = POINTS.HUMAN_HIT
      set((state) => ({
        aiScore: state.aiScore + points,
        aiHumanHits: state.aiHumanHits + 1,
        aiMisses: state.aiMisses + 1,
      }))
    } else {
      points = POINTS.WRONG_ANIMAL
      set((state) => ({
        aiScore: state.aiScore + points,
        aiMisses: state.aiMisses + 1,
      }))
    }
  },
  
  updateTime: (time) => set({ roundTimeLeft: time }),
  
  nextRound: () => {
    const state = get()
    
    // Salva histórico da rodada
    const roundData = {
      round: state.currentRound,
      playerPoints: state.playerScore,
      aiPoints: state.aiScore,
      boarsFound: state.playerHits + state.aiHits,
    }
    
    if (state.currentRound >= state.totalRounds) {
      // Fim do jogo
      set((state) => ({
        gameStatus: 'finished',
        roundHistory: [...state.roundHistory, roundData],
      }))
    } else {
      // Próxima rodada
      set((state) => ({
        currentRound: state.currentRound + 1,
        roundTimeLeft: ROUND_DURATION,
        currentImage: null,
        detections: [],
        revealedDetections: [],
        hitMarkers: [],
        roundHistory: [...state.roundHistory, roundData],
      }))
    }
  },
  
  addHitMarker: (marker) => {
    const id = `hit_${Date.now()}_${Math.random()}`
    const newMarker = { ...marker, id, timestamp: Date.now() }
    
    set((state) => ({
      hitMarkers: [...state.hitMarkers, newMarker],
    }))
    
    // Remove após animação
    setTimeout(() => {
      get().removeHitMarker(id)
    }, 1000)
  },
  
  removeHitMarker: (id) => {
    set((state) => ({
      hitMarkers: state.hitMarkers.filter(m => m.id !== id),
    }))
  },
  
  toggleDetections: () => set((state) => ({ showDetections: !state.showDetections })),
  toggleSound: () => set((state) => ({ soundEnabled: !state.soundEnabled })),
}))

