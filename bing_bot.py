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

    @abstractmethod
    def searchSetup(self):
        """Faz as preparações necessárias para iniciar a pesquisa. Depende de qual navegador está sendo usado."""
        pass

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

    def scrapCurrentPts(self) -> int:
        scrp = RewardsScraper()
        return scrp.getCurrentPts()

    def start(self, current_pts:int = None):
        """Realiza as pesquisas até alcançar o limite de pontos.
        
        :param current_pts: Quantidade de pontos atuais. Se não especificado, usa Web Scrapping para obter automaticamente.
        :type current_pts: int (opcional)"""

        if current_pts is None:
            current_pts = self.scrapCurrentPts()

        if current_pts < 0:
            raise ValueError("Quantidade de pontos atual/inicial inválida.")

        if current_pts < self.mp:
            self.searchSetup()

        while current_pts < self.mp:
            self.__searchLoop()
            current_pts += self.pps

        print(f"Quantidade limite de pontos alcançada: {self.mp} pontos.")
        return

class EdgeSearch(Search):
    def __init__(self, limit:int = 60):
        super().__init__(limit)

    def searchSetup(self):
        Script.openApp("Microsoft Edge", 0.3)
        auto.hotkey("win" + "up")
