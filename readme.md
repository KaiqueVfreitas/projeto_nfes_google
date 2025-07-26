# 📦 integracao_rps_nfse

## 🧠 O que é o projeto?
Automação da emissão de Notas Fiscais de Serviço Eletrônicas (NFS-e) com base em dados do Google Sheets.  
O sistema gera os XMLs de RPS conforme o padrão da Prefeitura de Curitiba, assina digitalmente com certificado ICP-Brasil, envia via FTP para máquina do cliente e consulta o status no webservice da prefeitura.  
Também gera PDFs dos documentos e envia para os clientes, mantendo logs e estrutura modular para manutenção e expansão.

## 📊 Status do projeto
Finalizado, projeto foi entregue para o cliente que solicitou com êxito, por isso está não é a versão refatora e usada em produção (está a 6 versões da oficial), além de incompleto

## 🚀 Como rodar o projeto
Passo a passo para executar localmente:

```bash
# Clone o repositório
git clone https://github.com/KaiqueVfreitas/integracao_rps_nfse.git

# Acesse a pasta do projeto
cd integracao_rps_nfse

# (Recomenda-se uso de virtualenv)
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências (se houver requirements.txt)
pip install -r requirements.txt

# Execute o script principal
python criacao_rps.py
