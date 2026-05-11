import { useState, useEffect, useCallback } from 'react'
import { RefreshCw, ExternalLink, Inbox } from 'lucide-react'
import api from '../api/backend'

const GRUPOS = [
  { key: null,       label: 'Todos' },
  { key: 'Fiscal',   label: 'Fiscal',   cor: 'text-[#D4537E] border-[#D4537E]/40 bg-[#D4537E]/10' },
  { key: 'Producao', label: 'Produção', cor: 'text-[#7F77DD] border-[#7F77DD]/40 bg-[#7F77DD]/10' },
  { key: 'G1',       label: 'G1',       cor: 'text-[#378ADD] border-[#378ADD]/40 bg-[#378ADD]/10' },
  { key: 'GW',       label: 'GW',       cor: 'text-[#888780] border-[#888780]/40 bg-[#888780]/10' },
]

const GRUPO_BORDA = {
  Fiscal:   'border-l-[#D4537E]',
  Producao: 'border-l-[#7F77DD]',
  G1:       'border-l-[#378ADD]',
  GW:       'border-l-[#888780]',
}

const STATUS_STYLE = {
  'Em Atendimento': 'text-warning',
  'Novo':           'text-accent',
  '5 - Resolvido':  'text-success',
  '6 - Fechado':    'text-text-muted',
}

function statusLabel(status) {
  if (!status) return '—'
  if (status.includes('Resolvido')) return 'Resolvido'
  if (status.includes('Fechado'))   return 'Fechado'
  if (status.includes('Cancelado')) return 'Cancelado'
  return status
}

function TicketRow({ t }) {
  const borda = GRUPO_BORDA[t.grupo] || 'border-l-border'
  const cat   = [t.serviceFirst, t.serviceSecond].filter(Boolean).join(' › ')

  return (
    <div className={`flex items-start gap-3 px-4 py-3 border-b border-border/50 hover:bg-surface/60 transition-colors border-l-2 ${borda} selectable`}>
      {/* ID + link */}
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

      {/* Assunto + farmácia */}
      <div className="flex-1 min-w-0">
        <p className="text-text text-sm truncate">{t.subject || '(sem assunto)'}</p>
        <p className="text-text-dim text-xs mt-0.5 truncate">{t.client_name || '—'}</p>
      </div>

      {/* Analista */}
      <div className="hidden md:block w-32 flex-shrink-0 text-xs text-text-dim truncate text-right">
        {t.owner_name || '—'}
      </div>

      {/* Categoria */}
      <div className="hidden lg:block w-48 flex-shrink-0 text-xs text-text-dim truncate text-right">
        {cat || '—'}
      </div>

      {/* Status */}
      <div className={`flex-shrink-0 text-xs font-medium w-20 text-right ${STATUS_STYLE[t.status] || 'text-text-dim'}`}>
        {statusLabel(t.status)}
      </div>
    </div>
  )
}

export default function AbertosHoje() {
  const [tickets,   setTickets]   = useState([])
  const [contagem,  setContagem]  = useState({})
  const [total,     setTotal]     = useState(0)
  const [data,      setData]      = useState('')
  const [loading,   setLoading]   = useState(true)
  const [filtroGrupo, setFiltroGrupo] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const { data: res } = await api.gestaoAbertosHoje()
      setTickets(res.tickets || [])
      setContagem(res.contagem || {})
      setTotal(res.total || 0)
      setData(res.data || '')
    } catch {}
    setLoading(false)
  }, [])

  useEffect(() => { load() }, [load])

  const ticketsFiltrados = filtroGrupo
    ? tickets.filter(t => t.grupo === filtroGrupo)
    : tickets

  const dataFormatada = data
    ? new Date(data + 'T12:00:00').toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long' })
    : ''

  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">
      {/* Header */}
      <div className="flex-shrink-0 px-6 pt-5 pb-3 border-b border-border">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-text font-semibold text-lg flex items-center gap-2">
              <Inbox size={18} className="text-accent" />
              Abertos Hoje
            </h1>
            <p className="text-text-dim text-xs mt-0.5 capitalize">
              {loading
                ? 'carregando...'
                : `${total} chamado${total !== 1 ? 's' : ''} · ${dataFormatada}`}
            </p>
          </div>
          <button
            onClick={load}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-50">
            <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            Atualizar
          </button>
        </div>

        {/* Filtros por grupo */}
        <div className="flex items-center gap-2 mt-3 flex-wrap">
          {GRUPOS.map(g => {
            const count = g.key === null ? total : (contagem[g.key] || 0)
            const ativo = filtroGrupo === g.key
            return (
              <button
                key={String(g.key)}
                onClick={() => setFiltroGrupo(g.key)}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium border transition-colors
                  ${ativo
                    ? (g.cor || 'bg-accent/20 text-accent border-accent/30')
                    : 'bg-surface2 text-text-dim border-border hover:text-text'}`}>
                {g.label}
                <span className={`font-mono ${ativo ? '' : 'text-text-muted'}`}>{count}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Cabeçalho da tabela */}
      <div className="flex-shrink-0 flex items-center gap-3 px-4 py-2 border-b border-border bg-surface2/50">
        <span className="w-20 text-[10px] font-semibold uppercase tracking-wider text-text-muted">#ID</span>
        <span className="flex-1 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Assunto / Farmácia</span>
        <span className="hidden md:block w-32 text-[10px] font-semibold uppercase tracking-wider text-text-muted text-right">Analista</span>
        <span className="hidden lg:block w-48 text-[10px] font-semibold uppercase tracking-wider text-text-muted text-right">Categoria</span>
        <span className="w-20 text-[10px] font-semibold uppercase tracking-wider text-text-muted text-right">Status</span>
      </div>

      {/* Lista */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <p className="text-text-dim text-sm py-12 text-center">Carregando...</p>
        ) : ticketsFiltrados.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center space-y-3">
            <Inbox size={36} className="text-text-dim/30" />
            <p className="text-text-dim text-sm">
              {filtroGrupo
                ? `Nenhum chamado do grupo ${filtroGrupo} hoje`
                : 'Nenhum chamado aberto hoje ainda'}
            </p>
          </div>
        ) : (
          ticketsFiltrados.map(t => <TicketRow key={t.id} t={t} />)
        )}
      </div>
    </div>
  )
}
