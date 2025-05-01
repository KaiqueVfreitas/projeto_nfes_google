"""
Módulo para gerar XML de NFSe no formato da Prefeitura de Curitiba.
Baseado no modelo 'ArrayOfTcCompNfse' fornecido.
"""
import json
import os
from xml.etree import ElementTree as et
from datetime import datetime

# --- CONSTANTES --- #
CAMINHO_JSON = "acesso_servidor_ftp/dados_gerar_rps.json"
PASTA_SAIDA_XML = "pdf_xml_gerados_rps"
NAMESPACES = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsd": "http://www.w3.org/2001/XMLSchema"
}

# --- FUNÇÕES AUXILIARES --- #
def formatar_data_iso(data_str):
    """
    Converte datas para o padrão ISO 8601 (AAAA-MM-DDTHH:MM:SS).
    Exemplo: "04/12/2018 11:01" → "2018-12-04T11:01:00"
    """
    try:
        if "T" in data_str:  # Já está no formato ISO?
            return data_str.split(".")[0]  # Remove milissegundos se existirem
        data_obj = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
        return data_obj.strftime("%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        return "1900-01-01T00:00:00"

def criar_elemento_xml(pai, nome, texto=None, namespace=None):
    """
    Cria um elemento XML com namespace opcional.
    Exemplo: criar_elemento_xml(root, "Numero", "54")
    """
    elemento = et.SubElement(pai, nome)
    if texto is not None:
        elemento.text = str(texto)
    return elemento

# --- GERADOR XML (MODELO ArrayOfTcCompNfse) --- #
def gerar_xml_nfse(dados_nfse):
    """
    Gera o XML de NFSe no formato 'ArrayOfTcCompNfse'.
    Retorna o XML como string e o nome do arquivo gerado.
    """
    # Raiz do XML
    root = et.Element("ArrayOfTcCompNfse", attrib={
        "xmlns:xsi": NAMESPACES["xsi"],
        "xmlns:xsd": NAMESPACES["xsd"]
    })
    tc_comp_nfse = criar_elemento_xml(root, "tcCompNfse")
    nfse = criar_elemento_xml(tc_comp_nfse, "Nfse")
    inf_nfse = criar_elemento_xml(nfse, "InfNfse")

    # Dados básicos da NFSe
    criar_elemento_xml(inf_nfse, "Numero", "54")  # Número fictício (gerado pela prefeitura)
    criar_elemento_xml(inf_nfse, "CodigoVerificacao", "ZAWB3F0M")  # Código fictício
    criar_elemento_xml(inf_nfse, "DataEmissao", formatar_data_iso(dados_nfse["data_hora_emissao"]))
    criar_elemento_xml(inf_nfse, "NaturezaOperacao", dados_nfse["natureza_operacao"])
    criar_elemento_xml(inf_nfse, "OptanteSimplesNacional", dados_nfse["optante_simples_nacional"])

    # Serviço e Valores
    servico = criar_elemento_xml(inf_nfse, "Servico")
    valores = criar_elemento_xml(servico, "Valores")
    criar_elemento_xml(valores, "ValorServicos", dados_nfse["valor_servicos"])
    criar_elemento_xml(valores, "ItemListaServico", dados_nfse["item_lista_servicos"])
    criar_elemento_xml(servico, "Discriminacao", dados_nfse["discriminacao"])

    # Prestador
    prestador = criar_elemento_xml(inf_nfse, "PrestadorServico")
    identificacao_prestador = criar_elemento_xml(prestador, "IdentificacaoPrestador")
    criar_elemento_xml(identificacao_prestador, "Cnpj", dados_nfse["cnpj_prestador"])
    criar_elemento_xml(identificacao_prestador, "InscricaoMunicipal", dados_nfse["inscricao_municipal_prestador"])

    # Tomador
    tomador = criar_elemento_xml(inf_nfse, "TomadorServico")
    identificacao_tomador = criar_elemento_xml(tomador, "IdentificacaoTomador")
    cpf_cnpj = criar_elemento_xml(identificacao_tomador, "CpfCnpj")
    criar_elemento_xml(cpf_cnpj, "Cnpj", dados_nfse["cnpj_tomador"])
    criar_elemento_xml(tomador, "RazaoSocial", dados_nfse["razao_social_tomador"])

    # Endereço do Tomador
    endereco = criar_elemento_xml(tomador, "Endereco")
    criar_elemento_xml(endereco, "Endereco", dados_nfse["endereco_tomador"])
    criar_elemento_xml(endereco, "Numero", dados_nfse["numero"])
    criar_elemento_xml(endereco, "Complemento", dados_nfse["complemento"])

    # Converter para string
    et.indent(root, space="    ")  # Melhora legibilidade (Python 3.9+)
    xml_str = et.tostring(root, encoding="utf-8", xml_declaration=True).decode()

    # Salvar em arquivo
    nome_arquivo = f"nfse_{dados_nfse['id']}.xml"
    with open(os.path.join(PASTA_SAIDA_XML, nome_arquivo), "w", encoding="utf-8") as f:
        f.write(xml_str)

    return xml_str, nome_arquivo

# --- FLUXO PRINCIPAL --- #
def gerar_nfse_a_partir_de_json():
    """Lê o JSON e gera um XML para cada RPS."""
    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")
        return

    for nfse in dados:
        xml_str, nome_arquivo = gerar_xml_nfse(nfse)
        print(f"XML gerado: {nome_arquivo}")

if __name__ == "__main__":
    if not os.path.exists(PASTA_SAIDA_XML):
        os.makedirs(PASTA_SAIDA_XML)
    gerar_nfse_a_partir_de_json()