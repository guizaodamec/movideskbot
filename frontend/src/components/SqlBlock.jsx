import { useState } from 'react'
import { Play, Copy, Check, AlertTriangle } from 'lucide-react'

const SQL_KEYWORDS = /\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|CROSS|FULL|ON|AS|AND|OR|NOT|IN|IS|NULL|LIKE|ILIKE|ORDER|BY|GROUP|HAVING|LIMIT|OFFSET|UNION|ALL|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|DROP|ALTER|TABLE|INDEX|VIEW|WITH|DISTINCT|COUNT|SUM|AVG|MAX|MIN|CASE|WHEN|THEN|ELSE|END|EXISTS|BETWEEN|ASC|DESC|RETURNING|TRUNCATE|BEGIN|COMMIT|ROLLBACK)\b/gi

function highlight(sql) {
  return sql
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/'([^']*)'/g, '<span style="color:#22c55e">\'$1\'</span>')
    .replace(/\b(\d+(\.\d+)?)\b/g, '<span style="color:#fb923c">$1</span>')
    .replace(SQL_KEYWORDS, '<span style="color:#60a5fa;font-weight:600">$1</span>')
    .replace(/--[^\n]*/g, '<span style="color:#6b7a94;font-style:italic">$&</span>')
}

function classifySQL(sql) {
  const up = sql.trim().toUpperCase()
  if (up.startsWith('SELECT') || up.startsWith('WITH')) return 'SELECT'
  return 'MODIFY'
}

export default function SqlBlock({ sql, onExecute }) {
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const type = classifySQL(sql)
  const isModify = type === 'MODIFY'

  const handleCopy = () => {
    navigator.clipboard.writeText(sql).catch(() => {})
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const handleExecute = async () => {
    if (!onExecute) return
    setLoading(true)
    setResult(null)
    const res = await onExecute(sql, type)
    setResult(res)
    setLoading(false)
  }

  return (
    <div className="w-full rounded-xl overflow-hidden border border-border my-1">
      {/* Header */}
      <div className="flex items-center justify-between bg-sql-bg px-3 py-1.5 border-b border-border">
        <span className="text-[10px] font-mono font-semibold text-text-dim uppercase tracking-widest">SQL</span>
        <div className="flex items-center gap-1">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-2 py-1 text-[10px] text-text-dim hover:text-text rounded transition-colors"
          >
            {copied ? <Check size={11} className="text-success" /> : <Copy size={11} />}
            {copied ? 'Copiado' : 'Copiar'}
          </button>
          {onExecute && (
            <button
              onClick={handleExecute}
              disabled={loading}
              className={[
                'flex items-center gap-1 px-2.5 py-1 text-[10px] font-semibold rounded transition-colors disabled:opacity-50',
                isModify
                  ? 'bg-warning/15 text-warning hover:bg-warning/25 border border-warning/30'
                  : 'bg-success/15 text-success hover:bg-success/25 border border-success/30',
              ].join(' ')}
            >
              {isModify && <AlertTriangle size={10} />}
              <Play size={10} />
              {loading ? 'Executando...' : 'Executar'}
            </button>
          )}
        </div>
      </div>

      {/* Código SQL com highlight */}
      <pre
        className="bg-sql-bg px-4 py-3 text-xs font-mono overflow-x-auto selectable leading-relaxed text-text"
        dangerouslySetInnerHTML={{ __html: highlight(sql) }}
      />

      {/* Resultado */}
      {result && (
        <div className="bg-surface border-t border-border">
          {result.error ? (
            <p className="px-3 py-2 text-xs text-error font-mono selectable">{result.error}</p>
          ) : result.columns && result.columns.length > 0 && result.rows && result.rows.length > 0 ? (
            <div className="overflow-x-auto max-h-52">
              <table className="w-full text-xs font-mono">
                <thead className="sticky top-0 bg-surface2">
                  <tr>
                    {result.columns.map((col) => (
                      <th key={col} className="text-left px-3 py-1.5 text-text-dim font-semibold border-b border-border whitespace-nowrap">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.rows.slice(0, 10).map((row, i) => (
                    <tr key={i} className="hover:bg-surface2 selectable">
                      {result.columns.map((col) => (
                        <td key={col} className="px-3 py-1 border-b border-border/30 text-text-dim whitespace-nowrap">
                          {row[col] == null
                            ? <span className="text-text-muted italic">null</span>
                            : String(row[col])}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {result.rows.length > 10 && (
                <p className="text-center py-1.5 text-[10px] text-text-muted border-t border-border">
                  + {result.rows.length - 10} linha(s) não exibidas
                </p>
              )}
            </div>
          ) : result.affected != null ? (
            <p className="px-3 py-2 text-xs text-success font-mono">
              {result.affected} linha(s) afetada(s)
            </p>
          ) : (
            <p className="px-3 py-2 text-xs text-text-dim">Nenhum resultado.</p>
          )}
        </div>
      )}
    </div>
  )
}
