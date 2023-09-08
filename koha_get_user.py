import requests
import os

# Documentación de la API de Koha: https://api.koha-community.org/

def datos_usuario(dominio, card_number):
    usuario = 'soporte'
    passwd = 'Shei5oom'
    url = dominio + '/api/v1/patrons'
    response = requests.get(url, auth=(usuario, passwd), params= {"cardnumber": card_number})
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "Palacios"})
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data = response.json()
        return data
    else:
        print('Hubo un problema al cargar el archivo JSON')
    print(response.status_code)

def prestamos_usuario(dominio, card_number):
    # pre : dominio es la url  admin del koha de la biblioteca
    #       card_number es el número de socio (el DNI)
    # post: devuelve una 2-ulpa
    #       coordenada 0: lista de diccionarios con los items préstamos
    #       coordenada 1: True si el socio tiene restricciones (suspendido), False en caso contrario
    usuario = 'soporte'
    passwd = 'Shei5oom'
    socio =  datos_usuario(dominio, card_number)
    if len(socio) == 0:
        print('No se encontró el socio')
        return None
    else:
        patron_id = socio[0]['patron_id']
        url = dominio + '/api/v1/checkouts'
        response = requests.get(url, auth=(usuario, passwd),  params= {'patron_id': patron_id})
        if response.status_code == 200:
            # El archivo JSON fue encontrado y cargado correctamente
            data = response.json()
            return (data, socio[0]['restricted'])
        else:
            print('Hubo un problema al cargar el archivo JSON')
        print(response.status_code)

def listar_bibliotecas(dominio):
    usuario = 'soporte'
    passwd = 'Shei5oom'
    url = dominio + '/api/v1/libraries'
    response = requests.get(url, auth=(usuario, passwd))
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data = response.json()
        return data
    else:
        print('Hubo un problema al cargar el archivo JSON')
    print(response.status_code)

def datos_item(dominio, item_id):
    usuario = 'soporte'
    passwd = 'Shei5oom'
    url_item = dominio + '/api/v1/items/' + str(item_id)
    response = requests.get(url_item, auth=(usuario, passwd))
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "Palacios"})
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data_item = response.json()
        biblio_id = data_item['biblio_id']
        url_biblio = dominio + '/api/v1/biblios/' + str(biblio_id)
        response = requests.get(url_biblio, auth=(usuario, passwd), headers={"Content-Type": "application/marc-in-json"})
        data_biblio = response.json()
        return (data_biblio, data_item) # no trae los dados bibliogràfico (la primera coordenada no sirve)
    else:
        print('Hubo un problema al cargar el archivo JSON')
    print(response.status_code)
    

def main():
    dominio = 'https://faud.biblioadmin.unc.edu.ar'
    # usuario = bajar_usuario(url, 1)
    # bibliotecas = listar_bibliotecas(dominio)
    # for bib in bibliotecas:
    #     print(bib['library_id'],':', bib['name'])

    socio =  datos_usuario(dominio, '21062181')[0]
    # for campo  in socio:
    #     print(campo, ':', socio[campo])
    socio =  datos_usuario(dominio, '13821438')[0]
    # for campo  in socio:
    #     print(campo, ':', socio[campo])
    # print('patron_id', socio['patron_id'])
    # print('cardnumber', socio['cardnumber'])
    estatus = prestamos_usuario(dominio, socio['cardnumber'])
    for pres in estatus[0]:
        print('Item : \n',pres)
    print('Suspendido :',estatus[1])

    print('aaaa',datos_item(dominio, 83627))


    usuario = 'soporte'
    passwd = 'Shei5oom'
    response = requests.get('https://faud.biblioadmin.unc.edu.ar/api/v1/biblios/1459', auth=(usuario, passwd))
    data = response.json()
    print('bbb', data)

    





# RUN
if __name__ == '__main__':
    main()