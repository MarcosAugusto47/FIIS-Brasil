from fastapi import FastAPI
import pandas as pd
import boto3

app = FastAPI()

dynamodb_resource = boto3.resource("dynamodb")

fiis = dynamodb_resource.Table("fiis").scan()
fiis = pd.DataFrame(fiis['Items'])
fiis = fiis[fiis.date==fiis.date.max()]
first_column = fiis.pop('ticker')
fiis.insert(0, 'ticker', first_column)
fiis = fiis.to_dict(orient='records')

ifix = dynamodb_resource.Table("ifix").scan()
ifix = pd.DataFrame(ifix['Items'])
ifix = ifix[ifix.date==ifix.date.max()]
first_column = ifix.pop('ticker')
ifix.insert(0, 'ticker', first_column)
ifix = ifix.to_dict(orient='records')

@app.get('/')
def home():
    return fiis

@app.get("/ticker/{fii}")
def get_ticker(fii:str):
    return list(filter(lambda d: d['ticker'] in [fii], fiis))

@app.get("/ifix")
def get_ifix():
    return ifix