from selenium import webdriver                                      # pyright: ignore[reportMissingImports]
from selenium.webdriver.common.by import By                         # pyright: ignore[reportMissingImports]
from selenium.webdriver.edge.service import Service                 # pyright: ignore[reportMissingImports]
from selenium.webdriver.edge.options import Options                 # pyright: ignore[reportMissingImports]
from selenium.webdriver.support.ui import WebDriverWait             # pyright: ignore[reportMissingImports]
from selenium.webdriver.support import expected_conditions as EC    # pyright: ignore[reportMissingImports]
import time as tm

class RewardsScraper:
    """
    Realiza Web Scrapping para obter dados relativos ao Rewards.
    """
    def __init__(self):
        self.options = Options()
        caminho_bot = r"user-data-dir=C:\Users\rodri\AppData\Local\Microsoft\Edge\Bot Data"
        self.options.add_argument(caminho_bot)

    def getCurrentPts(self) -> int:
        """
        Acede à página do Rewards e extrai a pontuação atual.
        
        :return: Quantidade de pontos (de pesquisa diária) que o usuário já tem.
        :rtype: int
        """
        print("Iniciando Web Scrapping para obter pontos...")
        
        # Inicializamos a variável driver como None por segurança
        driver = None 
        
        try:    
            driver = webdriver.Edge(options=self.options)
            driver.get("https://rewards.bing.com/earn")
            
            print("Acessando site em segundo plano...")
            wait = WebDriverWait(driver, 10)
            
            print("Esperando Detalhamento de produtos...")
            icone_seta = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[class*='-rotate-90']")))
            
            driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", icone_seta)
            print("Abrindo Detalhamento de produtos...")

            tm.sleep(1)

            elementos_pontos = driver.find_elements(By.CSS_SELECTOR, "span.font-semibold")
            
            for elemento in elementos_pontos:
                texto_sujo = elemento.text
                texto_limpo = texto_sujo.replace(".", "").replace(",", "").strip()
                
                if texto_limpo.isdigit():
                    pontos = int(texto_limpo)

                    if pontos > 0:
                        print(f"Concluído: {pontos} pontos encontrados.")
                        return pontos
            
        except Exception as erro:
            print(f"[ERRO] Durante o web scraping: {erro}")
            return 0
            
        finally:
            # O 'if driver:' garante que só tentamos fechar o navegador se ele chegou a abrir
            if driver is not None:
                driver.quit()
                pass