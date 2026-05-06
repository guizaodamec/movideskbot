import { useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FileText, Upload, Loader, Copy, Check, AlertTriangle, X, MessageSquare } from 'lucide-react'
import api from '../api/backend'

export default function LogAnalysis({ onTokensUpdate, onSendToChat }) {
  const [logText, setLogText]     = useState('')
  const [contexto, setContexto]   = useState('')
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState('')
  const [error, setError]         = useState('')
  const [copied, setCopied]       = useState(false)
  const [fileName, setFileName]   = useState('')
  const fileRef = useRef(null)

  const handleFile = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setFileName(file.name)
    const reader = new FileReader()
    reader.onload = (ev) => setLogText(ev.target.result || '')
    reader.readAsText(file, 'utf-8')
    e.target.value = ''
  }

  const handleAnalyze = async () => {
    if (!logText.trim() || loading) return
    setLoading(true)
    setResult('')
    setError('')
    try {
      const res = await api.analisarLog(logText, contexto)
      setResult(res.data.resposta || '')
      try {
        const tok = await api.tokens()
        onTokensUpdate && onTokensUpdate(tok.data.total)
      } catch {}
    } catch (err) {
      setError(err.response?.data?.error || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(result).catch(() => {})
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const handleClear = () => {
    setLogText('')
    setFileName('')
    setResult('')
    setError('')
    setContexto('')
  }

  const handleSendToChat = () => {
    if (!result || !onSendToChat) return
    const preview = logText.slice(0, 300).trim()
    const userContent =
      'Analisei o seguinte log' +
      (contexto ? ' (' + contexto + ')' : '') +
      ':\n\n' + preview + (logText.length > 300 ? '\n...' : '')
    onSendToChat([
      { role: 'user',      content: userContent },
      { role: 'assistant', content: result },
    ])
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex-shrink-0">
        <h2 className="text-text font-semibold text-sm">Analisar Log</h2>
        <p className="text-text-dim text-xs mt-0.5">Diagnóstico de logs PostgreSQL e ERP com IA</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">

        {/* Upload / paste */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-text-dim text-[10px] font-semibold uppercase tracking-wider">
              Conteúdo do Log
            </label>
            <div className="flex items-center gap-2">
              {(logText || fileName) && (
                <button onClick={handleClear}
                  className="flex items-center gap-1 text-[10px] text-text-muted hover:text-error transition-colors">
                  <X size={11} /> Limpar
                </button>
              )}
              <button
                onClick={() => fileRef.current?.click()}
                className="flex items-center gap-1.5 px-2.5 py-1.5 bg-surface2 border border-border hover:border-accent text-text-dim text-[11px] rounded-lg transition-colors"
              >
                <Upload size={12} />
                {fileName ? fileName : 'Carregar arquivo'}
              </button>
              <input ref={fileRef} type="file" accept=".log,.txt,.csv" className="hidden" onChange={handleFile} />
            </div>
          </div>

          <textarea
            value={logText}
            onChange={(e) => setLogText(e.target.value)}
            placeholder={"Cole o conteúdo do log aqui...\n\nExemplos:\n- postgresql.log\n- pg_log/*.log\n- Mensagens de erro do sistema ERP\n- Output do pg_dump com erro"}
            rows={12}
            className="w-full bg-surface2 border border-border rounded-xl px-4 py-3 text-text text-xs font-mono outline-none focus:border-accent transition-colors resize-none selectable leading-relaxed"
          />
          <p className="text-text-muted text-[10px]">
            {logText.length > 0
              ? logText.length.toLocaleString() + ' caracteres' + (logText.length > 8000 ? ' — será truncado para 8.000' : '')
              : 'Máximo 8.000 caracteres analisados'}
          </p>
        </div>

        {/* Contexto */}
        <div className="space-y-2">
          <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider">
            Contexto adicional (opcional)
          </label>
          <input
            type="text"
            value={contexto}
            onChange={(e) => setContexto(e.target.value)}
            placeholder="Ex: banco corrompido após queda de energia, cliente com lentidão extrema..."
            className="w-full bg-surface2 border border-border rounded-xl px-4 py-2.5 text-text text-sm outline-none focus:border-accent transition-colors selectable"
          />
        </div>

        {/* Botão analisar */}
        <button
          onClick={handleAnalyze}
          disabled={!logText.trim() || loading}
          className="w-full py-3 bg-accent hover:bg-accent-hover text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-40 flex items-center justify-center gap-2"
        >
          {loading
            ? <><Loader size={15} className="animate-spin" /> Analisando...</>
            : <><FileText size={15} /> Analisar Log</>}
        </button>

        {/* Erro */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex items-start gap-2 p-3 bg-error/10 border border-error/20 rounded-xl text-error text-sm"
            >
              <AlertTriangle size={15} className="flex-shrink-0 mt-0.5" />
              <span className="selectable">{error}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Resultado */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-surface border border-border rounded-xl overflow-hidden"
            >
              <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-surface2">
                <span className="text-text text-xs font-semibold">Análise da IA</span>
                <div className="flex items-center gap-3">
                  <button
                    onClick={handleSendToChat}
                    className="flex items-center gap-1 text-[11px] text-accent hover:text-accent-hover font-medium transition-colors"
                    title="Continuar análise no chat"
                  >
                    <MessageSquare size={12} />
                    Levar pro Chat
                  </button>
                  <button
                    onClick={handleCopy}
                    className="flex items-center gap-1 text-[11px] text-text-dim hover:text-text transition-colors"
                  >
                    {copied ? <Check size={12} className="text-success" /> : <Copy size={12} />}
                    {copied ? 'Copiado' : 'Copiar'}
                  </button>
                </div>
              </div>
              <div className="px-4 py-4 text-sm text-text leading-relaxed whitespace-pre-wrap selectable font-mono text-xs">
                {result}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
