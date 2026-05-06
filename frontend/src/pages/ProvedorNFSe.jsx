import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  AlertTriangle, CheckCircle, XCircle, RefreshCw, ChevronDown, ChevronUp,
  Building2, Search, Filter, ExternalLink, ShieldAlert, X, User, Calendar,
  Tag, Copy, Check, Sparkles, Send, Download, Link2, GitBranch, Zap,
  AlertCircle,
} from 'lucide-react'
import api from '../api/backend'

const JIRA_BASE = 'https://prismadelphi.atlassian.net'

// ── Helpers ────────────────────────────────────────────────────────────────────

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
      <span className="text-text selectable">{value}</span>
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

// ── Modal de detalhe — idêntico ao Tarefas ────────────────────────────────────

function DetalheModal({ issueKey, onClose, onSendToChat }) {
  const [d, setD]               = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [lightbox, setLightbox] = useState(null)
  const [analyzing, setAnalyzing]   = useState(false)
  const [analysis, setAnalysis]     = useState(null)
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
      { role: 'user',      content: `Analise a issue ${issueKey} do Jira: ${analysis.titulo}\n\n${analysis.issue_text}`, timestamp: Date.now() },
      { role: 'assistant', content: analysis.resposta, timestamp: Date.now() },
    ])
    onClose()
  }

  const tipoClass = d ? (TIPO_COLORS[d.tipo] || 'bg-surface2 text-text-dim border-border') : ''
  const prio      = d ? (PRIO_MAP[d.prioridade] || null) : null

  return (
    <>
      <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm" onClick={onClose} />

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
              >
                <Sparkles size={12} className={analyzing ? 'animate-pulse' : ''} />
                {analyzing ? 'Analisando...' : 'Analisar com IA'}
              </button>
            )}
            {d && (
              <a href={`${JIRA_BASE}/browse/${d.key}`} target="_blank" rel="noopener noreferrer"
                className="p-1.5 text-text-dim hover:text-accent rounded-lg hover:bg-surface transition-colors" title="Abrir no Jira">
                <ExternalLink size={14} />
              </a>
            )}
            <button onClick={onClose} className="p-1.5 text-text-dim hover:text-error rounded-lg hover:bg-surface transition-colors">
              <X size={16} />
            </button>
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

          {/* Análise IA */}
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
                  <button onClick={handleContinuarChat}
                    className="flex items-center gap-1.5 px-2.5 py-1 bg-accent hover:bg-accent-hover text-white rounded-lg text-[10px] font-medium transition-colors">
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
              <Section title="Detalhes">
                <div className="grid grid-cols-1 gap-2">
                  <MetaItem icon={User}     label="Responsável"  value={d.responsavel} />
                  <MetaItem icon={User}     label="Reporter"     value={d.reporter} />
                  <MetaItem icon={Calendar} label="Criado"       value={d.criado_em} />
                  <MetaItem icon={Calendar} label="Atualizado"   value={d.atualizado} />
                  {d.sprint       && <MetaItem icon={Zap}       label="Sprint"       value={d.sprint} />}
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

              {d.descricao && (
                <Section title="Descrição">
                  <div
                    className="jira-html text-sm text-text leading-relaxed bg-surface rounded-xl border border-border p-4"
                    dangerouslySetInnerHTML={{ __html: d.descricao }}
                  />
                </Section>
              )}

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

              {d.anexos && d.anexos.length > 0 && (
                <Section title={`Anexos (${d.anexos.length})`}>
                  <div className="grid grid-cols-2 gap-2">
                    {d.anexos.map(a => (
                      a.eh_imagem ? (
                        <button key={a.id} onClick={() => setLightbox(a.url)}
                          className="rounded-xl overflow-hidden border border-border hover:border-accent/40 transition-all group bg-surface text-left">
                          <img src={a.url} alt=""
                            className="w-full h-36 object-cover group-hover:scale-105 transition-transform duration-200"
                            onError={e => { e.target.style.display = 'none' }} />
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
          <img src={lightbox} alt=""
            className="max-w-[92vw] max-h-[92vh] rounded-2xl shadow-2xl object-contain select-none"
            onClick={e => e.stopPropagation()} />
          <button className="absolute top-5 right-5 p-2.5 bg-black/60 rounded-full text-white hover:bg-black/80 transition-colors border border-white/10"
            onClick={() => setLightbox(null)}>
            <X size={20} />
          </button>
        </div>
      )}
    </>
  )
}

// ── Badges e cards ────────────────────────────────────────────────────────────

function StatusBadge({ status }) {
  if (status === 'critico')
    return (
      <span className="flex items-center gap-1 px-2 py-0.5 bg-error/20 text-error border border-error/30 rounded-full text-[10px] font-semibold">
        <XCircle size={10} /> Crítico
      </span>
    )
  if (status === 'alerta')
    return (
      <span className="flex items-center gap-1 px-2 py-0.5 bg-warning/20 text-warning border border-warning/30 rounded-full text-[10px] font-semibold">
        <AlertTriangle size={10} /> Alerta
      </span>
    )
  return (
    <span className="flex items-center gap-1 px-2 py-0.5 bg-success/10 text-success border border-success/20 rounded-full text-[10px] font-semibold">
      <CheckCircle size={10} /> OK
    </span>
  )
}

function StatCard({ label, value, sub, color = 'text-text', bg = 'bg-surface', border = 'border-border' }) {
  return (
    <div className={`${bg} border ${border} rounded-xl p-4`}>
      <p className="text-text-muted text-[10px] uppercase tracking-wider font-semibold">{label}</p>
      <p className={`${color} text-3xl font-bold mt-1`}>{value}</p>
      {sub && <p className="text-text-muted text-[10px] mt-1">{sub}</p>}
    </div>
  )
}

function ProvedorCard({ provedor, onIssueClick, buscaFarmacia }) {
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    if (buscaFarmacia) setExpanded(true)
  }, [buscaFarmacia])

  const farmaciasFiltradas = buscaFarmacia
    ? provedor.farmacias.filter(f =>
        f.nome.toLowerCase().includes(buscaFarmacia.toLowerCase()) ||
        f.municipio.toLowerCase().includes(buscaFarmacia.toLowerCase())
      )
    : provedor.farmacias

  const borderColor =
    provedor.status === 'critico' ? 'border-error/40' :
    provedor.status === 'alerta'  ? 'border-warning/30' :
    'border-border'
  const bgColor =
    provedor.status === 'critico' ? 'bg-error/5' :
    provedor.status === 'alerta'  ? 'bg-warning/5' :
    'bg-surface'

  return (
    <div className={`rounded-xl border ${borderColor} ${bgColor} overflow-hidden`}>
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-surface/40 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <StatusBadge status={provedor.status} />
          <span className="text-text font-medium text-sm">{provedor.nome}</span>
          {provedor.issues.length > 0 && (
            <span className="text-[10px] text-error bg-error/10 px-1.5 py-0.5 rounded-full">
              {provedor.issues.length} issue{provedor.issues.length > 1 ? 's' : ''}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 text-text-dim">
          <span className="text-[11px]">
            {buscaFarmacia && farmaciasFiltradas.length !== provedor.farmacias.length
              ? <><span className="text-accent font-semibold">{farmaciasFiltradas.length}</span>/{provedor.farmacias.length} farmácia{provedor.farmacias.length !== 1 ? 's' : ''}</>
              : <>{provedor.farmacias.length} farmácia{provedor.farmacias.length !== 1 ? 's' : ''}</>
            }
          </span>
          <span className="text-[11px] text-text-muted">{provedor.total_municipios} mun.</span>
          {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </div>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 space-y-3 border-t border-border/50">

              {provedor.issues.length > 0 && (
                <div className="mt-3 space-y-1.5">
                  <p className="text-[10px] font-semibold text-text-dim uppercase tracking-wider">Issues em aberto</p>
                  {provedor.issues.map(issue => (
                    <button
                      key={issue.key}
                      onClick={() => onIssueClick(issue.key)}
                      className="w-full text-left flex items-start gap-2 p-2.5 bg-surface2 rounded-lg border border-border/50 hover:border-accent/40 hover:bg-surface transition-all"
                    >
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-accent text-[11px] font-mono">{issue.key}</span>
                          <span className={`text-[10px] px-1.5 py-0.5 rounded-full border ${
                            issue.prioridade?.toLowerCase().includes('high') ||
                            issue.prioridade?.toLowerCase().includes('crit') ||
                            issue.prioridade?.toLowerCase().includes('block')
                              ? 'bg-error/10 text-error border-error/20'
                              : 'bg-surface text-text-dim border-border'
                          }`}>{issue.prioridade || 'N/A'}</span>
                          <span className="text-[10px] text-text-muted">{issue.status}</span>
                        </div>
                        <p className="text-text text-xs mt-0.5 leading-snug">{issue.titulo}</p>
                        {(issue.responsavel || issue.atualizado) && (
                          <p className="text-text-muted text-[10px] mt-0.5">
                            {issue.responsavel}{issue.responsavel && issue.atualizado ? ' · ' : ''}{issue.atualizado}
                          </p>
                        )}
                      </div>
                      <ChevronDown size={12} className="text-text-muted flex-shrink-0 mt-1 -rotate-90" />
                    </button>
                  ))}
                </div>
              )}

              {farmaciasFiltradas.length > 0 && (
                <div className="space-y-1">
                  <p className="text-[10px] font-semibold text-text-dim uppercase tracking-wider">
                    Farmácias com NFS-e ({farmaciasFiltradas.length}{buscaFarmacia && farmaciasFiltradas.length !== provedor.farmacias.length ? ` de ${provedor.farmacias.length}` : ''})
                  </p>
                  <div>
                    {farmaciasFiltradas.map((farm, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs text-text-dim py-1.5 border-b border-border/30 last:border-0 selectable">
                        <Building2 size={11} className="flex-shrink-0 text-text-muted" />
                        <span className="flex-1 truncate">{farm.nome || '(sem nome)'}</span>
                        <span className="text-text-muted text-[10px] flex-shrink-0">
                          {farm.municipio}{farm.uf ? ` - ${farm.uf}` : ''}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {buscaFarmacia && farmaciasFiltradas.length === 0 && provedor.farmacias.length > 0 && (
                <p className="text-text-muted text-[10px] py-2 italic">Nenhuma farmácia corresponde ao filtro neste provedor.</p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// ── Página principal ──────────────────────────────────────────────────────────

export default function ProvedorNFSe({ onSendToChat }) {
  const [data, setData]                     = useState(null)
  const [loading, setLoading]               = useState(true)
  const [error, setError]                   = useState('')
  const [buscaFarmacia, setBuscaFarmacia]   = useState('')
  const [buscaProvedor, setBuscaProvedor]   = useState('')
  const [filtroStatus, setFiltroStatus]     = useState('todos')
  const [atualizandoIni, setAtualizandoIni]   = useState(false)
  const [atualizandoJira, setAtualizandoJira] = useState(false)
  const [lastUpdate, setLastUpdate]         = useState(null)
  const [selectedIssueKey, setSelectedIssueKey] = useState(null)
  const [copied, setCopied]                 = useState(false)

  const carregar = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const res = await api.provedorStatus()
      setData(res.data)
      setLastUpdate(new Date())
    } catch (err) {
      setError(err.response?.data?.error || err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { carregar() }, [carregar])
  useEffect(() => {
    const t = setInterval(carregar, 5 * 60 * 1000)
    return () => clearInterval(t)
  }, [carregar])

  const handleAtualizarIni = async () => {
    setAtualizandoIni(true)
    try { await api.provedorAtualizarIni(); await carregar() }
    catch (err) { setError(err.response?.data?.error || err.message) }
    finally { setAtualizandoIni(false) }
  }

  const handleAtualizarJira = async () => {
    setAtualizandoJira(true)
    try { await api.provedorAtualizarJira(); await carregar() }
    catch (err) { setError(err.response?.data?.error || err.message) }
    finally { setAtualizandoJira(false) }
  }

  const provedoresFiltrados = (data?.provedores || []).filter(p => {
    if (filtroStatus === 'alerta' && p.status === 'ok') return false
    if (filtroStatus === 'ok'    && p.status !== 'ok') return false
    if (buscaProvedor && !p.nome.toLowerCase().includes(buscaProvedor.toLowerCase())) return false
    if (buscaFarmacia) {
      const busca = buscaFarmacia.toLowerCase()
      if (!p.farmacias.some(f => f.nome.toLowerCase().includes(busca) || f.municipio.toLowerCase().includes(busca))) return false
    }
    return true
  })

  const handleCopiar = () => {
    const linhas = ['=== PROVEDORES NFS-e — STATUS ===', `Data: ${new Date().toLocaleString('pt-BR')}`, '']
    for (const p of provedoresFiltrados) {
      const emoji = p.status === 'critico' ? '🔴' : p.status === 'alerta' ? '🟡' : '🟢'
      linhas.push(`${emoji} ${p.nome.toUpperCase()} — ${p.farmacias.length} farmácia(s), ${p.total_municipios} municípios`)
      if (p.issues.length > 0) {
        linhas.push('  Issues NFS-e abertas:')
        p.issues.forEach(i => linhas.push(`    [${i.key}] ${i.titulo} (${i.status} · ${i.prioridade})`))
      }
      if (p.farmacias.length > 0) {
        linhas.push('  Farmácias:')
        p.farmacias.forEach(f => linhas.push(`    - ${f.nome} (${f.municipio}${f.uf ? ' - ' + f.uf : ''})`))
      }
      linhas.push('')
    }
    navigator.clipboard.writeText(linhas.join('\n')).catch(() => {})
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  // Stats derivados
  const totalOk      = (data?.provedores || []).filter(p => p.status === 'ok').length
  const totalAlerta  = (data?.provedores || []).filter(p => p.status === 'alerta').length
  const totalCritico = (data?.provedores || []).filter(p => p.status === 'critico').length
  const pctOk = data?.total_provedores > 0
    ? Math.round((totalOk / data.total_provedores) * 100)
    : 0

  return (
    <>
      {/* CSS Jira HTML — idêntico ao Tarefas */}
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
        .jira-html h1,.jira-html h2,.jira-html h3 { font-weight:600; margin-bottom:0.4rem; }
        .jira-html h1 { font-size:1.1em; } .jira-html h2 { font-size:1em; } .jira-html h3 { font-size:0.95em; }
        .jira-html blockquote { border-left:3px solid rgba(255,255,255,0.2); padding-left:0.75rem; color:rgba(255,255,255,0.6); margin-bottom:0.5rem; }
        .jira-html hr { border:none; border-top:1px solid rgba(255,255,255,0.1); margin:0.75rem 0; }
      `}</style>

      <div className="flex flex-col h-full overflow-hidden">

        {/* Modal lateral */}
        <AnimatePresence>
          {selectedIssueKey && (
            <DetalheModal
              issueKey={selectedIssueKey}
              onClose={() => setSelectedIssueKey(null)}
              onSendToChat={onSendToChat}
            />
          )}
        </AnimatePresence>

        {/* Header */}
        <div className="px-5 py-3 border-b border-border bg-surface/40 flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShieldAlert size={16} className="text-accent" />
              <div>
                <h2 className="text-text font-semibold text-sm">Provedores NFS-e</h2>
                <p className="text-text-dim text-xs mt-0.5">Monitoramento de provedores de nota fiscal de serviço</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {lastUpdate && (
                <span className="text-text-muted text-[10px]">
                  {lastUpdate.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                </span>
              )}
              <button onClick={carregar} disabled={loading}
                className="p-1.5 rounded-lg bg-surface2 border border-border hover:border-accent text-text-dim hover:text-accent transition-colors"
                title="Recarregar">
                <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5">

          {loading && !data && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center space-y-2">
                <RefreshCw size={22} className="animate-spin text-accent mx-auto" />
                <p className="text-text-dim text-sm">Carregando...</p>
                <p className="text-text-muted text-xs">Consultando ACBr INI, tickets e Jira</p>
              </div>
            </div>
          )}

          {error && (
            <div className="flex items-start gap-2 p-3 bg-error/10 border border-error/20 rounded-xl text-error text-sm">
              <AlertTriangle size={15} className="flex-shrink-0 mt-0.5" />
              <span className="selectable">{error}</span>
            </div>
          )}

          {data && (
            <>
              {/* ── Dashboard ── */}
              <div className="space-y-3">

                {/* Linha 1: 4 stat cards */}
                <div className="grid grid-cols-4 gap-3">
                  <StatCard
                    label="Provedores monitorados"
                    value={data.total_provedores}
                    sub={`${data.total_municipios_ini} municípios no INI`}
                  />
                  <StatCard
                    label="Farmácias com NFS-e"
                    value={data.total_farmacias_nfse ?? '—'}
                    sub={`de ${data.total_clientes_mv ?? '—'} clientes totais`}
                    color="text-accent"
                  />
                  <StatCard
                    label="Provedores com issues"
                    value={data.com_alerta}
                    sub={data.com_alerta > 0 ? 'requerem atenção' : 'tudo ok'}
                    color={data.com_alerta > 0 ? 'text-warning' : 'text-text'}
                    bg={data.com_alerta > 0 ? 'bg-warning/5' : 'bg-surface'}
                    border={data.com_alerta > 0 ? 'border-warning/30' : 'border-border'}
                  />
                  <StatCard
                    label="Farmácias afetadas"
                    value={data.farmacias_afetadas_total}
                    sub={data.farmacias_afetadas_total > 0 ? 'em risco de impacto' : 'sem impacto atual'}
                    color={data.farmacias_afetadas_total > 0 ? 'text-error' : 'text-text'}
                    bg={data.farmacias_afetadas_total > 0 ? 'bg-error/5' : 'bg-surface'}
                    border={data.farmacias_afetadas_total > 0 ? 'border-error/30' : 'border-border'}
                  />
                </div>

                {/* Linha 2: distribuição de status */}
                <div className="bg-surface border border-border rounded-xl p-4">
                  <div className="flex items-center justify-between mb-3">
                    <p className="text-[10px] font-semibold text-text-muted uppercase tracking-wider">Distribuição de status</p>
                    <div className="flex items-center gap-4 text-[10px] text-text-muted">
                      <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-success inline-block" /> OK: {totalOk}</span>
                      <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-warning inline-block" /> Alerta: {totalAlerta}</span>
                      <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-error inline-block" /> Crítico: {totalCritico}</span>
                    </div>
                  </div>
                  {data.total_provedores > 0 ? (
                    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
                      {totalCritico > 0 && (
                        <div
                          className="bg-error rounded-l-full"
                          style={{ width: `${(totalCritico / data.total_provedores) * 100}%` }}
                          title={`Crítico: ${totalCritico}`}
                        />
                      )}
                      {totalAlerta > 0 && (
                        <div
                          className={`bg-warning ${totalCritico === 0 ? 'rounded-l-full' : ''}`}
                          style={{ width: `${(totalAlerta / data.total_provedores) * 100}%` }}
                          title={`Alerta: ${totalAlerta}`}
                        />
                      )}
                      {totalOk > 0 && (
                        <div
                          className={`bg-success flex-1 ${totalCritico === 0 && totalAlerta === 0 ? 'rounded-l-full' : ''} rounded-r-full`}
                          title={`OK: ${totalOk} (${pctOk}%)`}
                        />
                      )}
                    </div>
                  ) : (
                    <div className="h-3 bg-surface2 rounded-full" />
                  )}
                  <p className="text-text-muted text-[10px] mt-1.5">{pctOk}% dos provedores sem issues NFS-e</p>
                </div>
              </div>

              {/* ── Filtros ── */}
              <div className="flex flex-wrap items-center gap-2">
                <div className="flex items-center gap-1.5 bg-surface2 border border-border rounded-xl px-3 py-1.5 flex-1 min-w-[140px]">
                  <Search size={12} className="text-text-muted flex-shrink-0" />
                  <input type="text" value={buscaProvedor} onChange={e => setBuscaProvedor(e.target.value)}
                    placeholder="Filtrar por provedor..." className="bg-transparent text-text text-xs outline-none flex-1" />
                </div>
                <div className="flex items-center gap-1.5 bg-surface2 border border-border rounded-xl px-3 py-1.5 flex-1 min-w-[170px]">
                  <Building2 size={12} className="text-text-muted flex-shrink-0" />
                  <input type="text" value={buscaFarmacia} onChange={e => setBuscaFarmacia(e.target.value)}
                    placeholder="Filtrar por farmácia ou município..." className="bg-transparent text-text text-xs outline-none flex-1" />
                </div>
                <div className="flex items-center gap-1">
                  {[{key:'todos',label:'Todos'},{key:'alerta',label:'Com alerta'},{key:'ok',label:'OK'}].map(f => (
                    <button key={f.key} onClick={() => setFiltroStatus(f.key)}
                      className={`px-3 py-1.5 rounded-lg text-[11px] font-medium transition-colors border ${
                        filtroStatus === f.key
                          ? 'bg-accent/15 text-accent border-accent/30'
                          : 'bg-surface2 text-text-dim border-border hover:border-accent/30'
                      }`}>
                      {f.label}
                    </button>
                  ))}
                </div>
                <button onClick={handleAtualizarIni} disabled={atualizandoIni}
                  title="Força re-download do arquivo de municípios do ACBr (cache 24h)"
                  className="px-3 py-1.5 rounded-lg text-[11px] font-medium text-text-dim bg-surface2 border border-border hover:border-accent/30 transition-colors flex items-center gap-1.5 disabled:opacity-50">
                  <RefreshCw size={11} className={atualizandoIni ? 'animate-spin' : ''} />
                  Atualizar municípios
                </button>
                <button onClick={handleAtualizarJira} disabled={atualizandoJira}
                  title="Força re-busca das issues do Jira (cache 30min)"
                  className="px-3 py-1.5 rounded-lg text-[11px] font-medium text-text-dim bg-surface2 border border-border hover:border-accent/30 transition-colors flex items-center gap-1.5 disabled:opacity-50">
                  <RefreshCw size={11} className={atualizandoJira ? 'animate-spin' : ''} />
                  {atualizandoJira ? 'Buscando...' : 'Atualizar Jira'}
                </button>
                <button onClick={handleCopiar} disabled={provedoresFiltrados.length === 0}
                  className="px-3 py-1.5 rounded-lg text-[11px] font-medium text-text-dim bg-surface2 border border-border hover:border-accent/30 transition-colors flex items-center gap-1.5 disabled:opacity-50">
                  {copied ? <Check size={11} className="text-success" /> : <Copy size={11} />}
                  {copied ? 'Copiado!' : 'Copiar'}
                </button>
              </div>

              {/* ── Lista de provedores ── */}
              {provedoresFiltrados.length === 0 ? (
                <div className="text-center py-10 text-text-dim text-sm">
                  <Filter size={20} className="mx-auto mb-2 opacity-30" />
                  Nenhum provedor encontrado com os filtros aplicados
                </div>
              ) : (
                <div className="space-y-2">
                  <p className="text-text-muted text-[10px]">
                    {provedoresFiltrados.length} de {data.total_provedores} provedor{data.total_provedores !== 1 ? 'es' : ''}
                  </p>
                  {provedoresFiltrados.map(p => (
                    <ProvedorCard key={p.nome} provedor={p} onIssueClick={setSelectedIssueKey} buscaFarmacia={buscaFarmacia} />
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </>
  )
}
