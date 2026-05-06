import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { RefreshCw, CheckCircle, XCircle, Building, Database, Zap, AlertTriangle, Clock } from 'lucide-react'
import api from '../api/backend'

function Card({ children, className = '', delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={'bg-surface rounded-card border border-border p-4 ' + className}
    >
      {children}
    </motion.div>
  )
}

function SectionTitle({ icon: Icon, label, color = 'text-accent' }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <Icon size={14} className={color} />
      <h4 className="text-text text-[11px] font-semibold uppercase tracking-wider">{label}</h4>
    </div>
  )
}

export default function Profile({ profile: initialProfile }) {
  const [profile, setProfile] = useState(initialProfile)
  const [scanning, setScanning] = useState(false)
  const [lastScan, setLastScan] = useState(null)

  useEffect(() => {
    if (initialProfile) {
      setProfile(initialProfile)
      setLastScan(new Date())
    }
  }, [initialProfile])

  const handleRefresh = async () => {
    setScanning(true)
    try {
      await api.scan()
      const poll = setInterval(async () => {
        try {
          const res = await api.scanStatus()
          if (res.data.done && !res.data.error) {
            clearInterval(poll)
            const pRes = await api.perfil()
            setProfile(pRes.data)
            setLastScan(new Date())
            setScanning(false)
          } else if (res.data.error) {
            clearInterval(poll)
            setScanning(false)
          }
        } catch {
          clearInterval(poll)
          setScanning(false)
        }
      }, 600)
    } catch {
      setScanning(false)
    }
  }

  if (!profile || Object.keys(profile).length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-text-dim text-sm">
        Aguardando dados do perfil...
      </div>
    )
  }

  const empresa    = profile.razao_social || profile.empresa || '—'
  const cnpj       = profile.cnpj || '—'
  const cidade     = [profile.cidade, profile.uf].filter(Boolean).join(' / ') || '—'
  const regime     = profile.regime_tributario || '—'
  const versao     = profile.versao_sistema || '—'
  const postgres   = profile.versao_postgres || '—'
  const backup     = profile.ultimo_backup || '—'
  const modulos    = profile.modulos || []
  const volumes    = profile.volumes || []
  const erros      = profile.erros_recorrentes || []
  const lentas     = profile.queries_lentas || []

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex items-center justify-between flex-shrink-0">
        <div>
          <h2 className="text-text font-semibold text-sm">Perfil do Cliente</h2>
          {lastScan && (
            <p className="text-text-dim text-xs mt-0.5 flex items-center gap-1">
              <Clock size={10} />
              Atualizado às {lastScan.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
            </p>
          )}
        </div>
        <button
          onClick={handleRefresh}
          disabled={scanning}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-surface2 hover:bg-border text-text-dim hover:text-text rounded-lg text-xs transition-colors disabled:opacity-50"
        >
          <RefreshCw size={12} className={scanning ? 'animate-spin' : ''} />
          Atualizar scan
        </button>
      </div>

      {/* Conteúdo */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="grid grid-cols-2 gap-3 max-w-4xl">

          {/* Empresa — coluna inteira */}
          <Card className="col-span-2" delay={0}>
            <div className="flex items-start gap-3">
              <Building size={20} className="text-accent mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <h3 className="text-text font-bold text-base truncate">{empresa}</h3>
                <div className="grid grid-cols-3 gap-x-6 gap-y-2 mt-3">
                  {[
                    ['CNPJ', cnpj],
                    ['Cidade', cidade],
                    ['Regime Tributário', regime],
                    ['Versão Sistema', versao],
                    ['PostgreSQL', postgres],
                    ['Último Backup', backup],
                  ].map(([label, value]) => (
                    <div key={label}>
                      <p className="text-text-muted text-[9px] font-semibold uppercase tracking-wider">{label}</p>
                      <p className="text-text-dim text-xs font-mono mt-0.5">{value}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          {/* Módulos */}
          <Card delay={0.05}>
            <SectionTitle icon={Zap} label="Módulos Detectados" />
            {modulos.length > 0 ? (
              <div className="space-y-1.5">
                {modulos.map((m, i) => {
                  const nome = typeof m === 'string' ? m : m.nome
                  const ativo = typeof m === 'object' ? m.ativo : true
                  return (
                    <div key={i} className="flex items-center gap-2">
                      {ativo
                        ? <CheckCircle size={12} className="text-success flex-shrink-0" />
                        : <XCircle size={12} className="text-text-muted flex-shrink-0" />}
                      <span className={['text-xs', ativo ? 'text-text-dim' : 'text-text-muted'].join(' ')}>
                        {nome}
                      </span>
                    </div>
                  )
                })}
              </div>
            ) : (
              <p className="text-text-muted text-xs">Nenhum módulo detectado</p>
            )}
          </Card>

          {/* Volumes */}
          <Card delay={0.1}>
            <SectionTitle icon={Database} label="Top Tabelas por Volume" />
            {volumes.length > 0 ? (
              <div className="space-y-1">
                {volumes.slice(0, 8).map((v, i) => {
                  const nome = v.tabela || v.tablename || '?'
                  const qtd = Number(v.registros || v.n_live_tup || 0).toLocaleString('pt-BR')
                  const max = Number(volumes[0]?.registros || volumes[0]?.n_live_tup || 1)
                  const pct = Math.round((Number(v.registros || v.n_live_tup || 0) / max) * 100)
                  return (
                    <div key={i}>
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="text-[11px] text-text-dim font-mono truncate max-w-[65%]">{nome}</span>
                        <span className="text-[11px] text-text-muted font-mono">{qtd}</span>
                      </div>
                      <div className="h-0.5 bg-surface2 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-accent/50 rounded-full"
                          style={{ width: pct + '%' }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <p className="text-text-muted text-xs">Sem dados de volume</p>
            )}
          </Card>

          {/* Erros recorrentes */}
          {erros.length > 0 && (
            <Card className="col-span-2" delay={0.15}>
              <SectionTitle icon={AlertTriangle} label="Erros Recorrentes" color="text-warning" />
              <div className="flex flex-wrap gap-2">
                {erros.slice(0, 8).map((e, i) => (
                  <span
                    key={i}
                    className="px-2 py-1 bg-error/10 border border-error/20 text-error text-[11px] font-mono rounded-lg truncate max-w-xs selectable"
                  >
                    {typeof e === 'string' ? e : JSON.stringify(e)}
                  </span>
                ))}
              </div>
            </Card>
          )}

          {/* Queries lentas */}
          {lentas.length > 0 && (
            <Card className="col-span-2" delay={0.2}>
              <SectionTitle icon={Clock} label="Queries Lentas (Top 5)" color="text-warning" />
              <div className="overflow-x-auto">
                <table className="w-full text-xs font-mono">
                  <thead>
                    <tr>
                      <th className="text-left text-text-muted pb-2 font-semibold">Query</th>
                      <th className="text-right text-text-muted pb-2 pr-4 font-semibold whitespace-nowrap">Chamadas</th>
                      <th className="text-right text-text-muted pb-2 font-semibold whitespace-nowrap">Média (ms)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {lentas.slice(0, 5).map((q, i) => (
                      <tr key={i} className="border-t border-border/30">
                        <td className="py-1.5 text-text-dim truncate max-w-[400px]">
                          {(q.query || '').slice(0, 90)}{(q.query || '').length > 90 ? '...' : ''}
                        </td>
                        <td className="text-right py-1.5 pr-4 text-text-muted">{q.calls || '—'}</td>
                        <td className="text-right py-1.5 text-warning">
                          {Number(q.mean_exec_time || 0).toFixed(1)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
