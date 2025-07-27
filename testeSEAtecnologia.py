from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Constantes
URL_APLICACAO = "https://analista-teste.seatecnologia.com.br"
TEMPO_ESPERA_PADRAO = 10

class PaginaInicial:
    """
    Representa a página inicial da aplicação e suas interações.
    Encapsula seletores e métodos relacionados à página inicial.
    """
    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, TEMPO_ESPERA_PADRAO)
        self.nomes_arquivos_icones_esperados = [
            "building-22d5608a.svg",
            "edit-dfcb7eed.svg",
            "node-tree-924036ae.svg",
            "bell-181193f6.svg",
            "history-9102babe.svg",
            "person-bde031c5.svg"
        ]
        self.INDICADOR_CARREGAMENTO_PAGINA = (By.ID, "root")

    def navegar_para_pagina_inicial(self):
        """
        Navega para a URL da aplicação e espera um elemento chave carregar
        para confirmar que a página está pronta.
        """
        print(f"Acessando a página: {URL_APLICACAO}")
        self.driver.get(URL_APLICACAO)
        try:
            self.espera.until(EC.presence_of_element_located(self.INDICADOR_CARREGAMENTO_PAGINA))
            print("Página principal carregada com sucesso.")
        except TimeoutException:
            print(f"ERRO: A página {URL_APLICACAO} demorou muito para carregar ou o elemento "
                  f"{self.INDICADOR_CARREGAMENTO_PAGINA} não foi encontrado.")
            raise

    def clicar_icone_pelo_nome_arquivo(self, nome_arquivo):
        """
        Tenta localizar e clicar em um ícone SVG pelo seu nome de arquivo.
        Retorna True se o clique for bem-sucedido, False caso contrário.
        """
        seletor_css = f"img[src*='{nome_arquivo}']"
        print(f"  Tentando localizar e clicar: '{nome_arquivo}' usando seletor: '{seletor_css}'")
        try:
            elemento_icone = self.espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor_css)))
            elemento_icone.click()
            print(f"    SUCESSO: Clicado no ícone '{nome_arquivo}'. Full src: {elemento_icone.get_attribute('src')}")
            return True
        except (TimeoutException, NoSuchElementException):
            print(f"    FALHA: Não foi possível localizar ou clicar no ícone '{nome_arquivo}' no tempo esperado.")
            return False
        except Exception as e:
            print(f"    FALHA: Ocorreu um erro inesperado ao tentar interagir com '{nome_arquivo}'. Erro: {e}")
            raise

    def verificar_e_clicar_todos_os_icones(self):
        """
        Itera sobre a lista de ícones esperados e tenta clicar em cada um.
        """
        print("\n--- Iniciando verificação e cliques nos ícones SVG ---")
        todos_com_sucesso = True
        for nome_arquivo_icone in self.nomes_arquivos_icones_esperados:
            if not self.clicar_icone_pelo_nome_arquivo(nome_arquivo_icone):
                todos_com_sucesso = False
        print("\n--- Verificação e cliques nos ícones SVG concluídos. ---")
        return todos_com_sucesso



# --- Função Principal de Teste ---
def executar_teste_navegacao_icones():
    """
    Função principal que orquestra a execução do teste de navegação pelos ícones.
    Responsável por inicializar e finalizar o navegador.
    """
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        pagina_inicial = PaginaInicial(driver)
        pagina_inicial.navegar_para_pagina_inicial()

        pagina_inicial.verificar_e_clicar_todos_os_icones()

        print("\nTeste de navegação de ícones finalizado.")

    except Exception as e:
        print(f"OCORREU UM ERRO GERAL DURANTE A EXECUÇÃO DO TESTE: {e}")

    finally:
        if driver:
            print("Fechando o navegador.")
            driver.quit()

# --- Execução do Teste ---
if __name__ == "__main__":
    executar_teste_navegacao_icones()