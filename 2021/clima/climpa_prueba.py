import requests
import json 
import urllib.request

# https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-year&dataTypes=DP01,DP05,DP10,DSND,DSNW,DT00,DT32,DX32,DX70,DX90,SNOW,PRCP&stations=ASN00084027&startDate=1952-01-01&endDate=1970-12-31&includeAttributes=true&format=json

# Página de referencia: https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Paso 1. En una shell correr: pip install requests
# Paso 2. En cada archivo .py poner import requests
# Paso 3. En cada archivo .py poner import json
"""
response = requests.get("http://api.open-notify.org/astros.json")
print(response)

query = {'lat':'45', 'lon':'180'}
response = requests.get('http://api.open-notify.org/iss-pass.json', params=query)
print(response.json())

response = requests.get("https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-summary-of-the-year&dataTypes=DP01,DP05,DP10,DSND,DSNW,DT00,DT32,DX32,DX70,DX90,SNOW,PRCP&stations=ASN00084027&startDate=1952-01-01&endDate=1970-12-31&includeAttributes=true&format=json")
lista_req = response.json() # Una lista de diccionarios
print(lista_req[0].keys())



response = requests.get('http://api.openweathermap.org/data/2.5/find?q=London&units=metric&appid=ccf56232dbbc6c4dd5c94ea3a53d5776&lang=es')
print(response.json())
"""

infile = requests.get('https://www.tutiempo.net/registros/saco/' + '5-marzo-2015' + '.html', verify=False)
# print(infile.text)
jsonD = json.dumps(infile.text)
jsonL = json.loads(jsonD)
print(jsonL[:])

