import { useState } from 'react'
import { ClipboardCheck, ExternalLink, ChevronDown, ChevronRight, AlertTriangle, XCircle, Search } from 'lucide-react'
import api from '../api/backend'

function hoje() {
  return new Date().toISOString().slice(0, 10)
}
function diasAtras(n) {
  const d = new Date()
  d.setDate(d.getDate() - n)
  return d.toISOString().slice(0, 10)
}

const TIPO_STYLE = {
  resolvido_indevido:  { cor: 'text-error bg-error/10 border-error/30',   icon: XCircle },
  cancelado_prematuro: { cor: 'text-warning bg-warning/10 border-warning/30', icon: AlertTriangle },
}

function BadgeTipo({ tipo, label }) {
  const s = TIPO_STYLE[tipo] || {}
  const Icon = s.icon || AlertTriangle
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-lg border text-[11px] font-medium ${s.cor}`}>
      <Icon size={11} />
      {label}
    </span>
  )
}

function DotDias({ datas }) {
  return (
    <div className="flex items-center gap-1 flex-wrap mt-1">
      {datas.map((d, i) => (
        <span key={i} className="text-[10px] bg-surface2 border border-border rounded px-1.5 py-0.5 font-mono text-text-dim">
          {d.slice(5)}
        </span>
      ))}
      {datas.length === 0 && <span className="text-[10px] text-text-muted italic">sem datas registradas</span>}
    </div>
  )
}

function TicketRow({ t }) {
  return (
    <div className="flex items-start gap-3 px-4 py-3 border-b border-border/40 hover:bg-surface/40 transition-colors selectable">
      <div className="flex items-center gap-1.5 flex-shrink-0 w-20">
        <span className="text-text-muted font-mono text-xs">#{t.id}</span>
        <a
          href={`https://prismafive.movidesk.com/Ticket/Edit/${t.id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-accent hover:text-accent/70 transition-colors"
          title="Abrir no Movidesk">
          <ExternalLink size={11} />
        </a>
      </div>

      <div className="flex-1 min-w-0 space-y-1">
        <p className="text-text text-sm truncate">{t.subject || '(sem assunto)'}</p>
        <p className="text-text-dim text-xs">{t.client_name || '—'}</p>
        <BadgeTipo tipo={t.tipo} label={t.label} />
        <div className="flex items-center gap-1.5 text-[10px] text-text-muted">
          <span>Tentativas ({t.tentativas}):</span>
          <DotDias datas={t.datas} />
        </div>
      </div>

      <div className="flex-shrink-0 text-[10px] text-text-muted text-right">
        {t.fechado_em || '—'}
      </div>
    </div>
  )
}

function AnalistaCard({ analista, total, resolvidos_indevidos, cancelados_prematuros, tickets }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="border border-border rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-surface transition-colors">
        <div className="flex-1 min-w-0">
          <span className="text-text font-medium text-sm">{analista}</span>
          <div className="flex items-center gap-3 mt-0.5 flex-wrap">
            {resolvidos_indevidos > 0 && (
              <span className="text-[11px] text-error flex items-center gap-1">
                <XCircle size={11} /> {resolvidos_indevidos} resolvido{resolvidos_indevidos !== 1 ? 's' : ''} indevidamente
              </span>
            )}
            {cancelados_prematuros > 0 && (
              <span className="text-[11px] text-warning flex items-center gap-1">
                <AlertTriangle size={11} /> {cancelados_prematuros} cancelado{cancelados_prematuros !== 1 ? 's' : ''} prematuro{cancelados_prematuros !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </div>
        <span className="flex-shrink-0 px-2.5 py-1 bg-error/10 text-error border border-error/20 rounded-lg text-xs font-bold">
          {total} violação{total !== 1 ? 'ões' : ''}
        </span>
        {open ? <ChevronDown size={15} className="text-text-dim flex-shrink-0" /> : <ChevronRight size={15} className="text-text-dim flex-shrink-0" />}
      </button>

      {open && (
        <div className="border-t border-border">
          {tickets.map(t => <TicketRow key={t.id} t={t} />)}
        </div>
      )}
    </div>
  )
}

export default function AuditoriaContato() {
  const [dateFrom,   setDateFrom]   = useState(diasAtras(30))
  const [dateTo,     setDateTo]     = useState(hoje())
  const [loading,    setLoading]    = useState(false)
  const [resultado,  setResultado]  = useState(null)
  const [erro,       setErro]       = useState('')

  const analisar = async () => {
    setLoading(true)
    setErro('')
    setResultado(null)
    try {
      const { data } = await api.gestaoAuditoriaContato(dateFrom, dateTo)
      setResultado(data)
    } catch (e) {
      setErro(e.response?.data?.error || 'Erro ao buscar dados. Tente novamente.')
    }
    setLoading(false)
  }

  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">
      {/* Header */}
      <div className="flex-shrink-0 px-6 pt-5 pb-4 border-b border-border">
        <div className="flex items-start gap-3">
          <ClipboardCheck size={20} className="text-accent mt-0.5 flex-shrink-0" />
          <div>
            <h1 className="text-text font-semibold text-lg">Auditoria de Contato</h1>
            <p className="text-text-dim text-xs mt-0.5 max-w-xl">
              Monitora tickets encerrados ou cancelados sem seguir o procedimento correto:
              macro <strong className="text-text">Cliente Indisponível</strong> por{' '}
              <strong className="text-text">5 dias diferentes</strong> antes de cancelar.
            </p>
          </div>
        </div>

        {/* Controles */}
        <div className="flex items-end gap-3 mt-4 flex-wrap">
          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold uppercase tracking-wider text-text-muted">De</label>
            <input
              type="date"
              value={dateFrom}
              onChange={e => setDateFrom(e.target.value)}
              className="bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent transition-colors"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-[10px] font-semibold uppercase tracking-wider text-text-muted">Até</label>
            <input
              type="date"
              value={dateTo}
              onChange={e => setDateTo(e.target.value)}
              className="bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent transition-colors"
            />
          </div>
          <button
            onClick={analisar}
            disabled={loading || !dateFrom || !dateTo}
            className="flex items-center gap-2 px-4 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50">
            <Search size={14} className={loading ? 'animate-pulse' : ''} />
            {loading ? 'Analisando...' : 'Analisar'}
          </button>
          {loading && (
            <p className="text-text-muted text-xs self-center">
              Buscando tickets e verificando ações — pode demorar alguns segundos...
            </p>
          )}
        </div>
      </div>

      {/* Conteúdo */}
      <div className="flex-1 overflow-y-auto px-6 py-4">

        {erro && (
          <div className="bg-error/10 border border-error/30 rounded-xl px-4 py-3 text-error text-sm">
            {erro}
          </div>
        )}

        {resultado && (
          <div className="space-y-4">
            {/* Resumo */}
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: 'Tickets analisados', value: resultado.total_analisados, cor: 'text-text' },
                { label: 'Violações encontradas', value: resultado.total_violacoes, cor: resultado.total_violacoes > 0 ? 'text-error' : 'text-success' },
                { label: 'Analistas com violação', value: resultado.resultado.length, cor: resultado.resultado.length > 0 ? 'text-warning' : 'text-success' },
              ].map(c => (
                <div key={c.label} className="bg-surface2 border border-border rounded-xl px-4 py-3 text-center">
                  <p className={`text-2xl font-bold ${c.cor}`}>{c.value}</p>
                  <p className="text-text-dim text-xs mt-0.5">{c.label}</p>
                </div>
              ))}
            </div>

            {/* Lista por analista */}
            {resultado.resultado.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <ClipboardCheck size={36} className="text-success/50" />
                <p className="text-text-dim text-sm">Nenhuma violação encontrada no período</p>
                <p className="text-text-muted text-xs">Todos os procedimentos estão sendo seguidos corretamente</p>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-text-muted pb-1">
                  Analistas com violações — ordenado por mais ocorrências
                </p>
                {resultado.resultado.map(r => (
                  <AnalistaCard key={r.analista} {...r} />
                ))}
              </div>
            )}
          </div>
        )}

        {!resultado && !loading && !erro && (
          <div className="flex flex-col items-center justify-center py-20 text-center space-y-3">
            <ClipboardCheck size={40} className="text-text-dim/20" />
            <p className="text-text-dim text-sm">Selecione o período e clique em Analisar</p>
          </div>
        )}
      </div>
    </div>
  )
}
