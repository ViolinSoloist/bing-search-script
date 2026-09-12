from selenium import webdriver                                      # pyright: ignore[reportMissingImports]
from selenium.webdriver.common.by import By                         # pyright: ignore[reportMissingImports]
from selenium.webdriver.edge.options import Options                 # pyright: ignore[reportMissingImports]
from selenium.webdriver.support.ui import WebDriverWait             # pyright: ignore[reportMissingImports]
from selenium.webdriver.support import expected_conditions as EC    # pyright: ignore[reportMissingImports]
from selenium.common.exceptions import TimeoutException             # pyright: ignore[reportMissingImports]
import time as tm
import os
import shutil
from exceptions import ScrapError

class RewardsScraper:
    """
    Realiza Web Scrapping dinâmico para obter dados relativos ao Rewards.
    """
    def __init__(self):
        caminho_base = os.getenv('LOCALAPPDATA')
        caminho_final = os.path.join(caminho_base, "Microsoft", "Edge", "Bot Data")
        self.caminho_bot = f"user-data-dir={caminho_final}"
        self.win_path = f"{caminho_final}"
        # Guarda-se apenas o caminho do perfil. Outras configurações serão definidas go-to

    def __extrair_pontos(self, driver) -> int:
        """
        Função auxiliar da rotina de extrair pontos.
        """
        wait = WebDriverWait(driver, 10)
        icone_seta = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[class*='-rotate-90']")))
        
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));", icone_seta)
        
        tm.sleep(1)
        elementos_pontos = driver.find_elements(By.CSS_SELECTOR, "span.font-semibold")
        
        for elemento in elementos_pontos:
            texto_limpo = elemento.text.replace(".", "").replace(",", "").strip()
            
            if texto_limpo.isdigit():
                pontos = int(texto_limpo)
                if pontos > 0:
                    return pontos
                    
        raise ScrapError("Não foi encontrado valor válido para pontos atuais.")

    def getCurrentPts(self) -> int:
        """
        Inicia em segundo plano. Muda para janela ativa apenas se precisar de login (se for a primeira vez rodando o código ou se não há pasta do destino)
        """
        print("Verificação em segundo plano se a conta Microsoft está conectada...")
        
        # setup da verificação
        opcoes_invisivel = Options()
        opcoes_invisivel.add_argument(self.caminho_bot)
        opcoes_invisivel.add_argument("--headless") # segundo plano

        driver = None
        
        try:
            driver = webdriver.Edge(options=opcoes_invisivel)
            driver.get("https://rewards.bing.com/earn")
            
            wait_curto = WebDriverWait(driver, 5)
            
            try:
                # verifica em segundo plano se está logado
                wait_curto.until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[class*='-rotate-90']")))
                print("Conta logada, a extrair pontos...")
                
                pontos = self.__extrair_pontos(driver)
                print(f"Concluído: {pontos} pontos encontrados.")
                return pontos
                
            except TimeoutException:
                # quando não há login detectado, fecha-se o navegador em sgeundo plano para abrir um em primeiro para possibilitar login
                print("\n ! Login não detectado. Fechando guia em segundo plano.")
                
                driver.quit() 
                
                # novo navegador visível para login
                opcoes_visivel = Options()
                opcoes_visivel.add_argument(self.caminho_bot)

                print("Abrindo guia visível de login...")
                driver = webdriver.Edge(options=opcoes_visivel)
                driver.get("https://rewards.bing.com/earn")
                
                print("\n1. Vá até à janela do Microsoft Edge que se acabou de abrir.")
                print("2. Faça o seu login manualmente e aguarde a página carregar.")
                input("3. Pressione [ENTER] aqui no terminal assim que o login for concluído. <<<")
                
                print("\nRetomando extração de pontos...")
                driver.get("https://rewards.bing.com/earn")
                
                pontos = self.__extrair_pontos(driver)
                print(f"Concluído: {pontos} pontos encontrados.")
                return pontos

        except Exception as erro:
            print(f"Falha no Web Scrapping: {erro}")
            return 0
            
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except:
                    pass
    
    def deleteProfileDir(self):
        """Deleta todo conteúdo da pasta do usuário usado no Web Scrapping e a pasta em si.
        Útil para redefinir qual conta microsoft se deseja saber a quantidade de pontos diários de pesquisa atual (Necessário refazer login)."""

        if os.path.exists(self.win_path):
            try:
                shutil.rmtree(self.win_path)
                print("Perfil apagado.")
            except Exception as erro:
                print(f"Falha ao tentar apagar o perfil: {erro}")
        else:
            print("Diretório do perfil inexistente.")
