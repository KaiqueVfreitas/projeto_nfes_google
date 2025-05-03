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

DADOS_FIXOS_PRESTADOR = {
    "cnpj": "38057542000254",
    "inscricao_municipal": "11126723",
    "nome_fantasia": "GRACINHA DO CARMO GONCALVES  LTDA",
    "endereco": "R. 1º DE MAIO",
    "numero": "1515",
    "bairro": "XAXIM",
    "codigo_municipio": "4106902",
    "uf": "PR",
    "cep": "81820340"
}

# --- FUNÇÕES AUXILIARES --- #
def formatar_data_iso(data_str):
    try:
        if "T" in data_str:
            return data_str.split(".")[0]  # Remove milissegundos se existirem
        data_obj = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
        return data_obj.strftime("%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        return "1900-01-01T00:00:00"

def extrair_codigo(valor):
    return valor.split()[0] if valor else ""

def criar_elemento_xml(pai, nome, texto=None):
    elemento = et.SubElement(pai, nome)
    if texto is not None:
        elemento.text = str(texto)
    return elemento

# --- GERADOR XML (MODELO ArrayOfTcCompNfse) --- #
def gerar_xml_nfse(dados_nfse):
    root = et.Element("ArrayOfTcCompNfse", attrib={
        "xmlns:xsi": NAMESPACES["xsi"],
        "xmlns:xsd": NAMESPACES["xsd"]
    })
    tc_comp_nfse = criar_elemento_xml(root, "tcCompNfse")
    nfse = criar_elemento_xml(tc_comp_nfse, "Nfse")
    inf_nfse = criar_elemento_xml(nfse, "InfNfse")

    criar_elemento_xml(inf_nfse, "Numero", dados_nfse.get("numero_rps", ""))
    criar_elemento_xml(inf_nfse, "CodigoVerificacao", "ZAWB3F0M")
    criar_elemento_xml(inf_nfse, "DataEmissao", formatar_data_iso(dados_nfse.get("data_hora_emissao")))
    criar_elemento_xml(inf_nfse, "DataEmissaoRps", formatar_data_iso(dados_nfse.get("data_hora_emissao")))
    criar_elemento_xml(inf_nfse, "NaturezaOperacao", extrair_codigo(dados_nfse.get("natureza_operacao", "1")))
    criar_elemento_xml(inf_nfse, "RegimeEspecialTributacao", dados_nfse.get("regime_especial_tributacao", "0"))
    criar_elemento_xml(inf_nfse, "OptanteSimplesNacional", extrair_codigo(dados_nfse.get("optante_simples_nacional", "1")))
    criar_elemento_xml(inf_nfse, "IncentivadorCultural", extrair_codigo(dados_nfse.get("incentivador_cultural", "2")))
    criar_elemento_xml(inf_nfse, "Competencia", formatar_data_iso(dados_nfse.get("data_hora_emissao")))
    criar_elemento_xml(inf_nfse, "NfseSubstituida", "0")

    servico = criar_elemento_xml(inf_nfse, "Servico")
    valores = criar_elemento_xml(servico, "Valores")
    criar_elemento_xml(valores, "ValorServicos", dados_nfse.get("valor_servicos", "0.00"))
    criar_elemento_xml(valores, "ValorDeducoes", dados_nfse.get("valor_deducoes", "0.00"))
    criar_elemento_xml(valores, "ValorPis", dados_nfse.get("valor_pis", "0.00"))
    criar_elemento_xml(valores, "ValorCofins", dados_nfse.get("valor_cofins", "0.00"))
    criar_elemento_xml(valores, "ValorInss", dados_nfse.get("valor_inss", "0.00"))
    criar_elemento_xml(valores, "ValorIr", dados_nfse.get("valor_ir", "0.00"))
    criar_elemento_xml(valores, "ValorCsll", dados_nfse.get("valor_csll", "0.00"))
    criar_elemento_xml(valores, "IssRetido", extrair_codigo(dados_nfse.get("iss_retido", "2")))
    criar_elemento_xml(valores, "ValorIss", dados_nfse.get("valor_iss", "0.00"))
    criar_elemento_xml(valores, "ValorIssRetido", dados_nfse.get("valor_iss_retido", "0.00"))
    criar_elemento_xml(valores, "OutrasRetencoes", dados_nfse.get("outras_retencoes", "0.00"))
    criar_elemento_xml(valores, "BaseCalculo", dados_nfse.get("base_calculo", "0.00"))
    criar_elemento_xml(valores, "Aliquota", dados_nfse.get("aliquota", "0.00"))
    criar_elemento_xml(valores, "ValorLiquidoNfse", dados_nfse.get("valor_liquido_nfse", "0.00"))
    criar_elemento_xml(valores, "DescontoIncondicionado", dados_nfse.get("desconto_incondicionado", "0.00"))
    criar_elemento_xml(valores, "DescontoCondicionado", dados_nfse.get("desconto_condicionado", "0.00"))
    criar_elemento_xml(servico, "ItemListaServico", dados_nfse.get("item_lista_servicos", ""))
    criar_elemento_xml(servico, "CodigoCnae", "0")
    criar_elemento_xml(servico, "Discriminacao", dados_nfse.get("discriminacao", ""))
    criar_elemento_xml(servico, "CodigoMunicipio", dados_nfse.get("cod_municipio_servico", "0"))

    criar_elemento_xml(inf_nfse, "ValorCredito", dados_nfse.get("valor_credito", "0.00"))

    prestador = criar_elemento_xml(inf_nfse, "PrestadorServico")
    identificacao_prestador = criar_elemento_xml(prestador, "IdentificacaoPrestador")
    criar_elemento_xml(identificacao_prestador, "Cnpj", DADOS_FIXOS_PRESTADOR["cnpj"])
    criar_elemento_xml(identificacao_prestador, "InscricaoMunicipal", DADOS_FIXOS_PRESTADOR["inscricao_municipal"])
    criar_elemento_xml(prestador, "NomeFantasia", DADOS_FIXOS_PRESTADOR["nome_fantasia"])
    endereco_prestador = criar_elemento_xml(prestador, "Endereco")
    criar_elemento_xml(endereco_prestador, "Endereco", DADOS_FIXOS_PRESTADOR["endereco"])
    criar_elemento_xml(endereco_prestador, "Numero", DADOS_FIXOS_PRESTADOR["numero"])
    criar_elemento_xml(endereco_prestador, "Bairro", DADOS_FIXOS_PRESTADOR["bairro"])
    criar_elemento_xml(endereco_prestador, "CodigoMunicipio", DADOS_FIXOS_PRESTADOR["codigo_municipio"])
    criar_elemento_xml(endereco_prestador, "Uf", DADOS_FIXOS_PRESTADOR["uf"])
    criar_elemento_xml(endereco_prestador, "Cep", DADOS_FIXOS_PRESTADOR["cep"])

    tomador = criar_elemento_xml(inf_nfse, "TomadorServico")
    identificacao_tomador = criar_elemento_xml(tomador, "IdentificacaoTomador")
    cpf_cnpj = criar_elemento_xml(identificacao_tomador, "CpfCnpj")
    if dados_nfse.get("cnpj_tomador"):
        criar_elemento_xml(cpf_cnpj, "Cnpj", dados_nfse.get("cnpj_tomador"))
    else:
        criar_elemento_xml(cpf_cnpj, "Cpf", dados_nfse.get("cpf_tomador", ""))
    criar_elemento_xml(tomador, "RazaoSocial", dados_nfse.get("razao_social_tomador", ""))
    endereco_tomador = criar_elemento_xml(tomador, "Endereco")
    criar_elemento_xml(endereco_tomador, "Endereco", dados_nfse.get("endereco_tomador", ""))
    criar_elemento_xml(endereco_tomador, "Numero", dados_nfse.get("numero", ""))
    criar_elemento_xml(endereco_tomador, "Complemento", dados_nfse.get("complemento", ""))
    criar_elemento_xml(endereco_tomador, "Bairro", dados_nfse.get("bairro", ""))
    criar_elemento_xml(endereco_tomador, "CodigoMunicipio", dados_nfse.get("cod_municipio_tomador", "0"))
    criar_elemento_xml(endereco_tomador, "Uf", dados_nfse.get("uf", ""))
    criar_elemento_xml(endereco_tomador, "Cep", dados_nfse.get("cep", ""))
    contato = criar_elemento_xml(tomador, "Contato")
    criar_elemento_xml(contato, "Email", dados_nfse.get("email_tomador", ""))

    et.indent(root, space="    ")
    xml_str = et.tostring(root, encoding="utf-8", xml_declaration=True).decode()

    nome_arquivo = f"nfse_{dados_nfse['id']}.xml"
    with open(os.path.join(PASTA_SAIDA_XML, nome_arquivo), "w", encoding="utf-8") as f:
        f.write(xml_str)

    return xml_str, nome_arquivo

def gerar_nfse_a_partir_de_json():
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