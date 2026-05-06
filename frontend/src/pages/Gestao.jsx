import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  RefreshCw, BarChart2, Building2, User, FileSearch, Brain,
  AlertCircle, CheckCircle, Send, Sparkles, Clock, TrendingUp,
  TrendingDown, Minus, Filter, X, ChevronUp, ChevronDown, ChevronRight,
  Copy, Check, Target, Calendar, Info, Download, ExternalLink,
  Users, Zap, Activity, Award, AlertTriangle, LayoutDashboard, ShieldAlert
} from 'lucide-react'
import api from '../api/backend'

// ── Skeleton ─────────────────────────────────────────────────────────────────
function Skeleton({ className = '' }) {
  return <div className={`animate-pulse bg-surface2 rounded-lg ${className}`} />
}

function SkeletonCard() {
  return (
    <div className="rounded-2xl border border-border bg-surface p-4 space-y-3">
      <div className="flex items-center gap-3">
        <Skeleton className="w-8 h-8 rounded-full flex-shrink-0" />
        <div className="flex-1 space-y-1.5">
          <Skeleton className="h-3 w-24" />
          <Skeleton className="h-2 w-16" />
        </div>
        <Skeleton className="h-6 w-12 rounded-xl" />
      </div>
      <Skeleton className="h-1.5 w-full rounded-full" />
      <div className="space-y-2 pt-1">
        <Skeleton className="h-2.5 w-full" />
        <Skeleton className="h-2.5 w-4/5" />
        <Skeleton className="h-2.5 w-3/5" />
      </div>
    </div>
  )
}

function SkeletonStatRow() {
  return (
    <div className="flex items-center gap-3 py-2">
      <Skeleton className="w-5 h-3 rounded" />
      <div className="flex-1 space-y-1">
        <Skeleton className="h-3 w-32" />
        <Skeleton className="h-1.5 w-full rounded-full" />
      </div>
      <Skeleton className="h-3 w-8 rounded" />
    </div>
  )
}

// ── Count-up ─────────────────────────────────────────────────────────────────
function useCountUp(target, duration = 600) {
  const [value, setValue] = useState(0)
  const prev = useRef(0)
  useEffect(() => {
    if (target === undefined || target === null) return
    const start = prev.current
    const end   = Number(target)
    if (start === end) return
    const startTime = performance.now()
    const tick = (now) => {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(Math.round(start + (end - start) * eased))
      if (progress < 1) requestAnimationFrame(tick)
      else prev.current = end
    }
    requestAnimationFrame(tick)
  }, [target, duration])
  return value
}

function CountUp({ value, suffix = '', className = '' }) {
  const animated = useCountUp(value)
  return <span className={className}>{animated}{suffix}</span>
}

// ── Segmented control ─────────────────────────────────────────────────────────
function SegmentedControl({ options, value, onChange, size = 'sm' }) {
  const px  = size === 'xs' ? 'px-2.5 py-1' : 'px-3 py-1.5'
  const txt = size === 'xs' ? 'text-[11px]' : 'text-xs'
  return (
    <div className="inline-flex items-center bg-surface2 border border-border rounded-xl p-0.5 gap-0.5">
      {options.map(opt => (
        <button
          key={opt.key}
          onClick={() => onChange(opt.key)}
          className={`${px} ${txt} font-medium rounded-[10px] transition-all whitespace-nowrap ${
            value === opt.key
              ? 'bg-accent text-white shadow-sm'
              : 'text-text-dim hover:text-text'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}

// ── Copy button ──────────────────────────────────────────────────────────────
function CopyButton({ text, className = '' }) {
  const [copied, setCopied] = useState(false)
  const handle = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    })
  }
  return (
    <button onClick={handle}
      className={`flex items-center gap-1 px-2 py-1 rounded-lg text-xs transition-colors
        ${copied ? 'text-success bg-success/10 border border-success/20' : 'text-text-dim hover:text-text bg-surface2 hover:bg-surface border border-border'}
        ${className}`}
      title="Copiar texto">
      {copied ? <Check size={11} /> : <Copy size={11} />}
      {copied ? 'Copiado!' : 'Copiar'}
    </button>
  )
}

// ── Info tooltip ─────────────────────────────────────────────────────────────
function InfoTooltip({ text }) {
  const [show, setShow] = useState(false)
  return (
    <span className="relative inline-flex items-center ml-1 align-middle">
      <button
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        className="w-3.5 h-3.5 rounded-full border border-border bg-surface2 text-text-muted flex items-center justify-center text-[9px] hover:border-accent/40 hover:text-accent transition-colors flex-shrink-0"
      >?</button>
      {show && (
        <div className="absolute z-50 left-5 top-0 w-52 bg-bg border border-border rounded-xl p-2.5 text-[11px] text-text-dim shadow-2xl pointer-events-none">
          {text}
        </div>
      )}
    </span>
  )
}

// ── Export utils ─────────────────────────────────────────────────────────────
function downloadFile(content, filename, type = 'text/plain') {
  const blob = new Blob([content], { type })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

function exportTXT(content, filename) {
  downloadFile(content, filename, 'text/plain;charset=utf-8')
}

function exportCSV(rows, filename) {
  const lines = rows.map(r => r.map(c => `"${String(c ?? '').replace(/"/g, '""')}"`).join(';'))
  downloadFile(lines.join('\n'), filename, 'text/csv;charset=utf-8')
}

function ExportMenu({ onTXT, onCSV, disabled = false }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="relative">
      <button onClick={() => setOpen(v => !v)} disabled={disabled}
        className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-40">
        <Download size={12} /> Exportar
      </button>
      {open && (
        <div className="absolute right-0 top-9 z-50 bg-bg border border-border rounded-xl shadow-2xl min-w-[130px] overflow-hidden">
          {onTXT && (
            <button onClick={() => { onTXT(); setOpen(false) }}
              className="w-full text-left px-4 py-2.5 text-xs text-text-dim hover:text-text hover:bg-surface transition-colors">
              .txt — Texto simples
            </button>
          )}
          {onCSV && (
            <button onClick={() => { onCSV(); setOpen(false) }}
              className="w-full text-left px-4 py-2.5 text-xs text-text-dim hover:text-text hover:bg-surface transition-colors">
              .csv — Excel/Planilha
            </button>
          )}
          <button onClick={() => { window.print(); setOpen(false) }}
            className="w-full text-left px-4 py-2.5 text-xs text-text-dim hover:text-text hover:bg-surface transition-colors border-t border-border">
            Imprimir / PDF
          </button>
        </div>
      )}
    </div>
  )
}

const TABS = [
  { key: 'demandas',     label: 'Dashboard',        icon: LayoutDashboard, analista: true  },
  { key: 'analistas',    label: 'Analistas',        icon: User,            analista: true  },
  { key: 'farmacias',    label: 'Farmácias',        icon: Building2,       analista: true  },
  { key: 'metas',        label: 'Metas',            icon: Target,          analista: true  },
  { key: 'sazonalidade', label: 'Sazonalidade',     icon: Calendar,        analista: false },
  { key: 'chamados',     label: 'Base de Chamados', icon: FileSearch,      analista: false },
  { key: 'duplicados',   label: 'Duplicados',       icon: AlertCircle,     analista: false },
  { key: 'analise',      label: 'Análise IA',       icon: Sparkles,        analista: false },
  { key: 'ia-chat',      label: 'Chat com IA',      icon: Brain,           analista: false },
]

const PERGUNTAS_RAPIDAS = [
  'Qual analista está mais sobrecarregado?',
  'Quem fechou mais chamados hoje?',
  'Qual categoria mais cresceu essa semana?',
  'Quais farmácias têm mais problemas recorrentes?',
  'Quem tem mais chamados fora do SLA?',
  'Qual o tempo médio de resolução por analista?',
  'Onde devo focar treinamento essa semana?',
  'Quais analistas precisam de suporte?',
]

// ── Sistema de cores unificado por grupo ─────────────────────────────────────
// Fonte única de verdade — todos os componentes derivam daqui
const GRUPOS_CONFIG = {
  Fiscal:   {
    label: 'Fiscal',   desc: 'SPED, NFe Saída, ECF, obrigações fiscais',
    membros: ['Vinicius', 'Rebeca medeiros', 'Rubens Milton Destro Junior'],
    accent:  '#60a5fa',
    text:    'text-blue-400',
    bg:      'bg-blue-500/10',
    border:  'border-blue-500/30',
    headBg:  'bg-blue-500/15',
    badge:   'bg-blue-500/20 text-blue-400 border-blue-500/30',
  },
  Producao: {
    label: 'Produção', desc: 'Nota de Entrada, manipulação, produção farmacêutica',
    membros: ['Isaac Santos', 'Raul Neto', 'Matheus Miranda de Lima Araujo', 'Boeira', 'Ruam Pereira de Sá'],
    accent:  '#4ade80',
    text:    'text-green-400',
    bg:      'bg-green-500/10',
    border:  'border-green-500/30',
    headBg:  'bg-green-500/15',
    badge:   'bg-green-500/20 text-green-400 border-green-500/30',
  },
  G1:       {
    label: 'G1',       desc: 'Suporte geral, dúvidas operacionais, atendimento',
    membros: ['Marcello Filho', 'Alan vieira', 'Keven Silva dos Santos'],
    accent:  '#c084fc',
    text:    'text-purple-400',
    bg:      'bg-purple-500/10',
    border:  'border-purple-500/30',
    headBg:  'bg-purple-500/15',
    badge:   'bg-purple-500/20 text-purple-400 border-purple-500/30',
  },
  GW:       {
    label: 'GW',       desc: 'Orya, e-commerce, Alcance, FarmaFácil Web',
    membros: ['Nathan Lopes', 'Taynara Pereira'],
    accent:  '#fb923c',
    text:    'text-orange-400',
    bg:      'bg-orange-500/10',
    border:  'border-orange-500/30',
    headBg:  'bg-orange-500/15',
    badge:   'bg-orange-500/20 text-orange-400 border-orange-500/30',
  },
  Ouvidoria: {
    label: 'Ouvidoria', desc: 'Reclamações, elogios, sugestões, ouvidoria interna',
    membros: ['Erica Milo Nardo Portezani', 'Lucas Eduardo Durante', 'Guilherme Cordeiro', 'Taynara Ribeiro'],
    accent:  '#f472b6',
    text:    'text-pink-400',
    bg:      'bg-pink-500/10',
    border:  'border-pink-500/30',
    headBg:  'bg-pink-500/15',
    badge:   'bg-pink-500/20 text-pink-400 border-pink-500/30',
  },
}
// Alias para manter compatibilidade com componentes que usavam os objetos antigos
const GRUPO_INFO        = Object.fromEntries(Object.entries(GRUPOS_CONFIG).map(([k, v]) => [k, { ...v, color: v.text }]))
const GRUPO_BADGE       = Object.fromEntries(Object.entries(GRUPOS_CONFIG).map(([k, v]) => [k, v.badge]))
const GRUPO_LABEL       = Object.fromEntries(Object.entries(GRUPOS_CONFIG).map(([k, v]) => [k, v.label]))
const GRUPO_COLORS_EXT  = GRUPOS_CONFIG
const ADER_COLORS       = GRUPOS_CONFIG

// Movidesk ticket URL
const MOVIDESK_TICKET_URL = (id) => `https://prismafive.movidesk.com/Ticket/Edit/${id}`

// ── Helpers de data ────────────────────────────────────────────────────────────
function toISO(d) { return d.toISOString().slice(0, 10) }

function getPeriodo(key) {
  const hoje = new Date()
  const d = (offset) => { const x = new Date(hoje); x.setDate(x.getDate() + offset); return x }
  const diaSemana   = hoje.getDay() === 0 ? 6 : hoje.getDay() - 1
  const inicioSemana = d(-diaSemana)
  const inicioSemAnt = d(-diaSemana - 7)
  const fimSemAnt    = d(-diaSemana - 1)
  const inicioMes    = new Date(hoje.getFullYear(), hoje.getMonth(), 1)
  const inicioMesAnt = new Date(hoje.getFullYear(), hoje.getMonth() - 1, 1)
  const fimMesAnt    = new Date(hoje.getFullYear(), hoje.getMonth(), 0)
  const MAP = {
    hoje:    { from: toISO(hoje),        to: toISO(hoje),       label: 'Hoje' },
    ontem:   { from: toISO(d(-1)),        to: toISO(d(-1)),      label: 'Ontem' },
    semana:  { from: toISO(inicioSemana), to: toISO(hoje),       label: 'Esta semana' },
    sem_ant: { from: toISO(inicioSemAnt), to: toISO(fimSemAnt),  label: 'Semana passada' },
    mes:     { from: toISO(inicioMes),    to: toISO(hoje),       label: 'Este mês' },
    mes_ant: { from: toISO(inicioMesAnt), to: toISO(fimMesAnt),  label: 'Mês passado' },
    '30d':   { from: toISO(d(-30)),       to: toISO(hoje),       label: 'Últimos 30d' },
    '90d':   { from: toISO(d(-90)),       to: toISO(hoje),       label: 'Últimos 90d' },
    '180d':  { from: toISO(d(-180)),      to: toISO(hoje),       label: 'Últimos 6 meses' },
  }
  return MAP[key] || MAP['semana']
}

const PERIODO_KEYS = [
  { key: 'hoje',    label: 'Hoje' },
  { key: 'ontem',   label: 'Ontem' },
  { key: 'semana',  label: 'Esta semana' },
  { key: 'sem_ant', label: 'Sem. passada' },
  { key: 'mes',     label: 'Este mês' },
  { key: 'mes_ant', label: 'Mês passado' },
  { key: '30d',     label: '30 dias' },
  { key: '90d',     label: '90 dias' },
  { key: '180d',    label: '6 meses' },
  { key: 'custom',  label: 'Personalizado' },
]

// ── Componentes reutilizáveis ──────────────────────────────────────────────────

function StatCard({ label, value, sub, color = 'accent', tooltip }) {
  const colors = {
    accent:  'border-accent/20  bg-accent/5  text-accent',
    success: 'border-success/20 bg-success/5 text-success',
    warning: 'border-warning/20 bg-warning/5 text-warning',
    error:   'border-error/20   bg-error/5   text-error',
  }
  const isNum = typeof value === 'number'
  const animated = useCountUp(isNum ? value : 0)
  return (
    <motion.div
      whileHover={{ y: -2, scale: 1.02 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
      className={`rounded-xl border p-4 cursor-default ${colors[color]}`}
    >
      <p className="text-text-dim text-xs font-semibold uppercase tracking-wider mb-1 flex items-center">
        {label}
        {tooltip && <InfoTooltip text={tooltip} />}
      </p>
      <p className="text-2xl font-bold">{isNum ? animated : (value ?? '—')}</p>
      {sub && <p className="text-text-dim text-xs mt-1">{sub}</p>}
    </motion.div>
  )
}

function RankingTable({ items, label1, label2 = 'Chamados', showTrend = false }) {
  if (!items?.length) return <p className="text-text-dim text-sm py-4">Sem dados no período.</p>
  const max = items[0][1]
  return (
    <div className="space-y-2">
      {items.map(([name, count], i) => (
        <div key={i} className="flex items-center gap-3">
          <span className="text-text-muted text-xs w-5 text-right font-mono">{i + 1}</span>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-0.5">
              <span className="text-text text-sm truncate">{name || '(sem nome)'}</span>
              <span className="text-accent font-mono text-xs ml-2 flex-shrink-0">{count}</span>
            </div>
            <div className="h-1.5 bg-surface2 rounded-full overflow-hidden">
              <div className="h-full bg-accent rounded-full transition-all"
                style={{ width: `${(count / max) * 100}%` }} />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

function AnalistaTable({ items }) {
  if (!items?.length) return <p className="text-text-dim text-sm py-4">Sem dados no período.</p>
  const maxRes = Math.max(...items.map(a => a.resolvidos || 0), 1)
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border text-xs text-text-dim uppercase tracking-wider">
            <th className="text-left py-2 pr-4 font-semibold">Analista</th>
            <th className="text-right py-2 px-3 font-semibold">
              Recebidos
              <InfoTooltip text="Chamados atribuídos ao analista no período (abertos em seu nome)" />
            </th>
            <th className="text-right py-2 px-3 font-semibold">
              Resolvidos
              <InfoTooltip text="Chamados que o analista fechou no período" />
            </th>
            <th className="text-right py-2 px-3 font-semibold">
              Média dias
              <InfoTooltip text="Tempo médio entre abertura e resolução do chamado. SLA = máx 3 dias" />
            </th>
            <th className="text-right py-2 pl-3 font-semibold">
              Fora SLA
              <InfoTooltip text="Chamados que levaram mais de 3 dias para ser resolvidos" />
            </th>
            <th className="py-2 pl-4 font-semibold w-28">Desempenho</th>
          </tr>
        </thead>
        <tbody>
          {items.map((a, i) => {
            const slaColor   = a.sla_pct > 30 ? 'text-error' : a.sla_pct > 10 ? 'text-warning' : 'text-success'
            const mediaColor = a.media_dias == null ? 'text-text-dim' : a.media_dias > 5 ? 'text-error' : a.media_dias > 2 ? 'text-warning' : 'text-success'
            return (
              <tr key={i} className="border-b border-border/50 hover:bg-surface/50 transition-colors">
                <td className="py-2.5 pr-4"><span className="text-text font-medium">{a.nome}</span></td>
                <td className="py-2.5 px-3 text-right font-mono text-text">{a.recebidos}</td>
                <td className="py-2.5 px-3 text-right font-mono text-accent font-semibold">{a.resolvidos}</td>
                <td className={`py-2.5 px-3 text-right font-mono ${mediaColor}`}>
                  {a.media_dias != null ? `${a.media_dias}d` : '—'}
                </td>
                <td className={`py-2.5 pl-3 text-right font-mono ${slaColor}`}>
                  {a.fora_sla > 0 ? `${a.fora_sla} (${a.sla_pct}%)` : '0'}
                </td>
                <td className="py-2.5 pl-4">
                  <div className="h-1.5 bg-surface2 rounded-full overflow-hidden w-full">
                    <div className="h-full bg-accent rounded-full transition-all"
                      style={{ width: `${(a.resolvidos / maxRes) * 100}%` }} />
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function TicketRow({ t }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-border rounded-xl overflow-hidden">
      <button onClick={() => setOpen(!open)}
        className="w-full flex items-start gap-3 p-3 text-left hover:bg-surface transition-colors">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-text-muted font-mono text-xs">#{t.id}</span>
            <span className="text-text text-sm font-medium truncate">{t.subject}</span>
          </div>
          <div className="flex gap-3 mt-1 flex-wrap">
            <span className="text-text-dim text-xs">{t.client_name}</span>
            {t.owner_name && <span className="text-accent/70 text-xs">{t.owner_name}</span>}
            {t.serviceSecond && <span className="text-text-dim text-xs">{t.serviceFirst} › {t.serviceSecond}</span>}
            <span className="text-text-muted text-xs">{t.createdDate}</span>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className={`text-xs px-2 py-0.5 rounded-full border ${
            t.status === '5 - Resolvido' || t.status === '6 - Fechado'
              ? 'border-success/30 text-success bg-success/10'
              : 'border-warning/30 text-warning bg-warning/10'
          }`}>{t.status?.split(' - ')[1] || t.status}</span>
          {t.extracted && (t.problema || t.solucao) && <CheckCircle size={13} className="text-success" />}
        </div>
      </button>
      {open && (
        <div className="border-t border-border bg-surface2 p-3 space-y-2 text-sm">
          {t.problema && (
            <div>
              <p className="text-warning text-xs font-semibold uppercase tracking-wider mb-0.5">Problema</p>
              <p className="text-text">{t.problema}</p>
            </div>
          )}
          {t.solucao && (
            <div>
              <p className="text-success text-xs font-semibold uppercase tracking-wider mb-0.5">Solução</p>
              <p className="text-text">{t.solucao}</p>
            </div>
          )}
          {!t.problema && !t.solucao && (
            <p className="text-text-dim text-xs italic">
              {t.extracted ? 'Sem problema/solução extraídos.' : 'Ainda não processado pela IA.'}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

function Select({ value, onChange, options, placeholder }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)}
      className="bg-surface2 border border-border rounded-lg px-3 py-1.5 text-text text-xs outline-none focus:border-accent transition-colors appearance-none cursor-pointer">
      <option value="">{placeholder}</option>
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  )
}

// ── Duplicados ────────────────────────────────────────────────────────────────
function isTicketAberto(t) {
  const s = (t.status || '').toLowerCase()
  return !s.includes('resolvido') && !s.includes('fechado') && !s.includes('cancelado')
}

function DuplicadoCard({ g, dismissedIds, onDismissTicket }) {
  const [open, setOpen] = useState(false)
  const tickets    = g.tickets.filter(t => !dismissedIds.has(String(t.id)))
  const temAbertos = tickets.length > 0

  return (
    <div className={`border rounded-xl overflow-hidden ${temAbertos ? 'border-error/30 bg-error/5' : 'border-warning/30 bg-warning/5'}`}>
      <button onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-white/5 transition-colors">
        <div className={`flex-shrink-0 px-2 py-0.5 text-xs font-bold rounded-lg border ${temAbertos ? 'bg-error/20 text-error border-error/30' : 'bg-warning/20 text-warning border-warning/30'}`}>
          {tickets.length}x
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-text text-sm font-medium truncate">{g.client_name}</p>
          <p className="text-text-dim text-xs">{g.categoria || 'Sem categoria'}</p>
        </div>
        <div className="text-xs text-text-dim flex-shrink-0 text-right hidden sm:block">
          <p className="text-error font-medium">{tickets.length} em aberto</p>
          <p className="text-text-muted">#{g.mais_antigo.id} → #{g.mais_recente.id}</p>
        </div>
        {open ? <ChevronDown size={14} className="text-text-dim flex-shrink-0" /> : <ChevronRight size={14} className="text-text-dim flex-shrink-0" />}
      </button>
      {open && (
        <div className="border-t border-white/10 px-4 py-3 space-y-2">
          {tickets.map((t, i) => (
            <div key={i} className="flex items-start gap-3 text-xs rounded-lg px-3 py-2 border bg-error/10 border-error/20">
              <div className="flex items-center gap-1.5 flex-shrink-0">
                <AlertTriangle size={11} className="text-error" />
                <span className="font-mono text-text-muted">#{t.id}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-text truncate">{t.subject}</p>
                <p className="text-text-muted mt-0.5">{t.createdDate} · {t.owner_name || '—'} · <span className="text-error font-medium">{t.status?.split(' - ')[1] || t.status}</span></p>
              </div>
              <div className="flex items-center gap-1.5 flex-shrink-0">
                <a href={MOVIDESK_TICKET_URL(t.id)} target="_blank" rel="noreferrer"
                  title="Abrir no Movidesk"
                  className="flex items-center gap-1 px-2 py-1 bg-accent/10 hover:bg-accent/20 border border-accent/20 rounded-lg text-accent text-[10px] transition-colors">
                  <ExternalLink size={10} /> Abrir
                </a>
                <button
                  onClick={() => onDismissTicket(t.id)}
                  title="Marcar como resolvido e remover da lista"
                  className="flex items-center gap-1 px-2 py-1 bg-success/10 hover:bg-success/20 border border-success/30 rounded-lg text-success text-[10px] font-medium transition-colors">
                  <CheckCircle size={10} /> Resolvido
                </button>
              </div>
            </div>
          ))}
          <p className="text-error text-xs font-medium pt-1 flex items-center gap-1">
            <AlertTriangle size={11} />
            Ação recomendada: manter chamado #{g.mais_antigo.id} e cancelar os duplicados em aberto.
          </p>
        </div>
      )}
    </div>
  )
}

// ── Período dropdown ─────────────────────────────────────────────────────────
function PeriodoPicker({ periodoKey, onChange, customFrom, customTo, onCustomFromChange, onCustomToChange }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const current = PERIODO_KEYS.find(p => p.key === periodoKey) || PERIODO_KEYS[0]
  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])
  return (
    <div className="relative" ref={ref}>
      <button onClick={() => setOpen(v => !v)}
        className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 border border-border rounded-lg text-[11px] hover:text-text transition-colors whitespace-nowrap">
        <Clock size={11} className="text-text-dim flex-shrink-0" />
        <span className="text-text font-medium">{current.label}</span>
        <ChevronDown size={10} className={`text-text-dim transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute left-0 top-9 z-50 bg-bg border border-border rounded-xl shadow-2xl w-44 overflow-hidden">
          <div className="py-1">
            {PERIODO_KEYS.filter(p => p.key !== 'custom').map(({ key, label }) => (
              <button key={key} onClick={() => { onChange(key); setOpen(false) }}
                className={`w-full text-left px-3 py-2 text-xs transition-colors hover:bg-surface
                  ${periodoKey === key ? 'text-accent font-semibold bg-accent/5' : 'text-text-dim'}`}>
                {label}
              </button>
            ))}
            <button onClick={() => onChange('custom')}
              className={`w-full text-left px-3 py-2 text-xs transition-colors hover:bg-surface border-t border-border
                ${periodoKey === 'custom' ? 'text-accent font-semibold bg-accent/5' : 'text-text-dim'}`}>
              Personalizado...
            </button>
          </div>
          {periodoKey === 'custom' && (
            <div className="border-t border-border px-3 py-2 space-y-1.5">
              <input type="date" value={customFrom} onChange={e => onCustomFromChange(e.target.value)}
                className="w-full bg-surface2 border border-border rounded px-2 py-1 text-text text-xs outline-none focus:border-accent" />
              <input type="date" value={customTo} onChange={e => onCustomToChange(e.target.value)}
                className="w-full bg-surface2 border border-border rounded px-2 py-1 text-text text-xs outline-none focus:border-accent" />
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Section header ────────────────────────────────────────────────────────────
function SectionHeader({ color = 'bg-accent', label, sub }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <div className={`w-1 h-5 ${color} rounded-full flex-shrink-0`} />
      <h2 className="text-text font-bold text-sm uppercase tracking-wider">{label}</h2>
      {sub && <span className="text-text-muted text-xs">{sub}</span>}
    </div>
  )
}

// ── Categoria com badge de grupo ──────────────────────────────────────────────

function CategoriaComGrupoBars({ items }) {
  if (!items?.length) return <p className="text-text-dim text-sm py-4">Sem dados no período.</p>
  const max = Math.max(...items.map(i => i.count || i[1] || 0), 1)
  return (
    <div className="space-y-2">
      {items.slice(0, 15).map((item, i) => {
        const cat   = item.cat ?? item[0]
        const count = item.count ?? item[1]
        const grupo = item.grupo ?? null
        const badge = grupo ? GRUPO_BADGE[grupo] : null
        return (
          <div key={i} className="flex items-center gap-3">
            <span className="text-text-muted text-xs w-5 text-right font-mono">{i + 1}</span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-0.5">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-text text-sm truncate">{cat || '(sem categoria)'}</span>
                  {badge && (
                    <span className={`flex-shrink-0 text-[10px] font-semibold px-1.5 py-0.5 rounded border ${badge}`}>
                      {GRUPO_LABEL[grupo]}
                    </span>
                  )}
                </div>
                <span className="text-accent font-mono text-xs ml-2 flex-shrink-0">{count}</span>
              </div>
              <div className="h-1.5 bg-surface2 rounded-full overflow-hidden">
                <div className="h-full bg-accent rounded-full transition-all" style={{ width: `${(count / max) * 100}%` }} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// ── Dashboard por equipes ─────────────────────────────────────────────────────

const CAT_PALETTE = ['#60a5fa','#4ade80','#fb923c','#c084fc','#facc15','#f87171','#34d399','#818cf8','#fb7185','#a3e635']

function getGrupoForAnalista(nome) {
  const low = (nome || '').toLowerCase().trim()
  for (const [g, info] of Object.entries(GRUPO_INFO)) {
    if (info.membros.some(m => m.toLowerCase().trim() === low)) return g
  }
  const first = low.split(' ')[0]
  for (const [g, info] of Object.entries(GRUPO_INFO)) {
    if (info.membros.some(m => m.toLowerCase().split(' ')[0] === first)) return g
  }
  return null
}

function computeGrupoStats(analistas, grupo) {
  const membros = (analistas || []).filter(a => getGrupoForAnalista(a.nome) === grupo)
  if (!membros.length) return null
  const totalRec  = membros.reduce((s, a) => s + (a.recebidos  || 0), 0)
  const totalRes  = membros.reduce((s, a) => s + (a.resolvidos || 0), 0)
  const totalFora = membros.reduce((s, a) => s + (a.fora_sla   || 0), 0)
  const slaOkPct  = totalRec > 0 ? Math.round((1 - totalFora / totalRec) * 100) : null
  const efic      = totalRec > 0 ? Math.round((totalRes / totalRec) * 100) : null
  const top       = [...membros].sort((a, b) => (b.resolvidos || 0) - (a.resolvidos || 0))[0]
  return { membros, totalRec, totalRes, slaOkPct, efic, top }
}

function DonutChart({ slices, size = 84 }) {
  if (!slices?.length) return null
  const total = slices.reduce((s, d) => s + d.value, 0)
  if (!total) return null
  let cur = 0
  const parts = slices.map(s => {
    const start = (cur / total) * 100
    cur += s.value
    const end = (cur / total) * 100
    return `${s.color} ${start.toFixed(1)}% ${end.toFixed(1)}%`
  })
  const inner = Math.round(size * 0.38)
  return (
    <div style={{
      width: size, height: size, borderRadius: '50%', flexShrink: 0,
      background: `conic-gradient(${parts.join(', ')})`,
      WebkitMaskImage: `radial-gradient(circle, transparent ${inner}px, black ${inner}px)`,
      maskImage: `radial-gradient(circle, transparent ${inner}px, black ${inner}px)`,
    }} />
  )
}

function TeamSummaryCard({ grupo, analistas, categorias }) {
  const info   = GRUPO_INFO[grupo] || {}
  const colors = GRUPO_COLORS_EXT[grupo] || GRUPO_COLORS_EXT.G1
  const gs     = computeGrupoStats(analistas, grupo)

  const catGrupo = (categorias || []).filter(c => c.grupo === grupo).slice(0, 5)
  const catTotal = catGrupo.reduce((s, c) => s + (c.count || 0), 0)
  const allTotal = (categorias || []).filter(c => c.grupo === grupo).reduce((s, c) => s + (c.count || 0), 0)
  const donutSlices = catGrupo.map((c, i) => ({ value: c.count, color: CAT_PALETTE[i], label: c.cat }))
  if (allTotal > catTotal) donutSlices.push({ value: allTotal - catTotal, color: '#374151', label: 'Outros' })

  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
      className={`rounded-2xl border ${colors.border} bg-surface overflow-hidden flex flex-col cursor-default`}
    >
      <div className={`${colors.headBg} border-b ${colors.border} px-4 py-3 flex items-center gap-2`}>
        <motion.div
          animate={{ scale: [1, 1.3, 1] }}
          transition={{ duration: 2, repeat: 1e9, ease: 'easeInOut' }}
          className="w-2 h-2 rounded-full flex-shrink-0"
          style={{ background: colors.accent }}
        />
        <span className={`${colors.text} font-bold text-xs uppercase tracking-widest`}>{info.label}</span>
      </div>
      <div className="px-4 pt-4 pb-4 flex-1">
        {gs ? (
          <>
            <div className="flex items-start justify-between mb-4 gap-2">
              <div>
                <p className="text-text-muted text-[10px] uppercase tracking-wider mb-0.5">Total de Chamados</p>
                <p className={`text-4xl font-black ${colors.text} leading-none`}>{gs.totalRec}</p>
                <p className="text-text-muted text-xs mt-1.5">{gs.totalRes} resolvidos</p>
              </div>
              {donutSlices.length > 0 && <DonutChart slices={donutSlices} size={80} />}
            </div>

            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className={`rounded-xl border ${colors.border} ${colors.bg} px-3 py-2.5`}>
                <p className="text-text-muted text-[10px] uppercase tracking-wider mb-0.5">Eficiência</p>
                <p className={`text-xl font-bold ${colors.text}`}>{gs.efic != null ? `${gs.efic}%` : '—'}</p>
              </div>
              <div className={`rounded-xl border ${colors.border} ${colors.bg} px-3 py-2.5`}>
                <p className="text-text-muted text-[10px] uppercase tracking-wider mb-0.5">SLA Ok</p>
                <p className={`text-xl font-bold ${gs.slaOkPct >= 80 ? 'text-success' : gs.slaOkPct >= 60 ? 'text-warning' : 'text-error'}`}>
                  {gs.slaOkPct != null ? `${gs.slaOkPct}%` : '—'}
                </p>
              </div>
            </div>

            {donutSlices.length > 0 && (
              <div className="space-y-1.5">
                <p className="text-text-muted text-[10px] uppercase tracking-wider mb-1">Tipos de Chamados</p>
                {donutSlices.filter(s => s.label !== 'Outros').map((s, i) => (
                  <div key={i} className="flex items-center justify-between text-[10px]">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: s.color }} />
                      <span className="text-text-dim truncate">{s.label}</span>
                    </div>
                    <span className="text-text-muted font-mono ml-2 flex-shrink-0">{s.value}</span>
                  </div>
                ))}
              </div>
            )}
          </>
        ) : (
          <p className="text-text-dim text-xs py-6 text-center">Sem dados no período.</p>
        )}
      </div>
    </motion.div>
  )
}

function AnalistaPerformCard({ analista, maxResolvidos, grupo }) {
  const colors   = GRUPO_COLORS_EXT[grupo] || GRUPO_COLORS_EXT.G1
  const initials = (analista.nome || '').split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
  const pct      = maxResolvidos > 0 ? Math.round(((analista.resolvidos || 0) / maxResolvidos) * 100) : 0
  const slaColor = (analista.sla_pct || 0) > 30 ? 'text-error' : (analista.sla_pct || 0) > 10 ? 'text-warning' : 'text-success'

  return (
    <div className="flex items-center gap-3 py-2.5">
      <div className={`w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold border ${colors.bg} ${colors.text} ${colors.border}`}>
        {initials}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <span className="text-text text-xs font-medium truncate">{analista.nome.split(' ')[0]}</span>
          <div className="flex items-center gap-2 flex-shrink-0 ml-2">
            <span className={`text-[10px] font-mono ${slaColor}`}>SLA {analista.sla_pct ?? 0}%</span>
            <span className={`text-sm font-bold font-mono ${colors.text}`}>{analista.resolvidos || 0}</span>
          </div>
        </div>
        <div className="h-1.5 bg-surface2 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.7, ease: 'easeOut', delay: 0.1 }}
            className="h-full rounded-full"
            style={{ background: colors.accent }}
          />
        </div>
      </div>
    </div>
  )
}

function GrupoAnalistasCard({ grupo, analistas }) {
  const info   = GRUPO_INFO[grupo] || {}
  const colors = GRUPO_COLORS_EXT[grupo] || GRUPO_COLORS_EXT.G1
  const membros = (analistas || [])
    .filter(a => getGrupoForAnalista(a.nome) === grupo)
    .sort((a, b) => (b.resolvidos || 0) - (a.resolvidos || 0))
  const maxRes = Math.max(...membros.map(a => a.resolvidos || 0), 1)

  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
      className={`rounded-2xl border ${colors.border} bg-surface overflow-hidden cursor-default`}
    >
      <div className={`${colors.headBg} border-b ${colors.border} px-4 py-2.5 flex items-center gap-2`}>
        <motion.div
          animate={{ scale: [1, 1.3, 1] }}
          transition={{ duration: 2.4, repeat: 1e9, ease: 'easeInOut', delay: 0.6 }}
          className="w-2 h-2 rounded-full flex-shrink-0"
          style={{ background: colors.accent }}
        />
        <span className={`${colors.text} font-bold text-[10px] uppercase tracking-widest`}>
          Desempenho Individual · {info.label}
        </span>
      </div>
      <div className="px-4 divide-y divide-border/40">
        {membros.length ? membros.map((a, i) => (
          <AnalistaPerformCard key={i} analista={a} maxResolvidos={maxRes} grupo={grupo} />
        )) : (
          <p className="text-text-dim text-xs py-6 text-center">Sem analistas no período.</p>
        )}
      </div>
    </motion.div>
  )
}

// ── Aderência ao Perfil ────────────────────────────────────────────────────────

function AderenciaAnalistaCard({ a }) {
  const [expanded, setExpanded] = useState(false)
  const colors = ADER_COLORS[a.grupo] || ADER_COLORS.G1
  const pct    = a.aderencia_pct ?? 0
  const barColor = pct >= 70 ? '#4ade80' : pct >= 40 ? '#facc15' : '#f87171'
  const pctText  = pct >= 70 ? 'text-success' : pct >= 40 ? 'text-warning' : 'text-error'
  const initials = (a.nome || '').split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()

  return (
    <div className={`rounded-xl border ${colors.border} bg-surface overflow-hidden`}>
      <button
        onClick={() => setExpanded(e => !e)}
        className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-surface2/50 transition-colors text-left"
      >
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-[11px] font-bold border ${colors.bg} ${colors.text} ${colors.border}`}>
          {initials}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <span className="text-text text-xs font-medium truncate">{a.nome.split(' ')[0]}</span>
            <div className="flex items-center gap-2 flex-shrink-0 ml-2">
              <span className="text-text-muted text-[10px] font-mono">{a.total_resolvidos} fechados</span>
              <span className={`text-sm font-bold font-mono ${pctText}`}>{pct}%</span>
            </div>
          </div>
          <div className="h-1.5 bg-surface2 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${pct}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
              className="h-full rounded-full"
              style={{ background: barColor }}
            />
          </div>
        </div>
        <ChevronDown size={12} className={`text-text-muted flex-shrink-0 transition-transform ${expanded ? 'rotate-180' : ''}`} />
      </button>

      {expanded && (
        <div className="px-3 pb-3 border-t border-border/40 pt-2 space-y-1">
          <div className="flex justify-between text-[10px] text-text-muted mb-1.5">
            <span>{a.na_categoria} no perfil · {a.fora_categoria} fora</span>
            <span className={`font-semibold ${colors.text}`}>{colors.label}</span>
          </div>
          {(a.top_categorias || []).map(([cat, n], i) => {
            const maxN = a.top_categorias[0]?.[1] || 1
            return (
              <div key={i} className="flex items-center gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between text-[10px] mb-0.5">
                    <span className="text-text-dim truncate">{cat}</span>
                    <span className="text-text-muted flex-shrink-0 ml-1">{n}</span>
                  </div>
                  <div className="h-1 bg-surface2 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${Math.round((n / maxN) * 100)}%`, background: colors.accent + '99' }} />
                  </div>
                </div>
              </div>
            )
          })}

          {(a.tickets_fora || []).length > 0 && (
            <div className="mt-3 pt-2 border-t border-border/30">
              <p className="text-[10px] text-text-muted font-semibold uppercase tracking-wider mb-1.5">
                Chamados fora do perfil ({a.tickets_fora.length})
              </p>
              <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
                {a.tickets_fora.map((t, i) => (
                  <div key={i} className="rounded-lg bg-surface2/60 border border-border/30 px-2.5 py-1.5">
                    <div className="flex items-start justify-between gap-2 mb-0.5">
                      <span className="text-text text-[10px] leading-snug flex-1 min-w-0">{t.subject}</span>
                      <span className="text-text-muted text-[9px] font-mono flex-shrink-0">{t.data}</span>
                    </div>
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="text-[9px] text-text-dim truncate">{t.categoria}</span>
                      {t.grupo_cat && t.grupo_cat !== '—' && (
                        <span className={`text-[9px] font-semibold px-1 rounded ${
                          t.grupo_cat === 'Fiscal'    ? 'text-blue-400 bg-blue-500/10' :
                          t.grupo_cat === 'Producao'  ? 'text-green-400 bg-green-500/10' :
                          t.grupo_cat === 'GW'        ? 'text-orange-400 bg-orange-500/10' :
                          t.grupo_cat === 'Ouvidoria' ? 'text-pink-400 bg-pink-500/10' :
                          'text-purple-400 bg-purple-500/10'
                        }`}>{GRUPO_LABEL[t.grupo_cat] || t.grupo_cat}</span>
                      )}
                      {t.cliente && <span className="text-[9px] text-text-muted truncate">· {t.cliente}</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function AderenciaSection({ aderencia, loading, filterGrupo }) {
  if (loading) return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {[1,2,3,4].map(i => <SkeletonCard key={i} />)}
    </div>
  )
  const analistas = aderencia?.analistas || []
  if (!analistas.length) return null
  const gruposToShow = filterGrupo ? [filterGrupo] : ['Fiscal', 'Producao', 'G1', 'GW', 'Ouvidoria']

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-text font-bold text-sm uppercase tracking-wider">Aderência ao Perfil</p>
          <p className="text-text-dim text-xs">% dos chamados fechados dentro da categoria do grupo · clique para detalhar</p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {gruposToShow.map(grupo => {
          const membros = analistas.filter(a => a.grupo === grupo)
          const colors  = ADER_COLORS[grupo] || ADER_COLORS.G1
          if (!membros.length) return null
          const mediaGrupo = Math.round(membros.reduce((s, a) => s + a.aderencia_pct, 0) / membros.length)
          return (
            <div key={grupo} className={`rounded-2xl border ${colors.border} bg-surface overflow-hidden`}>
              <div className={`${colors.bg} border-b ${colors.border} px-4 py-2.5 flex items-center justify-between`}>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: colors.accent }} />
                  <span className={`${colors.text} font-bold text-[10px] uppercase tracking-widest`}>
                    Aderência · {colors.label}
                  </span>
                </div>
                <span className={`text-[11px] font-mono font-bold ${colors.text}`}>média {mediaGrupo}%</span>
              </div>
              <div className="px-3 py-2 space-y-1">
                {membros.map((a, i) => <AderenciaAnalistaCard key={i} a={a} />)}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Componente principal ───────────────────────────────────────────────────────

export default function Gestao({ role = 'analista' }) {
  const isAnalista = role === 'analista'
  const visibleTabs = isAnalista ? TABS.filter(t => t.analista) : TABS
  const [tab,           setTab]          = useState('demandas')
  const [stats,         setStats]        = useState(null)
  const [tickets,       setTickets]      = useState([])
  const [ticketsTotal,  setTicketsTotal] = useState(0)
  const [ticketPage,    setTicketPage]   = useState(0)
  const [search,        setSearch]       = useState('')
  const [searchInput,   setSearchInput]  = useState('')
  const [syncing,       setSyncing]      = useState(false)
  const [extracting,    setExtracting]   = useState(false)
  const [syncMsg,       setSyncMsg]      = useState('')
  const [loadingTickets, setLoadingTickets] = useState(false)

  // Filtros globais
  const [filterGrupo,     setFilterGrupo]     = useState('')
  const [filterAnalista,  setFilterAnalista]  = useState('')
  const [filterCategoria, setFilterCategoria] = useState('')
  const [filterOpts,      setFilterOpts]      = useState({ analistas: [], categorias: [], farmacias: [] })

  const isLider = role === 'lideres' || role === 'administrador'
  const GRUPOS = [
    { key: '',           label: 'Todos'     },
    { key: 'Fiscal',     label: 'Fiscal'    },
    { key: 'Producao',   label: 'Produção'  },
    { key: 'G1',         label: 'G1'        },
    { key: 'GW',         label: 'GW'        },
    ...(isLider ? [{ key: 'Ouvidoria', label: 'Ouvidoria' }] : []),
  ]

  // Período
  const [periodoKey,  setPeriodoKey]  = useState('semana')
  const [customFrom,  setCustomFrom]  = useState('')
  const [customTo,    setCustomTo]    = useState('')

  const periodo = periodoKey === 'custom'
    ? { from: customFrom, to: customTo, label: `${customFrom} → ${customTo}` }
    : getPeriodo(periodoKey)

  // Análise IA
  const [analise,        setAnalise]        = useState('')
  const [analiseStats,   setAnaliseStats]   = useState(null)
  const [loadingAnalise, setLoadingAnalise] = useState(false)

  // Duplicados
  const [duplicados,        setDuplicados]        = useState([])
  const [loadingDuplicados, setLoadingDuplicados] = useState(false)
  const [dupGrupo,          setDupGrupo]          = useState('')
  const [dismissedIds,      setDismissedIds]      = useState(() => {
    try { return new Set(JSON.parse(localStorage.getItem('farmabot_dismissed_tickets') || '[]')) }
    catch { return new Set() }
  })

  const dismissTicket = (id) => {
    setDismissedIds(prev => {
      const next = new Set(prev)
      next.add(String(id))
      localStorage.setItem('farmabot_dismissed_tickets', JSON.stringify([...next]))
      return next
    })
  }

  // Metas
  const [metas,             setMetas]             = useState(null)
  const [metasSemanas,      setMetasSemanas]      = useState(4)
  const [loadingMetas,      setLoadingMetas]      = useState(false)
  const [metasErro,         setMetasErro]         = useState('')
  const [metasAnalise,      setMetasAnalise]      = useState({})
  const [metasExpandido,    setMetasExpandido]    = useState({})
  const [metaGrupoFiltro,   setMetaGrupoFiltro]   = useState('')
  const [syncingMetaHist,   setSyncingMetaHist]   = useState(false)
  const [metaHistMsg,       setMetaHistMsg]       = useState('')

  // Aderência ao perfil
  const [aderencia,        setAderencia]        = useState(null)
  const [loadingAderencia, setLoadingAderencia] = useState(false)

  // Sazonalidade
  const [sazoData,      setSazoData]      = useState([])
  const [sazoAgrup,     setSazoAgrup]     = useState('semana')
  const [sazoGrupo,     setSazoGrupo]     = useState('')
  const [loadingSazo,   setLoadingSazo]   = useState(false)
  const [sazoAnalise,   setSazoAnalise]   = useState('')
  const [loadingSazoAI, setLoadingSazoAI] = useState(false)

  // Chat IA
  const [chatMsgs,    setChatMsgs]    = useState([])
  const [chatInput,   setChatInput]   = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const chatEndRef = useRef(null)

  const fmtDate = (iso) => iso ? iso.replace('T', ' ').slice(0, 16) : '—'

  const periodoAtualLabel = (() => {
    const p = periodo
    const from = p.from ? p.from.slice(5).replace('-', '/') : ''
    const to   = p.to   ? p.to.slice(5).replace('-', '/')   : ''
    if (!from) return p.label
    if (from === to) return `${p.label} (${from})`
    return `${p.label} (${from} – ${to})`
  })()

  const loadAderencia = useCallback(async (p) => {
    const pr = p || periodo
    setLoadingAderencia(true)
    try {
      const { data } = await api.gestaoAderencia(pr.from, pr.to)
      setAderencia(data)
    } catch {}
    finally { setLoadingAderencia(false) }
  }, []) // eslint-disable-line

  const loadStats = useCallback(async (p, analista, categoria, grupo) => {
    const pr = p || periodo
    const an = analista !== undefined ? analista : filterAnalista
    const ca = categoria !== undefined ? categoria : filterCategoria
    const gr = grupo     !== undefined ? grupo     : filterGrupo
    try {
      const { data } = await api.gestaoStats(pr.from, pr.to, an, ca, gr)
      setStats(data)
    } catch {}
  }, []) // eslint-disable-line

  const loadTickets = useCallback(async (page = 0, q = search, p = periodo) => {
    setLoadingTickets(true)
    try {
      const { data } = await api.gestaoTickets({
        page, search: q,
        analista: filterAnalista, categoria: filterCategoria,
        date_from: p.from, date_to: p.to
      })
      setTickets(data.tickets || [])
      setTicketsTotal(data.total || 0)
      setTicketPage(page)
    } catch {}
    setLoadingTickets(false)
  }, [search, filterAnalista, filterCategoria]) // eslint-disable-line

  const loadFilterOpts = useCallback(async () => {
    try {
      const { data } = await api.gestaoFilters()
      setFilterOpts(data)
    } catch {}
  }, [])

  useEffect(() => {
    loadStats(periodo, filterAnalista, filterCategoria, filterGrupo)
    loadAderencia(periodo)
    if (tab === 'chamados') loadTickets(0, search, periodo)
  }, [periodoKey, customFrom, customTo, filterAnalista, filterCategoria, filterGrupo]) // eslint-disable-line

  useEffect(() => {
    if (tab === 'chamados')    loadTickets(0, search, periodo)
    if (tab === 'duplicados')  handleLoadDuplicados()
  }, [tab]) // eslint-disable-line

  useEffect(() => {
    if (tab !== 'metas') return
    setLoadingMetas(true)
    setMetasErro('')
    api.gestaoMetas(metasSemanas)
      .then(({ data }) => setMetas(Array.isArray(data) ? data : []))
      .catch(e => { setMetasErro(e.response?.data?.error || e.message || 'Erro'); setMetas([]) })
      .finally(() => setLoadingMetas(false))
  }, [tab]) // eslint-disable-line

  useEffect(() => {
    if (tab !== 'sazonalidade') return
    setLoadingSazo(true)
    api.gestaoSazonalidade(periodo.from, periodo.to, sazoAgrup, sazoGrupo)
      .then(({ data }) => setSazoData(Array.isArray(data) ? data : []))
      .catch(() => setSazoData([]))
      .finally(() => setLoadingSazo(false))
  }, [tab]) // eslint-disable-line

  useEffect(() => { loadFilterOpts() }, []) // eslint-disable-line

  const handleSync = async () => {
    setSyncing(true)
    setSyncMsg(`Sincronizando: ${periodo.label}...`)
    try {
      await api.gestaoSync(periodo.from, periodo.to)
      const poll = setInterval(async () => {
        try {
          const { data } = await api.gestaoSyncStatus()
          setSyncMsg(data.msg || '')
          if (!data.running) {
            clearInterval(poll)
            setSyncing(false)
            loadStats(periodo, filterAnalista, filterCategoria)
            loadFilterOpts()
          }
        } catch { clearInterval(poll); setSyncing(false) }
      }, 1500)
    } catch (e) {
      setSyncMsg('Erro: ' + (e.response?.data?.error || e.message))
      setSyncing(false)
    }
  }

  const handleExtract = async () => {
    setExtracting(true)
    setSyncMsg('Extraindo problema/solução com IA...')
    try {
      await api.gestaoExtract({ batch: 30 })
      setSyncMsg('Extração iniciada. Pode levar alguns minutos.')
      setTimeout(() => {
        loadStats(periodo, filterAnalista, filterCategoria)
        setExtracting(false)
        setSyncMsg('')
      }, 5000)
    } catch (e) {
      setSyncMsg('Erro: ' + (e.response?.data?.error || e.message))
      setExtracting(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    setSearch(searchInput)
    loadTickets(0, searchInput, periodo)
  }

  const handleSyncMetaHistorico = async () => {
    setSyncingMetaHist(true)
    setMetaHistMsg('')
    try {
      await api.gestaoSyncMetaHistorico(3)
      setMetaHistMsg('Dados históricos atualizados!')
      handleLoadMetas(metasSemanas)
    } catch (e) {
      setMetaHistMsg('Erro: ' + (e.response?.data?.error || e.message))
    }
    setSyncingMetaHist(false)
    setTimeout(() => setMetaHistMsg(''), 5000)
  }

  const handleLoadMetas = async (semanas = metasSemanas) => {
    setLoadingMetas(true)
    setMetasErro('')
    setMetasAnalise({})
    try {
      const { data } = await api.gestaoMetas(semanas)
      setMetas(Array.isArray(data) ? data : [])
    } catch (e) {
      setMetasErro(e.response?.data?.error || e.message || 'Erro ao carregar metas')
      setMetas([])
    }
    setLoadingMetas(false)
  }

  const handleMetasAnalise = async (grupo) => {
    setMetasAnalise(prev => ({ ...prev, [grupo]: { loading: true, text: '', erro: '' } }))
    setMetasExpandido(prev => ({ ...prev, [grupo]: true }))
    try {
      const { data } = await api.gestaoMetasAnalise(grupo, metasSemanas)
      setMetasAnalise(prev => ({ ...prev, [grupo]: { loading: false, text: data.resposta || '', erro: '' } }))
    } catch (e) {
      setMetasAnalise(prev => ({
        ...prev,
        [grupo]: { loading: false, text: '', erro: e.response?.data?.error || e.message || 'Erro' }
      }))
    }
  }

  const handleLoadSazo = async (agrup = sazoAgrup, grupo = sazoGrupo) => {
    setLoadingSazo(true)
    setSazoAnalise('')
    try {
      const { data } = await api.gestaoSazonalidade(periodo.from, periodo.to, agrup, grupo)
      setSazoData(data || [])
    } catch {}
    setLoadingSazo(false)
  }

  const handleSazoAnalise = async () => {
    setLoadingSazoAI(true)
    setSazoAnalise('')
    try {
      const { data } = await api.gestaoSazonalidadeAnalise(periodo.from, periodo.to, sazoAgrup, sazoGrupo)
      setSazoAnalise(data.resposta || '')
    } catch (e) {
      setSazoAnalise('Erro: ' + (e.response?.data?.error || e.message))
    }
    setLoadingSazoAI(false)
  }

  const handleLoadDuplicados = async (grupo = dupGrupo) => {
    setLoadingDuplicados(true)
    try {
      const { data } = await api.gestaoDuplicados(true, grupo)
      setDuplicados(data.duplicados || [])
    } catch {}
    setLoadingDuplicados(false)
  }

  const handleGerarAnalise = async () => {
    setLoadingAnalise(true)
    setAnalise('')
    setAnaliseStats(null)
    try {
      const { data } = await api.gestaoAnalise(periodo.from, periodo.to)
      setAnalise(data.resposta || '')
      setAnaliseStats(data.stats || null)
    } catch (e) {
      setAnalise('Erro: ' + (e.response?.data?.error || e.message))
    }
    setLoadingAnalise(false)
  }

  const handleChatSend = async (pergunta) => {
    const p = (pergunta || chatInput).trim()
    if (!p || chatLoading) return
    setChatInput('')
    const historico = chatMsgs.map(m => ({ role: m.role, content: m.content }))
    setChatMsgs(prev => [...prev, { role: 'user', content: p }])
    setChatLoading(true)
    try {
      const { data } = await api.gestaoIaChat(p, historico, periodo.from, periodo.to)
      setChatMsgs(prev => [...prev, { role: 'assistant', content: data.resposta }])
    } catch (e) {
      setChatMsgs(prev => [...prev, {
        role: 'assistant', content: 'Erro: ' + (e.response?.data?.error || e.message), isError: true
      }])
    }
    setChatLoading(false)
    setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100)
  }

  const handlePeriodo = (key) => {
    setPeriodoKey(key)
  }

  const clearFilters = () => {
    setFilterGrupo('')
    setFilterAnalista('')
    setFilterCategoria('')
  }

  const hasFilters = filterGrupo || filterAnalista || filterCategoria

  // ── Export helpers ─────────────────────────────────────────────────────────
  const exportMetasTXT = () => {
    if (!metas) return
    const lines = [
      `RELATÓRIO DE METAS POR EQUIPE`,
      `Gerado em: ${new Date().toLocaleDateString('pt-BR')} ${new Date().toLocaleTimeString('pt-BR')}`,
      `Cálculo: entradas do mês ÷ analistas ÷ 22 dias úteis = meta/dia por analista`,
      '',
    ]
    for (const eq of metas) {
      const gi = GRUPO_INFO[eq.grupo] || {}
      lines.push(`=== EQUIPE ${eq.grupo.toUpperCase()} ===`)
      lines.push(`Área: ${gi.desc || '—'}`)
      lines.push(`Analistas: ${eq.membros_count}`)
      lines.push(`Fila em aberto: ${eq.fila_total} chamados`)
      lines.push('')
      lines.push('Histórico mensal:')
      for (const mh of (eq.historico_meses || [])) {
        const proj = mh.parcial ? ` (projetado, real: ${mh.entradas})` : ''
        const aviso = mh.acima_media ? ` ⚠ +${mh.pct_vs_media}% vs média` : ''
        lines.push(`  ${mh.label}: ${mh.entradas_proj || mh.entradas} entradas${proj} → meta ${mh.equilibrio_dia}/dia/analista${aviso}`)
      }
      lines.push(`  Média mensal: ${eq.media_entradas_mes} chamados`)
      lines.push('')
      lines.push(`Meta atual por analista/dia: ${eq.equilibrio_dia}`)
      lines.push(`Ritmo atual por analista/dia: ${eq.taxa_dia_analista}`)
      lines.push(`Status: ${eq.ritmo_ok ? '✓ Atingindo meta' : '✗ Abaixo da meta'}`)
      lines.push('')
      lines.push('Desempenho por analista:')
      for (const m of (eq.membros || [])) {
        const st = m.atingiu ? '✓' : '✗'
        lines.push(`  ${st} ${m.nome}: fila=${m.fila}, ritmo=${m.taxa_dia}/dia, meta=${m.meta_dia}/dia`)
      }
      lines.push('')
      lines.push('Top categorias na fila:')
      for (const [cat, n] of (eq.top_categorias || [])) {
        lines.push(`  ${n}x ${cat}`)
      }
      lines.push('')
    }
    exportTXT(lines.join('\n'), `metas_${new Date().toISOString().slice(0,10)}.txt`)
  }

  const exportMetasCSV = () => {
    if (!metas) return
    const rows = [['Equipe', 'Analista', 'Fila', 'Ritmo/dia', 'Meta/dia', 'Atingiu meta']]
    for (const eq of metas) {
      for (const m of (eq.membros || [])) {
        rows.push([eq.grupo, m.nome, m.fila, m.taxa_dia, m.meta_dia, m.atingiu ? 'Sim' : 'Não'])
      }
    }
    exportCSV(rows, `metas_${new Date().toISOString().slice(0,10)}.csv`)
  }

  const exportAnalistasTXT = () => {
    if (!stats?.analistas_detalhe) return
    const lines = [
      `RELATÓRIO DE ANALISTAS — ${periodoAtualLabel}`,
      `Gerado em: ${new Date().toLocaleDateString('pt-BR')}`,
      '',
    ]
    for (const a of stats.analistas_detalhe) {
      lines.push(`${a.nome}`)
      lines.push(`  Recebidos: ${a.recebidos} | Resolvidos: ${a.resolvidos}`)
      lines.push(`  Tempo médio: ${a.media_dias != null ? a.media_dias + 'd' : '—'} | Fora SLA: ${a.fora_sla} (${a.sla_pct}%)`)
      lines.push('')
    }
    exportTXT(lines.join('\n'), `analistas_${new Date().toISOString().slice(0,10)}.txt`)
  }

  const exportDuplicadosTXT = () => {
    const lines = [
      `CHAMADOS EM ABERTO DUPLICADOS`,
      `Gerado em: ${new Date().toLocaleDateString('pt-BR')}`,
      '',
    ]
    for (const g of duplicados) {
      lines.push(`${g.client_name} — ${g.categoria || 'Sem categoria'} (${g.count} duplicados)`)
      for (const t of g.tickets) {
        const status = !t.status?.includes('Resolvido') && !t.status?.includes('Fechado') ? 'ABERTO' : 'Fechado'
        lines.push(`  #${t.id} [${status}] ${t.subject} — ${t.createdDate} — ${t.owner_name || '—'}`)
      }
      lines.push('')
    }
    exportTXT(lines.join('\n'), `duplicados_${new Date().toISOString().slice(0,10)}.txt`)
  }

  // ── Render ────────────────────────────────────────────────────────────────────
  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">

      {/* ── Header compacto ── */}
      <div className="flex-shrink-0 border-b border-border">
        <div className="flex items-center gap-2 px-4 py-2 flex-wrap">

          {/* Título */}
          <span className="text-text font-semibold text-sm flex-shrink-0">Gestão</span>
          <div className="w-px h-4 bg-border flex-shrink-0" />

          {/* Período dropdown */}
          <PeriodoPicker
            periodoKey={periodoKey}
            onChange={handlePeriodo}
            customFrom={customFrom}
            customTo={customTo}
            onCustomFromChange={setCustomFrom}
            onCustomToChange={setCustomTo}
          />

          {/* Separador */}
          <div className="w-px h-4 bg-border flex-shrink-0" />

          {/* Grupo */}
          <SegmentedControl
            options={GRUPOS}
            value={filterGrupo}
            onChange={v => { setFilterGrupo(v); setFilterAnalista('') }}
            size="xs"
          />

          {/* Analista + Categoria */}
          <Select value={filterAnalista}
            onChange={v => { setFilterAnalista(v); if (v) setFilterGrupo('') }}
            options={filterGrupo && GRUPO_INFO[filterGrupo]
              ? GRUPO_INFO[filterGrupo].membros.filter(m => filterOpts.analistas.includes(m))
              : filterOpts.analistas}
            placeholder="Analista" />
          <Select value={filterCategoria} onChange={setFilterCategoria}
            options={filterOpts.categorias} placeholder="Categoria" />

          {hasFilters && (
            <button onClick={clearFilters}
              className="flex items-center gap-1 text-error text-[11px] hover:underline px-1">
              <X size={10} /> Limpar
            </button>
          )}

          {/* Ações — direita */}
          <div className="ml-auto flex items-center gap-1.5">
            {syncMsg && (
              <span className="text-text-muted text-[10px] max-w-[180px] truncate">{syncMsg}</span>
            )}
            {stats?.last_sync && !syncMsg && (
              <span className="text-text-muted text-[10px] hidden md:block">
                sync {fmtDate(stats.last_sync)}
              </span>
            )}
            {!isAnalista && (
              <button onClick={handleExtract} disabled={extracting || syncing}
                className="flex items-center gap-1 px-2.5 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-[11px] transition-colors disabled:opacity-50">
                <Brain size={11} />
                {extracting ? 'Extraindo...' : 'Extrair IA'}
              </button>
            )}
            <button onClick={handleSync} disabled={syncing || extracting}
              className="flex items-center gap-1 px-2.5 py-1.5 bg-accent/10 hover:bg-accent/20 border border-accent/20 rounded-lg text-accent text-[11px] transition-colors disabled:opacity-50">
              <RefreshCw size={11} className={syncing ? 'animate-spin' : ''} />
              {syncing ? 'Sincronizando...' : 'Sincronizar'}
            </button>
          </div>
        </div>
      </div>

      {/* ── Tabs ── */}
      <div className="flex-shrink-0 flex gap-0 px-4 border-b border-border overflow-x-auto">
        {visibleTabs.map(({ key, label, icon: Icon }) => (
          <button key={key} onClick={() => setTab(key)}
            className={`relative flex items-center gap-1.5 px-3 py-2.5 text-xs font-medium transition-colors whitespace-nowrap
              ${tab === key ? 'text-accent' : 'text-text-dim hover:text-text'}`}>
            <Icon size={13} />{label}
            {tab === key && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent rounded-t-full" />
            )}
          </button>
        ))}
      </div>

      {/* ── Conteúdo ── */}
      <div className="flex-1 overflow-y-auto px-6 py-4 selectable">

        {/* DASHBOARD */}
        {tab === 'demandas' && (
          <div className="space-y-4">

            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div>
                <p className="text-text font-bold text-sm uppercase tracking-wider">Painel de Desempenho</p>
                <p className="text-text-dim text-xs">Visão por equipes · {periodoAtualLabel}</p>
              </div>
              {stats && (() => {
                const d   = stats.analistas_detalhe || []
                const top = [...d].sort((a,b)=>(b.resolvidos||0)-(a.resolvidos||0))[0]
                if (!top?.resolvidos) return null
                return (
                  <div className="flex items-center gap-2 px-3 py-1.5 bg-success/10 border border-success/20 rounded-xl">
                    <Award size={13} className="text-success flex-shrink-0" />
                    <p className="text-success text-xs font-medium">
                      {top.nome.split(' ')[0]} lidera com {top.resolvidos} resolvidos
                    </p>
                  </div>
                )
              })()}
            </div>

            {/* Cards por equipe */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {stats === null
                ? [1,2,3,4].map(i => <SkeletonCard key={i} />)
                : (filterGrupo ? [filterGrupo] : ['Fiscal', 'Producao', 'G1', 'GW', 'Ouvidoria']).map(g => (
                    <TeamSummaryCard
                      key={g}
                      grupo={g}
                      analistas={stats?.analistas_detalhe}
                      categorias={stats?.top_categorias_com_grupo}
                    />
                  ))
              }
            </div>

            {/* Desempenho individual por equipe */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {stats === null
                ? [1,2,3,4].map(i => <SkeletonCard key={i} />)
                : (filterGrupo ? [filterGrupo] : ['Fiscal', 'Producao', 'G1', 'GW', 'Ouvidoria']).map(g => (
                    <GrupoAnalistasCard
                      key={g}
                      grupo={g}
                      analistas={stats?.analistas_detalhe}
                    />
                  ))
              }
            </div>

            {/* Aderência ao perfil */}
            <AderenciaSection aderencia={aderencia} loading={loadingAderencia} filterGrupo={filterGrupo} />

            {/* Insights automáticos */}
            {stats && (() => {
              const d = stats.analistas_detalhe || []
              const insights = []
              const piorSla = [...d].filter(a=>a.fora_sla>0).sort((a,b)=>b.sla_pct-a.sla_pct)[0]
              if (piorSla?.sla_pct > 15) insights.push({
                Icon: ShieldAlert, color: 'text-error', bg: 'bg-error/10 border-error/20',
                text: `${piorSla.nome.split(' ')[0]} tem ${piorSla.sla_pct}% dos chamados fora do SLA`
              })
              const topCat = stats.top_categorias?.[0]
              if (topCat) insights.push({
                Icon: TrendingUp, color: 'text-warning', bg: 'bg-warning/10 border-warning/20',
                text: `"${topCat[0]}" é a categoria dominante: ${topCat[1]} chamados`
              })
              if ((stats.recorrentes||0) > 0) insights.push({
                Icon: AlertCircle, color: 'text-error', bg: 'bg-error/10 border-error/20',
                text: `${stats.recorrentes} farmácia${stats.recorrentes!==1?'s':''} com chamados recorrentes`
              })
              const topFarm = stats.top_farmacias?.[0]
              if (topFarm && topFarm[1] >= 3) insights.push({
                Icon: Building2, color: 'text-warning', bg: 'bg-warning/10 border-warning/20',
                text: `"${topFarm[0]}" concentra ${topFarm[1]} chamados — farmácia de atenção`
              })
              if (!insights.length) return null
              return (
                <div>
                  <SectionHeader color="bg-warning" label="Alertas" />
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {insights.map((ins, i) => (
                      <div key={i} className={`flex items-start gap-3 p-3 rounded-xl border ${ins.bg}`}>
                        <ins.Icon size={13} className={`${ins.color} mt-0.5 flex-shrink-0`} />
                        <p className="text-text text-xs leading-relaxed">{ins.text}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })()}
          </div>
        )}

        {/* FARMÁCIAS */}
        {tab === 'farmacias' && (
          <div>
            <SectionHeader color="bg-green-400" label="Farmácias com mais chamados" sub={periodoAtualLabel} />
            <RankingTable items={stats?.top_farmacias} label1="Farmácia" />
          </div>
        )}

        {/* ANALISTAS */}
        {tab === 'analistas' && (
          <div className="space-y-6">

            {/* Highlights */}
            {stats?.analistas_detalhe?.length > 1 && (() => {
              const d = stats.analistas_detalhe
              const melhor   = [...d].sort((a, b) => (b.resolvidos || 0) - (a.resolvidos || 0))[0]
              const piorSla  = [...d].filter(a => a.fora_sla > 0).sort((a, b) => b.sla_pct - a.sla_pct)[0]
              const maisRap  = [...d].filter(a => a.media_dias != null).sort((a, b) => a.media_dias - b.media_dias)[0]
              const maisLent = [...d].filter(a => a.media_dias != null).sort((a, b) => b.media_dias - a.media_dias)[0]
              return (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <StatCard label="Mais resolvidos" value={melhor?.nome?.split(' ')[0]} sub={`${melhor?.resolvidos} chamados`} color="success" />
                  {piorSla ? <StatCard label="Maior risco SLA" value={piorSla?.nome?.split(' ')[0]} sub={`${piorSla?.sla_pct}% fora`} color="error" /> : <div />}
                  {maisRap ? <StatCard label="Mais rápido" value={maisRap?.nome?.split(' ')[0]} sub={`${maisRap?.media_dias}d em média`} color="success" /> : <div />}
                  {maisLent && maisLent?.nome !== maisRap?.nome
                    ? <StatCard label="Mais lento" value={maisLent?.nome?.split(' ')[0]} sub={`${maisLent?.media_dias}d em média`} color="warning" />
                    : <div />}
                </div>
              )
            })()}

            {/* Tabela detalhada */}
            <div>
              <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
                <SectionHeader color="bg-accent" label="Performance Detalhada" sub={periodoAtualLabel} />
                <div className="flex gap-2 items-center flex-wrap">
                  <div className="flex gap-3 text-xs text-text-dim">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-success inline-block" /> SLA ok</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-warning inline-block" /> &gt;10% fora</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-error inline-block" /> &gt;30% fora</span>
                  </div>
                  <ExportMenu onTXT={exportAnalistasTXT} disabled={!stats?.analistas_detalhe?.length} />
                </div>
              </div>
              <AnalistaTable items={stats?.analistas_detalhe} />
            </div>

            {/* Rankings lado a lado */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <SectionHeader color="bg-blue-400" label="Recebidos" sub="atribuídos" />
                <RankingTable items={stats?.top_analistas} label1="Analista" />
              </div>
              <div>
                <SectionHeader color="bg-green-400" label="Resolvidos" sub="fechados" />
                <RankingTable items={stats?.top_analistas_resolvidos} label1="Analista" />
              </div>
            </div>
          </div>
        )}

        {/* BASE DE CHAMADOS */}
        {tab === 'chamados' && (
          <div className="space-y-3">
            <form onSubmit={handleSearch} className="flex gap-2">
              <input value={searchInput} onChange={e => setSearchInput(e.target.value)}
                placeholder="Buscar por assunto, farmácia, problema ou solução..."
                className="flex-1 bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent transition-colors" />
              <button type="submit"
                className="px-4 py-2 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-colors">
                Buscar
              </button>
            </form>

            {hasFilters && (
              <p className="text-text-dim text-xs flex items-center gap-1">
                <Filter size={11} />
                Filtrando por: {[filterAnalista, filterCategoria].filter(Boolean).join(' · ')}
              </p>
            )}

            {loadingTickets ? (
              <p className="text-text-dim text-sm py-4">Carregando...</p>
            ) : (
              <>
                <p className="text-text-dim text-xs">{ticketsTotal} chamados encontrados</p>
                <div className="space-y-2">
                  {tickets.map(t => <TicketRow key={t.id} t={t} />)}
                </div>
                {ticketsTotal > 50 && (
                  <div className="flex gap-2 justify-center pt-2">
                    <button onClick={() => loadTickets(ticketPage - 1)} disabled={ticketPage === 0}
                      className="px-3 py-1.5 bg-surface2 border border-border rounded-lg text-xs text-text-dim disabled:opacity-40 hover:text-text transition-colors">
                      Anterior
                    </button>
                    <span className="text-text-dim text-xs py-1.5">Pág {ticketPage + 1}</span>
                    <button onClick={() => loadTickets(ticketPage + 1)} disabled={(ticketPage + 1) * 50 >= ticketsTotal}
                      className="px-3 py-1.5 bg-surface2 border border-border rounded-lg text-xs text-text-dim disabled:opacity-40 hover:text-text transition-colors">
                      Próxima
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* DUPLICADOS */}
        {tab === 'duplicados' && (
          <div className="space-y-4">
            {/* Filtros no topo */}
            <div className="flex items-center gap-2 flex-wrap">
              <SegmentedControl
                options={[
                  { key: '',           label: 'Todas'     },
                  { key: 'Fiscal',     label: 'Fiscal'    },
                  { key: 'Producao',   label: 'Produção'  },
                  { key: 'G1',         label: 'G1'        },
                  { key: 'GW',         label: 'GW'        },
                  ...(isLider ? [{ key: 'Ouvidoria', label: 'Ouvidoria' }] : []),
                ]}
                value={dupGrupo}
                onChange={v => { setDupGrupo(v); handleLoadDuplicados(v) }}
              />
              <div className="ml-auto flex items-center gap-2">
                <ExportMenu onTXT={exportDuplicadosTXT} disabled={!duplicados.length} />
                <button onClick={() => handleLoadDuplicados(dupGrupo)} disabled={loadingDuplicados}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-accent/10 hover:bg-accent/20 border border-accent/20 rounded-lg text-accent text-xs transition-colors disabled:opacity-50">
                  <RefreshCw size={12} className={loadingDuplicados ? 'animate-spin' : ''} />
                  {loadingDuplicados ? 'Analisando...' : 'Atualizar'}
                </button>
              </div>
            </div>

            {/* Info card */}
            <div className="bg-surface2 border border-border rounded-xl p-4 space-y-1.5">
              <div className="flex items-start gap-2">
                <AlertTriangle size={15} className="text-error mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-text text-sm font-semibold">Chamados em aberto duplicados</p>
                  <p className="text-text-dim text-xs mt-0.5">
                    Detecta quando a <strong>mesma farmácia</strong> tem <strong>2+ chamados em aberto sobre o mesmo assunto</strong>.
                    A IA identifica assuntos semelhantes mesmo com textos diferentes — ex: "dúvidas NFE", "erro na nota", "nfe não envia" são agrupados.
                    Mantenha o chamado mais antigo e cancele os demais.
                  </p>
                </div>
              </div>
              <p className="text-text-dim text-xs font-medium ml-5">
                {loadingDuplicados ? 'Analisando...' : `${duplicados.length} grupo${duplicados.length !== 1 ? 's' : ''} com duplicação detectada${dupGrupo ? ` — ${GRUPO_INFO[dupGrupo]?.label || dupGrupo}` : ''}`}
              </p>
            </div>

            {loadingDuplicados ? (
              <p className="text-text-dim text-sm py-8 text-center">Analisando chamados em aberto...</p>
            ) : duplicados.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-2">
                <CheckCircle size={32} className="text-success/50" />
                <p className="text-text-dim text-sm">Nenhum chamado duplicado em aberto</p>
                <p className="text-text-muted text-xs">Clique em "Atualizar" para re-analisar</p>
              </div>
            ) : (
              <div className="space-y-3">
                {duplicados
                  .filter(g => g.tickets.some(t => !dismissedIds.has(String(t.id))))
                  .map((g, i) => (
                    <DuplicadoCard key={i} g={g} dismissedIds={dismissedIds} onDismissTicket={dismissTicket} />
                  ))}
              </div>
            )}
          </div>
        )}

        {/* METAS POR EQUIPE */}
        {tab === 'metas' && (
          <div className="space-y-4">
            {/* FILTROS NO TOPO */}
            <div className="flex items-center gap-2 flex-wrap">
              <SegmentedControl
                options={[
                  { key: '',         label: 'Todas'    },
                  { key: 'Fiscal',   label: 'Fiscal'   },
                  { key: 'Producao', label: 'Produção' },
                  { key: 'G1',       label: 'G1'       },
                  { key: 'GW',       label: 'GW'       },
                ]}
                value={metaGrupoFiltro}
                onChange={setMetaGrupoFiltro}
              />
              <div className="ml-auto flex items-center gap-2">
                <ExportMenu onTXT={exportMetasTXT} onCSV={exportMetasCSV} disabled={!metas?.length} />
                <button onClick={handleSyncMetaHistorico} disabled={syncingMetaHist || loadingMetas}
                  title="Busca dados históricos direto do Movidesk para meses anteriores ficarem precisos"
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-50">
                  <Zap size={12} className={syncingMetaHist ? 'animate-pulse text-accent' : ''} />
                  {syncingMetaHist ? 'Buscando...' : 'Sincronizar histórico'}
                </button>
                <button onClick={() => handleLoadMetas(metasSemanas)} disabled={loadingMetas}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-accent/10 hover:bg-accent/20 border border-accent/20 rounded-lg text-accent text-xs transition-colors disabled:opacity-50">
                  <RefreshCw size={12} className={loadingMetas ? 'animate-spin' : ''} />
                  Atualizar
                </button>
              </div>
            </div>

            {metaHistMsg && (
              <div className={`px-4 py-2 rounded-lg text-xs ${metaHistMsg.startsWith('Erro') ? 'bg-error/10 text-error border border-error/20' : 'bg-success/10 text-success border border-success/20'}`}>
                {metaHistMsg}
              </div>
            )}

            {/* Legenda */}
            <div className="bg-surface2 border border-border rounded-xl px-4 py-3">
              <p className="text-text text-xs font-semibold mb-1 flex items-center gap-1.5">
                <Target size={12} className="text-accent" /> Como a meta é calculada?
              </p>
              <p className="text-text-dim text-xs leading-relaxed">
                <strong>Mês atual:</strong> entradas reais ÷ analistas ÷ dias úteis decorridos (Seg–Sex, sem feriados) — bate com a aba Analistas.
                <strong className="ml-1">Meses anteriores:</strong> busca direto do Movidesk via "Sincronizar histórico" para garantir precisão.
                Ritmo real = fechados no mês ÷ dias úteis ÷ analistas.
              </p>
            </div>

            {metasErro && (
              <div className="bg-error/10 border border-error/30 rounded-xl px-4 py-3 text-error text-sm">
                Erro: {metasErro}
              </div>
            )}

            {loadingMetas ? (
              <p className="text-text-dim text-sm py-8 text-center">Calculando metas...</p>
            ) : metas === null ? (
              <p className="text-text-dim text-sm py-8 text-center">Carregando...</p>
            ) : metas.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-2">
                <Target size={32} className="text-text-dim/40" />
                <p className="text-text-dim text-sm">Nenhum dado disponível</p>
                <p className="text-text-muted text-xs">Sincronize os chamados primeiro</p>
              </div>
            ) : (
              <div className="space-y-6">
                {metas
                  .filter(eq => !metaGrupoFiltro || eq.grupo === metaGrupoFiltro)
                  .map(eq => {
                  const gi          = GRUPO_INFO[eq.grupo] || { label: eq.grupo, desc: '', color: 'text-text-dim' }
                  const ritmoOk     = eq.ritmo_ok ?? (eq.taxa_dia_analista >= eq.equilibrio_dia)
                  const borderColor = ritmoOk ? 'border-success/30' : eq.status === 'crescendo' ? 'border-error/40' : 'border-warning/30'
                  const statusBg    = ritmoOk ? 'text-success bg-success/10 border-success/20' : eq.status === 'crescendo' ? 'text-error bg-error/10 border-error/20' : 'text-warning bg-warning/10 border-warning/20'
                  const statusLabel = ritmoOk ? '✓ Ritmo positivo' : eq.status === 'crescendo' ? '↑ Fila crescendo' : '→ Ritmo abaixo da meta'
                  const ai          = metasAnalise[eq.grupo] || {}
                  const maxEnt      = Math.max(...(eq.historico_meses || []).map(m => m.entradas_proj || m.entradas), 1)

                  return (
                    <div key={eq.grupo} className={`border ${borderColor} rounded-2xl overflow-hidden`}>
                      {/* Cabeçalho do grupo */}
                      <div className="px-5 py-4">
                        <div className="flex items-center justify-between gap-3 flex-wrap mb-4">
                          <div>
                            <div className="flex items-center gap-2 flex-wrap">
                              <h3 className={`text-text font-bold text-lg ${gi.color}`}>{gi.label}</h3>
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${statusBg}`}>
                                {statusLabel}
                              </span>
                              <span className="text-text-muted text-xs">{eq.membros_count} analistas · {eq.dias_uteis_dec ?? '—'} dias úteis este mês</span>
                            </div>
                            <p className="text-text-muted text-xs mt-0.5">{gi.desc}</p>
                          </div>
                          <button onClick={() => handleMetasAnalise(eq.grupo)} disabled={ai.loading}
                            className="flex items-center gap-1.5 px-3 py-1.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
                            <Sparkles size={12} className={ai.loading ? 'animate-pulse' : ''} />
                            {ai.loading ? 'Analisando...' : 'Analisar com IA'}
                          </button>
                        </div>

                        {/* Histórico mensal */}
                        {eq.historico_meses?.length > 0 && (
                          <div className="mb-4">
                            <p className="text-text-dim text-[10px] uppercase tracking-wider font-semibold mb-2 flex items-center gap-1">
                              <Activity size={10} /> Entradas por mês
                              <InfoTooltip text="Chamados abertos por clientes em cada mês. Meses >25% acima da média são sinalizados — possível incidente, queda de sistema ou versão com bug." />
                            </p>
                            <div className="space-y-1.5">
                              {eq.historico_meses.map((mh, i) => {
                                const pct = Math.round(((mh.entradas_proj || mh.entradas) / maxEnt) * 100)
                                return (
                                  <div key={i}>
                                    <div className="flex items-center gap-3">
                                      <span className="text-text-dim text-xs w-16 text-right flex-shrink-0 font-mono">{mh.label}</span>
                                      <div className="flex-1 h-6 bg-surface2 rounded overflow-hidden">
                                        <div className={`h-full rounded transition-all ${mh.acima_media ? 'bg-error/60' : 'bg-accent/50'} ${mh.parcial ? 'opacity-70' : ''}`}
                                          style={{ width: `${pct}%` }} />
                                      </div>
                                      <span className="text-text text-xs font-mono font-bold w-12 text-right flex-shrink-0">
                                        {mh.entradas}{mh.parcial && <span className="text-accent font-normal text-[9px]"> ↻</span>}
                                      </span>
                                      <span className="text-text-muted text-[10px] w-24 text-right flex-shrink-0">
                                        meta {mh.equilibrio_dia}/dia/analista
                                      </span>
                                      {mh.acima_media && <span className="text-error text-[10px] flex-shrink-0 font-semibold">+{mh.pct_vs_media}% ⚠</span>}
                                    </div>
                                    {mh.acima_media && (
                                      <p className="text-error text-[10px] ml-20 mt-0.5">Mês atípico — provável incidente, versão ou queda de sistema.</p>
                                    )}
                                  </div>
                                )
                              })}
                            </div>
                            <p className="text-text-muted text-[10px] mt-1 ml-20">Média mensal (meses fechados): {eq.media_entradas_mes} chamados · Mês atual: entradas reais até hoje</p>
                          </div>
                        )}

                        {/* Cards de resumo */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                          <div className="bg-accent/10 border border-accent/20 rounded-xl p-3">
                            <p className="text-accent text-[10px] uppercase tracking-wider font-semibold flex items-center gap-0.5">
                              Meta/dia por analista
                              <InfoTooltip text="Entradas deste mês ÷ nº analistas ÷ dias úteis do mês (22). Ritmo mínimo para o mês terminar no zero a zero." />
                            </p>
                            <p className="text-accent font-bold text-2xl mt-1">{eq.equilibrio_dia}</p>
                            <p className="text-accent/60 text-[10px] mt-0.5">chamados/dia para equilibrar</p>
                          </div>
                          <div className={`border rounded-xl p-3 ${ritmoOk ? 'bg-success/10 border-success/20' : 'bg-error/10 border-error/20'}`}>
                            <p className={`text-[10px] uppercase tracking-wider font-semibold flex items-center gap-0.5 ${ritmoOk ? 'text-success' : 'text-error'}`}>
                              Ritmo real/dia
                              <InfoTooltip text="Chamados fechados neste mês ÷ dias úteis decorridos ÷ nº analistas. Baseado no mês corrente, como no Movidesk." />
                            </p>
                            <p className={`font-bold text-2xl mt-1 ${ritmoOk ? 'text-success' : 'text-error'}`}>{eq.taxa_dia_analista}</p>
                            <p className={`text-[10px] mt-0.5 ${ritmoOk ? 'text-success/60' : 'text-error/60'}`}>
                              {eq.fechados_mes ?? '—'} fechados · {eq.dias_uteis_dec ?? '—'} dias
                            </p>
                          </div>
                          <div className="bg-surface2 border border-border rounded-xl p-3">
                            <p className="text-text-muted text-[10px] uppercase tracking-wider font-semibold flex items-center gap-0.5">
                              Fila em aberto
                              <InfoTooltip text="Total de chamados em aberto agora. Contexto — a meta é baseada em entradas mensais, não em zerar a fila toda." />
                            </p>
                            <p className="text-text font-bold text-2xl mt-1">{eq.fila_total}</p>
                            <p className="text-text-muted text-[10px] mt-0.5">chamados em aberto</p>
                          </div>
                          <div className={`border rounded-xl p-3 ${eq.saldo_semana > 0 ? 'bg-success/5 border-success/20' : 'bg-error/5 border-error/20'}`}>
                            <p className="text-text-muted text-[10px] uppercase tracking-wider font-semibold flex items-center gap-0.5">
                              Saldo semanal
                              <InfoTooltip text="Fechamentos da equipe na semana − entradas da semana. Positivo = equipe está diminuindo a fila." />
                            </p>
                            <p className={`font-bold text-2xl mt-1 ${eq.saldo_semana > 0 ? 'text-success' : 'text-error'}`}>
                              {eq.saldo_semana > 0 ? '+' : ''}{eq.saldo_semana}
                            </p>
                            <p className="text-text-muted text-[10px] mt-0.5">fechados − entrados/sem</p>
                          </div>
                        </div>

                        {/* TABELA COMPLETA DE ANALISTAS */}
                        {eq.membros?.length > 0 && (
                          <div>
                            <p className="text-text-dim text-[10px] uppercase tracking-wider font-semibold mb-2 flex items-center gap-1">
                              <Users size={10} /> Desempenho por analista — mês atual
                              <InfoTooltip text="Ritmo/dia = fechados neste mês ÷ dias úteis decorridos. Meta/dia = entradas do mês ÷ analistas ÷ 22 dias. Verde = atingindo a meta." />
                            </p>
                            <div className="rounded-xl border border-border overflow-hidden">
                              <table className="w-full text-xs">
                                <thead className="bg-surface2">
                                  <tr>
                                    <th className="text-left px-4 py-2.5 text-text-dim font-semibold">Analista</th>
                                    <th className="text-right px-3 py-2.5 text-text-dim font-semibold whitespace-nowrap">Fechou este mês</th>
                                    <th className="text-right px-3 py-2.5 text-text-dim font-semibold whitespace-nowrap">Dias úteis</th>
                                    <th className="text-right px-3 py-2.5 text-text-dim font-semibold whitespace-nowrap">Ritmo/dia</th>
                                    <th className="text-right px-3 py-2.5 text-text-dim font-semibold whitespace-nowrap">Meta/dia</th>
                                    <th className="text-right px-3 py-2.5 text-text-dim font-semibold">Fila</th>
                                    <th className="text-center px-3 py-2.5 text-text-dim font-semibold">Status</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {eq.membros.map((m, i) => {
                                    const pct = (eq.equilibrio_dia || 0) > 0
                                      ? Math.min(((m.taxa_dia || 0) / eq.equilibrio_dia) * 100, 110)
                                      : 0
                                    return (
                                      <tr key={i} className={`border-t border-border/50 ${m.atingiu ? 'bg-success/5' : 'bg-error/5'}`}>
                                        <td className="px-4 py-3">
                                          <span className="text-text font-medium">{m.nome}</span>
                                          <div className="h-1 bg-surface2 rounded-full mt-1.5 overflow-hidden">
                                            <div className={`h-full rounded-full ${m.atingiu ? 'bg-success' : 'bg-error/70'}`}
                                              style={{ width: `${Math.min(pct, 100)}%` }} />
                                          </div>
                                        </td>
                                        <td className="px-3 py-3 text-right">
                                          <span className="text-text font-bold text-sm">{m.fechou_mes ?? m.fila ?? '—'}</span>
                                        </td>
                                        <td className="px-3 py-3 text-right text-text-dim">{m.dias_uteis ?? eq.dias_uteis_dec ?? '—'}</td>
                                        <td className="px-3 py-3 text-right">
                                          <span className={`font-bold ${m.atingiu ? 'text-success' : 'text-error'}`}>{m.taxa_dia}</span>
                                        </td>
                                        <td className="px-3 py-3 text-right text-text-dim">{m.meta_dia}</td>
                                        <td className="px-3 py-3 text-right text-text-dim">{m.fila}</td>
                                        <td className="px-3 py-3 text-center">
                                          {m.atingiu
                                            ? <span className="inline-flex items-center gap-1 text-success text-[10px] font-semibold"><CheckCircle size={11} /> Meta</span>
                                            : <span className="inline-flex items-center gap-1 text-error text-[10px] font-semibold"><AlertTriangle size={11} /> Abaixo</span>}
                                        </td>
                                      </tr>
                                    )
                                  })}
                                </tbody>
                              </table>
                            </div>
                            <p className="text-text-muted text-[10px] mt-2 leading-relaxed">
                              ⚠ Analista abaixo da meta em mês atípico (volume alto)? O problema provavelmente é o volume de incidentes, não o analista. Use "Analisar com IA" para contextualizar.
                            </p>
                          </div>
                        )}

                        {/* Top categorias */}
                        {eq.top_categorias?.length > 0 && (
                          <div className="mt-4">
                            <p className="text-text-dim text-[10px] uppercase tracking-wider font-semibold mb-2 flex items-center gap-1">
                              <Activity size={10} /> Top categorias na fila
                            </p>
                            <div className="space-y-1.5">
                              {eq.top_categorias.map(([cat, n], i) => {
                                const pct = eq.fila_total > 0 ? Math.round((n / eq.fila_total) * 100) : 0
                                return (
                                  <div key={i} className="flex items-center gap-2">
                                    <span className="text-text-dim text-xs w-5 text-right font-mono font-bold">{n}</span>
                                    <div className="flex-1 h-4 bg-surface2 rounded overflow-hidden">
                                      <div className="h-full bg-accent/50 rounded" style={{ width: `${pct}%` }} />
                                    </div>
                                    <span className="text-text text-xs truncate max-w-[220px]">{cat}</span>
                                    <span className="text-text-muted text-[10px] w-8 text-right">{pct}%</span>
                                  </div>
                                )
                              })}
                            </div>
                          </div>
                        )}

                        {/* Análise IA */}
                        {(ai.erro || ai.loading || ai.text) && (
                          <div className="mt-4">
                            {ai.erro && <p className="text-error text-xs">Erro: {ai.erro}</p>}
                            {ai.loading && (
                              <div className="flex items-center gap-2 py-2">
                                <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                <span className="text-text-dim text-xs">IA analisando equipe {gi.label}...</span>
                              </div>
                            )}
                            {ai.text && (
                              <div className="bg-surface2 border border-accent/20 rounded-xl p-4">
                                <div className="flex items-center justify-between mb-3">
                                  <p className="text-accent text-[10px] font-semibold uppercase tracking-wider flex items-center gap-1">
                                    <Sparkles size={10} /> Análise IA — {gi.label}
                                  </p>
                                  <CopyButton text={ai.text} />
                                </div>
                                <pre className="text-text text-sm font-sans whitespace-pre-wrap leading-relaxed">{ai.text}</pre>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}

                <p className="text-text-muted text-xs">
                  Meta calculada com base nas entradas de cada mês. Objetivo: terminar o mês no zero a zero — não zerar toda a fila de uma vez.
                </p>
              </div>
            )}
          </div>
        )}

        {/* SAZONALIDADE */}
        {tab === 'sazonalidade' && (
          <div className="space-y-4">
            {/* Info card */}
            <div className="bg-surface2 border border-border rounded-xl p-3 flex items-start gap-2">
              <Calendar size={14} className="text-accent mt-0.5 flex-shrink-0" />
              <p className="text-text-dim text-xs leading-relaxed">
                Mostra o <strong>volume de chamados abertos por semana ou mês</strong>. Use "Explicar com IA" para entender o porquê dos picos — sazonalidade fiscal, atualizações do sistema, períodos de alta demanda, etc.
              </p>
            </div>

            {/* Controles */}
            <div className="flex items-center gap-3 flex-wrap">
              <div>
                <p className="text-text-dim text-xs uppercase tracking-wider font-semibold mb-0.5">Volume de abertura de chamados</p>
                <p className="text-accent text-xs">{periodoAtualLabel}</p>
              </div>
              <div className="ml-auto flex items-center gap-2 flex-wrap">
                <SegmentedControl
                  options={[{ key: 'semana', label: 'Por semana' }, { key: 'mes', label: 'Por mês' }]}
                  value={sazoAgrup}
                  onChange={v => { setSazoAgrup(v); handleLoadSazo(v, sazoGrupo) }}
                  size="xs"
                />
                <SegmentedControl
                  options={GRUPOS}
                  value={sazoGrupo}
                  onChange={v => { setSazoGrupo(v); handleLoadSazo(sazoAgrup, v) }}
                  size="xs"
                />
                <button onClick={() => handleLoadSazo()} disabled={loadingSazo}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-text-dim text-xs transition-colors disabled:opacity-50">
                  <RefreshCw size={12} className={loadingSazo ? 'animate-spin' : ''} />
                </button>
                <button onClick={handleSazoAnalise} disabled={loadingSazoAI || loadingSazo || sazoData.length === 0}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-xs font-medium transition-colors disabled:opacity-50">
                  <Sparkles size={12} className={loadingSazoAI ? 'animate-pulse' : ''} />
                  {loadingSazoAI ? 'Analisando...' : 'Explicar com IA'}
                </button>
              </div>
            </div>

            {loadingSazo ? (
              <p className="text-text-dim text-sm py-8 text-center">Carregando dados...</p>
            ) : sazoData.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-2">
                <Calendar size={32} className="text-text-dim/40" />
                <p className="text-text-dim text-sm">Nenhum dado no período selecionado</p>
                <p className="text-text-muted text-xs">Tente um período mais longo como "90 dias" ou "6 meses"</p>
              </div>
            ) : (() => {
              const maxTotal = Math.max(...sazoData.map(p => p.total), 1)
              const media    = Math.round(sazoData.reduce((s, p) => s + p.total, 0) / sazoData.length)
              return (
                <div className="space-y-3">
                  <div className="flex gap-4 text-xs text-text-dim flex-wrap">
                    <span>Total: <strong className="text-text">{sazoData.reduce((s,p)=>s+p.total,0)}</strong></span>
                    <span>Média/{sazoAgrup === 'semana' ? 'semana' : 'mês'}: <strong className="text-text">{media}</strong></span>
                    <span>Pico: <strong className="text-accent">{Math.max(...sazoData.map(p=>p.total))}</strong> ({sazoData.find(p=>p.total===Math.max(...sazoData.map(x=>x.total)))?.label})</span>
                  </div>

                  <div className="space-y-1.5">
                    {sazoData.map((p, i) => {
                      const isPico       = p.total === maxTotal
                      const prev         = i > 0 ? sazoData[i-1].total : null
                      const delta        = prev !== null ? p.total - prev : null
                      const acimaDaMedia = p.total > media * 1.2
                      return (
                        <div key={p.key} className="group">
                          <div className="flex items-center gap-3">
                            <span className="text-text-dim font-mono text-xs w-12 text-right flex-shrink-0">{p.label}</span>
                            <div className="flex-1 h-6 bg-surface2 rounded-md overflow-hidden relative">
                              <div
                                className={`h-full rounded-md transition-all ${isPico ? 'bg-error/70' : acimaDaMedia ? 'bg-warning/60' : 'bg-accent/50'}`}
                                style={{ width: `${(p.total / maxTotal) * 100}%` }}
                              />
                              <div className="absolute top-0 bottom-0 border-l border-dashed border-text-dim/30"
                                style={{ left: `${(media / maxTotal) * 100}%` }} />
                            </div>
                            <span className={`font-mono text-xs w-8 text-right flex-shrink-0 font-bold ${isPico ? 'text-error' : acimaDaMedia ? 'text-warning' : 'text-text'}`}>
                              {p.total}
                            </span>
                            {delta !== null && (
                              <span className={`text-[10px] w-10 flex-shrink-0 ${delta > 0 ? 'text-error' : delta < 0 ? 'text-success' : 'text-text-dim'}`}>
                                {delta > 0 ? `+${delta}` : delta < 0 ? `${delta}` : '—'}
                              </span>
                            )}
                          </div>
                          {p.top_categorias?.length > 0 && (
                            <div className="hidden group-hover:flex ml-15 pl-16 gap-2 flex-wrap text-[10px] text-text-muted mt-0.5 pb-1">
                              {p.top_categorias.slice(0,3).map(([cat,n],j) => (
                                <span key={j} className="bg-surface2 border border-border rounded px-1.5 py-0.5">{cat} ({n})</span>
                              ))}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>

                  <div className="flex items-center gap-4 text-[10px] text-text-dim pt-1">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-error/70 inline-block" /> Pico máximo</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-warning/60 inline-block" /> Acima da média</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-accent/50 inline-block" /> Normal</span>
                    <span>| Linha tracejada = média ({media})</span>
                  </div>

                  {(sazoAnalise || loadingSazoAI) && (
                    <div className="bg-surface2 border border-border rounded-xl p-5 mt-2">
                      {loadingSazoAI ? (
                        <div className="flex items-center gap-3 py-4 justify-center">
                          <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                          <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                          <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        </div>
                      ) : (
                        <>
                          <div className="flex justify-between items-center mb-3">
                            <p className="text-accent text-xs font-semibold uppercase tracking-wider flex items-center gap-1">
                              <Sparkles size={11} /> Análise IA — Explicação dos picos
                            </p>
                            <CopyButton text={sazoAnalise} />
                          </div>
                          <pre className="text-text text-sm font-sans whitespace-pre-wrap leading-relaxed">{sazoAnalise}</pre>
                        </>
                      )}
                    </div>
                  )}
                </div>
              )
            })()}
          </div>
        )}

        {/* ANÁLISE IA */}
        {tab === 'analise' && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 flex-wrap">
              <div className="flex items-center gap-2">
                <Clock size={13} className="text-accent" />
                <span className="text-text-dim text-xs">Período:</span>
                <span className="text-accent text-xs font-semibold">{periodoAtualLabel}</span>
                {hasFilters && <span className="text-warning text-xs">(filtrado)</span>}
              </div>
              <button onClick={handleGerarAnalise} disabled={loadingAnalise}
                className="flex items-center gap-1.5 px-4 py-1.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50 ml-auto">
                <Sparkles size={13} className={loadingAnalise ? 'animate-pulse' : ''} />
                {loadingAnalise ? 'Analisando...' : 'Gerar Relatório'}
              </button>
            </div>

            {analiseStats && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <StatCard label="Chamados no período" value={analiseStats.total_periodo} color="accent" />
                <StatCard label="Esta semana" value={analiseStats.esta_semana} color="accent" />
                <StatCard label="Fora SLA (>3d)"
                  value={`${analiseStats.fora_sla_count} (${analiseStats.fora_sla_pct}%)`}
                  color={analiseStats.fora_sla_pct > 20 ? 'error' : 'warning'} />
                <StatCard label="Categorias em alta" value={analiseStats.crescimento_semana?.length || 0} color="warning" />
              </div>
            )}

            {analise ? (
              <div className="bg-surface2 border border-border rounded-xl p-5">
                <div className="flex justify-end mb-2">
                  <CopyButton text={analise} />
                </div>
                <pre className="text-text text-sm font-sans whitespace-pre-wrap leading-relaxed">{analise}</pre>
              </div>
            ) : !loadingAnalise && (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <Sparkles size={32} className="text-accent/40" />
                <p className="text-text-dim text-sm">Clique em "Gerar Relatório" para analisar os dados com IA</p>
                <p className="text-text-muted text-xs">A IA analisa volume, SLA, tendências e sugere ações práticas</p>
              </div>
            )}

            {loadingAnalise && (
              <div className="flex items-center gap-3 py-8 justify-center">
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            )}
          </div>
        )}

        {/* CHAT COM IA */}
        {tab === 'ia-chat' && (
          <div className="flex flex-col h-full" style={{ minHeight: '500px' }}>
            <div className="flex items-center gap-2 mb-3 flex-wrap">
              <Clock size={13} className="text-accent" />
              <span className="text-text-dim text-xs">Contexto:</span>
              <span className="text-accent text-xs font-semibold">{periodoAtualLabel}</span>
              {hasFilters && (
                <span className="text-warning text-xs">· {[filterAnalista, filterCategoria].filter(Boolean).join(' · ')}</span>
              )}
              {chatMsgs.length > 0 && (
                <button onClick={() => setChatMsgs([])}
                  className="ml-auto text-xs text-text-muted hover:text-error transition-colors">
                  Limpar conversa
                </button>
              )}
            </div>

            {chatMsgs.length === 0 && (
              <div className="mb-4">
                <p className="text-text-dim text-xs mb-2 uppercase tracking-wider font-semibold">Perguntas rápidas</p>
                <div className="flex flex-wrap gap-2">
                  {PERGUNTAS_RAPIDAS.map(q => (
                    <button key={q} onClick={() => handleChatSend(q)}
                      className="px-3 py-1.5 bg-surface2 hover:bg-surface border border-border rounded-lg text-xs text-text-dim hover:text-text transition-colors">
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="flex-1 overflow-y-auto space-y-3 mb-3">
              {chatMsgs.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] rounded-xl px-4 py-3 text-sm relative group
                    ${m.role === 'user'
                      ? 'bg-accent/15 border border-accent/20 text-text'
                      : m.isError
                        ? 'bg-error/10 border border-error/20 text-error'
                        : 'bg-surface2 border border-border text-text'}`}>
                    {m.role === 'assistant' && !m.isError && (
                      <div className="flex justify-end mb-1.5">
                        <CopyButton text={m.content} />
                      </div>
                    )}
                    <pre className="whitespace-pre-wrap font-sans leading-relaxed">{m.content}</pre>
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="bg-surface2 border border-border rounded-xl px-4 py-3 flex gap-1.5">
                    <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-1.5 h-1.5 bg-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form onSubmit={e => { e.preventDefault(); handleChatSend() }} className="flex gap-2">
              <input value={chatInput} onChange={e => setChatInput(e.target.value)}
                placeholder='Ex: "quantos chamados o Alan fechou hoje?" ou "quem está com mais SLA estourado?"'
                disabled={chatLoading}
                className="flex-1 bg-surface2 border border-border rounded-xl px-4 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors disabled:opacity-50" />
              <button type="submit" disabled={chatLoading || !chatInput.trim()}
                className="p-2.5 bg-accent hover:bg-accent-hover text-white rounded-xl transition-colors disabled:opacity-40">
                <Send size={15} />
              </button>
            </form>
          </div>
        )}

      </div>
    </div>
  )
}
