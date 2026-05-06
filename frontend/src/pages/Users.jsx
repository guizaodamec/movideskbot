import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Plus, Trash2, Key, Loader, RefreshCw, Shield, Link } from 'lucide-react'
import api from '../api/backend'

const ROLES = [
  { key: 'analista',      label: 'Analista',      desc: 'Chat apenas',          color: 'text-text-dim border-border bg-surface2' },
  { key: 'backservice',   label: 'Backservice',   desc: 'Chat + Log',           color: 'text-blue-400 border-blue-400/30 bg-blue-400/10' },
  { key: 'fiscal',        label: 'Fiscal',        desc: 'Chat + XML',           color: 'text-purple-400 border-purple-400/30 bg-purple-400/10' },
  { key: 'lideres',       label: 'Líderes',       desc: 'Chat + Log + Gestão',  color: 'text-warning border-warning/30 bg-warning/10' },
  { key: 'administrador', label: 'Administrador', desc: 'Acesso completo',      color: 'text-accent border-accent/20 bg-accent/10' },
]

function RoleBadge({ role }) {
  const r = ROLES.find(x => x.key === role) || ROLES[0]
  return (
    <span className={`px-2 py-0.5 text-[10px] font-semibold rounded-md border ${r.color}`}>
      {r.label}
    </span>
  )
}

function RoleSelect({ value, onChange }) {
  return (
    <select
      value={value}
      onChange={e => onChange(e.target.value)}
      className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
    >
      {ROLES.map(r => (
        <option key={r.key} value={r.key}>{r.label} — {r.desc}</option>
      ))}
    </select>
  )
}

export default function Users({ currentUser }) {
  const [users, setUsers]               = useState([])
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState('')
  const [showForm, setShowForm]         = useState(false)
  const [form, setForm]                 = useState({ username: '', password: '', role: 'analista', must_change_password: false, movidesk_name: '' })
  const [mvModal, setMvModal]           = useState(null)
  const [mvName,  setMvName]            = useState('')
  const [mvAnalistas, setMvAnalistas]   = useState([])
  const [formErr, setFormErr]           = useState('')
  const [saving, setSaving]             = useState(false)
  const [pwdModal, setPwdModal]         = useState(null)
  const [newPwd, setNewPwd]             = useState('')
  const [roleModal, setRoleModal]       = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const res = await api.users()
      setUsers(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Erro ao carregar usuários')
    } finally {
      setLoading(false)
    }
  }

  const loadMvAnalistas = async () => {
    try {
      const res = await api.movideskAnalistas()
      setMvAnalistas(Array.isArray(res.data) ? res.data : [])
    } catch {
      setMvAnalistas([])
    }
  }

  useEffect(() => { load(); loadMvAnalistas() }, [])

  const handleSaveMvName = async (e) => {
    e?.preventDefault()
    try { await api.setMovideskName(mvModal.username, mvName); setMvModal(null); await load() }
    catch (e) { alert(e.response?.data?.error || 'Erro') }
  }

  const handleCreate = async (e) => {
    e?.preventDefault()
    if (!form.username.trim() || !form.password) { setFormErr('Preencha todos os campos.'); return }
    setSaving(true)
    setFormErr('')
    try {
      await api.createUser(
        form.username.trim(), form.password,
        form.role === 'administrador',
        form.must_change_password,
        form.role
      )
      if (form.movidesk_name.trim()) {
        await api.setMovideskName(form.username.trim().toUpperCase(), form.movidesk_name.trim())
      }
      setForm({ username: '', password: '', role: 'analista', must_change_password: false, movidesk_name: '' })
      setShowForm(false)
      await load()
    } catch (e) {
      setFormErr(e.response?.data?.error || 'Erro ao criar usuário')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (username) => {
    if (!window.confirm('Remover usuário ' + username + '?')) return
    try { await api.deleteUser(username); await load() }
    catch (e) { alert(e.response?.data?.error || 'Erro ao remover') }
  }

  const handleChangePwd = async (e) => {
    e?.preventDefault()
    if (!newPwd) return
    try { await api.changePassword(pwdModal.username, newPwd); setPwdModal(null); setNewPwd('') }
    catch (e) { alert(e.response?.data?.error || 'Erro ao alterar senha') }
  }

  const handleSetRole = async (username, role) => {
    try { await api.setRole(username, role); setRoleModal(null); await load() }
    catch (e) { alert(e.response?.data?.error || 'Erro ao alterar perfil') }
  }

  const handleToggleMustChange = async (u) => {
    try { await api.setMustChangePassword(u.username, !u.must_change_password); await load() }
    catch (e) { alert(e.response?.data?.error || 'Erro') }
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex items-center justify-between flex-shrink-0">
        <div>
          <h2 className="text-text font-semibold text-sm">Usuários</h2>
          <p className="text-text-dim text-xs mt-0.5">Gerenciamento de acesso — somente administrador</p>
        </div>
        <button
          onClick={() => { setShowForm(!showForm); setFormErr('') }}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-accent hover:bg-accent-hover text-white rounded-lg text-xs font-medium transition-colors"
        >
          <Plus size={13} /> Novo usuário
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {/* Formulário de criação */}
        {showForm && (
          <motion.form
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            onSubmit={handleCreate}
            className="bg-surface border border-accent/20 rounded-card p-4 space-y-3"
          >
            <p className="text-text text-sm font-semibold">Novo usuário</p>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-text-dim text-[10px] uppercase tracking-wider mb-1.5">Usuário</label>
                <input
                  type="text"
                  value={form.username}
                  onChange={e => setForm({ ...form, username: e.target.value })}
                  className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent font-mono"
                  placeholder="nome_usuario"
                />
              </div>
              <div>
                <label className="block text-text-dim text-[10px] uppercase tracking-wider mb-1.5">Senha</label>
                <input
                  type="password"
                  value={form.password}
                  onChange={e => setForm({ ...form, password: e.target.value })}
                  className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
                  placeholder="••••••••"
                />
              </div>
            </div>
            <div>
              <label className="block text-text-dim text-[10px] uppercase tracking-wider mb-1.5">Perfil de acesso</label>
              <RoleSelect value={form.role} onChange={v => setForm({ ...form, role: v })} />
            </div>
            <div>
              <label className="block text-text-dim text-[10px] uppercase tracking-wider mb-1.5">
                Nome no Movidesk <span className="normal-case font-normal">(para fila do analista)</span>
              </label>
              {mvAnalistas.length > 0 ? (
                <select
                  value={form.movidesk_name}
                  onChange={e => setForm({ ...form, movidesk_name: e.target.value })}
                  className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
                >
                  <option value="">— Sem vínculo —</option>
                  {mvAnalistas.map(n => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="text"
                  value={form.movidesk_name}
                  onChange={e => setForm({ ...form, movidesk_name: e.target.value })}
                  className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
                  placeholder='Ex: "Alan vieira" (como aparece no Movidesk)'
                />
              )}
            </div>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={form.must_change_password}
                onChange={e => setForm({ ...form, must_change_password: e.target.checked })}
                className="accent-accent"
              />
              <span className="text-text-dim text-sm">Obrigar troca de senha no primeiro login</span>
            </label>
            {formErr && <p className="text-error text-xs">{formErr}</p>}
            <div className="flex gap-2 justify-end">
              <button type="button" onClick={() => setShowForm(false)}
                className="px-4 py-2 text-xs text-text-dim bg-surface2 hover:bg-border rounded-lg">
                Cancelar
              </button>
              <button type="submit" disabled={saving}
                className="px-4 py-2 text-xs text-white bg-accent hover:bg-accent-hover rounded-lg font-semibold disabled:opacity-50 flex items-center gap-1.5">
                {saving && <Loader size={12} className="animate-spin" />} Criar
              </button>
            </div>
          </motion.form>
        )}

        {loading ? (
          <div className="flex items-center justify-center h-32 text-text-dim text-sm gap-2">
            <Loader size={15} className="animate-spin" /> Carregando...
          </div>
        ) : error ? (
          <p className="text-error text-sm">{error}</p>
        ) : (
          <div className="space-y-2">
            {users.map(u => (
              <div key={u.username}
                className="bg-surface border border-border rounded-xl px-4 py-3 flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center flex-shrink-0">
                    <span className="text-accent text-xs font-bold">{u.username[0]}</span>
                  </div>
                  <div className="min-w-0">
                    <p className="text-text text-sm font-medium font-mono truncate">{u.username}</p>
                    <p className="text-text-muted text-[10px] mt-0.5">
                      {u.created_at?.slice(0, 10) || ''}
                      {u.movidesk_name && <span className="ml-2 text-accent/70">↔ {u.movidesk_name}</span>}
                    </p>
                  </div>
                  <RoleBadge role={u.role} />
                  {u.must_change_password && (
                    <span className="px-1.5 py-0.5 bg-warning/15 text-warning text-[10px] font-semibold rounded-md border border-warning/20 whitespace-nowrap">
                      Troca obrigatória
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1 flex-shrink-0">
                  {/* Nome no Movidesk */}
                  <button
                    onClick={() => { setMvModal(u); setMvName(u.movidesk_name || '') }}
                    className="p-1.5 text-text-dim hover:text-accent hover:bg-surface2 rounded-lg transition-colors"
                    title="Nome no Movidesk (para fila do analista)"
                  >
                    <Link size={14} />
                  </button>
                  {/* Alterar perfil */}
                  {u.username !== currentUser?.username && (
                    <button
                      onClick={() => setRoleModal(u)}
                      className="p-1.5 text-text-dim hover:text-accent hover:bg-surface2 rounded-lg transition-colors"
                      title="Alterar perfil de acesso"
                    >
                      <Shield size={14} />
                    </button>
                  )}
                  {/* Forçar troca de senha */}
                  {u.username !== currentUser?.username && (
                    <button
                      onClick={() => handleToggleMustChange(u)}
                      className={`p-1.5 rounded-lg transition-colors ${u.must_change_password ? 'text-warning hover:text-text hover:bg-surface2' : 'text-text-dim hover:text-warning hover:bg-surface2'}`}
                      title={u.must_change_password ? 'Remover obrigação de troca' : 'Obrigar troca de senha'}
                    >
                      <RefreshCw size={14} />
                    </button>
                  )}
                  {/* Trocar senha */}
                  <button
                    onClick={() => { setPwdModal(u); setNewPwd('') }}
                    className="p-1.5 text-text-dim hover:text-text hover:bg-surface2 rounded-lg transition-colors"
                    title="Alterar senha"
                  >
                    <Key size={14} />
                  </button>
                  {/* Deletar */}
                  {u.username !== currentUser?.username && (
                    <button
                      onClick={() => handleDelete(u.username)}
                      className="p-1.5 text-text-dim hover:text-error hover:bg-surface2 rounded-lg transition-colors"
                      title="Remover usuário"
                    >
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal trocar senha */}
      {pwdModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" onClick={() => setPwdModal(null)} />
          <motion.form
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            onSubmit={handleChangePwd}
            className="relative z-10 bg-surface border border-border rounded-card p-5 w-80 space-y-4"
          >
            <p className="text-text font-semibold text-sm">Nova senha — {pwdModal.username}</p>
            <input
              type="password"
              value={newPwd}
              onChange={e => setNewPwd(e.target.value)}
              autoFocus
              className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
              placeholder="Nova senha"
            />
            <div className="flex gap-2 justify-end">
              <button type="button" onClick={() => setPwdModal(null)}
                className="px-4 py-2 text-xs text-text-dim bg-surface2 hover:bg-border rounded-lg">Cancelar</button>
              <button type="submit"
                className="px-4 py-2 text-xs text-white bg-accent hover:bg-accent-hover rounded-lg font-semibold">Salvar</button>
            </div>
          </motion.form>
        </div>
      )}

      {/* Modal nome no Movidesk */}
      {mvModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" onClick={() => setMvModal(null)} />
          <motion.form
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            onSubmit={handleSaveMvName}
            className="relative z-10 bg-surface border border-border rounded-card p-5 w-96 space-y-4"
          >
            <div>
              <p className="text-text font-semibold text-sm">Nome no Movidesk — {mvModal.username}</p>
              <p className="text-text-dim text-xs mt-1">
                Selecione o analista do Movidesk para vincular à fila do painel.
              </p>
            </div>
            {mvAnalistas.length > 0 ? (
              <select
                value={mvName}
                onChange={e => setMvName(e.target.value)}
                autoFocus
                className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
              >
                <option value="">— Sem vínculo —</option>
                {mvAnalistas.map(n => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={mvName}
                onChange={e => setMvName(e.target.value)}
                autoFocus
                className="w-full bg-surface2 border border-border rounded-lg px-3 py-2 text-text text-sm outline-none focus:border-accent"
                placeholder='Ex: "Alan vieira" (como aparece no Movidesk)'
              />
            )}
            {mvName && <p className="text-accent text-xs">Selecionado: <strong>{mvName}</strong></p>}
            <div className="flex gap-2 justify-end">
              <button type="button" onClick={() => setMvModal(null)}
                className="px-4 py-2 text-xs text-text-dim bg-surface2 hover:bg-border rounded-lg">Cancelar</button>
              <button type="submit"
                className="px-4 py-2 text-xs text-white bg-accent hover:bg-accent-hover rounded-lg font-semibold">Salvar</button>
            </div>
          </motion.form>
        </div>
      )}

      {/* Modal alterar perfil */}
      {roleModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" onClick={() => setRoleModal(null)} />
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative z-10 bg-surface border border-border rounded-card p-5 w-96 space-y-4"
          >
            <p className="text-text font-semibold text-sm">Perfil de acesso — {roleModal.username}</p>
            <div className="space-y-2">
              {ROLES.map(r => (
                <button
                  key={r.key}
                  onClick={() => handleSetRole(roleModal.username, r.key)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-colors
                    ${roleModal.role === r.key
                      ? 'border-accent/40 bg-accent/10'
                      : 'border-border hover:border-border/80 hover:bg-surface2'}`}
                >
                  <div className="flex-1">
                    <p className="text-text text-sm font-medium">{r.label}</p>
                    <p className="text-text-dim text-xs">{r.desc}</p>
                  </div>
                  {roleModal.role === r.key && (
                    <div className="w-2 h-2 rounded-full bg-accent flex-shrink-0" />
                  )}
                </button>
              ))}
            </div>
            <button onClick={() => setRoleModal(null)}
              className="w-full py-2 text-xs text-text-dim bg-surface2 hover:bg-border rounded-lg">
              Cancelar
            </button>
          </motion.div>
        </div>
      )}
    </div>
  )
}
