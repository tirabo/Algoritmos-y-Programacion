import requests
from bs4 import BeautifulSoup
import json


CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres']
DIR = './2021/tareas/rossi/'


def registro_fila_tabla(fila_tabla) -> dict: # procesa una fila de la tabla, devuelve un diccionario con las mediciones registradas en esa fila
    celdas_fila = fila_tabla.findAll('td')
    registro = {}
    i = 0
    for celda in celdas_fila:                # recorre las celdas de la fila correspondiente a una toma de mediciones
        if celda.img != None: # si existe el tag 'img'
            input_tag = celda.img['title'] # recupera en el tag 'img' el valor del atributo 'title'
            registro[CLAVES[i]] = input_tag # dirección del viento
            i = i + 1
        registro[CLAVES[i]] = celda.text
        i = i + 1
    return registro


def registros_tabla(tabla) -> dict:          # procesa una tabla, devuelve un diccionario de registros contenidos en esa tabla
    registros = {}
    for fila_tabla in tabla.findAll('tr'):
        registro = registro_fila_tabla(fila_tabla)
        if len(registro) != 0:
            hora = registro.pop('hora')
            hh = int(hora[:2])
            registros[hh] = registro
    return registros


def es_bisiesto(anho: int) -> bool:
    # post: devuelve si anho es bisiesto
    anho_bisiesto = anho % 4 == 0
    if anho % 100 == 0:
        anho_bisiesto = anho % 400 == 0
    return anho_bisiesto 


def es_fecha_valida(fecha: tuple) -> bool:
    # post: devuelve si fecha es una fecha válida
    dia, mes, anho = fecha
    anho_ok = 1 <= anho
    mes_ok = 1 <= mes <= 12
    if mes in [4, 6, 9, 11]:
        dia_ok = 1 <= dia <= 30
    elif mes == 2:
        dia_ok = 1 <= dia <= 28 or (dia == 29 and es_bisiesto(anho))
    else:
        dia_ok = 1 <= dia <= 31
    
    return dia_ok and mes_ok and anho_ok    


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha valida en formato 'AAAAMMDD'
    # post: devuelve la fecha  en el formato dia-nombre del mes-año
    anho = int (fecha[:4])
    mes = int (fecha[4:6])
    dia = int (fecha[6:])
    assert type (fecha) == str and len(fecha) == 8 and es_fecha_valida((dia, mes, anho)), 'Error: fecha debe ser una fecha válida en str con formato AAAAMMDD '
    
    MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    nombre_del_mes = MESES[mes-1]
    
    fecha_en_formato = str(dia) + '-' + nombre_del_mes + '-' + str(anho)
    
    return fecha_en_formato


def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}

    digitos_valor = []

    for clave in (registro):
        if clave == 'temp' or clave == 'hum':
            # tenemos que quitar el ultimo digito
            digitos_valor = list (registro[clave])
            digitos_valor.pop(-1)
            valor_sin_unidades = ''.join(digitos_valor)
            registro[clave] = valor_sin_unidades
            
        if clave == 'vel' or clave == 'pres':
            # tenemos que quitar la segunda palabra
            palabras = registro[clave].split()
            registro[clave] = (palabras[0])

        try :
            registro[clave] = int (registro[clave])            
        except:
            None
    return registro


def registros_dia(estacion: str, fecha: str) -> dict:
    # pre: fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la informacion del clima del día fecha en formato de diccionario sin unidades
    assert type (estacion) == type (fecha) == str and len(fecha) == 8 , 'Error: la fecha debe ser un str con formato AAAAMMDD'
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion + '/' + formatear_fecha(fecha) + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    
    tabla_dic = {}
    tabla_dic_sin_unid = {}
    
    # nos aseguramos que la tabla se pueda procesar
    if tabla_dia != None:
        tabla_dic = registros_tabla(tabla_dia)
            
        for hora in tabla_dic:
            tabla_dic_sin_unid[hora] = eliminar_unidades(tabla_dic[hora])

    return tabla_dic_sin_unid


def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):   
    # pre: recibe dos str y dos int entre 1 y 12, con mes_ini <= mes_fin
    # post: crear el archivo AAAA.txt con datos del clima de estacion entre mes_ini y mes_fin
    precond = type (estacion) == type (anho) == str and type (mes_ini) == type (mes_fin) == int
    meses_validos = 1 <= mes_ini <= 12 and 1 <= mes_fin <= 12
    assert  precond and meses_validos and mes_ini <= mes_fin, 'Error: debe ingresar un str y dos int entre 1 y 12, con mes_ini <= mes_fin' 
    
    # creamos el archivo anho.txt e iniciamos variables a utilizar
    archivo_clima = open(DIR + anho + '.txt','w')
    archivo_clima.close() # 
    anho_num = int(anho)
    cadena_de_dicc = {}
    for mes in range(mes_ini, mes_fin + 1):
        for dia in range(1, 32):
            clima_del_dia = {}
            dia_str = str(dia)
            mes_str = str(mes)
            
            if es_fecha_valida((dia, mes, anho_num)):
                if dia < 10 :
                    dia_str = '0' + str(dia)
                if mes < 10 :
                    mes_str = '0' + str(mes)   
                
                # guardamos en la clave AAAAMMDD un dict con el registro del clima de la fecha correspondiente
                key = anho + mes_str + dia_str
                clima_del_dia[key] = registros_dia(estacion, key) 
                
                # agregamos el diccionario al archivo, en cadena json
                archivo_clima = open(DIR + anho + '.txt','a')
                print(clima_del_dia)
                archivo_clima.write(json.dumps(clima_del_dia) + '\n')
                archivo_clima.close()          
            dia = dia + 1
        mes = mes + 1

"""A partir de las funciones definidas previamente y de estas dos funciones,  se deberán definir tres funciones que devuelven los resultados deseados  en el formato que les resulte más conveniente."""

def temp_min_max_del_mes(estacion: str, anho: str, mes: int):
    # post: devuelve las temperaturas máximas y mínimas de cada mes de anho de la estacion meteorologica ingresada
    
    # creamos el archivo anho.txt e iniciamos variables a utilizar
    # clima_anho(estacion, anho, mes, mes) # Corrección: correrlo antes
    archivo = open(DIR + anho + '.txt', 'r')
    clima_dia_list = []
    temp_lista = []
    valor = []
    clima_dia_dicc = {}
    res={}
    max_temp = 0
    min_temp = 0
    
    # hacemos una lista de diccionarios de cada dia del mes
    for line in archivo:           
        clima_dia_list.append(json.loads(line)) 

    # accedemos a cada diccionario de diccionario la lista 
    for i in range(len(clima_dia_list)):
        clima_dia_dicc = clima_dia_list[i] 
        
        for key in clima_dia_dicc:
            contenido_dia = clima_dia_dicc[key]   
            # hacemos una lista con las temperaturas de cada dia del mes
            for hora in contenido_dia:
                temp_lista.append(contenido_dia[hora]['temp'])
    # i = i + 1 # no se entiende esta asignación
    archivo.close()
    # hacemos una lista donde no se repitan los valores de temperaturas
    valor_de_temp = list(set(temp_lista))
    
    # nos aseguramos que todos los valores sean int
    for i in range(len(valor_de_temp)):
        try:
            valor.append(int(valor_de_temp[i]))
        except:
            None
    # buscamos el maximo y minimo valor de temperatura
    max_temp = valor[0]
    min_temp = valor[0]
    for j in range(len(valor) - 1):
        if max_temp < valor[j+1]:
            max_temp = valor[j+1]
        
        if min_temp > valor[j+1]:
            min_temp = valor[j+1]    
        j = j+1 
    res['temp, max'] = max_temp
    res['temp, min'] = min_temp 
    return res



def temp_min_max(estacion: str, anho: str):
    # post: devuelve un dict con las temperaturas máximas y mínimas de cada mes del año
    temp_anho = {}
    for mes in range(1, 13):
        temp_anho[str(mes)] = temp_min_max_del_mes(estacion, anho, mes)
    return temp_anho


def temp_max(estacion, mes_ini, mes_fin):
    pass

def dir_viento(estacion, mes_ini, mes_fin):
    pass

"""Finalemente, deberán ejecutar las funciones y mostrar los resultados obtenidos."""

# Resultados


def main():
    estacion, anho = 'mtpp', '2018' # Puerto Príncipe
    # clima_anho(estacion, anho, 1, 12)
    print(temp_min_max('mtpp', '2018'))
    


# RUN

if __name__ == '__main__':
    main()