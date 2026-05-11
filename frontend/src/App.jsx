import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import TitleBar from './components/TitleBar'
import Sidebar from './components/Sidebar'
import StatusBar from './components/StatusBar'
import Setup from './pages/Setup'
import Chat from './pages/Chat'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Users from './pages/Users'
import Gestao from './pages/Gestao'
import AbertosHoje from './pages/AbertosHoje'
import AuditoriaContato from './pages/AuditoriaContato'
import Tarefas from './pages/Tarefas'
import ProvedorNFSe from './pages/ProvedorNFSe'
import Painel from './pages/Painel'
import api from './api/backend'

const PAGE_TRANSITION = { duration: 0.15 }

const ROLE_PAGES = {
  analista:      new Set(['chat', 'tarefas', 'gestao', 'provedor']),
  backservice:   new Set(['chat', 'abertos-hoje', 'tarefas', 'gestao', 'provedor']),
  fiscal:        new Set(['chat', 'abertos-hoje', 'tarefas', 'gestao', 'provedor']),
  lideres:       new Set(['chat', 'gestao', 'abertos-hoje', 'tarefas', 'provedor', 'painel', 'auditoria']),
  administrador: new Set(['chat', 'profile', 'config', 'gestao', 'users', 'abertos-hoje', 'tarefas', 'provedor', 'painel', 'auditoria']),
}

function MustChangePasswordModal({ username, onDone }) {
  const [pwd, setPwd]       = useState('')
  const [pwd2, setPwd2]     = useState('')
  const [error, setError]   = useState('')
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e) => {
    e?.preventDefault()
    if (!pwd || pwd.length < 4) { setError('Senha deve ter ao menos 4 caracteres.'); return }
    if (pwd !== pwd2) { setError('As senhas não coincidem.'); return }
    setSaving(true)
    setError('')
    try {
      await api.changePassword(username, pwd)
      await api.setMustChangePassword(username, false)
      onDone()
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao salvar senha.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-surface rounded-card border border-warning/30 w-[380px] overflow-hidden shadow-2xl"
    >
      <div className="p-6 pb-4 border-b border-border">
        <p className="text-warning font-bold text-base">Troca de senha obrigatória</p>
        <p className="text-text-dim text-sm mt-1">
          O administrador exige que você defina uma nova senha antes de continuar.
        </p>
      </div>
      <form onSubmit={handleSubmit} className="p-6 space-y-4">
        <div>
          <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">Nova senha</label>
          <input
            type="password"
            value={pwd}
            onChange={(e) => setPwd(e.target.value)}
            autoFocus
            className="w-full bg-surface2 border border-border rounded-xl px-3 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors"
            placeholder="••••••••"
          />
        </div>
        <div>
          <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">Confirmar senha</label>
          <input
            type="password"
            value={pwd2}
            onChange={(e) => setPwd2(e.target.value)}
            className="w-full bg-surface2 border border-border rounded-xl px-3 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors"
            placeholder="••••••••"
          />
        </div>
        {error && <p className="text-error text-xs">{error}</p>}
        <button
          type="submit"
          disabled={saving}
          className="w-full py-2.5 bg-accent hover:bg-accent-hover text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {saving ? 'Salvando...' : 'Definir nova senha e continuar'}
        </button>
      </form>
    </motion.div>
  )
}

export default function App() {
  const [page, setPage] = useState('loading') // loading | setup | chat | print | profile | config | users | xml
  const [profile, setProfile] = useState(null)
  const [connected, setConnected] = useState(false)
  const [host, setHost] = useState('')
  const [tokens, setTokens] = useState(0)
  const [backendStatus, setBackendStatus] = useState('waiting') // waiting | ready | error
  const [backendErrMsg, setBackendErrMsg] = useState('')
  const [session, setSession] = useState(null) // { token, username, is_admin, role }
  const [mustChangePwd, setMustChangePwd] = useState(false)
  const [chatInitContext, setChatInitContext] = useState(null) // mensagens vindas de análise
  const [tvMode, setTvMode] = useState(localStorage.getItem('erp_tv_mode') === '1')

  // ── Inicialização ──────────────────────────────────────────────────────────

  useEffect(() => {
    if (!window.electron) {
      setBackendStatus('ready')
      return
    }

    const onReady = () => setBackendStatus('ready')
    const onError = (msg) => {
      setBackendStatus('error')
      setBackendErrMsg(msg)
    }

    window.electron.onBackendReady(onReady)
    window.electron.onBackendError(onError)

    return () => {
      window.electron.removeListener('backend-ready')
      window.electron.removeListener('backend-error')
    }
  }, [])

  // Após backend pronto, verifica sessão
  useEffect(() => {
    if (backendStatus !== 'ready') return
    checkSession()
  }, [backendStatus])

  // Atalho Ctrl+Shift+P via Electron
  useEffect(() => {
    if (!window.electron) return
    const handler = () => setPage('print')
    window.electron.onCaptureShortcut(handler)
    return () => window.electron.removeListener('capture-shortcut')
  }, [])

  const checkSession = async () => {
    // TV auto-login: detecta ?tv=CHAVE na URL
    const params = new URLSearchParams(window.location.search)
    const tvKey  = params.get('tv')
    if (tvKey) {
      try {
        const { data } = await api.tvLogin(tvKey)
        localStorage.setItem('erp_token',   data.token)
        localStorage.setItem('erp_username', data.username)
        localStorage.setItem('erp_is_admin', '0')
        localStorage.setItem('erp_role',     data.role)
        localStorage.setItem('erp_tv_mode',  '1')
        window.history.replaceState({}, '', window.location.pathname)
        setSession({ token: data.token, username: data.username, is_admin: false, role: data.role })
        setTvMode(true)
        setPage('painel')
        return
      } catch { /* chave inválida — cai no fluxo normal */ }
    }

    const token    = localStorage.getItem('erp_token')
    const username = localStorage.getItem('erp_username')
    const is_admin = localStorage.getItem('erp_is_admin') === '1'
    const role     = localStorage.getItem('erp_role') || 'analista'
    const isTv     = localStorage.getItem('erp_tv_mode') === '1'

    if (!token || !username) {
      setPage('login')
      return
    }

    // Valida token com o backend
    try {
      const me = await api.me()
      const updatedRole = me.data?.role || role
      localStorage.setItem('erp_role', updatedRole)
      setSession({ token, username, is_admin, role: updatedRole })
      if (isTv) {
        setPage('painel')
      } else {
        tryAutoConnect()
      }
    } catch {
      // Token expirado ou inválido
      localStorage.removeItem('erp_token')
      localStorage.removeItem('erp_username')
      localStorage.removeItem('erp_is_admin')
      localStorage.removeItem('erp_role')
      localStorage.removeItem('erp_tv_mode')
      setTvMode(false)
      setPage('login')
    }
  }

  const tryAutoConnect = async () => {
    const savedHost = localStorage.getItem('erp_host')
    const savedDb   = localStorage.getItem('erp_dbname')

    if (!savedHost || !savedDb) {
      setPage('chat')
      return
    }

    try {
      const res = await api.perfil()
      const p   = res.data
      if (p && Object.keys(p).length > 0) {
        setProfile(p)
        setConnected(true)
        setHost(savedHost)
        setPage('chat')
        return
      }
    } catch {}

    // Perfil vazio — reconecta
    try {
      await api.connect(savedHost, savedDb)
      setHost(savedHost)
      setConnected(true)
      setPage('chat')
      pollProfile()
    } catch {
      setPage('setup')
    }
  }

  const pollProfile = () => {
    let tries = 0
    const poll = setInterval(async () => {
      tries++
      try {
        const { data } = await api.scanStatus()
        if (data.done && !data.error) {
          clearInterval(poll)
          const pRes = await api.perfil()
          if (pRes.data) setProfile(pRes.data)
        }
      } catch {}
      if (tries > 60) clearInterval(poll)
    }, 500)
  }

  // ── Callbacks ──────────────────────────────────────────────────────────────

  const handleLogin = useCallback((sess) => {
    setSession(sess)
    if (sess.must_change_password) {
      setMustChangePwd(true)
    } else {
      tryAutoConnect()
    }
  }, [])

  const handleLogout = useCallback(async () => {
    try { await api.logout() } catch {}
    localStorage.removeItem('erp_token')
    localStorage.removeItem('erp_username')
    localStorage.removeItem('erp_is_admin')
    localStorage.removeItem('erp_role')
    setSession(null)
    setConnected(false)
    setProfile(null)
    setHost('')
    setPage('login')
  }, [])

  const handleConnected = useCallback(async ({ host: h }) => {
    setHost(h)
    setConnected(true)
    setPage('chat')
    pollProfile()
    try {
      const res = await api.perfil()
      if (res.data && Object.keys(res.data).length > 0) setProfile(res.data)
    } catch {}
  }, [])

  const canAccess = useCallback((p) => {
    const role = session?.role || 'analista'
    return ROLE_PAGES[role]?.has(p) ?? false
  }, [session])

  const handleNavigate = useCallback((p) => {
    if (canAccess(p)) setPage(p)
  }, [canAccess])
  const handleTokensUpdate = useCallback((t) => setTokens(t), [])
  const handleSendToChat = useCallback((contextMessages) => {
    setChatInitContext(contextMessages)
    setPage('chat')
  }, [])

  // ── Render helpers ─────────────────────────────────────────────────────────

  const empresa = profile?.razao_social || profile?.empresa || ''
  const versao  = profile?.versao_sistema || ''

  if (backendStatus === 'waiting') {
    return (
      <div className="flex flex-col h-screen bg-bg overflow-hidden">
        <TitleBar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center space-y-5">
            <div className="w-14 h-14 rounded-2xl bg-accent/20 border border-accent/30 flex items-center justify-center mx-auto">
              <span className="text-accent font-bold text-2xl">E</span>
            </div>
            <div>
              <h2 className="text-text font-semibold text-lg">FarmaFacil Assistente</h2>
              <p className="text-text-dim text-sm mt-1">Inicializando backend...</p>
            </div>
            <div className="flex justify-center">
              <div className="w-40 h-1 bg-surface2 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-accent rounded-full w-1/3"
                  animate={{ x: ['0%', '200%', '0%'] }}
                  transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (backendStatus === 'error') {
    return (
      <div className="flex flex-col h-screen bg-bg overflow-hidden">
        <TitleBar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center space-y-3 max-w-sm px-4">
            <p className="text-error font-semibold text-lg">Backend não iniciou</p>
            <p className="text-text-dim text-sm">{backendErrMsg}</p>
            <p className="text-text-muted text-xs">
              Verifique se o Python está instalado e as dependências estão configuradas.
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Tela de login
  if (page === 'login' || !session) {
    return (
      <div className="flex flex-col h-screen bg-bg overflow-hidden">
        <TitleBar />
        <div className="flex-1 overflow-hidden">
          <Login onLogin={handleLogin} />
        </div>
      </div>
    )
  }

  // Troca de senha obrigatória
  if (mustChangePwd) {
    return (
      <div className="flex flex-col h-screen bg-bg overflow-hidden">
        <TitleBar />
        <div className="flex-1 flex items-center justify-center">
          <MustChangePasswordModal
            username={session.username}
            onDone={() => { setMustChangePwd(false); tryAutoConnect() }}
          />
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-bg overflow-hidden">
      <TitleBar />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar — oculta no setup e no modo TV */}
        {page !== 'setup' && !tvMode && (
          <Sidebar
            active={page}
            onNavigate={handleNavigate}
            onLogout={handleLogout}
            host={host}
            connected={connected}
            isAdmin={session?.is_admin}
            role={session?.role || 'analista'}
            username={session?.username}
          />
        )}

        {/* Conteúdo principal */}
        <main className="flex-1 overflow-hidden relative">
          <AnimatePresence mode="wait">
            {page === 'setup' && (
              <motion.div key="setup" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Setup onConnected={handleConnected} />
              </motion.div>
            )}
            {page === 'chat' && (
              <motion.div key="chat" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Chat
                  profile={profile}
                  onTokensUpdate={handleTokensUpdate}
                  initContext={chatInitContext}
                  onContextConsumed={() => setChatInitContext(null)}
                />
              </motion.div>
            )}
            {page === 'profile' && (
              <motion.div key="profile" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Profile profile={profile} />
              </motion.div>
            )}
            {page === 'config' && (
              <motion.div key="config" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Setup onConnected={handleConnected} />
              </motion.div>
            )}
            {page === 'users' && canAccess('users') && (
              <motion.div key="users" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Users currentUser={session} />
              </motion.div>
            )}
            {page === 'gestao' && canAccess('gestao') && (
              <motion.div key="gestao" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Gestao role={session?.role || 'analista'} />
              </motion.div>
            )}
            {page === 'abertos-hoje' && canAccess('abertos-hoje') && (
              <motion.div key="abertos-hoje" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <AbertosHoje />
              </motion.div>
            )}
            {page === 'tarefas' && canAccess('tarefas') && (
              <motion.div key="tarefas" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Tarefas onSendToChat={handleSendToChat} />
              </motion.div>
            )}
            {page === 'provedor' && canAccess('provedor') && (
              <motion.div key="provedor" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <ProvedorNFSe onSendToChat={handleSendToChat} />
              </motion.div>
            )}
            {page === 'auditoria' && canAccess('auditoria') && (
              <motion.div key="auditoria" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <AuditoriaContato />
              </motion.div>
            )}
            {page === 'painel' && canAccess('painel') && (
              <motion.div key="painel" className="absolute inset-0"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                transition={PAGE_TRANSITION}>
                <Painel />
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>

      {!tvMode && (
        <StatusBar
          connected={connected}
          empresa={empresa}
          versao={versao}
          tokens={tokens}
        />
      )}
    </div>
  )
}
