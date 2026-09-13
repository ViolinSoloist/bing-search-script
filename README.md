# Biblioteca de automação em Python

## Script de pesquisas automáticas no Bing para ganhar pontos
  
## Resumo
  Desenvolvido em Python. Este módulo que desenvolvi usa a biblioteca ```pyautogui``` como mecânica de automação principal e ```wonderwords``` para gerar palavras aleatórias e usá-las no termo de busca. Por enquanto, funciona apenas no _**Windows**_, nos navegadores _**Microsoft Edge**_ e _**Firefox**_ (Pode ser compatível com outros navegadores, mas o código foi testado apenas com os previamente citados).

  Especialmente no _**Microsoft Edge**_, é possível realizar Webscrapping para obter os pontos de pesquisa atuais, tirando a necessidade de conferi-los no site/aplicativo.

## Instruções

  É necessário ter Python instalado, bem como as bibliotecas necessárias: ```pyautogui```, ```wonderwords``` e ```selenium``` (caso use Webscrapping). [Veja aqui como instalar bibliotecas do Python](https://docs.python.org/pt-br/3/installing/index.html).
  
  Por padrão, o limite de pontos diários de pesquisa é de 60. Porém, caso deseje mudá-lo, faça-o ao chamar a classe. Ex.: ```EdgeSearch(90)```. Se não, apenas deixe o parâmetro (o espaço entre os parênteses) vazio.

### Microsoft Edge
  
  Apenas copie todos os arquivos Python para o diretório em que se deseja (não é necessário ser um diretório específico) e execute ```mainEdge.py```. Caso não deseje ou não seja possível executar _Webscrapping_ para determinar a quantidade de pontos de pesquisa atual, especifique-a nesse mesmo arquivo com um parâmetro inteiro da função ```start()```. Ex.: ```start(0)```.

### Firefox (e outros navegadores)
  Faça o mesmo passo o do tópico anterior, mas no lugar do arquivo ```mainEdge.py```, use ```mainDefault.py```. Como _Webscrapping_ ainda foi implementado para este caso, é mandatório a especificação da quantidade de pontos de pesquisa atual, conforme explicado anteriormente.
  
  Além disso, a escolha do navegador também é obrigatória, para que a funcionalidade principal (```start()```). O arquivo ```mainDefault.py``` já dá uma ideia de como fazer isso. Escolha o navegador através da funcionalidade ```setBrowser()``` com o ID do navegador de parâmetro. Para saber os IDs deles, execute a função ```showBrowsers()```, que listará todos os navegadores disponíveis e seus IDs correspondentes.

## Interface/documentação da biblioteca
  Em desenvolvimento.
