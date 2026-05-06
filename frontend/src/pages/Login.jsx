import { useState } from 'react'
import { motion } from 'framer-motion'
import { Loader, AlertCircle } from 'lucide-react'
import api from '../api/backend'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)

  const handleSubmit = async (e) => {
    e?.preventDefault()
    if (!username.trim() || !password) {
      setError('Preencha usuário e senha.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const res = await api.login(username.trim(), password)
      localStorage.setItem('erp_token',    res.data.token)
      localStorage.setItem('erp_username', res.data.username)
      localStorage.setItem('erp_is_admin', res.data.is_admin ? '1' : '0')
      localStorage.setItem('erp_role',     res.data.role || 'analista')
      onLogin({
        token:                res.data.token,
        username:             res.data.username,
        is_admin:             res.data.is_admin,
        role:                 res.data.role || 'analista',
        must_change_password: res.data.must_change_password,
      })
    } catch (err) {
      setError(err.response?.data?.error || 'Falha ao autenticar. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center h-full bg-bg">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-surface rounded-card border border-border w-[400px] overflow-hidden shadow-2xl"
      >
        {/* Cabeçalho */}
        <div className="p-8 pb-6">
          <div className="flex items-center gap-3 mb-7">
            <div className="w-10 h-10 rounded-xl bg-accent/20 border border-accent/30 flex items-center justify-center flex-shrink-0">
              <span className="text-accent font-bold text-lg leading-none">E</span>
            </div>
            <div>
              <h1 className="text-text font-bold text-xl leading-tight">FarmaFacil Assistente</h1>
              <p className="text-text-dim text-sm">Acesse sua conta</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">
                Usuário
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
                disabled={loading}
                className="w-full bg-surface2 border border-border rounded-xl px-3 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors selectable font-mono disabled:opacity-50"
                placeholder="seu usuário"
              />
            </div>

            <div>
              <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">
                Senha
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                className="w-full bg-surface2 border border-border rounded-xl px-3 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors selectable disabled:opacity-50"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className="flex items-start gap-2 text-error text-xs selectable">
                <AlertCircle size={13} className="flex-shrink-0 mt-0.5" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-accent hover:bg-accent-hover text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
            >
              {loading && <Loader size={14} className="animate-spin" />}
              {loading ? 'Verificando...' : 'Entrar'}
            </button>
          </form>
        </div>

        <div className="px-8 py-3 border-t border-border text-center">
          <p className="text-text-muted text-[10px]">FarmaFacil Assistente AI — Prismafive</p>
        </div>
      </motion.div>
    </div>
  )
}
