# FarmaFacil Assistente — Contexto Completo

## O que é

Assistente de IA para suporte técnico ao sistema **FarmaFácil** (ERP farmacêutico da Prismafive).
Roda localmente na rede interna da empresa. Qualquer máquina da rede acessa via browser.
Permite consultar o banco de dados do FarmaFácil em linguagem natural, analisar prints de erro
e analisar logs. A IA é a **FarmaBot** — assistente focada em analistas de suporte, inclusive os que nunca tiveram contato com farmácia.

---

## Arquitetura Geral

```
[ Browser de qualquer PC da rede ]
         |
         | HTTP  :5000
         v
[ Backend Flask — Python ]          ← iniciar_servidor.bat
    backend/main.py
    (ou dist_backend/backend.exe)
         |
         |-- Serve o frontend React (frontend/dist/)
         |-- Autentica usuários (users.json)
         |-- Conecta ao PostgreSQL do FarmaFácil
         |-- Chama a IA via OmniRoute
         |
         | HTTP  localhost:20128/v1   (OpenAI-compatible)
         v
[ OmniRoute — Node.js ]             ← npx omniroute --port 20128 --no-open
    Proxy para múltiplos backends de IA
         |
         |-- cc/claude-sonnet-4-6    (Claude Code local — PRIORIDADE 1)
         |-- kr/claude-sonnet-4.5    (Kiro — PRIORIDADE 2)
         |-- pollinations/openai     (GPT-4o — PRIORIDADE 3)
         `-- pollinations/gemini     (Gemini — PRIORIDADE 4)
```

---

## Fluxo de Inicialização

```
iniciar_servidor.bat
  1. Abre portas 5000 e 20128 no firewall do Windows
  2. Verifica/inicia OmniRoute na porta 20128
  3. Verifica se frontend/dist existe (senão faz o build)
  4. Inicia backend Flask na porta 5000
  5. Abre http://localhost:5000 no browser
```

---

## Componentes

### 1. OmniRoute (`npx omniroute --port 20128 --no-open`)
- **O que faz:** Expõe múltiplos backends de IA como API OpenAI-compatível na porta 20128
- **Autenticação CC:** Token gerado pelo OmniRoute deve ser autenticado via Claude Code local
- **Reconstrução do módulo nativo:** Se der erro 193 (arquitetura errada):
  ```
  npm rebuild better-sqlite3 --prefix "%APPDATA%\npm\node_modules\omniroute\app"
  ```
- **Expor para a rede:** Rodar `expor_ia_na_rede.bat` como administrador
  (usa `netsh portproxy` para redirecionar a porta 20128 externamente)

### 2. Backend Flask (`backend/main.py` ou `dist_backend/backend.exe`)
- **Porta:** 5000, escuta em `0.0.0.0` (aceita conexões da rede)
- **Serve:** O frontend React estático de `frontend/dist/`
- **API:** Todos os endpoints em `/api/*` com CORS aberto
- **IA endpoint:** Lê de `connection.json` → campo `ai_host` (padrão: `localhost`)

### 3. Frontend React (`frontend/src/`)
- **Build:** `cd frontend && npx vite build` → gera `frontend/dist/`
- **API URL:** Dinâmica — `http://${window.location.hostname}:5000/api`
- **Recompilar:** Necessário sempre que mudar arquivos em `frontend/src/`

---

## Configuração de IA (`config.py`)

```python
OPENAI_BASE_URL  = "http://localhost:20128/v1"
OPENAI_API_KEY   = "sk-9fd0b1b97a3a09ea-2483f0-bd7896e0"   # chave Kiro
MODEL            = "cc/claude-sonnet-4-6"                    # modelo padrão

OMNIROUTE_MODELS = [
    "cc/claude-sonnet-4-6",    # Claude Code local — prioridade 1
    "kr/claude-sonnet-4.5",    # Kiro Claude — prioridade 2
    "pollinations/openai",     # GPT-4o — prioridade 3
    "pollinations/gemini",     # Gemini — prioridade 4
]
```

### Fallback automático (`ai/client.py`)
- **429 (rate limit):** cai automaticamente para o próximo modelo sem avisar o analista
- **Outros erros** com modelo específico selecionado: para e mostra erro
- **Modelo selecionado no UI:** tenta ele primeiro; se 429, faz fallback pela lista completa
- Todos os modelos usam formato padrão OpenAI: `{"role": "system"}` nas messages + `stream=False`

### Seletor de modelo no Chat
Dropdown no UI permite escolher:
- **Claude (CC)** — `cc/claude-sonnet-4-6` — padrão
- **Kiro** — `kr/claude-sonnet-4.5`
- **GPT-4o** — `pollinations/openai`

---

## FarmaBot — Personalidade e Foco

A IA é a **FarmaBot**, assistente da equipe de suporte do FarmaFácil.

**Público-alvo:** Analistas de suporte novatos (< 1 mês de empresa, sem background em farmácia).

**Comportamento:**
- Explica termos farmacêuticos sempre que os usa (ex: "fórmula magistral = medicamento feito sob medida")
- Usa analogias do dia a dia (ex: "cadastro de fórmula é como cadastrar um produto no iFood")
- Prioriza: onde clicar, passos, erros comuns
- **NÃO gera SQL por padrão** — só quando o analista pede explicitamente
- Linguagem simples, emojis com moderação, sempre em português brasileiro
- Nunca inventa nomes de tabelas, nunca acessa arquivos/código-fonte

**Post-processamento das respostas (`backend/main.py` → `_strip_bold`):**
- Remove `**negrito**` e `*itálico*`
- Remove headers `## Título`
- Remove `---` (horizontal rules)
- Remove linhas separadoras de tabela `|---|---|`
- Converte tabelas markdown em texto limpo: cabeçalho simples + linhas `Campo: valor  Campo: valor`
- Detecta alucinações de tool-calls (`<read_code>`, `<search_code>` etc.) e substitui por mensagem honesta

---

## Base de Conhecimento

A IA busca artigos relevantes por palavras-chave e injeta até 4 artigos (máx. 6.000 chars) no contexto de cada pergunta.

**Total atual: 442 artigos carregados** (scraper + base_conhecimento + knowledge_structured + suporte_erp_kb).

### Fontes (ordem de prioridade no search)
1. **`knowledge_corrections.json`** — correções verificadas pela equipe (prioridade máxima)
2. **`base_conhecimento.json`** — 79 entradas: 63 manuais + 16 do `Resumo.odt` (prioridade alta 1.5x)
3. **`knowledge_structured.json`** — 398 artigos processados pelo `processar_kb.py` (prioridade alta 1.5x)
4. **`suporte_erp_kb.json`** — 191 artigos gerados da análise do EXE do FarmaFácil (prioridade alta 1.5x)
5. **`farmafacil_knowledge.md`** — artigos em markdown (prioridade média 1.2x)
6. **`scraper_cache.json`** — 398 artigos brutos raspados do portal Prismafive (base)

### Arquivos de Conhecimento

| Arquivo | Localização | Conteúdo |
|---|---|---|
| `scraper_cache.json` | `erp_assistant/` | 398 artigos brutos do portal (títulos, textos, alt das imagens) |
| `knowledge_structured.json` | `melhorar IA/` | 398 artigos processados pela IA (313 OK com solução) |
| `base_conhecimento.json` | `melhorar IA/` | 79 entradas dos manuais (Resumo.odt + outros .docs) |
| `suporte_erp_kb.json` | `erp_assistant/` | 191 artigos gerados pelo `converter_erp_kb.py` (análise do EXE) |
| `farmafacil_knowledge.md` | `erp_assistant/` | Base de conhecimento em markdown |
| `knowledge_corrections.json` | `erp_assistant/` | Correções manuais da equipe (prioridade máxima) |

### suporte_erp_kb.json — Domínios cobertos

Gerado automaticamente a partir da análise binária do `Prisma5_MD.exe` v20.0.90.0 e dos arquivos de configuração reais da instalação. Cobre:

| Domínio | Exemplos de artigos |
|---|---|
| **NFC-e** | Configuração, Windows 7/OpenSSL, cStat de rejeição (100/431/451/656...), contingência |
| **NF-e** | Operações, cancelamento, carta de correção, erros comuns |
| **NFS-e** | XML de configuração (todos os campos), RPS, 26 provedores, erros catalogados |
| **SNGPC/ANVISA** | Estrutura XML, fluxo de transmissão, campos obrigatórios |
| **SAT/CFe, PAF-ECF, SPED, SINTEGRA** | Configuração e erros |
| **Certificados Digitais** | A1, A3, expiração, senha, CNPJ |
| **Arquivos de config** | farmafacil.ini, confprop.ini, ELGIN.INI, nfseLocais.ini, ACBrNFSeXServicos.ini |
| **Licença** | PrismaFivePortal.Service.exe, porta 2502, diagnóstico |
| **DLLs / Portal B2B** | Pasta DLLs\\, RegistrarDLLs.exe, Entity Framework + Npgsql |
| **Produção** | Ordens, fórmulas magistrais, homeopatia (CH/DH/LM), florais, CQ, pesagem, PCP, lotes |
| **Vendas/PDV** | Fluxo de venda, caixa abertura/fechamento, sangria, problemas comuns |
| **Estoque/Compras** | Nota de entrada, inventário, estoque negativo |
| **Financeiro** | Contas, boletos (Bradesco, Banco do Brasil, Santander, Sicredi, Ailos) |
| **Cadastros** | Clientes, produtos, médicos, fornecedores |
| **Integrações** | iFood, WhatsApp, Dotz, TEF/POS, PBMs, B2B, cashback, convênios |
| **Banco de Dados** | farmafacil.ini, 100+ tabelas por módulo, diagnóstico, VACUUM, erros PostgreSQL |
| **Logs** | Localização de todos os logs (LogErro.txt, NFSe/, NFCe/, SNGPC/, ChaveFarmaFacil/) |
| **FAQ** | 35+ perguntas frequentes cobrindo todos os módulos |

### Scripts de Geração do suporte_erp_kb.json (`C:\FarmaFacil\EXE\`)

```
converter_erp_kb.py     → Lê os 5 JSONs de suporte e gera suporte_erp_kb.json
                           Entrada: suporte_fiscal.json + suporte_producao.json +
                                    suporte_geral.json + suporte_banco.json +
                                    suporte_farmafacil.json
                           Saída:   erp_assistant/suporte_erp_kb.json (191 artigos)

gerar_jsons_suporte.py  → Gera os 4 JSONs de domínio a partir de dados estruturados
                           suporte_fiscal.json (23 KB) | suporte_producao.json (10 KB)
                           suporte_geral.json (17 KB)  | suporte_banco.json (10 KB)

suporte_farmafacil.json → JSON original abrangente (67 KB, base para converter)
```

**Para regenerar o suporte_erp_kb.json após atualizar os JSONs de suporte:**
```
cd C:\FarmaFacil\EXE
python converter_erp_kb.py
```
Depois reiniciar o servidor (invalida o cache em memória — `_kb_articles` global).

### Scripts de Manutenção do Portal (`C:\Users\guilherme.cordeiro\Desktop\melhorar IA\`)

```
scraper.py          → Baixa artigos do portal Prismafive → scraper_cache.json
                      (retomável: pula artigos já baixados)

processar_kb.py     → Processa scraper_cache.json via IA → knowledge_structured.json
                      (retomável: pula artigos já processados)
                      Modelos: kr/claude-sonnet-4.5 → pollinations/openai → pollinations/gemini

processar_odt.py    → Lê Resumo.odt, divide em blocos, processa via IA
                      → adiciona ao base_conhecimento.json
```

**Para atualizar a base de conhecimento do portal:**
1. Adicionar novas URLs em `links.txt`
2. `python scraper.py` — baixa os novos artigos
3. `python processar_kb.py` — processa os novos artigos com IA
4. Reiniciar o servidor (invalida o cache em memória)

---

## Autenticação e Controle de Acesso (RBAC)

- Arquivo: `users.json` na **raiz do projeto**
- Hash: SHA-256 com salt `erp_assistant_salt_v1`
- Tokens: em memória (expiram ao reiniciar o backend)
- Login retorna: `token`, `username`, `is_admin`, `role`, `must_change_password`

### Perfis de Acesso (roles)

| Role | Páginas |
|---|---|
| `analista` | Chat, Tarefas, Gestão (tabs limitados), Provedores NFS-e |
| `backservice` | Chat, Abertos Hoje, Tarefas, Gestão, Provedores NFS-e |
| `fiscal` | Chat, Abertos Hoje, Tarefas, Gestão, Provedores NFS-e |
| `lideres` | Chat, Abertos Hoje, Tarefas, Gestão, Provedores NFS-e, Painel TV, Auditoria |
| `administrador` | Chat, Perfil, Configuração, Gestão, Usuários, Abertos Hoje, Tarefas, Provedores NFS-e, Painel TV, Auditoria |

**Páginas removidas do menu:** Analisar Print, Analisar Log, Analisar XML, Painel Analista (removidas)

**Gestão — tabs visíveis por role:**
- `analista`: Dashboard, Analistas, Farmácias, Metas + botão Sincronizar
- Demais roles: todos os tabs + Sazonalidade, Base de Chamados, Análise IA, Chat com IA, Extrair IA

**"Nova Versão" (sprint Jira)** está na aba **Tarefas**, não em Gestão.

- Somente **administrador** pode gerenciar usuários e definir roles
- Troca de senha obrigatória: `must_change_password: true` no usuário → modal abre no login

---

## Bancos de Dados Configurados

| Label | Host | Banco |
|---|---|---|
| NatuFarma Linhares | 192.168.0.121 | natufarma_linhares |
| FarmaFácil Univali | 192.168.0.102 | farmafacil_univali |
| FarmaFácil Boiron | 192.168.0.102 | farmafacil_boiron |
| Ouro FarmaCerto | 192.168.0.64 | ourofarmacerto |
| FarmaFácil São Bernardo | 192.168.0.102 | farmafacil_fasaobernardo |
| FarmaFácil (115) | 192.168.0.115 | farmafacil |
| FarmaFácil C&V | 192.168.0.102 | farmafacil_cienciaevida |
| Pronim | 127.0.0.1 | pronim |

Credenciais fixas: `sistema` / `sistemafarmafacil123` porta 5432

---

## Arquivos Importantes

```
erp_assistant/
├── tv.html                    ← Painel TV standalone (HTML puro, sem React) — acessível em /tv
├── iniciar_servidor.bat       ← ENTRADA PRINCIPAL — inicia tudo
├── expor_ia_na_rede.bat       ← Expõe OmniRoute (porta 20128) para a rede via portproxy
├── compilar_backend.bat       ← Gera dist_backend/backend.exe
├── sincronizar_chamados.py    ← Script para sync noturno do Movidesk
├── sincronizar_chamados.bat   ← Chama sincronizar_chamados.py → agendável no Windows
├── config.py                  ← Configurações globais + modelos OmniRoute + chaves
├── users.json                 ← Usuários e senhas (hash SHA-256)
├── connection.json            ← Última conexão salva (host DB + ai_host)
├── client_profile.json        ← Cache do scan do banco (schema, volumes, erros)
├── scraper_cache.json         ← 398 artigos do portal Prismafive (base bruta)
├── farmafacil_knowledge.md    ← Base de conhecimento em markdown
│
├── backend/
│   └── main.py                ← Servidor Flask (API + serve frontend + _strip_bold)
│
├── frontend/
│   ├── src/
│   │   ├── api/backend.js     ← URL da API (usa window.location.hostname)
│   │   └── pages/
│   │       ├── Login.jsx
│   │       ├── Chat.jsx             ← Seletor de modelo (CC / Kiro / GPT-4o)
│   │       ├── Setup.jsx
│   │       ├── Users.jsx
│   │       ├── ProvedorNFSe.jsx     ← Monitoramento de provedores NFS-e
│   │       ├── Gestao.jsx
│   │       ├── AbertosHoje.jsx      ← Chamados abertos no dia com filtro por grupo
│   │       └── AuditoriaContato.jsx ← Auditoria de procedimento cliente indisponível (lideres+)
│   └── dist/                  ← Build gerado pelo vite (servido pelo Flask)
│
├── ai/
│   ├── client.py              ← Fallback automático: CC → Kiro → Pollinations (429 = skip silencioso)
│   ├── prompts.py             ← System prompt FarmaBot (foco em analistas novatos, sem SQL default)
│   └── context_builder.py    ← Monta system prompt com perfil do banco
│
├── db/
│   ├── connector.py           ← Conexão PostgreSQL (psycopg2)
│   └── scanner.py             ← Scan do schema/perfil do banco
│
└── utils/
    ├── auth.py
    ├── paths.py
    ├── profile_cache.py
    ├── memory.py
    ├── screenshot.py
    ├── chat_logger.py
    ├── knowledge_search.py    ← Busca em 5 fontes: corrections > base_conhecimento > knowledge_structured > md > scraper_cache
    ├── movidesk_client.py
    ├── movidesk_sync.py
    ├── checklists.py
    └── gestao_config.py

C:\Users\guilherme.cordeiro\Desktop\melhorar IA\
├── links.txt                  ← URLs dos artigos do portal Prismafive
├── scraper.py                 ← Baixa artigos → scraper_cache.json
├── processar_kb.py            ← Processa artigos com IA → knowledge_structured.json
├── processar_odt.py           ← Processa Resumo.odt → base_conhecimento.json
├── Resumo.odt                 ← Manual técnico FarmaFácil (195K chars, 25 seções)
├── knowledge_structured.json  ← 398 artigos processados (313 OK)
└── base_conhecimento.json     ← 79 entradas dos manuais
```

---

## Features Implementadas

### Busca Web Automática (`utils/web_search.py`) — DESATIVADA

A busca web foi implementada mas está **desativada** em `backend/main.py` (bloco comentado).

**Motivo da desativação:** A integração causou alucinações graves — a IA gerava `<web_search>` XML tags e inventava notícias da SEFAZ (Resolução 130/2026, Plataforma NF-e 4.0, etc.) que não existem.

**Infra implementada (pronta para reativar futuramente):**
- Cadeia de fallback: Brave Search API → Tavily → DuckDuckGo
- Quota Brave: 2000/mês, rastreada em `web_search_usage.json`
- Chaves em `config.py`: `BRAVE_API_KEY`, `TAVILY_API_KEY`

**Para reativar:** descomentar o bloco `# Busca web` em `backend/main.py` E revisar a instrução no system prompt (atualmente removida para evitar confusão).

### Chat com Seletor de Modelo
- Dropdown no topo do input: Claude (CC) | Kiro | GPT-4o
- Modelo selecionado é passado para o backend via `model` no body do POST
- Se o modelo selecionado levar 429, faz fallback automático pelos demais (silencioso)

### Base de Conhecimento Multi-fonte
- Busca por palavras-chave em 5 fontes simultâneas
- Injeta os 4 artigos mais relevantes por pergunta (máx. 6.000 chars)
- Recência calculada: ≤12 meses = +60% score, 12–24 meses = +30%
- `knowledge_structured.json` e `base_conhecimento.json` têm peso 1.5x (alta prioridade)
- `farmafacil_knowledge.md` tem peso 1.2x

### OCR em Análise de Prints
- Transcreve todo o texto visível na tela antes de diagnosticar

### Fallback de IA Automático
Cadeia silenciosa — analista não vê erros de troca de modelo:
1. `cc/claude-sonnet-4-6` (Claude Code local)
2. `kr/claude-sonnet-4.5` (Kiro)
3. `pollinations/openai` (GPT-4o)
4. `pollinations/gemini` (Gemini)

### Chat Logger
- Salva histórico em `chat_logs/<usuario>/YYYY-MM-DD.txt`

### Módulo Gestão (Movidesk)
Acessível por todos os roles com permissão (ver tabela RBAC).

**Tabs (todos os roles):** Dashboard | Analistas | Farmácias | Metas | Sazonalidade | Base de Chamados | Duplicados | Análise IA | Chat com IA
**Tabs (analista):** Dashboard | Analistas | Farmácias | Metas

**Grupos de analistas** (`gestao_config.py` + `Gestao.jsx` GRUPOS_CONFIG — devem estar sincronizados):
- **Fiscal:** Vinicius, Rebeca Medeiros, Rubens — SPED, NF-e, obrigações fiscais
- **Produção:** Isaac, Raul, Matheus, Boeira, Ruam — Nota de Entrada, manipulação, produção
- **G1:** Marcello, Alan, Keven — Suporte geral
- **GW:** Nathan Lopes — Orya, e-commerce, Alcance, FarmaFácil Web
- **Ouvidoria:** Érica Milo Nardo Portezani, Lucas Eduardo Durante, Guilherme Cordeiro, Taynara Ribeiro — reclamações, elogios, sugestões
- **Fórmula Animal:** Diego Teixeira — atendimento exclusivo redes Fórmula Animal (cor esmeralda)

**Notas sobre grupos:**
- Guilherme Cordeiro está somente em Ouvidoria (não em Fiscal)
- Gomes foi removido de todos os grupos (saiu da empresa)
- `excluir_metas`: apenas Guilherme Cordeiro (não entra no cálculo de metas)
- Diego Teixeira é membro regular do grupo FormulaAnimal — **não está** em `excluir_metas`
- `_CATEGORIA_GRUPOS` foi removido de `movidesk_sync.py` — todos os grupos filtram por nome do analista, não por categoria
- `get_metas_por_equipe()` inclui 6 grupos: Fiscal, Producao, G1, GW, Ouvidoria, FormulaAnimal
- **`client_filters`** em `gestao_config.json`: grupos com filtro de cliente só contam tickets cujo `client_name` contém a substring configurada. FormulaAnimal usa `"formula animal"` — todas as filiais seguem o padrão `FORMULA ANIMAL - <cidade>`
- `count_open_by_owner()` retorna `{owner: {'total': N, 'by_client': Counter}}` para suportar fila filtrada por cliente
- Filtros de grupo (Dashboard, Duplicados, Metas, cards) mostram Ouvidoria e Fórmula Animal somente para `isLider` (lideres/administrador)

**Endpoints principais:**
- `GET /api/gestao/analista-view` — fila do analista logado
- `GET /api/gestao/respostas-rapidas` — top 20 soluções por categoria
- `GET /api/gestao/duplicados?grupo=Fiscal` — chamados duplicados em aberto
- `GET /api/gestao/metas?semanas_alvo=4` — metas por equipe
- `GET /api/gestao/sazonalidade` — volume por semana/mês
- `GET /api/gestao/aderencia?date_from=&date_to=` — aderência ao perfil por analista
- `GET /api/gestao/nova-versao` — issues do sprint ativo do Jira (somente leitura, cache 30 min)
- `POST /api/gestao/sync-abertos` — sync de todos os tickets em aberto (sem filtro de data)
- `GET /api/gestao/abertos-hoje` — tickets criados hoje do cache local com classificação de grupo
- `GET /api/gestao/auditoria-contato?date_from=&date_to=` — auditoria de procedimento cliente indisponível (lideres+ only)

**Aderência ao perfil (`/api/gestao/aderencia`):**
- Para cada analista em grupo conhecido (exceto `excluir_metas`), computa:
  - `total_resolvidos`, `na_categoria` (categoria do ticket bate com o grupo do analista), `fora_categoria`, `aderencia_pct`
  - `top_categorias`: top 6 serviceFirst dos tickets resolvidos pelo analista
- Classificação do ticket por grupo: `get_grupo_for_ticket()` — prioridade categoria > analista
- Frontend: seção "Aderência ao Perfil" no Dashboard, até 5 colunas (Fiscal/Produção/G1/GW/Ouvidoria), card por analista
  - Barra colorida: verde ≥70%, amarelo ≥40%, vermelho <40%
  - Clique no card expande breakdown de categorias com mini-barras
  - Média do grupo exibida no header de cada coluna
  - Visível para todos os roles com acesso ao Dashboard
  - **Filtro de grupo:** quando `filterGrupo` está ativo (ex: Ouvidoria selecionado), os cards de equipe (TeamSummaryCard, GrupoAnalistasCard) e a seção Aderência exibem somente o grupo selecionado. Ao mudar período (mês passado, etc.) o filtro é mantido.

**Sincronização:**
- Etapa 0: todos os tickets em aberto (sem filtro de data) via `sync_open_tickets()`
- Etapa 1: 3 batches mensais com data explícita (últimos 90 dias)
- Etapa 2: tickets > 90 dias via `/tickets/past`

### Módulo Suporte — Painel do Analista
Acessível por **todos os roles**.

**Tabs:** Minha Fila | Respostas Rápidas

- Fila ordenada do mais antigo ao mais novo com badge de urgência por cores (verde/amarelo/laranja/vermelho)
- Card expansível mostra similares resolvidos + checklist automático por categoria
- `movidesk_name` em `users.json` mapeia login → nome exato no Movidesk

---

## Regras da API Movidesk

**Base:** `https://api.movidesk.com/public/v1/tickets`
**Auth:** parâmetro `token` em todas as requisições

**Status relevantes:**
- `5 - Resolvido` — analista resolveu
- `6 - Fechado` — fechamento administrativo
- `6 - Cancelado` — cancelado (excluído da fila e dos similares)

**"Resolvidos hoje" (igual ao dashboard):**
```
status eq '5 - Resolvido' AND lastUpdate ge 2026-04-17 AND lastUpdate lt 2026-04-18
```

---

## Módulo Provedores NFS-e

Página standalone no menu lateral (`provedor`). Acessível por: **todos os roles** (analista, backservice, fiscal, lideres, administrador).

**Objetivo:** Monitorar se algum provedor de NFS-e tem issues abertas no Jira e alertar quais farmácias serão impactadas.

### Fontes de dados

| Fonte | O que traz | Cache |
|---|---|---|
| `ACBrNFSeXServicos.ini` (GitHub raw) | Mapa `município → provedor NFS-e` (todos os municípios do Brasil) | 24h |
| `movidesk_tickets.json` (local) | Farmácias detectadas por palavras-chave NFS-e nos tickets do Movidesk | sem cache (lido direto do arquivo) |
| Jira (via `_get_jira_issues_cached()`) | Issues abertas (`status_cat != done`) — busca nome do provedor no título + descrição + comentários + componentes + labels | 30 min |

### Detecção de farmácias NFS-e (`_get_farmacias_do_cache()`)

Lê o arquivo `movidesk_tickets.json` e filtra somente clientes com ao menos um ticket que contenha palavras-chave relacionadas a nota fiscal de serviço nos campos `subject`, `serviceFirst`, `serviceSecond`, `problema`, `solucao`.

**Palavras-chave (`_NFSE_KW_TICKETS`):** `nfse`, `nfs-e`, `nota fiscal de servi`, `prefeitura`, `rps`, `danfse`, `webiss`, `ginfes`, `emissão de nota`, `lote nfs`, etc.

Retorna tupla `(farmacias_nfse: list, total_clientes: int)` — lista de clientes com evidência de NFS-e + total de clientes únicos no cache.

### Normalização de municípios (`_norm_mun()`)

Remove acentos, substitui apóstrofo e hífen por espaço, normaliza espaços, lowercase. Resolve mismatch como `"Alta Floresta D'Oeste"` vs `"Alta Floresta D Oeste"`.

### Lógica de cruzamento

1. Parseia o `.ini` do ACBr: `norm_municipio → {nome, uf, provedor}`
2. Lê farmácias com evidência de NFS-e do cache de tickets (`_get_farmacias_do_cache()`)
3. Para cada farmácia, faz match normalizado `cityName → provedor no INI`
4. Para cada provedor com ao menos uma farmácia: detecta issues Jira abertas onde o nome do provedor aparece como palavra inteira (`\b`) em título, desc_text, comment_text, components ou labels
5. Status do provedor: `ok` | `alerta` (issue com prioridade normal) | `critico` (High/Highest/Blocker)
6. Ordena: crítico → alerta → ok

**Importante:** `_provedor_in_issue()` usa `re.search(r'\b' + re.escape(nome) + r'\b', texto, IGNORECASE)` — evita falsos positivos como "EL" casando em "elaboração".

### Extração de texto das issues Jira (`_fetch_all_jira_issues()`)

Campos buscados: `summary, status, issuetype, priority, assignee, updated, description, labels, comment, components`

- `desc_text`: até **3.000 chars** do texto plano da descrição (ADF ou HTML)
- `comment_text`: últimos **20 comentários**, cada um até **500 chars**, com corpo ADF parseado corretamente via `_adf_text()` (não mais `str(dict)`)
- `components`: nomes dos componentes da issue (ex: "Betha", "WebISS")
- `_provedor_in_issue()` pesquisa em: titulo + desc_text + comment_text + components + labels

### Endpoints Backend

| Rota | Método | Descrição |
|---|---|---|
| `/api/provedor/status` | GET | Retorna todos os provedores com farmácias + issues + status |
| `/api/provedor/atualizar-ini` | POST | Invalida cache do INI (24h) e força re-download do GitHub |
| `/api/provedor/atualizar-jira` | POST | Invalida cache de issues do Jira (30min) e força re-busca |

**Resposta de `/api/provedor/status`:**
```json
{
  "provedores": [
    {
      "nome": "Fiorilli",
      "status": "alerta",
      "issues": [{"key": "ID-123", "titulo": "...", "status": "Em andamento", "prioridade": "High", "responsavel": "...", "atualizado": "2026-04-28"}],
      "farmacias": [{"nome": "NatuFarma Linhares", "municipio": "Linhares", "uf": "ES"}],
      "total_municipios": 42
    }
  ],
  "total_provedores": 15,
  "com_alerta": 2,
  "farmacias_afetadas_total": 4,
  "total_municipios_ini": 5843,
  "total_farmacias_nfse": 150,
  "total_clientes_mv": 922
}
```

### Frontend (`frontend/src/pages/ProvedorNFSe.jsx`)

- Header com botão de reload + timestamp da última atualização
- **Dashboard:** 4 stat cards (Provedores monitorados / Farmácias com NFS-e / Provedores com issues / Farmácias afetadas) + barra de distribuição de status (crítico/alerta/ok)
- **Filtros:** busca por nome do provedor, busca por farmácia/município, botões Todos | Com alerta | OK
- **Botão "Atualizar municípios"** → invalida cache INI (24h) e recarrega
- **Botão "Atualizar Jira"** → invalida cache Jira (30min) e recarrega issues
- **Botão "Copiar"** → copia relatório de todos os provedores filtrados para o clipboard
- **Cards por provedor:** colapsável, auto-expande quando há filtro de farmácia
  - Badge de status colorido
  - Issues Jira clicáveis → abre `DetalheModal` lateral (igual ao Tarefas)
  - Lista de farmácias afetadas com município e UF — **texto selecionável** (Ctrl+C funciona)
  - Quando filtro de farmácia ativo: mostra só as farmácias que batem + contador "X de Y"
- **DetalheModal:** idêntico ao Tarefas — `dangerouslySetInnerHTML` com classe `jira-html`, lightbox para imagens, "Analisar com IA", "Continuar no Chat"
- Auto-refresh a cada 5 minutos
- `onSendToChat` passado de `App.jsx` → "Continuar no Chat" funciona

### Arquivos relevantes

```
backend/main.py              → _norm_mun, _fetch_acbr_ini, _get_acbr_ini_cached,
                               _NFSE_KW_TICKETS, _get_farmacias_do_cache,
                               _is_nfse_issue (mantida mas não usada no filtro principal),
                               _provedor_in_issue, rotas /api/provedor/*
frontend/src/pages/ProvedorNFSe.jsx  → página completa + DetalheModal + StatCard
frontend/src/api/backend.js          → provedorStatus(), provedorAtualizarIni(), provedorAtualizarJira()
```

---

## Módulo Painel TV

Acessível somente por **lideres** e **administrador**.

Painel para exibição em televisão na sala de suporte. Mostra métricas semanais (segunda a sexta) de chamados entrados e fechados no Movidesk.

Existem **duas formas de acesso**:

| Forma | URL | Tecnologia | Quando usar |
|---|---|---|---|
| React (moderno) | `http://192.168.0.118:5000/?tv=tv-suporte-2026` | React + framer-motion | Navegadores modernos |
| Standalone HTML | `http://192.168.0.118:5000/tv` | HTML/CSS/JS puro, zero dependências | TV antiga / browser legado |

### TV auto-login (React)

O React detecta `?tv=KEY` na URL em `checkSession()`:
1. Chama `GET /api/tv-login?key=tv-suporte-2026` → recebe token com role `lideres`
2. Salva `erp_tv_mode=1` no localStorage → persiste entre reloads
3. Redireciona para a página `painel` automaticamente
4. Sidebar e StatusBar ficam ocultos (modo fullscreen)

### Standalone `tv.html`

Arquivo `erp_assistant/tv.html` servido pela rota `GET /tv` no Flask.

**Design (tv.html):**
- Fundo escuro `#080c18`, scanline overlay sutil
- **3 abas em rotação:** Metas Individuais → Ritmo Diário → Desempenho por Equipe
- **Metas Individuais:** top 5 analistas apenas (não todos os 13)
  - Medalhas via CSS (círculos `1` / `2` / `3` em dourado/prata/bronze) — sem emoji (TV antiga não renderiza)
  - Sem banner "Líder da semana"
  - Sem avatar (letra inicial removida)
  - Separadores verticais entre as colunas Entr. / Fech. / Saldo para evitar confusão visual
  - Nome do analista 32px, números Entr/Fech 46px, Saldo 46px (mesma escala), rank com `margin-right` para respirar
- **Ritmo Diário:** barra de progresso horizontal por analista mostrando avanço em relação à meta diária
  - Meta diária = tickets entrados no mês / n_analistas / dias úteis decorridos
  - Exibe `fechados_hoje / meta_dia` por analista
  - Barra fica inteiramente verde (`#00c853`) quando analista atinge ou supera a meta
  - `barMax` calculado apenas com analistas que têm `meta_dia > 0`
  - Sem tag de equipe abaixo do nome; sem coluna ritmo/dia
- **Desempenho por Equipe:** grid 2×2
  - Card com borda esquerda 4px na cor da equipe (sem bloco de cor pesado)
  - Fundo neutro escuro `rgba(255,255,255,0.025)`
  - 3 métricas centralizadas (Entrados / Fechados / Saldo) em **66px monospace**
  - Rodapé discreto com barra de progresso (2px, opacidade 0.5) + Taxa de resolução
- Botão **Pausar / Retomar** para fixar aba; botão **Atualizar** para forçar reload
- Rotação automática a cada **30s** com barra de progresso no topo
- Reconecta automaticamente se o token expirar (re-chama `/api/tv-login`)
- Auto-refresh dos dados a cada **12s** (backend: cache TTL 2 min)

### Analistas monitorados (`_PAINEL_ANALISTAS`)

| Equipe    | Label TV | Cor TV    | Analistas |
|-----------|----------|-----------|-----------|
| Fiscal    | G2       | `#D4537E` | Vinicius, Rebeca, Rubens |
| Producao  | G3       | `#7F77DD` | Matheus, Boeira, Isaac, Raul, Ruam |
| G1        | G1       | `#378ADD` | Alan, Marcello, Keven |
| GW        | GW       | `#888780` | Nathan, Taynara |
| FormulaAnimal | FA   | `#34d399` | Diego Teixeira |

Diego Teixeira pertence ao grupo FormulaAnimal. Sua meta diária é calculada dinamicamente pelos tickets da Fórmula Animal (igual aos outros grupos), sem valor fixo.

### Lógica de dados

**`/api/painel/semanal`**
- **Entrados** = tickets criados na semana (segunda a sexta) onde owner = analista
- **Fechados** = tickets resolvidos (`5 - Resolvido` **ou** `6 - Fechado`) na semana onde owner = analista
- **Saldo** = fechados − entrados (pode ser negativo)
- Fonte: Movidesk API ao vivo (não usa cache local de tickets)
- Cache em memória TTL 2 min (`_painel_cache`)
- `_painel_match()` faz match case-insensitive (exact first, partial fallback ≥4 chars)

**`/api/painel/diario`** (Ritmo Diário)
- **fechados_hoje** = tickets com `resolvedDate` hoje onde owner = analista (status 5 ou 6)
- **meta_dia** = tickets entrados no mês / n_analistas (excluindo `excluir_metas`) / dias úteis decorridos
- Analistas em `excluir_metas` recebem `meta_dia = 0` (ex: Guilherme Cordeiro)
- `metas_fixas` em `gestao_config.json` pode sobrepor o cálculo automático para analistas específicos (atualmente vazio)
- Cache em memória TTL 2 min (`_diario_cache`)

### Módulo Abertos Hoje (`AbertosHoje.jsx`)

Acessível por: **backservice, fiscal, lideres, administrador** (analista não vê).

Mostra todos os chamados cuja `createdDate == hoje` com filtro por grupo.

**Filtros:** Todos | Fiscal | Produção | G1 | GW (com contador em cada botão, na cor do grupo)

- Lista compacta com borda colorida esquerda por grupo
- Colunas: #ID (link Movidesk), Assunto/Farmácia, Analista, Categoria, Status
- Tickets classificados via `get_grupo_for_ticket()` do `gestao_config.py`
- Grupos Ouvidoria e FormulaAnimal aparecem em "Todos" mas não têm botão de filtro

**Endpoint:** `GET /api/gestao/abertos-hoje`
- Lê do cache local (`movidesk_tickets.json`)
- Filtra `createdDate == date.today()`
- Retorna `{tickets, total, contagem: {Fiscal, Producao, G1, GW, outros}, data}`

---

### Módulo Auditoria de Contato (`AuditoriaContato.jsx`)

Acessível somente por **lideres** e **administrador**. Backend verifica role — retorna 403 para os demais.

Monitora analistas que não seguem o procedimento correto ao tentar contato com clientes.

**Procedimento correto:**
1. Ligar para o cliente → não conseguiu → aplicar macro "3 - Cliente indisponível para resolução"
2. Quando a macro é aplicada: ticket muda para status `"Em pausa"` / `"9 - Cliente indisponivel"` e uma mensagem é inserida na conversa com o texto fixo `"tentativas de contato via telefone"`
3. Repetir em **5 dias diferentes** (dias corridos — fim de semana conta)
4. Após 5 tentativas: **CANCELAR** o ticket (nunca resolver)

**Tipos de violação detectados:**
- **Resolvido indevidamente** — ticket com macro aplicada foi fechado como `5 - Resolvido` em vez de cancelado
- **Cancelado prematuro** — ticket foi cancelado com menos de 5 dias distintos de tentativas

**Exclusões legítimas** — tickets ignorados mesmo com ações da macro (lista `_EXCLUIR_KW` em `gestao_auditoria_contato`):
1. `"incidente/"` → template `"Incidente/Dúvida Relatado:"` preenchido = analista resolveu de verdade com contato real
2. `"verifiquei que este ticket apresenta a mesma situa"` → ticket duplicado/vinculado a outro

Para adicionar novos critérios de exclusão, basta inserir a substring na lista `_EXCLUIR_KW` no endpoint.

**Detecção:** busca nas `actions` de cada ticket o texto `"tentativas de contato via telefone"` (substring fixa da macro) ou referência ao status `"9 - cliente indisponivel"`. Conta as datas distintas das actions da macro.

**Período:** date picker De/Até escolhido pelo líder. Padrão: últimos 30 dias.

**Resultado:** agrupado por analista, ordenado por mais violações. Cada card é expansível e mostra os tickets com tipo de violação, datas das tentativas e link para o Movidesk.

**Endpoints:**
- `GET /api/gestao/auditoria-contato?date_from=&date_to=` — busca na API Movidesk (não cache local) tickets resolvidos + cancelados no período com `$expand=actions`, aplica detecção e retorna `{resultado, total_violacoes, total_analisados, periodo}`
- `fetch_encerrados_auditoria()` em `movidesk_client.py` — faz o fetch paginado com `$expand=owner,clients,actions`

**Arquivos relevantes:**
```
backend/main.py                          → gestao_auditoria_contato(), proteção de role
utils/movidesk_client.py                 → fetch_encerrados_auditoria()
frontend/src/pages/AuditoriaContato.jsx  → página completa
frontend/src/api/backend.js              → gestaoAuditoriaContato()
```

---

### Sync automático de tickets abertos
Thread daemon iniciada junto com o backend (`_auto_sync_loop`):
- Aguarda 30s após subir, depois roda `sync_open_tickets()` a cada **15 minutos**
- Mantém o cache local (`movidesk_tickets.json`) alinhado com o Movidesk sem intervenção manual
- Log no terminal: `Auto-sync abertos: X ticket(s) atualizados/novos`
- Sync manual continua disponível para forçar atualização imediata

### Visual React (`Painel.jsx`)
- Fundo escuro `#080c18`, overlay scanline sutil (`.painel-scanline`)
- **Barras de progresso:** animação com `[0.22, 1, 0.36, 1]` + shimmer contínuo (`.progress-shimmer::after`)
- **1º lugar:** emoji 🥇 com pulso dourado (`.medal-pulse`)
- **Banner do líder:** card dourado slide+fade no topo das Metas
- **FLIP animation:** `motion.div` com `layout` + `layoutId` — framer-motion reordena suavemente
- **Setas ↑↓:** `motion.span` com `opacity: 0→fade` em 2s ao mudar posição
- **Count-up:** `useCountUp` hook com easing cubic nos totais e cards de equipe
- **Countdown:** relógio em tempo real para próximo sábado; últimos 60min → laranja pulsando

### Endpoints backend
| Rota | Método | Descrição |
|---|---|---|
| `GET /api/tv-login?key=KEY` | GET | Auto-login TV — retorna token com role `lideres` |
| `GET /tv` | GET | Serve `tv.html` (standalone, sem autenticação) |
| `GET /api/painel/semanal` | GET | Dados da semana por analista e por equipe |
| `GET /api/painel/diario` | GET | Fechados hoje + meta diária por analista (Ritmo Diário) |
| `POST /api/painel/reset-cache` | POST | Invalida ambos os caches (`_painel_cache` e `_diario_cache`) |

### Arquivos relevantes
```
erp_assistant/tv.html              → standalone HTML/CSS/JS para TV antiga (sem React)
backend/main.py                    → _TV_KEY, _PAINEL_ANALISTAS, _painel_match,
                                     rotas /api/tv-login, /tv, /api/painel/*
                                     _diario_cache / _diario_lock (Ritmo Diário)
utils/movidesk_client.py           → fetch_resolved_page: filtra status 5 e 6
utils/movidesk_sync.py             → _mem_cache / _mem_cache_mtime (cache em memória do JSON)
utils/gestao_config.py             → excluir_metas, metas_fixas, client_filters, get_metas_fixas(), get_client_filter()
frontend/src/pages/Painel.jsx      → página React completa + todos os sub-componentes
frontend/src/App.jsx               → detecção ?tv=KEY, tvMode state, erp_tv_mode localStorage
frontend/src/api/backend.js        → tvLogin(), painelSemanal(), painelResetCache()
frontend/src/components/Sidebar.jsx → ícone Trophy, rota 'painel' no ROLE_PAGES
frontend/src/styles/globals.css    → shimmer-move, medal-glow, pulse-dot, painel-scanline
```

---

## Como Compilar para Distribuição

```bat
:: 1. Gerar frontend web
cd frontend
npx vite build
cd ..

:: 2. Gerar backend.exe
compilar_backend.bat

:: 3. Copiar frontend para dist_backend
xcopy /E /I /Y frontend\dist dist_backend\frontend\dist
```

---

## Rede

- **Servidor roda em:** `192.168.0.118` (máquina do Guilherme)
- **Clientes acessam:** `http://192.168.0.118:5000`
- **OmniRoute:** `localhost:20128` (só na máquina servidora)
- **Para expor OmniRoute à rede:** rodar `expor_ia_na_rede.bat` como admin

---

## Workflow Git

**Repositório:** `https://github.com/guizaodamec/movideskbot`
**Branch principal:** `main`

**Regra:** toda alteração no código deve ser commitada no git logo em seguida.

### Como fazer push

Rodar `git_push.bat` na raiz do projeto:

```bat
git_push.bat
```

O script faz `git add -A`, exibe o status, pede uma mensagem de commit (ou gera uma com data/hora se Enter) e executa `git push origin main`.

### O que está no .gitignore (nunca vai ao git)

| Arquivo/pasta | Motivo |
|---|---|
| `connection.json` | Credenciais do banco + tokens Jira/Movidesk |
| `users.json` | Usuários e senhas do sistema |
| `config.py` / `.env` | Chave da API Anthropic |
| `movidesk_tickets.json` | Dados de clientes (privados) |
| `db_schema_*.json`, `schema_*.txt` | Gerados automaticamente |
| `frontend/node_modules/`, `frontend/dist*/` | Build e dependências |
| `_backups/`, `memory/`, `.claude/` | Cache e sessões do Claude Code |
| `chat_logs/` | Logs de conversa (dados do cliente) |

### Segredos — onde ficam localmente

- **Jira** (`jira_email`, `jira_token`): em `connection.json` — carregados em `backend/main.py` via `_load_jira_creds()`
- **Movidesk token**: em `config.py` — importado por `utils/movidesk_client.py`
- **Anthropic API key**: em `.env` — lida pelo backend na inicialização

---

## Jira — Rastreamento de Issues

**REGRA ABSOLUTA: NUNCA criar, editar ou excluir issues no Jira. Apenas leitura (GET).**

**Projeto:** Desenvolvimento-delphi (`ID`) em `prismadelphi.atlassian.net`
**Label padrão:** `sistema-farmafacil`

### Integração Jira no sistema (backend/main.py)

- `_fetch_all_jira_issues()` — busca todas as issues do projeto via JQL (somente GET/POST de busca)
- `_get_jira_issues_cached()` — cache em memória TTL 30 min
- `_fetch_sprint_issues()` — busca issues do sprint ativo via JQL `sprint in openSprints()` (somente leitura)
- `_get_sprint_issues_cached()` — cache separado TTL 30 min
- `_search_jira_context(query)` — injeta issues relevantes no chat principal; quando a query menciona "versão/sprint/novidade", injeta issues do sprint ativo
- `/api/tarefas` — lista todas as issues (GET)
- `/api/tarefas/<key>/detail` — detalhe de uma issue (GET)
- `/api/tarefas/<key>/analisar` — analisa issue com IA, baixa imagens, retorna análise em PT-BR (POST, somente leitura Jira)
- `/api/gestao/nova-versao` — issues do sprint ativo agrupadas por status (GET)

### Aba "Nova Versão" (em Tarefas, não em Gestão)

- Localização: página **Tarefas** → tab "Nova Versão"
- Mostra issues do sprint ativo agrupadas em: Em Andamento | A Fazer | Concluído
- Cada card mostra: key (ID-XXX), tipo, título, responsável, link para o Jira
- Cache de 30 min — botão "Atualizar" força nova busca

### Módulo Tarefas — Kanban + Nova Versão + Análise com IA

**Tabs:** Kanban | Nova Versão

**Kanban:** Board 3 colunas (A Fazer / Em Andamento / Finalizado). Clique num card → modal lateral com detalhes completos.

**Análise com IA (no modal de detalhe):**
- Botão "Analisar com IA" no header do modal
- Backend: `POST /api/tarefas/<key>/analisar` — busca issue completa via GET (somente leitura), baixa primeira imagem como base64, chama IA com prompt especializado
- A IA recebe: título, tipo, status, prioridade, responsável, descrição, últimos 10 comentários, issues relacionadas, subtarefas, e imagem (se houver)
- Retorna análise em linguagem natural: o que está sendo feito, impacto, pontos de atenção, próximos passos
- Badge "+ imagem" indica que imagem foi analisada visualmente
- Botão "Continuar no Chat" → abre Chat com o contexto da issue + análise pré-carregados

### FarmaBot — contexto de versão

Quando o analista perguntar no chat principal sobre "próxima versão", "o que vai sair", "novidades", "sprint", a IA recebe automaticamente a lista de issues do sprint ativo como contexto, podendo responder sobre funcionalidades em desenvolvimento.

Issues criadas em 24/04/2026 referentes à sessão de melhorias da FarmaBot:

| Key | Tipo | Título |
|---|---|---|
| ID-940 | Bug | IA inventava módulos e menus inexistentes no FarmaFácil |
| ID-941 | Bug | IA gerava notícias SEFAZ falsas via instrução de busca web |
| ID-942 | Bug | 429 rate limit não fazia fallback silencioso com modelo específico |
| ID-943 | Bug | Respostas com separadores --- e tabelas markdown brutas |
| ID-944 | Melhoria | Base de conhecimento multi-fonte com 5 origens e pesos diferenciados |
| ID-945 | Melhoria | Busca web automática Brave → Tavily → DuckDuckGo (desativada temporariamente) |
| ID-946 | Melhoria | System prompt reescrito para analistas sem background farmacêutico |
| ID-947 | Melhoria | Seletor de modelo no chat simplificado para 3 opções |
| ID-948 | Tarefa | knowledge_corrections.json com correções manuais de prioridade máxima |

---

## Bugs Corrigidos (histórico)

| # | Problema | Fix |
|---|---|---|
| 1 | Login falha em outras máquinas | `backend.js` URL era `localhost` fixo → mudado para `window.location.hostname` |
| 2 | Erro ao salvar usuários | `paths.py` gravava em `C:\ProgramData` (sem permissão) → usa raiz do projeto |
| 3 | Chat "Connection error" | OmniRoute não iniciava → `iniciar_servidor.bat` inicia automaticamente |
| 4 | OmniRoute erro 193 | `better-sqlite3` com arquitetura errada → `npm rebuild` |
| 5 | Troca de senha obrigatória não funcionava | `Login.jsx` não passava `must_change_password` → corrigido |
| 6 | Contagem errada de chamados no Gestão | Sync não usava date range → dois passes com datas explícitas |
| 7 | `checklists.py` crashava no Python 3.9 | Sintaxe `dict | None` (Python 3.10+) → removida anotação de retorno |
| 8 | Texto não selecionável no Painel do Analista | `user-select: none` em globals.css → adicionado `selectable` |
| 9 | Fila incluía cancelados | `get_analista_tickets` não excluía `6 - Cancelado` → usa `_is_aberto()` |
| 10 | Fila incompleta (tickets antigos em aberto) | Sync limitado a 90 dias → adicionado `sync_open_tickets()` sem filtro de data |
| 11 | IA respondia sobre geometria/jogos | System prompt sem glossário FarmaFácil → glossário completo adicionado |
| 12 | IA gerava tool-calls (`<read_code>`) | Claude tentando "ler código" → instrução explícita + `_strip_bold` remove tags |
| 13 | 429 não fazia fallback | Lista de modelos com 1 item ao usar modelo específico → agora usa lista completa com preferido primeiro |
| 14 | `---` apareciam nas respostas | `_strip_bold` não removia horizontal rules → regex adicionado |
| 15 | Tabelas markdown com `|` feias | `_strip_bold` só removia separadores → agora converte tabela em texto limpo |
| 16 | Kiro ignorava system prompt | Usava `extra_body={"system":...}` (Anthropic) → mudado para `{"role":"system"}` em messages |
| 17 | IA inventava módulos/menus inexistentes | Sem instrução explícita → adicionado `REGRAS ABSOLUTAS` com proibição de inventar caminhos + `knowledge_corrections.json` com correções específicas |
| 18 | IA gerava notícias SEFAZ falsas via busca web | Instrução `BUSCA WEB` no system prompt fazia IA simular ferramenta de busca → instrução removida, integração desativada |
| 19 | Provedor "EL" mostrava 85 falsos alertas | Match por substring (`"el" in texto`) casava em qualquer palavra → trocado por `re.search(r'\b...\b')` (word boundary) |
| 20 | Dashboard do Provedores todo zerado | Movidesk `/persons` vazia + mismatch de acentos nos municípios → trocado para `movidesk_tickets.json` + `_norm_mun()` para normalizar |
| 21 | HTML quebrado no modal de issues do Provedores | Modal usava `whitespace-pre-wrap` puro → copiado `DetalheModal` idêntico ao Tarefas com `dangerouslySetInnerHTML` + `jira-html` CSS |
| 22 | Filtro por farmácia mostrava provedor mas não filtrava as farmácias | `buscaFarmacia` não era passado para `ProvedorCard` → prop adicionada, lista filtrada dentro do card, card auto-expande |
| 23 | Farmácias não selecionáveis (Ctrl+C não funcionava) | Sem classe `selectable` nas linhas → adicionado `selectable` nas linhas de farmácia |
| 24 | Issues do Jira não detectadas (corpo ADF em comentários) | `str(dict)` gerava repr ilegível → `_adf_text()` agora usado para corpos de comentário; desc_text 800→3000 chars; 10→20 comentários; campo `components` adicionado |
| 25 | `onSendToChat` não funcionava em Provedores NFS-e | `App.jsx` não passava a prop → `onSendToChat={handleSendToChat}` adicionado |
| 26 | Chamados "Fechado" (status 6) não contavam no Painel TV | `fetch_resolved_page` filtrava só `5 - Resolvido` → filtro expandido para `status eq '5 - Resolvido' or status eq '6 - Fechado'` |
| 27 | Chat da IA lento (leitura de tickets.json a cada mensagem) | `load_cache()` em `movidesk_sync.py` lia arquivo do disco a cada chamada → cache em memória com invalidação por mtime |
| 28 | Barra do Diego desproporcional no Ritmo Diário | Diego sem meta (`meta_dia = 0`) inflava `barMax` para todos → `barMax` calculado só com analistas com `meta_dia > 0` |
| 29 | Fila de chamados desatualizada ao longo do dia | Sem sync automático, cache só atualizava com clique manual → thread daemon `_auto_sync_loop` roda `sync_open_tickets` a cada 15 min |
| 30 | Diego sem meta no Ritmo Diário (exibia `0/0`) | Estava em `excluir_metas` sem override → campo `metas_fixas` em `gestao_config.json` + `get_metas_fixas()` aplicado no `painel_diario` |
| 31 | Fila do Diego no Gestão incluía tickets de outros clientes | Diego atende só Fórmula Animal mas fila contava todos os tickets dele → grupo `FormulaAnimal` com `client_filters: "formula animal"` filtra métricas por `client_name` |
| 32 | Métricas do grupo FormulaAnimal zeradas no Gestão → Metas | Diego estava em `excluir_metas` → `membros_metas` ficava vazio, todas as métricas eram 0 → removido de `excluir_metas`; equipe alterada para `"FormulaAnimal"` no `_PAINEL_ANALISTAS` |
| 33 | Painel Analista removido | Substituído pela página Abertos Hoje — mostra chamados do dia com filtro por grupo (Fiscal/Produção/G1/GW) |
| 34 | Auditoria flagrava resoluções legítimas (1ª tentativa) | Tentativa de exclusão via `serviceFirstLevel/serviceSecondLevel` com texto "resolvido ticket - sem artigo" — não funcionou pois o campo não continha esse valor no ticket real |
| 35 | Auditoria flagrava resoluções legítimas (fix real) | Exclusão correta: verifica se qualquer `action.description` contém `"incidente/"` (template "Incidente/Dúvida Relatado:" preenchido pelo analista ao resolver de verdade) → ignora o ticket |
| 36 | Auditoria incluía tickets duplicados/vinculados | Actions com "Verifiquei que este ticket apresenta a mesma situação relatada" indicam duplicado → adicionado à lista `_EXCLUIR_KW` |
