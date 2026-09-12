import pyautogui as auto
import time
from exceptions import WinFocusError, UndefinedBrowserError

class PowerConfig:
    """Configurações de suspensão, desligamento automático, etc"""
    def __openSysToolsMenu(self):
        auto.hotkey('win', 'x')

    def powerOff(self):
        self.__openSysToolsMenu()
        auto.press('up', presses=2)
        auto.press('enter')
        auto.press('down', presses=2)
        auto.press('enter')

class Script:
    """Classe que implementa as funções mais gerais e úteis para projetos de automação usando pyautogui."""

    def openApp(nome:str, wait:float):
        """:param nome: do aplicativo a ser aberto.
        :param wait: Margem de segurança para esperar o aplicativo abrir."""
        if (nome == None):
            raise UndefinedBrowserError("Classe mãe usada ou navegador não foi definido.")

        auto.press("win")
        time.sleep(0.2)
        auto.write(nome)
        auto.press("enter")
        time.sleep(wait)

    def focusWin(nome:str) -> bool:
        """Foca/troca para um aplicativo/janela na tela.
        
        :param nome: do app ou janela que busca-se deixar na frente."""

        todas_janelas = auto.getAllWindows()
        janela_alvo = None

        # procura pela janela/aplicação alvo
        for janela in todas_janelas:
            if nome.lower() in janela.title.lower():
                janela_alvo = janela
                break
                
        if janela_alvo is not None:
            if janela_alvo.isMinimized:
                janela_alvo.restore()     

            janela_alvo.activate()
            time.sleep(0.3)
            return True
        
        raise WinFocusError("Janela não encontrada.")

if __name__ == "__main__":
    print("Hello, World!")
    Script.openApp("Microsoft Edge", 1.0)
