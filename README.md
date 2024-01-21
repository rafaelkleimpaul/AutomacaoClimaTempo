# Script de Automação ClimaTempo

Este script em Python utiliza o Selenium para automatizar a extração de dados meteorológicos do site ClimaTempo e os salva em um arquivo CSV.

## Instalação

1. Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/).

2. Clone este repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/seu-usuario/AutomacaoClimaTempo.git

3 - Acesse o diretório do projeto:
   
      cd seu-repositorio 
4 - Crie um ambiente virtual
    Crie um ambiente virtual usando o seguinte comando:

    ```bash
    python -m venv venv
    ```

    Este comando criará uma pasta chamada `venv` que conterá o ambiente virtual.
   

5 - Instale as dependências necessárias usando o pip:
      
      pip install -r requirements.txt
   
   Isso instalará as bibliotecas necessárias, incluindo o Selenium e o ChromeDriver.

6 - Desative o ambiente virtual quando não estiver mais trabalhando no projeto:

    ```bash
    deactivate
    ```


## Configuração
Nenhuma configuração adicional é necessária. O script já está configurado para utilizar o ChromeDriver automaticamente.

Execução
Execute o script usando o seguinte comando:
  python script_climatempo.py

O script abrirá o navegador Chrome, acessará o site ClimaTempo, coletará os dados meteorológicos e salvará as informações em um arquivo CSV chamado dados_climatempo.csv.

## Notas Importantes
Certifique-se de ter uma conexão estável com a internet durante a execução do script, pois ele acessa informações online.
O script usa o ChromeDriver para interagir com o navegador. Se encontrar problemas, verifique se a versão do ChromeDriver é compatível com a versão do Chrome instalada em seu sistema.

