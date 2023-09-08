import requests
import os

# Documentación de la API de Koha: https://api.koha-community.org/

def datos_usuario(dominio, card_number):
    # pre : dominio es la url  admin del koha de la biblioteca
    #       card_number es el número de socio (el DNI)
    # post: devuelve una lista de diccionarios con los datos del socio
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
    #       coordenada 0: True si el socio tiene restricciones (suspendido), False en caso contrario
    #       coordenada 1: lista de diccionarios con los items préstamos
    
    usuario = 'soporte'
    passwd = 'Shei5oom'
    socio =  datos_usuario(dominio, card_number)
    if len(socio) == 0:
        # print('No se encontró el socio')
        return None
    else:
        patron_id = socio[0]['patron_id']
        url = dominio + '/api/v1/checkouts'
        response = requests.get(url, auth=(usuario, passwd),  params= {'patron_id': patron_id})
        if response.status_code == 200:
            # El archivo JSON fue encontrado y cargado correctamente
            data = response.json()
            return (socio[0]['restricted'], data)
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
    # pre: url administrativa del sistema de gestión de la biblioteca
    #      item_id es el id del item
    # post: los datos del item
    usuario = 'soporte'
    passwd = 'Shei5oom'
    url_item = dominio + '/api/v1/items/' + str(item_id)
    response = requests.get(url_item, auth=(usuario, passwd))
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "Palacios"})
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data_item = response.json()
        return data_item 
    else:
        print('Hubo un problema al cargar el archivo JSON')
    print(response.status_code)

def verificar_socio(dominios, card_number):
    # pre: dominios es una lista de dominios administrativos del sistema de gestión de bibliotecas
    #      card_number es el número de socio (el DNI)
    # post: devuelve una lista de longitud len(dominios) donde  coordenada i tenemos
    #       (card_number, dominios[i], "¿es socio?", "¿está suspendido?", "¿tiene préstamos?", lista item_id de prestamos que tiene el socio)
    devuelve = []
    for dominio in dominios:
        es_socio, suspendido, tiene_prestamos, prestamos = False, False, False, []
        socio =  datos_usuario(dominio, card_number)
        # print(dominio, card_number, socio)
        if len(socio) > 0:
            es_socio = True
            suspendido, prsts = prestamos_usuario(dominio, card_number)
            if len(prsts) > 0:
                tiene_prestamos = True
                for pr in prsts:
                    prestamos.append(pr['item_id'])
        devuelve.append((card_number, dominio, es_socio, suspendido, tiene_prestamos, prestamos))
    return devuelve
    
    

def main():
    dominios = ['https://faud.biblioadmin.unc.edu.ar', 'https://eco.biblioadmin.unc.edu.ar', 'https://ffyh.biblioadmin.unc.edu.ar', 'https://agro.biblioadmin.unc.edu.ar', 'https://famaf.biblioadmin.unc.edu.ar']
    # usuario = bajar_usuario(url, 1)
    # bibliotecas = listar_bibliotecas(dominio)
    # for bib in bibliotecas:
    #     print(bib['library_id'],':', bib['name'])

    socio =  datos_usuario(dominios[0], '21062181')
    # print(socio)
    socio =  datos_usuario(dominios[1], '38111171')
    print(len(socio))
    # for campo  in socio:
    #     print(campo, ':', socio[campo])
    socio =  datos_usuario(dominios[0], '13821438')[0]
    # for campo  in socio:
    #     print(campo, ':', socio[campo])
    # print('patron_id', socio['patron_id'])
    # print('cardnumber', socio['cardnumber'])
    estatus = prestamos_usuario(dominios[0], socio['cardnumber'])
    # for pres in estatus[1]:
    #     print('Item : \n',pres)
    # print('Suspendido :',estatus[0])

    # print('aaaa',datos_item(dominio, 83627)) 


    # usuario = 'soporte'
    # passwd = 'Shei5oom'
    # response = requests.get('https://faud.biblioadmin.unc.edu.ar/api/v1/biblios/1459', auth=(usuario, passwd))
    # data = response.json()
    # print('bbb', data)

    card_number = '21062181'
    # card_number = '38111171'
    # card_number = '13821438'
    card_number = '14121588'
    v_socio = verificar_socio(dominios, card_number)
    print(v_socio)

    





# RUN
if __name__ == '__main__':
    main()