import { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, User, Settings, ChevronLeft, ChevronRight, Users, LogOut, BarChart2, Inbox, KanbanSquare, ShieldAlert, Trophy, ClipboardCheck, PackageCheck } from 'lucide-react'
import ConnectionBadge from './ConnectionBadge'

const ALL_NAV = [
  { key: 'chat',          label: 'Chat',              icon: MessageSquare  },
  { key: 'abertos-hoje',  label: 'Abertos Hoje',      icon: Inbox          },
  { key: 'tarefas',       label: 'Tarefas',           icon: KanbanSquare   },
  { key: 'provedor',      label: 'Provedores NFS-e',  icon: ShieldAlert    },
  { key: 'versoes',       label: 'Versões Clientes',  icon: PackageCheck   },
  { key: 'gestao',        label: 'Gestão',            icon: BarChart2      },
  { key: 'auditoria',     label: 'Auditoria',         icon: ClipboardCheck },
  { key: 'painel',        label: 'Painel TV',         icon: Trophy         },
  { key: 'profile',       label: 'Perfil',            icon: User           },
  { key: 'config',        label: 'Configuração',      icon: Settings       },
  { key: 'users',         label: 'Usuários',          icon: Users          },
]

const ROLE_PAGES = {
  analista:      new Set(['chat', 'tarefas', 'gestao', 'provedor', 'versoes']),
  backservice:   new Set(['chat', 'abertos-hoje', 'tarefas', 'gestao', 'provedor', 'versoes']),
  fiscal:        new Set(['chat', 'abertos-hoje', 'tarefas', 'gestao', 'provedor', 'versoes']),
  lideres:       new Set(['chat', 'gestao', 'abertos-hoje', 'tarefas', 'provedor', 'painel', 'auditoria', 'versoes']),
  administrador: new Set(['chat', 'profile', 'config', 'gestao', 'users', 'abertos-hoje', 'tarefas', 'provedor', 'painel', 'auditoria', 'versoes']),
}

const ROLE_LABELS = {
  analista:      'Analista',
  backservice:   'Backservice',
  fiscal:        'Fiscal',
  lideres:       'Líder',
  administrador: 'Admin',
}

export default function Sidebar({ active, onNavigate, onLogout, host, connected, isAdmin, role = 'analista', username }) {
  const [expanded, setExpanded] = useState(true)

  const allowed = ROLE_PAGES[role] || ROLE_PAGES['analista']
  const navItems = ALL_NAV.filter(item => allowed.has(item.key))
  const roleLabel = ROLE_LABELS[role] || role

  return (
    <motion.aside
      animate={{ width: expanded ? 220 : 64 }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
      className="flex flex-col bg-[#0e1120] border-r border-border h-full overflow-hidden flex-shrink-0"
    >
      {/* Toggle */}
      <div className="flex justify-end p-2 border-b border-border/40">
        <button
          onClick={() => setExpanded(!expanded)}
          className="p-1.5 rounded-lg text-text-dim hover:text-text hover:bg-surface transition-colors"
          title={expanded ? 'Recolher sidebar' : 'Expandir sidebar'}
        >
          {expanded ? <ChevronLeft size={15} /> : <ChevronRight size={15} />}
        </button>
      </div>

      {/* Navegação */}
      <nav className="flex-1 py-2 px-2 space-y-0.5 overflow-y-auto">
        {navItems.map(({ key, label, icon: Icon }) => {
          const isActive = active === key
          return (
            <div key={key} className="relative group">
              <button
                onClick={() => onNavigate(key)}
                className={`w-full flex items-center gap-3 pl-3 pr-3 py-2.5 rounded-xl text-sm transition-all
                  ${isActive
                    ? 'bg-accent/10 text-accent font-medium'
                    : 'text-text-dim hover:bg-surface hover:text-text'
                  }`}
              >
                {/* Indicador de ativo — borda esquerda */}
                {isActive && (
                  <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-accent rounded-full" />
                )}
                <Icon size={17} className="flex-shrink-0" />
                {expanded && (
                  <motion.span
                    initial={false}
                    animate={{ opacity: 1 }}
                    className="whitespace-nowrap truncate leading-none"
                  >
                    {label}
                  </motion.span>
                )}
              </button>
              {/* Tooltip quando recolhido */}
              {!expanded && (
                <div className="pointer-events-none absolute left-14 top-1/2 -translate-y-1/2 z-50
                  bg-[#1a2035] border border-border rounded-lg px-2.5 py-1.5 text-xs text-text
                  whitespace-nowrap shadow-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                  {label}
                </div>
              )}
            </div>
          )
        })}
      </nav>

      {/* Rodapé com status + logout */}
      <div className="p-3 border-t border-border/40 space-y-2">
        {expanded && username && (
          <p className="font-mono text-[10px] text-text-muted truncate px-1">
            {username}
            {' · '}
            <span className={role === 'administrador' ? 'text-accent' : 'text-text-dim'}>
              {roleLabel}
            </span>
          </p>
        )}

        <div className="flex items-center gap-2 min-w-0">
          <ConnectionBadge connected={connected} animate size={9} />
          {expanded && (
            <span className="font-mono text-[10px] text-text-muted truncate leading-none flex-1">
              {host || 'sem conexão'}
            </span>
          )}

          <button
            onClick={onLogout}
            title="Sair"
            className="p-1 rounded-lg text-text-muted hover:text-error hover:bg-surface transition-colors flex-shrink-0"
          >
            <LogOut size={13} />
          </button>
        </div>
      </div>
    </motion.aside>
  )
}
