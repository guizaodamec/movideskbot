"""
Busca por palavras-chave na base de conhecimento FarmaFácil.
Carrega scraper_cache.json (artigos + descrições de imagens) e retorna
os artigos mais relevantes para uma query.
"""
import os
import re
import json
from datetime import datetime
from utils.paths import get_bundle_dir

_articles = None      # cache em memória (scraper_cache.json)
_md_articles = None   # farmafacil_knowledge.md (sempre carregado)
_kb_articles = None   # base_conhecimento.json + knowledge_structured.json + suporte_erp_kb.json
_corrections = None   # correções verificadas pela equipe

_BASE_CONHECIMENTO_PATH = r"C:\Users\guilherme.cordeiro\Desktop\melhorar IA\base_conhecimento.json"
_KNOWLEDGE_STRUCTURED_PATH = r"C:\Users\guilherme.cordeiro\Desktop\melhorar IA\knowledge_structured.json"


def _to_str(v) -> str:
    """Converte qualquer valor para string limpa (suporta listas)."""
    if v is None:
        return ""
    if isinstance(v, list):
        return "\n".join(str(x) for x in v if x)
    return str(v)


def _parse_kb_item(item, id_field="bloco"):
    """Converte um item de qualquer fonte KB para o formato interno."""
    titulo   = _to_str(item.get("titulo")).strip()
    resumo   = _to_str(item.get("resumo") or item.get("resumo_simples")).strip()
    problema = _to_str(item.get("problema")).strip()
    causa    = _to_str(item.get("causa")).strip()
    solucao  = _to_str(item.get("solucao")).strip()
    passos   = item.get("passos", []) or []
    tags     = item.get("tags", []) or []

    if not titulo or (not problema and not solucao):
        return None

    passos_txt = "\n".join(f"- {p}" for p in passos) if passos else ""
    tags_txt   = " ".join(tags)
    full_text  = " ".join([titulo, resumo, problema, causa, solucao, passos_txt, tags_txt])

    display_parts = [f"## {titulo}"]
    if problema:
        display_parts.append(f"Problema: {problema}")
    if causa:
        display_parts.append(f"Causa: {causa}")
    if solucao:
        display_parts.append(f"Solucao: {solucao}")
    if passos:
        display_parts.append("Passos:\n" + passos_txt)

    title_clean = re.sub(r'[^\w\s\.\-\/]', '', titulo.lower()).strip()
    full_lower  = full_text.lower()

    return {
        "id": str(item.get(id_field, item.get("id", ""))),
        "title": title_clean,
        "title_nodots": _nodots(title_clean),
        "text_lower": full_lower,
        "text_nodots": _nodots(full_lower),
        "display": "\n".join(display_parts),
        "recency": 2,
    }


def _load_kb_articles():
    global _kb_articles
    if _kb_articles is not None:
        return _kb_articles

    arts = []

    # Fonte 1: base_conhecimento.json (lista)
    for p in [_BASE_CONHECIMENTO_PATH, os.path.join(get_bundle_dir(), "base_conhecimento.json")]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in (data if isinstance(data, list) else []):
                    parsed = _parse_kb_item(item, id_field="bloco")
                    if parsed:
                        arts.append(parsed)
                break
            except Exception:
                pass

    # Fonte 2: knowledge_structured.json (dict keyed by article id — gerado pelo processar_kb.py)
    for p in [_KNOWLEDGE_STRUCTURED_PATH, os.path.join(get_bundle_dir(), "knowledge_structured.json")]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in (data.values() if isinstance(data, dict) else data):
                    if item.get("erro") or not item.get("solucao"):
                        continue
                    parsed = _parse_kb_item(item, id_field="id")
                    if parsed:
                        arts.append(parsed)
                break
            except Exception:
                pass

    # Fonte 3: suporte_erp_kb.json — gerado pelo converter_erp_kb.py (análise do EXE)
    erp_kb_path = os.path.join(get_bundle_dir(), "suporte_erp_kb.json")
    if os.path.exists(erp_kb_path):
        try:
            with open(erp_kb_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in (data if isinstance(data, list) else []):
                try:
                    parsed = _parse_kb_item(item, id_field="bloco")
                    if parsed:
                        arts.append(parsed)
                except Exception:
                    pass
        except Exception:
            pass

    _kb_articles = arts
    return _kb_articles


def invalidate_corrections_cache():
    global _corrections
    _corrections = None

_STOPWORDS = {
    "que", "para", "com", "uma", "por", "dos", "das", "nos", "nas",
    "seu", "sua", "sao", "nao", "mais", "como", "mas", "foi", "ele",
    "ela", "isso", "esse", "essa", "este", "esta", "tem", "ter",
    "ser", "ver", "qual", "quais", "quando", "onde", "quem", "voce",
    "esse", "pelo", "pela", "pode", "deve", "caso", "tipo", "vez",
}


def _nodots(text: str) -> str:
    """Remove pontos entre dígitos: '90.15' → '9015'."""
    return re.sub(r'(?<=\d)\.(?=\d)', '', text)


def _recency(data_str: str) -> int:
    """Retorna 2 (recente), 1 (médio) ou 0 (antigo) com base na data DD/MM/YYYY."""
    try:
        pub = datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.now()
        meses = (hoje.year - pub.year) * 12 + (hoje.month - pub.month)
        if meses <= 12:
            return 2
        if meses <= 24:
            return 1
        return 0
    except Exception:
        return 0


def _load_corrections():
    """Carrega correções verificadas pela equipe (prioridade máxima)."""
    global _corrections
    if _corrections is not None:
        return _corrections

    path = os.path.join(get_bundle_dir(), "knowledge_corrections.json")
    if not os.path.exists(path):
        _corrections = []
        return _corrections

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        _corrections = []
        return _corrections

    arts = []
    for item in data:
        titulo = item.get("titulo", "").strip()
        conteudo = item.get("conteudo", "").strip()
        keywords = item.get("keywords", [])
        prioridade = item.get("prioridade", 100)
        data_str = item.get("data", "")
        fonte = item.get("fonte", "Correção equipe de suporte")

        full_text = titulo + "\n\n" + conteudo + "\n" + " ".join(keywords)
        display = (
            f"## ⚠️ CORREÇÃO VERIFICADA: {titulo} — {data_str}\n"
            f"Fonte: {fonte}\n\n"
            f"{conteudo}"
        )
        title_clean = re.sub(r'[^\w\s\.\-\/]', '', titulo.lower()).strip()
        full_lower = full_text.lower()

        arts.append({
            "id": item.get("id", ""),
            "title": title_clean,
            "title_nodots": _nodots(title_clean),
            "text_lower": full_lower,
            "text_nodots": _nodots(full_lower),
            "display": display,
            "recency": 2,
            "base_priority": prioridade,
        })

    _corrections = arts
    return _corrections


def _load_articles():
    global _articles
    if _articles is not None:
        return _articles

    path = os.path.join(get_bundle_dir(), "scraper_cache.json")
    if not os.path.exists(path):
        # Fallback para o markdown se JSON não existir
        _articles = _load_articles_from_md()
        return _articles

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    arts = []
    for art_id, art in data.items():
        if art.get("privado"):
            continue

        titulo = art.get("titulo", "").strip()
        texto = art.get("texto", "").strip()
        imagens = art.get("imagens", [])
        data_str = art.get("data", "")
        url = art.get("url", "")

        # Texto completo para busca: título + corpo + descrições de imagens
        imagens_txt = "\n\n".join(imagens) if imagens else ""
        full_text = titulo + "\n\n" + texto
        if imagens_txt:
            full_text += "\n\n[Telas do sistema]\n" + imagens_txt

        # Texto formatado para injetar no prompt da IA
        display = "## {titulo} — {data}\nFonte: {url}\n\n{texto}".format(
            titulo=titulo, data=data_str, url=url, texto=texto
        )
        if imagens:
            display += "\n\n[Descrições das telas]\n" + "\n\n".join(imagens)

        title_clean = re.sub(r'[^\w\s\.\-\/]', '', titulo.lower()).strip()
        full_lower = full_text.lower()
        full_nodots = _nodots(full_lower)
        title_nodots = _nodots(title_clean)

        arts.append({
            "id": art_id,
            "title": title_clean,
            "title_nodots": title_nodots,
            "text_lower": full_lower,
            "text_nodots": full_nodots,
            "display": display,
            "recency": _recency(data_str),
        })

    _articles = arts
    return _articles


def _load_md_articles():
    """Carrega farmafacil_knowledge.md — sempre, em paralelo com scraper_cache."""
    global _md_articles
    if _md_articles is not None:
        return _md_articles
    path = os.path.join(get_bundle_dir(), "farmafacil_knowledge.md")
    if not os.path.exists(path):
        _md_articles = []
        return _md_articles
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    parts = re.split(r'\n(?=## )', content)
    arts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        first_line = part.split("\n")[0]
        if any(x in first_line for x in ("ndice", "Índice")):
            continue
        title_clean = re.sub(r'[^\w\s\.\-\/]', '', re.sub(r'^#+\s*', '', first_line).lower()).strip()
        rec = 2 if "\U0001f7e2" in first_line else (1 if "\U0001f7e1" in first_line else 0)
        tl = part.lower()
        arts.append({
            "id": "md",
            "title": title_clean,
            "title_nodots": _nodots(title_clean),
            "text_lower": tl,
            "text_nodots": _nodots(tl),
            "display": part,
            "recency": rec,
        })
    _md_articles = arts
    return _md_articles


def _load_articles_from_md():
    """Fallback legado — delega para _load_md_articles."""
    return _load_md_articles()


def _load_md_articles_compat():
    """Fallback: carrega do farmafacil_knowledge.md se o JSON não existir."""
    path = os.path.join(get_bundle_dir(), "farmafacil_knowledge.md")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    parts = re.split(r'\n(?=## )', content)
    arts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        first_line = part.split("\n")[0]
        if any(x in first_line for x in ("ndice", "Índice")):
            continue
        title_clean = re.sub(r'[^\w\s\.\-\/]', '', re.sub(r'^#+\s*', '', first_line).lower()).strip()
        rec = 2 if "\U0001f7e2" in first_line else (1 if "\U0001f7e1" in first_line else 0)
        tl = part.lower()
        arts.append({
            "id": "",
            "title": title_clean,
            "title_nodots": _nodots(title_clean),
            "text_lower": tl,
            "text_nodots": _nodots(tl),
            "display": part,
            "recency": rec,
        })
    return arts


def _tokenize(text: str):
    """Extrai tokens incluindo versões sem pontos de números."""
    tokens = set()
    tl = text.lower()

    # Padrões de versão: "90.15" → também "9015"
    for m in re.findall(r'\d+\.\d+[\.\d]*', tl):
        tokens.add(m)
        tokens.add(_nodots(m))
        for part in m.split("."):
            if len(part) >= 2:
                tokens.add(part)

    # Palavras e números
    for w in re.findall(r'\w+', tl):
        if w.isdigit():
            if len(w) >= 2:
                tokens.add(w)
        elif len(w) >= 3 and w not in _STOPWORDS:
            tokens.add(w)

    return tokens


def search(query: str, top_n: int = 4, max_chars: int = 6000) -> str:
    """
    Busca artigos relevantes para a query.
    Correções verificadas pela equipe são retornadas primeiro quando relevantes.
    base_conhecimento.json tem prioridade alta sobre scraper_cache.json.
    """
    articles    = _load_articles()
    md_articles = _load_md_articles()
    kb_articles = _load_kb_articles()
    corrections = _load_corrections()
    if not articles and not md_articles and not kb_articles and not corrections:
        return ""

    tokens = _tokenize(query)
    if not tokens:
        return ""

    scored = []

    # Correções: pontuação base altíssima para garantir que apareçam primeiro
    for art in corrections:
        score = 0
        for token in tokens:
            count = art["text_lower"].count(token)
            if count:
                title_count = art["title"].count(token)
                score += title_count * 5 + (count - title_count)
        if score > 0:
            score = score * art.get("base_priority", 100)
            scored.append((score, art))

    kb_set = set(id(a) for a in kb_articles)
    md_set = set(id(a) for a in md_articles)

    for art in kb_articles + md_articles + articles:
        score = 0
        is_kb = id(art) in kb_set
        for token in tokens:
            for text_f, title_f in [
                (art["text_lower"], art["title"]),
                (art["text_nodots"], art["title_nodots"]),
            ]:
                count = text_f.count(token)
                if count:
                    title_count = title_f.count(token)
                    score += title_count * 5 + (count - title_count)

        if score > 0:
            score = score * (1 + art["recency"] * 0.3)
            if is_kb:
                score *= 1.5  # base_conhecimento.json — prioridade extra
            elif id(art) in md_set:
                score *= 1.2  # farmafacil_knowledge.md — prioridade média-alta
            scored.append((score, art))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_n]

    if not top:
        return ""

    result_parts = []
    total = 0
    for _, art in top:
        chunk = art["display"]
        if total + len(chunk) > max_chars:
            remaining = max_chars - total
            if remaining > 200:
                chunk = chunk[:remaining] + "\n...[artigo truncado]"
            else:
                break
        result_parts.append(chunk)
        total += len(chunk)

    return "\n\n---\n\n".join(result_parts)
