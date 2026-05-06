import { useState, useEffect, useCallback } from 'react'
import { RefreshCw, ExternalLink, AlertCircle, Clock, CheckCircle2, Circle,
         ChevronRight, X, Paperclip, MessageSquare, User, Calendar,
         Tag, Download, Link2, GitBranch, Zap, Package, Sparkles, Send } from 'lucide-react'
import api from '../api/backend'

// ── Helpers ───────────────────────────────────────────────────────────────────

const COLUNAS = [
  { key: 'new',          label: 'A Fazer',      cats: ['new','undefined',''], icon: Circle,       color: 'text-text-dim',  bg: 'bg-surface2/40', border: 'border-border',      dot: 'bg-text-dim',  header: 'bg-surface2/60' },
  { key: 'indeterminate',label: 'Em Andamento', cats: ['indeterminate'],      icon: Clock,        color: 'text-warning',   bg: 'bg-warning/5',   border: 'border-warning/20',  dot: 'bg-warning',   header: 'bg-warning/10'  },
  { key: 'done',         label: 'Finalizado',   cats: ['done'],              icon: CheckCircle2, color: 'text-success',   bg: 'bg-success/5',   border: 'border-success/20',  dot: 'bg-success',   header: 'bg-success/10'  },
]

const TIPO_COLORS = {
  'Bug':      'bg-red-500/15 text-red-400 border-red-500/20',
  'Defeito':  'bg-red-500/15 text-red-400 border-red-500/20',
  'Melhoria': 'bg-blue-500/15 text-blue-400 border-blue-500/20',
  'Tarefa':   'bg-purple-500/15 text-purple-400 border-purple-500/20',
  'História': 'bg-cyan-500/15 text-cyan-400 border-cyan-500/20',
  'Epic':     'bg-orange-500/15 text-orange-400 border-orange-500/20',
}

const PRIO_MAP = {
  'Highest': { symbol: '↑↑', cls: 'text-red-400' },
  'High':    { symbol: '↑',  cls: 'text-orange-400' },
  'Medium':  { symbol: '–',  cls: 'text-yellow-400' },
  'Low':     { symbol: '↓',  cls: 'text-blue-400' },
  'Lowest':  { symbol: '↓↓', cls: 'text-text-muted' },
}

function MetaItem({ icon: Icon, label, value }) {
  if (!value) return null
  return (
    <div className="flex items-start gap-2 text-xs">
      <Icon size={13} className="text-text-muted mt-0.5 flex-shrink-0" />
      <span className="text-text-muted min-w-[80px] flex-shrink-0">{label}</span>
      <span className="text-text">{value}</span>
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div className="space-y-2">
      <p className="text-[10px] font-semibold text-text-muted uppercase tracking-wider border-b border-border pb-1">{title}</p>
      {children}
    </div>
  )
}

// ── Card do Kanban ────────────────────────────────────────────────────────────

function TarefaCard({ t, onClick }) {
  const tipoClass = TIPO_COLORS[t.tipo] || 'bg-surface2 text-text-dim border-border'
  const prio = PRIO_MAP[t.prioridade] || null
  return (
    <button onClick={() => onClick(t.id)}
      className="w-full text-left group bg-surface rounded-xl border border-border hover:border-accent/40 hover:shadow-lg hover:shadow-accent/5 transition-all p-3 space-y-2">
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-[10px] text-text-muted">{t.id}</span>
        {prio && <span className={`text-[11px] font-bold ${prio.cls}`}>{prio.symbol}</span>}
      </div>
      <p className="text-text text-sm leading-snug line-clamp-3">{t.titulo}</p>
      <div className="flex items-center gap-1.5 flex-wrap">
        {t.tipo && <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-md border ${tipoClass}`}>{t.tipo}</span>}
      </div>
      <div className="flex items-center justify-between text-[10px] text-text-muted">
        <span className="truncate max-w-[130px]">{t.responsavel || '—'}</span>
        <span>{t.atualizado}</span>
      </div>
    </button>
  )
}

function Coluna({ col, tarefas, onCardClick }) {
  const Icon = col.icon
  return (
    <div className={`flex flex-col rounded-2xl border ${col.border} overflow-hidden min-h-0`}>
      <div className={`px-4 py-3 border-b border-border/50 flex items-center gap-2 flex-shrink-0 ${col.header}`}>
        <div className={`w-2 h-2 rounded-full ${col.dot}`} />
        <Icon size={14} className={col.color} />
        <span className={`text-sm font-semibold ${col.color}`}>{col.label}</span>
        <span className="ml-auto text-xs font-bold text-text-muted bg-surface/60 px-2 py-0.5 rounded-full border border-border/50">{tarefas.length}</span>
      </div>
      <div className={`flex-1 overflow-y-auto p-3 space-y-2 ${col.bg}`}>
        {tarefas.length === 0
          ? <div className="flex items-center justify-center py-8"><p className="text-text-muted text-xs">Nenhuma tarefa</p></div>
          : tarefas.map(t => <TarefaCard key={t.id} t={t} onClick={onCardClick} />)
        }
      </div>
    </div>
  )
}

// ── Modal de detalhe ──────────────────────────────────────────────────────────

function DetalheModal({ issueKey, onClose, onSendToChat }) {
  const [d, setD]               = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [lightbox, setLightbox] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysis, setAnalysis]   = useState(null)  // { resposta, issue_text, titulo }
  const [analysisErr, setAnalysisErr] = useState('')

  useEffect(() => {
    setLoading(true); setError(''); setD(null); setAnalysis(null); setAnalysisErr('')
    api.tarefaDetail(issueKey)
      .then(r => setD(r.data))
      .catch(e => setError(e?.response?.data?.error || 'Erro ao carregar'))
      .finally(() => setLoading(false))
  }, [issueKey])

  useEffect(() => {
    const h = e => { if (e.key === 'Escape') lightbox ? setLightbox(null) : onClose() }
    window.addEventListener('keydown', h)
    return () => window.removeEventListener('keydown', h)
  }, [onClose, lightbox])

  const handleAnalisar = async () => {
    setAnalyzing(true); setAnalysisErr(''); setAnalysis(null)
    try {
      const { data } = await api.analisarTarefa(issueKey)
      setAnalysis(data)
    } catch (e) {
      setAnalysisErr(e?.response?.data?.error || 'Erro ao analisar')
    } finally {
      setAnalyzing(false)
    }
  }

  const handleContinuarChat = () => {
    if (!analysis) return
    onSendToChat && onSendToChat([
      {
        role: 'user',
        content: `Analise a issue ${issueKey} do Jira: ${analysis.titulo}\n\n${analysis.issue_text}`,
        timestamp: Date.now(),
      },
      {
        role: 'assistant',
        content: analysis.resposta,
        timestamp: Date.now(),
      },
    ])
    onClose()
  }

  const tipoClass = d ? (TIPO_COLORS[d.tipo] || 'bg-surface2 text-text-dim border-border') : ''
  const prio      = d ? (PRIO_MAP[d.prioridade] || null) : null

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm" onClick={onClose} />

      {/* Painel lateral */}
      <div className="fixed inset-y-0 right-0 z-50 w-[680px] max-w-full bg-bg border-l border-border flex flex-col shadow-2xl overflow-hidden">

        {/* Header */}
        <div className="flex items-start gap-3 px-5 py-4 border-b border-border flex-shrink-0 bg-surface/30">
          <div className="flex-1 min-w-0">
            {loading
              ? <div className="h-4 bg-surface2 rounded animate-pulse w-2/3" />
              : d && (
                <>
                  <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                    <span className="font-mono text-xs text-text-muted">{d.key}</span>
                    {d.tipo && <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-md border ${tipoClass}`}>{d.tipo}</span>}
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-surface2 text-text-dim border border-border">{d.status}</span>
                    {d.resolucao && <span className="text-[10px] px-2 py-0.5 rounded-full bg-success/10 text-success border border-success/20">{d.resolucao}</span>}
                    {prio && <span className={`text-[11px] font-bold ${prio.cls}`}>{prio.symbol} {d.prioridade}</span>}
                  </div>
                  <p className="text-text font-semibold text-sm leading-snug">{d.titulo}</p>
                </>
              )
            }
          </div>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            {d && !loading && (
              <button
                onClick={handleAnalisar}
                disabled={analyzing}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-accent/10 hover:bg-accent/20 border border-accent/30 rounded-lg text-accent text-xs font-medium transition-colors disabled:opacity-50"
                title="Analisar esta issue com IA"
              >
                <Sparkles size={12} className={analyzing ? 'animate-pulse' : ''} />
                {analyzing ? 'Analisando...' : 'Analisar com IA'}
              </button>
            )}
            {d && (
              <a href={d.url} target="_blank" rel="noopener noreferrer"
                className="p-1.5 text-text-dim hover:text-accent rounded-lg hover:bg-surface transition-colors" title="Abrir no Jira">
                <ExternalLink size={14} />
              </a>
            )}
            <button onClick={onClose} className="p-1.5 text-text-dim hover:text-error rounded-lg hover:bg-surface transition-colors"><X size={16} /></button>
          </div>
        </div>

        {/* Corpo */}
        <div className="flex-1 overflow-y-auto select-text">
          {loading && (
            <div className="flex items-center justify-center h-40">
              <div className="w-6 h-6 border-2 border-accent/30 border-t-accent rounded-full animate-spin" />
            </div>
          )}
          {error && (
            <div className="m-4 flex items-center gap-2 bg-error/10 border border-error/20 rounded-xl px-4 py-3 text-error text-xs">
              <AlertCircle size={14} />{error}
            </div>
          )}

          {/* Painel de análise IA */}
          {analyzing && (
            <div className="mx-5 mt-4 flex items-center gap-3 bg-accent/5 border border-accent/20 rounded-xl px-4 py-3">
              <Sparkles size={14} className="text-accent animate-pulse flex-shrink-0" />
              <p className="text-text-dim text-xs">Analisando issue, descrição, comentários e imagens...</p>
            </div>
          )}
          {analysisErr && (
            <div className="mx-5 mt-4 flex items-center gap-2 bg-error/10 border border-error/20 rounded-xl px-4 py-3 text-error text-xs">
              <AlertCircle size={14} />{analysisErr}
            </div>
          )}
          {analysis && (
            <div className="mx-5 mt-4 bg-accent/5 border border-accent/20 rounded-xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2.5 border-b border-accent/15">
                <div className="flex items-center gap-2">
                  <Sparkles size={13} className="text-accent" />
                  <span className="text-accent text-xs font-semibold">Análise IA</span>
                  {analysis.tem_imagem && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-accent/10 border border-accent/20 rounded text-accent">+ imagem</span>
                  )}
                </div>
                {onSendToChat && (
                  <button
                    onClick={handleContinuarChat}
                    className="flex items-center gap-1.5 px-2.5 py-1 bg-accent hover:bg-accent-hover text-white rounded-lg text-[10px] font-medium transition-colors"
                  >
                    <Send size={10} /> Continuar no Chat
                  </button>
                )}
              </div>
              <div className="px-4 py-3 text-sm text-text leading-relaxed whitespace-pre-wrap selectable">
                {analysis.resposta}
              </div>
            </div>
          )}

          {d && !loading && (
            <div className="p-5 space-y-6">

              {/* ── Detalhes ── */}
              <Section title="Detalhes">
                <div className="grid grid-cols-1 gap-2">
                  <MetaItem icon={User}     label="Responsável"  value={d.responsavel} />
                  <MetaItem icon={User}     label="Reporter"     value={d.reporter} />
                  <MetaItem icon={Calendar} label="Criado"       value={d.criado_em} />
                  <MetaItem icon={Calendar} label="Atualizado"   value={d.atualizado} />
                  {d.sprint      && <MetaItem icon={Zap}      label="Sprint"       value={d.sprint} />}
                  {d.story_points && <MetaItem icon={GitBranch} label="Story Points" value={String(d.story_points)} />}
                  {d.components && d.components.length > 0 && (
                    <MetaItem icon={Tag} label="Componentes" value={d.components.join(', ')} />
                  )}
                  {d.fix_versions && d.fix_versions.length > 0 && (
                    <MetaItem icon={Tag} label="Fix Version" value={d.fix_versions.join(', ')} />
                  )}
                  {d.labels && d.labels.length > 0 && (
                    <div className="flex items-start gap-2 text-xs">
                      <Tag size={13} className="text-text-muted mt-0.5 flex-shrink-0" />
                      <span className="text-text-muted min-w-[80px] flex-shrink-0">Labels</span>
                      <div className="flex flex-wrap gap-1">
                        {d.labels.map(l => (
                          <span key={l} className="text-[10px] px-1.5 py-0.5 bg-surface2 border border-border rounded-full text-text-dim">{l}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Section>

              {/* ── Descrição ── */}
              {d.descricao && (
                <Section title="Descrição">
                  <div
                    className="jira-html text-sm text-text leading-relaxed bg-surface rounded-xl border border-border p-4"
                    dangerouslySetInnerHTML={{ __html: d.descricao }}
                  />
                </Section>
              )}

              {/* ── Links ── */}
              {d.links && d.links.length > 0 && (
                <Section title={`Issues relacionadas (${d.links.length})`}>
                  <div className="space-y-1.5">
                    {d.links.map((l, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs bg-surface rounded-lg border border-border px-3 py-2">
                        <Link2 size={11} className="text-text-muted flex-shrink-0" />
                        <span className="text-text-muted">{l.tipo}</span>
                        <span className="font-mono text-accent">{l.key}</span>
                        <span className="text-text truncate flex-1">{l.titulo}</span>
                        <span className="text-text-muted text-[10px] flex-shrink-0">{l.status}</span>
                      </div>
                    ))}
                  </div>
                </Section>
              )}

              {/* ── Subtasks ── */}
              {d.subtasks && d.subtasks.length > 0 && (
                <Section title={`Subtarefas (${d.subtasks.length})`}>
                  <div className="space-y-1.5">
                    {d.subtasks.map((s, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs bg-surface rounded-lg border border-border px-3 py-2">
                        <span className="font-mono text-accent">{s.key}</span>
                        <span className="text-text truncate flex-1">{s.titulo}</span>
                        <span className="text-text-muted text-[10px]">{s.status}</span>
                      </div>
                    ))}
                  </div>
                </Section>
              )}

              {/* ── Anexos ── */}
              {d.anexos && d.anexos.length > 0 && (
                <Section title={`Anexos (${d.anexos.length})`}>
                  <div className="grid grid-cols-2 gap-2">
                    {d.anexos.map(a => (
                      a.eh_imagem ? (
                        <button key={a.id} onClick={() => setLightbox(a.url)}
                          className="rounded-xl overflow-hidden border border-border hover:border-accent/40 transition-all group bg-surface text-left">
                          <img
                            src={a.url} alt=""
                            className="w-full h-36 object-cover group-hover:scale-105 transition-transform duration-200"
                            onError={e => { e.target.style.display = 'none' }}
                          />
                          <p className="text-[10px] text-text-muted px-2 py-1.5 truncate">{a.nome}</p>
                        </button>
                      ) : (
                        <a key={a.id} href={a.url} target="_blank" rel="noopener noreferrer"
                          className="flex items-center gap-2 p-3 bg-surface rounded-xl border border-border hover:border-accent/40 transition-all">
                          <Download size={14} className="text-text-dim flex-shrink-0" />
                          <div className="min-w-0">
                            <p className="text-xs text-text truncate">{a.nome}</p>
                            <p className="text-[10px] text-text-muted">{(a.tamanho / 1024).toFixed(1)} KB</p>
                          </div>
                        </a>
                      )
                    ))}
                  </div>
                </Section>
              )}

              {/* ── Comentários ── */}
              {d.comentarios && d.comentarios.length > 0 && (
                <Section title={`Comentários (${d.comentarios.length})`}>
                  <div className="space-y-3">
                    {d.comentarios.map((c, i) => (
                      <div key={i} className="bg-surface rounded-xl border border-border p-4">
                        <div className="flex items-center gap-2 mb-3">
                          <div className="w-7 h-7 rounded-full bg-accent/20 flex items-center justify-center flex-shrink-0">
                            <span className="text-[11px] font-bold text-accent">{(c.autor || '?')[0].toUpperCase()}</span>
                          </div>
                          <div>
                            <p className="text-xs font-semibold text-text">{c.autor}</p>
                            <p className="text-[10px] text-text-muted">{c.criado}</p>
                          </div>
                        </div>
                        <div
                          className="jira-html text-sm text-text-dim leading-relaxed"
                          dangerouslySetInnerHTML={{ __html: c.corpo }}
                        />
                      </div>
                    ))}
                  </div>
                </Section>
              )}

            </div>
          )}
        </div>
      </div>

      {/* Lightbox */}
      {lightbox && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/90 backdrop-blur-sm"
          onClick={() => setLightbox(null)}>
          <img
            src={lightbox} alt=""
            className="max-w-[92vw] max-h-[92vh] rounded-2xl shadow-2xl object-contain select-none"
            onClick={e => e.stopPropagation()}
          />
          <button
            className="absolute top-5 right-5 p-2.5 bg-black/60 rounded-full text-white hover:bg-black/80 transition-colors border border-white/10"
            onClick={() => setLightbox(null)}>
            <X size={20} />
          </button>
        </div>
      )}
    </>
  )
}

// ── Página principal ──────────────────────────────────────────────────────────

const TABS_TAREFAS = [
  { key: 'kanban',      label: 'Kanban',      icon: Circle },
  { key: 'nova-versao', label: 'Nova Versão', icon: Package },
]

export default function Tarefas({ onSendToChat }) {
  const [tab, setTab]                 = useState('kanban')
  const [tarefas, setTarefas]         = useState([])
  const [loading, setLoading]         = useState(true)
  const [error, setError]             = useState('')
  const [filtro, setFiltro]           = useState('')
  const [tipoFiltro, setTipo]         = useState('')
  const [selectedKey, setSelectedKey] = useState(null)

  // Nova Versão — sprint ativo (somente leitura Jira)
  const [sprintIssues, setSprintIssues] = useState([])
  const [sprintName,   setSprintName]   = useState('')
  const [loadingNV,    setLoadingNV]    = useState(false)

  const carregar = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const { data } = await api.tarefas()
      setTarefas(Array.isArray(data) ? data : [])
    } catch (e) {
      setError(e?.response?.data?.error || 'Erro ao carregar tarefas')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleLoadNovaVersao = useCallback(async () => {
    setLoadingNV(true)
    try {
      const { data } = await api.gestaoNovaVersao()
      setSprintIssues(data.issues || [])
      setSprintName(data.sprint_name || '')
    } catch {}
    setLoadingNV(false)
  }, [])

  useEffect(() => { carregar() }, [carregar])

  useEffect(() => {
    if (tab === 'nova-versao') handleLoadNovaVersao()
  }, [tab]) // eslint-disable-line

  const tipos     = [...new Set(tarefas.map(t => t.tipo).filter(Boolean))]
  const filtradas = tarefas.filter(t => {
    const q = filtro.toLowerCase()
    return (!q || t.titulo.toLowerCase().includes(q) || t.id.toLowerCase().includes(q))
        && (!tipoFiltro || t.tipo === tipoFiltro)
  })
  const porColuna = col => filtradas.filter(t => col.cats.includes(t.status_cat || ''))

  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">
      {/* CSS para HTML do Jira */}
      <style>{`
        .jira-html p { margin-bottom: 0.5rem; }
        .jira-html ul, .jira-html ol { padding-left: 1.25rem; margin-bottom: 0.5rem; }
        .jira-html li { margin-bottom: 0.2rem; }
        .jira-html a { color: #818cf8; text-decoration: underline; word-break: break-all; }
        .jira-html code { background: rgba(255,255,255,0.08); padding: 0.1rem 0.35rem; border-radius: 4px; font-size: 0.82em; font-family: monospace; }
        .jira-html pre { background: rgba(255,255,255,0.06); padding: 0.75rem 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.8em; margin-bottom: 0.5rem; }
        .jira-html strong, .jira-html b { font-weight: 600; }
        .jira-html em, .jira-html i { font-style: italic; }
        .jira-html img { max-width: 100%; border-radius: 8px; margin: 0.5rem 0; cursor: pointer; display: block; }
        .jira-html table { border-collapse: collapse; width: 100%; font-size: 0.82em; margin-bottom: 0.5rem; }
        .jira-html th, .jira-html td { border: 1px solid rgba(255,255,255,0.1); padding: 0.4rem 0.6rem; }
        .jira-html th { background: rgba(255,255,255,0.06); font-weight: 600; }
        .jira-html blockquote { border-left: 3px solid rgba(255,255,255,0.2); padding-left: 0.75rem; opacity: 0.75; margin: 0.5rem 0; }
        .jira-html h1,.jira-html h2,.jira-html h3 { font-weight: 600; margin-bottom: 0.4rem; color: inherit; }
        .jira-html h1 { font-size: 1.1em; } .jira-html h2 { font-size: 1em; } .jira-html h3 { font-size: 0.95em; }
        .jira-html del { text-decoration: line-through; opacity: 0.6; }
        .jira-html hr { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0; }
      `}</style>

      {/* Topo */}
      <div className="flex items-center gap-3 px-5 py-3 border-b border-border flex-shrink-0">
        <div>
          <h1 className="text-text font-semibold text-sm">Tarefas — FarmaFácil</h1>
          <p className="text-text-muted text-[10px]">Desenvolvimento-delphi · somente visualização</p>
        </div>
        {tab === 'kanban' && (
          <div className="flex items-center gap-2 ml-auto">
            <input
              type="text" placeholder="Buscar..."
              value={filtro} onChange={e => setFiltro(e.target.value)}
              className="bg-surface border border-border rounded-lg px-3 py-1.5 text-xs text-text outline-none focus:border-accent transition-colors w-40"
            />
            {tipos.length > 0 && (
              <select value={tipoFiltro} onChange={e => setTipo(e.target.value)}
                className="bg-surface border border-border rounded-lg px-2 py-1.5 text-xs text-text outline-none focus:border-accent transition-colors">
                <option value="">Todos</option>
                {tipos.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            )}
            <button onClick={carregar} disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-surface border border-border rounded-lg text-xs text-text-dim hover:text-text hover:border-accent/40 transition-all disabled:opacity-50">
              <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
              Atualizar
            </button>
          </div>
        )}
        {tab === 'nova-versao' && (
          <button onClick={handleLoadNovaVersao} disabled={loadingNV}
            className="ml-auto flex items-center gap-1.5 px-3 py-1.5 bg-surface border border-border rounded-lg text-xs text-text-dim hover:text-text hover:border-accent/40 transition-all disabled:opacity-50">
            <RefreshCw size={12} className={loadingNV ? 'animate-spin' : ''} />
            {loadingNV ? 'Carregando...' : 'Atualizar'}
          </button>
        )}
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 px-5 py-2 border-b border-border flex-shrink-0">
        {TABS_TAREFAS.map(t => {
          const Icon = t.icon
          const active = tab === t.key
          return (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                active ? 'bg-accent/15 text-accent border border-accent/30' : 'text-text-dim hover:text-text hover:bg-surface2'
              }`}>
              <Icon size={12} />
              {t.label}
            </button>
          )
        })}
      </div>

      {/* ── Kanban ── */}
      {tab === 'kanban' && (
        <>
          {error && (
            <div className="mx-5 mt-3 flex items-center gap-2 bg-error/10 border border-error/20 rounded-xl px-4 py-2.5 text-error text-xs flex-shrink-0">
              <AlertCircle size={14} />{error}
            </div>
          )}
          {loading && !error ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center space-y-3">
                <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin mx-auto" />
                <p className="text-text-muted text-xs">Carregando tarefas...</p>
              </div>
            </div>
          ) : !error && (
            <div className="flex-1 overflow-hidden px-4 py-4">
              <div className="grid grid-cols-3 gap-4 h-full">
                {COLUNAS.map(col => (
                  <Coluna key={col.key} col={col} tarefas={porColuna(col)} onCardClick={setSelectedKey} />
                ))}
              </div>
            </div>
          )}
          {!loading && !error && (
            <div className="px-5 py-2 border-t border-border flex-shrink-0 flex items-center gap-1 text-[10px] text-text-muted">
              <span>{filtradas.length} de {tarefas.length} tarefas</span>
              <ChevronRight size={10} />
              <span>Clique num card para ver todos os detalhes</span>
            </div>
          )}
        </>
      )}

      {/* ── Nova Versão ── */}
      {tab === 'nova-versao' && (
        <div className="flex-1 overflow-y-auto px-5 py-4 space-y-4">
          {sprintName && (
            <p className="text-text-dim text-xs">
              Sprint em andamento: <span className="text-accent font-medium">{sprintName}</span>
            </p>
          )}
          {loadingNV ? (
            <div className="flex items-center justify-center py-16">
              <div className="text-center space-y-3">
                <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin mx-auto" />
                <p className="text-text-muted text-xs">Buscando issues do sprint...</p>
              </div>
            </div>
          ) : sprintIssues.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center space-y-2">
              <Package size={32} className="text-text-muted/40" />
              <p className="text-text-dim text-sm">Nenhuma issue encontrada no sprint ativo</p>
              <p className="text-text-muted text-xs">Clique em "Atualizar" para buscar</p>
            </div>
          ) : (() => {
            const STATUS_CONFIG = {
              indeterminate: { label: 'Em Andamento', color: 'text-warning', bg: 'bg-warning/10', border: 'border-warning/20', dot: 'bg-warning' },
              new:           { label: 'A Fazer',      color: 'text-text-dim', bg: 'bg-surface2',   border: 'border-border',       dot: 'bg-text-muted' },
              done:          { label: 'Concluído',    color: 'text-success',  bg: 'bg-success/10',  border: 'border-success/20',   dot: 'bg-success' },
            }
            const TIPO_COLOR = {
              Bug:      'bg-error/15 text-error border-error/25',
              Melhoria: 'bg-blue-500/15 text-blue-400 border-blue-500/25',
              Story:    'bg-accent/15 text-accent border-accent/25',
              Tarefa:   'bg-text-dim/15 text-text-dim border-text-dim/25',
            }
            const grouped = {}
            for (const iss of sprintIssues) {
              const cat = iss.status_cat || 'new'
              if (!grouped[cat]) grouped[cat] = []
              grouped[cat].push(iss)
            }
            const ORDER = ['indeterminate', 'new', 'done']
            return (
              <div className="space-y-5">
                {ORDER.filter(k => grouped[k]?.length).map(cat => {
                  const cfg = STATUS_CONFIG[cat] || STATUS_CONFIG.new
                  return (
                    <div key={cat}>
                      <div className="flex items-center gap-2 mb-2">
                        <div className={`w-2 h-2 rounded-full ${cfg.dot}`} />
                        <span className={`text-xs font-bold uppercase tracking-wider ${cfg.color}`}>
                          {cfg.label} — {grouped[cat].length}
                        </span>
                      </div>
                      <div className="space-y-2">
                        {grouped[cat].map(iss => {
                          const tipoCls = TIPO_COLOR[iss.tipo] || TIPO_COLOR.Tarefa
                          return (
                            <div key={iss.key}
                              className={`flex items-start gap-3 px-4 py-3 rounded-xl border ${cfg.bg} ${cfg.border}`}>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 flex-wrap mb-0.5">
                                  <span className="text-text-muted font-mono text-xs">{iss.key}</span>
                                  <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded border ${tipoCls}`}>
                                    {iss.tipo}
                                  </span>
                                  {iss.responsavel && (
                                    <span className="text-text-muted text-[10px]">{iss.responsavel}</span>
                                  )}
                                </div>
                                <p className="text-text text-sm leading-snug">{iss.titulo}</p>
                              </div>
                              <a href={iss.url} target="_blank" rel="noreferrer"
                                title="Abrir no Jira (somente leitura)"
                                className="flex items-center gap-1 px-2 py-1 bg-accent/10 hover:bg-accent/20 border border-accent/20 rounded-lg text-accent text-[10px] transition-colors flex-shrink-0">
                                <ExternalLink size={10} /> Jira
                              </a>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )
                })}
                <p className="text-text-muted text-[10px] text-center pt-2">
                  Dados do Jira — somente leitura · atualizado a cada 30 min
                </p>
              </div>
            )
          })()}
        </div>
      )}

      {selectedKey && (
        <DetalheModal issueKey={selectedKey} onClose={() => setSelectedKey(null)} onSendToChat={onSendToChat} />
      )}
    </div>
  )
}
