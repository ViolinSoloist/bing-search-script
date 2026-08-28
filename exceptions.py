# Flags
class InfiniteLoopFlag(Exception):
    """Loop em script excede o limite estipulado."""
    pass

class FullLoopFlag(Exception):
    """Quando detecta-se uma interação completa e com sucesso."""
    pass

# Erros
class ScriptMissError(Exception):
    """Quando acontece algo fora do esperado, que pode causar comportamentos indefinidos no script."""
    pass

class ImgNotCopiedError(Exception):
    """Quando ocorre uma tentativa falha de copiar uma imagem."""
    pass

class WinFocusError(Exception):
    """Falha em focar/mudar para algum app/janela."""

class ScrapError(Exception):
    """Quando não se obtém o valor esperado ao fazer Web Scrapping."""