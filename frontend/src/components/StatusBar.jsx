import ConnectionBadge from './ConnectionBadge'

function formatTokens(n) {
  if (!n) return '0 tokens'
  if (n >= 1000) return '~' + (n / 1000).toFixed(1) + 'k tokens'
  return n + ' tokens'
}

export default function StatusBar({ connected, empresa, versao, tokens }) {
  return (
    <div className="flex items-center h-7 bg-[#0a0c12] border-t border-border px-3 gap-3 text-[11px] font-mono text-text-dim flex-shrink-0 select-none">
      {/* Status conexão */}
      <span className="flex items-center gap-1.5">
        <ConnectionBadge connected={connected} />
        <span className={connected ? 'text-success' : 'text-error'}>
          {connected ? 'Conectado' : 'Desconectado'}
        </span>
      </span>

      {empresa && (
        <>
          <span className="text-text-muted">|</span>
          <span className="truncate max-w-[200px]">{empresa}</span>
        </>
      )}

      {versao && (
        <>
          <span className="text-text-muted">|</span>
          <span>v{versao}</span>
        </>
      )}

      {/* Tokens - lado direito */}
      <span className="ml-auto">{formatTokens(tokens)}</span>
    </div>
  )
}
