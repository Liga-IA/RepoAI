/**
 * Constantes do sistema Javali Hunter - Frontend
 *
 * Este arquivo contém todas as constantes de configuração do jogo,
 * pontuação e UI. Valores que não são sensíveis e podem ser
 * versionados no repositório.
 */

// ===========================================
// Configurações do Jogo
// ===========================================
export const ROUND_DURATION = 5 // segundos por rodada
export const TOTAL_ROUNDS = 10 // número total de rodadas
export const COUNTDOWN_SECONDS = 3 // contagem regressiva antes da rodada

// ===========================================
// Sistema de Pontuação
// ===========================================
export const POINTS = {
  BOAR_HIT: 100, // Pontos por acertar javali
  WRONG_ANIMAL: -30, // Penalidade por acertar animal errado
  HUMAN_HIT: -200, // Penalidade severa por acertar humano
  MISS: 0, // Pontos por errar (clicar onde não há nada)
  SPEED_BONUS: 1.5, // multiplicador para cliques rápidos (< 3s)
} as const

// Pontuação detalhada por classe
export const POINTS_BY_CLASS = {
  boar: 100, // Javali - alvo principal
  'wild-boar': 100, // Javali selvagem - também alvo
  pig: -30, // Porco - penalidade
  deer: -30, // Veado - penalidade
  dog: -30, // Cachorro - penalidade
  monkey: -30, // Macaco - penalidade
  human: -200, // Humano - penalidade severa
  other: -10, // Outros - penalidade leve
} as const

// ===========================================
// Configurações da IA
// ===========================================
export const AI_CONFIG = {
  BASE_REACTION_TIME: 1000, // Tempo base de reação em ms
  REACTION_VARIANCE: 3000, // Variância no tempo de reação em ms
  BOAR_HIT_CHANCE: 0.85, // 85% de chance de acertar javali
  HUMAN_HIT_CHANCE: 0.05, // 5% de chance de acertar humano (evita)
  OTHER_HIT_CHANCE: 0.15, // 15% de chance de acertar outros (erro)
} as const

// ===========================================
// Classes do Modelo
// ===========================================
export const MODEL_CLASSES = {
  0: 'boar', // Javali - ALVO
  1: 'wild-boar', // Javali selvagem - ALVO
  2: 'dog', // Cachorro - distrator
  3: 'monkey', // Macaco - distrator
  4: 'person', // Pessoa - PENALIDADE
} as const

// Classes que são alvos válidos (dão pontos positivos)
export const TARGET_CLASSES = ['boar', 'wild-boar'] as const

// Classes que geram penalidade severa
export const PENALTY_CLASSES = ['human', 'person'] as const

// ===========================================
// Configurações de UI/UX
// ===========================================
export const UI_CONFIG = {
  HIT_MARKER_DURATION: 1000, // Duração do marcador de acerto em ms
  DETECTION_BOX_OPACITY: 0.7, // Opacidade das caixas de detecção
  SEGMENTATION_STROKE_WIDTH: 2, // Largura do contorno de segmentação
} as const

// Cores para detecções
export const DETECTION_COLORS = {
  TARGET: '#22c55e', // Verde para alvos (javali)
  PENALTY: '#ef4444', // Vermelho para penalidades (humano)
  OTHER: '#f59e0b', // Amarelo para outros animais
  SEGMENTATION_FILL: 'rgba(34, 197, 94, 0.2)', // Preenchimento de segmentação
} as const

// ===========================================
// Debug
// ===========================================
export const DEBUG_MODE = false // Mostrar boxes de detecção no jogo
