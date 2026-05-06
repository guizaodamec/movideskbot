import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import api from '../api/backend'

/* ─── Constants ──────────────────────────────────────────────────────────── */

const ROTATION_INTERVAL = 30 // seconds
const FETCH_INTERVAL    = 5 * 60 * 1000

const TEAM_COLORS = {
  Fiscal:   { accent: '#F59E0B', bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.28)' },
  Producao: { accent: '#10B981', bg: 'rgba(16,185,129,0.12)', border: 'rgba(16,185,129,0.28)' },
  G1:       { accent: '#8B5CF6', bg: 'rgba(139,92,246,0.12)', border: 'rgba(139,92,246,0.28)' },
  GW:       { accent: '#EC4899', bg: 'rgba(236,72,153,0.12)', border: 'rgba(236,72,153,0.28)' },
}

/* ─── Hooks ──────────────────────────────────────────────────────────────── */

function useClock() {
  const [now, setNow] = useState(new Date())
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(id)
  }, [])
  return now
}

function useCountdown() {
  const [cd, setCd] = useState({ d: 0, h: 0, m: 0, s: 0, urgent: false })
  useEffect(() => {
    const calc = () => {
      const now   = new Date()
      const dow   = now.getDay()
      const toSat = ((6 - dow) + 7) % 7 || 7
      const sat   = new Date(now)
      sat.setDate(now.getDate() + toSat)
      sat.setHours(0, 0, 0, 0)
      const diff   = sat - now
      const urgent = diff <= 3600000
      setCd({
        d: Math.floor(diff / 86400000),
        h: Math.floor((diff % 86400000) / 3600000),
        m: Math.floor((diff % 3600000)  / 60000),
        s: Math.floor((diff % 60000)    / 1000),
        urgent,
      })
    }
    calc()
    const id = setInterval(calc, 1000)
    return () => clearInterval(id)
  }, [])
  return cd
}

function useCountUp(target, duration = 800) {
  const [val, setVal] = useState(0)
  const fromRef = useRef(0)
  useEffect(() => {
    const from = fromRef.current
    if (from === target) { fromRef.current = target; return }
    const start = Date.now()
    let raf
    const step = () => {
      const progress = Math.min((Date.now() - start) / duration, 1)
      const eased    = 1 - Math.pow(1 - progress, 3)
      setVal(Math.round(from + (target - from) * eased))
      if (progress < 1) raf = requestAnimationFrame(step)
      else fromRef.current = target
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [target, duration])
  return val
}

/* ─── Helpers ────────────────────────────────────────────────────────────── */

function pad2(n) { return String(n).padStart(2, '0') }

function saldoColor(s) {
  return s > 0 ? '#10B981' : s < 0 ? '#EF4444' : '#F59E0B'
}

function SaldoDisplay({ saldo, size = 'text-sm' }) {
  const color = saldoColor(saldo)
  return (
    <span className={`font-mono font-bold ${size}`} style={{ color }}>
      {saldo > 0 ? '+' : ''}{saldo}
    </span>
  )
}

/* ─── Progress bar with shimmer ──────────────────────────────────────────── */

function ProgressBar({ pct, color, height = 6 }) {
  return (
    <div className="relative rounded-full overflow-hidden flex-shrink-0"
         style={{ height, background: 'rgba(255,255,255,0.07)' }}>
      <motion.div
        className="absolute inset-y-0 left-0 rounded-full progress-shimmer"
        initial={{ width: 0 }}
        animate={{ width: `${Math.min(pct, 100)}%` }}
        transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
        style={{ background: color }}
      />
    </div>
  )
}

/* ─── Total card (top of Metas) ─────────────────────────────────────────── */

function TotalCard({ label, value, color }) {
  const displayed = useCountUp(value)
  return (
    <div className="flex-1 rounded-xl border px-4 py-2.5 flex items-center justify-between"
         style={{ background: 'rgba(255,255,255,0.03)', borderColor: 'rgba(255,255,255,0.07)' }}>
      <span className="text-text-dim text-sm">{label}</span>
      <span className="font-mono font-bold text-2xl" style={{ color }}>
        {label === 'Saldo' && displayed > 0 ? '+' : ''}{displayed}
      </span>
    </div>
  )
}

/* ─── Individual analista card ───────────────────────────────────────────── */

function AnalistaCard({ analista, rank, prevRank }) {
  const c = TEAM_COLORS[analista.equipe] || TEAM_COLORS.G1
  const barColor = saldoColor(analista.saldo)
  const barPct   = analista.entrados > 0
    ? Math.min((analista.fechados / analista.entrados) * 100, 100)
    : analista.fechados > 0 ? 100 : 0
  const isLeader = rank === 0
  const movedUp   = prevRank !== undefined && prevRank !== null && prevRank > rank
  const movedDown = prevRank !== undefined && prevRank !== null && prevRank < rank

  return (
    <motion.div
      layout
      layoutId={`card-${analista.nome}`}
      className="flex items-center gap-3 px-4 rounded-xl border flex-shrink-0"
      style={{
        height: 46,
        background: isLeader
          ? 'linear-gradient(135deg,rgba(245,158,11,0.13),rgba(245,158,11,0.03))'
          : 'rgba(255,255,255,0.025)',
        borderColor: isLeader ? 'rgba(245,158,11,0.4)' : 'rgba(255,255,255,0.05)',
      }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
    >
      {/* Rank */}
      <div className="w-9 flex-shrink-0 flex items-center justify-center">
        {rank === 0 && <span className="medal-pulse text-xl leading-none">🥇</span>}
        {rank === 1 && <span className="text-xl leading-none">🥈</span>}
        {rank === 2 && <span className="text-xl leading-none">🥉</span>}
        {rank  > 2  && <span className="font-mono text-sm text-text-dim">#{rank + 1}</span>}
      </div>

      {/* Avatar */}
      <div className="w-8 h-8 flex-shrink-0 rounded-xl flex items-center justify-center font-bold text-sm"
           style={{ background: c.bg, border: `1.5px solid ${c.border}`, color: c.accent }}>
        {analista.display[0]}
      </div>

      {/* Name */}
      <div className="flex items-center gap-1.5 w-[110px] flex-shrink-0">
        <span className="font-semibold text-white text-sm leading-none truncate">{analista.display}</span>
        {(movedUp || movedDown) && (
          <motion.span
            key={`mv-${rank}-${prevRank}`}
            initial={{ opacity: 1 }}
            animate={{ opacity: 0 }}
            transition={{ duration: 2 }}
            className={`text-xs font-bold flex-shrink-0 ${movedUp ? 'text-emerald-400' : 'text-red-400'}`}
          >
            {movedUp ? '↑' : '↓'}
          </motion.span>
        )}
      </div>

      {/* Team tag */}
      <span className="text-[10px] font-bold px-1.5 py-0.5 rounded flex-shrink-0"
            style={{ background: c.bg, color: c.accent, border: `1px solid ${c.border}` }}>
        {analista.equipe === 'Producao' ? 'Prod.' : analista.equipe}
      </span>

      {/* Bar */}
      <div className="flex-1 min-w-0">
        <ProgressBar pct={barPct} color={barColor} height={5} />
      </div>

      {/* Stats */}
      <div className="flex items-center gap-4 flex-shrink-0">
        <div className="text-right">
          <div className="text-[10px] text-text-dim leading-none mb-0.5">Entr.</div>
          <div className="font-mono font-bold text-sm text-white leading-none">{analista.entrados}</div>
        </div>
        <div className="text-right">
          <div className="text-[10px] text-text-dim leading-none mb-0.5">Fech.</div>
          <div className="font-mono font-bold text-sm text-white leading-none">{analista.fechados}</div>
        </div>
        <div className="text-right w-10">
          <div className="text-[10px] text-text-dim leading-none mb-0.5">Saldo</div>
          <SaldoDisplay saldo={analista.saldo} size="text-sm" />
        </div>
      </div>
    </motion.div>
  )
}

/* ─── Team card (Desempenho tab) ─────────────────────────────────────────── */

function EquipeCard({ equipe, index, isLeader }) {
  const c        = TEAM_COLORS[equipe.chave] || TEAM_COLORS.G1
  const entrados = useCountUp(equipe.entrados)
  const fechados = useCountUp(equipe.fechados)
  const barColor = saldoColor(equipe.saldo)
  const barPct   = equipe.entrados > 0
    ? Math.min((equipe.fechados / equipe.entrados) * 100, 100)
    : 0

  return (
    <motion.div
      initial={{ opacity: 0, y: 28 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ delay: index * 0.12, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="relative rounded-2xl border p-5 flex flex-col gap-3 overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${c.bg}, rgba(8,12,24,0.85))`,
        borderColor: isLeader ? c.accent : c.border,
        boxShadow:   isLeader ? `0 0 28px ${c.accent}28` : undefined,
      }}
    >
      {isLeader && (
        <motion.div
          className="absolute top-0 left-0 right-0 h-px"
          style={{ background: c.accent }}
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      )}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-bold text-2xl leading-none" style={{ color: c.accent }}>{equipe.nome}</h3>
          <p className="text-text-dim text-xs mt-1">{equipe.analistas} analistas</p>
        </div>
        <div>
          {equipe.saldo > 0 && (
            <span className="text-emerald-400 text-xs font-bold px-2.5 py-1 rounded-lg bg-emerald-400/10 border border-emerald-400/20">
              ▲ Superávit
            </span>
          )}
          {equipe.saldo < 0 && (
            <span className="text-red-400 text-xs font-bold px-2.5 py-1 rounded-lg bg-red-400/10 border border-red-400/20">
              ▼ Déficit
            </span>
          )}
          {equipe.saldo === 0 && (
            <span className="text-amber-400 text-xs font-bold px-2.5 py-1 rounded-lg bg-amber-400/10 border border-amber-400/20">
              = Neutro
            </span>
          )}
        </div>
      </div>

      {/* Metrics 2×2 grid */}
      <div className="grid grid-cols-4 gap-2">
        {[
          { label: 'Entrados', val: entrados,           color: '#94A3B8',     prefix: '',  suffix: ''  },
          { label: 'Fechados', val: fechados,           color: '#E2E8F6',     prefix: '',  suffix: ''  },
          { label: 'Saldo',    val: equipe.saldo,       color: barColor,      prefix: equipe.saldo > 0 ? '+' : '', suffix: '' },
          { label: 'Taxa',     val: equipe.taxa_resolucao, color: c.accent,   prefix: '',  suffix: '%' },
        ].map(({ label, val, color, prefix, suffix }) => (
          <div key={label} className="text-center rounded-xl py-3"
               style={{ background: 'rgba(255,255,255,0.04)' }}>
            <div className="text-[11px] text-text-dim leading-none mb-1.5">{label}</div>
            <div className="font-mono font-bold text-2xl leading-none" style={{ color }}>
              {prefix}{val}{suffix}
            </div>
          </div>
        ))}
      </div>

      {/* Progress */}
      <ProgressBar pct={barPct} color={barColor} height={7} />
    </motion.div>
  )
}

/* ─── Main component ─────────────────────────────────────────────────────── */

export default function Painel() {
  const [data,     setData]     = useState(null)
  const [loading,  setLoading]  = useState(true)
  const [error,    setError]    = useState('')
  const [tab,      setTab]      = useState('metas')
  const [paused,   setPaused]   = useState(false)
  const [timeLeft, setTimeLeft] = useState(ROTATION_INTERVAL)

  const clock      = useClock()
  const countdown  = useCountdown()
  const prevOrderRef = useRef({})

  /* ── Fetch ── */
  const fetchData = async () => {
    try {
      const { data: res } = await api.painelSemanal()
      setData(prev => {
        if (prev?.analistas) {
          const order = {}
          prev.analistas.forEach((a, i) => { order[a.nome] = i })
          prevOrderRef.current = order
        }
        return res
      })
      setError('')
    } catch (e) {
      setError(e.response?.data?.error || e.message || 'Erro ao buscar dados')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const id = setInterval(fetchData, FETCH_INTERVAL)
    return () => clearInterval(id)
  }, [])

  /* ── Tab rotation ── */
  useEffect(() => {
    if (paused) return
    setTimeLeft(ROTATION_INTERVAL)
    const start = Date.now()
    let switched = false
    const id = setInterval(() => {
      const elapsed = (Date.now() - start) / 1000
      setTimeLeft(Math.max(0, ROTATION_INTERVAL - elapsed))
      if (elapsed >= ROTATION_INTERVAL && !switched) {
        switched = true
        setTab(t => t === 'metas' ? 'desempenho' : 'metas')
      }
    }, 200)
    return () => clearInterval(id)
  }, [tab, paused])

  /* ── Derived ── */
  const analistas   = data?.analistas || []
  const equipes     = data?.equipes   || []
  const totais      = data?.totais    || { entrados: 0, fechados: 0, saldo: 0 }
  const leader      = analistas.find(a => a.saldo > 0)
  const leaderEq    = equipes.reduce((best, e) =>
    (!best || e.saldo > best.saldo) ? e : best, null
  )
  const progressPct = ((ROTATION_INTERVAL - timeLeft) / ROTATION_INTERVAL) * 100

  const timeStr = `${pad2(clock.getHours())}:${pad2(clock.getMinutes())}:${pad2(clock.getSeconds())}`
  const dateStr = clock.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' })

  return (
    <div className="flex flex-col h-full overflow-hidden select-none"
         style={{ background: '#080c18' }}>

      {/* Scanline overlay */}
      <div className="painel-scanline" />

      {/* ── Header ── */}
      <div className="flex items-center justify-between px-6 flex-shrink-0"
           style={{ height: 56, borderBottom: '1px solid rgba(255,255,255,0.05)' }}>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400"
                 style={{ animation: 'pulse-dot 2s ease-in-out infinite' }} />
            <span className="font-bold text-white text-lg tracking-tight">FarmaFácil Suporte</span>
          </div>
          <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full text-text-dim"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
            📺 TV
          </span>
        </div>

        <div className="text-center">
          {error && !data && <span className="text-red-400 text-xs">{error}</span>}
          {loading && !data && <span className="text-text-dim text-xs animate-pulse">Carregando dados...</span>}
          {data && (
            <span className="text-text-dim text-xs">
              Semana {data.semana_inicio} — {data.semana_fim}
              {data.updated_at && <> · atualizado {data.updated_at}</>}
            </span>
          )}
        </div>

        <div className="text-right">
          <div className="font-mono font-bold text-2xl text-white leading-none">{timeStr}</div>
          <div className="text-text-dim text-xs capitalize mt-0.5">{dateStr}</div>
        </div>
      </div>

      {/* ── Tab bar ── */}
      <div className="flex items-center px-6 gap-3 flex-shrink-0"
           style={{ height: 42, borderBottom: '1px solid rgba(255,255,255,0.05)' }}>

        {[
          { key: 'metas',      label: '🏆 Metas Individuais' },
          { key: 'desempenho', label: '📊 Desempenho por Equipe' },
        ].map(({ key, label }) => (
          <button
            key={key}
            onClick={() => { setTab(key); setTimeLeft(ROTATION_INTERVAL) }}
            className="text-sm font-semibold px-3.5 py-1 rounded-lg transition-all"
            style={tab === key ? {
              background: 'rgba(59,130,246,0.13)',
              color: '#60A5FA',
              border: '1px solid rgba(59,130,246,0.28)',
            } : {
              color: '#4B5A72',
              border: '1px solid transparent',
            }}
          >
            {label}
          </button>
        ))}

        {/* Rotation progress */}
        <div className="flex-1 flex items-center gap-2 ml-2">
          <div className="flex-1 h-0.5 rounded-full overflow-hidden"
               style={{ background: 'rgba(255,255,255,0.06)' }}>
            <motion.div
              className="h-full rounded-full"
              style={{ background: 'rgba(99,102,241,0.45)' }}
              animate={{ width: `${progressPct}%` }}
              transition={{ duration: 0.2 }}
            />
          </div>
          <span className="font-mono text-[11px] text-text-dim w-6 text-right">
            {Math.ceil(timeLeft)}s
          </span>
        </div>

        <button
          onClick={() => setPaused(p => !p)}
          className="px-3 py-1 rounded-lg text-xs font-semibold transition-all"
          style={paused ? {
            background: 'rgba(245,158,11,0.12)',
            color: '#F59E0B',
            border: '1px solid rgba(245,158,11,0.28)',
          } : {
            background: 'rgba(255,255,255,0.04)',
            color: '#4B5A72',
            border: '1px solid rgba(255,255,255,0.07)',
          }}
        >
          {paused ? '▶ Retomar' : '⏸ Pausar'}
        </button>

        <button
          onClick={fetchData}
          className="px-3 py-1 rounded-lg text-xs font-semibold transition-all"
          style={{
            background: 'rgba(255,255,255,0.04)',
            color: '#4B5A72',
            border: '1px solid rgba(255,255,255,0.07)',
          }}
          title="Atualizar agora"
        >
          ↺
        </button>
      </div>

      {/* ── Content ── */}
      <div className="flex-1 overflow-hidden px-6 py-3">
        <AnimatePresence mode="wait">

          {/* ── Metas tab ── */}
          {tab === 'metas' && (
            <motion.div
              key="metas"
              initial={{ opacity: 0, x: -16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 16 }}
              transition={{ duration: 0.25 }}
              className="flex flex-col gap-2.5 h-full"
            >
              {/* Global totals */}
              <div className="flex gap-3 flex-shrink-0">
                <TotalCard label="Entrados" value={totais.entrados} color="#94A3B8" />
                <TotalCard label="Fechados" value={totais.fechados} color="#E2E8F6" />
                <TotalCard label="Saldo"    value={totais.saldo}    color={saldoColor(totais.saldo)} />
              </div>

              {/* Leader banner */}
              {leader && (
                <motion.div
                  key={`leader-${leader.nome}`}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex-shrink-0 flex items-center gap-4 px-5 py-2.5 rounded-xl"
                  style={{
                    background: 'linear-gradient(135deg,rgba(245,158,11,0.16),rgba(245,158,11,0.03))',
                    border: '1px solid rgba(245,158,11,0.38)',
                    boxShadow: '0 0 20px rgba(245,158,11,0.1)',
                  }}
                >
                  <span className="medal-pulse text-3xl leading-none">🥇</span>
                  <div>
                    <div className="text-amber-500 text-[10px] font-bold uppercase tracking-widest leading-none mb-1">
                      Líder da semana
                    </div>
                    <div className="font-bold text-white text-xl leading-none">{leader.display}</div>
                  </div>
                  <div className="ml-auto flex items-center gap-5">
                    <div className="text-right">
                      <div className="text-amber-500/70 text-[10px] leading-none mb-0.5">Saldo</div>
                      <div className="font-mono font-bold text-amber-300 text-xl leading-none">+{leader.saldo}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-text-dim text-[10px] leading-none mb-0.5">Fechados</div>
                      <div className="font-mono font-bold text-white text-xl leading-none">{leader.fechados}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-text-dim text-[10px] leading-none mb-0.5">Entrados</div>
                      <div className="font-mono font-bold text-white text-xl leading-none">{leader.entrados}</div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Countdown */}
              <div
                className="flex-shrink-0 flex items-center gap-3 px-4 py-1.5 rounded-xl"
                style={{
                  background: countdown.urgent ? 'rgba(245,158,11,0.07)' : 'rgba(255,255,255,0.02)',
                  border: `1px solid ${countdown.urgent ? 'rgba(245,158,11,0.28)' : 'rgba(255,255,255,0.05)'}`,
                }}
              >
                <span className="text-text-dim text-[11px]">Reset em:</span>
                <span
                  className="font-mono font-bold text-sm"
                  style={{ color: countdown.urgent ? '#F59E0B' : '#6B7A94' }}
                >
                  {countdown.d > 0 && `${countdown.d}d `}
                  {pad2(countdown.h)}:{pad2(countdown.m)}:{pad2(countdown.s)}
                </span>
                {countdown.urgent && (
                  <motion.span
                    className="text-amber-400 text-[11px] font-bold"
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 1, repeat: Infinity }}
                  >
                    ⚠ Menos de 1h
                  </motion.span>
                )}
              </div>

              {/* Ranking */}
              <div className="flex-1 flex flex-col gap-1.5 overflow-hidden">
                {analistas.length > 0 ? (
                  analistas.map((a, i) => (
                    <AnalistaCard
                      key={a.nome}
                      analista={a}
                      rank={i}
                      prevRank={prevOrderRef.current[a.nome] ?? null}
                    />
                  ))
                ) : (
                  <div className="flex-1 flex items-center justify-center text-text-dim text-sm">
                    {loading ? 'Carregando...' : 'Nenhum dado para esta semana.'}
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {/* ── Desempenho tab ── */}
          {tab === 'desempenho' && (
            <motion.div
              key="desempenho"
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -16 }}
              transition={{ duration: 0.25 }}
              className="h-full"
              style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: '1fr 1fr', gap: '1rem' }}
            >
              {equipes.length > 0 ? (
                equipes.map((eq, i) => (
                  <EquipeCard
                    key={eq.chave}
                    equipe={eq}
                    index={i}
                    isLeader={leaderEq?.chave === eq.chave && eq.saldo > 0}
                  />
                ))
              ) : (
                <div className="col-span-2 row-span-2 flex items-center justify-center text-text-dim text-sm">
                  {loading ? 'Carregando dados...' : 'Nenhum dado disponível.'}
                </div>
              )}
            </motion.div>
          )}

        </AnimatePresence>
      </div>
    </div>
  )
}
