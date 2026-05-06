import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Camera, Upload, Loader, MessageSquare } from 'lucide-react'
import api from '../api/backend'

export default function PrintAnalysis({ onTokensUpdate, onSendToChat }) {
  const [image, setImage] = useState(null)  // base64 string
  const [imgDims, setImgDims] = useState(null)
  const [description, setDescription] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [capturing, setCapturing] = useState(false)
  const [countdown, setCountdown] = useState(0)
  const [copyLabel, setCopyLabel] = useState('Copiar')
  const fileRef = useRef(null)

  // Atalho global via Electron
  useEffect(() => {
    if (!window.electron) return
    const handler = () => handleCapture()
    window.electron.onCaptureShortcut(handler)
    return () => window.electron.removeListener('capture-shortcut')
  }, [])

  const handleCapture = async () => {
    // Countdown de 3s para o usuário trocar de janela
    setCapturing(true)
    setCountdown(3)
    await new Promise((resolve) => {
      let c = 3
      const t = setInterval(() => {
        c--
        setCountdown(c)
        if (c <= 0) { clearInterval(t); resolve() }
      }, 1000)
    })
    setCountdown(0)
    try {
      const res = await api.capturarTela()
      setImage(res.data.imagem)
      setImgDims(null)
    } catch (err) {
      setResult('Erro ao capturar tela: ' + (err.response?.data?.error || err.message))
    } finally {
      setCapturing(false)
    }
  }

  const handleFileLoad = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (ev) => {
      const base64 = ev.target.result.split(',')[1]
      setImage(base64)
      // Ler dimensões
      const img = new Image()
      img.onload = () => setImgDims({ w: img.naturalWidth, h: img.naturalHeight })
      img.src = ev.target.result
    }
    reader.readAsDataURL(file)
    // Limpa input para permitir recarregar o mesmo arquivo
    e.target.value = ''
  }

  const handleAnalyze = async () => {
    if (!image) return
    setLoading(true)
    setResult('')
    try {
      const res = await api.analisarPrint(image, description)
      setResult(res.data.resposta)
      try {
        const tok = await api.tokens()
        onTokensUpdate && onTokensUpdate(tok.data.total)
      } catch {}
    } catch (err) {
      setResult('Erro na análise: ' + (err.response?.data?.error || err.message))
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (!result) return
    navigator.clipboard.writeText(result).catch(() => {})
    setCopyLabel('Copiado!')
    setTimeout(() => setCopyLabel('Copiar'), 1500)
  }

  const handleSendToChat = () => {
    if (!result || !onSendToChat) return
    const userContent = description
      ? 'Analisei uma imagem. Descrição: ' + description
      : 'Analisei uma imagem do sistema ERP.'
    onSendToChat([
      { role: 'user',      content: userContent },
      { role: 'assistant', content: result },
    ])
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex-shrink-0">
        <h2 className="text-text font-semibold text-sm">Análise de Print</h2>
        <p className="text-text-dim text-xs mt-0.5">Capture ou carregue uma imagem para diagnóstico</p>
      </div>

      {/* Corpo */}
      <div className="flex-1 flex overflow-hidden">
        {/* Coluna esquerda — imagem */}
        <div className="w-2/5 border-r border-border flex flex-col p-4 gap-3 overflow-hidden">
          {/* Botões de ação */}
          <div className="flex gap-2 flex-shrink-0">
            <button
              onClick={handleCapture}
              disabled={capturing}
              className="flex-1 flex items-center justify-center gap-2 py-2 bg-accent hover:bg-accent-hover text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-50"
            >
              {countdown > 0
                ? <span className="text-lg font-bold leading-none">{countdown}</span>
                : capturing
                  ? <Loader size={14} className="animate-spin" />
                  : <Camera size={14} />
              }
              {countdown > 0 ? 'Preparando...' : capturing ? 'Capturando...' : 'Capturar Tela'}
            </button>
            <button
              onClick={() => fileRef.current?.click()}
              className="flex-1 flex items-center justify-center gap-2 py-2 bg-surface2 hover:bg-border text-text rounded-xl text-sm font-medium transition-colors"
            >
              <Upload size={14} />
              Carregar
            </button>
            <input
              ref={fileRef}
              type="file"
              accept="image/png,image/jpeg,image/bmp,image/gif"
              className="hidden"
              onChange={handleFileLoad}
            />
          </div>

          {/* Preview */}
          <div className="flex-1 bg-surface2 rounded-xl border border-border overflow-hidden flex items-center justify-center min-h-0">
            <AnimatePresence mode="wait">
              {image ? (
                <motion.img
                  key="img"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  src={'data:image/png;base64,' + image}
                  alt="Preview"
                  className="max-w-full max-h-full object-contain"
                />
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center text-text-muted p-8 select-none"
                >
                  <Camera size={32} className="mx-auto mb-2 opacity-25" />
                  <p className="text-xs">Nenhuma imagem carregada</p>
                  <p className="text-[10px] mt-1">Ctrl+Shift+P para capturar</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {imgDims && (
            <p className="text-[10px] text-text-muted text-center flex-shrink-0 select-none">
              {imgDims.w} × {imgDims.h} px
            </p>
          )}
        </div>

        {/* Coluna direita — formulário + resultado */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Descrição + botão analisar */}
          <div className="p-4 border-b border-border space-y-3 flex-shrink-0">
            <div>
              <label className="block text-text-dim text-[10px] font-semibold uppercase tracking-wider mb-2">
                Descrição do problema (opcional)
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Descreva o erro ou comportamento observado..."
                rows={3}
                style={{ resize: 'none' }}
                className="w-full bg-surface2 border border-border rounded-xl px-3 py-2.5 text-sm text-text outline-none focus:border-accent transition-colors selectable font-sans leading-relaxed"
              />
            </div>
            <button
              onClick={handleAnalyze}
              disabled={!image || loading}
              className="w-full py-2.5 bg-[#6d4ae0] hover:bg-[#7c5cf6] text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading && <Loader size={14} className="animate-spin" />}
              {loading ? 'Analisando...' : 'Analisar com IA'}
            </button>
          </div>

          {/* Resultado */}
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="px-4 py-2 border-b border-border flex items-center justify-between flex-shrink-0">
              <span className="text-text-muted text-[10px] font-semibold uppercase tracking-wider select-none">
                Resultado da Análise
              </span>
              {result && (
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
                    className="text-[10px] text-text-dim hover:text-text transition-colors"
                  >
                    {copyLabel}
                  </button>
                </div>
              )}
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {loading ? (
                <div className="flex items-center gap-3 text-text-dim">
                  <Loader size={15} className="animate-spin flex-shrink-0" />
                  <span className="text-sm">Aguardando resposta da IA...</span>
                </div>
              ) : result ? (
                <p className="text-text text-sm leading-relaxed whitespace-pre-wrap selectable">{result}</p>
              ) : (
                <p className="text-text-muted text-sm">
                  Capture ou carregue uma imagem e clique em "Analisar com IA".
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
