const SERVER = 'http://192.168.0.118:5000'

async function getToken() {
  return new Promise(resolve => {
    chrome.storage.local.get(['ff_token'], r => resolve(r.ff_token || null))
  })
}

async function apiGet(path) {
  const token = await getToken()
  if (!token) return { error: 'Não autenticado. Configure o login na extensão.' }
  try {
    const r = await fetch(`${SERVER}/api${path}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (r.status === 401) {
      chrome.storage.local.remove(['ff_token'])
      return { error: 'Sessão expirada. Faça login novamente na extensão.' }
    }
    return await r.json()
  } catch (e) {
    return { error: 'Servidor indisponível. Verifique se o assistente está rodando.' }
  }
}

async function login(username, password) {
  try {
    const r = await fetch(`${SERVER}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    const data = await r.json()
    if (data.token) {
      await chrome.storage.local.set({
        ff_token:    data.token,
        ff_username: data.username,
        ff_role:     data.role || 'analista',
      })
      return { ok: true, username: data.username }
    }
    return { error: data.error || 'Credenciais inválidas' }
  } catch (e) {
    return { error: 'Servidor indisponível.' }
  }
}

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === 'GET_CONTEXT') {
    apiGet(`/cliente-contexto?ticket_id=${msg.ticketId}`)
      .then(sendResponse)
    return true
  }
  if (msg.type === 'LOGIN') {
    login(msg.username, msg.password).then(sendResponse)
    return true
  }
  if (msg.type === 'LOGOUT') {
    chrome.storage.local.remove(['ff_token', 'ff_username', 'ff_role'])
    sendResponse({ ok: true })
    return true
  }
  if (msg.type === 'GET_AUTH') {
    chrome.storage.local.get(['ff_token', 'ff_username', 'ff_role'], r => {
      sendResponse({ token: r.ff_token, username: r.ff_username, role: r.ff_role })
    })
    return true
  }
})
