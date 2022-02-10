# Bibliotecas já instaladas no ambiente Python
import time
# Importar as funções que iremos utilizar do Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
import pandas as pd
import os
import sys

class Webscraper():
    def __init__(self):
        # Endereco do driver do browser de sua preferência
        if sys.platform.startswith('linux'):
         s = Service(os.path.abspath("chromedriver"))
        elif sys.platform == "win32":
         s = Service(os.path.abspath("chromedriver.exe"))
        # Para desabilitar a abertura de uma nova janela do browser pelo Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Configurando o Selenium
        self.browser = webdriver.Chrome(options=chrome_options,service=s)

        # Atribuir ao Selenium o site que será acessado 
        self.browser.get('https://tempo.inmet.gov.br/TabelaEstacoes/')

        # Recomendado para evitar ban do servidor
        time.sleep(3)


    def get_stations_info_selenium (self, ID, data_init, data_end):
        
        # Selecionar em "Produto" a opção "Tabela de Dados das Estações"
        self.browser.find_element(By.XPATH, "//select/option[@value='TabelaEstacoes']").click()

        # Selecionamos a opção de estação automática
        self.browser.find_element(By.XPATH,"//select/option[@value='T']").click()

        # Selecionamos qual estação estamos interessados
        self.browser.find_element(By.XPATH,"//select/option[@value='"+ID+"']").click()

        # Primeiro limpados o formulário e então preenchemos com a data inicial que desejamos.

        self.browser.find_element(By.ID,"datepicker_EstacoesTabela_Inicio").clear()
        self.browser.find_element(By.ID,"datepicker_EstacoesTabela_Inicio").send_keys(data_init)

        # O mesmo para a data final
        self.browser.find_element(By.ID,"datepicker_EstacoesTabela_Fim").clear()
        self.browser.find_element(By.ID,"datepicker_EstacoesTabela_Fim").send_keys(data_end)

        # Por fim, clicamos em "gerar tabela"
        self.browser.find_element(By.ID,"EstacoesTabela").click()


        # Pedimos para o Selenium aguardar por alguns segundos até que a tabela seja gerada pelo site
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tabela")))

        # atribuimos a estrutura atual do site para uma variável para que o BeautifulSoup possa fazer sua mágica!
        return  self.browser.page_source

    def get_estations_data_bs4(self, ID, data_init, data_end):
        # "Limpamos" a estrutura do site com o BeautifulSoup
        from bs4 import BeautifulSoup
        page_source = self.get_stations_info_selenium(ID, data_init, data_end)
        soup = BeautifulSoup(page_source,features="Lxml")

        # Pede para retornar a tabela existente na tag "table"

        return soup.find('table')

    def export(self, ID, data_init, data_end):

        # Converter a tabela html em Dataframe.
        # Definimos como separador decimal ',' e milhar '.'

        table = self.get_estations_data_bs4(ID, data_init, data_end)
        df = pd.read_html(str(table), decimal=',', thousands='.')[0]
        df = pd.DataFrame(df.to_records())

        # Se preferir, também há como renomear o cabeçalho da planilha.

        New_Names = ['Index', 'Date', 'Time', 'T', 'Tmax', 'Tmin', 'RH', 'RHmax', 'RHmin', 'PtOrvalhoinst',
                     'PtOrvalhomax', 'PtOrvalhmin',
                     'P', 'Pmax', 'Pmin', 'u2', 'Vdir', 'Vraj', 'Rn', 'PREC'
                     ]

        for n in range(0, len(df.keys())):
            df = df.rename(columns={df.keys()[n]: New_Names[n]})

        # Substituindo os valores NaN por 0 para funcionar no SQLITE:
        df = df.fillna(0)

        data = []
        # Inserindo o Dataframe pandas na tabela SQLite
        for row in df.itertuples():
            body = {
                "Date": row[2],
                "Time": row[3],
                "T": row[4],
                "Tmax": row[5],
                "Tmin": row[6],
                "RH": row[7],
                "RHmax": row[8],
                "RHmin": row[9],
                "PtOrvalhoinst": row[10],
                "PtOrvalhomax": row[11],
                "PtOrvalhomin": row[12],
                "P": row[13],
                "Pmax": row[14],
                "Pmin": row[15],
                "u2": row[16],
                "Vdir": row[17],
                "Vraj": row[18],
                "Rn": row[19],
                "PREC": row[10],
            }
            data.append(body)


        return data

    def media_dados(self,df):
        # Tirando a  média de colunas específicas e exibindo-as.
        mean_df = df[["Tmax", "Tmin", "RHmax", "RHmin", "Pmax", "Pmin", "u2", "Rn", "PREC"]].mean()
        print(mean_df)
        return mean_df

    def status_estacao(self, ID):
        # Atribuindo ao Selenium o site que será acessado
        self.browser.get('https://portal.inmet.gov.br/paginas/catalogoaut')

        # Recomendado para evitar ban do servidor
        wait_time_out = 15
        wait_variable = W(self.browser, wait_time_out)
        # Garantindo o click no elemento desejado
        wait_variable.until(E.element_to_be_clickable((By.LINK_TEXT, "Download CSV"))).click()
        self.browser.back()
        # wait_variable.until(E.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Download CSV")))

        # Puxado a tabela do diretório e adicionando-a  a um Dataframe pandas (*sujeito a mudanças*)
        df = pd.read_csv(r"C:/Users/peric/Downloads/CatalogoEstaçõesAutomáticas.csv", delimiter=';')

        # print(df)

        # Armazenando em variáveis as informações desejadas da tabela
        row = df.loc[df['CD_ESTACAO'] == ID]
        estation_name = row['DC_NOME'].values[0]
        estation_state = row['SG_ESTADO'].values[0]
        estation_situation = row['CD_SITUACAO'].values[0]
        estation_lat = row['VL_LATITUDE'].values[0]
        estation_long = row['VL_LONGITUDE'].values[0]
        estation_alt = row['VL_ALTITUDE'].values[0]

        print("A estação de ID {} se encontra em {},{}, está em status {}, localizada em {}, {}, {}.".format(ID, estation_name, estation_state, estation_situation, estation_lat, estation_long, estation_alt))


# webscraper = Webscraper()
# ID = str(input("Insira a TAG da estação: "))
# data_init = str(input("Insira a data inicial [DD/MM/AAAA]: "))
# data_end = str(input("Insira a data final [DD/MM/AAAA]: "))
# # data_avg = str(input("Deseja tirar a média dos dados? [S/N]: "))

# # df = webscraper.storage(ID, data_init, data_end)
# # webscraper.media_dados(df)

# print(webscraper.storage(ID, data_init, data_end))
# print("Exibindo dados da estação {} referentes as datas de {} a {}".format(ID, data_init, data_end))

# webscraper.status_estacao(ID)
