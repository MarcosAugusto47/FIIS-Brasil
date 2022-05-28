# libraries
import re 
import datetime
import pandas as pd

import urllib.request as urllib_request
from urllib.error import URLError, HTTPError

from utils.helpers import *
from utils.functions import *

# procedure
URL = 'https://fiis.com.br/lista-de-fundos-imobiliarios/'
soup = create_bsoup_object(URL)
tickers = get_tickers(soup)
dataset = create_fiis_dataframe(tickers)
COLUMNS_LIST = ['ultimo_rendimento',
                'valor_patrimonial_por_cota',
                'numero_cotas',
                'numero_cotistas',
                'cotacao',
                'min_52_weeks',
                'max_52_weeks']
dataset = convert_string_to_float(dataset, COLUMNS_LIST)
dataset = convert_percentages_to_float(dataset, ['dividend_yield', 'return_12_months'])
dataset = break_tipo_FII(dataset)
dataset['registro_CVM'] = dataset['registro_CVM'].apply(lambda x: str(convert_to_datetime(x)))
#dataset["p_vp"] = (dataset['cotacao'] / dataset['valor_patrimonial_por_cota']).replace(np.inf, np.nan)
dataset['date'] = str(datetime.date.today())
print(dataset.head())