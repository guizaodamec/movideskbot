"""
Localiza automaticamente as pastas de XMLs NF-e e NFS-e do FarmaFacil.
"""
import os
import glob
import getpass
from datetime import datetime


def get_current_user():
    try:
        return getpass.getuser()
    except Exception:
        return "FarmaFacil"


def find_nfe_folder():
    """
    Busca a pasta de XMLs NF-e em cascata.
    Retorna o primeiro caminho encontrado ou None.
    """
    usuario = get_current_user()

    caminhos = [
        r"C:\PharmaFacil\NFE",
        r"C:\FarmaFacil\NFE",
        os.path.join("C:\\Users", usuario, "PharmaFacil", "NFE"),
        os.path.join("C:\\Users", usuario, "FarmaFacil", "NFE"),
        os.path.join("C:\\Users", usuario, "AppData", "Local", "PharmaFacil", "NFE"),
        os.path.join("C:\\Users", usuario, "AppData", "Local", "FarmaFacil", "NFE"),
        r"C:\Prisma\NFE",
        r"C:\PrismaFive\NFE",
        r"C:\FarmaFacil\EXE\NFE",
        r"C:\PharmaFacil\EXE\NFE",
    ]

    for caminho in caminhos:
        if os.path.exists(caminho):
            return caminho

    return None


def find_nfse_folder():
    """
    Busca a pasta NFS-e mais recente dentro do diretorio XZ.
    Estrutura: .../XZ/YYYY-MM/envio e .../XZ/YYYY-MM/retorno
    Retorna dict com: base, pasta_data, envio, retorno
    """
    usuario = get_current_user()

    bases_xz = [
        os.path.join("C:\\Users", usuario, "FarmaFacil", "EXE", "XZ"),
        os.path.join("C:\\Users", usuario, "PharmaFacil", "EXE", "XZ"),
        r"C:\FarmaFacil\EXE\XZ",
        r"C:\PharmaFacil\EXE\XZ",
        os.path.join("C:\\Users", usuario, "AppData", "Local", "FarmaFacil", "EXE", "XZ"),
    ]

    for base in bases_xz:
        if not os.path.exists(base):
            continue

        subpastas = []
        for item in os.listdir(base):
            caminho_item = os.path.join(base, item)
            if os.path.isdir(caminho_item):
                subpastas.append(item)

        if not subpastas:
            continue

        subpastas.sort(reverse=True)
        pasta_mais_recente = subpastas[0]
        caminho_data = os.path.join(base, pasta_mais_recente)

        envio = os.path.join(caminho_data, "envio")
        retorno = os.path.join(caminho_data, "retorno")

        return {
            "base": base,
            "pasta_data": pasta_mais_recente,
            "caminho_data": caminho_data,
            "envio": envio if os.path.exists(envio) else None,
            "retorno": retorno if os.path.exists(retorno) else None,
        }

    return None


def find_acbr_config():
    """
    Busca o arquivo de configuracao ACBr (servicos.xml.n).
    """
    usuario = get_current_user()

    caminhos = [
        r"C:\FarmaFacil\EXE\ACBr\servicos.xml.n",
        r"C:\PharmaFacil\EXE\ACBr\servicos.xml.n",
        os.path.join("C:\\Users", usuario, "FarmaFacil", "EXE", "ACBr", "servicos.xml.n"),
        os.path.join("C:\\Users", usuario, "PharmaFacil", "EXE", "ACBr", "servicos.xml.n"),
        r"C:\FarmaFacil\ACBr\servicos.xml.n",
    ]

    for caminho in caminhos:
        if os.path.exists(caminho):
            return caminho

    return None


def list_nfe_xmls(pasta, limit=20):
    """
    Lista os XMLs de NF-e mais recentes em uma pasta.
    """
    if not pasta or not os.path.exists(pasta):
        return []

    xmls = glob.glob(os.path.join(pasta, "*.xml"))
    xmls.sort(key=os.path.getmtime, reverse=True)

    resultado = []
    for xml in xmls[:limit]:
        nome = os.path.basename(xml)
        tipo = _classificar_xml_nfe(nome)
        resultado.append({
            "caminho": xml,
            "nome": nome,
            "tipo": tipo,
            "tamanho": os.path.getsize(xml),
            "modificado": datetime.fromtimestamp(os.path.getmtime(xml)).strftime("%d/%m/%Y %H:%M:%S"),
        })

    return resultado


def _classificar_xml_nfe(nome_arquivo):
    """Classifica o tipo de XML pelo nome do arquivo."""
    nome = nome_arquivo.lower()
    if "ret" in nome or "retorno" in nome:
        return "retorno"
    elif "proc" in nome or "protocolo" in nome:
        return "protocolo"
    elif "canc" in nome or "cancel" in nome:
        return "cancelamento"
    elif "env" in nome or "envio" in nome:
        return "envio"
    else:
        return "desconhecido"
