import csv
from datetime import datetime
import logging
import ssl
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ssl._create_default_https_context = ssl._create_unverified_context

def salvar_dados_csv(regiao_temp, temp, sensacao_ter, condicao_ter, ventos, umidade):
    dados = {
        "Região": regiao_temp,
        "Temperatura Atual": temp,
        "Sensação Térmica": sensacao_ter,
        "Condição Térmica": condicao_ter,
        "Ventos": ventos,
        "Umidade": umidade
    }

    csv_path = 'dados_climatempo.csv'

    # Verifica se o arquivo já existe
    arquivo_existe = True
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as arquivo_csv:
            reader = csv.reader(arquivo_csv)
            if not list(reader):
                arquivo_existe = False
    except FileNotFoundError:
        arquivo_existe = False

    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        campos = ["Região", "Temperatura Atual", "Sensação Térmica", "Condição Térmica", "Ventos", "Umidade"]

        writer = csv.DictWriter(csvfile, fieldnames=campos)

        # Se o arquivo não existir, escreve o cabeçalho
        if not arquivo_existe:
            campos.append("Data da Coleta")
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()

        # Adiciona a data da coleta ao dicionário
        dados["Data da Coleta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Escreve os dados no arquivo
        writer.writerow(dados)

def configurar_saida_utf8():
    sys.stdout.reconfigure(encoding='utf-8')

def aguardar_elemento_presente(driver, by, value, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except Exception as e:
        logging.error(f"Erro ao aguardar a presença do elemento {by}: {value}. Detalhes: {str(e)}")
        # Se o elemento não for encontrado, recarrega a página
        driver.refresh()

def coletar_dados_climatempo():
    # Configuração de logs
    logging.basicConfig(filename='coletar_dados.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')

    try:
        # Configura o serviço do ChromeDriver com o tempo limite explicitamente definido
        chrome_service = ChromeService(executable_path=ChromeDriverManager().install(), chrome_connect_timeout=10)

        # Inicializa o driver do Selenium usando o serviço configurado
        with webdriver.Chrome(service=chrome_service) as driver:
            # URL para acessar
            url = 'https://www.climatempo.com.br/'

            # Abre a URL no navegador
            driver.get(url)

            # Maximiza a tela
            driver.maximize_window()

            # Aguarda até que o conteúdo seja carregado
            driver.implicitly_wait(10)

            # Aguarda 5s
            time.sleep(5)

            try:
                # Aguarda a presença do botão de fechar o pop-up
                aguardar_elemento_presente(driver, By.XPATH, '/html/body/div[6]/div/div[2]')
                close_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/button')
                close_button.click()

            except Exception as e:
                logging.error("Pop-up não encontrado ou não pôde ser fechado: %s", e)
                # Se o elemento não for encontrado, recarrega a página
                driver.refresh()

            # Aguarda a presença do elemento que contém as informações sobre a temperatura
            aguardar_elemento_presente(driver, By.XPATH, '//*[@id="current-weather-city"]')

            # Inicializa variáveis
            regiao_temp = temp = sensacao_ter = condicao_ter = ventos = umidade = None

            # Loop até que todas as variáveis sejam preenchidas
            while not all([regiao_temp, temp, sensacao_ter, condicao_ter, ventos, umidade]):
                try:
                    # Captura dados sobre a temperatura
                    regiao_temp = driver.find_element(By.XPATH, '//*[@id="current-weather-city"]').text
                    temp = driver.find_element(By.XPATH, '//*[@id="current-weather-temperature"]').text
                    sensacao_ter = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[4]/div[2]/div[1]/div/div[2]/div[2]/span').text
                    condicao_ter = driver.find_element(By.XPATH, '//*[@id="current-weather-condition"]').text
                    ventos = driver.find_element(By.XPATH, '//*[@id="current-weather-wind"]').text
                    umidade = driver.find_element(By.XPATH, '//*[@id="current-weather-humidity"]').text

                except Exception as e:
                    logging.error(f"Erro ao capturar dados: {str(e)}")
                    # Se houver erro, recarrega a página
                    driver.refresh()

            configurar_saida_utf8()  # Configura a saída para UTF-8

            print("Dados Meteorológicos:")
            print(f"Região: {regiao_temp}")
            print(f"Temperatura Atual: {temp}")
            print(f"Sensação Térmica: {sensacao_ter}")
            print(f"Ventos: {ventos}")
            print(f"Umidade: {umidade}")

            # Salva os dados em um arquivo CSV com codificação UTF-8
            salvar_dados_csv(regiao_temp, temp, sensacao_ter, condicao_ter, ventos, umidade)

    except Exception as e:
        logging.error(f"Ocorreu um erro: {str(e)}")
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    coletar_dados_climatempo()
