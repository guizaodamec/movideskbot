# ERP Assistant AI

Assistente tecnico com IA para sistemas de gestao (ERP). Conecta ao banco PostgreSQL do cliente, escaneia o contexto e oferece diagnostico em linguagem natural com suporte a analise de prints de tela.

---

## Versoes de Python recomendadas

| Sistema Alvo          | Python recomendado       |
|-----------------------|--------------------------|
| Windows 10 / 11       | Python 3.8+ (qualquer)   |
| Windows 7 (64-bit)    | Python 3.8.x             |
| Windows 7 (32-bit)    | Python 3.8.x (32-bit)    |
| Windows XP SP3        | Python 3.4.x (build esp) |
| Windows Server 2008+  | Python 3.8.x             |

> Para Windows XP use builds especiais de Python 3.4 disponíveis em repositorios de terceiros.

---

## Configuracao rapida

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar a API Key

```bash
cp .env.example .env
# Edite .env e coloque sua ANTHROPIC_API_KEY
```

### 3. Rodar o app

```bash
python main.py
```

---

## Login padrao

| Campo    | Valor           |
|----------|-----------------|
| Usuario  | GUILHERME       |
| Senha    | Flamengo135@    |
| Perfil   | Administrador   |

O administrador pode criar, excluir e gerenciar outros usuarios na aba "Usuarios".

---

## Funcionalidades

- **Chat com IA** — Pergunte sobre qualquer aspecto do ERP em linguagem natural
- **Analise de Print** — Capture a tela (Ctrl+Shift+P) e a IA diagnostica o problema
- **Perfil do Cliente** — Visualize modulos, volumes, erros e queries lentas
- **Configuracao** — Reconecte ao banco sem reiniciar o app
- **Gerenciamento de Usuarios** — Crie/exclua usuarios e defina admins (apenas admin)

### Seguranca de dados

- SELECT: executado automaticamente para trazer dados ao chat
- UPDATE / DELETE / INSERT: **SEMPRE** exigem confirmacao explicita via dialog
- Todas as modificacoes sao registradas em `query_log.txt`

---

## Build para .exe (distribuicao)

### Pre-requisitos

```bash
pip install pyinstaller==4.10
```

### Gerar o executavel

```bash
# Colocar o .env preenchido na raiz do projeto
pyinstaller build.spec
```

O arquivo `dist/ERPAssistant.exe` sera gerado. Copie junto com o `.env`.

### Deploy no cliente

1. Copie `ERPAssistant.exe` para a maquina do cliente
2. Copie o `.env` com a API Key para a mesma pasta
3. Duplo clique em `ERPAssistant.exe` — sem instalacao

---

## Estrutura de arquivos

```
erp_assistant/
├── main.py                  # Entry point
├── config.py                # Configuracoes e credenciais fixas
├── .env                     # API Key (NAO commitar)
├── .env.example             # Modelo do .env
├── requirements.txt
├── build.spec               # PyInstaller
├── db/
│   ├── connector.py         # Conexao PostgreSQL
│   └── scanner.py           # Scan automatico do banco
├── ai/
│   ├── client.py            # Cliente Anthropic com prompt caching
│   ├── context_builder.py   # Monta system prompt com perfil
│   └── prompts.py           # Templates de prompt
├── ui/
│   ├── app_window.py        # Janela principal
│   ├── chat_tab.py          # Aba de chat
│   ├── print_tab.py         # Aba de analise de print
│   ├── profile_tab.py       # Aba de perfil do cliente
│   ├── config_tab.py        # Aba de configuracao
│   ├── users_tab.py         # Aba de usuarios (admin)
│   ├── confirm_dialog.py    # Dialog confirmacao DML
│   ├── login_dialog.py      # Tela de login
│   └── setup_dialog.py      # Dialog de conexao
└── utils/
    ├── auth.py              # Autenticacao e gestao de usuarios
    ├── screenshot.py        # Captura de tela
    ├── profile_cache.py     # Cache local do perfil
    └── query_log.py         # Log de queries modificadoras
```

---

## Credenciais do banco (fixas no codigo)

```
Usuario:  sistema
Senha:    sistemafarmafacil123
Porta:    5432
```

O cliente informa apenas o IP/Hostname e o nome do banco.

---

## Arquivos gerados em tempo de execucao

| Arquivo              | Conteudo                              |
|----------------------|---------------------------------------|
| `connection.json`    | IP e nome do banco salvos             |
| `client_profile.json`| Perfil do cliente (cache do scan)     |
| `query_log.txt`      | Log de todas as modificacoes no banco |
| `users.json`         | Usuarios do sistema                   |
