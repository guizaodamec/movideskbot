import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Server, Database, CheckCircle, AlertCircle, Loader, ChevronDown } from 'lucide-react'
import api from '../api/backend'

export default function Setup({ onConnected }) {
  const [host, setHost] = useState(localStorage.getItem('erp_host') || '')
  const [dbname, setDbname] = useState(localStorage.getItem('erp_dbname') || '')
  const [databases, setDatabases] = useState([])
  const [showDbList, setShowDbList] = useState(false)

  useEffect(() => {
    api.databases().then(res => setDatabases(res.data)).catch(() => {})
  }, [])

  const selectDb = (db) => {
    setHost(db.host + ':' + db.port)
    setDbname(db.dbname)
    setShowDbList(false)
  }
  const [status, setStatus] = useState('idle') // idle | connecting | scanning | done | error
  const [progress, setProgress] = useState(0)
  const [statusMsg, setStatusMsg] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const pollRef = useRef(null)

  // Limpa polling ao desmontar
  useEffect(() => () => clearInterval(pollRef.current), [])

  const handleConnect = async () => {
    const h = host.trim()
    const d = dbname.trim()
    if (!h || !d) {
      setErrorMsg('Preencha o IP e o nome do banco de dados.')
      return
    }

    setStatus('connecting')
    setErrorMsg('')
    setStatusMsg('Conectando...')
    setProgress(10)

    try {
      await api.connect(h, d)
      localStorage.setItem('erp_host', h)
      localStorage.setItem('erp_dbname', d)
      setStatus('scanning')
      setStatusMsg('Escaneando banco de dados...')
      setProgress(30)
      startPolling(h, d)
    } catch (err) {
      setStatus('error')
      const msg = err.response?.data?.error || err.message || 'Falha desconhecida'
      setErrorMsg('Falha na conexão: ' + msg)
    }
  }

  const startPolling = (h, d) => {
    pollRef.current = setInterval(async () => {
      try {
        const res = await api.scanStatus()
        const { pct, msg, done, error } = res.data
        if (pct) setProgress(Math.min(pct, 99))
        if (msg) setStatusMsg(msg)

        if (done && !error) {
          clearInterval(pollRef.current)
          setProgress(100)
          setStatus('done')
          setTimeout(() => onConnected({ host: h, dbname: d }), 700)
        } else if (error) {
          clearInterval(pollRef.current)
          setStatus('error')
          setErrorMsg('Erro no scan: ' + error)
        }
      } catch {
        // ignora erros pontuais de polling
      }
    }, 500)
  }

  const isLoading = status === 'connecting' || status === 'scanning'

  return (
    <div className="flex items-center justify-center h-full bg-bg">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-surface rounded-card border border-border w-[460px] overflow-hidden shadow-2xl"
      >
        {/* Cabeçalho */}
        <div className="p-8 pb-0">
          <div className="flex items-center gap-3 mb-7">
            <div className="w-10 h-10 rounded-xl bg-accent/20 border border-accent/30 flex items-center justify-center flex-shrink-0">
              <span className="text-accent font-bold text-lg leading-none">E</span>
            </div>
            <div>
              <h1 className="text-text font-bold text-xl leading-tight">FarmaFacil Assistente</h1>
              <p className="text-text-dim text-sm">Configuração de conexão</p>
            </div>
          </div>

          {/* Atalhos pré-configurados */}
          {databases.length > 0 && (
            <div className="mb-5">
              <button
                onClick={() => setShowDbList(!showDbList)}
                className="w-full flex items-center justify-between px-3 py-2 bg-surface2 border border-border rounded-xl text-text-dim text-xs hover:border-accent transition-colors"
              >
                <span>Selecionar banco pré-configurado</span>
                <ChevronDown size={13} className={showDbList ? 'rotate-180 transition-transform' : 'transition-transform'} />
              </button>
              <AnimatePresence>
                {showDbList && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden mt-1 border border-border rounded-xl bg-surface2"
                  >
                    {databases.map((db, i) => (
                      <button
                        key={i}
                        onClick={() => selectDb(db)}
                        className="w-full text-left px-3 py-2 text-xs hover:bg-border transition-colors border-b border-border/40 last:border-0"
                      >
                        <span className="text-text font-medium">{db.label}</span>
                        <span className="text-text-muted font-mono ml-2">{db.host}/{db.dbname}</span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}

          <div className="space-y-4">
            {/* Campo IP */}
            <div>
              <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">
                IP ou Hostname do servidor
              </label>
              <div className="flex items-center gap-2 bg-surface2 border border-border rounded-xl px-3 py-2.5 focus-within:border-accent transition-colors">
                <Server size={15} className="text-text-dim flex-shrink-0" />
                <input
                  type="text"
                  value={host}
                  onChange={(e) => setHost(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleConnect()}
                  placeholder="192.168.1.10 ou nome-do-servidor"
                  disabled={isLoading || status === 'done'}
                  className="bg-transparent text-text text-sm outline-none w-full font-mono placeholder:text-text-muted selectable"
                />
              </div>
            </div>

            {/* Campo banco */}
            <div>
              <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">
                Nome do banco de dados
              </label>
              <div className="flex items-center gap-2 bg-surface2 border border-border rounded-xl px-3 py-2.5 focus-within:border-accent transition-colors">
                <Database size={15} className="text-text-dim flex-shrink-0" />
                <input
                  type="text"
                  value={dbname}
                  onChange={(e) => setDbname(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleConnect()}
                  placeholder="farmafacil"
                  disabled={isLoading || status === 'done'}
                  className="bg-transparent text-text text-sm outline-none w-full font-mono placeholder:text-text-muted selectable"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Área de ação */}
        <div className="px-8 py-6 space-y-4">
          {/* Barra de progresso */}
          <AnimatePresence>
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="space-y-2 overflow-hidden"
              >
                <div className="h-1.5 bg-surface2 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-accent rounded-full"
                    animate={{ width: progress + '%' }}
                    transition={{ duration: 0.4 }}
                  />
                </div>
                <p className="text-text-dim text-xs font-mono">{statusMsg}</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Sucesso */}
          {status === 'done' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 text-success text-sm"
            >
              <CheckCircle size={16} />
              <span>Conectado com sucesso!</span>
            </motion.div>
          )}

          {/* Erro */}
          {errorMsg && (
            <div className="flex items-start gap-2 text-error text-sm selectable">
              <AlertCircle size={16} className="flex-shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Botão */}
          <button
            onClick={handleConnect}
            disabled={isLoading || status === 'done'}
            className="w-full py-3 bg-accent hover:bg-accent-hover text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {isLoading && <Loader size={15} className="animate-spin" />}
            {isLoading ? statusMsg || 'Conectando...' : 'Conectar e escanear banco'}
          </button>

          <p className="text-[10px] text-text-muted text-center">
            Credenciais de acesso ao banco são configuradas pelo administrador
          </p>
        </div>
      </motion.div>
    </div>
  )
}
