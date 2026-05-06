"""
Le e parseia XMLs de NF-e e NFS-e.
"""
import xml.etree.ElementTree as ET
import re


def ler_xml(caminho):
    """Le um arquivo XML e retorna conteudo como string e como dict."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except UnicodeDecodeError:
        with open(caminho, "r", encoding="latin-1") as f:
            conteudo = f.read()

    try:
        tree = ET.parse(caminho)
        root = tree.getroot()
        dados = _xml_to_dict(root)
    except ET.ParseError as e:
        dados = {"erro_parse": str(e)}

    return {"conteudo": conteudo, "dados": dados}


def _xml_to_dict(element):
    """Converte ElementTree para dict removendo namespaces."""
    tag = re.sub(r'\{.*?\}', '', element.tag)
    result = {}

    for child in element:
        child_tag = re.sub(r'\{.*?\}', '', child.tag)
        child_data = _xml_to_dict(child)
        if child_tag in result:
            if not isinstance(result[child_tag], list):
                result[child_tag] = [result[child_tag]]
            result[child_tag].append(child_data)
        else:
            result[child_tag] = child_data

    if element.text and element.text.strip():
        if result:
            result["_text"] = element.text.strip()
        else:
            return element.text.strip()

    for attr, val in element.attrib.items():
        result["@" + attr] = val

    return result


def extrair_erros_retorno_nfe(conteudo_xml):
    """
    Extrai codigo de status, motivo e chave da NF-e do XML de retorno.
    """
    erros = []
    try:
        root = ET.fromstring(conteudo_xml)

        cstat = None
        xmotivo = None

        for elem in root.iter():
            tag = re.sub(r'\{.*?\}', '', elem.tag)
            if tag == 'cStat' and cstat is None:
                cstat = elem.text
            if tag == 'xMotivo' and xmotivo is None:
                xmotivo = elem.text

        if cstat or xmotivo:
            erros.append({"cStat": cstat or "", "xMotivo": xmotivo or ""})

        # Detalhes por nota (infProt)
        for prot in root.iter():
            tag = re.sub(r'\{.*?\}', '', prot.tag)
            if tag == 'infProt':
                erro = {}
                for filho in prot:
                    filho_tag = re.sub(r'\{.*?\}', '', filho.tag)
                    erro[filho_tag] = filho.text
                if erro:
                    erros.append(erro)

    except Exception as e:
        erros.append({"erro_leitura": str(e)})

    return erros


def extrair_erros_retorno_nfse(conteudo_xml):
    """
    Extrai erros do retorno NFS-e. Formato varia por provedor.
    """
    erros = []
    try:
        root = ET.fromstring(conteudo_xml)

        tags_erro = {
            'Mensagem', 'Descricao', 'MensagemRetorno',
            'ListaMensagemRetorno', 'Codigo', 'message',
            'error', 'erro', 'descricao', 'InformacoesComplementares',
        }

        for elem in root.iter():
            tag = re.sub(r'\{.*?\}', '', elem.tag)
            if tag in tags_erro:
                if elem.text and elem.text.strip():
                    erros.append({"campo": tag, "valor": elem.text.strip()})

    except Exception as e:
        erros.append({"erro_leitura": str(e)})

    return erros
