"""
Analise de NFS-e: busca XMLs, le configuracao ACBr e envia para Claude.
"""
import os
import sys
import glob

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from .file_finder import find_nfse_folder, find_acbr_config
from .xml_reader import ler_xml, extrair_erros_retorno_nfse

from openai import OpenAI

try:
    from config import OPENAI_BASE_URL, OPENAI_API_KEY, MODEL
except ImportError:
    OPENAI_BASE_URL = "http://localhost:20128/v1"
    OPENAI_API_KEY  = "sk-ba3858d046b68de6-c258d1-0a3ea5e4"
    MODEL           = "cc/claude-sonnet-4-5-20250929"

_openai_client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

_SYSTEM_NFSE = """
Voce e um especialista em NFS-e, ACBr e sistema FarmaFacil.
Conhece os padroes ABRASF, Nota Carioca, e os principais provedores municipais.
Conhece os erros comuns de cada prefeitura e como configurar o ACBr corretamente.
Responda SEMPRE em portugues brasileiro.

Formato da resposta:

## Erro identificado
[descricao do erro do provedor]

## Causa
[por que aconteceu: problema no XML, na configuracao, no cadastro?]

## Como corrigir
[passo a passo: FarmaFacil / ACBr / outro]

## Verificacao da configuracao ACBr
[configuracao esta ok? o que ajustar se necessario?]
"""


def analisar_nfse(pasta_customizada=None):
    """
    Fluxo completo de analise NFS-e.
    """
    info_pasta = pasta_customizada or find_nfse_folder()

    if not info_pasta:
        return {
            "ok": False,
            "erro": "Pasta de XMLs NFS-e nao encontrada automaticamente. Informe o caminho manualmente.",
        }

    # Se veio como string (caminho manual), montar estrutura esperada
    if isinstance(info_pasta, str):
        envio   = os.path.join(info_pasta, "envio")
        retorno = os.path.join(info_pasta, "retorno")
        info_pasta = {
            "base": info_pasta,
            "pasta_data": os.path.basename(info_pasta),
            "caminho_data": info_pasta,
            "envio":   envio   if os.path.exists(envio)   else None,
            "retorno": retorno if os.path.exists(retorno) else None,
        }

    xmls_retorno = []
    if info_pasta.get("retorno"):
        xmls_retorno = glob.glob(os.path.join(info_pasta["retorno"], "*.xml"))
        xmls_retorno.sort(key=os.path.getmtime, reverse=True)

    xmls_envio = []
    if info_pasta.get("envio"):
        xmls_envio = glob.glob(os.path.join(info_pasta["envio"], "*.xml"))
        xmls_envio.sort(key=os.path.getmtime, reverse=True)

    conteudo_retorno = ""
    erros_nfse       = []
    if xmls_retorno:
        dados            = ler_xml(xmls_retorno[0])
        conteudo_retorno = dados["conteudo"]
        erros_nfse       = extrair_erros_retorno_nfse(conteudo_retorno)

    conteudo_envio = ""
    if xmls_envio:
        dados_envio    = ler_xml(xmls_envio[0])
        conteudo_envio = dados_envio["conteudo"][:2000]

    caminho_acbr   = find_acbr_config()
    conteudo_acbr  = ""
    if caminho_acbr:
        try:
            with open(caminho_acbr, "r", encoding="utf-8") as f:
                conteudo_acbr = f.read()
        except UnicodeDecodeError:
            try:
                with open(caminho_acbr, "r", encoding="latin-1") as f:
                    conteudo_acbr = f.read()
            except Exception as e:
                conteudo_acbr = "Erro ao ler arquivo: " + str(e)

    prompt = _montar_prompt(
        info_pasta=info_pasta,
        conteudo_retorno=conteudo_retorno,
        conteudo_envio=conteudo_envio,
        erros_extraidos=erros_nfse,
        conteudo_acbr=conteudo_acbr,
        caminho_acbr=caminho_acbr,
    )

    resposta = _openai_client.chat.completions.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": _SYSTEM_NFSE},
            {"role": "user", "content": prompt},
        ],
    )

    return {
        "ok": True,
        "info_pasta": info_pasta,
        "xmls_retorno": [os.path.basename(x) for x in xmls_retorno[:5]],
        "xmls_envio":   [os.path.basename(x) for x in xmls_envio[:5]],
        "caminho_acbr": caminho_acbr,
        "erros_extraidos": erros_nfse,
        "diagnostico": resposta.choices[0].message.content,
    }


def _montar_prompt(info_pasta, conteudo_retorno, conteudo_envio,
                   erros_extraidos, conteudo_acbr, caminho_acbr):
    erros_str = "\n".join(
        "{campo}: {valor}".format(**e) for e in erros_extraidos if "campo" in e
    ) or "Nenhum erro estruturado extraido"

    return (
        "Analise os XMLs de NFS-e e a configuracao ACBr abaixo.\n\n"
        "## Pasta de XMLs\n"
        "Data: {pasta_data}\n"
        "Envio: {envio}\n"
        "Retorno: {retorno}\n\n"
        "## Erros extraidos do retorno da prefeitura\n{erros}\n\n"
        "## XML de retorno da prefeitura\n```xml\n{retorno_xml}\n```\n\n"
        "## XML de envio (contexto)\n```xml\n{envio_xml}\n```\n\n"
        "## Configuracao ACBr ({acbr_path})\n```\n{acbr}\n```\n\n"
        "Com base nos dados acima:\n"
        "1. Qual o erro retornado pela prefeitura/provedor?\n"
        "2. Por que aconteceu?\n"
        "3. A configuracao do ACBr esta correta para este provedor?\n"
        "4. O que deve ser alterado: no FarmaFacil, na configuracao ACBr, ou no cadastro?\n"
    ).format(
        pasta_data=info_pasta.get("pasta_data", ""),
        envio=info_pasta.get("envio") or "nao encontrado",
        retorno=info_pasta.get("retorno") or "nao encontrado",
        erros=erros_str,
        retorno_xml=conteudo_retorno[:3000] if conteudo_retorno else "XML nao encontrado",
        envio_xml=conteudo_envio or "XML nao encontrado",
        acbr_path=caminho_acbr or "nao encontrado",
        acbr=conteudo_acbr[:3000] if conteudo_acbr else "Arquivo nao encontrado",
    )
