import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import json

# Conforme o escopo, o acesso que o sistema terá será apenas de leitura
ESCOPO_AUTORIZACAO = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Caminhos de arquivos
ROTA_ARQUIVO_ID_PLANILHA = "acesso_servidor_ftp/id_planilha.txt"
ROTA_ARQUIVO_CREDENCIAIS = "acesso_servidor_ftp/client_google_api.json"
ROTA_TOKEN = "acesso_servidor_ftp/token.json"  # Vai ser criado automaticamente

# Intervalo da planilha a ser lido (ajuste se necessário)
DADOS_PLANILHA_SELECIONADOS = "NOVOS!A1:AS11"


def carregar_id_planilha():
    """
    Lê o ID da planilha salvo no arquivo de configuração.
    """
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

    # Acessa o google planilhas
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

    # Retorna todos os valores na planilha
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

if __name__ == "__main__":
    acessar_planilha_google_sheets()
   