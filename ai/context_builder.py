from ai.prompts import SYSTEM_PROMPT_TEMPLATE, WELCOME_TEMPLATE
from db.scanner import build_schema_summary, build_volumes_summary


def _format_modulos(modulos):
    if not modulos:
        return "Nenhum modulo padrao detectado."
    return "\n".join("- " + m for m in modulos)


def _format_erros(erros):
    if not erros:
        return "Nenhum erro recorrente encontrado."
    lines = []
    for i, err in enumerate(erros[:5]):
        parts = []
        for k, v in err.items():
            parts.append("{0}: {1}".format(k, str(v)[:100]))
        lines.append("  " + " | ".join(parts))
        if i >= 4:
            break
    return "\n".join(lines)


def _format_queries_lentas(queries):
    if not queries:
        return "pg_stat_statements nao disponivel ou sem dados."
    lines = []
    for q in queries[:5]:
        lines.append("  {0:.1f}ms (calls:{1}) - {2}".format(
            q.get("mean_ms", 0),
            q.get("calls", 0),
            q.get("query", "")[:120]
        ))
    return "\n".join(lines)


def build_system_prompt(profile, query=None):
    """
    Monta o system prompt com dados do cliente.
    Retorna (static_part, dynamic_part):
    - static_part: None (base de conhecimento injetada dinamicamente por relevancia)
    - dynamic_part: dados do cliente + schema ao vivo + artigos relevantes da knowledge base
    """
    # Busca artigos relevantes para a query (injeta apenas o necessario)
    knowledge_section = ""
    if query:
        try:
            from utils.knowledge_search import search as _kb_search
            kb_result = _kb_search(query, top_n=4, max_chars=6000)
            if kb_result:
                knowledge_section = (
                    "\n\n## Artigos relevantes da Base de Conhecimento FarmaFacil\n"
                    + kb_result + "\n"
                )
        except Exception:
            pass

    if not profile:
        dynamic_part = SYSTEM_PROMPT_TEMPLATE.format(
            knowledge_section=knowledge_section,
            razao_social="Nao identificada",
            cnpj="N/A",
            cidade="N/A",
            uf="N/A",
            regime_tributario="N/A",
            versao_sistema="N/A",
            versao_postgres="N/A",
            ultimo_backup="N/A",
            modulos_detectados="Nao escaneado ainda.",
            schema_resumido="Nao disponivel.",
            volumes="Nao disponivel.",
            erros_recorrentes="Nao disponivel.",
            queries_lentas="Nao disponivel.",
        )
        return None, dynamic_part

    # max_tables=60: prioriza tabelas de negocio, cobre o essencial do FarmaFacil
    schema_resumido = build_schema_summary(profile.get("schema", []), max_tables=60)

    dynamic_part = SYSTEM_PROMPT_TEMPLATE.format(
        knowledge_section=knowledge_section,
        razao_social=profile.get("razao_social", "N/A"),
        cnpj=profile.get("cnpj", "N/A"),
        cidade=profile.get("cidade", "N/A"),
        uf=profile.get("uf", "N/A"),
        regime_tributario=profile.get("regime_tributario", "N/A"),
        versao_sistema=profile.get("versao_sistema", "N/A"),
        versao_postgres=profile.get("versao_postgres", "N/A"),
        ultimo_backup=profile.get("ultimo_backup", "N/A"),
        modulos_detectados=_format_modulos(profile.get("modulos_detectados", [])),
        schema_resumido=schema_resumido,
        volumes=build_volumes_summary(profile.get("volumes", [])),
        erros_recorrentes=_format_erros(profile.get("erros_recorrentes", [])),
        queries_lentas=_format_queries_lentas(profile.get("queries_lentas", [])),
    )
    return None, dynamic_part


def build_welcome_message(profile):
    """Monta mensagem de boas-vindas apos conexao."""
    if not profile:
        return "Conectado ao banco. Como posso ajudar?"
    modulos = profile.get("modulos_detectados", [])
    if modulos:
        modulos_lista = "\n".join("- " + m for m in modulos)
    else:
        modulos_lista = "- Nenhum modulo padrao detectado"

    return WELCOME_TEMPLATE.format(
        razao_social=profile.get("razao_social", "N/A"),
        cnpj=profile.get("cnpj", "N/A"),
        versao_sistema=profile.get("versao_sistema", "N/A"),
        versao_postgres=profile.get("versao_postgres", "N/A"),
        modulos_lista=modulos_lista,
    )
