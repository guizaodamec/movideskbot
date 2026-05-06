import { useState, useEffect } from 'react'
import { Minus, Square, X, Maximize2 } from 'lucide-react'

export default function TitleBar() {
  const [isMax, setIsMax] = useState(false)

  useEffect(() => {
    if (!window.electron) return
    const interval = setInterval(async () => {
      const max = await window.electron.isMaximized()
      setIsMax(max)
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div
      className="drag-region flex items-center justify-between h-8 bg-[#0a0c12] border-b border-[#1a1d27] select-none flex-shrink-0"
    >
      {/* Logo + nome */}
      <div className="no-drag flex items-center gap-2 px-4">
        <div className="w-4 h-4 rounded-full bg-accent flex items-center justify-center flex-shrink-0">
          <span className="text-white text-[8px] font-bold leading-none">E</span>
        </div>
        <span className="text-text-dim text-xs font-medium">FarmaFacil Assistente</span>
      </div>

      {/* Controles */}
      <div className="no-drag flex items-stretch h-full">
        <button
          onClick={() => window.electron?.minimize()}
          className="w-10 flex items-center justify-center text-text-dim hover:text-text hover:bg-surface transition-colors"
          title="Minimizar"
        >
          <Minus size={12} />
        </button>
        <button
          onClick={() => window.electron?.maximize()}
          className="w-10 flex items-center justify-center text-text-dim hover:text-text hover:bg-surface transition-colors"
          title={isMax ? 'Restaurar' : 'Maximizar'}
        >
          {isMax ? <Square size={11} /> : <Maximize2 size={11} />}
        </button>
        <button
          onClick={() => window.electron?.close()}
          className="w-10 flex items-center justify-center text-text-dim hover:text-white hover:bg-red-600 transition-colors"
          title="Fechar"
        >
          <X size={12} />
        </button>
      </div>
    </div>
  )
}
