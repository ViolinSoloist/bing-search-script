from bing_bot import DefaultSearch

ds = DefaultSearch()
ds.showBrowsers()       # Mostra os navegadores disponíveis
ds.setBrowser(1)        # Seleciona o Firefox
ds.start(0)             # (É necessário especificar a quantidade de pontos aqui)