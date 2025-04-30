<?php
/********************************************************************************************************/
/*                                  Prefeitura Municipal de Curitiba                                    */
/*                     Blueprint para conexão com Webservice Piloto - v1 - Dez/2018                     */
/********************************************************************************************************/
/*                       Desenvolvido por: Instituto das Cidades Inteligentes - ICI                     */
/********************************************************************************************************/


/************************************* Configurando ambiente ********************************************

- Habilite o cURL em seu arquivo de configuração "php.ini"
    Procure por "extension=php_curl.dll" dentro de seu "php.ini".
    Se houver um ponto vírgula na frente (ex: ;extension=php_curl.dll) remova-o que a DLL será habilitada.

*/

/******************************* Geração da chave e certificado .pem ************************************

Para sistemas operacionais Windows, efetue o download e instalação do Win32OpenSSL seguindo a arquitetura 
do OS (x86 ou x64) através do endereço https://slproweb.com/products/Win32OpenSSL.html .

Será necessário gerar a chave e certificado .pem através do arquivo .pfx .
Abaixo seguem as linhas de comando para cada arquivo:

OBS: O comando 'openssl' deve ser executado na pasta raiz da instalação do Win32OpenSSL.
--------------------------------------------------- Key ------------------------------------------------
> openssl pkcs12 -in Caminho_do_certificado\Certificado.pfx -nocerts -out Caminho_do_certificado\key.pem

----------------------------------------------- Certificado --------------------------------------------
> openssl pkcs12 -in Caminho_do_certificado\Certificado.pfx -clcerts -nokeys -out Caminho_do_certificado\cert.pem

Atenção! 
A chave (key) e o certificado são necessários no formato .pem para envio através do método a seguir.

*/

/************************************* Parâmetros iniciais **********************************************/
//  Preencha a URL do Webservice da Piloto
$url_webservice = "https://piloto-iss.curitiba.pr.gov.br/nfse_ws/nfsews.asmx?WSDL";

//  Preencha com o caminho da pasta do Arquivo XML a ser enviado
$caminho_arquivo_xml = getcwd() . "\XML\CancelarLoteRPS.xml";

//  Preencha com o caminho do certificado (.pem)
$pem_certificado = getcwd() . "\Certificados\cert.pem";

//  Preencha com o caminho da key do certificado (.pem)
$key_certificado = getcwd() . "\Certificados\key.pem";

//  Preencha com a senha do certificado
$senha_certificado = "123456";

//  Ativar modo de depuração - Recomendado ativar (true) quando não retornar resposta do servidor
$modoDepuracao = false;

/****************************************** Definir método **********************************************/
/* 
    CancelarLoteNfse
    CancelarLoteRps
    CancelarNfse
    ConsultarLoteRps
    ConsultarNfse
    ConsultarNfsePorRps
    ConsultarSituacaoLoteRps
    RecepcionarLoteRps
    RecepcionarXml
    ValidarXml
*/
// Preencha a variável $metodo com uma das opções acima
$metodo = "CancelarLoteNfse"; 


/*************************** Leitura, parametrização e envio dos arquivos *******************************/
$xml = file_get_contents($caminho_arquivo_xml);

/**************************************** Cabeçalho SOAP ************************************************/
$headers = array(
    "POST /nfse_ws/nfsews.asmx HTTP/1.1",
    "Host: piloto-iss.curitiba.pr.gov.br",
    "Content-Type: text/xml; charset=utf-8",
    "Content-Length: " . strlen($xml),
    "SOAPAction: \"http://www.e-governeapps2.com.br/".$metodo."\""    
);

/********************************* Definindo variáveis da conexão ***************************************/
$conexao = curl_init();
curl_setopt($conexao, CURLOPT_URL, "$url_webservice");      //URL do Webservice
curl_setopt($conexao, CURLOPT_HTTPHEADER, $headers);        //Cabeçalho do Arquivo
curl_setopt($conexao, CURLOPT_POST, True);                  //Definir envio como POST (Default: True)
curl_setopt($conexao, CURLOPT_SSLKEY, $key_certificado);    //Caminho para Chave SSL (*.pem)   
curl_setopt($conexao, CURLOPT_SSLCERT, $pem_certificado);   //Caminho para Certificado SSL (*.pem)
curl_setopt($conexao, CURLOPT_SSLCERTPASSWD, $senha_certificado);   //Senha do certificado
curl_setopt($conexao, CURLOPT_POSTFIELDS, $xml);            //Especifica dados para POST para o servidor (Arquivo XML)
curl_setopt($conexao, CURLOPT_RETURNTRANSFER, True);        //Retorno da conexão (Default: True)
curl_setopt($conexao, CURLOPT_SSL_VERIFYHOST, 2);           //Validação de URL de conexão do servidor com a pretendida no envio (Default: 2)
curl_setopt($conexao, CURLOPT_SSL_VERIFYPEER, False);       //Verificação da cadeia de certificados SSL (Default: False)
curl_setopt($conexao, CURLOPT_VERBOSE, $modoDepuracao);     //Modo de depuração (Default: False)

/********************************* Estabelecer conexão e enviar ****************************************/
$resultado = curl_exec($conexao);

/*************************************** Fechando conexão **********************************************/
curl_close($conexao);

/************************************** Resposta do envio **********************************************/
print_r($resultado);
?>