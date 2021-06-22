CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 

#pip install beautifulsoup4
#pip install lxml
import json
import requests
from bs4 import BeautifulSoup

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
    if tabla == None:
      registros = None
    else  :
      for fila_tabla in tabla.findAll('tr'):
          registro = registro_fila_tabla(fila_tabla)  
          if len(registro) != 0:
              hora = registro.pop('hora')
              hh = int(hora[:2])
              registro = eliminar_unidades(registro)
              registros[hh] = registro        
    return registros

def registros_dia(estacion:str , fecha: str) -> dict:
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    return registros_tabla(tabla_dia)
    

def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    mes=['','enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    resultado = str(int(fecha)%100) + '-' + mes[int(fecha[4:6])] + '-' + fecha[0:4]
    return resultado

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    if registro['temp'][0:len(registro['temp'])-1] != 'N/D':
      registro['temp'] = int(registro['temp'][0:len(registro['temp'])-1])
    if registro['hum'][0:len(registro['hum'])-1] != 'N/D':
      registro['hum'] = int(registro['hum'][0:len(registro['hum'])-1])
    if registro['pres'][0:len(registro['pres'])-4] != '-' and registro['pres'][0:len(registro['pres'])-4] != '1011RMK':
      registro['pres'] = int(registro['pres'][0:len(registro['pres'])-4])
    return registro
    

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
  archivo = open(anho + '.txt', 'w')
  registros = {}
  for i in range(mes_ini,mes_fin+1):
    if i == 1 or i == 3 or i == 5 or i == 7 or i == 8 :
      for j in range(1,32):
        if j<10:
          registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + '0' + str(j)]) +'\n')
        else:
          registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + str(j)]) +'\n')
    elif i == 10 or i == 12:    
      for j in range(1,32):
        if j<10:
          registros[anho + str(i) + '0' + str(j)] = registros_dia(estacion, anho + str(i) + '0' + str(j))
          archivo.write(json.dumps(registros[anho + str(i) + '0' + str(j)]) +'\n')
        else:
          registros[anho + str(i) + str(j)] = registros_dia(estacion, anho + str(i) + str(j))
          archivo.write(json.dumps(registros[anho + str(i) + str(j)]) +'\n')
    elif i == 2:
      for j in range(1,29):
        if j<10:
          registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + '0' + str(j)]) +'\n')
        else:
          registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + str(j)]) +'\n')
    elif i == 11:
      for j in range(1,31):
        if j<10:
          registros[anho + str(i) + '0' + str(j)] = registros_dia(estacion, anho + str(i) + '0' + str(j))
          archivo.write(json.dumps(registros[anho + str(i) + '0' + str(j)]) +'\n')
        else:
          registros[anho + str(i) + str(j)] = registros_dia(estacion, anho + str(i) + str(j))
          archivo.write(json.dumps(registros[anho + str(i) + str(j)]) +'\n')       
    else:
      for j in range(1,31):
        if j<10:
          registros[anho + '0' + str(i) + '0' + str(j)] = registros_dia(estacion, anho + '0' + str(i) + '0' + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + '0' + str(j)]) +'\n')
        else:
          registros[anho + '0' + str(i) + str(j)] = registros_dia(estacion, anho + '0' + str(i) + str(j))
          archivo.write(json.dumps(registros[anho + '0' + str(i) + str(j)]) +'\n') 
  archivo.close()
  

def clima_estacion(estacion: str, anho: str):
  clima_anho(estacion, anho)
  texto = open(anho + '.txt', 'r')
  dias = []
  for linea in texto:
    dias.append(json.loads(linea))
  texto.close() 
  return dias  

def es_bisiesto(anho: int) -> bool:
  if anho%100==0:
    a=anho%400==0
  else: 
    a=anho%4==0
  return a 

def dias_del_anho_actual(fecha: tuple) -> int:
    # pre: fecha es una fecha válida
    # post: devuelve el número de días transcurridos en el corriente año, contando el actual
    DIAS_MESES_ANTERIORES = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    dia, mes, anho = fecha   

    dias = dia + DIAS_MESES_ANTERIORES[mes-1]
    if es_bisiesto(anho) and mes >= 3:
        dias = dias + 1
    return dias   




def temp_min_max(estacion: str , anho: str):
  for i in range(1,13):
    texto=open(anho + '.txt', 'r')
    dias = []
    mes = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)  
    if es_bisiesto(int(anho)):
      mes = (31, 29, 31,30,31,30,31,31,30,31,30,31)  
    max = 0
    min = 1000
    for linea in texto:
      dias.append(json.loads(linea))
    for j in range(mes[i-1]):
      fecha = (j, i, int(anho))
      hoy = dias_del_anho_actual(fecha) -1
      for hora in dias[hoy].keys():
        if dias[hoy][hora]['temp'] > max:
          max = dias[j][hora]['temp']
        if dias[hoy][hora]['temp'] < min:
          min = dias[j][hora]['temp']
    print('Temperatura maxima mes ',i , ':', max) 
    print('Temperatura minima mes ',i , ':', min)        


      


def temp_max(estacion, mes_ini, mes_fin):
    suma =  0
    cantidad_mediciones = 0
    for i in range(mes_ini,mes_fin+1):
      texto=open('2018.txt', 'r')
      dias = []
      mes = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)  
      if es_bisiesto(int(anho)):
        mes = (31, 29, 31,30,31,30,31,31,30,31,30,31)  
      for linea in texto:
        dias.append(json.loads(linea))
      for j in range(mes[i-1]):  
        max = 0
        fecha = (j, i, int(anho))
        hoy = dias_del_anho_actual(fecha) -1
        for hora in dias[hoy].keys():
          if dias[j][hora]['temp'] > max:
            max = dias[j][hora]['temp']
        cantidad_mediciones = cantidad_mediciones + 1      
        suma = suma + max   
    promedio = suma / cantidad_mediciones    
    return promedio 



def dir_viento(estacion, mes_ini, mes_fin):
  for i in range(mes_ini,mes_fin+1):
     texto=open('2018.txt', 'r')
     viento = []
     dias = []
     mes = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)  
     if es_bisiesto(int(anho)):
       mes = (31, 29, 31,30,31,30,31,31,30,31,30,31)  
     for linea in texto:
       dias.append(json.loads(linea))
     for j in range(mes[i-1]):
       fecha = (j, i, int(anho))
       hoy = dias_del_anho_actual(fecha) -1
       for hora in dias[hoy].keys():
         dias.append(dias[j][hora]['dir'])
  direcciones = ['Norte', 'Noroeste', 'Oeste', 'Suroeste', 'Sur', 'Sureste', 'Este', 'Noreste']
  max = 0
  for z in range(len(direcciones)):
    if dias.count(direcciones[z]) > max :
      max = dias.count(direcciones[z])
      direccion = direcciones[z]      
  return direccion    

clima_anho('legr', '2018', 1, 12)
temp_min_max('legr', '2018')
print('Promedio de temperaturas maximas en primavera:', temp_max('legr', 1, 12))
print('Direccion del viento predominante en primavera:', dir_viento('legr', 8, 12))