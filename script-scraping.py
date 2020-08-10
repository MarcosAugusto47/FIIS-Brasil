# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import re 

import bs4
import urllib.request as urllib_request
import pandas as pd
print("BeautifulSoup ->", bs4.__version__)
print("urllib ->", urllib_request.__version__)
print("pandas ->", pd.__version__)

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def trata_html(input):
    return " ".join(input.split()).replace('> <', '><')

## Rotina de scraping
### Declara-se a variável cards
cards = []

###
url = 'https://fiis.com.br/lista-de-fundos-imobiliarios/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
req = Request(url, headers = headers)
response = urlopen(req)
html = response.read()
html = html.decode('utf-8')
html = trata_html(html)

## Criação de um objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
tickets = soup.findAll('span', {'class': 'ticker'})
codigos = []
for ticket in tickets:
    codigos.append(ticket.get_text().lower())
        
for codigo in codigos:
    url = 'https://fiis.com.br/' + codigo
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    req = Request(url, headers = headers)
    response = urlopen(req)
    html = response.read()
    html = html.decode('utf-8')
    html = trata_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('span', {'class': 'value'})
    infos = []
    card = {}
    for item in items:
        infos.append(item.get_text())
    card['Dividend Yield'] = infos[0]
    card['Ultimo Rendimento'] = infos[1]
    card['Patrimonio Liquido'] = infos[2]
    card['Valor Patrimonial por Cota'] = infos[3]
    card['Site'] = infos[6]
    card['Codigo'] = infos[7]
    card['Tipo do FII'] = infos[8]
    card['Registro CVM'] = infos[10]
    card['Numero de Cotas'] = infos[11]
    card['Numero de Cotistas'] = infos[12]
    card['Ticker'] = codigo.upper()
    
    admin = soup.findAll("div", {"class": "text-wrapper"})
    card['Administrador'] = re.sub("ADMINISTRADOR|[0-9].*[0-9]", "", admin[0].get_text())
    
    cotacao = soup.findAll("div", {"class": "item quotation"})
    cotacao = cotacao[0].find("span", {"class": "value"}).get_text()
    
    min52 = soup.findAll("div", {"class": "item min52"})
    min52 = min52[0].find("div", {"class": "value"}).get_text()

    max52 = soup.findAll("div", {"class": "item max52"})
    max52 = max52[0].find("div", {"class": "value"}).get_text()

    valorizacao12 = soup.findAll("div", {"class": "item val12"})
    valorizacao12 = valorizacao12[0].find("div", {"class": "value"}).get_text()
    
    card["Cotacao Atual"] = cotacao
    card["Min. 52 semanas"] = min52
    card["Max. 52 semanas"] = max52
    card["Valorizacao"] = valorizacao12
    
    cards.append(card)

## Cria-se um dataframe com os resultados
dataset = pd.DataFrame(cards)
dataset = dataset.apply(lambda x: x.str.replace("R\\$|\\.","", regex = True).str.replace(",", ".").astype(float) if x.name in ["Ultimo Rendimento", "Valor Patrimonial por Cota", "Numero de Cotas", "Numero de Cotistas", "Cotacao Atual","Min. 52 semanas", "Max. 52 semanas"] else x)
dataset["P/VP"] = dataset['Cotacao Atual'] / dataset['Valor Patrimonial por Cota']
dataset.to_csv('C:/Users/marco/Desktop/Estatistica/Cursos/Alura/Scraping com Python - Coleta de dados na web/Projeto - R jobs/fiis_dataset.csv',
               sep = ';',
               index = False)