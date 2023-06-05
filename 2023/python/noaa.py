import requests
token = 'LsJXpYprYMzOKjMtqAlDmMUzwGelIQDf'
my_headers = {'token' : token}
# Ejemplo: datasets disponibles en NOAA
response = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets', headers=my_headers)
respuesta = response.json()

resultados = respuesta['results'] # Datasets disponibles

for w in resultados:
    pass
    print(w['id'],':',w['name'])
