const $ = id => document.getElementById(id)

function showLogin()  { $('view-login').style.display = ''; $('view-logged').style.display = 'none' }
function showLogged(username) {
  $('view-login').style.display = 'none'
  $('view-logged').style.display = ''
  $('lbl-user').textContent = username || '—'
}

// Verifica estado inicial
chrome.runtime.sendMessage({ type: 'GET_AUTH' }, r => {
  if (r?.token) showLogged(r.username)
  else showLogin()
})

// Login
$('btn-login').addEventListener('click', async () => {
  const user = $('inp-user').value.trim()
  const pass = $('inp-pass').value
  if (!user || !pass) return
  $('btn-login').textContent = 'Entrando...'
  $('btn-login').disabled = true
  $('login-error').style.display = 'none'

  chrome.runtime.sendMessage({ type: 'LOGIN', username: user, password: pass }, r => {
    $('btn-login').textContent = 'Entrar'
    $('btn-login').disabled = false
    if (r?.ok) {
      showLogged(r.username)
    } else {
      $('login-error').textContent = r?.error || 'Erro ao fazer login.'
      $('login-error').style.display = 'block'
    }
  })
})

// Enter no campo de senha
$('inp-pass').addEventListener('keydown', e => {
  if (e.key === 'Enter') $('btn-login').click()
})

// Logout
$('btn-logout').addEventListener('click', () => {
  chrome.runtime.sendMessage({ type: 'LOGOUT' }, () => showLogin())
})
