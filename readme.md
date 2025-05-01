# Projeto Integração RPS/NFS-e - Google Sheets para FTP

---

## Escopo

O objetivo do projeto é automatizar a emissão de notas fiscais de serviço eletrônicas (NFS-e) a partir de dados armazenados em uma planilha do Google Sheets.  
O sistema irá ler as informações da planilha, criar os documentos de RPS (Recibo Provisório de Serviço), enviar para a Prefeitura de Curitiba para formalizar a NFS-e, e acompanhar o status do processo.  
O envio será feito por meio do servidor FTP da empresa, usando o certificado digital existente, e em alguns casos será possível gerar um arquivo PDF para facilitar a visualização.

---

## Pontos Técnicos Importantes

- **Formato de Comunicação:**  
  Todas as trocas de dados seguem o padrão **XML** e utilizam o modelo **WS-I Basic Profile -- NFS-e Nacionais**, com o tipo de comunicação **Document/Literal Wrapped**.

- **Assinatura Digital:**  
  Os arquivos XML devem ser **assinados digitalmente** com certificado ICP-Brasil tipo A1 ou A3, respeitando o padrão de assinatura XML (XMLDSig).  
  A assinatura precisa ser feita nos elementos corretos (`InfRps` e `InfLoteRps`) antes do envio.

- **Certificado Digital:**  
  Deve ser utilizado certificado digital válido, emitido por Autoridade Certificadora reconhecida pela ICP-Brasil.  
  O certificado também é exigido para autenticação na comunicação SSL.

- **Envio dos Arquivos:**  
  O envio dos arquivos XML será feito via **FTP** seguro para o servidor da empresa.  
  O projeto não fará envio direto para o sistema da Prefeitura.

- **Validação dos XMLs:**  
  Todos os XMLs gerados devem ser validados com seus respectivos **arquivos XSD** fornecidos pela Prefeitura antes do envio.

- **Consulta de Retornos:**  
  O sistema deverá ter um processo de consulta para verificar se as RPS enviadas foram aceitas, rejeitadas ou convertidas em NFS-e.

- **Geração de PDF (opcional):**  
  Quando aplicável, o XML da NFS-e poderá ser convertido em arquivo PDF para facilitar o acesso ou impressão do documento.

- **Padrão de Nomeação:**  
  Todos os arquivos, variáveis, funções e métodos devem seguir o padrão da linguagem (snake_case para Python), usando **nomes em português**, intuitivos e autoexplicativos.

---

## Lista de Tarefas

### 1. Conexão e Extração de Dados

- [X] Configurar acesso autorizado ao Google Sheets.
- [X] Ler e mapear os dados necessários da planilha.

### 2. Processamento e Validação de Dados

- [X] Verificar obrigatoriedade dos campos exigidos pela Prefeitura.
- [ ] Tratar formatação dos dados (datas, valores numéricos, CPF/CNPJ).
- [ ] Validar se o número de RPS está conforme sequencial.

### 3. Geração de XML

- [ ] Gerar o XML do Lote de RPS conforme padrão ABRASF/NFS-e (EnviarLoteRpsEnvio -> LoteRps -> ListaRps -> Rps).
- [ ] Gerar cada RPS com os dados obrigatórios.
- [ ] Respeitar todos os esquemas XSD disponibilizados pela Prefeitura.

### 4. Assinatura Digital de XML

- [ ] Assinar digitalmente os elementos `InfRps` e `InfLoteRps`.
- [ ] Garantir que o XML assinado esteja válido sem informações redundantes (sem KeyValue, Modulus, etc.).

### 5. Envio dos Arquivos

- [ ] Conectar ao servidor FTP usando as credenciais fornecidas.
- [ ] Enviar os arquivos XML assinados para a pasta correta.
- [ ] Confirmar o envio e registrar logs dos envios.

### 6. Consulta de Status

- [ ] Criar processo para verificar se há resposta da Prefeitura no FTP.
- [ ] Baixar arquivos de resposta XML.
- [ ] Interpretar o status dos envios (processado, erro, rejeitado).

### 7. Geração de PDF

- [ ] Implementar geração de PDF a partir dos XMLs de RPS e NFS-e.

### 8. Controle de Logs

#### - [ ] Implementar registro de logs para:
  - [ ] Envio de arquivos
  - [ ] Respostas recebidas
  - [ ] Falhas e erros no processo

### 9. Documentação

- [ ] Elaborar manual de uso do sistema.
- [ ] Criar documentação técnica básica para instalação, configuração e manutenção.

---

## Estrutura de Pastas

<!-- Sendo desenvolvido -->
manual_exemplo_sistema_prefeitura/  # Manual fornecido pela prefeitura
        NFSE-NACIONAL_ManualDeIntegracao_Curitiba-v1.pdf # Descrição de cada detalhe

## Pastas que não estão no código por questão de segurança
acesso_servidor_ftp/ # Informações da empresa
seguranca_privacidade/ # Conta usada para manusear o google sheets
## Tecnologias usadas
Python
