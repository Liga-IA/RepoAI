'use client'

import { motion } from 'framer-motion'
import { X, Target, AlertTriangle, Brain, Clock, MousePointer2, Trophy } from 'lucide-react'

interface HowToPlayProps {
  onClose: () => void
}

export default function HowToPlay({ onClose }: HowToPlayProps) {
  const rules = [
    {
      icon: <Target className="w-8 h-8 text-forest-400" />,
      title: 'Objetivo',
      description: 'Identifique e clique nos javalis (Sus scrofa) nas imagens o mais rápido possível.',
    },
    {
      icon: <MousePointer2 className="w-8 h-8 text-forest-400" />,
      title: 'Clique Preciso',
      description: 'Clique diretamente sobre os javalis para marcar pontos. Quanto mais rápido, mais bônus!',
    },
    {
      icon: <AlertTriangle className="w-8 h-8 text-danger-400" />,
      title: 'Cuidado com Humanos',
      description: 'Acertar humanos resulta em penalidade severa (-200 pts). Segurança é prioridade!',
    },
    {
      icon: <Brain className="w-8 h-8 text-warning-400" />,
      title: 'IA Competidora',
      description: 'A IA também está caçando! Ela usa YOLOv8 para detectar javalis automaticamente.',
    },
    {
      icon: <Clock className="w-8 h-8 text-earth-400" />,
      title: 'Tempo Limitado',
      description: 'Cada rodada tem 15 segundos. São 10 rodadas no total para provar quem é melhor!',
    },
    {
      icon: <Trophy className="w-8 h-8 text-warning-400" />,
      title: 'Pontuação',
      description: 'Javali: +100 pts | Outro animal: -30 pts | Humano: -200 pts',
    },
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        className="card-glow max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-b from-earth-950 to-transparent p-6 pb-8 flex items-center justify-between z-10">
          <h2 className="font-display text-4xl text-white">COMO JOGAR</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-earth-800/50 text-earth-400 hover:text-white hover:bg-earth-700/50 transition-all"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Conteúdo */}
        <div className="px-6 pb-6 space-y-6">
          {/* Intro */}
          <div className="p-4 bg-forest-900/20 border border-forest-800/30 rounded-xl">
            <p className="text-forest-300">
              <strong>Javali Hunter</strong> é um jogo competitivo onde você enfrenta uma IA 
              de visão computacional para ver quem consegue identificar mais javalis em imagens 
              de armadilhas fotográficas.
            </p>
          </div>

          {/* Regras */}
          <div className="grid gap-4">
            {rules.map((rule, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex gap-4 p-4 bg-earth-900/30 rounded-xl"
              >
                <div className="flex-shrink-0">{rule.icon}</div>
                <div>
                  <h3 className="text-white font-semibold mb-1">{rule.title}</h3>
                  <p className="text-earth-400 text-sm">{rule.description}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Dicas */}
          <div className="p-4 bg-warning-900/20 border border-warning-800/30 rounded-xl">
            <h3 className="text-warning-400 font-semibold mb-2 flex items-center gap-2">
              💡 Dicas
            </h3>
            <ul className="text-warning-300/80 text-sm space-y-1">
              <li>• Javalis têm corpo robusto, focinho alongado e pelos escuros</li>
              <li>• A IA aprende com seus acertos e erros para melhorar</li>
              <li>• Cliques mais rápidos ganham bônus de tempo</li>
              <li>• Na dúvida, não clique - erros custam pontos!</li>
            </ul>
          </div>

          {/* Legenda visual */}
          <div className="p-4 bg-earth-900/30 rounded-xl">
            <h3 className="text-white font-semibold mb-3">Identificação Visual</h3>
            <div className="grid grid-cols-3 gap-3 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 border-2 border-forest-400 rounded bg-forest-400/10" />
                <span className="text-forest-400">Javali (Alvo)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 border-2 border-warning-400 rounded bg-warning-400/10" />
                <span className="text-warning-400">Outro Animal</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 border-2 border-danger-500 rounded bg-danger-500/10" />
                <span className="text-danger-400">Humano</span>
              </div>
            </div>
          </div>

          {/* Botão fechar */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClose}
            className="btn-primary w-full"
          >
            ENTENDI, VAMOS CAÇAR!
          </motion.button>
        </div>
      </motion.div>
    </motion.div>
  )
}

