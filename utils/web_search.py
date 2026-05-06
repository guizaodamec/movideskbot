"""
Busca web com cadeia de fallback: Brave → Tavily → DuckDuckGo.

Brave: 2000 queries/mês grátis — contador em web_search_usage.json
Tavily: pago por query — usado só quando Brave esgota
DuckDuckGo: grátis, ilimitado — último recurso
"""
import os
import json
import logging
import datetime
import requests as _requests

from config import (
    BRAVE_API_KEY,
    TAVILY_API_KEY,
    BRAVE_MONTHLY_LIMIT,
)
from utils.paths import get_data_dir

logger = logging.getLogger(__name__)

_USAGE_FILE = None


def _get_usage_file():
    global _USAGE_FILE
    if _USAGE_FILE is None:
        _USAGE_FILE = os.path.join(get_data_dir(), "web_search_usage.json")
    return _USAGE_FILE


def _load_usage():
    path = _get_usage_file()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"month": "", "brave_count": 0, "tavily_count": 0}


def _save_usage(usage):
    path = _get_usage_file()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usage, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _brave_quota_ok():
    usage = _load_usage()
    current_month = datetime.date.today().strftime("%Y-%m")
    if usage.get("month") != current_month:
        return True  # mês novo — resetará no incremento
    return usage.get("brave_count", 0) < BRAVE_MONTHLY_LIMIT


def _increment_brave():
    usage = _load_usage()
    current_month = datetime.date.today().strftime("%Y-%m")
    if usage.get("month") != current_month:
        usage = {"month": current_month, "brave_count": 0, "tavily_count": 0}
    usage["brave_count"] = usage.get("brave_count", 0) + 1
    _save_usage(usage)


def _increment_tavily():
    usage = _load_usage()
    current_month = datetime.date.today().strftime("%Y-%m")
    if usage.get("month") != current_month:
        usage = {"month": current_month, "brave_count": 0, "tavily_count": 0}
    usage["tavily_count"] = usage.get("tavily_count", 0) + 1
    _save_usage(usage)


def get_usage_stats():
    """Retorna estatísticas de uso para exibição."""
    usage = _load_usage()
    current_month = datetime.date.today().strftime("%Y-%m")
    if usage.get("month") != current_month:
        return {"brave": 0, "brave_limit": BRAVE_MONTHLY_LIMIT, "tavily": 0, "month": current_month}
    return {
        "brave": usage.get("brave_count", 0),
        "brave_limit": BRAVE_MONTHLY_LIMIT,
        "brave_restante": BRAVE_MONTHLY_LIMIT - usage.get("brave_count", 0),
        "tavily": usage.get("tavily_count", 0),
        "month": current_month,
    }


# ── Providers ────────────────────────────────────────────────────────────────

def _search_brave(query, max_results=3):
    """Brave Search API — 2000 queries/mês grátis."""
    if not BRAVE_API_KEY or BRAVE_API_KEY.startswith("SUA_"):
        return []
    if not _brave_quota_ok():
        logger.info("Brave quota esgotada este mês — usando fallback")
        return []
    try:
        resp = _requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_API_KEY,
            },
            params={"q": query, "count": max_results, "lang": "pt-BR", "country": "BR"},
            timeout=8,
        )
        if resp.status_code != 200:
            logger.warning("Brave HTTP %s", resp.status_code)
            return []
        data = resp.json()
        results = []
        for item in data.get("web", {}).get("results", [])[:max_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("description", ""),
                "source": "Brave",
            })
        _increment_brave()
        return results
    except Exception as e:
        logger.warning("Brave falhou: %s", e)
        return []


def _search_tavily(query, max_results=3):
    """Tavily API — pago por query, usado como fallback do Brave."""
    if not TAVILY_API_KEY or TAVILY_API_KEY.startswith("tvly-SUA"):
        return []
    try:
        resp = _requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
                "include_answer": False,
            },
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning("Tavily HTTP %s", resp.status_code)
            return []
        data = resp.json()
        results = []
        for item in data.get("results", [])[:max_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:400],
                "source": "Tavily",
            })
        _increment_tavily()
        return results
    except Exception as e:
        logger.warning("Tavily falhou: %s", e)
        return []


def _search_duckduckgo(query, max_results=3):
    """DuckDuckGo — grátis, ilimitado, último recurso."""
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="br-pt", max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:400],
                    "source": "DuckDuckGo",
                })
        return results
    except ImportError:
        logger.warning("duckduckgo_search não instalado — pip install duckduckgo-search")
        return []
    except Exception as e:
        logger.warning("DuckDuckGo falhou: %s", e)
        return []


# ── Interface pública ─────────────────────────────────────────────────────────

def search(query, max_results=3):
    """
    Busca web com fallback automático: Brave → Tavily → DuckDuckGo.
    Retorna lista de {title, url, snippet, source}.
    """
    # Foca a busca no contexto FarmaFácil
    query_focada = f"FarmaFácil Prismafive {query}"

    results = _search_brave(query_focada, max_results)
    if results:
        logger.info("Web search via Brave (%d resultados)", len(results))
        return results

    results = _search_tavily(query_focada, max_results)
    if results:
        logger.info("Web search via Tavily (%d resultados)", len(results))
        return results

    results = _search_duckduckgo(query_focada, max_results)
    if results:
        logger.info("Web search via DuckDuckGo (%d resultados)", len(results))
        return results

    return []


def format_for_prompt(results, max_chars=2000):
    """Formata resultados para injetar no prompt da IA."""
    if not results:
        return ""

    lines = ["## Resultados de busca na web (referência adicional):"]
    total = 0
    for r in results:
        chunk = f"- {r['title']}\n  {r['snippet']}\n  Fonte: {r['url']}"
        if total + len(chunk) > max_chars:
            break
        lines.append(chunk)
        total += len(chunk)

    return "\n".join(lines)


def should_search(query, kb_result):
    """
    Decide se vale fazer busca web.
    Busca quando: KB vazia/curta OU query contém erro/versão/código específico.
    """
    if len(kb_result) < 300:
        return True

    keywords = [
        "erro", "error", "exception", "code", "codigo", "versao", "versão",
        "atualiz", "release", "patch", "acbr", "sefaz", "receita", "prefeitura",
        "nf-e", "nfc-e", "nfs-e", "sat", "sped", "sintegra", "ecf",
        "portal", "certificado", "a1", "a3", "token",
        "noticia", "notícia", "novidade", "novo", "mudanca", "mudança",
        "prazo", "obrigatorio", "obrigatório", "lei", "decreto", "resolucao",
        "contingencia", "contingência", "indisponivel", "indisponível",
    ]
    q = query.lower()
    return any(kw in q for kw in keywords)
