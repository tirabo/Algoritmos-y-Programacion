import requests
import os

# Documentación de la API de Koha: https://api.koha-community.org/

usuario = 'soporte'
passwd = 'Shei5oom'

def datos_usuario(dominio, card_number, surname=''):
    # pre : dominio es la url  admin del koha de la biblioteca
    #       card_number es el número de socio (el DNI)
    # post: devuelve una lista de diccionarios con los datos del socio
    data = []
    url = dominio + '/api/v1/patrons'
    if len(surname) > 0:
        response = requests.get(url, auth=(usuario, passwd), params= {"cardnumber": card_number, "surname": surname})
    else:
        response = requests.get(url, auth=(usuario, passwd), params= {"cardnumber": card_number})
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "Palacios"})
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data = response.json()
        return data
    else:
        print('Hubo un problema al cargar el archivo JSON del usuario con cardnumber', card_number, 'en', dominio, '(status code:', str(response.status_code)+')' )


def prestamos_usuario(dominio, card_number, surname=''):
    # pre : dominio es la url  admin del koha de la biblioteca
    #       card_number es el número de socio (el DNI)
    #       surname parte del apellido del socio (opcional)
    # post: devuelve una 2-ulpa
    #       coordenada 0: True si el socio tiene restricciones (suspendido), False en caso contrario
    #       coordenada 1: lista de diccionarios con los items préstamos
    socio =  datos_usuario(dominio, card_number, surname)
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
            print('Hubo un problema al cargar el archivo JSON de préstamos del usuario con cardnumber', card_number, 'en', dominio, '(status code:', str(response.status_code)+')' )


def listar_bibliotecas(dominio):
    url = dominio + '/api/v1/libraries'
    response = requests.get(url, auth=(usuario, passwd))
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data = response.json()
        return data
    else:
        print('Hubo un problema al cargar el archivo JSON de bibliotecas en', dominio, '(status code:', str(response.status_code)+')' )


def datos_item(dominio, item_id):
    # pre: url administrativa del sistema de gestión de la biblioteca
    #      item_id es el id del item
    # post: los datos del item
    url_item = dominio + '/api/v1/items/' + str(item_id)
    response = requests.get(url_item, auth=(usuario, passwd))
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "Palacios"})
    if response.status_code == 200:
        # El archivo JSON fue encontrado y cargado correctamente
        data_item = response.json()
        return data_item 
    else:
        print('Hubo un problema al cargar el archivo JSON del item con itemnunber', item_id, 'en', dominio, '(status code:', str(response.status_code)+')' )


def verificar_socio(dominios, card_number, surname=''):
    # pre: dominios es una lista de dominios administrativos del sistema de gestión de bibliotecas
    #      card_number es el número de socio (el DNI)
    # post: devuelve una lista de longitud len(dominios) donde  coordenada i tenemos
    #       (dominios[i], card_number, "¿es socio?", "¿está suspendido?", "¿tiene préstamos?", lista item_id de prestamos que tiene el socio)
    devuelve = []
    for dominio in dominios:
        es_socio, suspendido, tiene_prestamos, prestamos = False, False, False, []
        socio =  datos_usuario(dominio, card_number, surname)
        # print(dominio, card_number, socio)
        if len(socio) > 0:
            es_socio = True
            suspendido, prsts = prestamos_usuario(dominio, card_number, surname)
            if len(prsts) > 0:
                tiene_prestamos = True
                for pr in prsts:
                    prestamos.append(pr['item_id'])
        devuelve.append((dominio, card_number, surname, es_socio, suspendido, tiene_prestamos, prestamos))
    return devuelve

def mostrar_socio_verificado(socio_verificado):
    # pre: socio_verificado es el output de la función verificar_socio()
    # post: muestra por pantalla los datos del socio verificado
    for biblioteca in socio_verificado:
        if biblioteca[3]:
            dominio, card_number, surname, es_socio, suspendido, tiene_prestamos, prestamos  = biblioteca[0], biblioteca[1], biblioteca[2], biblioteca[3], biblioteca[4], biblioteca[5], biblioteca[6]
            socio = datos_usuario(dominio, card_number, surname)
            apellido, nombre = socio[0]['surname'], socio[0]['firstname']
            print('\nSocio: ', apellido+',', nombre, '(' + str(card_number) + ')', 'en', biblioteca[0])
            susp= 'Sí' if suspendido else 'No'
            print('Suspendido:', susp)
            print('Prestamos: ', end='')
            if len(prestamos) > 0:
                print('Sí')
                print('Libros no devueltos:')
                for libro in prestamos:
                    item = datos_item(dominio, libro)
                    # print(libro, item)
                    if item:
                        print('- El item con  código de barras', item['external_id'], 'está prestado', end='')
                        # https://faud.biblioadmin.unc.edu.ar/cgi-bin/koha/catalogue/moredetail.pl?biblionumber=48232&itemnumber=83627
                        # print(' (ver en', str(dominio)+'/cgi-bin/koha/catalogue/moredetail.pl?biblionumber='+str(item['biblio_id'])+'&itemnumber='+str(item['item_id'])+')')
                        # o bien https://faud.biblio.unc.edu.ar/cgi-bin/koha/opac-detail.pl?biblionumber=48232
                        print(' (ver en', str(dominio)+'/cgi-bin/koha/opac-detail.pl?biblionumber='+str(item['biblio_id'])+')')
                if len(prestamos) >= 20:
                    print('La cantidad de préstamos es 20 o más')
                else:
                    print('La cantidad de préstamos es', len(prestamos))
            else:
                print('No')
                        

    
    

def main():
    dominios = ['https://faud.biblioadmin.unc.edu.ar', 'https://eco.biblioadmin.unc.edu.ar', 'https://ffyh.biblioadmin.unc.edu.ar', 'https://agro.biblioadmin.unc.edu.ar', 'https://famaf.biblioadmin.unc.edu.ar']
    # usuario = bajar_usuario(url, 1)
    # bibliotecas = listar_bibliotecas(dominio)
    # for bib in bibliotecas:
    #     print(bib['library_id'],':', bib['name'])

    socio =  datos_usuario(dominios[0], '21062181')
    # print(socio)
    socio =  datos_usuario(dominios[0], '13821438')
    # print(socio)
    socio =  datos_usuario(dominios[0], '462','ENC')
    # print(socio)

    socio =  datos_usuario(dominios[1], '38111171')
    # print(len(socio))
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

    # print('Datos de un item:',datos_item(dominios[0], 83627)) 

    # response = requests.get('https://faud.biblioadmin.unc.edu.ar/api/v1/biblios/1459', auth=(usuario, passwd))
    # data = response.json()
    # print('bbb', data)

    # url = dominios[0] + '/api/v1/patrons'
    # response = requests.get(url, auth=(usuario, passwd), params= {"surname": "ENCUADERNACION LIBROS 2022"})
    # print(response.json())

    # item_id = 83627
    # item_id = 28970 # este falla aunque existe
    # url_item = dominios[0] + '/api/v1/items/' + str(item_id)
    # response = requests.get(url_item, auth=(usuario, passwd))
    # print(response)

    # url = dominios[0] + '/api/v1/patrons'
    # response = requests.get(url, auth=(usuario, passwd), params= {"cardnumber": '462'})
    # respuesta = response.json()
    # for rr in respuesta:
    #     print(rr['cardnumber'], rr['firstname'], rr['surname'])


    # card_number = '21062181'
    # card_number = '38111171'
    card_number = '13821438'
    # card_number = '14121588'
    v_socio = verificar_socio(dominios, card_number)
    # print(v_socio)
    mostrar_socio_verificado(v_socio)
    card_number, surname = '462', 'ENCUADERNACI'
    v_socio = verificar_socio(dominios, card_number, surname)
    mostrar_socio_verificado(v_socio)

    





# RUN
if __name__ == '__main__':
    main()