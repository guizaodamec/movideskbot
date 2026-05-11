import { useState, useEffect, useMemo } from 'react'
import { RefreshCw, Search, X, PackageCheck } from 'lucide-react'
import api from '../api/backend'

function badge(versao, versaoAtual, versoesList) {
  if (!versao || !versaoAtual) return 'bg-surface2 text-text-dim'
  const idx = versoesList.indexOf(versao)
  const idxAtual = versoesList.indexOf(versaoAtual)
  const atraso = idx - idxAtual   // positivo = mais antigo
  if (atraso === 0)  return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
  if (atraso <= 2)   return 'bg-yellow-500/15  text-yellow-400  border border-yellow-500/30'
  if (atraso <= 5)   return 'bg-orange-500/15  text-orange-400  border border-orange-500/30'
  return                    'bg-red-500/15     text-red-400     border border-red-500/30'
}

function StatCard({ label, value, sub, color = 'text-text' }) {
  return (
    <div className="bg-surface rounded-xl border border-border p-4 flex flex-col gap-1">
      <p className="text-text-dim text-xs uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
      {sub && <p className="text-text-muted text-xs">{sub}</p>}
    </div>
  )
}

export default function VersaoClientes() {
  const [data, setData]         = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [busca, setBusca]       = useState('')
  const [versaoFiltro, setVersaoFiltro] = useState('')
  const [updatedAt, setUpdatedAt] = useState('')

  const load = async (forcar = false) => {
    setLoading(true)
    setError('')
    try {
      if (forcar) await api.versoesClientesAtualizar()
      const { data: d } = await api.versoesClientes()
      setData(d)
      setUpdatedAt(d.updated_at || '')
    } catch (e) {
      setError(e.response?.data?.error || 'Erro ao carregar dados.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const versoesList = useMemo(
    () => (data?.distribuicao || []).map(d => d.versao),
    [data]
  )

  const clientesFiltrados = useMemo(() => {
    if (!data?.clientes) return []
    const q = busca.toLowerCase().trim()
    return data.clientes.filter(c => {
      const matchBusca = !q || c.nome.toLowerCase().includes(q) ||
        c.cidade.toLowerCase().includes(q) || c.estado.toLowerCase().includes(q)
      const matchVersao = !versaoFiltro || c.versao === versaoFiltro
      return matchBusca && matchVersao
    })
  }, [data, busca, versaoFiltro])

  const desatualizados = useMemo(() => {
    if (!data) return 0
    return data.clientes.filter(c => c.versao !== data.versao_atual).length
  }, [data])

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center h-full text-text-dim text-sm">
        <RefreshCw size={16} className="animate-spin mr-2" />
        Carregando versões...
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center space-y-3">
          <p className="text-error font-semibold">{error}</p>
          <button onClick={() => load()} className="text-accent text-sm hover:underline">Tentar novamente</button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-bg overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-border flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
          <PackageCheck size={20} className="text-accent" />
          <div>
            <h1 className="text-text font-semibold text-base">Versões de Clientes</h1>
            <p className="text-text-dim text-xs">
              Versão atual: <span className="text-emerald-400 font-mono font-semibold">{data?.versao_atual}</span>
              {updatedAt && <span className="ml-2 text-text-muted">· atualizado às {updatedAt}</span>}
            </p>
          </div>
        </div>
        <button
          onClick={() => load(true)}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface border border-border text-text-dim hover:text-text text-xs transition-colors disabled:opacity-50"
        >
          <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
          Atualizar
        </button>
      </div>

      {/* Stat cards */}
      <div className="px-6 py-4 grid grid-cols-3 gap-3 flex-shrink-0">
        <StatCard
          label="Clientes monitorados"
          value={data?.total_clientes ?? 0}
        />
        <StatCard
          label="Na versão atual"
          value={data?.na_versao_atual ?? 0}
          sub={`${Math.round((data?.na_versao_atual / data?.total_clientes) * 100) || 0}% do total`}
          color="text-emerald-400"
        />
        <StatCard
          label="Desatualizados"
          value={desatualizados}
          sub="alguma versão anterior"
          color={desatualizados > 0 ? 'text-orange-400' : 'text-emerald-400'}
        />
      </div>

      {/* Filtros */}
      <div className="px-6 pb-3 flex gap-3 flex-shrink-0 flex-wrap">
        <div className="relative flex-1 min-w-[200px]">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            value={busca}
            onChange={e => setBusca(e.target.value)}
            placeholder="Buscar cliente, cidade ou estado..."
            className="w-full pl-8 pr-8 py-2 bg-surface border border-border rounded-xl text-sm text-text placeholder-text-muted outline-none focus:border-accent transition-colors"
          />
          {busca && (
            <button onClick={() => setBusca('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text">
              <X size={13} />
            </button>
          )}
        </div>

        <select
          value={versaoFiltro}
          onChange={e => setVersaoFiltro(e.target.value)}
          className="px-3 py-2 bg-surface border border-border rounded-xl text-sm text-text outline-none focus:border-accent transition-colors"
        >
          <option value="">Todas as versões</option>
          {(data?.distribuicao || []).map(d => (
            <option key={d.versao} value={d.versao}>
              {d.versao} ({d.total})
            </option>
          ))}
        </select>

        {(busca || versaoFiltro) && (
          <button
            onClick={() => { setBusca(''); setVersaoFiltro('') }}
            className="px-3 py-2 rounded-xl border border-border text-text-dim text-sm hover:text-text hover:bg-surface transition-colors"
          >
            Limpar
          </button>
        )}
      </div>

      {/* Contador */}
      <div className="px-6 pb-2 flex-shrink-0">
        <p className="text-text-muted text-xs">
          {clientesFiltrados.length} cliente{clientesFiltrados.length !== 1 ? 's' : ''}
          {(busca || versaoFiltro) && ` de ${data?.total_clientes}`}
        </p>
      </div>

      {/* Tabela */}
      <div className="flex-1 overflow-auto px-6 pb-6">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="border-b border-border text-left">
              <th className="pb-2 pr-4 text-text-muted text-xs uppercase tracking-wider font-medium w-8">#</th>
              <th className="pb-2 pr-4 text-text-muted text-xs uppercase tracking-wider font-medium">Cliente</th>
              <th className="pb-2 pr-4 text-text-muted text-xs uppercase tracking-wider font-medium">Cidade / Estado</th>
              <th className="pb-2 pr-4 text-text-muted text-xs uppercase tracking-wider font-medium">Versão</th>
              <th className="pb-2 text-text-muted text-xs uppercase tracking-wider font-medium">Última atualização</th>
            </tr>
          </thead>
          <tbody>
            {clientesFiltrados.map((c, i) => {
              const cls = badge(c.versao, data?.versao_atual, versoesList)
              const dt  = c.ultima_atualizacao
                ? new Date(c.ultima_atualizacao).toLocaleDateString('pt-BR')
                : '—'
              return (
                <tr key={c.id + '-' + i} className="border-b border-border/40 hover:bg-surface/50 transition-colors">
                  <td className="py-2.5 pr-4 text-text-muted text-xs">{i + 1}</td>
                  <td className="py-2.5 pr-4 text-text font-medium selectable">{c.nome}</td>
                  <td className="py-2.5 pr-4 text-text-dim text-xs selectable">
                    {c.cidade && c.estado ? `${c.cidade} · ${c.estado}` : c.cidade || c.estado || '—'}
                  </td>
                  <td className="py-2.5 pr-4">
                    <span className={`inline-block px-2 py-0.5 rounded-md font-mono text-xs ${cls}`}>
                      {c.versao || '—'}
                    </span>
                  </td>
                  <td className="py-2.5 text-text-dim text-xs selectable">{dt}</td>
                </tr>
              )
            })}
            {clientesFiltrados.length === 0 && (
              <tr>
                <td colSpan={5} className="py-8 text-center text-text-muted text-sm">
                  Nenhum cliente encontrado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
