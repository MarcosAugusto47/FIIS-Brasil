from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def trata_html(input):
   return " ".join(input.split()).replace('> <', '><')

def create_bsoup_object(url):
    headers = {'User-Agent': 'xxxx'}
    req = Request(url, headers = headers)
    response = urlopen(req)
    html = response.read()
    html = html.decode('utf-8')
    html = trata_html(html)
    ## create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_tickers(soup):
    tickets = soup.findAll('span', {'class': 'ticker'})
    codigos = []
    
    for ticket in tickets:
        codigos.append(ticket.get_text().lower())
    
    return codigos