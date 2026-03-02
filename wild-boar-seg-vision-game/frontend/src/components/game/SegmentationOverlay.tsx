'use client'

import { motion } from 'framer-motion'
import { Detection, SegmentationPoint } from '@/store/gameStore'

interface SegmentationOverlayProps {
  detection: Detection
  showLabel?: boolean
  animate?: boolean
  strokeWidth?: number
}

/**
 * Componente que renderiza o contorno de segmentação de uma detecção
 * Similar às imagens de referência com contorno amarelo/verde
 */
export function SegmentationOverlay({ 
  detection, 
  showLabel = true,
  animate = true,
  strokeWidth = 3,
}: SegmentationOverlayProps) {
  const { bbox, class_name, confidence, is_target, segmentation } = detection
  
  // Cores baseadas no tipo de detecção - cores vibrantes como nas imagens de referência
  const getColors = () => {
    if (is_target) {
      return {
        stroke: '#c8ff00', // Verde-limão MUITO brilhante (como na imagem)
        fill: 'rgba(200, 255, 0, 0.15)',
        glow: '#e0ff66',
        labelBg: 'bg-lime-500',
      }
    }
    if (class_name === 'human') {
      return {
        stroke: '#ff3333', // Vermelho brilhante
        fill: 'rgba(255, 51, 51, 0.15)',
        glow: '#ff6666',
        labelBg: 'bg-red-500',
      }
    }
    return {
      stroke: '#ffee00', // Amarelo brilhante
      fill: 'rgba(255, 238, 0, 0.15)',
      glow: '#fff566',
      labelBg: 'bg-yellow-400',
    }
  }

  const colors = getColors()

  // Se temos segmentação (polígono), renderiza o contorno
  if (segmentation && segmentation.length > 2) {
    return (
      <SegmentationPolygon
        points={segmentation}
        colors={colors}
        className={class_name}
        confidence={confidence}
        showLabel={showLabel}
        animate={animate}
        strokeWidth={strokeWidth}
      />
    )
  }

  // Fallback: renderiza bounding box estilizado como contorno
  return (
    <BoundingBoxContour
      bbox={bbox}
      colors={colors}
      className={class_name}
      confidence={confidence}
      showLabel={showLabel}
      animate={animate}
      strokeWidth={strokeWidth}
    />
  )
}

// Renderiza um polígono de segmentação real
function SegmentationPolygon({
  points,
  colors,
  className,
  confidence,
  showLabel,
  animate,
  strokeWidth,
}: {
  points: SegmentationPoint[]
  colors: { stroke: string; fill: string; glow: string; labelBg: string }
  className: string
  confidence: number
  showLabel: boolean
  animate: boolean
  strokeWidth: number
}) {
  // Calcula bounding box para posicionar o label
  const minX = Math.min(...points.map(p => p.x))
  const minY = Math.min(...points.map(p => p.y))
  
  // Cria um ID único para o filtro
  const filterId = `glow-${className}-${Math.random().toString(36).substr(2, 9)}`

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <svg 
        className="w-full h-full" 
        viewBox="0 0 100 100" 
        preserveAspectRatio="none"
        style={{ position: 'absolute', inset: 0 }}
      >
        <defs>
          {/* Glow/shadow effect para contorno */}
          <filter id={filterId} x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="0.8" floodColor={colors.glow} floodOpacity="0.8"/>
            <feDropShadow dx="0" dy="0" stdDeviation="0.3" floodColor={colors.stroke} floodOpacity="1"/>
          </filter>
        </defs>

        {/* Preenchimento sutil com gradiente */}
        <motion.polygon
          points={points.map(p => `${p.x * 100},${p.y * 100}`).join(' ')}
          fill={colors.fill}
          initial={animate ? { opacity: 0 } : undefined}
          animate={animate ? { opacity: 0.15 } : undefined}
          transition={{ duration: 0.4, delay: 0.2 }}
        />

        {/* Contorno de fundo (mais grosso, cria efeito de borda) */}
        <motion.polygon
          points={points.map(p => `${p.x * 100},${p.y * 100}`).join(' ')}
          fill="none"
          stroke="rgba(0,0,0,0.5)"
          strokeWidth={strokeWidth * 0.5}
          strokeLinejoin="round"
          strokeLinecap="round"
          initial={animate ? { opacity: 0 } : undefined}
          animate={animate ? { opacity: 1 } : undefined}
          transition={{ duration: 0.3 }}
        />

        {/* Contorno principal - SÓLIDO e BRILHANTE como nas imagens de referência */}
        <motion.polygon
          points={points.map(p => `${p.x * 100},${p.y * 100}`).join(' ')}
          fill="none"
          stroke={colors.stroke}
          strokeWidth={strokeWidth * 0.35}
          strokeLinejoin="round"
          strokeLinecap="round"
          filter={`url(#${filterId})`}
          initial={animate ? { opacity: 0, scale: 0.95 } : undefined}
          animate={animate ? { opacity: 1, scale: 1 } : undefined}
          transition={{ duration: 0.4, ease: 'easeOut' }}
          style={{ 
            transformOrigin: 'center',
          }}
        />
      </svg>

      {/* Label com background */}
      {showLabel && (
        <motion.div
          className={`absolute ${colors.labelBg} text-white text-xs font-bold px-2 py-1 rounded shadow-lg`}
          style={{
            left: `${minX * 100}%`,
            top: `${Math.max(8, minY * 100)}%`,
            transform: 'translate(0, -120%)',
            zIndex: 10,
          }}
          initial={animate ? { opacity: 0, y: 10, scale: 0.8 } : undefined}
          animate={animate ? { opacity: 1, y: 0, scale: 1 } : undefined}
          transition={{ delay: 0.3, duration: 0.3 }}
        >
          <span className="drop-shadow-sm">
            {className.toUpperCase()} {(confidence * 100).toFixed(0)}%
          </span>
        </motion.div>
      )}
    </div>
  )
}

// Renderiza contorno de bounding box estilizado
function BoundingBoxContour({
  bbox,
  colors,
  className,
  confidence,
  showLabel,
  animate,
  strokeWidth,
}: {
  bbox: { x: number; y: number; width: number; height: number }
  colors: { stroke: string; fill: string; glow: string; labelBg: string }
  className: string
  confidence: number
  showLabel: boolean
  animate: boolean
  strokeWidth: number
}) {
  const left = (bbox.x - bbox.width / 2) * 100
  const top = (bbox.y - bbox.height / 2) * 100
  const width = bbox.width * 100
  const height = bbox.height * 100

  // Cria um path com cantos arredondados para simular contorno orgânico
  const cornerRadius = Math.min(width, height) * 0.1

  return (
    <motion.div
      className="absolute pointer-events-none"
      style={{
        left: `${left}%`,
        top: `${top}%`,
        width: `${width}%`,
        height: `${height}%`,
      }}
      initial={animate ? { scale: 0.8, opacity: 0 } : undefined}
      animate={animate ? { scale: 1, opacity: 1 } : undefined}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {/* Borda com glow */}
      <div
        className="absolute inset-0 rounded-lg"
        style={{
          border: `${strokeWidth}px solid ${colors.stroke}`,
          borderRadius: `${cornerRadius}%`,
          boxShadow: `0 0 10px ${colors.glow}, 0 0 20px ${colors.glow}40`,
          background: colors.fill,
        }}
      />

      {/* Cantos destacados */}
      <CornerMarkers color={colors.stroke} size={Math.min(width, height) * 0.15} />

      {/* Label */}
      {showLabel && (
        <motion.div
          className={`absolute -top-6 left-0 ${colors.labelBg} text-white text-xs font-bold px-2 py-0.5 rounded shadow-lg whitespace-nowrap`}
          initial={animate ? { opacity: 0, y: 10 } : undefined}
          animate={animate ? { opacity: 1, y: 0 } : undefined}
          transition={{ delay: 0.2 }}
        >
          {className.toUpperCase()} {(confidence * 100).toFixed(0)}%
        </motion.div>
      )}
    </motion.div>
  )
}

// Marcadores de canto estilo mira
function CornerMarkers({ color, size }: { color: string; size: number }) {
  const cornerStyle = {
    position: 'absolute' as const,
    width: `${size}%`,
    height: `${size}%`,
    borderColor: color,
    borderWidth: '3px',
  }

  return (
    <>
      {/* Top-left */}
      <div
        style={{
          ...cornerStyle,
          top: 0,
          left: 0,
          borderTop: `3px solid ${color}`,
          borderLeft: `3px solid ${color}`,
          borderRight: 'none',
          borderBottom: 'none',
        }}
      />
      {/* Top-right */}
      <div
        style={{
          ...cornerStyle,
          top: 0,
          right: 0,
          borderTop: `3px solid ${color}`,
          borderRight: `3px solid ${color}`,
          borderLeft: 'none',
          borderBottom: 'none',
        }}
      />
      {/* Bottom-left */}
      <div
        style={{
          ...cornerStyle,
          bottom: 0,
          left: 0,
          borderBottom: `3px solid ${color}`,
          borderLeft: `3px solid ${color}`,
          borderRight: 'none',
          borderTop: 'none',
        }}
      />
      {/* Bottom-right */}
      <div
        style={{
          ...cornerStyle,
          bottom: 0,
          right: 0,
          borderBottom: `3px solid ${color}`,
          borderRight: `3px solid ${color}`,
          borderLeft: 'none',
          borderTop: 'none',
        }}
      />
    </>
  )
}

// Componente para múltiplas detecções
interface AIDetectionOverlayProps {
  detections: Detection[]
  showLabels?: boolean
  animate?: boolean
}

export function AIDetectionOverlay({ 
  detections, 
  showLabels = true,
  animate = true,
}: AIDetectionOverlayProps) {
  return (
    <>
      {detections.map((detection, index) => (
        <SegmentationOverlay
          key={`detection-${index}-${detection.class_name}`}
          detection={detection}
          showLabel={showLabels}
          animate={animate}
        />
      ))}
    </>
  )
}

export default SegmentationOverlay
