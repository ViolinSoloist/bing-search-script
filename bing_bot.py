import pyautogui as auto
import time as tm
import random
from wonderwords import RandomWord  # pyright: ignore[reportMissingImports]
from abc import ABC, abstractmethod

from script_utils import Script

class Search(ABC):
    def __init__(self, limit:int = 60):
        self.mp = limit
        self.pps = 3 # points per search

    @abstractmethod
    def searchSetup(self):
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


    def start(self, current_pts:int):
        if current_pts < 0 or current_pts % self.pps != 0:
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


