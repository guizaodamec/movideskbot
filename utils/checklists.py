"""
Checklists automáticos por categoria de chamado.
Mapeados por palavras-chave presentes no serviceFirst ou serviceSecond.
"""

_CHECKLISTS = [
    {
        "keywords": ["nf-e", "nfe", "nota fiscal eletrônica", "nota fiscal eletr"],
        "label": "NF-e",
        "itens": [
            "Verificar validade do certificado digital (A1/A3)",
            "Verificar status da SEFAZ (sefazstatus.com.br)",
            "Verificar numeração: próximo número e série configurados",
            "Verificar ambiente: homologação vs produção",
            "Verificar dados do emitente (CNPJ, IE, endereço)",
            "Verificar configuração do webservice (URL da SEFAZ estadual)",
        ],
    },
    {
        "keywords": ["nfs-e", "nfse", "nota fiscal de serviço", "nota de serviço"],
        "label": "NFS-e",
        "itens": [
            "Verificar certificado digital",
            "Verificar código do serviço municipal (CNAE/LC116)",
            "Verificar configuração do webservice da prefeitura",
            "Verificar se há lote pendente de envio",
            "Verificar CNPJ do tomador",
            "Verificar tributação do serviço",
        ],
    },
    {
        "keywords": ["boleto", "cobrança bancária", "remessa"],
        "label": "Boleto",
        "itens": [
            "Verificar configuração do banco e convênio",
            "Verificar nosso número/sequência",
            "Verificar validade do certificado bancário (se aplicável)",
            "Verificar limite de vencimento configurado",
            "Testar geração com valor simbólico (R$ 0,01)",
        ],
    },
    {
        "keywords": ["estoque", "inventário", "saldo"],
        "label": "Estoque",
        "itens": [
            "Verificar se há movimentações pendentes de lançamento",
            "Verificar se o produto está cadastrado corretamente",
            "Verificar unidade de medida e fator de conversão",
            "Verificar lote e validade (se controle ativo)",
            "Verificar se há reservas afetando o saldo",
        ],
    },
    {
        "keywords": ["caixa", "financeiro", "pagamento", "recebimento"],
        "label": "Caixa / Financeiro",
        "itens": [
            "Verificar se o caixa está aberto",
            "Verificar forma de pagamento configurada",
            "Verificar permissão do usuário para a operação",
            "Verificar se há sangria/suprimento pendente",
            "Verificar conciliação do dia anterior",
        ],
    },
    {
        "keywords": ["sat", "cfe", "cupom fiscal"],
        "label": "SAT / CF-e",
        "itens": [
            "Verificar se o SAT está ativado e comunicando",
            "Verificar código de ativação do SAT",
            "Verificar CNPJ do software house e código de ativação",
            "Testar comunicação: extrair logs do SAT",
            "Verificar se há CFe pendente de cancelamento",
        ],
    },
    {
        "keywords": ["integração", "api", "webservice", "import", "export"],
        "label": "Integração / API",
        "itens": [
            "Verificar credenciais da integração (usuário/senha/token)",
            "Verificar URL do endpoint configurado",
            "Verificar log de erros da integração",
            "Testar conectividade (ping/telnet na porta)",
            "Verificar formato do arquivo (se integração por arquivo)",
        ],
    },
    {
        "keywords": ["backup", "banco de dados", "restaur"],
        "label": "Banco de Dados / Backup",
        "itens": [
            "Verificar se o serviço PostgreSQL está rodando",
            "Verificar espaço em disco disponível",
            "Verificar logs do PostgreSQL (pg_log)",
            "Verificar último backup realizado com sucesso",
            "Verificar permissões do usuário do banco",
        ],
    },
    {
        "keywords": ["lentidão", "lento", "desempenho", "travando", "trava"],
        "label": "Desempenho / Lentidão",
        "itens": [
            "Verificar uso de CPU e memória do servidor",
            "Verificar queries lentas no PostgreSQL (pg_stat_activity)",
            "Verificar índices das tabelas principais",
            "Verificar número de conexões abertas no banco",
            "Verificar se há backup ou processo pesado rodando em paralelo",
        ],
    },
]


def get_checklist(categoria: str):
    """Retorna o checklist para uma categoria, ou None se não encontrado."""
    if not categoria:
        return None
    cat_lower = categoria.lower()
    for c in _CHECKLISTS:
        if any(kw in cat_lower for kw in c["keywords"]):
            return c
    return None


def get_all_checklists() -> list:
    return _CHECKLISTS
