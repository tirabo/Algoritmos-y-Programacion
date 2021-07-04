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
    archivo_clima.close()
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
                archivo_clima = open(anho + '.txt','a')
                archivo_clima.write(json.dumps(clima_del_dia) + '\n')
                archivo_clima.close()          

            dia = dia + 1
            
        mes = mes + 1



def min_max(lista: list):
    # post: devuelve una lista con el minimo y el maximo de la lista ingresada
    max = lista[0]
    min = lista[0]
    for j in range(len(lista) - 1):
        if max < lista[j+1]:
            max = lista[j+1]
        if min > lista[j+1]:
            min = lista[j+1]    
        j = j+1 
        
    return [min, max]



def temp_min_max(estacion: str, anho: str):
    # post: devuelve un diccionario con las temperaturas min y max de cada mes del año ingresado
    MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio' , 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    temp = []
    dic_temp = {}
    i = 1
    
    # vemos si existe el archivo del año correspondiente
    # si no existe, lo creamos
    archivo = open(DIR + anho + '.txt', 'r')
    # Corregir: metí todo dentro del try
    for linea in archivo:
        dicc_linea = json.loads(linea)
        for fecha in dicc_linea:
            mes = int(fecha[4:6])
            dia = int(fecha[6:])
            clima_dia = dicc_linea[fecha]
        
        # enlistamos las temperaturas de todo un mes
        if mes == i:
            for hora in clima_dia:
                try:
                    temp.append(int(clima_dia[hora]['temp']))
                    
                except:
                    None    
        
        # si mes != i -> estamos con los registros del próximo mes
        # buscamos los valores min y max del mes que terminamos
        if mes != i or (mes == 12 and dia == 31):
            
            temp_min = min_max(temp)[0]
            temp_max = min_max(temp)[1]
            dic_temp[MESES[i-1]] = {'temp. min' : temp_min, 'temp. max' : temp_max}
            
            
            # vaciamos la lista de temperaturas y cargamos las del próximo mes 
            temp = []
            try:
                temp.append(int(clima_dia[hora]['temp']))
            except:
                None
            
            i = i + 1 
    archivo.close()

    return dic_temp        


def temp_max(estacion, anho):
    # post: devuelve el promedio de las temperaturas máximas diarias durante la primavera del año y la ciudad ingresada
    temp_max_diaria = []
    suma = 0
    # vemos si existe el archivo del año correspondiente
    # si no existe, lo creamos
    archivo = open(DIR + anho + '.txt', 'r') # Corregir: el close() debe estar dentro del try. Si  no, puede ocurrir que no haya open y cuando llegués a la instrucción archivo.close() te va a dar error. 
    for linea in archivo:
        dicc_linea = json.loads(linea)
        for fecha in dicc_linea:
            mes = int(fecha[4:6])
            dia = int(fecha[6:])

            # solo nos interesan los valores de la primavera -> del 21-09 al 21-12
            if (mes == 9 and dia >= 21) or (9 < mes < 12) or (mes == 12 and dia < 21):
                temp = []
                clima_dia_primavera = dicc_linea[fecha]
                # hacemos una lista con las temperaturas del dia
                for hora in clima_dia_primavera:
                    try:
                        temp.append(int(clima_dia_primavera[hora]['temp']))
                    
                    except:
                        None    
                # enlistamos la maxima temperatura del dia
                temp_max_diaria.append(min_max(temp)[1])
    archivo.close()
    for i in range(len(temp_max_diaria)):
        suma = suma + temp_max_diaria[i]
    temp_prom = suma // len(temp_max_diaria)

    return temp_prom 



def dir_viento(estacion, anho):
    # post: devuelve la dirección del viento predominante durante la primavera del año y la ciudad elegida.
    dir = []
    lista_dir = []
    pos = 0
    archivo = open(DIR + anho + '.txt', 'r')
    for linea in archivo:
            dicc_linea = json.loads(linea)
            for fecha in dicc_linea:
                mes = int(fecha[4:6])
                dia = int(fecha[6:])
                # solo nos interesan los valores de la primavera -> del 21-09 al 21-12
                if (mes == 9 and dia >= 21) or (9 < mes < 12) or (mes == 12 and dia < 21):
                        clima_dia_primavera = dicc_linea[fecha]
                        # hacemos una lista con las direcciones del viento del dia
                        for hora in clima_dia_primavera:
                            try:
                                    dir.append(clima_dia_primavera[hora]['dir'])
                                    
                            except:
                                    None                         
    archivo.close()


    
    # vemos cuales son todas las direcciones posibles del viento
    dir_distintas = list (set(dir))
    
    for i in range(len(dir_distintas)):
            direccion = dir_distintas[i]
            cont = 0
            # hacemos una lista que contenga una lista con la direccion del viento y cuántas veces se repite
            for j in range(len(dir)):
                    if dir[j] == direccion:
                            cont = cont + 1 
            lista_dir.append([direccion, cont])

    # vemos cuál es la direccion del viento que mas se repite en la primavera     
    max = lista_dir[0][1]        
    for i in range(len(lista_dir)):
            if max < lista_dir[i][1]:
                    max = lista_dir[i][1]
                    pos = i
                    
    return lista_dir[pos][0]

"""Finalemente, deberán ejecutar las funciones y mostrar los resultados obtenidos."""

# Resultados
# creamos el archivo con el clima del año 2018 de una estacion meteorologica
# clima_anho('mtpp', '2018', 1, 12)

print(temp_min_max('mtpp', '2018'))
print(temp_max('mtpp', '2018'))
print(dir_viento('mtpp', '2018'))