'use client'

import { useCallback, useEffect, useRef } from 'react'
import { useGameStore } from '@/store/gameStore'

// URLs de sons (usando sons gratuitos ou placeholders)
const SOUNDS = {
  hit: '/sounds/hit.mp3',
  miss: '/sounds/miss.mp3',
  penalty: '/sounds/penalty.mp3',
  roundStart: '/sounds/round-start.mp3',
  roundEnd: '/sounds/round-end.mp3',
  victory: '/sounds/victory.mp3',
  defeat: '/sounds/defeat.mp3',
  countdown: '/sounds/countdown.mp3',
}

export function useSoundEffects() {
  const { soundEnabled } = useGameStore()
  const audioRefs = useRef<Map<string, HTMLAudioElement>>(new Map())

  // Pré-carrega sons
  useEffect(() => {
    if (typeof window === 'undefined') return

    Object.entries(SOUNDS).forEach(([key, url]) => {
      const audio = new Audio()
      audio.preload = 'auto'
      // Usa um som placeholder se o arquivo não existir
      audio.src = url
      audio.volume = 0.5
      audioRefs.current.set(key, audio)
    })

    return () => {
      audioRefs.current.forEach((audio) => {
        audio.pause()
        audio.src = ''
      })
      audioRefs.current.clear()
    }
  }, [])

  const playSound = useCallback(
    (sound: keyof typeof SOUNDS, volume = 0.5) => {
      if (!soundEnabled) return

      const audio = audioRefs.current.get(sound)
      if (audio) {
        audio.volume = volume
        audio.currentTime = 0
        audio.play().catch(() => {
          // Ignora erros de autoplay bloqueado
        })
      }
    },
    [soundEnabled]
  )

  const playHit = useCallback(() => playSound('hit', 0.6), [playSound])
  const playMiss = useCallback(() => playSound('miss', 0.4), [playSound])
  const playPenalty = useCallback(() => playSound('penalty', 0.7), [playSound])
  const playRoundStart = useCallback(() => playSound('roundStart', 0.5), [playSound])
  const playRoundEnd = useCallback(() => playSound('roundEnd', 0.5), [playSound])
  const playVictory = useCallback(() => playSound('victory', 0.7), [playSound])
  const playDefeat = useCallback(() => playSound('defeat', 0.5), [playSound])
  const playCountdown = useCallback(() => playSound('countdown', 0.4), [playSound])

  return {
    playHit,
    playMiss,
    playPenalty,
    playRoundStart,
    playRoundEnd,
    playVictory,
    playDefeat,
    playCountdown,
  }
}

