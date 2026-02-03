# Agente de Análise de Dados

Esse é um agente que tem como objetivo ser um assistente de análise dos dados contidos em um arquivo `csv` sobre vendas.

O framework utilizado para esse projeto foi o LangGraph na linguagem Python. O modelo de linguagem usado é O Gemini 3, da Google. Para usar esse agente você precisa ter uma chave API da Google AI Studio, que você pode conseguir [aqui](https://aistudio.google.com/api-keys). Configure ela como variável no seu ambiente com o nome GOOGLE_API_KEY.

## Como ele funciona?

O arquivo CSV é lido em um DataFrame pandas. É dado ao agente a capacidade de criar e executar comandos em Python para fazer as pesquisas necessárias no DataFrame e responder às perguntas.

## Exemplos

Pergunta: Qual produto foi mais vendido?

Resposta gerada:

    O produto mais vendido foi o **Product_1359**, com um total de **95.112.506** unidades vendidas.

Pergunta: Qual local teve maior volume de vendas?

Resposta gerada:

    O local com o maior volume de vendas foi **Whse_J**, com um total de **617.421.620** unidades vendidas.

Pergunta: Qual foi o total de vendas no dia 21 de fevereiro de 2012?

Resposta gerada:

    O total de vendas (receita) no dia 21 de fevereiro de 2012 foi de **70.391.722**.
