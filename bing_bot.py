import pyautogui as auto
import time as tm
import random
from wonderwords import RandomWord                  # pyright: ignore[reportMissingImports]
from abc import ABC, abstractmethod

from selenium import webdriver                      # pyright: ignore[reportMissingImports]
from selenium.webdriver.common.by import By         # pyright: ignore[reportMissingImports]
from selenium.webdriver.edge.service import Service # pyright: ignore[reportMissingImports]
from selenium.webdriver.edge.options import Options # pyright: ignore[reportMissingImports]

from script_utils import Script
from scrapper import RewardsScraper
from exceptions import UndefinedBrowserError

class Search(ABC):
    """Classe abstrata de pesquisa, antes de se especificar qual navegador será usado.
    
    :param limit: Limite de pontos possíveis de se ganhar por dia pesquisando. Geralmente é 60.
    :type limit: int (opcional)"""

    def __init__(self, limit:int = 60):
        self.browser = None
        self._mp = limit
        self._pps = 3 # points per search

    def __writeRandSentence(self):
        search_str = RandomWord().word()
        auto.write(search_str)

    def __cooldown(self):
        tm.sleep(random.uniform(3.5, 4.5))
        auto.moveTo(1080/2 + random.randint(-160, 160), 1920/2 + random.randint(-80,80))
        auto.scroll(random.randint(-500, -200))
        tm.sleep(random.uniform(3.5, 4.5))

    def _searchLoop(self):
        self.__writeRandSentence()
        tm.sleep(0.1)
        auto.press("enter")
        self.__cooldown()
        auto.press("a")             # Could be any key
        tm.sleep(0.1)
        auto.keyDown('shift')
        auto.keyDown('home')
        tm.sleep(0.2)
        auto.press('backspace')
        tm.sleep(0.2)
        auto.keyUp('home')
        auto.keyUp('shift')

    def _searchSetup(self):
        """Faz as preparações necessárias para iniciar a pesquisa. Depende de qual navegador está sendo usado."""
        Script.openApp(self.browser, 1.5)
        auto.hotkey("win" + "up") # Maximiza a janela do navegador, depois de abrí-lo

    @abstractmethod
    def showBrowsers(self):
        """Mostra os navegadores disponíveis para o script."""
        pass

    @abstractmethod
    def scrapCurrentPts(self) -> int:
        """Faz Web Scrapping para obter a quantidade de pontos atuais. Necessário fazer login se for a primeira vez executando esse script."""
        pass

    def start(self, current_pts = None):
        """Realiza as pesquisas até alcançar o limite de pontos. Se for no Microsoft Edge, o parâmetro é opcional
        (deixá-lo em branco faz o programa realizar Web Scrapping para obter os pontos atuais).
        
        :param current_pts: Quantidade de pontos atuais.
        :type current_pts: int"""
        if current_pts is None and self.browser == "Microsoft Edge":
            try:
                current_pts = self.scrapCurrentPts()
            except Exception as erro:
                print(f"Erro: {erro}. Não foi possível determinar valor inicial: valor considerado será 0. ")  

        if current_pts == None or current_pts < 0:
            raise ValueError("Quantidade de pontos atual/inicial inválida.")

        if current_pts < self._mp:
            try:
                self._searchSetup()
            except UndefinedBrowserError as e:
                print(f"Erro ao abrir o navegador {self.browser}: {e}")

        while current_pts < self._mp + self._pps: #margem de erro: 1 pesquisa extra
            self._searchLoop()
            current_pts += self._pps

        auto.hotkey("alt", "f4")
        print(f"Quantidade limite de pontos alcançada: {self._mp} pontos.")
        return

# CLASSES ESPECÍFICAS PÚBLICAS PARA CADA NAVEGADOR

class DefaultSearch(Search):
    """Roda o script usando outros navegadores padrões, como Firefox, Opera GX, Chrome, etc
    
    :attention: Por enquanto, apenas o Firefox é suportado. Outros navegadores podem ser adicionados futuramente.
    :param limit: Limite de pontos possíveis de se ganhar por dia pesquisando. Geral"""

    def __init__(self, limit = 60):
        super().__init__(limit)
        self.__browsers_dict = {1:"Firefox"}

    # Override
    def showBrowsers(self):
        print("\nLista de navegadores disponíveis:\nID            Nome\n")
        for num, name in self.__browsers_dict.items():
            print(f"{num}             {name}")
        print()

    def setBrowser(self, id:int):
        if id not in self.__browsers_dict:
            print(f"Navegador com ID {id} não definido.")
            return
        
        self.browser = self.__browsers_dict[id]
        print("Navegador selecionado: " + self.browser)

    def selectedBrowser(self):
        print(f"Navegador selecionado: {self.browser}")

    # Override
    def _searchSetup(self):
        super()._searchSetup()
        auto.write("bing.com")
        auto.press("enter")
        tm.sleep(1)

    # Override
    def scrapCurrentPts(self) -> int:
        pass
    
class EdgeSearch(Search):
    """Necessário usar Windows. Instancia o script para rodar especificamente no navegador Microsoft Store, que é o mais próprio
    para os fins deste script.

    :param limit: Limite de pontos possíveis de se ganhar por dia pesquisando. Geralmente é 60.
    :type limit: int (opcional)"""
    def __init__(self, limit:int = 60):
        super().__init__(limit)
        self.browser = "Microsoft Edge"

    # Override
    def showBrowsers(self):
        print("Classe EdgeSearch permite apenas o navegador Microsoft Edge.")

    # Override
    def scrapCurrentPts(self) -> int:
        """Faz Web Scrapping para obter a quantidade de pontos atuais. Necessário fazer login se for a primeira vez executando esse script."""
        scrp = RewardsScraper()
        return scrp.getCurrentPts()

    def resetProfile(self):
        """Reseta (deleta) o perfil usado no Web Scrapping, apagando o diretório com as informações de usuário.
        Não interefere com o perfil usual de navegação do usuário."""
        profile = RewardsScraper()
        profile.deleteProfileDir()
