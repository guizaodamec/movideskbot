import { useState } from 'react'
import { motion } from 'framer-motion'
import { Copy, Check } from 'lucide-react'
import SqlBlock from './SqlBlock'

function formatTime(ts) {
  if (!ts) return ''
  try {
    return new Date(ts).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

// Divide mensagem em partes: texto comum e blocos SQL
function parseContent(text) {
  const parts = []
  const regex = /```sql\s*\n?([\s\S]*?)\n?```/gi
  let lastIndex = 0
  let match

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: text.slice(lastIndex, match.index) })
    }
    parts.push({ type: 'sql', content: match[1].trim() })
    lastIndex = match.index + match[0].length
  }

  if (lastIndex < text.length) {
    parts.push({ type: 'text', content: text.slice(lastIndex) })
  }

  return parts
}

export default function ChatMessage({ role, content, timestamp, onExecuteQuery }) {
  const isUser = role === 'user'
  const parts = isUser ? [{ type: 'text', content }] : parseContent(content)
  const [copied, setCopied] = useState(false)

  function handleCopy() {
    navigator.clipboard.writeText(content).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.18 }}
      className={['flex mb-3 px-4', isUser ? 'justify-end' : 'justify-start'].join(' ')}
    >
      {/* Avatar IA */}
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-accent flex items-center justify-center text-white text-[10px] font-bold mr-2 flex-shrink-0 mt-0.5 select-none">
          IA
        </div>
      )}

      <div className={['flex flex-col gap-1 max-w-[80%]', isUser ? 'items-end' : 'items-start'].join(' ')}>
        {parts.map((part, i) =>
          part.type === 'sql' ? (
            <SqlBlock
              key={i}
              sql={part.content}
              onExecute={onExecuteQuery}
            />
          ) : (
            part.content.trim() ? (
              <div
                key={i}
                className={[
                  'rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap selectable',
                  isUser
                    ? 'bg-[#1e3a5f] text-white rounded-br-sm'
                    : 'bg-msg-ai text-text rounded-bl-sm border border-border/50',
                ].join(' ')}
              >
                {part.content.trim()}
              </div>
            ) : null
          )
        )}

        {/* Timestamp + botão copiar */}
        <div className="flex items-center gap-2 px-1">
          <span className="text-[10px] text-text-muted select-none">
            {formatTime(timestamp)}
          </span>
          {!isUser && (
            <button
              onClick={handleCopy}
              title="Copiar resposta"
              className="text-text-muted hover:text-text transition-colors select-none"
            >
              {copied
                ? <Check size={12} className="text-green-400" />
                : <Copy size={12} />}
            </button>
          )}
        </div>
      </div>
    </motion.div>
  )
}
