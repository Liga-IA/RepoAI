import axios from 'axios'
import { Detection } from '@/store/gameStore'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Tipos de resposta da API
export interface ImageAnalysisResponse {
  image_id: string
  detections: Detection[]
  processing_time_ms: number
  has_boar: boolean
  boar_count: number
}

export interface GameSession {
  session_id: string
  created_at: string
  rounds_completed: number
  total_rounds: number
  player_total_score: number
  ai_total_score: number
  status: string
}

export interface ClickResult {
  hit: boolean
  target_class: string | null
  points_earned: number
  is_penalty: boolean
  message: string
}

export interface LeaderboardEntry {
  rank: number
  player_name: string
  score: number
  accuracy: number
  games_played: number
  best_streak: number
}

export interface AILearningSummary {
  global_metrics: {
    total_rounds: number
    human_correct: number
    human_wrong: number
    ai_correct: number
    ai_wrong: number
    avg_reaction_time: number
  }
  class_patterns: Record<string, {
    hits: number
    misses: number
    avg_confidence: number
  }>
  confidence_adjustments: Record<string, number>
  total_images_analyzed: number
}

// Funções da API
export const api = {
  // Health check
  async healthCheck() {
    const response = await apiClient.get('/health')
    return response.data
  },

  // Análise de imagem
  async analyzeImage(imageBase64: string): Promise<ImageAnalysisResponse> {
    const response = await apiClient.post('/detect', {
      image_base64: imageBase64,
    })
    return response.data
  },

  // Upload de arquivo para análise
  async analyzeImageFile(file: File): Promise<ImageAnalysisResponse> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await apiClient.post('/detect/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Sessão de jogo
  async startGame(playerName?: string): Promise<GameSession> {
    const response = await apiClient.post('/game/start', null, {
      params: { player_name: playerName },
    })
    return response.data
  },

  async getGameSession(sessionId: string): Promise<GameSession> {
    const response = await apiClient.get(`/game/${sessionId}`)
    return response.data
  },

  async startRound(sessionId: string, imageBase64: string) {
    const response = await apiClient.post(`/game/${sessionId}/round/start`, {
      image_base64: imageBase64,
    })
    return response.data
  },

  async processClick(
    sessionId: string,
    click: {
      x: number
      y: number
      timestamp: number
      image_id: string
      game_session_id: string
    }
  ): Promise<ClickResult> {
    const response = await apiClient.post(`/game/${sessionId}/click`, click)
    return response.data
  },

  async simulateAITurn(sessionId: string, imageId: string) {
    const response = await apiClient.post(`/game/${sessionId}/ai-turn`, null, {
      params: { image_id: imageId },
    })
    return response.data
  },

  async endRound(sessionId: string) {
    const response = await apiClient.post(`/game/${sessionId}/round/end`)
    return response.data
  },

  async endGame(sessionId: string) {
    const response = await apiClient.post(`/game/${sessionId}/end`)
    return response.data
  },

  // Leaderboard
  async getLeaderboard(limit = 10): Promise<LeaderboardEntry[]> {
    const response = await apiClient.get('/leaderboard', {
      params: { limit },
    })
    return response.data
  },

  // Aprendizado da IA
  async getLearningSummary(): Promise<AILearningSummary> {
    const response = await apiClient.get('/learning/summary')
    return response.data
  },

  async resetLearning(): Promise<{ message: string }> {
    const response = await apiClient.post('/learning/reset')
    return response.data
  },

  // ============== Imagens do Dataset Agriculture ==============
  
  // Lista imagens disponíveis
  async listImages(split: 'test' | 'valid' | 'train' = 'test', limit = 50) {
    const response = await apiClient.get('/images/list', {
      params: { split, limit },
    })
    return response.data as { split: string; count: number; images: string[] }
  },

  // Obtém imagem aleatória
  async getRandomImage(split: 'test' | 'valid' | 'train' = 'test') {
    const response = await apiClient.get('/images/random', {
      params: { split },
    })
    return response.data as { filename: string; split: string; image_base64: string }
  },

  // Obtém imagem aleatória já analisada (para o jogo)
  async getRandomAnalyzedImage(split: 'test' | 'valid' | 'train' = 'test') {
    const response = await apiClient.get('/images/random/analyzed', {
      params: { split },
    })
    return response.data as {
      filename: string
      split: string
      image_base64: string
      analysis: ImageAnalysisResponse
    }
  },

  // URL para imagem do dataset
  getImageUrl(split: string, filename: string): string {
    return `${API_BASE_URL}/images/file/${split}/${filename}`
  },
}

// Helper para converter arquivo para base64
export async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

// Helper para converter URL de imagem para base64
export async function imageUrlToBase64(url: string): Promise<string> {
  const response = await fetch(url)
  const blob = await response.blob()
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

export default api

