import { useState, useEffect, useCallback } from 'react'
import { AlertCircle, CheckCircle, Clock, ChevronDown, ChevronRight, Copy, Check, Zap, ClipboardList, RefreshCw, ExternalLink } from 'lucide-react'
import api from '../api/backend'

// ── Urgência por dias em aberto ────────────────────────────────────────────────
function urgencia(dias) {
  if (dias == null) return { label: '?', color: 'text-text-dim', bg: 'bg-surface2', border: 'border-border' }
  if (dias === 0)   return { label: 'Hoje',        color: 'text-success', bg: 'bg-success/10',  border: 'border-success/30' }
  if (dias <= 2)    return { label: `${dias}d`,     color: 'text-warning', bg: 'bg-warning/10',  border: 'border-warning/30' }
  if (dias <= 6)    return { label: `${dias}d`,     color: 'text-orange-400', bg: 'bg-orange-400/10', border: 'border-orange-400/30' }
  return             { label: `${dias}d ⚠`,        color: 'text-error',   bg: 'bg-error/10',    border: 'border-error/30' }
}

// ── Botão copiar ───────────────────────────────────────────────────────────────
function CopyBtn({ text }) {
  const [ok, setOk] = useState(false)
  return (
    <button
      onClick={() => { navigator.clipboard.writeText(text); setOk(true); setTimeout(() => setOk(false), 1500) }}
      className={`p-1 rounded transition-colors flex-shrink-0 ${ok ? 'text-success' : 'text-text-dim hover:text-text'}`}
      title="Copiar">
      {ok ? <Check size={11} /> : <Copy size={11} />}
    </button>
  )
}

// ── Card de ticket ─────────────────────────────────────────────────────────────
function TicketCard({ t }) {
  const [open, setOpen] = useState(false)
  const u   = urgencia(t.dias_aberto)
  const cat = t.serviceSecond || t.serviceFirst || ''

  return (
    <div className={`rounded-xl border ${u.border} overflow-hidden`}>
      {/* Cabeçalho do card */}
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-start gap-3 px-4 py-3 text-left hover:bg-surface transition-colors">
        {/* Badge de urgência */}
        <div className={`flex-shrink-0 min-w-[44px] text-center px-2 py-0.5 rounded-lg text-xs font-bold ${u.color} ${u.bg} border ${u.border}`}>
          {u.label}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-text-muted font-mono text-xs">#{t.id}</span>
            <span
              onClick={e => { e.stopPropagation(); window.open(`https://prismafive.movidesk.com/Ticket/Edit/${t.id}`, '_blank') }}
              className="text-accent hover:text-accent/70 transition-colors cursor-pointer flex-shrink-0"
              title="Abrir no Movidesk">
              <ExternalLink size={11} />
            </span>
            <span className="text-text text-sm font-medium truncate">{t.subject}</span>
          </div>
          <div className="flex items-center gap-3 mt-0.5 text-xs text-text-dim flex-wrap">
            <span className="font-medium text-text-dim">{t.client_name}</span>
            {cat && <span>{t.serviceFirst} › {t.serviceSecond}</span>}
            <span>{t.createdDate}</span>
          </div>
        </div>
        {/* Indicadores */}
        <div className="flex items-center gap-1.5 flex-shrink-0">
          {t.similares?.length > 0 && (
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-accent/15 text-accent border border-accent/20 font-medium">
              {t.similares.length} similar{t.similares.length > 1 ? 'es' : ''}
            </span>
          )}
          {t.checklist && (
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-surface2 text-text-dim border border-border">
              checklist
            </span>
          )}
          {open ? <ChevronDown size={14} className="text-text-dim" /> : <ChevronRight size={14} className="text-text-dim" />}
        </div>
      </button>

      {/* Detalhes expandidos */}
      {open && (
        <div className="border-t border-border bg-[#0e1120]/50 px-4 py-3 space-y-4 selectable">

          {/* Chamados similares */}
          {t.similares?.length > 0 && (
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wider text-accent mb-2 flex items-center gap-1 select-none">
                <Zap size={10} /> Chamados similares já resolvidos
              </p>
              <div className="space-y-2">
                {t.similares.map((s, i) => (
                  <div key={i} className="bg-surface2 border border-border rounded-lg px-3 py-2 text-xs">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-text-dim font-mono">#{s.id} · {s.client_name} · {(s.resolvedIn || s.lastUpdate || '').slice(0, 10)}</span>
                          <a
                            href={`https://prismafive.movidesk.com/Ticket/Edit/${s.id}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-accent hover:text-accent/70 transition-colors flex-shrink-0 select-none"
                            title="Abrir no Movidesk"
                            onClick={e => e.stopPropagation()}>
                            <ExternalLink size={11} />
                          </a>
                        </div>
                        {s.problema && <p className="text-warning mt-1"><span className="font-semibold">Problema:</span> {s.problema}</p>}
                        {s.solucao  && <p className="text-success mt-0.5"><span className="font-semibold">Solução:</span> {s.solucao}</p>}
                      </div>
                      {s.solucao && <CopyBtn text={s.solucao} />}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Checklist */}
          {t.checklist && (
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wider text-text-dim mb-2 flex items-center gap-1">
                <ClipboardList size={10} /> Checklist — {t.checklist.label}
              </p>
              <ul className="space-y-1.5">
                {t.checklist.itens.map((item, i) => (
                  <ChecklistItem key={i} text={item} />
                ))}
              </ul>
            </div>
          )}

          {t.similares?.length === 0 && !t.checklist && (
            <p className="text-text-dim text-xs italic">Nenhuma sugestão disponível para este chamado.</p>
          )}
        </div>
      )}
    </div>
  )
}

function ChecklistItem({ text }) {
  const [done, setDone] = useState(false)
  return (
    <li
      onClick={() => setDone(d => !d)}
      className={`flex items-start gap-2 cursor-pointer text-xs px-2 py-1.5 rounded-lg transition-colors
        ${done ? 'line-through text-text-muted bg-surface2' : 'text-text hover:bg-surface2'}`}>
      <div className={`w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 mt-px transition-colors
        ${done ? 'border-success bg-success/20 text-success' : 'border-border'}`}>
        {done && <Check size={10} />}
      </div>
      {text}
    </li>
  )
}

// ── Componente principal ───────────────────────────────────────────────────────
export default function Suporte({ session }) {
  const [tickets,   setTickets]   = useState([])
  const [respostas, setRespostas] = useState([])
  const [loading,   setLoading]   = useState(true)
  const [syncing,   setSyncing]   = useState(false)
  const [analista,  setAnalista]  = useState('')
  const [catFiltro, setCatFiltro] = useState('')
  const [tab,       setTab]       = useState('fila')  // 'fila' | 'respostas'

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [viewRes, rpRes] = await Promise.all([
        api.gestaoAnalistaView(),
        api.gestaoRespostasRapidas(),
      ])
      setTickets(viewRes.data.tickets || [])
      setAnalista(viewRes.data.analista || '')
      setRespostas(rpRes.data || [])
    } catch {}
    setLoading(false)
  }, [])

  const syncAbertos = useCallback(async () => {
    setSyncing(true)
    try {
      await api.gestaoSyncAbertos()
      await load()
    } catch {}
    setSyncing(false)
  }, [load])

  useEffect(() => { load() }, [load])

  const ticketsFiltrados = catFiltro
    ? tickets.filter(t => (t.serviceSecond || t.serviceFirst || '').toLowerCase().includes(catFiltro.toLowerCase()))
    : tickets

  const categorias = [...new Set(tickets.map(t => t.serviceSecond || t.serviceFirst || '').filter(Boolean))]

  // Agrupa respostas por categoria
  const rpPorCat = respostas.reduce((acc, r) => {
    acc[r.categoria] = acc[r.categoria] || []
    acc[r.categoria].push(r)
    return acc
  }, {})

  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">
      {/* Header */}
      <div className="flex-shrink-0 px-6 pt-5 pb-3 border-b border-border">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-text font-semibold text-lg">Painel do Analista</h1>
            <p className="text-text-dim text-xs mt-0.5">
              {analista ? `${analista} · ` : ''}
              {loading ? 'carregando...' : `${tickets.length} chamado${tickets.length !== 1 ? 's' : ''} em aberto`}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={syncAbertos} disabled={syncing || loading}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-50"
              title="Busca todos os chamados em aberto no Movidesk, incluindo tickets antigos fora da janela de sync">
              <RefreshCw size={13} className={syncing ? 'animate-spin' : ''} />
              {syncing ? 'Sincronizando...' : 'Sync fila'}
            </button>
            <button onClick={load} disabled={loading || syncing}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-50">
              <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
              Atualizar
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mt-3">
          {[
            { key: 'fila',      label: `Minha Fila (${tickets.length})` },
            { key: 'respostas', label: `Respostas Rápidas (${respostas.length})` },
          ].map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors
                ${tab === t.key
                  ? 'bg-accent/20 text-accent border-accent/30'
                  : 'bg-surface2 text-text-dim border-border hover:text-text'}`}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4 select-text">

        {/* FILA */}
        {tab === 'fila' && (
          <div className="space-y-3">
            {/* Filtro rápido por categoria */}
            {categorias.length > 1 && (
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-text-dim text-xs">Categoria:</span>
                <button onClick={() => setCatFiltro('')}
                  className={`px-2 py-0.5 rounded text-xs border transition-colors
                    ${!catFiltro ? 'bg-accent/20 text-accent border-accent/30' : 'bg-surface2 text-text-dim border-border hover:text-text'}`}>
                  Todas
                </button>
                {categorias.map(c => (
                  <button key={c} onClick={() => setCatFiltro(c === catFiltro ? '' : c)}
                    className={`px-2 py-0.5 rounded text-xs border transition-colors whitespace-nowrap
                      ${catFiltro === c ? 'bg-accent/20 text-accent border-accent/30' : 'bg-surface2 text-text-dim border-border hover:text-text'}`}>
                    {c}
                  </button>
                ))}
              </div>
            )}

            {/* Legenda de urgência */}
            <div className="flex items-center gap-3 text-[10px] text-text-dim pb-1">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-success inline-block" /> Hoje</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-warning inline-block" /> 1–2 dias</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-orange-400 inline-block" /> 3–6 dias</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-error inline-block" /> 7+ dias</span>
            </div>

            {loading ? (
              <p className="text-text-dim text-sm py-8 text-center">Carregando chamados...</p>
            ) : ticketsFiltrados.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <CheckCircle size={32} className="text-success/50" />
                <p className="text-text-dim text-sm">Nenhum chamado em aberto</p>
                {!analista && (
                  <p className="text-text-muted text-xs max-w-sm">
                    Configure seu "Nome no Movidesk" em Usuários para ver sua fila.
                  </p>
                )}
              </div>
            ) : (
              <div className="space-y-2">
                {ticketsFiltrados.map(t => <TicketCard key={t.id} t={t} />)}
              </div>
            )}
          </div>
        )}

        {/* RESPOSTAS RÁPIDAS */}
        {tab === 'respostas' && (
          <div className="space-y-4">
            {Object.keys(rpPorCat).length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <AlertCircle size={32} className="text-text-dim/40" />
                <p className="text-text-dim text-sm">Nenhuma resposta rápida disponível ainda</p>
                <p className="text-text-muted text-xs">Use "Extrair com IA" no Gestão para gerar a base de soluções</p>
              </div>
            ) : (
              Object.entries(rpPorCat).map(([cat, itens]) => (
                <div key={cat}>
                  <p className="text-[10px] font-semibold uppercase tracking-wider text-text-dim mb-2">{cat}</p>
                  <div className="space-y-1.5">
                    {itens.map((r, i) => (
                      <div key={i} className="flex items-start gap-2 bg-surface2 border border-border rounded-lg px-3 py-2.5">
                        <div className="flex-1 min-w-0">
                          <p className="text-text text-sm leading-relaxed">{r.solucao}</p>
                          <p className="text-text-muted text-[10px] mt-0.5">usado {r.frequencia}x</p>
                        </div>
                        <CopyBtn text={r.solucao} />
                      </div>
                    ))}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}
