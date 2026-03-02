import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Javali Hunter | IA vs Humano',
  description: 'Jogo de detecção de javalis usando visão computacional - Quem é mais rápido: você ou a IA?',
  keywords: ['javali', 'detecção', 'ia', 'visão computacional', 'jogo'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link 
          href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" 
          rel="stylesheet" 
        />
      </head>
      <body className="font-body antialiased bg-forest-950 text-white">
        {children}
      </body>
    </html>
  )
}

