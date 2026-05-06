import { useState, useRef, useCallback } from 'react'
import { Search, FileCode, Send, FolderOpen, Upload, X, FileText } from 'lucide-react'
import ChatMessage from '../components/ChatMessage'
import LoadingDots from '../components/LoadingDots'
import api from '../api/backend'

const TIPOS = [
  { value: 'nfe',  label: 'NFe / NFCe' },
  { value: 'nfse', label: 'NFSe (Serviço)' },
]

function getMesAtual() {
  const d = new Date()
  return String(d.getFullYear()) + String(d.getMonth() + 1).padStart(2, '0')
}

function lerArquivo(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload  = (e) => resolve({ nome: file.name, conteudo: e.target.result })
    reader.onerror = reject
    reader.readAsText(file, 'utf-8')
  })
}

export default function XmlAnalysis({ onSendToChat }) {
  const [modo, setModo]               = useState('upload')    // 'upload' | 'numero'
  const [tipo, setTipo]               = useState('nfe')
  const [numeroNota, setNumeroNota]   = useState('')
  const [dataRef, setDataRef]         = useState(getMesAtual())
  const [caminhoCustom, setCaminhoCustom] = useState('')
  const [mostrarCustom, setMostrarCustom] = useState(false)
  const [arquivos, setArquivos]       = useState([])          // [{nome, conteudo}]
  const [dragOver, setDragOver]       = useState(false)
  const [loading, setLoading]         = useState(false)
  const [resultado, setResultado]     = useState(null)
  const [erro, setErro]               = useState('')
  const inputFileRef = useRef(null)

  // ── Drag & drop ────────────────────────────────────────────────────────────
  const adicionarArquivos = useCallback(async (fileList) => {
    const novos = []
    for (const file of fileList) {
      if (!file.name.toLowerCase().endsWith('.xml')) continue
      try {
        const parsed = await lerArquivo(file)
        novos.push(parsed)
      } catch {}
    }
    if (novos.length > 0) setArquivos((prev) => [...prev, ...novos])
  }, [])

  const onDrop = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    adicionarArquivos(e.dataTransfer.files)
  }, [adicionarArquivos])

  const onDragOver = (e) => { e.preventDefault(); setDragOver(true) }
  const onDragLeave = () => setDragOver(false)

  const removerArquivo = (i) => setArquivos((prev) => prev.filter((_, idx) => idx !== i))

  // ── Analisar ───────────────────────────────────────────────────────────────
  const analisar = async () => {
    const podeAnalisar = modo === 'upload' ? arquivos.length > 0 : numeroNota.trim()
    if (!podeAnalisar || loading) return

    setLoading(true)
    setResultado(null)
    setErro('')

    try {
      let res
      if (modo === 'upload') {
        res = await api.analisarXmlUpload(arquivos, tipo)
      } else {
        res = await api.analisarXml(
          numeroNota.trim(),
          tipo,
          tipo === 'nfse' ? dataRef : '',
          caminhoCustom.trim()
        )
      }
      setResultado(res.data)
    } catch (err) {
      setErro(err.response?.data?.error || err.message)
    } finally {
      setLoading(false)
    }
  }

  const enviarParaChat = () => {
    if (!resultado?.resposta) return
    const label = modo === 'upload'
      ? arquivos.map((a) => a.nome).join(', ')
      : 'nota ' + numeroNota
    onSendToChat && onSendToChat([
      { role: 'user',      content: 'Analise o XML: ' + label },
      { role: 'assistant', content: resultado.resposta },
    ])
  }

  const podeanalisar = modo === 'upload' ? arquivos.length > 0 : numeroNota.trim()

  return (
    <div className="flex flex-col h-full overflow-hidden">

      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/40 flex-shrink-0">
        <div className="flex items-center gap-2">
          <FileCode size={16} className="text-accent" />
          <h2 className="text-text font-semibold text-sm">Análise de XML</h2>
        </div>
        <p className="text-text-dim text-xs mt-0.5">NFe, NFCe e NFSe — arraste XMLs ou busque pelo número da nota</p>
      </div>

      {/* Controles */}
      <div className="p-4 border-b border-border bg-surface/20 flex-shrink-0 space-y-3">

        {/* Tipo de nota */}
        <div className="flex gap-2">
          {TIPOS.map((t) => (
            <button key={t.value} onClick={() => setTipo(t.value)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border
                ${tipo === t.value
                  ? 'bg-accent/15 text-accent border-accent/30'
                  : 'text-text-dim border-border hover:bg-surface hover:text-text'}`}>
              {t.label}
            </button>
          ))}
        </div>

        {/* Modo: upload ou número */}
        <div className="flex gap-2">
          {[['upload','Arrastar XML'], ['numero','Número da nota']].map(([m, label]) => (
            <button key={m} onClick={() => setModo(m)}
              className={`px-3 py-1 rounded-lg text-[11px] transition-colors border
                ${modo === m
                  ? 'bg-surface2 text-text border-border'
                  : 'text-text-muted border-transparent hover:text-text-dim'}`}>
              {label}
            </button>
          ))}
        </div>

        {/* Upload mode */}
        {modo === 'upload' && (
          <div>
            {/* Drop zone */}
            <div
              onDrop={onDrop}
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onClick={() => inputFileRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-colors
                ${dragOver
                  ? 'border-accent bg-accent/10 text-accent'
                  : 'border-border hover:border-accent/50 hover:bg-surface/50 text-text-muted'}`}>
              <Upload size={20} className="mx-auto mb-2 opacity-60" />
              <p className="text-xs">Arraste os XMLs aqui ou clique para selecionar</p>
              <p className="text-[10px] mt-1 opacity-60">Envio, retorno, protocolo — pode soltar vários de uma vez</p>
              <input
                ref={inputFileRef}
                type="file"
                accept=".xml"
                multiple
                className="hidden"
                onChange={(e) => adicionarArquivos(e.target.files)}
              />
            </div>

            {/* Lista de arquivos adicionados */}
            {arquivos.length > 0 && (
              <div className="mt-2 space-y-1">
                {arquivos.map((arq, i) => (
                  <div key={i} className="flex items-center gap-2 bg-surface2 border border-border rounded-lg px-3 py-1.5">
                    <FileText size={12} className="text-accent flex-shrink-0" />
                    <span className="text-xs text-text font-mono flex-1 truncate">{arq.nome}</span>
                    <button onClick={() => removerArquivo(i)}
                      className="text-text-muted hover:text-error transition-colors flex-shrink-0">
                      <X size={12} />
                    </button>
                  </div>
                ))}
                {arquivos.length > 1 && (
                  <button onClick={() => setArquivos([])}
                    className="text-[10px] text-text-muted hover:text-error transition-colors">
                    Remover todos
                  </button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Número da nota mode */}
        {modo === 'numero' && (
          <div className="space-y-2">
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
                <input
                  type="text"
                  value={numeroNota}
                  onChange={(e) => setNumeroNota(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && analisar()}
                  placeholder="Número da nota (ex: 1234)"
                  className="w-full bg-surface2 border border-border rounded-xl pl-8 pr-4 py-2 text-sm text-text outline-none focus:border-accent transition-colors"
                />
              </div>
              {tipo === 'nfse' && (
                <input type="text" value={dataRef} onChange={(e) => setDataRef(e.target.value)}
                  placeholder="YYYYMM" maxLength={6}
                  title="Mês de referência (ex: 202604)"
                  className="w-24 bg-surface2 border border-border rounded-xl px-3 py-2 text-sm text-text outline-none focus:border-accent transition-colors text-center" />
              )}
            </div>

            <div>
              <button onClick={() => setMostrarCustom(!mostrarCustom)}
                className="text-[10px] text-text-muted hover:text-text-dim transition-colors flex items-center gap-1">
                <FolderOpen size={11} />
                {mostrarCustom ? 'Ocultar caminho' : 'Caminho personalizado (WTS, outro)'}
              </button>
              {mostrarCustom && (
                <input type="text" value={caminhoCustom} onChange={(e) => setCaminhoCustom(e.target.value)}
                  placeholder="Ex: C:\usuarios\farmafacil\NFE"
                  className="mt-1.5 w-full bg-surface2 border border-border rounded-xl px-3 py-2 text-xs text-text outline-none focus:border-accent transition-colors font-mono" />
              )}
              <p className="text-[10px] text-text-muted mt-1">
                Padrão: {tipo === 'nfse'
                  ? 'C:\\FarmaFacil\\EXE\\' + (dataRef || 'YYYYMM') + '\\NFSe'
                  : 'C:\\FarmaFacil\\NFE'}
              </p>
            </div>
          </div>
        )}

        {/* Botão analisar */}
        <button
          onClick={analisar}
          disabled={loading || !podeanalisar}
          className="w-full py-2 bg-accent hover:bg-accent-hover text-white rounded-xl text-sm font-medium transition-colors disabled:opacity-40 flex items-center justify-center gap-2">
          {loading ? <LoadingDots /> : <><Search size={14} /> Analisar{tipo === 'nfse' ? ' (busca fórum ACBR)' : ''}</>}
        </button>
      </div>

      {/* Resultado */}
      <div className="flex-1 overflow-y-auto">
        {erro && (
          <div className="m-4 p-3 bg-error/10 border border-error/30 rounded-xl text-error text-sm">{erro}</div>
        )}

        {loading && (
          <div className="flex justify-start px-4 mt-4">
            <div className="w-7 h-7 rounded-full bg-accent flex items-center justify-center text-white text-[10px] font-bold mr-2 flex-shrink-0 mt-0.5">IA</div>
            <div className="bg-msg-ai border border-border/50 rounded-2xl rounded-bl-sm px-4 py-2.5">
              <LoadingDots />
            </div>
          </div>
        )}

        {resultado && !loading && (
          <div>
            {/* Arquivos analisados */}
            {resultado.arquivos?.length > 0 && (
              <div className="mx-4 mt-4 mb-2 flex flex-wrap gap-1.5">
                {resultado.arquivos.map((arq, i) => (
                  <span key={i} className="text-[10px] font-mono bg-surface2 border border-border rounded px-2 py-0.5 text-text-dim">
                    {arq}
                  </span>
                ))}
              </div>
            )}

            {/* Erros detectados */}
            {resultado.erros_detectados?.length > 0 && (
              <div className="mx-4 mb-2 flex flex-wrap gap-1.5 items-center">
                <span className="text-[10px] text-text-muted">Códigos detectados:</span>
                {resultado.erros_detectados.map((e, i) => (
                  <span key={i} className="text-[10px] font-mono bg-warning/10 border border-warning/30 text-warning rounded px-2 py-0.5">
                    {e}
                  </span>
                ))}
              </div>
            )}

            <ChatMessage role="assistant" content={resultado.resposta} timestamp={Date.now()} />

            <div className="px-4 pb-4">
              <button onClick={enviarParaChat}
                className="flex items-center gap-2 text-xs text-text-dim hover:text-accent transition-colors px-3 py-1.5 rounded-lg border border-border hover:border-accent/40">
                <Send size={12} />
                Continuar no Chat
              </button>
            </div>
          </div>
        )}

        {!resultado && !loading && !erro && (
          <div className="flex items-center justify-center h-full text-text-muted text-sm">
            {modo === 'upload' ? 'Arraste os XMLs acima para começar' : 'Informe o número da nota para analisar'}
          </div>
        )}
      </div>
    </div>
  )
}
