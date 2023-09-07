import requests
import os

def bajar_usuario(url, card_mumber):
    response = requests.get(url)
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data = response.json() 
    else:
        print('Hubo un problema al cargar el archivo JSON')
    print(response.status_code)
    return data


def main():
    url = 'https://api.magicthegathering.io/v1/cards'
    bajar_usuario(url, 1)

# RUN

if __name__ == '__main__':
    main()