from bing_bot import EdgeSearch

try:
    EdgeSearch().resetProfile()
except Exception as erro:
    print(erro)
