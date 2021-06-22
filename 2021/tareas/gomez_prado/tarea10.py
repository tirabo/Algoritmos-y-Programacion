import requests 
from bs4 import BeautifulSoup
import json

DIR = './2021/tareas/gomez_prado/'
CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 


# Función de estadísticas anuales del clima
def estadisticas(estacion: str,archivo: dict):
    # pre:recibe un str y un dict.
    # post operaciones de print.
    assert type(estacion) ==str and type(archivo) == dict,'nombre o archivo invalido'
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    lista5 = []
    j = 0
    for key in archivo.keys():
        # print(key)
        valor = str(j)
        for i in range(24):
            #print(i,key,archivo[key][valor]['temp'])
            lista1.append(archivo[key][valor]['temp'])
            lista2.append(archivo[key][valor]['hum'])
            lista3.append(archivo[key][valor]['vel'])
            lista4.append(archivo[key][valor]['pres'])
            lista5.append(archivo[key][valor]['dir'])
            j+=1     
    print("Estación: " ,estacion)
    print("Variables:", 'temp','hum','vel','pres','dir')
    print("valor Max: ",max(lista1),"",max(lista2),max(lista3),"",max(lista4),max(lista5))
    print("Promedio:    ",int(sum(lista1)/len(lista1)),"",int(sum(lista2)/len(lista2)),"",int(sum(lista3)/len(lista3))," ",int(sum(lista4)/len(lista4)))
    print("valor Min: ",min(lista1),"",min(lista2),"",min(lista3)," ",min(lista4),min(lista5))


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

# codigo de ejercicio    
def registros_tabla(tabla) -> dict:          # procesa una tabla, devuelve un diccionario de registros contenidos en esa tabla
    registros = {}
    for fila_tabla in tabla.findAll('tr'):
        registro = registro_fila_tabla(fila_tabla)
        if len(registro) != 0:
            hora = registro.pop('hora')
            hh = int(hora[:2])
            registros[hh] = registro
    return registros


# Guardar archivo json
def guardar_archivo(archivo: dict) -> str: # Corrección: devuelve str no dict
    #pre: recibe un diccionario.
    #post: devuelve un archivo dumps de json.
    assert type(archivo) == dict , 'Archivo incorrecto'
    json_string = json.dumps(archivo)
    with open(DIR + "Data_fmmi.json", "w") as outfile: 
        json.dump(json_string, outfile)
    outfile.close()
    return json_string


# Abrir archivo json
def abrir_json(archivo) ->dict:
    # pre: recibe un archivo dict dumps de json
    # post: devuelve un dict de json
    assert type(archivo) == dict or type(archivo) == str, 'Archivo incorrecto'
    with open(DIR + archivo, "r") as read_file:
        json_data = json.load(read_file)
    read_file.close()    
    py_data = json.loads(json_data)
    print("Archivo Cargado")
    print("Cantidad de Registros: ", len(py_data))
    #for key, value in py_data.items(): 
    #  print(key, value)
    return py_data   


# Función que modifica las claves de los diccionarios
def modificar(i,fecha_dic,buscar_fecha,lista_dict,diccionario):
    # pre : recibe  5 valores para reindexar las claves de los dicts.
    # post: devuelve una lista y un diccionario reindexado.
    assert type(i)== int and type(fecha_dic) == dict and type(buscar_fecha) == str and type(lista_dict) == list and type(diccionario) == dict, 'Error de tipo de dato'
    num = 24 * (i-1) if i == 2 else (24 * (i-1)) -1
    claves_dict = generador_claves(num)
    reg_ = dict((claves_dict[key], value) for (key, value) in fecha_dic.items())
    lista_dict.append(reg_)
    diccionario[buscar_fecha] = lista_dict[i-1]
    return lista_dict,diccionario


# Función que genera claves.
def generador_claves(n: int) ->dict:
    # pre: recibe un valor entero.
    # post: devuelve un diccionario con 23 claves y valores.
    assert type(n) == int, 'n es un entero'
    valor = range(0,24)
    # creo un diccionario por comprensión
    if n == 0:
        claves = (dict((x, x+24) for x in (valor)))
    else:
        claves = (dict((x, x+n) for x in (valor)))    
    #print(claves.keys())
    #print(claves.values())
    return claves


# Pre procesado de datos
def eliminar_unidades(registro: dict):
    # pre : recibe un diccionario.
    # post : devuelve un diccionario preprocesado.
    assert type(registro)== dict , 'Error de archivo invalido'
    for i in registro:
        if registro[i]['temp'] == 'N/D°':
            registro[i]['temp'] = int(registro.get(i-1)['temp'])
        else:
            registro[i]['temp'] = int(registro[i]['temp'].replace('°',"").strip())

        registro[i]['hum'] = int(registro[i]['hum'].replace('%',"").strip()) if registro[i]['hum'] != 'N/D%' else int(registro.get(i-1)['hum'])

        if registro[i]['vel'] != 'En calma':
            if len(registro.get(i)['vel']) < 9:# cuento cuantos digitos tiene vel 
                registro[i]['vel'] = int(registro[i]['vel'].replace('km/h',"").strip())
            else:
                val_1 = int(registro.get(i)['vel'].strip()[:2])
                val_2 = int(registro.get(i)['vel'].strip()[5:7])
                prom = (val_1 + val_2)/2
                registro[i]['vel'] = prom
        else:
            registro[i]['vel'] = int(0)

        if registro[i]['pres'] == '- hPa':
            registro[i]['pres'] = int((1016+1017+1018+1019+1020)/5)
        else:
            registro[i]['pres'] = int(registro[i]['pres'][:4])                
    return registro


# Función que formatea una fecha
def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve str(fecha_formateada) = dia-mes-año 
    assert type(fecha) == str and len(fecha) == 8 , 'son 8 digitos para fecha'
    diccionario = {1 : 'enero', 
                    2 : 'febrero', 
                    3 : 'marzo', 
                    4 : 'abril', 
                    5 : 'mayo', 
                    6 : 'junio', 
                    7 : 'julio', 
                    8 : 'agosto', 
                    9 : 'septiembre', 
                    10 : 'octubre', 
                    11 : 'noviembre', 
                    12 : 'diciembre'}

    año = fecha[:4]
    if int(fecha[-4]) == 0:
        mes = int((fecha)[-3:6])
    else:
        mes = int((fecha)[-4:6])

    if int(fecha[-2]) == 0:
        dia = fecha[-1]
    else:
        dia = fecha[-2:]
    fecha_formateada = dia + '-' + diccionario[mes] + '-' + año
    return fecha_formateada


# Función que busca un registro por estación y fecha.
def registros_dia(estacion: str, fecha: str)-> dict:
    # pre: recibe un valor str para estacion, recibe un valor srt(fecha).
    # post: Devuelve un diccionario de la busqueda. 
    assert type(estacion) == type(fecha) == str and len(fecha) == 8 , 'son 8 digitos para fecha'
    nombre_fecha = formatear_fecha(fecha) 
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+ estacion +'/'+ nombre_fecha + '.html',timeout=None)
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml')  
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) 
    return eliminar_unidades(registros_tabla(tabla_dia))

# Función Principal
def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre: recibe un valor para estación, año , mes inicial y mes final.
    # post: devuelve un archivo json con los datos formateados. 
    # el diccionario "dias_del_mes" se armo manual verificando que la data exista en la pagina para evitar errores
    assert type(estacion) == type(anho) == str and type(mes_ini) == int and type(mes_fin) == int, 'Error de tipo de dato en función principal'
    print("Descargando y Procesando -> Aguarde...")
    reg_cont = 0
    lista_dict = []
    diccionario = dict()
    dias_del_mes = { 1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30,
                                    7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31 }
    inicio = mes_ini
    hasta = mes_fin
    j = - inicio
    cont = 0
    while cont <= hasta + j:
        for i in range(1,dias_del_mes[inicio]+1):
            reg_cont += 1
            mes_1 = ""
            mes_2 = ""
            dia = '0'+ str(i) if len(str(i)) == 1 else str(i)
            mes = str(cont+1)
            if (cont+1) < 10:
                mes_1 = '0' + mes
                buscar_fecha = anho + mes_1 + dia    
            else:
                mes_2 = str(cont+1)
                buscar_fecha = anho + mes_2 + dia    

            fecha_dic = registros_dia(estacion,buscar_fecha)
            print(reg_cont,buscar_fecha,fecha_dic) # print registros descargados y pre procesados con claves duplicadas.

            # Modifico las claves de valores de los diccionarios y los almaceno en una lista.
            # de esta manera evito errores de claves duplicadas cuando quiera recuperar los datos.
            if cont == 0:
                if i == 1:
                    lista_dict.append(fecha_dic)
                    diccionario[buscar_fecha] = lista_dict[0]    
                else:
                    lista_dict,diccionario = modificar(i,fecha_dic,buscar_fecha,lista_dict,diccionario)
            else:
                lista_dict,diccionario = modificar(reg_cont,fecha_dic,buscar_fecha,lista_dict,diccionario)
        cont += 1
        inicio += 1

    print("Proceso Completado")
    print("Archivo guardado con exito")
    print("Cantidad de elementos en la lista: ",len(diccionario))
    json_string = guardar_archivo(diccionario)
    print("dumps: ",type(json_string))
    # print("loads: ",type(json.loads(json_string)))


def temp_min_max(estacion, anho):
    # pre : recibe dos string
    # post : print de datos
    assert type(estacion) == type(anho)== str, 'Error de tipo de dato'
    lista1 = []
    mes = 1
    cont = 0 
    j = 0
    data = abrir_json('Data_fmmi.json')
    for key in data.keys():
        #print(key)
        cont += 1
        valor = str(j) 
        for i in range(24):
            # print(i,key,data[key][valor]['temp'])
            # print(valor,' ', end='')
            lista1.append(data[key][valor]['temp']) # Corrección: no estás considerando la hora, para el mismo día siempre da lo mismo sin importar la hora.
            j+=1 # Corrección: con esto no aumentas la variable valor (si es lo que querías hacer), solo la variable j. 
        if cont == 31 or cont == 59 or cont == 90 or cont == 120 or cont == 151 or cont == 181 or cont == 212 or cont == 243 or cont == 273 or cont == 304 or cont == 334 or cont == 365:
            print("")
            print("Temperaturas", end='')
            # print("mes :",mes) 
            # print("días:",cont)
            print("max :" ,(max(lista1)), ' ', end='')
            print("min :" ,(min(lista1)))
            #print("año :",anho)
            #print("est :",estacion)
            mes += 1


def temp_max(estacion, mes_ini, mes_fin):
    # pre : recibe un str y dos enteros.
    # post : print de datos
    assert type(estacion)==str and int == type(mes_ini) == type(mes_fin), 'Error de tipo de datos'
    lista1 = []
    lista2 = []
    mes = 1
    cont = 0 
    j = 0
    # clave = data # Corrección: uso de variable global
    data = abrir_json('Data_fmmi.json')
    for key in data.keys():
        #print(key)
        cont += 1
        valor = str(j)
        for i in range(24):
            #print(i,key,data[key][valor]['temp'])
            if cont >= 283 and cont <= 355: # primavera del 21 de sep al 21 de diciembre
                lista1.append(data[key][valor]['temp'])
            j+=1
            mes += 1 
            if cont >= 283 and cont <= 355: # primavera del 21 de sep al 21 de diciembre
                lista2.append(max(lista1)) 
    print("")
    print("Temp Máximas")
    print("mes            : ",mes_ini) 
    print("hasta        : ",mes_fin)
    #print("meses:",len(lista2))
    print("promedio : " ,int(sum(lista2)/len(lista2)))
            #print("min :" ,(min(lista1)))
            #print("año :",anho)
    print("estación : ",estacion)
            #mes += 1


def dir_viento(estacion, mes_ini, mes_fin):
    # pre : recibe un str y dos enteros.
    # post : print de datos
    assert type(estacion)==str and int == type(mes_ini) == type(mes_fin), 'Error de tipo de datos'
    lista1 = []
    lista2 = []
    mes = 1
    cont = 0 
    j = 0
    data = abrir_json('Data_fmmi.json')
    for key in data.keys():
        #print(key)
        cont += 1
        valor = str(j)
        for i in range(24):
            #print(i,key,data[key][valor]['temp'])
            lista1.append(data[key][valor]['vel'])
            lista2.append(data[key][valor]['dir'])
            j+=1
        if cont == 283 and cont <= 355: # primavera del 21 de sep al 21 de diciembre
            print("")
            print("Viento Predominante")
            print("mes            :",mes_ini) 
            print("hasta        :",mes_fin)
            print("vel prom :" ,int(sum(lista1)/len(lista1)))
            print("dir max    :" ,max(lista2))
            print("dir min    :" ,min(lista2))
            print("año            :",'2018')
            print("estación :",estacion)
            mes += 1


def main():
    año = '2018'
    estacion = 'fmmi' 
    # 1.Test - Obtener las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
    temp_min_max(estacion,año)
    # 2.Test - Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida.
    temp_max(estacion,9,11)# Primavera: septiembre, octubre y noviembre
    # 3.Test - Calcular la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.
    dir_viento(estacion,9,11)# Primavera: septiembre, octubre y noviembre

# RUN

if __name__ == '__main__':
    main()