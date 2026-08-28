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

class Search(ABC):
    """Classe abstrata de pesquisa, antes de se especificar qual navegador será usado.
    
    :param limit: Limite de pontos possíveis de se ganhar por dia pesquisando. Geralmente é 60.
    :type limit: int (opcional)"""
    def __init__(self, limit:int = 60):
        self.mp = limit
        self.pps = 3 # points per search


    def __writeRandSentence(self):
        search_str = RandomWord().word()
        auto.write(search_str)

    def __cooldown(self):
        tm.sleep(random.uniform(3, 4))
        auto.moveTo(1080/2 + random.randint(-160, 160), 1920/2 + random.randint(-80,80))
        auto.scroll(random.randint(-500, -200))
        tm.sleep(random.uniform(3, 4))

    def __searchLoop(self):
        self.__writeRandSentence()
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

    @abstractmethod
    def searchSetup(self):
        """Faz as preparações necessárias para iniciar a pesquisa. Depende de qual navegador está sendo usado."""
        pass

    @abstractmethod
    def start(self, current_pts:int = None):
        """Realiza as pesquisas até alcançar o limite de pontos. Se for no Microsoft Edge, o parâmetro é opcional
        (deixá-lo em branco faz o programa realizar Web Scrapping para obter os pontos atuais).
        
        :param current_pts: Quantidade de pontos atuais.
        :type current_pts: int"""
        pass

class EdgeSearch(Search):
    """Necessário usar Windows. Instancia o script para rodar especificamente no navegador Microsoft Store, que é o mais próprio
    para os fins deste script.

    :param limit: Limite de pontos possíveis de se ganhar por dia pesquisando. Geralmente é 60.
    :type limit: int (opcional)"""
    def __init__(self, limit:int = 60):
        super().__init__(limit)

    # Override
    def searchSetup(self):
        Script.openApp("Microsoft Edge", 0.3)
        auto.hotkey("win" + "up")

    def scrapCurrentPts(self) -> int:
        """Faz Web Scrapping para obter a quantidade de pontos atuais. Necessário fazer login se for a primeira vez executando esse script."""
        scrp = RewardsScraper()
        return scrp.getCurrentPts()

    def resetProfile(self):
        """Reseta (deleta) o perfil usado no Web Scrapping, apagando o diretório com as informações de usuário.
        Não interefere com o perfil usual de navegação do usuário."""
        profile = RewardsScraper()
        profile.deleteProfileDir()

    # Override
    def start(self, current_pts = None):
        """Realiza as pesquisas usando Microsoft Edge até alcançar o limite de pontos. Se não especificado, usa Web Scrapping para obter automaticamente.
        Deve estar logado na conta microsoft em que se deseja ganhar pontos."""
        if current_pts is None:
            try:
                current_pts = self.scrapCurrentPts()
            except Exception as erro:
                print(f"Erro: {erro}. Não foi possível determinar valor inicial: valor considerado será 0. ")  

        if current_pts < 0:
            raise ValueError("Quantidade de pontos atual/inicial inválida.")

        if current_pts < self.mp:
            self.searchSetup()

        while current_pts < self.mp + self.pps: #margem de erro: 1 pesquisa extra
            self.__searchLoop()
            current_pts += self.pps

        print(f"Quantidade limite de pontos alcançada: {self.mp} pontos.")
        return
