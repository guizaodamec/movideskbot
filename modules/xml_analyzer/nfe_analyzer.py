"""
Analise de NF-e: busca XMLs, extrai erros e envia para Claude.
"""
import os
import sys

# Garantir que a raiz do projeto esta no path
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from .file_finder import find_nfe_folder, list_nfe_xmls
from .xml_reader import ler_xml, extrair_erros_retorno_nfe

from openai import OpenAI

try:
    from config import OPENAI_BASE_URL, OPENAI_API_KEY, MODEL
except ImportError:
    OPENAI_BASE_URL = "http://localhost:20128/v1"
    OPENAI_API_KEY  = "sk-ba3858d046b68de6-c258d1-0a3ea5e4"
    MODEL           = "cc/claude-sonnet-4-5-20250929"

_openai_client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

_SYSTEM_NFE = """
Voce e um especialista em NF-e, SEFAZ e sistema FarmaFacil.
Conhece todos os codigos de rejeicao da SEFAZ (100 a 999) e suas causas.
Responda SEMPRE em portugues brasileiro.
Seja direto: erro -> causa -> solucao exata no FarmaFacil.

Formato da resposta:

## Erro identificado
[codigo e descricao]

## Causa
[explicacao clara do motivo]

## Como corrigir no FarmaFacil
[passo a passo exato: qual tela, qual campo, qual valor]

## Observacao adicional
[se houver algo importante a verificar]
"""


def analisar_nfe(pasta_customizada=None):
    """
    Fluxo completo de analise NF-e.
    """
    pasta = pasta_customizada or find_nfe_folder()

    if not pasta:
        return {
            "ok": False,
            "erro": "Pasta de XMLs NF-e nao encontrada automaticamente. Informe o caminho manualmente.",
            "caminhos_tentados": True,
        }

    xmls = list_nfe_xmls(pasta)

    if not xmls:
        return {
            "ok": False,
            "erro": "Nenhum XML encontrado na pasta: " + pasta,
            "pasta": pasta,
        }

    retornos  = [x for x in xmls if x["tipo"] == "retorno"]
    envios    = [x for x in xmls if x["tipo"] == "envio"]

    conteudo_retorno = ""
    erros_extraidos  = []
    xml_retorno      = None

    if retornos:
        xml_retorno = retornos[0]
        dados = ler_xml(xml_retorno["caminho"])
        conteudo_retorno = dados["conteudo"]
        erros_extraidos  = extrair_erros_retorno_nfe(conteudo_retorno)

    conteudo_envio = ""
    if envios:
        dados_envio    = ler_xml(envios[0]["caminho"])
        conteudo_envio = dados_envio["conteudo"][:3000]

    prompt = _montar_prompt(
        pasta=pasta,
        xmls_listados=xmls,
        conteudo_retorno=conteudo_retorno,
        conteudo_envio=conteudo_envio,
        erros_extraidos=erros_extraidos,
    )

    resposta = _openai_client.chat.completions.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": _SYSTEM_NFE},
            {"role": "user", "content": prompt},
        ],
    )

    return {
        "ok": True,
        "pasta": pasta,
        "xmls": xmls,
        "erros_extraidos": erros_extraidos,
        "diagnostico": resposta.choices[0].message.content,
        "xml_retorno": xml_retorno,
    }


def _montar_prompt(pasta, xmls_listados, conteudo_retorno, conteudo_envio, erros_extraidos):
    linhas_xmls = "\n".join(
        "- {nome} ({tipo}) - {modificado}".format(**x) for x in xmls_listados[:10]
    )

    erros_str = ""
    if erros_extraidos:
        for e in erros_extraidos:
            erros_str += "\n" + str(e)

    return (
        "Analise os XMLs de NF-e abaixo e forneca um diagnostico completo.\n\n"
        "## Pasta analisada\n{pasta}\n\n"
        "## XMLs encontrados (mais recentes)\n{xmls}\n\n"
        "## Erros extraidos do retorno SEFAZ\n{erros}\n\n"
        "## Conteudo do XML de retorno (mais recente)\n```xml\n{retorno}\n```\n\n"
        "## Trecho do XML de envio (contexto)\n```xml\n{envio}\n```\n\n"
        "Com base nos dados acima:\n"
        "1. Qual e o erro e o codigo de rejeicao?\n"
        "2. Por que esse erro aconteceu?\n"
        "3. O que exatamente deve ser alterado no FarmaFacil para corrigir?\n"
        "4. Se envolver CFOP, CST, aliquota ou outro campo fiscal, indique o valor correto.\n"
    ).format(
        pasta=pasta,
        xmls=linhas_xmls,
        erros=erros_str or "Nenhum erro estruturado extraido — ver XML completo",
        retorno=conteudo_retorno[:4000] if conteudo_retorno else "XML de retorno nao encontrado",
        envio=conteudo_envio or "XML de envio nao encontrado",
    )
