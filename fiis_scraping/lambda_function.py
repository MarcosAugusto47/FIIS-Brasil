# libraries
import json
import boto3
import datetime

import urllib.request as urllib_request
from urllib.error import URLError, HTTPError

from utils.helpers import *
from utils.functions import *

def lambda_handler(event, context):
    
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
    dataset['date'] = str(datetime.date.today() - datetime.timedelta(days=1))
    
    ticker_data_dict = dataset.to_dict(orient='records')
    dynamodb_resource = boto3.resource("dynamodb")
    batch_write(dynamodb_resource, "fiis", ticker_data_dict, ['ticker', 'date'])
    
    URL = 'https://fiis.com.br/ifix/'
    df_ifix = create_ifix_dataframe(URL)
    COLUMNS_LIST = ['peso']
    df_ifix = convert_percentages_to_float(df_ifix, COLUMNS_LIST)
    df_ifix['date'] = str(datetime.date.today())
    
    ifix_data_dict = df_ifix.to_dict(orient='records')
    batch_write(dynamodb_resource, "ifix", ifix_data_dict, ['ticker', 'date'])

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps("FII's data scraped!")
    }