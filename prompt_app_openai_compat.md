# Prompt para Claude Code — ERP Assistant (OpenAI Compatibility Layer)

Crie um aplicativo desktop completo chamado **ERP Assistant** — IDÊNTICO ao projeto
anterior, com a única diferença sendo o cliente de IA: em vez da Anthropic SDK,
usar a biblioteca OpenAI apontando para o endpoint local do Claude Code.

---

## ⚠️ DIFERENÇA PRINCIPAL — CLIENTE DE IA

### ANTES (Anthropic SDK — NÃO usar):
```python
import anthropic
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    system="...",
    messages=[...]
)
texto = response.content[0].text
```

### AGORA (OpenAI SDK apontando para Claude Code — USAR):
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="sk-ba3858d046b68de6-c258d1-0a3ea5e4"
)

response = client.chat.completions.create(
    model="cc/claude-sonnet-4-5-20250929",  # prefixo "cc/" = Claude Code
    messages=[
        {"role": "system", "content": "..."},   # system vira primeira mensagem
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
        {"role": "user", "content": "..."},
    ]
)

texto = response.choices[0].message.content
```

**ATENÇÃO às diferenças de API:**
- `system` não é parâmetro separado — vai como primeira mensagem com `role: "system"`
- Resposta fica em `response.choices[0].message.content` (não em `response.content[0].text`)
- Não há `cache_control` — remover qualquer referência a prompt caching
- `max_tokens` vira `max_completion_tokens` (ou manter `max_tokens` — ambos funcionam)
- Não instalar `anthropic` — instalar `openai`

---

## CONFIGURAÇÃO FIXA

```python
# config.py
OPENAI_BASE_URL = "http://localhost:20128/v1"
OPENAI_API_KEY  = "sk-ba3858d046b68de6-c258d1-0a3ea5e4"
MODEL           = "cc/claude-sonnet-4-5-20250929"  # nome completo com data
```

Esses valores são FIXOS no código — não vêm de `.env` nem de variável de ambiente.
O endpoint `localhost:20128` é o Claude Code rodando localmente na máquina.

---

## CLIENTE DE IA — `ai/client.py`

```python
from openai import OpenAI
from config import OPENAI_BASE_URL, OPENAI_API_KEY, MODEL
import base64

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)


def ask(system_prompt, messages, image_base64=None):
    """
    Envia mensagem para o Claude via OpenAI compatibility layer.
    O system prompt vira a primeira mensagem com role='system'.
    """
    # Montar lista completa de mensagens
    msgs = [{"role": "system", "content": system_prompt}]

    # Adicionar histórico
    for msg in messages:
        if image_base64 and msg == messages[-1]:
            # Última mensagem com imagem
            msgs.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/png;base64," + image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": msg["content"]
                    }
                ]
            })
        else:
            msgs.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=2048,
        messages=msgs
    )

    return response.choices[0].message.content


def classify_query(sql):
    """SELECT/WITH = seguro. Qualquer outro = requer confirmacao."""
    sql_upper = sql.strip().upper()
    if sql_upper.startswith("SELECT") or sql_upper.startswith("WITH"):
        return "SELECT"
    return "MODIFY"


def extract_queries(ai_response):
    """Extrai todas as queries SQL da resposta da IA."""
    import re
    queries = re.findall(r'```sql\n(.*?)\n```', ai_response, re.DOTALL)
    result = []
    for q in queries:
        result.append({
            "sql": q.strip(),
            "type": classify_query(q)
        })
    return result
```

---

## RESTO DO PROJETO — IDÊNTICO AO ANTERIOR

Todo o restante do projeto deve ser EXATAMENTE igual ao ERP Assistant já
implementado. Apenas o cliente de IA muda. Implementar tudo:

---

### COMPATIBILIDADE WINDOWS

O app DEVE rodar nos seguintes sistemas operacionais Windows sem dependências externas:

| Sistema | Suporte |
|---|---|
| Windows XP SP3 (32-bit) | ✅ |
| Windows 7 (32-bit e 64-bit) | ✅ |
| Windows 10 (32-bit e 64-bit) | ✅ |
| Windows Server 2003/2008/2012/2016 | ✅ |

Regras obrigatórias:
- Usar Python 3.8.x como alvo
- NUNCA usar f-strings — usar `.format()` ou `%`
- NUNCA usar `asyncio` — usar `threading` puro
- NUNCA usar `pathlib` em caminhos críticos — usar `os.path`
- Usar `tkinter` para interface (já vem no Python, funciona no XP)
- O `.exe` gerado pelo PyInstaller deve ser único (`--onefile`)

---

### CREDENCIAIS DO BANCO

```python
DB_USER     = "sistema"
DB_PASSWORD = "sistemafarmafacil123"
DB_PORT     = 5432
```

Fixas no código, não editáveis pelo cliente.
O cliente informa apenas IP/Hostname e nome do banco.

---

### REGRA DE OURO — NUNCA EXECUTAR UPDATE/DELETE SEM CONFIRMAÇÃO

- SELECT: executar automaticamente
- UPDATE / DELETE / INSERT: SEMPRE exibir dialog de confirmação antes
- Dialog deve mostrar: faixa amarela de aviso, query completa, botão EXECUTAR (vermelho) e Cancelar
- Após execução, registrar em `query_log.txt`

---

### ESTRUTURA DE ARQUIVOS

```
erp_assistant/
├── main.py
├── config.py
├── db/
│   ├── connector.py
│   └── scanner.py
├── ai/
│   ├── client.py            ← ÚNICO ARQUIVO DIFERENTE (usa OpenAI SDK)
│   ├── context_builder.py
│   └── prompts.py
├── ui/
│   ├── app_window.py
│   ├── chat_tab.py
│   ├── print_tab.py
│   ├── profile_tab.py
│   ├── confirm_dialog.py
│   └── setup_dialog.py
├── utils/
│   ├── screenshot.py
│   ├── profile_cache.py
│   └── query_log.py
├── requirements.txt
└── build.spec
```

---

### `config.py` COMPLETO

```python
import os

# ============================================================
# CLIENTE DE IA — OpenAI Compatibility Layer (Claude Code)
# ============================================================
OPENAI_BASE_URL = "http://localhost:20128/v1"
OPENAI_API_KEY  = "sk-ba3858d046b68de6-c258d1-0a3ea5e4"
MODEL           = "cc/claude-sonnet-4-5-20250929"  # nome completo com data

# ============================================================
# CREDENCIAIS DO BANCO — FIXAS, NAO EXPOR AO CLIENTE
# ============================================================
DB_USER     = "sistema"
DB_PASSWORD = "sistemafarmafacil123"
DB_PORT     = 5432

# ============================================================
# APP
# ============================================================
APP_NAME            = "ERP Assistant"
APP_VERSION         = "1.0.0"
PROFILE_FILE        = "client_profile.json"
CONNECTION_FILE     = "connection.json"
QUERY_LOG_FILE      = "query_log.txt"
SCAN_INTERVAL_HOURS = 24
MAX_CHAT_HISTORY    = 20
```

---

### `requirements.txt`

```
# Versoes compativeis com Windows XP/7/10/Server
openai>=1.0.0
psycopg2==2.8.6
Pillow==6.2.2
pyautogui==0.9.50
python-dotenv>=0.19.0
pyinstaller==4.10
```

**IMPORTANTE:** NÃO incluir `anthropic` nas dependências. Usar apenas `openai`.

---

### SCANNER DO BANCO — `db/scanner.py`

Ao conectar, executar as seguintes queries (cada uma em try/except individual):

```sql
SELECT chave, valor FROM configuracoes
WHERE chave IN ('razao_social','cnpj','versao_sistema',
                'regime_tributario','uf','cidade','ultimo_backup')

SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position

SELECT schemaname, tablename, n_live_tup AS registros
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC LIMIT 30

SELECT version()

SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10

SELECT count(*), state FROM pg_stat_activity GROUP BY state

SELECT count(*) FROM pg_locks WHERE NOT granted

SELECT * FROM log_erros ORDER BY data_hora DESC LIMIT 20

SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'nfe','nfce','nfs',
    'ordem_producao','producao',
    'estoque','produto','movimentacao',
    'conta_pagar','conta_receber',
    'funcionario','folha_pagamento',
    'pedido','venda','orcamento'
)
```

---

### CONTEXT BUILDER — `ai/context_builder.py`

```python
import os

def load_knowledge_base():
    """Carrega base de conhecimento do Farmafacil se existir."""
    caminhos = [
        "farmafacil_knowledge.md",
        os.path.join(os.path.dirname(__file__), "..", "farmafacil_knowledge.md"),
    ]
    for path in caminhos:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return ""


def build_system_prompt(profile):
    knowledge = load_knowledge_base()

    knowledge_section = ""
    if knowledge:
        knowledge_section = "\n## Base de Conhecimento do Farmafacil\n{0}\n".format(knowledge)

    return (
        "Voce e um assistente tecnico especialista em sistemas ERP de gestao empresarial.\n"
        "Voce esta conectado ao banco de dados do cliente e tem acesso completo ao contexto.\n"
        "Responda SEMPRE em portugues brasileiro. Seja tecnico mas acessivel.\n"
        "\n"
        "## REGRAS ABSOLUTAS DE SEGURANCA\n"
        "1. Voce PODE sugerir e executar queries SELECT automaticamente.\n"
        "2. Voce PODE sugerir UPDATE, DELETE ou INSERT quando necessario.\n"
        "3. Voce NUNCA executa UPDATE/DELETE/INSERT diretamente — apenas sugere.\n"
        "4. O sistema exibira um dialog de confirmacao antes de qualquer modificacao.\n"
        "5. Sempre explique o que a query ira modificar ANTES de sugeri-la.\n"
        "6. Se houver risco de perda de dados, avise com destaque: ATENCAO.\n"
        "\n"
        "{knowledge_section}"
        "\n"
        "## Dados do Cliente\n"
        "Empresa: {razao_social}\n"
        "CNPJ: {cnpj}\n"
        "Cidade: {cidade} / {uf}\n"
        "Regime Tributario: {regime_tributario}\n"
        "Versao do Sistema: {versao_sistema}\n"
        "Versao do PostgreSQL: {versao_postgres}\n"
        "Ultimo Backup: {ultimo_backup}\n"
        "\n"
        "## Modulos Ativos\n"
        "{modulos_detectados}\n"
        "\n"
        "## Schema do Banco\n"
        "{schema_resumido}\n"
        "\n"
        "## Volumes de Dados\n"
        "{volumes}\n"
        "\n"
        "## Erros Recorrentes\n"
        "{erros_recorrentes}\n"
        "\n"
        "## Queries Lentas\n"
        "{queries_lentas}\n"
        "\n"
        "## Instrucoes\n"
        "- Para perguntas sobre dados: gere SELECT e execute para trazer resposta real\n"
        "- Para erros de tela: analise a imagem, cruze com o schema, explique a causa raiz\n"
        "- Para lentidao: verifique pg_stat_activity e pg_locks\n"
        "- Para erros de versao: compare versao instalada com comportamento esperado\n"
        "- Para producao/estoque/financeiro: consulte tabelas relevantes\n"
        "- Se identificar problema critico: alerte com ATENCAO em destaque\n"
        "- Ao sugerir UPDATE/DELETE, explique linha a linha o que sera modificado\n"
    ).format(
        knowledge_section=knowledge_section,
        razao_social=profile.get("razao_social", "Nao identificado"),
        cnpj=profile.get("cnpj", ""),
        cidade=profile.get("cidade", ""),
        uf=profile.get("uf", ""),
        regime_tributario=profile.get("regime_tributario", ""),
        versao_sistema=profile.get("versao_sistema", ""),
        versao_postgres=profile.get("versao_postgres", ""),
        ultimo_backup=profile.get("ultimo_backup", ""),
        modulos_detectados=profile.get("modulos_detectados", ""),
        schema_resumido=profile.get("schema_resumido", ""),
        volumes=profile.get("volumes", ""),
        erros_recorrentes=profile.get("erros_recorrentes", ""),
        queries_lentas=profile.get("queries_lentas", ""),
    )
```

---

### INTERFACE GRÁFICA — `ui/`

Usar **tkinter** com ttk. Compatível com Windows XP. Layout com abas:

**Aba 1 — Chat**
- Área de mensagens com scroll
- Mensagens do usuário: fundo azul claro
- Mensagens da IA: fundo cinza claro
- Queries SELECT executadas: fundo verde claro + resultado em tabela
- Queries MODIFY sugeridas: fundo amarelo + botão "Executar (requer confirmação)"
- Campo de input + botão Enviar + Enter para enviar
- Indicador "Aguardando IA..." com barra de progresso durante chamada

**Aba 2 — Analisar Print**
- Botão "Capturar tela agora"
- Preview miniatura da imagem (max 400x300px)
- Campo "Descreva o problema (opcional)"
- Botão "Analisar com IA"
- Área de resultado com scroll
- Atalho Ctrl+Shift+P captura e inicia análise

**Aba 3 — Perfil do Cliente**
- Dados da empresa em cards
- Módulos detectados: ativo/não encontrado
- Top 10 tabelas por volume
- Erros recorrentes, queries lentas
- Botão "Atualizar scan agora"

**Aba 4 — Configuração**
- Campo IP/Hostname
- Campo nome do banco
- Botão "Reconectar"
- Status da conexão + log do scanner

**Barra de status (rodapé):**
- Indicador verde/vermelho: status conexão
- Nome da empresa
- Versão do sistema

---

### DIALOG DE CONFIRMAÇÃO — `ui/confirm_dialog.py`

Exibido SEMPRE que IA sugerir UPDATE/DELETE/INSERT:

```python
import tkinter as tk

class ConfirmQueryDialog(object):
    def __init__(self, parent, query, explanation):
        self.result = False
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Confirmacao necessaria")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        warn = tk.Frame(self.dialog, bg="#FFF3CD", pady=10, padx=16)
        warn.pack(fill=tk.X)
        tk.Label(
            warn,
            text="ATENCAO: Esta operacao ira modificar dados no banco.",
            bg="#FFF3CD", fg="#856404",
            font=("Arial", 10, "bold"), wraplength=460
        ).pack()

        exp = tk.Frame(self.dialog, padx=16, pady=8)
        exp.pack(fill=tk.X)
        tk.Label(exp, text="O que sera feito:", font=("Arial", 9, "bold"), anchor="w").pack(fill=tk.X)
        tk.Label(exp, text=explanation, font=("Arial", 9), wraplength=460,
                 anchor="w", justify=tk.LEFT).pack(fill=tk.X)

        qf = tk.Frame(self.dialog, padx=16, pady=4)
        qf.pack(fill=tk.X)
        tk.Label(qf, text="Query a ser executada:", font=("Arial", 9, "bold"), anchor="w").pack(fill=tk.X)
        qt = tk.Text(qf, height=6, font=("Courier New", 9), bg="#FFF8DC", relief=tk.SOLID, bd=1)
        qt.insert(tk.END, query)
        qt.config(state=tk.DISABLED)
        qt.pack(fill=tk.X)

        bf = tk.Frame(self.dialog, padx=16, pady=12)
        bf.pack(fill=tk.X)
        tk.Button(bf, text="Cancelar", width=14, command=self._cancel).pack(side=tk.RIGHT, padx=(8,0))
        tk.Button(
            bf, text="EXECUTAR", width=14,
            bg="#DC3545", fg="white", font=("Arial", 9, "bold"),
            activebackground="#C82333", activeforeground="white",
            command=self._confirm
        ).pack(side=tk.RIGHT)

        self.dialog.wait_window()

    def _confirm(self):
        self.result = True
        self.dialog.destroy()

    def _cancel(self):
        self.result = False
        self.dialog.destroy()
```

---

### CAPTURA DE TELA — `utils/screenshot.py`

```python
import base64
from io import BytesIO

def capture_screen():
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
    except Exception:
        import pyautogui
        screenshot = pyautogui.screenshot()

    from PIL import Image
    if screenshot.size[0] > 1280:
        ratio = 1280.0 / screenshot.size[0]
        new_w = 1280
        new_h = int(screenshot.size[1] * ratio)
        screenshot = screenshot.resize((new_w, new_h), Image.ANTIALIAS)

    buffer = BytesIO()
    screenshot.save(buffer, format="PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
```

---

### MÓDULO DE ANÁLISE DE XML — `modules/xml_analyzer/`

Implementar o módulo completo de diagnóstico de NF-e e NFS-e:

```
modules/xml_analyzer/
├── __init__.py
├── file_finder.py      # detecta pastas automaticamente
├── xml_reader.py       # lê e parseia XMLs
├── nfe_analyzer.py     # diagnóstico NF-e
├── nfse_analyzer.py    # diagnóstico NFS-e
└── routes.py           # rotas Flask
```

**Caminhos de busca NF-e (cascata):**
```python
CAMINHOS_NFE = [
    r"C:\PharmaFacil\NFE",
    r"C:\FarmaFacil\NFE",
    os.path.join("C:\\Users", usuario, "PharmaFacil", "NFE"),
    os.path.join("C:\\Users", usuario, "FarmaFacil", "NFE"),
    os.path.join("C:\\Users", usuario, "AppData", "Local", "PharmaFacil", "NFE"),
]
```

**Caminhos NFS-e:**
```python
# Base XZ, busca subpasta com data mais recente (YYYY-MM)
# dentro da data: /envio e /retorno
BASES_XZ = [
    os.path.join("C:\\Users", usuario, "FarmaFacil", "EXE", "XZ"),
    os.path.join("C:\\Users", usuario, "PharmaFacil", "EXE", "XZ"),
    r"C:\FarmaFacil\EXE\XZ",
]
```

**Config ACBr:**
```python
CAMINHOS_ACBR = [
    r"C:\FarmaFacil\EXE\ACBr\servicos.xml.n",
    os.path.join("C:\\Users", usuario, "FarmaFacil", "EXE", "ACBr", "servicos.xml.n"),
]
```

**No analyzer, usar o cliente OpenAI:**
```python
from openai import OpenAI
from config import OPENAI_BASE_URL, OPENAI_API_KEY, MODEL

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

def analisar_xml(system_prompt, conteudo):
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conteudo}
        ]
    )
    return response.choices[0].message.content
```

---

### FLUXO PRINCIPAL

```
1. App abre → verifica connection.json
   → SIM: conecta automaticamente, vai para aba Chat
   → NAO: abre dialog pedindo IP/Hostname e nome do banco

2. Conexao → scanner executa em thread separada
   → Perfil salvo em client_profile.json
   → Mensagem de boas-vindas personalizada no chat

3. Chat:
   → Context builder monta system prompt com perfil + knowledge base
   → OpenAI SDK chama localhost:20128
   → SELECT: executar automaticamente
   → UPDATE/DELETE/INSERT: ConfirmDialog obrigatório

4. Print:
   → Captura tela → envia como image_url base64
   → Diagnóstico retornado

5. XML Analyzer:
   → Detecta pastas automaticamente
   → Lê XMLs de retorno NF-e ou NFS-e
   → Envia para IA via OpenAI SDK
   → Retorna diagnóstico com causa e solução
```

---

### `build.spec` PARA PYINSTALLER

```python
a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("farmafacil_knowledge.md", "."),
        ("client_profile.json", "."),
    ],
    hiddenimports=[
        "psycopg2",
        "PIL._tkinter_finder",
        "openai",
        "tkinter",
        "tkinter.ttk",
        "tkinter.scrolledtext",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["anthropic"],  # garantir que anthropic NAO entre no bundle
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
    name="ERPAssistant",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon="icon.ico",
)
```

---

## RESUMO DAS ÚNICAS DIFERENÇAS

| Item | Versão Anthropic | Esta versão (OpenAI compat) |
|---|---|---|
| Biblioteca | `anthropic` | `openai` |
| Endpoint | `api.anthropic.com` | `http://localhost:20128/v1` |
| API Key | `sk-ant-...` (do .env) | `sk-ba3858d046b68de6-c258d1-0a3ea5e4` (fixo) |
| Model | `claude-sonnet-4-20250514` | `cc/claude-sonnet-4-5-20250929` |
| System prompt | parâmetro separado | primeira mensagem `role: system` |
| Resposta | `response.content[0].text` | `response.choices[0].message.content` |
| Prompt caching | sim | não — remover todo `cache_control` |
| Imagem | `source.type: base64` | `image_url: data:image/png;base64,...` |

---

## OBSERVAÇÕES FINAIS

- O endpoint `localhost:20128` é o Claude Code rodando como servidor local —
  ele deve estar ativo na máquina para o app funcionar
- Todo o restante (banco PostgreSQL, scanner, interface, confirmação de queries,
  módulo XML, base de conhecimento) é IDÊNTICO ao projeto anterior
- NÃO instalar `anthropic` — apenas `openai`
- NÃO usar `.env` para API key — valores fixos em `config.py`
- Threading obrigatório para todas as chamadas à IA e ao banco

---

## ENTREGÁVEIS ESPERADOS

1. Todos os arquivos do projeto completos e funcionais
2. `requirements.txt` com `openai` no lugar de `anthropic`
3. `build.spec` com `anthropic` nos excludes
4. `README.md` explicando que o Claude Code deve estar rodando na porta 20128
5. Testar chamada simples antes de implementar tudo:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:20128/v1",
                api_key="sk-ba3858d046b68de6-c258d1-0a3ea5e4")
r = client.chat.completions.create(
    model="cc/claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Ola!"}]
)
print(r.choices[0].message.content)
```

**Ordem de implementação:**
`config.py` → `ai/client.py` → `db/connector.py` → `db/scanner.py` →
`ai/context_builder.py` → `ui/confirm_dialog.py` → demais `ui/` →
`utils/` → `modules/xml_analyzer/` → `main.py` → `build.spec` → `README.md`
