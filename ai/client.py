import re
import logging
import requests as _requests

from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError

from config import (
    OPENAI_BASE_URL, OPENAI_API_KEY, MODEL,
    OMNIROUTE_MODELS,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
    OPENROUTER_API_KEY, OPENROUTER_MODELS,
)

logger = logging.getLogger(__name__)

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
ANTHROPIC_COMPAT_BASE = "https://api.anthropic.com"


# ── Clientes (criados sob demanda) ────────────────────────────────────────────

_omniroute_client = None
_openrouter_client = None


def _get_omniroute_client():
    global _omniroute_client
    try:
        from utils.profile_cache import load_connection
        conn = load_connection()
        if conn and conn.get("ai_host"):
            base = "http://{}:20128/v1".format(conn["ai_host"].strip())
        else:
            base = OPENAI_BASE_URL
    except Exception:
        base = OPENAI_BASE_URL

    if _omniroute_client is None or str(_omniroute_client.base_url) != base + "/":
        _omniroute_client = OpenAI(base_url=base, api_key=OPENAI_API_KEY)
    return _omniroute_client


def _get_openrouter_client():
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenAI(
            base_url=OPENROUTER_BASE,
            api_key=OPENROUTER_API_KEY,
        )
    return _openrouter_client


# ── Construtores de mensagens ─────────────────────────────────────────────────

def _build_messages_omniroute(messages, image_base64):
    """Formato Anthropic-style para OmniRoute."""
    msgs = []
    for msg in messages:
        if image_base64 and msg == messages[-1] and msg.get("role") == "user":
            text = msg["content"] if isinstance(msg["content"], str) else ""
            msgs.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64,
                        },
                    },
                    {"type": "text", "text": text},
                ],
            })
        else:
            msgs.append({"role": msg["role"], "content": msg["content"]})
    return msgs


def _build_messages_openai(messages, image_base64):
    """Formato OpenAI-style (OpenRouter / Anthropic compat)."""
    msgs = []
    for msg in messages:
        if image_base64 and msg == messages[-1] and msg.get("role") == "user":
            text = msg["content"] if isinstance(msg["content"], str) else ""
            msgs.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/png;base64," + image_base64},
                    },
                    {"type": "text", "text": text},
                ],
            })
        else:
            msgs.append({"role": msg["role"], "content": msg["content"]})
    return msgs


# ── Chamadas por provedor ─────────────────────────────────────────────────────

def _call_omniroute(system_prompt, messages, image_base64, model=None):
    client = _get_omniroute_client()
    m = model or MODEL
    # Todos os modelos via OmniRoute aceitam system role nas messages
    msgs = _build_messages_openai(messages, image_base64)
    resp = client.chat.completions.create(
        model=m,
        max_tokens=4096,
        stream=False,
        messages=[{"role": "system", "content": system_prompt}] + msgs,
    )
    if resp.choices:
        return resp.choices[0].message.content
    if hasattr(resp, "content") and resp.content:
        block = resp.content[0]
        return block["text"] if isinstance(block, dict) else block.text
    raise ValueError(f"OmniRoute/{m}: resposta sem conteúdo")


def _call_anthropic_direct(system_prompt, messages, image_base64):
    """Chama Anthropic API usando openai-compat via SDK."""
    try:
        import anthropic as _ant

        client = _ant.Anthropic(api_key=ANTHROPIC_API_KEY)

        ant_messages = []
        for msg in messages:
            if image_base64 and msg == messages[-1] and msg.get("role") == "user":
                text = msg["content"] if isinstance(msg["content"], str) else ""
                ant_messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64,
                            },
                        },
                        {"type": "text", "text": text},
                    ],
                })
            else:
                ant_messages.append({"role": msg["role"], "content": msg["content"]})

        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=ant_messages,
        )
        return resp.content[0].text

    except ImportError:
        # anthropic não instalado — usa openai-compat com base URL da Anthropic
        client = OpenAI(
            base_url="https://api.anthropic.com/v1",
            api_key=ANTHROPIC_API_KEY,
            default_headers={"anthropic-version": "2023-06-01"},
        )
        msgs = _build_messages_openai(messages, image_base64)
        resp = client.chat.completions.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2048,
            messages=[{"role": "system", "content": system_prompt}] + msgs,
        )
        return resp.choices[0].message.content


def _call_openrouter(model, system_prompt, messages, image_base64):
    client = _get_openrouter_client()
    msgs = _build_messages_openai(messages, image_base64)
    resp = client.chat.completions.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "system", "content": system_prompt}] + msgs,
        extra_headers={"HTTP-Referer": "https://farmafacil.app"},
    )
    return resp.choices[0].message.content


# ── Cadeia de fallback ────────────────────────────────────────────────────────

_RETRYABLE = (429, 500, 502, 503, 504)


def _is_retryable(exc):
    if isinstance(exc, (RateLimitError, APIConnectionError)):
        return True
    if isinstance(exc, APIStatusError) and exc.status_code in _RETRYABLE:
        return True
    # Erros de rede genéricos
    msg = str(exc).lower()
    if any(kw in msg for kw in ("connection", "timeout", "rate limit", "overloaded")):
        return True
    return False


def _is_rate_limit(exc):
    return "429" in str(exc)


def ask_stream(system_prompt, messages, image_base64=None, static_prefix=None, model=None):
    """
    Versão streaming de ask(). Yields tokens de texto conforme chegam.
    Fallback automático em caso de 429, igual ao ask() normal.
    """
    if static_prefix:
        system_prompt = static_prefix + "\n\n" + system_prompt

    if model:
        outros = [m for m in OMNIROUTE_MODELS if m != model]
        models_to_try = [model] + outros
    else:
        models_to_try = OMNIROUTE_MODELS

    preferred_done = False
    last_exc = None

    for m in models_to_try:
        is_preferred = (model and not preferred_done)
        try:
            client = _get_omniroute_client()
            msgs = _build_messages_openai(messages, image_base64)
            stream = client.chat.completions.create(
                model=m,
                max_tokens=4096,
                stream=True,
                messages=[{"role": "system", "content": system_prompt}] + msgs,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            return
        except Exception as exc:
            logger.warning("OmniRoute:%s stream falhou (%s), tentando próximo...", m, exc)
            last_exc = exc
            if is_preferred:
                preferred_done = True
                if not _is_rate_limit(exc):
                    break

    raise RuntimeError(f"Streaming falhou em todos os modelos. Último erro: {last_exc}")


def ask(system_prompt, messages, image_base64=None, static_prefix=None, model=None):
    """
    Envia mensagem para IA.
    Se `model` for especificado, tenta ele primeiro.
    Em caso de 429 (rate limit), faz fallback automático para os demais OMNIROUTE_MODELS.
    Outros erros com modelo específico param imediatamente (sem fallback).
    """
    if static_prefix:
        system_prompt = static_prefix + "\n\n" + system_prompt

    last_exc = None

    # Monta lista: modelo preferido primeiro, depois os demais como fallback de 429
    if model:
        outros = [m for m in OMNIROUTE_MODELS if m != model]
        models_to_try = [model] + outros
    else:
        models_to_try = OMNIROUTE_MODELS

    preferred_done = False
    for m in models_to_try:
        is_preferred = (model and not preferred_done)
        try:
            result = _call_omniroute(system_prompt, messages, image_base64, model=m)
            if last_exc is not None:
                logger.info("Fallback bem-sucedido via OmniRoute:%s", m)
            return result
        except Exception as exc:
            logger.warning("OmniRoute:%s falhou (%s), tentando próximo...", m, exc)
            last_exc = exc
            if is_preferred:
                preferred_done = True
                if not _is_rate_limit(exc):
                    break  # erro que não é 429 no modelo preferido → não faz fallback

    raise RuntimeError(
        f"Todos os modelos OmniRoute falharam. Último erro: {last_exc}"
    )


# ── Utilitários ───────────────────────────────────────────────────────────────

def get_token_count():
    return 0, 0


def reset_token_count():
    pass


def classify_query(sql):
    sql_upper = sql.strip().upper()
    if sql_upper.startswith("SELECT") or sql_upper.startswith("WITH"):
        return "SELECT"
    return "MODIFY"


def extract_queries(ai_response):
    pattern = r"```sql\s*\n(.*?)\n```"
    matches = re.findall(pattern, ai_response, re.DOTALL | re.IGNORECASE)
    result = []
    for q in matches:
        q = q.strip()
        if q:
            result.append({"sql": q, "type": classify_query(q)})
    return result
