import axios from 'axios'

const BASE = `http://${window.location.hostname}:5000/api`

const instance = axios.create({
  baseURL: BASE,
  timeout: 60000,
})

// Injeta token Bearer em todas as requisições
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('erp_token')
  if (token) config.headers['Authorization'] = 'Bearer ' + token
  return config
})

const api = {
  // Saúde
  health: () =>
    instance.get('/health'),

  // Autenticação
  login: (username, password) =>
    instance.post('/login', { username, password }),

  logout: () =>
    instance.post('/logout'),

  me: () =>
    instance.get('/me'),

  // Usuários (admin)
  users: () =>
    instance.get('/users'),

  createUser: (username, password, is_admin, must_change_password, role) =>
    instance.post('/users', { username, password, is_admin, must_change_password, role }),

  setMustChangePassword: (username, value) =>
    instance.put('/users/' + username + '/must_change_password', { value }),

  deleteUser: (username) =>
    instance.delete('/users/' + username),

  changePassword: (username, password) =>
    instance.put('/users/' + username + '/password', { password }),

  setAdmin: (username, is_admin) =>
    instance.put('/users/' + username + '/admin', { is_admin }),

  setRole: (username, role) =>
    instance.put('/users/' + username + '/role', { role }),

  // Bancos pré-configurados
  databases: () =>
    instance.get('/databases'),

  // Conexão e scan
  connect: (host, database) =>
    instance.post('/connect', { host, database }),

  scanStatus: () =>
    instance.get('/scan/status'),

  scan: () =>
    instance.post('/scan'),

  // Chat
  chat: (mensagem, historico, imagem, model) =>
    instance.post('/chat', { mensagem, historico, imagem, model }, { timeout: 120000 }),

  // Execução de query
  executarQuery: (sql) =>
    instance.post('/query', { sql }, { timeout: 30000 }),

  // Print
  capturarTela: () =>
    instance.post('/screenshot', {}, { timeout: 15000 }),

  analisarPrint: (imagemBase64, descricao) =>
    instance.post('/analyze-print', { imagem: imagemBase64, descricao }, { timeout: 120000 }),

  // Log
  analisarLog: (log, contexto) =>
    instance.post('/analyze-log', { log, contexto }, { timeout: 120000 }),

  // XML
  analisarXml: (numero_nota, tipo, data_ref, caminho) =>
    instance.post('/analyze-xml', { numero_nota, tipo, data_ref, caminho }, { timeout: 120000 }),

  analisarXmlUpload: (xmlUpload, tipo) =>
    instance.post('/analyze-xml', { xml_upload: xmlUpload, tipo }, { timeout: 120000 }),

  // Perfil
  perfil: () =>
    instance.get('/profile'),

  // Tokens
  tokens: () =>
    instance.get('/tokens'),

  // Memória
  getMemory: () =>
    instance.get('/memory'),

  addMemory: (content, category = 'geral') =>
    instance.post('/memory', { content, category }),

  // Gestão — Movidesk
  gestaoSync: (date_from, date_to) =>
    instance.post('/gestao/sync', { date_from, date_to }),

  gestaoSyncStatus: () =>
    instance.get('/gestao/sync/status'),

  gestaoExtract: (opts = {}) =>
    instance.post('/gestao/extract', opts),

  gestaoStats: (date_from, date_to, analista = '', categoria = '', grupo = '') =>
    instance.get('/gestao/stats', { params: { date_from, date_to, analista, categoria, grupo } }),

  gestaoFilters: () =>
    instance.get('/gestao/filters'),

  gestaoTickets: ({ page = 0, search = '', analista = '', categoria = '', date_from, date_to } = {}) =>
    instance.get('/gestao/tickets', { params: { page, search, analista, categoria, date_from, date_to } }),

  gestaoSimilar: (subject, client_name = '') =>
    instance.post('/gestao/similar', { subject, client_name }),

  gestaoAnalistaView: () =>
    instance.get('/gestao/analista-view'),

  gestaoRespostasRapidas: () =>
    instance.get('/gestao/respostas-rapidas'),

  gestaoDuplicados: (soAbertos = true, grupo = '') =>
    instance.get('/gestao/duplicados', { params: { abertos: soAbertos, grupo: grupo || undefined } }),

  gestaoSyncMetaHistorico: (monthsBack = 3) =>
    instance.post('/gestao/sync-meta-historico', { months_back: monthsBack }),

  gestaoSyncAbertos: () =>
    instance.post('/gestao/sync-abertos'),

  gestaoChecklists: () =>
    instance.get('/gestao/checklists'),

  setMovideskName: (username, movidesk_name) =>
    instance.put('/users/' + username + '/movidesk_name', { movidesk_name }),

  gestaoAnalise: (date_from, date_to) =>
    instance.post('/gestao/analise', { date_from, date_to }, { timeout: 120000 }),

  gestaoIaChat: (pergunta, historico = [], date_from, date_to) =>
    instance.post('/gestao/ia-chat', { pergunta, historico, date_from, date_to }, { timeout: 120000 }),

  gestaoAderencia: (date_from, date_to) =>
    instance.get('/gestao/aderencia', { params: { date_from, date_to } }),

  gestaoMetas: (semanasAlvo = 4) =>
    instance.get('/gestao/metas', { params: { semanas_alvo: semanasAlvo } }),

  gestaoMetasAnalise: (grupo, semanasAlvo = 4) =>
    instance.post('/gestao/metas-analise', { grupo, semanas_alvo: semanasAlvo }, { timeout: 120000 }),

  gestaoSazonalidade: (date_from, date_to, agrupamento = 'semana', grupo = '') =>
    instance.get('/gestao/sazonalidade', { params: { date_from, date_to, agrupamento, grupo } }),

  gestaoSazonalidadeAnalise: (date_from, date_to, agrupamento = 'semana', grupo = '') =>
    instance.post('/gestao/sazonalidade-analise', { date_from, date_to, agrupamento, grupo }, { timeout: 120000 }),

  gestaoNovaVersao: () =>
    instance.get('/gestao/nova-versao'),

  movideskAnalistas: () =>
    instance.get('/movidesk-analistas'),

  // Tarefas — leitura Jira (somente visualização, nunca escrever)
  tarefas: () =>
    instance.get('/tarefas'),

  tarefaDetail: (key) =>
    instance.get('/tarefas/' + key + '/detail'),

  analisarTarefa: (key) =>
    instance.post('/tarefas/' + key + '/analisar', {}, { timeout: 120000 }),

  listCorrections: () =>
    instance.get('/knowledge-corrections'),

  addCorrection: (data) =>
    instance.post('/knowledge-corrections', data),

  deleteCorrection: (id) =>
    instance.delete('/knowledge-corrections/' + id),

  // Provedores NFS-e
  provedorStatus: () =>
    instance.get('/provedor/status', { timeout: 30000 }),

  provedorAtualizarIni: () =>
    instance.post('/provedor/atualizar-ini'),

  provedorAtualizarJira: () =>
    instance.post('/provedor/atualizar-jira', {}, { timeout: 60000 }),

  gestaoAbertosHoje: () =>
    instance.get('/gestao/abertos-hoje'),

  // TV auto-login
  tvLogin: (key) =>
    instance.get('/tv-login', { params: { key } }),

  // Painel TV — Metas & Desempenho (lideres + admin)
  painelSemanal: () =>
    instance.get('/painel/semanal', { timeout: 30000 }),

  painelResetCache: () =>
    instance.post('/painel/reset-cache'),
}

export default api
