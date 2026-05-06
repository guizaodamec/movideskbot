import time
from db.connector import execute_query

# Modulos detectaveis — usa matching parcial (substring) no nome da tabela
KNOWN_MODULES = {
    "Fiscal (NF-e)":      ["nfe", "nfce", "nota_fiscal", "notafiscal"],
    "Fiscal (NFS-e)":     ["nfse", "nfs_"],
    "Producao":           ["ordem_prod", "producao", "manipulacao", "ordem_man"],
    "Estoque":            ["estoque", "movimentacao", "mov_", "lote"],
    "Produtos":           ["produto", "materia_prima"],
    "Financeiro":         ["conta_pagar", "conta_receber", "financeiro", "titulo"],
    "RH / Folha":         ["funcionario", "folha_pagamento"],
    "Vendas":             ["pedido", "venda", "orcamento"],
    "SNGPC":              ["sngpc", "controlado"],
    "Caixa / PDV":        ["caixa", "pdv", "recebimento"],
    "Compras":            ["compra", "pedido_compra"],
}

# Variacoes de nomes de tabelas de configuracao
CONFIG_TABLE_VARIANTS = [
    "configuracoes", "parametros", "config", "sistema_config", "empresa",
    "par_sistema", "par_empresa", "cadastro_empresa", "cfg_sistema",
    "far_configuracoes", "far_parametros", "far_empresa",
]

# Variacoes de nomes de tabelas de log de erros
LOG_TABLE_VARIANTS = [
    "log_erros", "log_sistema", "erros", "eventos_erro", "log",
    "far_log_erros", "far_log", "log_evento",
]


def _safe_query(sql, label=""):
    try:
        rows, cols, err = execute_query(sql)
        if err:
            return None, err
        return rows, None
    except Exception as e:
        return None, str(e)


def scan_bank(progress_callback=None):
    """
    Escaneia o banco e retorna um dicionario de perfil.
    progress_callback(pct, msg) — atualiza progresso (0-100).
    """
    profile = {
        "razao_social":       "Empresa nao identificada",
        "cnpj":               "N/A",
        "versao_sistema":     "N/A",
        "regime_tributario":  "N/A",
        "uf":                 "N/A",
        "cidade":             "N/A",
        "ultimo_backup":      "N/A",
        "versao_postgres":    "N/A",
        "modulos_detectados": [],
        "schema":             [],
        "volumes":            [],
        "erros_recorrentes":  [],
        "queries_lentas":     [],
        "conexoes_ativas":    {},
        "locks_ativos":       0,
        "scanned_at":         time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    def _progress(pct, msg):
        if progress_callback:
            try:
                progress_callback(pct, msg)
            except Exception:
                pass

    _progress(5, "Conectado. Verificando versao do PostgreSQL...")

    # Versao do Postgres
    rows, err = _safe_query("SELECT version()")
    if rows:
        profile["versao_postgres"] = str(rows[0].get("version", "N/A"))[:80]

    _progress(15, "Lendo configuracoes da empresa...")

    # Configuracoes da empresa
    # Tenta cada variante de tabela; tambem tenta por matching parcial nas tabelas existentes
    _cfg_candidates = list(CONFIG_TABLE_VARIANTS)

    # Buscar tabelas existentes no banco que contenham palavras-chave
    rows_tbls, _ = _safe_query(
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_schema NOT IN ('pg_catalog','information_schema','pg_toast') "
        "AND table_schema NOT LIKE 'pg_%'"
    )
    if rows_tbls:
        existing = [str(r.get("table_name", "")).lower() for r in rows_tbls]
        for tbl in existing:
            if any(k in tbl for k in ("config", "parametro", "empresa", "param")):
                if tbl not in _cfg_candidates:
                    _cfg_candidates.insert(0, tbl)

    for table in _cfg_candidates:
        # Tenta estrutura chave/valor
        sql = (
            "SELECT chave, valor FROM {t} "
            "WHERE chave IN ('razao_social','cnpj','versao_sistema',"
            "'regime_tributario','uf','cidade','ultimo_backup')"
        ).format(t=table)
        rows, err = _safe_query(sql)
        if rows and not err:
            for row in rows:
                chave = str(row.get("chave", "")).lower()
                valor = str(row.get("valor", ""))
                if chave in profile:
                    profile[chave] = valor
            if any(profile[k] != "N/A" and profile[k] != "Empresa nao identificada"
                   for k in ("razao_social", "cnpj", "versao_sistema")):
                break
        # Tenta estrutura de colunas diretas (ex: SELECT razao_social, cnpj, ... FROM empresa)
        sql2 = "SELECT * FROM {t} LIMIT 1".format(t=table)
        rows2, err2 = _safe_query(sql2)
        if rows2 and not err2 and rows2:
            row = rows2[0]
            for key in ("razao_social", "cnpj", "versao_sistema",
                        "regime_tributario", "uf", "cidade", "ultimo_backup"):
                if key in row and row[key]:
                    profile[key] = str(row[key])
            if any(profile[k] != "N/A" and profile[k] != "Empresa nao identificada"
                   for k in ("razao_social", "cnpj", "versao_sistema")):
                break

    _progress(30, "Lendo schema do banco...")

    # Descobrir schemas disponiveis (excluindo os internos do postgres)
    rows_schemas, _ = _safe_query(
        "SELECT schema_name FROM information_schema.schemata "
        "WHERE schema_name NOT IN ('pg_catalog','information_schema','pg_toast') "
        "AND schema_name NOT LIKE 'pg_%'"
    )
    schemas_found = []
    if rows_schemas:
        schemas_found = [str(r.get("schema_name", "")) for r in rows_schemas]
    if not schemas_found:
        schemas_found = ["public"]

    profile["schemas_found"] = schemas_found
    _progress(32, "Schemas encontrados: {0}".format(", ".join(schemas_found)))

    # Schema completo — busca em todos os schemas encontrados
    schema_filter = ", ".join("'{0}'".format(s) for s in schemas_found)
    sql_schema = (
        "SELECT table_schema, table_name, column_name, data_type "
        "FROM information_schema.columns "
        "WHERE table_schema IN ({0}) "
        "ORDER BY table_schema, table_name, ordinal_position"
    ).format(schema_filter)
    rows, err = _safe_query(sql_schema)
    if rows:
        profile["schema"] = [
            {
                "schema": str(r.get("table_schema", "public")),
                "table":  str(r.get("table_name", "")),
                "column": str(r.get("column_name", "")),
                "type":   str(r.get("data_type", ""))
            }
            for r in rows
        ]

    _progress(38, "Tabelas encontradas: {0}".format(
        len(set(r["table"] for r in profile["schema"]))))

    _progress(45, "Verificando volumes de dados...")

    # Volumes por tabela
    sql_vol = (
        "SELECT schemaname, tablename, n_live_tup AS registros "
        "FROM pg_stat_user_tables "
        "ORDER BY n_live_tup DESC "
        "LIMIT 30"
    )
    rows, err = _safe_query(sql_vol)
    if rows:
        profile["volumes"] = [
            {
                "table":    str(r.get("tablename", "")),
                "registros": int(r.get("registros", 0))
            }
            for r in rows
        ]

    _progress(55, "Detectando modulos ativos...")

    # Modulos ativos — matching parcial: verifica se o keyword esta contido no nome da tabela
    all_tables = set(r["table"].lower() for r in profile["schema"])
    detected = []
    for modulo, keywords in KNOWN_MODULES.items():
        for keyword in keywords:
            if any(keyword in tbl for tbl in all_tables):
                detected.append(modulo)
                break
    profile["modulos_detectados"] = detected

    _progress(65, "Verificando queries lentas...")

    # Queries lentas
    sql_slow = (
        "SELECT query, calls, mean_exec_time, total_exec_time "
        "FROM pg_stat_statements "
        "ORDER BY mean_exec_time DESC "
        "LIMIT 10"
    )
    rows, err = _safe_query(sql_slow)
    if rows and not err:
        profile["queries_lentas"] = [
            {
                "query":     str(r.get("query", ""))[:200],
                "calls":     int(r.get("calls", 0)),
                "mean_ms":   float(r.get("mean_exec_time", 0.0))
            }
            for r in rows
        ]

    _progress(75, "Verificando conexoes e locks...")

    # Conexoes ativas
    sql_conn = "SELECT count(*) AS cnt, state FROM pg_stat_activity GROUP BY state"
    rows, err = _safe_query(sql_conn)
    if rows:
        for row in rows:
            state = str(row.get("state", "outros"))
            cnt   = int(row.get("cnt", 0))
            profile["conexoes_ativas"][state if state != "None" else "idle"] = cnt

    # Locks ativos
    rows, err = _safe_query("SELECT count(*) AS cnt FROM pg_locks WHERE NOT granted")
    if rows:
        profile["locks_ativos"] = int(rows[0].get("cnt", 0))

    _progress(88, "Buscando erros recentes...")

    # Ultimos erros — tenta variantes conhecidas + matching parcial no schema
    _log_candidates = list(LOG_TABLE_VARIANTS)
    if rows_tbls:
        for tbl in existing:
            if any(k in tbl for k in ("log", "erro", "evento")):
                if tbl not in _log_candidates:
                    _log_candidates.insert(0, tbl)

    for log_table in _log_candidates:
        # Tenta ordenar por coluna de data (varia por tabela)
        for date_col in ("data_hora", "data", "created_at", "dt_registro", "timestamp"):
            sql_err = "SELECT * FROM {t} ORDER BY {c} DESC LIMIT 20".format(
                t=log_table, c=date_col)
            rows, err = _safe_query(sql_err)
            if rows and not err:
                profile["erros_recorrentes"] = [dict(r) for r in rows[:20]]
                break
        if profile["erros_recorrentes"]:
            break

    _progress(100, "Scan concluido.")
    return profile


def build_schema_summary(schema, max_tables=60):
    """
    Monta resumo legivel do schema para o prompt.
    Prioriza tabelas de negocio (fiscal, venda, estoque, financeiro, etc.)
    para garantir que estejam sempre no resumo enviado a IA.
    """
    # Palavras-chave de prioridade alta (tabelas de negocio essenciais)
    PRIORITY_KEYWORDS = [
        'notafiscal', 'nota_fiscal', 'nfce', 'nfe', 'nfse',
        'itemnotafiscal', 'venda', 'itemvenda', 'caixavenda',
        'produto', 'itemproduto', 'estoque', 'lote',
        'sngpc', 'controlado',
        'formulavenda', 'itemformulavenda',
        'compra', 'itemcompra', 'notafiscalentrada', 'itemnotafiscalentrada',
        'financeiro', 'contapagar', 'contareceber', 'titulo',
        'cliente', 'fornecedor', 'medico',
        'caixa', 'cupomfiscal', 'itemcupomfiscal',
        'manipulacao', 'producao', 'ordemproducao',
        'funcionario', 'usuario',
        'configuracoes', 'parametros', 'empresa',
    ]

    tables = {}
    for col in schema:
        t = col["table"]
        tables.setdefault(t, []).append("{0} ({1})".format(col["column"], col["type"]))

    def _priority(name):
        nl = name.lower()
        for i, kw in enumerate(PRIORITY_KEYWORDS):
            if kw in nl:
                return i
        return len(PRIORITY_KEYWORDS)

    sorted_tables = sorted(tables.items(), key=lambda x: (_priority(x[0]), x[0]))

    lines = []
    count = 0
    for table, cols in sorted_tables:
        if count >= max_tables:
            remaining = len(tables) - max_tables
            lines.append("... e mais {0} tabelas (use information_schema para descobrir)".format(remaining))
            break
        col_preview = ", ".join(cols[:10])
        if len(cols) > 10:
            col_preview += " ..."
        lines.append("{0}: {1}".format(table, col_preview))
        count += 1
    return "\n".join(lines)


def build_volumes_summary(volumes):
    lines = []
    for v in volumes[:15]:
        lines.append("{0}: {1:,} registros".format(v["table"], v["registros"]))
    return "\n".join(lines)
