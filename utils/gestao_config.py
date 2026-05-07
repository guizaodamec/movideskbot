"""Configuração dos grupos de analistas para o módulo de Gestão."""
import json
import os
from utils.paths import get_data_dir

_CONFIG_FILE = "gestao_config.json"

_DEFAULT = {
    "grupos": {
        "Fiscal":   ["Vinicius", "Rebeca medeiros", "Rubens Milton Destro Junior"],
        "Producao": ["Isaac Santos", "Raul Neto", "Matheus Miranda de Lima Araujo", "Boeira", "Ruam Pereira de Sá"],
        "G1":       ["Marcello Filho", "Alan vieira", "Keven Silva dos Santos"],
        "GW":       ["Nathan Lopes", "Taynara Pereira", "Taynara Ribeiro"],
        "Ouvidoria": ["Erica Milo Nardo Portezani", "Lucas Eduardo Durante", "Guilherme Cordeiro", "Taynara Ribeiro"],
    },
    # Palavras-chave de categoria por grupo — usadas para classificar tickets
    # quando o filtro por grupo está ativo (além do filtro por analista)
    "categorias": {
        "Fiscal":   ["nf-e", "nfe", "nota fiscal eletrônica", "cupom fiscal", "sped", "ecf",
                     "obrigação fiscal", "documentos fiscais", "nf-e documentos"],
        "Producao": ["nota de entrada", "manipulação", "sngpc", "responsável técnico",
                     "vendas", "relatório", "produção", "compras"],
        "G1":       ["suporte", "instalação", "configuração", "acesso", "senha", "treinamento",
                     "certificado digital", "certificado"],
        "GW":       ["orya", "e-commerce", "ecommerce", "alcance", "farmafacil web", "farmafast web",
                     "prismasync", "prism sync", "sync", "ph24"],
        "Ouvidoria": ["ouvidoria", "reclamações", "elogios", "sugestões", "motivos internos"],
    },
    # Analistas excluídos do cálculo de metas (líderes, gerentes, etc.)
    # Continuam aparecendo nos filtros de tickets, mas não entram em n_analistas nem na tabela de metas.
    "excluir_metas": ["Guilherme Cordeiro", "Diego Teixeira"]
}


def load_config():
    p = os.path.join(get_data_dir(), _CONFIG_FILE)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return dict(_DEFAULT)


def save_config(cfg):
    p = os.path.join(get_data_dir(), _CONFIG_FILE)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def get_all_known_analistas():
    """Retorna lista plana de todos os analistas configurados em algum grupo."""
    cfg = load_config()
    known = set()
    for membros in cfg.get("grupos", {}).values():
        known.update(membros)
    return known


def get_grupo_analistas(grupo_nome):
    """Retorna lista de analistas de um grupo específico."""
    cfg = load_config()
    return cfg.get("grupos", {}).get(grupo_nome, [])


def get_excluir_metas():
    """Retorna analistas excluídos do cálculo de metas (líderes, gerentes)."""
    cfg = load_config()
    return {m.lower() for m in cfg.get("excluir_metas", [])}


def get_grupo_categorias(grupo_nome):
    """Retorna palavras-chave de categoria do grupo (lowercase)."""
    cfg = load_config()
    return [k.lower() for k in cfg.get("categorias", {}).get(grupo_nome, [])]


def ticket_pertence_grupo(ticket, grupo_nome):
    """
    True se o ticket pertence ao grupo — por analista (prioritário).
    Fallback por categoria apenas para tickets sem dono conhecido.
    """
    cfg      = load_config()
    membros  = {m.lower() for m in cfg.get("grupos", {}).get(grupo_nome, [])}
    owner    = (ticket.get("owner_name") or "").lower()
    if owner in membros:
        return True
    # Se o owner é de outro grupo conhecido, não usar fallback por categoria
    all_known = {m.lower() for grp in cfg.get("grupos", {}).values() for m in grp}
    if owner and owner in all_known:
        return False
    # Fallback: classificação por categoria (só para tickets sem dono reconhecido)
    keywords = get_grupo_categorias(grupo_nome)
    if not keywords:
        return False
    cat_text = " ".join([
        (ticket.get("serviceFirst") or ""),
        (ticket.get("serviceSecond") or ""),
    ]).lower()
    return any(kw in cat_text for kw in keywords)


def get_grupo_for_ticket(ticket):
    """Detecta a qual grupo o ticket pertence para exibição. Prioridade: categoria > analista."""
    cfg = load_config()
    cat_text = " ".join([
        (ticket.get("serviceFirst") or ""),
        (ticket.get("serviceSecond") or ""),
    ]).lower()
    # Categoria tem prioridade (ex: SPED é sempre Fiscal, independente do analista)
    for grupo, keywords in cfg.get("categorias", {}).items():
        if any(kw.lower() in cat_text for kw in keywords):
            return grupo
    # Fallback: pelo analista responsável
    owner = (ticket.get("owner_name") or "").lower()
    for grupo, membros in cfg.get("grupos", {}).items():
        if owner in {m.lower() for m in membros}:
            return grupo
    return None
