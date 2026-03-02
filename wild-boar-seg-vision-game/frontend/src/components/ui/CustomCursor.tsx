'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

export default function CustomCursor() {
  const [position, setPosition] = useState({ x: 0, y: 0 })
  const [isClicking, setIsClicking] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY })
      setIsVisible(true)
    }

    const handleMouseDown = () => setIsClicking(true)
    const handleMouseUp = () => setIsClicking(false)
    const handleMouseLeave = () => setIsVisible(false)
    const handleMouseEnter = () => setIsVisible(true)

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mousedown', handleMouseDown)
    document.addEventListener('mouseup', handleMouseUp)
    document.addEventListener('mouseleave', handleMouseLeave)
    document.addEventListener('mouseenter', handleMouseEnter)

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mousedown', handleMouseDown)
      document.removeEventListener('mouseup', handleMouseUp)
      document.removeEventListener('mouseleave', handleMouseLeave)
      document.removeEventListener('mouseenter', handleMouseEnter)
    }
  }, [])

  if (!isVisible) return null

  return (
    <motion.div
      className="crosshair"
      style={{
        left: position.x,
        top: position.y,
      }}
      animate={{
        scale: isClicking ? 0.8 : 1,
      }}
      transition={{ duration: 0.1 }}
    >
      {/* Anel externo */}
      <div className="crosshair-ring" />
      
      {/* Cruz central */}
      <div className="crosshair-inner" />
      
      {/* Ponto central */}
      <motion.div 
        className="crosshair-dot"
        animate={{
          scale: isClicking ? 1.5 : 1,
          backgroundColor: isClicking ? '#ef4444' : '#ef4444',
        }}
      />

      {/* Marcadores de canto */}
      <svg 
        className="absolute inset-0 w-full h-full" 
        viewBox="0 0 48 48"
      >
        {/* Canto superior esquerdo */}
        <path
          d="M 8 16 L 8 8 L 16 8"
          fill="none"
          stroke="#4ade80"
          strokeWidth="2"
          strokeLinecap="round"
        />
        {/* Canto superior direito */}
        <path
          d="M 32 8 L 40 8 L 40 16"
          fill="none"
          stroke="#4ade80"
          strokeWidth="2"
          strokeLinecap="round"
        />
        {/* Canto inferior esquerdo */}
        <path
          d="M 8 32 L 8 40 L 16 40"
          fill="none"
          stroke="#4ade80"
          strokeWidth="2"
          strokeLinecap="round"
        />
        {/* Canto inferior direito */}
        <path
          d="M 32 40 L 40 40 L 40 32"
          fill="none"
          stroke="#4ade80"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    </motion.div>
  )
}

