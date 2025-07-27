from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time
import os

# Constantes
URL_APLICACAO = "https://analista-teste.seatecnologia.com.br"
TEMPO_ESPERA_PADRAO = 15

MODO_TESTE_VISUAL = os.getenv('MODO_TESTE_VISUAL', 'true').lower() == 'true'
INTERVALO_ENTRE_CLIQUES_VISUAL = 2.0 if MODO_TESTE_VISUAL else 0
ATRASO_FINAL_VISUAL = 3.0 if MODO_TESTE_VISUAL else 0

class PaginaComInterruptor:
    """
    Representa a página que contém o interruptor (switch) e suas interações.
    """
    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, TEMPO_ESPERA_PADRAO)
        self.LOCALIZADOR_INTERRUPTOR = (By.CLASS_NAME, "ant-switch-inner")
        self.INDICADOR_CARREGAMENTO_PAGINA = (By.ID, "root")

    def navegar_para_pagina(self):
        """
        Navega para a URL da aplicação e espera a página carregar.
        """
        print(f"Acessando a página: {URL_APLICACAO}")
        self.driver.get(URL_APLICACAO)
        try:
            self.espera.until(EC.presence_of_element_located(self.INDICADOR_CARREGAMENTO_PAGINA))
            print("Página carregada com sucesso.")
            if MODO_TESTE_VISUAL:
                time.sleep(ATRASO_FINAL_VISUAL)
        except TimeoutException:
            print(f"ERRO: A página {URL_APLICACAO} demorou muito para carregar ou o elemento "
                  f"{self.INDICADOR_CARREGAMENTO_PAGINA} não foi encontrado.")
            raise

    def obter_elemento_interruptor(self):
        """
        Tenta localizar o elemento do interruptor e retorna-o.
        """
        print(f"Tentando localizar o interruptor com seletor: {self.LOCALIZADOR_INTERRUPTOR}")
        try:
            elemento = self.espera.until(EC.element_to_be_clickable(self.LOCALIZADOR_INTERRUPTOR))
            print("Elemento interruptor localizado com sucesso.")
            return elemento
        except (TimeoutException, NoSuchElementException) as e:
            print(f"FALHA: Não foi possível localizar ou o elemento interruptor no tempo esperado. Erro: {e}")
            raise

    def clicar_interruptor(self, elemento_interruptor):
        """
        Realiza um clique no elemento interruptor.
        """
        try:
            elemento_interruptor.click()
            print("SUCESSO: Clique realizado no interruptor.")

            if MODO_TESTE_VISUAL:
                time.sleep(INTERVALO_ENTRE_CLIQUES_VISUAL) # Atraso condicional para visualização
            return True
        except ElementNotInteractableException:
            print("FALHA: O elemento interruptor não está interagível (pode estar desabilitado ou oculto).")
            return False
        except Exception as e:
            print(f"FALHA: Ocorreu um erro inesperado ao clicar no interruptor. Erro: {e}")
            raise


def executar_teste_clicks_no_interruptor():
    """
    Função principal que orquestra o teste de múltiplos cliques em um interruptor.
    """
    driver = None
    NUMERO_DE_CLIQUES = 4

    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        pagina_interruptor = PaginaComInterruptor(driver)
        pagina_interruptor.navegar_para_pagina()

        print(f"\n--- Iniciando teste de {NUMERO_DE_CLIQUES} cliques no interruptor ---")

        elemento_interruptor = pagina_interruptor.obter_elemento_interruptor()

        for i in range(1, NUMERO_DE_CLIQUES + 1):
            print(f"Tentando clique número {i}...")
            if not pagina_interruptor.clicar_interruptor(elemento_interruptor):
                print(f"Teste interrompido após falha no clique {i}.")
                break
        else:
            print(f"\n--- Teste de {NUMERO_DE_CLIQUES} cliques no interruptor concluído com sucesso. ---")


    except Exception as e:
        print(f"OCORREU UM ERRO GERAL DURANTE A EXECUÇÃO DO TESTE: {e}")

    finally:
        if driver:
            print("Fechando o navegador.")
            driver.quit()
            if MODO_TESTE_VISUAL:
                time.sleep(ATRASO_FINAL_VISUAL)

# Execução
if __name__ == "__main__":
    executar_teste_clicks_no_interruptor()