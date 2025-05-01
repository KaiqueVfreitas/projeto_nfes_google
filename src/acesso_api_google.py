import os.path
import re
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


ESCOPO_AUTORIZACAO = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
ROTA_ARQUIVO_ID_PLANILHA = "acesso_servidor_ftp/id_planilha.txt"
ROTA_ARQUIVO_CREDENCIAIS = "acesso_servidor_ftp/client_google_api.json"
ROTA_TOKEN = "acesso_servidor_ftp/token.json"
DADOS_PLANILHA_SELECIONADOS = "emitirNFSe!A1:AP10"
CAMINHO_JSON_FINAL = "acesso_servidor_ftp/dados_gerar_rps.json"




def padrao_vazio(valor):
    """
    Retorna o valor tratado: se estiver vazio ou None, retorna ""; senão, retorna o valor limpo.
    """
    if valor is None:
        return ""
    if isinstance(valor, str):
        return valor.strip()
    return valor



def carregar_id_planilha():
    try:
        with open(ROTA_ARQUIVO_ID_PLANILHA, "r") as arquivo_id:
            conteudo = arquivo_id.read().strip()
            chave, valor = conteudo.split("=")
            if chave == "ID_PLANILHA":
                return valor
            else:
                raise ValueError("Formato inválido no arquivo id_planilha.txt")
    except Exception as erro:
        print(f"Erro ao carregar o ID da planilha: {erro}")
        return None




def acessar_planilha_google_sheets():
    credenciais = None

    if os.path.exists(ROTA_TOKEN):
        credenciais = Credentials.from_authorized_user_file(ROTA_TOKEN, ESCOPO_AUTORIZACAO)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            fluxo_autenticacao = InstalledAppFlow.from_client_secrets_file(
                ROTA_ARQUIVO_CREDENCIAIS, ESCOPO_AUTORIZACAO
            )
            credenciais = fluxo_autenticacao.run_local_server(port=0)

        with open(ROTA_TOKEN, "w") as arquivo_token:
            arquivo_token.write(credenciais.to_json())

    try:
        servico_planilhas = build('sheets', 'v4', credentials=credenciais)
        planilha = servico_planilhas.spreadsheets()

        id_planilha = carregar_id_planilha()

        if id_planilha:
            resultado = planilha.values().get(
                spreadsheetId=id_planilha,
                range=DADOS_PLANILHA_SELECIONADOS
            ).execute()

            dados_planilha = resultado.get('values', [])

            if not dados_planilha:
                print("Nenhum dado encontrado na planilha.")
                return []

            print("Leitura da planilha concluída com sucesso.")
            return dados_planilha

        else:
            print("Não foi possível carregar o ID da planilha.")
            return []

    except HttpError as erro:
        print(f"Ocorreu um erro ao acessar a API do Google Sheets: {erro}")
        return []


def atributo_identificador_unico(numero_lote, cnpj_prestador, inscricao_municipal_prestador):
    texto_concatenado = f"{numero_lote}-{cnpj_prestador}-{inscricao_municipal_prestador}".lower()
    texto_limpo = re.sub(r'[^a-zA-Z0-9]', '', texto_concatenado)
    return texto_limpo



def verificacao_atributo_identificador(identificador, lista_existente):
    contador = 1
    novo_identificador = identificador
    while novo_identificador in lista_existente:
        contador += 1
        novo_identificador = f"{identificador}-{contador}"
    return novo_identificador




def passagem_lista_json(lista_dados_planilha):
    json_formatado = []
    identificadores_gerados = set()

    # Captura o cabeçalho da planilha (títulos das colunas)
    cabecalhos = lista_dados_planilha[0]

    for linha in lista_dados_planilha[1:]:
        dados_linha = dict(zip(cabecalhos, linha))

        numero_lote = padrao_vazio(dados_linha.get("Número do Lote"))
        cnpj_prestador = padrao_vazio(dados_linha.get("CNPJ do Prestador"))
        inscricao_municipal_prestador = padrao_vazio(dados_linha.get("Inscrição Municipal do Prestador"))

        identificador_base = atributo_identificador_unico(numero_lote, cnpj_prestador, inscricao_municipal_prestador)
        identificador_unico = verificacao_atributo_identificador(identificador_base, identificadores_gerados)
        identificadores_gerados.add(identificador_unico)

        estrutura_json = {
            "id": identificador_unico,
            "numero_lote": numero_lote,
            "cnpj_prestador": cnpj_prestador,
            "inscricao_municipal_prestador": padrao_vazio(dados_linha.get("Inscrição Municipal do Prestador")),
            "qntd_rps": padrao_vazio(dados_linha.get("Quantidade de RPS")),
            "numero_rps": padrao_vazio(dados_linha.get("Número do RPS")),
            "serie_rps": padrao_vazio(dados_linha.get("Série do RPS")),
            "tipo_rps": padrao_vazio(dados_linha.get("Tipo de RPS")),
            "data_hora_emissao": padrao_vazio(dados_linha.get("Data de Emissão")),
            "natureza_operacao": padrao_vazio(dados_linha.get("Natureza da Operação")),
            "regime_especial_tributacao": padrao_vazio(dados_linha.get("Regime Especial de Tributação")),
            "optante_simples_nacional": padrao_vazio(dados_linha.get("Optante Simples Nacional")),
            "incentivador_cultural": padrao_vazio(dados_linha.get("Incentivador Cultural")),
            "status": padrao_vazio(dados_linha.get("Status")),
            "valor_servicos": padrao_vazio(dados_linha.get("Valor dos Serviços")),
            "valor_deducoes": padrao_vazio(dados_linha.get("Valor das Deduções")),
            "valor_pis": padrao_vazio(dados_linha.get("Valor PIS")),
            "valor_cofins": padrao_vazio(dados_linha.get("Valor Cofins")),
            "valor_inss": padrao_vazio(dados_linha.get("Valor INSS")),
            "valor_ir": padrao_vazio(dados_linha.get("Valor IR")),
            "valor_csll": padrao_vazio(dados_linha.get("Valor CSLL")),
            "iss_retido": padrao_vazio(dados_linha.get("ISS Retido")),
            "valor_iss": padrao_vazio(dados_linha.get("Valor ISS")),
            "valor_iss_retido": padrao_vazio(dados_linha.get("Valor ISS Retido")),
            "outras_retencoes": padrao_vazio(dados_linha.get("Outras Retencoes")),
            "base_calculo": padrao_vazio(dados_linha.get("Base de Cálculo")),
            "aliquota": padrao_vazio(dados_linha.get("Aliquota")),
            "valor_liquido_nfse": padrao_vazio(dados_linha.get("Valor Liquido da NFSe")),
            "desconto_incondicionado": padrao_vazio(dados_linha.get("Desconto Incondicionado")),
            "desconto_condicionado": padrao_vazio(dados_linha.get("Desconto Condicionado")),
            "item_lista_servicos": padrao_vazio(dados_linha.get("Item da Lista de Servicos")),
            "discriminacao": padrao_vazio(dados_linha.get("Discriminação")),
            "cod_municipio_servico": padrao_vazio(dados_linha.get("Código do Município do Serviço")),
            "cnpj_tomador": padrao_vazio(dados_linha.get("CNPJ do Tomador")),
            "razao_social_tomador": padrao_vazio(dados_linha.get("Razão Social do Tomador")),
            "endereco_tomador": padrao_vazio(dados_linha.get("Endereço do Tomador")),
            "numero": padrao_vazio(dados_linha.get("Número")),
            "complemento": padrao_vazio(dados_linha.get("Complemento")),
            "bairro": padrao_vazio(dados_linha.get("Bairro")),
            "cod_municipio_tomador": padrao_vazio(dados_linha.get("Código do Município do Tomador")),
            "uf": padrao_vazio(dados_linha.get("UF")),
            "cep": padrao_vazio(dados_linha.get("CEP")),
            "email_tomador": padrao_vazio(dados_linha.get("E-mail do Tomador"))
        }

        json_formatado.append(estrutura_json)

    try:
        with open(CAMINHO_JSON_FINAL, "w", encoding="utf-8") as arquivo_json:
            json.dump(json_formatado, arquivo_json, indent=4, ensure_ascii=False)
            print(f"Arquivo JSON salvo com sucesso em: {CAMINHO_JSON_FINAL}")
    except Exception as erro:
        print(f"Erro ao salvar o JSON: {erro}")

    return json_formatado



if __name__ == "__main__":
    dados_planilha = acessar_planilha_google_sheets()
    if dados_planilha:
        passagem_lista_json(dados_planilha)

