"""
Sincronização e análise de chamados do Movidesk.
- sync_tickets(): baixa chamados fechados para cache local
- extract_knowledge(): usa IA para extrair problema+solução
- get_stats(): calcula estatísticas para o dashboard
- find_similar(): detecta chamados similares para alertar analistas
- get_analista_context(): sugere artigos baseado no histórico do analista
"""
import os
import json
import re
from collections import Counter
from datetime import datetime
from utils.paths import get_data_dir

_CACHE_FILE = "movidesk_tickets.json"
_sync_progress = {"running": False, "done": 0, "total": 0, "msg": ""}

_mem_cache = None          # cache em memória do JSON de tickets
_mem_cache_mtime = None    # mtime do arquivo quando foi carregado

# Cache da contagem ao vivo de tickets abertos por dono (TTL 5 min)
_open_count_cache = None
_open_count_ts    = 0.0
_OPEN_COUNT_TTL   = 300


def _cache_path():
    return os.path.join(get_data_dir(), _CACHE_FILE)


def _invalidate_mem_cache():
    global _mem_cache, _mem_cache_mtime
    _mem_cache = None
    _mem_cache_mtime = None


def load_cache():
    global _mem_cache, _mem_cache_mtime
    p = _cache_path()
    if not os.path.exists(p):
        return {"tickets": {}, "last_sync": None, "last_extraction": None}
    try:
        mtime = os.path.getmtime(p)
    except OSError:
        mtime = None
    # Retorna do cache em memória se o arquivo não mudou desde a última leitura
    if _mem_cache is not None and mtime == _mem_cache_mtime:
        return _mem_cache
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    _mem_cache = data
    _mem_cache_mtime = mtime
    return data


def _save_cache(data):
    with open(_cache_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    _invalidate_mem_cache()


def sync_progress():
    return dict(_sync_progress)


def sync_tickets(max_tickets=1000, date_from=None, date_to=None):
    """
    Sincroniza chamados fechados do Movidesk para cache local.
    date_from/date_to (YYYY-MM-DD): filtra na API — muito mais rápido que baixar tudo.
    """
    global _sync_progress

    periodo_str = ""
    if date_from or date_to:
        periodo_str = f" ({date_from or '?'} → {date_to or 'hoje'})"
    _sync_progress = {"running": True, "done": 0, "total": 0, "msg": f"Iniciando{periodo_str}..."}

    from utils.movidesk_client import fetch_tickets_page, fetch_resolved_page
    cache   = load_cache()
    top     = 50
    new_cnt = 0

    def _upsert(page):
        nonlocal new_cnt
        for t in page:
            tid    = str(t["id"])
            status = t.get("status", "")
            if tid in cache["tickets"]:
                cache["tickets"][tid]["status"]     = status
                cache["tickets"][tid]["resolvedIn"] = (t.get("resolvedIn") or "")[:10]
                cache["tickets"][tid]["closedIn"]   = (t.get("closedIn") or "")[:10]
                cache["tickets"][tid]["lastUpdate"]  = (t.get("lastUpdate") or "")[:10]
                # Atualiza owner_name para refletir reatribuições de chamados
                new_owner = ((t.get("owner") or {}).get("businessName") or "").strip()
                if new_owner:
                    cache["tickets"][tid]["owner_name"] = new_owner
                continue
            client = (t.get("clients") or [{}])[0]
            owner  = t.get("owner") or {}
            fechado = status in ("5 - Resolvido", "6 - Fechado")
            cache["tickets"][tid] = {
                "id":           tid,
                "subject":      t.get("subject", ""),
                "status":       status,
                "createdDate":  (t.get("createdDate") or "")[:10],
                "resolvedIn":   (t.get("resolvedIn") or "")[:10],
                "closedIn":     (t.get("closedIn") or "")[:10],
                "lastUpdate":   (t.get("lastUpdate") or "")[:10],
                "serviceFirst":  t.get("serviceFirstLevel", ""),
                "serviceSecond": t.get("serviceSecondLevel", ""),
                "client_name":  client.get("businessName", ""),
                "client_city":  client.get("city", ""),
                "owner_name":   owner.get("businessName", ""),
                "problema":     "",
                "solucao":      "",
                "extracted":    False if fechado else True,
            }
            new_cnt += 1

    try:
        # Passo 1: tickets criados no período (abertos + fechados)
        skip = 0
        while skip < max_tickets:
            _sync_progress["msg"] = f"Buscando abertos/criados — pág {skip // top + 1}{periodo_str}..."
            try:
                page = fetch_tickets_page(skip=skip, top=top,
                                          since_date=date_from, until_date=date_to)
            except Exception as e:
                _sync_progress["msg"] = f"Erro na API: {e}"
                break
            if not page:
                break
            _upsert(page)
            _sync_progress["done"] = skip + len(page)
            skip += top
            if len(page) < top:
                break

        # Passo 2: tickets resolvidos no período (podem ter sido criados antes)
        if date_from or date_to:
            skip = 0
            while skip < max_tickets:
                _sync_progress["msg"] = f"Buscando resolvidos no período — pág {skip // top + 1}..."
                try:
                    page = fetch_resolved_page(skip=skip, top=top,
                                               since_date=date_from, until_date=date_to)
                except Exception as e:
                    _sync_progress["msg"] = f"Erro (resolvidos): {e}"
                    break
                if not page:
                    break
                _upsert(page)
                skip += top
                if len(page) < top:
                    break

        cache["last_sync"] = datetime.now().isoformat()
        _save_cache(cache)
        _sync_progress["msg"] = f"Concluído. {new_cnt} novos chamados."

    except Exception as e:
        _sync_progress["msg"] = f"Erro: {e}"
    finally:
        _sync_progress["running"] = False
        _sync_progress["total"]   = new_cnt

    return new_cnt


def sync_open_tickets(max_tickets=2000):
    """
    Busca TODOS os chamados atualmente em aberto no Movidesk, sem filtro de data.
    Garante que tickets antigos ainda abertos (criados antes da janela de 90 dias)
    apareçam corretamente na fila do analista.
    """
    from utils.movidesk_client import fetch_open_tickets_page
    cache   = load_cache()
    skip    = 0
    top     = 50
    new_cnt = 0

    while skip < max_tickets:
        try:
            page = fetch_open_tickets_page(skip=skip, top=top)
        except Exception as e:
            break
        if not page:
            break
        for t in page:
            tid        = str(t["id"])
            client     = (t.get("clients") or [{}])[0]
            owner      = t.get("owner") or {}
            owner_name = (owner.get("businessName") or "").strip()
            status     = t.get("status", "")
            if tid in cache["tickets"]:
                cache["tickets"][tid]["status"]    = status
                cache["tickets"][tid]["lastUpdate"] = (t.get("lastUpdate") or "")[:10]
                if owner_name:
                    cache["tickets"][tid]["owner_name"] = owner_name
            else:
                cache["tickets"][tid] = {
                    "id":           tid,
                    "subject":      t.get("subject", ""),
                    "status":       status,
                    "createdDate":  (t.get("createdDate") or "")[:10],
                    "resolvedIn":   (t.get("resolvedIn") or "")[:10],
                    "closedIn":     (t.get("closedIn") or "")[:10],
                    "lastUpdate":   (t.get("lastUpdate") or "")[:10],
                    "serviceFirst":  t.get("serviceFirstLevel", ""),
                    "serviceSecond": t.get("serviceSecondLevel", ""),
                    "client_name":  client.get("businessName", ""),
                    "client_city":  client.get("city", ""),
                    "owner_name":   owner_name,
                    "problema":     "",
                    "solucao":      "",
                    "extracted":    True,
                }
                new_cnt += 1
        skip += top
        if len(page) < top:
            break

    _save_cache(cache)
    return new_cnt


def extract_knowledge(batch=20):
    """
    Usa IA para extrair problema+solução dos chamados ainda não processados.
    Retorna número de chamados processados.
    """
    from utils.movidesk_client import fetch_ticket_actions
    from ai.client import ask

    cache      = load_cache()
    pendentes  = [
        t for t in cache["tickets"].values()
        if not t.get("extracted") and t.get("status") == "6 - Fechado"
    ][:batch]

    if not pendentes:
        return 0

    count = 0
    for ticket in pendentes:
        try:
            actions = fetch_ticket_actions(int(ticket["id"]))
            convo   = "\n\n".join(
                f"[{a.get('status','')}] {(a.get('description') or '')[:600]}"
                for a in actions if a.get("description")
            )[:4000]

            if not convo.strip():
                cache["tickets"][ticket["id"]]["extracted"] = True
                continue

            system = "Você extrai problema e solução de chamados de suporte técnico. Responda somente com JSON válido."
            prompt = (
                f"Chamado #{ticket['id']}: {ticket['subject']}\n"
                f"Categoria: {ticket['serviceFirst']} > {ticket['serviceSecond']}\n\n"
                f"Conversa:\n{convo}\n\n"
                'Responda APENAS com JSON:\n'
                '{"problema": "descrição objetiva do problema em 1-2 frases", '
                '"solucao": "solução que resolveu o problema em 1-2 frases"}'
            )

            resp = ask(system, [{"role": "user", "content": prompt}])

            m = re.search(r'\{[\s\S]*?"problema"[\s\S]*?"solucao"[\s\S]*?\}', resp)
            if m:
                data = json.loads(m.group())
                cache["tickets"][ticket["id"]]["problema"] = (data.get("problema") or "")[:300]
                cache["tickets"][ticket["id"]]["solucao"]  = (data.get("solucao") or "")[:300]

            cache["tickets"][ticket["id"]]["extracted"] = True
            count += 1

        except Exception:
            cache["tickets"][ticket["id"]]["extracted"] = True

    cache["last_extraction"] = datetime.now().isoformat()
    _save_cache(cache)
    return count


def _filter_by_period(tickets, date_from=None, date_to=None):
    """Filtra por createdDate — mesma referência do Movidesk para 'chamados do período'."""
    if not date_from and not date_to:
        return tickets
    result = []
    for t in tickets:
        d = (t.get("createdDate") or "")[:10]
        if not d:
            continue
        if date_from and d < date_from:
            continue
        if date_to and d > date_to:
            continue
        result.append(t)
    return result


_STATUS_RESOLVIDO = {"5 - Resolvido", "6 - Fechado"}


def _is_aberto(t):
    """True se o chamado está em aberto (não resolvido, fechado, cancelado ou concluído)."""
    s = (t.get("status") or "").lower()
    return not any(x in s for x in ("resolvido", "fechado", "cancelado", "concluido", "concluído"))


def _get_resolve_date(t):
    """Data correta de encerramento conforme o status do chamado."""
    sl = (t.get("status") or "").lower()
    if "resolvido" in sl:
        return (t.get("resolvedIn") or t.get("lastUpdate") or "")[:10]
    if "fechado" in sl:
        return (t.get("closedIn") or t.get("resolvedIn") or t.get("lastUpdate") or "")[:10]
    return ""


def _feriados_nacionais(year):
    """Feriados nacionais brasileiros fixos + Sexta-feira Santa (variável)."""
    from datetime import date, timedelta
    feriados = {
        date(year, 1, 1),   # Confraternização Universal
        date(year, 4, 21),  # Tiradentes
        date(year, 5, 1),   # Dia do Trabalho
        date(year, 9, 7),   # Independência do Brasil
        date(year, 10, 12), # Nossa Senhora Aparecida
        date(year, 11, 2),  # Finados
        date(year, 11, 15), # Proclamação da República
        date(year, 12, 25), # Natal
    }
    # Easter (Anonymous Gregorian algorithm)
    a = year % 19; b = year // 100; c = year % 100
    d = b // 4; e = b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4; k = c % 4; l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day   = ((h + l - 7*m + 114) % 31) + 1
    easter = date(year, month, day)
    feriados.add(easter - timedelta(days=2))  # Sexta-feira Santa
    return feriados


def _dias_uteis_decorridos(today):
    """Conta dias úteis (Seg-Sex, exceto feriados nacionais) do início do mês até hoje."""
    from datetime import date as _date, timedelta
    start    = _date(today.year, today.month, 1)
    feriados = _feriados_nacionais(today.year)
    count    = 0
    d        = start
    while d <= today:
        if d.weekday() < 5 and d not in feriados:
            count += 1
        d += timedelta(days=1)
    return max(count, 1)


def _filter_resolved_in_period(tickets, date_from=None, date_to=None):
    """
    Filtra tickets resolvidos usando lastUpdate como critério principal —
    igual ao dashboard Movidesk ("Tickets resolvidos por agente responsável").
    Fallback: resolvedIn/closedIn quando lastUpdate está vazio.
    """
    result = []
    for t in tickets:
        if t.get("status") not in _STATUS_RESOLVIDO:
            continue
        d = (t.get("lastUpdate") or _get_resolve_date(t) or "")[:10]
        if not d:
            continue
        if date_from and d < date_from:
            continue
        if date_to and d > date_to:
            continue
        result.append(t)
    return result


def _analista_stats(tickets_recebidos, tickets_resolvidos):
    """Calcula estatísticas detalhadas por analista."""
    nomes = set(
        t["owner_name"] for t in tickets_recebidos + tickets_resolvidos
        if t.get("owner_name")
    )
    result = []
    for nome in nomes:
        rec = [t for t in tickets_recebidos if t.get("owner_name") == nome]
        res = [t for t in tickets_resolvidos if t.get("owner_name") == nome]

        tempos = []
        fora_sla = 0
        for t in res:
            c = _parse_date(t.get("createdDate"))
            r = _parse_date(t.get("lastUpdate") or t.get("resolvedIn"))
            if c and r and r >= c:
                d = (r - c).days
                if d <= 180:
                    tempos.append(d)
                    if d > 3:
                        fora_sla += 1

        result.append({
            "nome":       nome,
            "recebidos":  len(rec),
            "resolvidos": len(res),
            "media_dias": round(sum(tempos) / len(tempos), 1) if tempos else None,
            "fora_sla":   fora_sla,
            "sla_pct":    round(fora_sla / len(res) * 100, 1) if res else 0,
        })

    result.sort(key=lambda x: x["resolvidos"], reverse=True)
    return result


def get_stats(date_from=None, date_to=None, analista=None, categoria=None, grupo=None):
    """Retorna estatísticas consolidadas para o dashboard, filtradas por período."""
    cache       = load_cache()
    all_tickets = list(cache["tickets"].values())

    # Tickets do período por createdDate (= "chamados abertos no período")
    tickets = _filter_by_period(all_tickets, date_from, date_to)

    # Tickets resolvidos no período
    resolvidos = _filter_resolved_in_period(all_tickets, date_from, date_to)

    # Filtros opcionais — comparações case-insensitive para tolerar diferenças de capitalização
    if grupo:
        from utils.gestao_config import get_grupo_analistas
        membros = {m.lower() for m in get_grupo_analistas(grupo)}
        tickets    = [t for t in tickets    if (t.get("owner_name") or "").lower() in membros]
        resolvidos = [t for t in resolvidos if (t.get("owner_name") or "").lower() in membros]
    elif analista:
        an_low = analista.lower()
        tickets    = [t for t in tickets    if (t.get("owner_name") or "").lower() == an_low]
        resolvidos = [t for t in resolvidos if (t.get("owner_name") or "").lower() == an_low]
    else:
        # Sem filtro explícito: mostra só analistas conhecidos (grupos configurados)
        from utils.gestao_config import get_all_known_analistas
        known = {k.lower() for k in get_all_known_analistas()}
        if known:
            tickets    = [t for t in tickets    if (t.get("owner_name") or "").lower() in known]
            resolvidos = [t for t in resolvidos if (t.get("owner_name") or "").lower() in known]
    if categoria:
        cat_low = categoria.lower()
        tickets    = [t for t in tickets    if cat_low in (t.get("serviceSecond") or "").lower() or cat_low in (t.get("serviceFirst") or "").lower()]
        resolvidos = [t for t in resolvidos if cat_low in (t.get("serviceSecond") or "").lower() or cat_low in (t.get("serviceFirst") or "").lower()]

    from utils.gestao_config import get_grupo_for_ticket
    categorias = Counter(
        f"{t['serviceFirst']} > {t['serviceSecond']}"
        for t in tickets if t.get("serviceFirst") or t.get("serviceSecond")
    )
    # Top categorias com grupo sugerido para facilitar leitura no Top Demandas
    top_cats_raw = categorias.most_common(20)
    top_categorias_com_grupo = [
        {
            "cat":   cat,
            "count": cnt,
            "grupo": get_grupo_for_ticket(next(
                (t for t in tickets if f"{t.get('serviceFirst','')} > {t.get('serviceSecond','')}" == cat),
                {}
            )),
        }
        for cat, cnt in top_cats_raw
    ]

    farmacias = Counter(t["client_name"] for t in tickets if t.get("client_name"))
    analistas_recebidos  = Counter(t["owner_name"] for t in tickets    if t.get("owner_name"))
    analistas_resolvidos = Counter(t["owner_name"] for t in resolvidos if t.get("owner_name"))

    # Estatísticas detalhadas por analista
    analistas_detalhe = _analista_stats(tickets, resolvidos)

    # Recorrência (mesma farmácia + categoria, no período)
    recorrencia_map = {}
    for t in tickets:
        key = f"{t['client_name']}|{t['serviceSecond']}"
        recorrencia_map.setdefault(key, []).append(t)
    recorrentes = sum(1 for v in recorrencia_map.values() if len(v) >= 2)

    extraidos        = sum(1 for t in all_tickets if t.get("extracted") and (t.get("problema") or t.get("solucao")))
    abertos_periodo  = sum(1 for t in tickets if t.get("status") not in _STATUS_RESOLVIDO)
    fechados_periodo = len(resolvidos)

    return {
        "total":                    len(all_tickets),
        "total_periodo":            len(tickets),
        "abertos_periodo":          abertos_periodo,
        "fechados_periodo":         fechados_periodo,
        "extraidos":                extraidos,
        "recorrentes":              recorrentes,
        "last_sync":                cache.get("last_sync"),
        "last_extraction":          cache.get("last_extraction"),
        "top_categorias":           categorias.most_common(20),
        "top_categorias_com_grupo": top_categorias_com_grupo,
        "top_farmacias":            farmacias.most_common(20),
        "top_analistas":            analistas_recebidos.most_common(20),
        "top_analistas_resolvidos": analistas_resolvidos.most_common(20),
        "analistas_detalhe":        analistas_detalhe,
        "date_from":                date_from,
        "date_to":                  date_to,
    }


def get_filter_options():
    """Retorna listas únicas de analistas, categorias e farmácias para os filtros."""
    cache   = load_cache()
    tickets = list(cache["tickets"].values())
    analistas  = sorted({t["owner_name"]  for t in tickets if t.get("owner_name")})
    categorias = sorted({t["serviceSecond"] for t in tickets if t.get("serviceSecond")})
    farmacias  = sorted({t["client_name"]  for t in tickets if t.get("client_name")})
    return {"analistas": analistas, "categorias": categorias, "farmacias": farmacias}


def get_tickets_list(page=0, per_page=50, search="", analista="", categoria="",
                     date_from=None, date_to=None):
    """Retorna lista paginada de chamados para a tabela."""
    cache   = load_cache()
    tickets = _filter_by_period(list(cache["tickets"].values()), date_from, date_to)

    # Filtros
    if search:
        sl = search.lower()
        tickets = [
            t for t in tickets
            if sl in t.get("subject", "").lower()
            or sl in t.get("client_name", "").lower()
            or sl in t.get("problema", "").lower()
            or sl in t.get("solucao", "").lower()
        ]
    if analista:
        tickets = [t for t in tickets if t.get("owner_name") == analista]
    if categoria:
        tickets = [t for t in tickets if categoria in t.get("serviceSecond", "")]

    # Mais recentes primeiro
    tickets.sort(key=lambda t: t.get("resolvedIn", "") or "", reverse=True)

    total  = len(tickets)
    offset = page * per_page
    return {"total": total, "tickets": tickets[offset: offset + per_page]}


def find_similar(subject, client_name=None, limit=3):
    """Encontra chamados similares — para alertar analistas no chat."""
    cache   = load_cache()
    tickets = [
        t for t in cache["tickets"].values()
        if t.get("extracted") and t.get("status") in _STATUS_RESOLVIDO
    ]

    from utils.knowledge_search import _tokenize
    tokens = _tokenize(subject)
    if not tokens:
        return []

    scored = []
    for t in tickets:
        text  = (t.get("problema", "") + " " + t.get("subject", "")).lower()
        score = sum(1 for tok in tokens if len(tok) >= 4 and tok in text)
        if client_name and t.get("client_name") == client_name:
            score *= 3
        if score >= 2:
            scored.append((score, t))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored[:limit]]


def get_analista_context(analista_name):
    """Retorna top categorias do analista para injetar como contexto no prompt."""
    cache   = load_cache()
    tickets = [t for t in cache["tickets"].values() if t.get("owner_name") == analista_name]
    if not tickets:
        return ""

    cats = Counter(
        f"{t['serviceFirst']} > {t['serviceSecond']}"
        for t in tickets if t.get("serviceFirst")
    ).most_common(5)

    if not cats:
        return ""

    linhas = "\n".join(f"- {cat} ({n} chamados)" for cat, n in cats)
    return f"Histórico do analista {analista_name} — áreas mais atendidas:\n{linhas}"


# ── Analytics avançados para análise por IA ───────────────────────────────────

def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s[:10])
    except Exception:
        return None


def _days_to_resolve(t):
    c = _parse_date(t.get("createdDate"))
    r = _parse_date(t.get("resolvedIn"))
    if c and r and r >= c:
        delta = (r - c).days
        return delta if delta <= 180 else None  # ignora outliers > 6 meses
    return None


_STOPWORDS_CHAT = {
    "que", "para", "com", "uma", "por", "dos", "das", "nos", "nas", "seu", "sua",
    "nao", "mais", "como", "mas", "foi", "ele", "ela", "isso", "esse", "essa",
    "este", "esta", "tem", "ter", "ser", "ver", "qual", "quando", "onde", "voce",
    "pelo", "pela", "pode", "deve", "caso", "tipo", "vez", "esta", "estao",
    "sistema", "farmafacil", "farma", "erro", "favor", "bom", "dia",
}


def _keywords_from_subjects(subjects, top_n=8):
    """Extrai palavras-chave mais frequentes de uma lista de assuntos de chamados."""
    words = Counter()
    for s in subjects:
        for w in re.findall(r'\b[a-záéíóúâêîôûãõçàü]{4,}\b', s.lower()):
            if w not in _STOPWORDS_CHAT:
                words[w] += 1
    return [w for w, _ in words.most_common(top_n)]


def get_detailed_stats(date_from=None, date_to=None, days=30):
    """
    Retorna estatísticas detalhadas para o módulo de análise IA:
    - Volume geral e por período
    - Tempo médio de resolução por analista e categoria
    - Chamados fora do SLA (> 3 dias)
    - Tendência semanal
    - Farmácias com problemas recorrentes
    - Assuntos e palavras-chave por categoria
    """
    from datetime import timedelta, date as date_type
    cache   = load_cache()
    tickets = list(cache["tickets"].values())

    hoje = datetime.now().date()

    # Usa date_from/date_to se fornecidos, senão usa days
    if date_from:
        corte_dt = date_type.fromisoformat(date_from)
    else:
        corte_dt = hoje - timedelta(days=days)

    fim_dt = date_type.fromisoformat(date_to) if date_to else hoje

    # Período anterior de mesmo tamanho (para comparação de tendência)
    span        = (fim_dt - corte_dt).days or 1
    ant_fim     = corte_dt - timedelta(days=1)
    ant_inicio  = ant_fim  - timedelta(days=span)

    semana     = hoje - timedelta(days=7)
    semana_ant = hoje - timedelta(days=14)

    def _in_range(t, d_from, d_to):
        d = _parse_date(t.get("resolvedIn"))
        return d and d_from <= d.date() <= d_to

    recentes    = [t for t in tickets if _in_range(t, corte_dt, fim_dt)]
    periodo_ant = [t for t in tickets if _in_range(t, ant_inicio, ant_fim)]
    esta_semana = [t for t in tickets if _in_range(t, semana, hoje)]
    sem_passada = [t for t in tickets if _in_range(t, semana_ant, semana - timedelta(days=1))]

    # Tempo médio por analista
    analista_tempo = {}
    for t in recentes:
        nome = t.get("owner_name", "Sem analista")
        d    = _days_to_resolve(t)
        if d is not None:
            analista_tempo.setdefault(nome, []).append(d)
    analista_stats = {
        nome: {
            "total":    len(dias),
            "media_dias": round(sum(dias) / len(dias), 1),
            "fora_sla": sum(1 for d in dias if d > 3),
        }
        for nome, dias in analista_tempo.items() if dias
    }
    analista_stats_sorted = sorted(
        analista_stats.items(), key=lambda x: x[1]["total"], reverse=True
    )

    # Tempo médio por categoria
    cat_tempo = {}
    for t in recentes:
        cat = f"{t.get('serviceFirst','')} > {t.get('serviceSecond','')}"
        d   = _days_to_resolve(t)
        if d is not None:
            cat_tempo.setdefault(cat, []).append(d)
    cat_stats = {
        cat: round(sum(dias) / len(dias), 1)
        for cat, dias in cat_tempo.items() if dias
    }

    # Chamados fora do SLA (> 3 dias) no período
    fora_sla = [t for t in recentes if (_days_to_resolve(t) or 0) > 3]

    # Tendência: período atual vs período anterior de mesmo tamanho
    cats_atual = Counter(t.get("serviceSecond","") for t in recentes)
    cats_ant   = Counter(t.get("serviceSecond","") for t in periodo_ant)
    tendencias = {}
    for cat in set(list(cats_atual.keys()) + list(cats_ant.keys())):
        atual = cats_atual.get(cat, 0)
        ant   = cats_ant.get(cat, 0)
        if atual > 0:
            tendencias[cat] = {"atual": atual, "anterior": ant, "delta": atual - ant}

    # Farmácias com > 1 chamado no período
    farm_recentes = Counter(t.get("client_name","") for t in recentes if t.get("client_name"))
    farm_criticas = {k: v for k, v in farm_recentes.items() if v >= 2}

    crescimento = sorted(
        [(cat, d["delta"]) for cat, d in tendencias.items() if d["delta"] > 0],
        key=lambda x: x[1], reverse=True
    )[:5]

    # Agrupa subjects, problemas e soluções por categoria para dar contexto real à IA
    from collections import defaultdict
    cat_subjects  = defaultdict(list)
    cat_pares     = defaultdict(list)
    for t in recentes:
        cat  = (t.get("serviceSecond") or t.get("serviceFirst") or "Sem categoria").strip()
        subj = (t.get("subject") or "").strip()
        if subj:
            cat_subjects[cat].append(subj)
        prob = (t.get("problema") or "").strip()
        sol  = (t.get("solucao")  or "").strip()
        if prob or sol:
            cat_pares[cat].append({"problema": prob, "solucao": sol})

    top_cats_list = Counter(
        (t.get("serviceSecond") or t.get("serviceFirst") or "Sem categoria").strip()
        for t in recentes
    ).most_common(8)

    cat_detalhes = {}
    for cat, count in top_cats_list:
        subjects_list = cat_subjects.get(cat, [])
        cat_detalhes[cat] = {
            "count":     count,
            "subjects":  subjects_list[:8],
            "keywords":  _keywords_from_subjects(subjects_list),
            "pares":     cat_pares.get(cat, [])[:5],
        }

    return {
        "hoje":               str(hoje),
        "date_from":          str(corte_dt),
        "date_to":            str(fim_dt),
        "periodo_dias":       span,
        "total_geral":        len(tickets),
        "total_periodo":      len(recentes),
        "periodo_anterior":   len(periodo_ant),
        "esta_semana":        len(esta_semana),
        "semana_passada":     len(sem_passada),
        "fora_sla_count":     len(fora_sla),
        "fora_sla_pct":       round(len(fora_sla) / len(recentes) * 100, 1) if recentes else 0,
        "analistas":          analista_stats_sorted,
        "top_categorias":     Counter(t.get("serviceSecond","") for t in recentes if t.get("serviceSecond")).most_common(10),
        "cat_tempo_medio":    sorted(cat_stats.items(), key=lambda x: x[1], reverse=True)[:10],
        "tendencias":         tendencias,
        "crescimento_semana": crescimento,
        "farmacias_criticas": sorted(farm_criticas.items(), key=lambda x: x[1], reverse=True)[:10],
        "cat_detalhes":       cat_detalhes,
    }


def get_analista_tickets(movidesk_name):
    """
    Retorna chamados em aberto do analista (por nome no Movidesk), ordenados
    por urgência — mais antigo primeiro.
    """
    if not movidesk_name:
        return []
    cache   = load_cache()
    name_lw = movidesk_name.lower()
    tickets = [
        t for t in cache["tickets"].values()
        if _is_aberto(t)
        and (t.get("owner_name") or "").lower() == name_lw
    ]
    tickets.sort(key=lambda t: t.get("createdDate") or "")
    return tickets


def get_respostas_rapidas(limit=20):
    """
    Retorna as soluções mais usadas por categoria a partir dos chamados extraídos.
    Útil para a base de respostas rápidas do analista.
    """
    cache = load_cache()
    from collections import defaultdict
    cat_solucoes = defaultdict(list)
    for t in cache["tickets"].values():
        if t.get("extracted") and t.get("solucao"):
            cat = t.get("serviceSecond") or t.get("serviceFirst") or "Geral"
            cat_solucoes[cat].append(t["solucao"])

    result = []
    for cat, solucoes in cat_solucoes.items():
        freq = Counter(solucoes)
        for sol, count in freq.most_common(3):
            result.append({"categoria": cat, "solucao": sol, "frequencia": count})

    result.sort(key=lambda x: x["frequencia"], reverse=True)
    return result[:limit]


def get_chamados_duplicados(so_abertos=True, grupo=None):
    """
    Detecta chamados em aberto da mesma farmácia sobre assuntos similares.
    Agrupa por similaridade de tokens no subject OU mesma categoria.
    Objetivo: diminuir fila identificando tickets redundantes para cancelar.
    so_abertos=True: ignora resolvidos, fechados E cancelados.
    grupo: filtra por equipe (Fiscal, Producao, G1). None = todos.
    """
    from utils.knowledge_search import _tokenize
    cache   = load_cache()
    tickets = list(cache["tickets"].values())
    if so_abertos:
        tickets = [t for t in tickets if _is_aberto(t)]

    if grupo:
        from utils.gestao_config import get_grupo_analistas
        membros = {m.lower() for m in get_grupo_analistas(grupo)}
        tickets = [t for t in tickets if (t.get("owner_name") or "").lower() in membros]

    # 1. Agrupa por farmácia
    por_cliente: dict = {}
    for t in tickets:
        nome = (t.get("client_name") or "").strip()
        if not nome:
            continue
        por_cliente.setdefault(nome, []).append(t)

    duplicados = []
    for nome, ts in por_cliente.items():
        if len(ts) < 2:
            continue

        # 2. Dentro de cada farmácia, agrupa por similaridade de assunto ou mesma categoria
        assigned = [False] * len(ts)
        for i in range(len(ts)):
            if assigned[i]:
                continue
            cluster = [i]
            assigned[i] = True
            tok_i  = {tok for tok in _tokenize(ts[i].get("subject", "")) if len(tok) >= 3}
            cat_i  = (ts[i].get("serviceSecond") or ts[i].get("serviceFirst") or "").strip().lower()

            for j in range(i + 1, len(ts)):
                if assigned[j]:
                    continue
                tok_j  = {tok for tok in _tokenize(ts[j].get("subject", "")) if len(tok) >= 3}
                cat_j  = (ts[j].get("serviceSecond") or ts[j].get("serviceFirst") or "").strip().lower()
                same_cat    = bool(cat_i and cat_i == cat_j)
                tok_overlap = bool(tok_i and tok_j and len(tok_i & tok_j) >= 1)
                if same_cat or tok_overlap:
                    cluster.append(j)
                    assigned[j] = True

            if len(cluster) >= 2:
                grupo_tickets = [ts[k] for k in cluster]
                ts_sorted = sorted(grupo_tickets, key=lambda x: x.get("createdDate") or "")
                cat_rep = (ts_sorted[0].get("serviceSecond") or ts_sorted[0].get("serviceFirst") or "").strip()
                duplicados.append({
                    "client_name":  nome,
                    "categoria":    cat_rep,
                    "count":        len(grupo_tickets),
                    "mais_antigo":  ts_sorted[0],
                    "mais_recente": ts_sorted[-1],
                    "tickets":      ts_sorted,
                })

    duplicados.sort(key=lambda x: x["count"], reverse=True)
    return duplicados


def sync_tickets_historical(date_from=None, date_to=None, max_tickets=1000):
    """
    Sync via endpoint /tickets/past — chamados criados há mais de 90 dias.
    Usa createdDate como filtro. Não sobrescreve tickets já existentes no cache.
    """
    from utils.movidesk_client import fetch_tickets_past_created
    cache   = load_cache()
    top     = 50
    new_cnt = 0

    def _upsert_past(page):
        nonlocal new_cnt
        for t in page:
            tid = str(t["id"])
            if tid in cache["tickets"]:
                # Atualiza apenas status/datas se já existe
                cache["tickets"][tid]["status"]     = t.get("status", cache["tickets"][tid]["status"])
                cache["tickets"][tid]["resolvedIn"] = (t.get("resolvedIn") or "")[:10] or cache["tickets"][tid]["resolvedIn"]
                cache["tickets"][tid]["lastUpdate"]  = (t.get("lastUpdate") or "")[:10] or cache["tickets"][tid]["lastUpdate"]
                continue
            client  = (t.get("clients") or [{}])[0]
            owner   = t.get("owner") or {}
            status  = t.get("status", "")
            fechado = status in ("5 - Resolvido", "6 - Fechado")
            cache["tickets"][tid] = {
                "id":           tid,
                "subject":      t.get("subject", ""),
                "status":       status,
                "createdDate":  (t.get("createdDate") or "")[:10],
                "resolvedIn":   (t.get("resolvedIn") or "")[:10],
                "closedIn":     (t.get("closedIn") or "")[:10],
                "lastUpdate":   (t.get("lastUpdate") or "")[:10],
                "serviceFirst":  t.get("serviceFirstLevel", ""),
                "serviceSecond": t.get("serviceSecondLevel", ""),
                "client_name":  client.get("businessName", ""),
                "client_city":  client.get("city", ""),
                "owner_name":   owner.get("businessName", ""),
                "problema":     "",
                "solucao":      "",
                "extracted":    not fechado,
            }
            new_cnt += 1

    skip = 0
    while skip < max_tickets:
        try:
            page = fetch_tickets_past_created(skip=skip, top=top,
                                              since_date=date_from, until_date=date_to)
        except Exception:
            break
        if not page:
            break
        _upsert_past(page)
        skip += top
        if len(page) < top:
            break

    _save_cache(cache)
    return new_cnt


def _fetch_entradas_mes_api(yr, mo):
    """
    Busca contagem de entradas por owner diretamente na API do Movidesk para um mês completo.
    Retorna dict {owner_name: count}.
    """
    import calendar as _cal
    from datetime import date as _date
    from utils.movidesk_client import fetch_tickets_page

    _, last_day = _cal.monthrange(yr, mo)
    date_from = _date(yr, mo, 1).isoformat()
    date_to   = _date(yr, mo, last_day).isoformat()

    entries_by_owner: dict = {}
    skip = 0
    top  = 100
    while True:
        try:
            page = fetch_tickets_page(skip=skip, top=top,
                                      since_date=date_from, until_date=date_to)
        except Exception:
            break
        if not page:
            break
        for t in page:
            owner = ((t.get("owner") or {}).get("businessName") or "").strip()
            if owner:
                entries_by_owner[owner] = entries_by_owner.get(owner, 0) + 1
        skip += top
        if len(page) < top:
            break
    return entries_by_owner


def sync_meta_entradas_historico(months_back=3):
    """
    Força re-fetch das contagens de entradas mensais via API para os últimos N meses.
    Armazena em cache['meta_entradas'][YYYY-MM] = {owners: {name: count}, updated_at: ...}
    """
    from datetime import datetime
    cache = load_cache()
    hoje  = datetime.now().date()

    def _prev_months(n):
        result = []
        y, m = hoje.year, hoje.month
        for _ in range(n):
            result.append((y, m))
            m -= 1
            if m == 0:
                m = 12
                y -= 1
        return result

    if "meta_entradas" not in cache:
        cache["meta_entradas"] = {}

    resultado = {}
    for (yr, mo) in _prev_months(months_back):
        key            = f"{yr}-{mo:02d}"
        owner_counts   = _fetch_entradas_mes_api(yr, mo)
        cache["meta_entradas"][key] = {
            "owners":     owner_counts,
            "updated_at": datetime.now().isoformat(),
        }
        resultado[key] = sum(owner_counts.values())

    _save_cache(cache)
    return resultado


def get_metas_por_equipe(semanas_alvo=4):
    """
    Metas baseadas em ENTRADAS mensais por equipe.
    Meta = entradas_do_mes / n_analistas / DIAS_UTEIS → chamados/dia para não crescer a fila.
    Exibe histórico dos últimos 3 meses para contextualizar picos (incidentes, versões).

    Estratégia de contagem de entradas:
      - Mês atual (parcial): usa cache local com createdDate <= hoje (igual à aba Analistas)
      - Meses anteriores: usa cache["meta_entradas"] (pré-fetchado via API). Se não disponível,
        busca da API on-demand e salva no cache.
    """
    import calendar as _cal
    import time as _time
    from datetime import datetime, timedelta
    from datetime import date as _date
    from utils.gestao_config import get_grupo_analistas

    cache       = load_cache()
    all_tickets = list(cache["tickets"].values())
    hoje        = datetime.now().date()
    DIAS_UTEIS  = 22  # dias úteis por mês

    # Fila ao vivo — busca da API com cache de 5 min
    global _open_count_cache, _open_count_ts
    now_ts = _time.time()
    if _open_count_cache is None or (now_ts - _open_count_ts) > _OPEN_COUNT_TTL:
        try:
            from utils.movidesk_client import count_open_by_owner
            _open_count_cache = count_open_by_owner()
            _open_count_ts    = now_ts
        except Exception:
            _open_count_cache = {}
    open_by_owner = _open_count_cache
    cache_dirty = False  # se precisarmos salvar cache no final

    def _prev_months(n):
        result = []
        y, m = hoje.year, hoje.month
        for _ in range(n):
            result.append((y, m))
            m -= 1
            if m == 0:
                m = 12
                y -= 1
        return list(reversed(result))

    meses_ref = _prev_months(3)

    def _entradas_mes_cache(tickets_g, yr, mo):
        """Conta entradas do mês usando cache local (para mês atual, usa date_to=hoje)."""
        s = _date(yr, mo, 1).isoformat()
        e = hoje.isoformat()  # sempre usa hoje como teto — igual à aba Analistas
        return [t for t in tickets_g if s <= (t.get("createdDate") or "")[:10] <= e]

    def _entradas_mes_api_cached(yr, mo):
        """
        Retorna dict {owner_name: count} para um mês completo.
        Usa cache['meta_entradas'] se disponível; caso contrário, busca da API.
        """
        nonlocal cache_dirty
        key      = f"{yr}-{mo:02d}"
        meta_ent = cache.get("meta_entradas", {})
        if key in meta_ent:
            return meta_ent[key].get("owners", {})
        # Não está no cache — busca da API
        owner_counts = _fetch_entradas_mes_api(yr, mo)
        if "meta_entradas" not in cache:
            cache["meta_entradas"] = {}
        cache["meta_entradas"][key] = {
            "owners":     owner_counts,
            "updated_at": datetime.now().isoformat(),
        }
        cache_dirty = True
        return owner_counts

    from utils.gestao_config import get_excluir_metas
    excluir = get_excluir_metas()

    resultado = []
    for grupo in ['Fiscal', 'Producao', 'G1', 'GW', 'Ouvidoria']:
        membros = {mb.lower() for mb in get_grupo_analistas(grupo)}
        if not membros:
            continue
        membros_metas = membros - excluir  # exclui líderes do cálculo
        n_analistas = max(len(membros_metas), 1)

        tickets_grupo = [t for t in all_tickets
                         if (t.get("owner_name") or "").lower() in membros]
        # Tickets só dos analistas que entram na meta (exclui líderes)
        tickets_metas = [t for t in all_tickets
                         if (t.get("owner_name") or "").lower() in membros_metas]

        # Fila ao vivo (API Movidesk) — números precisos
        fila = sum(open_by_owner.get(mb, 0) for mb in membros_metas)
        # Lista do cache apenas para top_cats e nome_map (não usada nos contadores)
        abertos = [t for t in tickets_metas if _is_aberto(t)]

        # Histórico mensal (últimos 3 meses)
        dias_uteis_dec = _dias_uteis_decorridos(hoje)
        historico_meses = []
        for (yr, mo) in meses_ref:
            label   = _date(yr, mo, 1).strftime('%b/%Y')
            parcial = (yr == hoje.year and mo == hoje.month)

            if parcial:
                # Mês atual: usa cache local com date_to=hoje (bate com aba Analistas)
                ents  = _entradas_mes_cache(tickets_metas, yr, mo)
                n_ent = len(ents)
                eq_dia = round(n_ent / n_analistas / dias_uteis_dec, 1) if n_ent > 0 else 0
            else:
                # Meses anteriores: usa API (via cache ou fetch on-demand)
                owner_counts = _entradas_mes_api_cached(yr, mo)
                n_ent = sum(v for owner, v in owner_counts.items()
                            if owner.lower() in membros_metas)
                eq_dia = round(n_ent / n_analistas / DIAS_UTEIS, 1) if n_ent > 0 else 0

            historico_meses.append({
                "label":          label,
                "ano":            yr,
                "mes":            mo,
                "entradas":       n_ent,
                "entradas_proj":  n_ent,
                "parcial":        parcial,
                "equilibrio_dia": eq_dia,
            })

        # Média dos meses completos
        meses_comp = [mh for mh in historico_meses if not mh["parcial"]]
        media_ent  = round(sum(mh["entradas"] for mh in meses_comp) / max(len(meses_comp), 1))
        for mh in historico_meses:
            mh["acima_media"] = mh["entradas_proj"] > media_ent * 1.25
            mh["pct_vs_media"] = round((mh["entradas_proj"] / media_ent - 1) * 100) if media_ent > 0 else 0

        # Meta base = mês atual (projetado); fallback: mês anterior
        mes_atual      = historico_meses[-1]
        equilibrio_dia = mes_atual["equilibrio_dia"] or (
            historico_meses[-2]["equilibrio_dia"] if len(historico_meses) >= 2 else 0
        )

        # Ritmo atual — baseado no MÊS CORRENTE (do dia 1 até hoje)
        # dias_uteis_dec já calculado acima para o historico
        mes_s           = _date(hoje.year, hoje.month, 1).isoformat()
        mes_e           = hoje.isoformat()

        fechados_mes_g  = [
            t for t in tickets_metas
            if t.get("status") in _STATUS_RESOLVIDO
            and mes_s <= (t.get("lastUpdate") or _get_resolve_date(t) or "") <= mes_e
        ]
        n_fechados_mes    = len(fechados_mes_g)
        taxa_dia_equipe   = round(n_fechados_mes / dias_uteis_dec, 1)
        taxa_dia_analista = round(taxa_dia_equipe / n_analistas, 2)
        taxa_sem_equipe   = round(taxa_dia_equipe * 5, 1)
        entrada_sem       = round(mes_atual["entradas_proj"] / 4.3, 1)
        saldo_sem         = round(taxa_sem_equipe - entrada_sem, 1)

        ritmo_ok = taxa_dia_analista >= equilibrio_dia
        status   = ("reduzindo" if taxa_dia_analista > equilibrio_dia
                    else ("crescendo" if taxa_dia_analista < equilibrio_dia * 0.9 else "estavel"))

        top_cats = Counter(
            (t.get("serviceSecond") or t.get("serviceFirst") or "Sem categoria")
            for t in abertos
        ).most_common(5)

        # Stats por analista
        nome_map = {}
        for t in abertos + fechados_mes_g:
            n = t.get("owner_name") or ""
            if n:
                nome_map[n.lower()] = n

        membros_stats = []
        for mb in membros_metas:
            nome_d        = nome_map.get(mb, mb.title())
            mb_fila       = open_by_owner.get(mb, 0)
            mb_fechou_mes = sum(1 for t in fechados_mes_g if (t.get("owner_name") or "").lower() == mb)
            mb_taxa_dia   = round(mb_fechou_mes / dias_uteis_dec, 2)
            membros_stats.append({
                "nome":       nome_d,
                "fila":       mb_fila,
                "fechou_mes": mb_fechou_mes,
                "dias_uteis": dias_uteis_dec,
                "taxa_dia":   mb_taxa_dia,
                "meta_dia":   equilibrio_dia,
                "atingiu":    mb_taxa_dia >= equilibrio_dia,
            })
        membros_stats.sort(key=lambda x: x["fila"], reverse=True)

        # Última atualização dos dados históricos
        hist_updated = None
        meta_ent_cache = cache.get("meta_entradas", {})
        for (yr2, mo2) in meses_ref:
            if not (yr2 == hoje.year and mo2 == hoje.month):
                key2 = f"{yr2}-{mo2:02d}"
                if key2 in meta_ent_cache:
                    hist_updated = meta_ent_cache[key2].get("updated_at")
                    break

        resultado.append({
            "grupo":              grupo,
            "membros_count":      n_analistas,
            "membros":            membros_stats,
            "fila_total":         fila,
            "historico_meses":    historico_meses,
            "media_entradas_mes": media_ent,
            "equilibrio_dia":     equilibrio_dia,
            "taxa_dia_analista":  taxa_dia_analista,
            "taxa_dia_equipe":    taxa_dia_equipe,
            "taxa_sem_equipe":    taxa_sem_equipe,
            "dias_uteis_dec":     dias_uteis_dec,
            "fechados_mes":       n_fechados_mes,
            "hist_updated":       hist_updated,
            "ritmo_ok":           ritmo_ok,
            "status":             status,
            "top_categorias":     top_cats,
            "semanas_alvo":       semanas_alvo,
            # Campos legados (compatibilidade)
            "taxa_semana":        taxa_sem_equipe,
            "meta_semana":        round(equilibrio_dia * 5 * n_analistas, 1),
            "meta_dia_equipe":    round(equilibrio_dia * n_analistas, 1),
            "meta_por_analista_dia": equilibrio_dia,
            "entrada_semana":     entrada_sem,
            "saldo_semana":       saldo_sem,
            "resolvidos_30d":     n_fechados_mes,
        })

    # Salva cache se buscamos dados novos da API
    if cache_dirty:
        _save_cache(cache)

    return resultado


def get_metas_por_grupo(grupo=None, semanas_alvo=4):
    """
    Calcula meta semanal de fechamentos por analista para reduzir a fila em
    `semanas_alvo` semanas, com base nos chamados dos últimos 30 dias.
    Retorna lista ordenada por fila_atual (desc).
    """
    from datetime import datetime, timedelta
    cache       = load_cache()
    all_tickets = list(cache["tickets"].values())
    hoje        = datetime.now().date()
    data_30d    = (hoje - timedelta(days=30)).isoformat()

    if grupo:
        from utils.gestao_config import get_grupo_analistas
        membros = {m.lower() for m in get_grupo_analistas(grupo)}
    else:
        from utils.gestao_config import get_all_known_analistas
        membros = {k.lower() for k in get_all_known_analistas()}

    if not membros:
        return []

    abertos_all = [t for t in all_tickets
                   if t.get("status") not in _STATUS_RESOLVIDO
                   and (t.get("owner_name") or "").lower() in membros]
    fila_por = Counter(t["owner_name"] for t in abertos_all if t.get("owner_name"))

    res_30d = _filter_resolved_in_period(all_tickets, date_from=data_30d)
    res_30d = [t for t in res_30d if (t.get("owner_name") or "").lower() in membros]
    res_por = Counter(t["owner_name"] for t in res_30d if t.get("owner_name"))

    rec_30d = _filter_by_period(all_tickets, date_from=data_30d)
    rec_30d = [t for t in rec_30d if (t.get("owner_name") or "").lower() in membros]
    rec_por = Counter(t["owner_name"] for t in rec_30d if t.get("owner_name"))

    nomes = {t["owner_name"] for t in abertos_all + res_30d if t.get("owner_name")}

    resultado = []
    for nome in sorted(nomes):
        fila          = fila_por.get(nome, 0)
        resolvidos    = res_por.get(nome, 0)
        recebidos     = rec_por.get(nome, 0)
        taxa_semana   = round(resolvidos / 4.3, 1)
        entrada_semana = round(recebidos / 4.3, 1)
        saldo_semana  = round(taxa_semana - entrada_semana, 1)
        meta_semana   = round(fila / max(semanas_alvo, 1) + entrada_semana, 1)
        meta_dia      = round(meta_semana / 5, 1)

        if saldo_semana > 0:
            status = 'reduzindo'
        elif saldo_semana < -1:
            status = 'crescendo'
        else:
            status = 'estavel'

        resultado.append({
            "nome":                  nome,
            "fila_atual":            fila,
            "resolvidos_30d":        resolvidos,
            "recebidos_30d":         recebidos,
            "taxa_resolucao_semana": taxa_semana,
            "entrada_semana":        entrada_semana,
            "saldo_semana":          saldo_semana,
            "meta_semana":           meta_semana,
            "meta_dia":              meta_dia,
            "semanas_alvo":          semanas_alvo,
            "status":                status,
        })

    resultado.sort(key=lambda x: x["fila_atual"], reverse=True)
    return resultado


def get_sazonalidade(date_from=None, date_to=None, agrupamento='semana', grupo=None):
    """
    Agrupa chamados abertos (por createdDate) por semana ou mês.
    Retorna lista cronológica para análise de picos e tendências.
    """
    from datetime import timedelta
    cache       = load_cache()
    all_tickets = list(cache["tickets"].values())

    if grupo:
        from utils.gestao_config import get_grupo_analistas
        membros = {m.lower() for m in get_grupo_analistas(grupo)}
        all_tickets = [t for t in all_tickets
                       if (t.get("owner_name") or "").lower() in membros]
    else:
        from utils.gestao_config import get_all_known_analistas
        known = {k.lower() for k in get_all_known_analistas()}
        if known:
            all_tickets = [t for t in all_tickets
                           if (t.get("owner_name") or "").lower() in known]

    tickets  = _filter_by_period(all_tickets, date_from, date_to)
    periodos: dict = {}

    for t in tickets:
        d = _parse_date(t.get("createdDate"))
        if not d:
            continue
        d = d.date()
        if agrupamento == 'mes':
            key   = d.strftime('%Y-%m')
            label = d.strftime('%b/%Y')
        else:
            monday = d - timedelta(days=d.weekday())
            key    = monday.strftime('%Y-%m-%d')
            label  = monday.strftime('%d/%m')

        if key not in periodos:
            periodos[key] = {
                "key":        key,
                "label":      label,
                "total":      0,
                "abertos":    0,
                "fechados":   0,
                "categorias": Counter(),
                "analistas":  Counter(),
            }
        periodos[key]["total"] += 1
        if t.get("status") in _STATUS_RESOLVIDO:
            periodos[key]["fechados"] += 1
        else:
            periodos[key]["abertos"] += 1
        cat = t.get("serviceSecond") or t.get("serviceFirst") or ""
        if cat:
            periodos[key]["categorias"][cat] += 1
        ana = t.get("owner_name") or ""
        if ana:
            periodos[key]["analistas"][ana] += 1

    result = sorted(periodos.values(), key=lambda x: x["key"])
    for r in result:
        r["top_categorias"] = r["categorias"].most_common(5)
        r["top_analistas"]  = r["analistas"].most_common(5)
        del r["categorias"]
        del r["analistas"]

    return result


def build_sazonalidade_context(periodos, agrupamento='semana'):
    """Formata dados de sazonalidade como texto para o prompt da IA."""
    if not periodos:
        return "Nenhum dado de sazonalidade disponível."

    unidade   = "semana" if agrupamento == 'semana' else "mês"
    total     = sum(p["total"] for p in periodos)
    media     = total / len(periodos) if periodos else 0
    max_p     = max(periodos, key=lambda x: x["total"])
    min_p     = min(periodos, key=lambda x: x["total"])

    sb = [
        f"=== SAZONALIDADE — {unidade.upper()} A {unidade.upper()} ===\n",
        f"Total no período: {total} chamados em {len(periodos)} {unidade}s",
        f"Média por {unidade}: {media:.1f}",
        f"Pico: {max_p['label']} — {max_p['total']} chamados (+{max_p['total'] - media:.0f} acima da média)",
        f"Vale: {min_p['label']} — {min_p['total']} chamados ({min_p['total'] - media:.0f} vs média)\n",
        f"DADOS POR {unidade.upper()}:",
    ]

    for i, p in enumerate(periodos):
        delta_str = ""
        if i > 0:
            diff = p["total"] - periodos[i - 1]["total"]
            delta_str = f" ({'+' if diff >= 0 else ''}{diff} vs {unidade} ant.)"
        cats = ", ".join(f"{c}({n})" for c, n in p["top_categorias"][:3])
        sb.append(f"  {p['label']:8s}: {p['total']:4d} chamados{delta_str} | Top: {cats}")

    return "\n".join(sb)


def build_ai_context(stats):
    """Formata os dados detalhados como texto para o prompt da IA."""
    d  = stats
    sb = []

    sb.append(f"=== DATA DE HOJE: {d.get('hoje', '')} ===")
    sb.append(f"=== PERÍODO ANALISADO: {d.get('date_from','')} até {d.get('date_to','')} ({d['periodo_dias']} dias) ===\n")
    sb.append(f"Total de chamados no período: {d['total_periodo']} (período anterior: {d.get('periodo_anterior',0)})")
    sb.append(f"Esta semana: {d['esta_semana']} | Semana passada: {d['semana_passada']}")
    sb.append(f"Fora do SLA (>3 dias): {d['fora_sla_count']} ({d['fora_sla_pct']}%)")
    sb.append(f"Total acumulado na base: {d['total_geral']}\n")

    if d["top_categorias"]:
        sb.append("TOP CATEGORIAS DE PROBLEMA:")
        for cat, n in d["top_categorias"]:
            tend = d["tendencias"].get(cat, {})
            delta_str = ""
            if tend.get("delta", 0) > 0:
                delta_str = f" ↑{tend['delta']}"
            elif tend.get("delta", 0) < 0:
                delta_str = f" ↓{abs(tend['delta'])}"
            sb.append(f"  {n:3d}x  {cat}{delta_str}")
        sb.append("")

    if d["crescimento_semana"]:
        sb.append("CATEGORIAS QUE MAIS CRESCERAM ESSA SEMANA:")
        for cat, delta in d["crescimento_semana"]:
            sb.append(f"  +{delta}  {cat}")
        sb.append("")

    if d["analistas"]:
        sb.append("ANALISTAS (por volume no período):")
        for nome, info in d["analistas"][:10]:
            sla_str = f" | {info['fora_sla']} fora SLA" if info["fora_sla"] else ""
            sb.append(f"  {info['total']:3d} chamados | média {info['media_dias']}d{sla_str} | {nome}")
        sb.append("")

    if d["cat_tempo_medio"]:
        sb.append("TEMPO MÉDIO DE RESOLUÇÃO POR CATEGORIA (dias):")
        for cat, media in d["cat_tempo_medio"][:8]:
            sla = " ⚠ LENTO" if media > 3 else ""
            sb.append(f"  {media:5.1f}d  {cat}{sla}")
        sb.append("")

    if d["farmacias_criticas"]:
        sb.append("FARMÁCIAS COM MAIS CHAMADOS NO PERÍODO:")
        for farm, n in d["farmacias_criticas"]:
            sb.append(f"  {n:3d}x  {farm}")
        sb.append("")

    if d.get("cat_detalhes"):
        sb.append("DETALHAMENTO POR CATEGORIA — ASSUNTOS E PALAVRAS-CHAVE DOS CHAMADOS REAIS:")
        sb.append("(Use estes dados para identificar padrões e causas raiz)")
        for cat, info in d["cat_detalhes"].items():
            sb.append(f"\n[{cat}] — {info['count']} chamados no período")
            if info.get("keywords"):
                sb.append(f"  Palavras mais frequentes nos assuntos: {', '.join(info['keywords'])}")
            if info.get("subjects"):
                sb.append("  Exemplos de assuntos (títulos reais dos chamados):")
                for s in info["subjects"]:
                    sb.append(f"    • {s}")
            if info.get("pares"):
                sb.append("  Problemas e soluções já identificados nesta categoria:")
                for p in info["pares"]:
                    if p.get("problema"):
                        sb.append(f"    Problema: {p['problema']}")
                    if p.get("solucao"):
                        sb.append(f"    Solução:  {p['solucao']}")
        sb.append("")

    return "\n".join(sb)
