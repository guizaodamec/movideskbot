const MOVIDESK_URL = 'https://prismafive.movidesk.com/Ticket/Edit/'

function getTicketId() {
  const m = location.pathname.match(/\/Ticket\/Edit\/(\d+)/i)
  return m ? m[1] : null
}

function badgeClass(versoes_atrasado) {
  if (versoes_atrasado === 0)  return 'ok'
  if (versoes_atrasado <= 2)  return 'warn'
  if (versoes_atrasado <= 5)  return 'warn'
  return 'danger'
}

function statusColor(status) {
  const s = (status || '').toLowerCase()
  if (s.includes('resolvido') || s.includes('fechado')) return '#34d399'
  if (s.includes('pausa'))  return '#fbbf24'
  if (s.includes('cancelado')) return '#6e7681'
  return '#60a5fa'
}

function renderLoading(body) {
  body.innerHTML = `
    <div class="ff-spinner">
      <div class="ff-dot"></div>
      <div class="ff-dot"></div>
      <div class="ff-dot"></div>
      Carregando...
    </div>`
}

function renderError(body, msg) {
  body.innerHTML = `<div class="ff-error">${msg}</div>`
}

function renderData(body, data, ticketId) {
  const v = data.versao || {}
  const t = data.ticket || {}
  const chamados = data.chamados_recentes || []
  const bugs = data.bugs_jira || []

  const atraso = v.versoes_atrasado ?? -1
  const bClass = atraso >= 0 ? badgeClass(atraso) : 'muted'
  const atrasoLabel = atraso === 0 ? 'Na versão atual' :
                      atraso > 0  ? `${atraso} versão${atraso>1?'s':''} atrás` : '—'

  const atrasoBarColor = atraso === 0 ? '#34d399' : atraso <= 2 ? '#fbbf24' : atraso <= 5 ? '#f97316' : '#ef4444'
  const maxAtraso = 20
  const barPct = Math.min((atraso / maxAtraso) * 100, 100)

  body.innerHTML = `
    <!-- Chamado -->
    <div class="ff-section">
      <div class="ff-section-title">Chamado #${t.id}</div>
      <div class="ff-row">
        <span class="ff-label">Status</span>
        <span class="ff-value" style="color:${statusColor(t.status)}">${t.status || '—'}</span>
      </div>
      <div class="ff-row">
        <span class="ff-label">Analista</span>
        <span class="ff-value">${t.analista || '—'}</span>
      </div>
      <div class="ff-row">
        <span class="ff-label">Categoria</span>
        <span class="ff-value">${t.categoria || '—'}</span>
      </div>
    </div>

    <!-- Versão -->
    <div class="ff-section">
      <div class="ff-section-title" style="display:flex;justify-content:space-between">
        <span>Versão do Cliente</span>
        <button class="ff-refresh-btn" id="ff-refresh">↻ Atualizar</button>
      </div>
      ${v.encontrado ? `
        <div class="ff-row">
          <span class="ff-label">Versão atual</span>
          <span class="ff-badge ${bClass}">${v.versao || '?'}</span>
        </div>
        <div class="ff-row">
          <span class="ff-label">Sistema</span>
          <span class="ff-value">${v.versao_atual_sistema || '—'}</span>
        </div>
        <div class="ff-row">
          <span class="ff-label">Situação</span>
          <span class="ff-value" style="color:${atrasoBarColor}">${atrasoLabel}</span>
        </div>
        ${atraso > 0 ? `
          <div class="ff-atraso-bar">
            <div class="ff-atraso-fill" style="width:${barPct}%;background:${atrasoBarColor}"></div>
          </div>` : ''}
        <div class="ff-row" style="margin-top:6px">
          <span class="ff-label">Última atualização</span>
          <span class="ff-value">${v.ultima_atualizacao ? v.ultima_atualizacao.slice(0,10) : '—'}</span>
        </div>
      ` : `<div style="color:#6e7681;font-size:11px;margin-top:4px">
        ${v.erro ? 'Erro ao consultar o banco.' : 'Cliente não encontrado no Avalon.'}
      </div>`}
    </div>

    <!-- Chamados recentes -->
    <div class="ff-section">
      <div class="ff-section-title">Últimos chamados do cliente</div>
      ${chamados.length === 0
        ? `<div style="color:#6e7681;font-size:11px">Nenhum chamado no cache local.</div>`
        : chamados.map(c => `
          <div class="ff-card">
            <div class="ff-card-title">
              <a class="ff-link" href="${MOVIDESK_URL}${c.id}" target="_blank">#${c.id}</a>
              ${c.assunto}
            </div>
            <div class="ff-card-meta">
              <span style="color:${statusColor(c.status)}">${c.status}</span>
              · ${c.analista || '—'}
              · ${c.data || '—'}
            </div>
          </div>`).join('')
      }
    </div>

    <!-- Bugs Jira abertos -->
    <div class="ff-section">
      <div class="ff-section-title">Bugs abertos no Jira</div>
      ${bugs.length === 0
        ? `<div style="color:#6e7681;font-size:11px">Nenhum bug aberto no momento.</div>`
        : bugs.map(b => `
          <div class="ff-card">
            <div class="ff-card-title">
              <span style="color:#6e7681;font-size:10px">${b.key}</span>
              ${b.titulo}
            </div>
            <div class="ff-card-meta">
              <span style="color:${b.prioridade?.toLowerCase().includes('high')||b.prioridade?.toLowerCase().includes('blocker')?'#f87171':'#fbbf24'}">${b.prioridade || ''}</span>
              · ${b.tipo || 'Bug'}
              · ${b.atualizado || '—'}
            </div>
          </div>`).join('')
      }
    </div>

    <!-- Link abrir assistente -->
    <div style="margin-top:8px;padding-top:10px;border-top:1px solid #1e2535;text-align:center">
      <a class="ff-link" href="http://192.168.0.118:5000" target="_blank">
        Abrir FarmaFacil Assistente ↗
      </a>
    </div>
  `

  document.getElementById('ff-refresh')?.addEventListener('click', () => {
    loadContext(ticketId, true)
  })
}

let _panel = null
let _toggle = null
let _currentTicket = null

function createPanel() {
  _panel = document.createElement('div')
  _panel.id = 'ff-panel'
  _panel.innerHTML = `
    <div id="ff-header">
      <div>
        <h3>FarmaFacil Assistente</h3>
        <div class="ff-sub" id="ff-client-name">Carregando...</div>
      </div>
    </div>
    <div id="ff-body"></div>`
  document.body.appendChild(_panel)

  _toggle = document.createElement('button')
  _toggle.id = 'ff-toggle'
  _toggle.title = 'FarmaFacil Assistente'
  _toggle.textContent = '⚕'
  _toggle.addEventListener('click', () => {
    _panel.classList.toggle('open')
    if (_panel.classList.contains('open') && _currentTicket) {
      loadContext(_currentTicket)
    }
  })
  document.body.appendChild(_toggle)
}

function loadContext(ticketId, forceRefresh = false) {
  const body = document.getElementById('ff-body')
  if (!body) return
  renderLoading(body)

  chrome.runtime.sendMessage({ type: 'GET_CONTEXT', ticketId }, (resp) => {
    if (chrome.runtime.lastError) {
      renderError(body, 'Erro de comunicação com a extensão.')
      return
    }
    if (resp?.error) {
      renderError(body, resp.error)
      return
    }
    const clientEl = document.getElementById('ff-client-name')
    if (clientEl) {
      clientEl.textContent = resp.ticket?.cliente || '—'
    }
    renderData(body, resp, ticketId)
  })
}

function init() {
  const ticketId = getTicketId()
  if (!ticketId) return
  _currentTicket = ticketId
  createPanel()
}

// Detecta navegação SPA (Movidesk é SPA)
let _lastUrl = location.href
const observer = new MutationObserver(() => {
  if (location.href !== _lastUrl) {
    _lastUrl = location.href
    const id = getTicketId()
    if (id && id !== _currentTicket) {
      _currentTicket = id
      if (_panel?.classList.contains('open')) loadContext(id)
    }
  }
})
observer.observe(document.body, { childList: true, subtree: true })

init()
