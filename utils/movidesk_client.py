"""
Cliente para a API REST do Movidesk.
"""
import requests
from config import MOVIDESK_TOKEN

BASE_URL = "https://api.movidesk.com/public/v1"
TIMEOUT  = 30


def _get(endpoint, params):
    params["token"] = MOVIDESK_TOKEN
    r = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _dt(date_str, end=False):
    """
    Movidesk OData: para início usa 'ge YYYY-MM-DD', para fim usa 'lt YYYY-MM-DD+1'
    (lt dia seguinte inclui o dia inteiro sem precisar de hora).
    """
    from datetime import datetime, timedelta
    d = datetime.strptime(date_str[:10], "%Y-%m-%d")
    if end:
        return (d + timedelta(days=1)).strftime("%Y-%m-%d")
    return d.strftime("%Y-%m-%d")


def fetch_tickets_page(skip=0, top=50, since_date=None, until_date=None, only_closed=False):
    """
    Busca página de chamados por createdDate.
    only_closed=True → só status '6 - Fechado'
    """
    filters = []
    if only_closed:
        filters.append("status eq '6 - Fechado'")
    if since_date:
        filters.append(f"createdDate ge {_dt(since_date)}")
    if until_date:
        filters.append(f"createdDate lt {_dt(until_date, end=True)}")


    params = {
        "$top":    top,
        "$skip":   skip,
        "$select": "id,subject,status,createdDate,resolvedIn,closedIn,lastUpdate,serviceFirstLevel,serviceSecondLevel,tags",
        "$expand": "owner,clients",
    }
    if filters:
        params["$filter"] = " and ".join(filters)
    return _get("tickets", params)


def fetch_resolved_page(skip=0, top=50, since_date=None, until_date=None):
    """
    Busca tickets RESOLVIDOS — status 5 (Resolvido) ou 6 (Fechado), ambos contam.
    """
    filters = ["(status eq '5 - Resolvido' or status eq '6 - Fechado')"]
    if since_date:
        filters.append(f"lastUpdate ge {_dt(since_date)}")
    if until_date:
        filters.append(f"lastUpdate lt {_dt(until_date, end=True)}")

    params = {
        "$top":    top,
        "$skip":   skip,
        "$select": "id,subject,status,createdDate,resolvedIn,closedIn,lastUpdate,serviceFirstLevel,serviceSecondLevel,tags",
        "$expand": "owner,clients",
        "$filter": " and ".join(filters),
    }
    return _get("tickets", params)


def fetch_tickets_past_page(skip=0, top=50, since_date=None, until_date=None):
    """Endpoint /tickets/past para tickets fechados com lastUpdate > 90 dias."""
    filters = ["status eq '6 - Fechado'"]
    if since_date:
        filters.append(f"resolvedIn ge {_dt(since_date)}")
    if until_date:
        filters.append(f"resolvedIn lt {_dt(until_date, end=True)}")

    params = {
        "$top":    top,
        "$skip":   skip,
        "$select": "id,subject,status,createdDate,resolvedIn,closedIn,serviceFirstLevel,serviceSecondLevel,tags",
        "$expand": "owner,clients",
        "$filter": " and ".join(filters),
    }
    return _get("tickets/past", params)


def fetch_tickets_past_created(skip=0, top=50, since_date=None, until_date=None):
    """
    Endpoint /tickets/past filtrado por createdDate — qualquer status.
    Usado para recuperar chamados criados há mais de 90 dias.
    """
    filters = []
    if since_date:
        filters.append(f"createdDate ge {_dt(since_date)}")
    if until_date:
        filters.append(f"createdDate lt {_dt(until_date, end=True)}")

    params = {
        "$top":    top,
        "$skip":   skip,
        "$select": "id,subject,status,createdDate,resolvedIn,closedIn,lastUpdate,serviceFirstLevel,serviceSecondLevel,tags",
        "$expand": "owner,clients",
    }
    if filters:
        params["$filter"] = " and ".join(filters)
    return _get("tickets/past", params)


def fetch_open_tickets_page(skip=0, top=50):
    """
    Busca todos os tickets em aberto sem filtro de data.
    Necessário para capturar tickets antigos ainda não resolvidos que ficam
    fora da janela de 90 dias do endpoint /tickets (que filtra por lastUpdate).
    """
    params = {
        "$top":    top,
        "$skip":   skip,
        "$select": "id,subject,status,createdDate,resolvedIn,closedIn,lastUpdate,serviceFirstLevel,serviceSecondLevel",
        "$expand": "owner,clients",
        "$filter": "status ne '5 - Resolvido' and status ne '6 - Fechado' and status ne '6 - Cancelado'",
    }
    return _get("tickets", params) or []


def count_open_by_owner(max_tickets=5000):
    """
    Busca todos os tickets abertos ao vivo.
    Retorna {owner_name_lower: {'total': N, 'by_client': {client_lower: count}}}.
    Usa paginação — percorre até max_tickets resultados.
    """
    from collections import defaultdict, Counter
    result = defaultdict(lambda: {'total': 0, 'by_client': Counter()})
    top  = 100
    skip = 0
    while skip < max_tickets:
        page = fetch_open_tickets_page(skip=skip, top=top)
        if not page:
            break
        for t in page:
            owner       = (t.get("owner") or {})
            owner_name  = (owner.get("businessName") or "").strip().lower()
            if not owner_name:
                continue
            clients     = t.get("clients") or []
            client_name = ((clients[0].get("businessName") if clients else "") or "").strip().lower()
            result[owner_name]['total'] += 1
            if client_name:
                result[owner_name]['by_client'][client_name] += 1
        if len(page) < top:
            break
        skip += top
    return dict(result)


def fetch_ticket_actions(ticket_id):
    """Busca as ações (conversa completa) de um chamado."""
    params = {
        "$select": "id,actions",
        "$filter": f"id eq {ticket_id}",
        "$expand": "actions",
    }
    result = _get("tickets", params)
    if result:
        return result[0].get("actions", [])
    return []
