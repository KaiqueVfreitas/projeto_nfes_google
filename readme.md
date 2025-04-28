# Integração RPS/NFS-e Curitiba - Google Sheets para FTP

## Pontos Técnicos Importantes
- Toda troca de informações será feita em *XML, seguindo o padrão **NFS-e Nacional*.
- Comunicação baseada no *WS-I Basic Profile, modelo **Document/Literal Wrapped*.
- Utilização obrigatória de *certificado digital ICP-Brasil (A1 ou A3)* para assinatura dos XMLs.
- Conexão segura via *SSL/TLS*.
- O envio dos arquivos será realizado via *FTP* para o servidor disponibilizado.
- O XML deve ser *validado pelo XSD* fornecido pela prefeitura antes do envio.
- Em casos específicos, poderá ser gerado *PDF* a partir das NFS-e para o cliente.
- Implementação de rotina de *consulta de status* de processamento do RPS/NFS-e.
- *Padrão de nomeação*: 
  - Seguir sempre as recomendações da linguagem (ex: snake_case no Python, camelCase no JavaScript).
  - Usar *nomes em português, **intuitivos e autoexplicativos* (ex.: gerar_xml_rps, enviar_para_ftp).

---

## Lista de Tarefas

### 1. Conexão e extração de dados

- [ ] Configurar acesso ao Google Sheets via gspread e google-auth.
- [ ] Ler e mapear os dados necessários da planilha.

### 2. Processamento de dados

- [ ] Validar os campos obrigatórios conforme o layout exigido pela prefeitura.
- [ ] Tratar dados para formatação correta (datas, números, CPF/CNPJ).

### 3. Geração de XML

- [ ] Criar XMLs conforme estrutura exigida (EnviarLoteRpsEnvio -> LoteRps -> ListaRps -> Rps).
- [ ] Validar os XMLs gerados contra os arquivos XSD.

### 4. Assinatura de XML

- [ ] Assinar digitalmente os XMLs usando o certificado ICP-Brasil.
- [ ] Assinar corretamente os elementos exigidos (InfRps e InfLoteRps).

### 5. Envio dos arquivos

- [ ] Conectar ao servidor FTP (ftp.gb.stackcp.com) usando ftplib ou ftplib.FTP_TLS.
- [ ] Fazer upload dos arquivos XML assinados para a pasta correta.

### 6. Consulta de status

- [ ] Implementar rotina de consulta de retorno no FTP (aguardar/baixar arquivos de resposta).
- [ ] Interpretar o status do lote (processado com sucesso, erro, etc).

### 7. Geração de PDF (Opcional)

- [ ] Criar PDFs das NFS-e a partir dos dados recebidos (usando WeasyPrint, reportlab, ou equivalente).

### 8. Controle de logs

- [ ] Registrar eventos importantes como envios, respostas e erros em arquivos de log ou banco de dados.

### 9. Documentação

- [ ] Criar um manual resumido de operação e manutenção do sistema.
- [ ] Gerar um guia de instalação e configuração dos componentes do projeto.

---

## Estrutura sugerida de pastas

```plaintext
/src
  /google_sheets/
    leitor_planilha.py
  /xml/
    gerador_xml.py
    assinador_xml.py
  /ftp/
    envio_ftp.py
    recebimento_ftp.py
  /nfs_e/
    gerador_pdf.py
  main.py
/logs/
/data/
  /xmls_enviados/
  /xmls_retorno/
requirements.txt
README.md 

