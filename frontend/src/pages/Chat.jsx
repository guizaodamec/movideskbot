import { useState, useRef, useEffect, useCallback } from 'react'
import { Send, Download, X, ChevronDown } from 'lucide-react'
import ChatMessage from '../components/ChatMessage'
import LoadingDots from '../components/LoadingDots'
import ConfirmDialog from '../components/ConfirmDialog'
import api from '../api/backend'

const MAX_HISTORY = 30

const AI_MODELS = [
  { id: 'cc/claude-sonnet-4-6',  label: 'Claude (CC)',  emoji: '⚡', desc: 'Claude local via Claude Code — principal' },
  { id: 'kr/claude-sonnet-4.5',  label: 'Kiro',         emoji: '🤖', desc: 'Claude Sonnet via Kiro' },
  { id: 'pollinations/openai',   label: 'GPT-4o',       emoji: '🟢', desc: 'OpenAI GPT-4o via Pollinations' },
]

function ModelSelector({ value, onChange }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const selected = AI_MODELS.find(m => m.id === value) || AI_MODELS[0]

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1.5 px-2.5 py-1.5 bg-surface2 border border-border hover:border-accent/60 rounded-lg text-xs text-text-dim hover:text-text transition-colors"
        title="Escolher IA"
      >
        <span>{selected.emoji}</span>
        <span className="font-medium">{selected.label}</span>
        <ChevronDown size={11} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute bottom-full mb-1 left-0 w-52 bg-surface border border-border rounded-xl shadow-xl z-50 overflow-hidden">
          <div className="px-3 py-2 border-b border-border/50">
            <p className="text-[10px] text-text-muted font-semibold uppercase tracking-wider">Escolher IA</p>
          </div>
          {AI_MODELS.map(m => (
            <button
              key={m.id}
              onClick={() => { onChange(m.id); setOpen(false) }}
              className={`w-full flex items-start gap-2.5 px-3 py-2 hover:bg-surface2 transition-colors text-left ${m.id === value ? 'bg-accent/10' : ''}`}
            >
              <span className="text-base mt-0.5">{m.emoji}</span>
              <div>
                <p className={`text-xs font-medium ${m.id === value ? 'text-accent' : 'text-text'}`}>{m.label}</p>
                <p className="text-[10px] text-text-muted leading-tight">{m.desc}</p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function getHistoryKey() {
  const user = localStorage.getItem('erp_username') || 'default'
  const db   = localStorage.getItem('erp_dbname')   || 'default'
  return 'chat_history_' + user + '_' + db
}

function loadHistory() {
  try {
    const raw = localStorage.getItem(getHistoryKey())
    if (raw) return JSON.parse(raw)
  } catch {}
  return []
}

function saveHistory(msgs) {
  try {
    // Salva as últimas MAX_HISTORY mensagens
    localStorage.setItem(getHistoryKey(), JSON.stringify(msgs.slice(-MAX_HISTORY)))
  } catch {}
}

export default function Chat({ profile, onTokensUpdate, initContext, onContextConsumed }) {
  const [messages, setMessages]           = useState(() => loadHistory())
  const [input, setInput]                 = useState('')
  const [loading, setLoading]             = useState(false)
  const [streamingContent, setStreaming]  = useState(null)
  const [confirmState, setConfirmState]   = useState(null)
  const [pendingImage, setPendingImage]   = useState(null)
  const [selectedModel, setSelectedModel] = useState(AI_MODELS[0].id)
  const bottomRef    = useRef(null)
  const inputRef     = useRef(null)
  const welcomeSent  = useRef(false)

  // Carrega contexto externo (vindo de Análise de Print ou Log)
  useEffect(() => {
    if (!initContext || initContext.length === 0) return
    const msgs = initContext.map((m) => ({ ...m, timestamp: m.timestamp || Date.now() }))
    setMessages(msgs)
    saveHistory(msgs)
    welcomeSent.current = true
    onContextConsumed && onContextConsumed()
  }, [initContext])

  // Mensagem de boas-vindas apenas se não tiver histórico salvo
  useEffect(() => {
    if (!profile || welcomeSent.current) return
    welcomeSent.current = true

    const saved = loadHistory()
    if (saved.length > 0) {
      // Já tem histórico — não manda boas-vindas de novo
      setMessages(saved)
      return
    }

    const empresa = profile.razao_social || profile.empresa || 'banco'
    const versao  = profile.versao_sistema
    const bv =
      'Conectado a ' + empresa +
      (versao ? ' v' + versao : '') + '.\n' +
      'Como posso ajudar?'

    const welcome = [{ role: 'assistant', content: bv, timestamp: Date.now() }]
    setMessages(welcome)
    saveHistory(welcome)
  }, [profile])

  // Persiste histórico a cada mudança
  useEffect(() => {
    if (messages.length > 0) saveHistory(messages)
  }, [messages])

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // Executa query — abre ConfirmDialog para MODIFY
  const executeQuery = useCallback(async (sql, type) => {
    if (type === 'MODIFY') {
      const confirmed = await new Promise((resolve) => {
        setConfirmState({ query: sql, resolve })
      })
      setConfirmState(null)
      if (!confirmed) return { error: 'Execução cancelada pelo usuário.' }
    }

    try {
      const res = await api.executarQuery(sql)
      try {
        const tok = await api.tokens()
        onTokensUpdate && onTokensUpdate(tok.data.total)
      } catch {}
      return res.data
    } catch (err) {
      return { error: err.response?.data?.error || err.message }
    }
  }, [onTokensUpdate])

  const handlePaste = useCallback((e) => {
    const items = e.clipboardData?.items || []
    for (const item of items) {
      if (item.type.startsWith('image/')) {
        e.preventDefault()
        const file   = item.getAsFile()
        const reader = new FileReader()
        reader.onload = (ev) => {
          // Remove o prefixo "data:image/...;base64,"
          const b64 = ev.target.result.split(',')[1]
          setPendingImage(b64)
        }
        reader.readAsDataURL(file)
        break
      }
    }
  }, [])

  const sendMessage = async () => {
    const text = input.trim()
    if ((!text && !pendingImage) || loading) return

    const userMsg     = { role: 'user', content: text || '(imagem)', timestamp: Date.now(), imagePreview: pendingImage }
    const newMessages = [...messages, userMsg].slice(-MAX_HISTORY)
    setMessages(newMessages)
    setInput('')
    const imgParaEnviar = pendingImage
    setPendingImage(null)
    setLoading(true)
    setStreaming('')

    try {
      const historico = newMessages.filter((m) => !m.isError).map((m) => ({ role: m.role, content: m.content }))
      const token     = localStorage.getItem('erp_token')
      const base      = `http://${window.location.hostname}:5000/api`

      const response = await fetch(`${base}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ mensagem: text || '(imagem)', historico, imagem: imgParaEnviar || undefined, model: selectedModel }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const reader  = response.body.getReader()
      const decoder = new TextDecoder()
      let accumulated = ''
      let buffer      = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const jsonStr = line.slice(6).trim()
          if (!jsonStr) continue
          try {
            const event = JSON.parse(jsonStr)
            if (event.token) {
              accumulated += event.token
              setStreaming(accumulated)
            } else if (event.done) {
              const finalText = event.text || accumulated
              const aiMsg = { role: 'assistant', content: finalText, timestamp: Date.now(), model: selectedModel }
              setMessages((prev) => {
                const updated = [...prev, aiMsg].slice(-MAX_HISTORY)
                saveHistory(updated)
                return updated
              })
            } else if (event.error) {
              throw new Error(event.error)
            }
          } catch (parseErr) {
            if (parseErr.message && !parseErr.message.startsWith('JSON')) throw parseErr
          }
        }
      }
    } catch (err) {
      const errMsg = {
        role: 'assistant',
        content: 'Erro ao processar sua mensagem: ' + (err.message || 'Falha na conexão'),
        timestamp: Date.now(),
        isError: true,
      }
      setMessages((prev) => [...prev, errMsg])
    } finally {
      setLoading(false)
      setStreaming(null)
      setTimeout(() => inputRef.current?.focus(), 0)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleInput = (e) => {
    setInput(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px'
  }

  const clearHistory = () => {
    localStorage.removeItem(getHistoryKey())
    welcomeSent.current = false
    setMessages([])
  }

  const downloadHistory = () => {
    const db      = localStorage.getItem('erp_dbname') || ''
    const usuario = localStorage.getItem('erp_username') || ''
    const agora   = new Date().toLocaleString('pt-BR')

    // ── Histórico completo ─────────────────────────────────────────────────
    const linhasChat = messages.map((m) => {
      const time  = m.timestamp ? new Date(m.timestamp).toLocaleString('pt-BR') : ''
      const role  = m.role === 'user' ? 'ANALISTA' : 'IA'
      const flag  = m.isError ? ' [ERRO]' : ''
      return '[' + time + '] ' + role + flag + ':\n' + m.content
    }).join('\n\n---\n\n')

    // ── Seção de erros para estudo ─────────────────────────────────────────
    const erros = messages.filter((m) =>
      m.isError ||
      (m.role === 'assistant' && /erro|error|rejeição|rejei|falha|exception|traceback/i.test(m.content))
    )

    let secaoErros = ''
    if (erros.length > 0) {
      secaoErros = '\n\n' + '='.repeat(60) + '\n'
      secaoErros += 'ERROS DETECTADOS — para estudo e melhoria da IA\n'
      secaoErros += '='.repeat(60) + '\n\n'
      erros.forEach((m, i) => {
        const time = m.timestamp ? new Date(m.timestamp).toLocaleString('pt-BR') : ''
        secaoErros += (i + 1) + '. [' + time + ']\n' + m.content + '\n\n'
      })
    }

    const cabecalho =
      'FarmaFácil Assistente — Histórico de Chat\n' +
      'Usuário: ' + usuario + ' | Banco: ' + (db || 'não conectado') + '\n' +
      'Exportado em: ' + agora + '\n' +
      '='.repeat(60) + '\n\n'

    const conteudo = cabecalho + linhasChat + secaoErros

    const blob = new Blob([conteudo], { type: 'text/plain;charset=utf-8' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = 'chat_' + new Date().toISOString().slice(0, 10) + '_' + (usuario || 'user') + '.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex-shrink-0 flex items-center justify-between">
        <div>
          <h2 className="text-text font-semibold text-sm leading-tight">
            {profile?.razao_social || profile?.empresa || 'Chat'}
          </h2>
          <p className="text-text-dim text-xs mt-0.5">Assistente técnico ERP com IA</p>
        </div>
        {messages.length > 1 && (
          <div className="flex items-center gap-1">
            <button
              onClick={downloadHistory}
              className="p-1.5 text-text-muted hover:text-accent transition-colors rounded"
              title="Baixar histórico do chat"
            >
              <Download size={13} />
            </button>
            <button
              onClick={clearHistory}
              className="text-[10px] text-text-muted hover:text-error transition-colors px-2 py-1 rounded"
              title="Limpar conversa"
            >
              Limpar
            </button>
          </div>
        )}
      </div>

      {/* Mensagens */}
      <div className="flex-1 overflow-y-auto py-4">
        {messages.length === 0 && !loading && (
          <div className="flex items-center justify-center h-full text-text-muted text-sm">
            Aguardando perfil do banco...
          </div>
        )}
        {messages.map((msg, i) => (
          <ChatMessage
            key={i}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
            onExecuteQuery={executeQuery}
          />
        ))}
        {loading && (
          <div className="flex justify-start px-4 mb-3">
            <div className="w-7 h-7 rounded-full bg-accent flex items-center justify-center text-white text-[10px] font-bold mr-2 flex-shrink-0 mt-0.5 select-none">
              IA
            </div>
            <div className="bg-msg-ai border border-border/50 rounded-2xl rounded-bl-sm px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap selectable text-text max-w-[80%]">
              {streamingContent ? streamingContent : <LoadingDots />}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-border p-3 bg-surface/30 flex-shrink-0">

        {/* Preview da imagem colada */}
        {pendingImage && (
          <div className="mb-2 relative inline-flex">
            <img
              src={'data:image/png;base64,' + pendingImage}
              alt="imagem colada"
              className="max-h-24 max-w-xs rounded-lg border border-accent/40 object-contain"
            />
            <button
              onClick={() => setPendingImage(null)}
              className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-error rounded-full flex items-center justify-center"
              title="Remover imagem"
            >
              <X size={9} className="text-white" />
            </button>
          </div>
        )}

        <div className="flex items-center justify-between mb-2">
          <ModelSelector value={selectedModel} onChange={setSelectedModel} />
          <p className="text-[10px] text-text-muted select-none">Enter · Shift+Enter · Ctrl+V imagem</p>
        </div>

        <div className="flex items-end gap-2">
          <div className="flex-1 bg-surface2 border border-border rounded-xl focus-within:border-accent transition-colors overflow-hidden">
            <textarea
              ref={inputRef}
              value={input}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              onPaste={handlePaste}
              placeholder={pendingImage ? 'Adicione um comentário (opcional)...' : 'Faça uma pergunta ou cole uma imagem (Ctrl+V)...'}
              rows={1}
              style={{ resize: 'none', height: '40px' }}
              className="w-full bg-transparent text-text text-sm px-4 py-2.5 outline-none selectable font-sans leading-relaxed overflow-y-auto"
              disabled={loading}
            />
          </div>

          <button
            onClick={sendMessage}
            disabled={loading || (!input.trim() && !pendingImage)}
            className="p-2.5 bg-accent hover:bg-accent-hover text-white rounded-xl transition-colors disabled:opacity-40 flex-shrink-0"
            title="Enviar (Enter)"
          >
            <Send size={16} />
          </button>
        </div>
      </div>

      <ConfirmDialog
        open={!!confirmState}
        query={confirmState?.query || ''}
        explanation="Esta query irá modificar dados no banco de dados. Revise com atenção antes de confirmar."
        onConfirm={() => confirmState?.resolve(true)}
        onCancel={() => confirmState?.resolve(false)}
      />
    </div>
  )
}
