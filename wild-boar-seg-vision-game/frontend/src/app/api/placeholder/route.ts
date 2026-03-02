import { NextRequest, NextResponse } from 'next/server'

/**
 * API Route para gerar imagens placeholder com detecções simuladas
 * Útil para testes sem backend real
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const width = parseInt(searchParams.get('width') || '800')
  const height = parseInt(searchParams.get('height') || '600')
  const seed = searchParams.get('seed') || Date.now().toString()

  // Gera SVG com padrão de floresta
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#1a3a20;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#0f2515;stop-opacity:1" />
        </linearGradient>
        <pattern id="noise" patternUnits="userSpaceOnUse" width="100" height="100">
          <circle cx="25" cy="25" r="2" fill="rgba(255,255,255,0.03)"/>
          <circle cx="75" cy="75" r="1.5" fill="rgba(255,255,255,0.02)"/>
          <circle cx="50" cy="10" r="1" fill="rgba(255,255,255,0.04)"/>
        </pattern>
      </defs>
      
      <!-- Fundo -->
      <rect width="100%" height="100%" fill="url(#bg)"/>
      <rect width="100%" height="100%" fill="url(#noise)"/>
      
      <!-- Elementos de floresta -->
      <ellipse cx="${width * 0.2}" cy="${height * 0.8}" rx="${width * 0.15}" ry="${height * 0.1}" fill="#1a3a20" opacity="0.7"/>
      <ellipse cx="${width * 0.8}" cy="${height * 0.85}" rx="${width * 0.2}" ry="${height * 0.12}" fill="#152d18" opacity="0.6"/>
      
      <!-- Texto informativo -->
      <text x="${width / 2}" y="${height / 2}" 
            font-family="Arial, sans-serif" 
            font-size="24" 
            fill="rgba(255,255,255,0.3)" 
            text-anchor="middle">
        Área de Caça - Imagem ${seed}
      </text>
      
      <!-- Ícone de javali estilizado -->
      <g transform="translate(${width / 2 - 30}, ${height / 2 + 40})">
        <ellipse cx="30" cy="20" rx="25" ry="15" fill="#3d2914" opacity="0.8"/>
        <circle cx="50" cy="18" r="4" fill="#2a1d0e"/>
        <ellipse cx="10" cy="22" rx="6" ry="4" fill="#3d2914"/>
      </g>
      
      <!-- Indicadores de câmera -->
      <circle cx="20" cy="20" r="5" fill="#ef4444" opacity="0.8">
        <animate attributeName="opacity" values="0.8;0.3;0.8" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="32" y="25" font-family="monospace" font-size="10" fill="#ef4444" opacity="0.8">REC</text>
      
      <!-- Timestamp -->
      <text x="${width - 10}" y="${height - 10}" 
            font-family="monospace" 
            font-size="12" 
            fill="rgba(255,255,255,0.5)" 
            text-anchor="end">
        ${new Date().toISOString()}
      </text>
    </svg>
  `

  return new NextResponse(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'no-cache',
    },
  })
}

