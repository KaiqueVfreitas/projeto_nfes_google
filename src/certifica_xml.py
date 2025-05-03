"""
Módulo para validação e assinatura digital de arquivos XML de NFSe com base no schema XSD
e na política de certificação digital exigida pela Prefeitura de Curitiba.

Este módulo realiza duas tarefas principais:
1. Valida os arquivos XML contra o schema XSD oficial.
2. Assina digitalmente os XMLs de acordo com o padrão XMLDSIG exigido pela Prefeitura,
   utilizando um certificado digital do tipo A1 (formato PFX).

Importante:
- O certificado de assinatura deve conter o CNPJ do emissor da NFSe ou da matriz.
- O XML NÃO deve conter tags como <X509IssuerName>, <RSAKeyValue>, etc., conforme especificação.
"""

import os
from lxml import etree
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from signxml import XMLSigner, methods

# --- CONSTANTES DE CAMINHO --- #
CAMINHO_PASTA_XML = "pdf_xml_gerados_rps"
CAMINHO_XSD = os.path.join("certificados_schemas", "ModeloNFSeValidado.xsd")
CAMINHO_CERT_PFX = os.path.join("certificados", "GRACINHA_DO_CARMO_GONCALVES_85475327904_1724777703229427900.pfx")
PASTA_XML_ASSINADO = "pdf_xml_assinados"
SENHA_PFX = b"#GRACA#28"  # Senha fornecida

# --- FUNÇÕES AUXILIARES DE VALIDAÇÃO --- #
def carregar_schema_xsd(caminho_arquivo_xsd):
    with open(caminho_arquivo_xsd, 'rb') as arquivo_xsd:
        schema_doc = etree.parse(arquivo_xsd)
        return etree.XMLSchema(schema_doc)

def listar_arquivos_xml_validos(pasta):
    return [
        os.path.join(pasta, nome)
        for nome in os.listdir(pasta)
        if nome.lower().endswith(".xml")
    ]

def validar_arquivo_xml_com_schema(caminho_xml, validador):
    try:
        with open(caminho_xml, 'rb') as arquivo:
            xml_doc = etree.parse(arquivo)
            validador.assertValid(xml_doc)
            return True, "Validação bem-sucedida."
    except (etree.DocumentInvalid, etree.XMLSyntaxError) as erro:
        return False, str(erro)

# --- EXTRAÇÃO DE CERTIFICADO DO PFX --- #
def extrair_cert_e_chave_de_pfx(caminho_pfx, senha_pfx):
    if not os.path.exists(caminho_pfx):
        raise FileNotFoundError(f"Certificado PFX não encontrado: {caminho_pfx}")

    with open(caminho_pfx, 'rb') as f:
        pfx_data = f.read()

    private_key, certificate, _ = pkcs12.load_key_and_certificates(
        data=pfx_data,
        password=senha_pfx,
        backend=default_backend()
    )

    if not private_key or not certificate:
        raise ValueError("Certificado ou chave privada não encontrados no PFX.")

    cert_pem = certificate.public_bytes(Encoding.PEM)
    key_pem = private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.TraditionalOpenSSL,
        NoEncryption()
    )

    return cert_pem, key_pem

# --- FUNÇÃO DE ASSINATURA DIGITAL --- #
def assinar_xml(xml_path):
    with open(xml_path, 'rb') as arquivo:
        xml = etree.parse(arquivo)

    elemento_alvo = xml.find(".//Nfse")
    if elemento_alvo is None:
        raise ValueError("Elemento <Nfse> não encontrado no XML.")

    cert, key = extrair_cert_e_chave_de_pfx(CAMINHO_CERT_PFX, SENHA_PFX)

    signer = XMLSigner(
        method=methods.enveloped,
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    )

    xml_assinado = signer.sign(
        data=elemento_alvo,
        key=key,
        cert=cert,
        always_add_key_value=False
    )

    nome_arquivo = os.path.basename(xml_path)
    caminho_saida = os.path.join(PASTA_XML_ASSINADO, nome_arquivo)

    if not os.path.exists(PASTA_XML_ASSINADO):
        os.makedirs(PASTA_XML_ASSINADO)

    with open(caminho_saida, 'wb') as f:
        f.write(etree.tostring(xml.getroot(), encoding='utf-8', xml_declaration=True, pretty_print=True))

    return caminho_saida

# --- FLUXO COMPLETO --- #
def validar_e_assinar_xmls():
    if not os.path.exists(CAMINHO_PASTA_XML):
        print(f"[ERRO] Pasta de entrada não encontrada: {CAMINHO_PASTA_XML}")
        return

    try:
        validador = carregar_schema_xsd(CAMINHO_XSD)
    except Exception as erro:
        print(f"[ERRO] Erro ao carregar o XSD: {erro}")
        return

    arquivos = listar_arquivos_xml_validos(CAMINHO_PASTA_XML)
    if not arquivos:
        print("[INFO] Nenhum arquivo XML para validar/assinar.")
        return

    for caminho_xml in arquivos:
        nome_arquivo = os.path.basename(caminho_xml)
        print(f"Validando {nome_arquivo}...")

        valido, mensagem = validar_arquivo_xml_com_schema(caminho_xml, validador)
        if not valido:
            print(f"  [ERRO] Validação falhou: {mensagem}")
            continue

        print("  [OK] Validação bem-sucedida. Assinando...")

        try:
            caminho_assinado = assinar_xml(caminho_xml)
            print(f"  [SUCESSO] XML assinado salvo em: {caminho_assinado}")
        except Exception as erro_ass:
            print(f"  [FALHA] Erro ao assinar XML: {erro_ass}")

if __name__ == "__main__":
    validar_e_assinar_xmls()
