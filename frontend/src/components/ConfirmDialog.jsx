import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle } from 'lucide-react'

export default function ConfirmDialog({ open, query, explanation, onConfirm, onCancel }) {
  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            onClick={onCancel}
          />

          {/* Dialog */}
          <motion.div
            initial={{ opacity: 0, scale: 0.92, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.92, y: 10 }}
            transition={{ duration: 0.18 }}
            className="relative z-10 bg-surface border border-border rounded-card w-[520px] max-w-[90vw] overflow-hidden shadow-2xl"
          >
            {/* Faixa de aviso */}
            <div className="flex items-center gap-3 bg-warning/10 border-b border-warning/20 px-4 py-3">
              <AlertTriangle size={18} className="text-warning flex-shrink-0" />
              <p className="text-warning text-sm font-semibold leading-snug">
                ATENÇÃO: Esta operação irá modificar dados no banco de dados.
              </p>
            </div>

            <div className="p-4 space-y-4">
              {/* Explicação */}
              {explanation && (
                <div>
                  <p className="text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-1.5">
                    O que será feito:
                  </p>
                  <p className="text-text text-sm leading-relaxed selectable">{explanation}</p>
                </div>
              )}

              {/* Query */}
              <div>
                <p className="text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-1.5">
                  Query a ser executada:
                </p>
                <pre className="bg-sql-bg border border-border rounded-lg p-3 text-xs font-mono text-text overflow-x-auto selectable whitespace-pre-wrap leading-relaxed max-h-48">
                  {query}
                </pre>
              </div>

              {/* Botões */}
              <div className="flex justify-end gap-2 pt-1">
                <button
                  onClick={onCancel}
                  className="px-4 py-2 text-sm text-text-dim bg-surface2 hover:bg-border rounded-lg font-medium"
                >
                  Cancelar
                </button>
                <button
                  onClick={onConfirm}
                  className="px-4 py-2 text-sm text-white bg-error hover:bg-red-700 rounded-lg font-bold"
                >
                  EXECUTAR
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
