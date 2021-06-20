import requests
from bs4 import BeautifulSoup
import ast

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/fahy/'

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

# Lo que escribí en ejercicios anteriores

# De ejercicio 1:
def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    precondition = type(fecha) == str and fecha.isnumeric() and len(fecha) == 8
    assert precondition, "Error: formatear_fecha() acepta un string de 8 cifras en el formato 'AAAAMMDD'"

    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    return ("{}-{}-{}".format(fecha[6:], meses[int(fecha[4:6]) - 1], fecha[:4])) if int(fecha[6:8]) > 9 else "{}-{}-{}".format(fecha[7:], meses[int(fecha[4:6]) - 1], fecha[:4])

def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    assert type(registro) == dict, "Error: eliminar_unidades recibe un diccionario"
    
    r = registro

    temp_strip = r['temp'].strip("°")
    if temp_strip.isnumeric() or temp_strip.strip("-").isnumeric():
        r['temp'] = int(temp_strip)
    else:
        r['temp'] = None

    vel_strip = r['vel'].strip(" km/h")
    if vel_strip.isnumeric():
        r['vel'] = int(vel_strip)
    else:
        r['vel'] = None

    hum_strip = r['hum'].strip("%")
    if hum_strip.isnumeric():
        r['hum'] = int(hum_strip)
    else:
        r['hum'] = None

    pres_strip = r['pres'].strip(" hPa")
    if pres_strip.isnumeric():
        r['pres'] = int(pres_strip)
    else:
        r['pres'] = None

    return r

# De ejercicio 2:

# esto viene de una tarea anterior
def es_bisiesto(anho: int) -> bool:
    # pre: anho > 0
    # post: devuelve True si anho es divisible por 4 (NO corresponde siempre a un año bisiesto)
    precondición = type(anho) == int and anho > 0
    assert precondición, 'Error: anho debe ser un entero positivo.'

    return anho % 4 == 0 and anho % 100 != 0 or anho % 400 == 0

def dias_en_el_mes(anho: int, mes: int) -> int:
    # pre: mes es un int entre 1 y 12 inclusivo, anho es mayor que 0
    # post: devuelve un int nr_dias, entre 1 y 31 inclusivo, correspondiendo al núúmero de días en el mes de este año
    precondition = type(anho) == type(mes) == int and 0 < anho and 1 <= mes <= 12
    assert precondition, 'Error: dias_en_el_mes() recibe 2 parámetros: el año con 4 cifras, y el mes con 1 <= mes <= 12'

    if mes in [4, 6, 9, 11]:
        nr_dias = 30
    elif mes == 2:
        nr_dias = 29 if es_bisiesto(anho) else 28
    else:
        nr_dias = 31

    return nr_dias

# Código redifinido de ejercicios anteriores 
def registros_dia(estacion: str, fecha: str) -> dict:
    # pre: estacion es la sigla de una estación con 4 letras; fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve un diccionario de diccionarios
    precondition = type(estacion) == type(fecha) == str and len(estacion) == 4 and estacion.isalpha() and fecha.isnumeric() and len(fecha) == 8
    assert precondition, 'Error: registros_dia() recibe la sigla de la estación de 4 letras y una fecha en el formato "AAAAMMDD"'

    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    dict_dia = registros_tabla(tabla_dia)

    for i in dict_dia:
        dict_dia[i] = eliminar_unidades(dict_dia[i])
    
    return dict_dia

def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre: recibe una sigla de 4 letras, una string 'AAAA', y dos numeros enteros entre 1 y 12 tal que mes_ini <= mes_fin
    # post: guarda en el archivo 'AAAA.txt', en cada renglón, los datos del clima de cada día en la estación de la sigla desde mes_ini hasta el mes_fin
    precondition = type(estacion) == type(anho) == str and type(mes_ini) == type(mes_fin) == int and estacion.isalpha() and len(estacion) == 4 and anho.isnumeric() and len(anho) == 4 and 1 <= mes_ini <= mes_fin <= 12
    assert precondition, "Error: clima_anho() recibe 4 parámetros: el estación como sigla de 4 letras, el año como string de 4 números, y 2 numeros, mes_inicial y mes_final, 1 <= mes_inicial <= mes_final <= 12"
    
    nombre = DIR + anho + '.txt'
    archivo = open(nombre,'w')
    
    mes = mes_ini

    while mes <= mes_fin:
        dia_ini = 1
        dia_fin = dias_en_el_mes(int(anho), mes)
        while dia_ini <= dia_fin:
            str_mes = str(mes) if mes >= 10 else '0' + str(mes)
            str_dia = str(dia_ini) if dia_ini >= 10 else '0' + str(dia_ini)
            fecha = anho + str_mes + str_dia

            linea = {}
            linea[fecha] = registros_dia(estacion, fecha)
            archivo.write(str(linea))
            archivo.write("\n")
            dia_ini = dia_ini + 1

        mes = mes + 1

    archivo.close()

# Como generar 2018.txt tarda tanto, para ahorrar tiempo he puesto como comentario (con # o con ''')
# los partes del código de los ejercicios 3(ii) y 3(iii) debajo que generan 2018.txt. Si quieren usar
# temp_max() o dir_viento() sin ejecutar previamente temp_min_max(), hay que sacar los comentarios
# para que se genere el archivo 2018.txt

# Ejercicio 3 (i):


def max_min_del_dia(data_dia: dict) -> list:
    # pre: recibe un dict correspondiendo a todos los datos de un día (una linea del archivo)
    # post: devuelve una lista de dos valores [max, min] con la temperatura máxima y mínima del día

    max_min = [-100, 100]

    # como un_dia sólo tiene 1 llave en el primer nivel, day_date es una lista de 1 item (p. ej. ['20181222'])
    dia_llave = list(data_dia.keys())[0]

    # iteramos sobre los datos del día
    horas = list(data_dia[dia_llave].keys())
        
    for hora in horas:
        temp = data_dia[dia_llave][hora]['temp']
        if temp >= max_min[0] and temp != None:
                max_min[0] = temp

        if temp <= max_min[1] and temp != None:
                max_min[1] = temp
    
    # por si el día no tiene ninguna temperatura registrada
    if max_min[0] == -100:
        max_min[0] = None

    if max_min[1] == 100:
        max_min[1] = None

    return max_min

def temp_min_max(estacion: str, anho: str) -> dict:
    # pre: recibe una sigla de 4 letras y una string de 4 números
    # post: devuelve un dict con (o también, sacando las comillas de comentario, imprime en la pantalla) las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
    precondition = type(estacion) == type(anho) == str and estacion.isalpha() and len(estacion) == 4 and anho.isnumeric() and len(anho) == 4
    assert precondition, 'Error: temp_min_max() recibe el estación como string de 4 letras y el año como string de 4 números'

    # genera el archivo de datos:
    clima_anho(estacion,anho,1,12)

    temps_max = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100]
    temps_min = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    
    nombre = DIR + anho + '.txt'
    archivo = open(nombre,'r')

    for linea in archivo:
        # dia es un dict con una llave cuyo valor correspondiente es otro dict
        dia = ast.literal_eval(linea)
        # buscamos las temperaturas del día [max, min]
        max_min = max_min_del_dia(dia)

        # como dia sólo tiene 1 llave en el primer nivel, dia_llave es el primer elemento de una lista de 1 item (ej. ['20181222'])
        dia_llave = list(dia.keys())[0]
        indice_mes = int(dia_llave[4:6]) - 1

        if max_min[0] >= temps_max[indice_mes] and max_min[0] != None:
            temps_max[indice_mes] = max_min[0]

        if max_min[1] <= temps_min[indice_mes] and max_min[1] != None:
            temps_min[indice_mes] = max_min[1]

    archivo.close()

    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    # para imprimir los resultados en pantalla:
    '''
    header = "{0:13}{1:17}{2:15}"
    print(header.format("mes", "temp max (en ˚C)", "temp min (en ˚C)"))
    print(header.format("--------", "--------", "--------"))

    mes = 0
    while mes < 12:
        mes_nombre = meses[mes]
        max = temps_max[mes]
        min = temps_min[mes]
        resultados = "{0:<13}{1:<17}{2:<15}"
        print(resultados.format(mes_nombre, max, min))
        mes = mes + 1
    '''

    # para devolver los resultados en forma dict
    meses_max_min = {}
    indice_temps = 0
    for mes in meses:
        meses_max_min[mes] = {'max': temps_max[indice_temps], 'min': temps_min[indice_temps]}
        indice_temps = indice_temps + 1
    
    return meses_max_min

# Ejercicio 3 (ii):

def data_de_la_primavera(hemisferio: str):
  # pre: recibe string 'hemisferio' de una letra (y necesita acesso al archivo 2018.txt)
  # post: crea un archivo 2018p.txt con los datos correspondiente a la primavera del 2018
  precondition = hemisferio == 'n' or hemisferio == 's'
  assert precondition, 'Error: data_de_la_primavera() acepta "n" o "s" como argumento'

  data_anho = '2018.txt'
  data_primavera = '2018p.txt'

  datos = open(DIR + data_anho, 'r')
  archivo = open(DIR + data_primavera,'w')

  comienzo_primavera = ''
  fin_primavera = ''

  # elije el rango de las fechas de la primavera según el hemisferio de la ciudad elegido
  if hemisferio == 'n':
      comienzo_primavera = '20180321'
      fin_primavera = '20180621'
  else:
      comienzo_primavera = '20180921'
      fin_primavera = '20181221'

  # itera por los datos en 2018.txt, copiando los de la primavera a 2018p.txt
  for linea in datos:
      dia = ast.literal_eval(linea)
      dia_llave = list(dia.keys())[0]
      if comienzo_primavera <= dia_llave and dia_llave < fin_primavera:
          archivo.write(linea)

  archivo.close()
  datos.close()

def temp_max(estacion: str, mes_ini, mes_fin: int) -> float:
  # pre: recibe una sigla de 4 letras 'estacion', y dos numeros enteros entre 1 y 12 tal que mes_ini <= mes_fin
  # post: devuelve el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida como float (con opción para devolver un int en vez)
  precondition = type(estacion) == str and type(mes_ini) == type(mes_fin) == int and estacion.isalpha() and len(estacion) == 4 and 1 <= mes_ini <= mes_fin <= 12
  assert precondition, "Error: temp_max() recibe 3 parámetros: el estación como sigla de 4 letras, y 2 numeros, mes_inicial y mes_final, 1 <= mes_inicial <= mes_final <= 12"
    
  # si 2018.txt no estaba generado anteriormente (con temp_min_max()), hay que ejecutar lo siguiente:
  # clima_anho(estacion,'2018',mes_ini,mes_fin)

  # genera 2018p.txt de 2018.txt (si hace falta generar 2018.txt, ejecutar la línea justo arriba de esta)
  if (mes_ini == 3 or mes_ini == 4) and (mes_fin == 5 or mes_fin == 6):
      data_de_la_primavera('n')
  else:
      data_de_la_primavera('s')

  # itera por los datos de la primavera de 2018, agregando la temperatura máxima de cada día a la lista temps_de_la_primavera
  temps_de_la_primavera = []
  archivo = open(DIR + '2018p.txt','r')
  for linea in archivo:
      dia = ast.literal_eval(linea)
      max_min = max_min_del_dia(dia)
      temps_de_la_primavera.append(max_min[0])

  # promedia las máximas diarios
  dias_p = len(temps_de_la_primavera)
  sum_temps = 0
  for temp in temps_de_la_primavera:
      sum_temps = sum_temps + temps_de_la_primavera[temp]
  # promedio como float
  promedio = sum_temps / dias_p
  # promedio como int
  # promedio = sum_temps // dias_p

  archivo.close()
  return promedio

# Ejercicio 3 (iii):

def dir_viento(estacion, mes_ini, mes_fin):
  # pre: recibe una sigla de 4 letras 'estacion', y dos números enteros entre 1 y 12 tal que mes_ini <= mes_fin
  # post: devuelve la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida
  precondition = type(estacion) == str and type(mes_ini) == type(mes_fin) == int and estacion.isalpha() and len(estacion) == 4 and 1 <= mes_ini <= mes_fin <= 12
  assert precondition, "Error: dir_viento() recibe 3 parámetros: el estación como sigla de 4 letras, y 2 numeros, mes_inicial y mes_final, 1 <= mes_inicial <= mes_final <= 12"
    

  # si ya han sido generados 2018.txt (con temp_min_max()) y 2018p.txt (con temp_max()), no hace falta ejecutar el siguiente bloque:
  '''
  # si 2018.txt no estaba generado anteriormente (con temp_min_max()), hay que ejecutar lo siguiente:
  # clima_anho(estacion,'2018',mes_ini,mes_fin)

  # genera 2018p.txt de 2018.txt (si hace falta generar 2018.txt, ejecutar la línea justo arriba de esta)
  if (mes_ini == 3 or mes_ini == 4) and (mes_fin == 5 or mes_fin == 6):
      data_de_la_primavera('n')
  else:
      data_de_la_primavera('s')
  '''

  direcciones = {'Norte': 0, 'Nordeste': 0, 'Este': 0, 'Sureste': 0, 'Sur': 0, 'Suroeste': 0, 'Oeste': 0, 'Noroeste': 0, 'En calma': 0, 'Variable': 0}

  # itera por cada hora de cada día en 2018p.txt, sumando 1 en el dict direcciones a la dirección del viento encontrando
  archivo = open(DIR + '2018p.txt','r')
  for linea in archivo:
      dia = ast.literal_eval(linea)
      dia_llave = list(dia.keys())[0]
      horas = list(dia[dia_llave].keys())
      for hora in horas:
          viento = dia[dia_llave][hora]['dir']
          if viento != None:
              direcciones[viento] = direcciones[viento] + 1
  
  archivo.close()

  # itera por las direcciones, buscando la dirección correspondiende al número más alto
  direcciones_lista = list(direcciones.items())
  predominante = ''
  cuenta = 0
  for tupla in direcciones_lista:
      if tupla[1] > cuenta:
          cuenta = tupla[1]
          predominante = tupla[0]

  return predominante

# Resultados

# He probado con EHAM en Holanda y CWDK en Canada.
def main():
    estacion, anho = 'cwdk', '2018' # Claresholm
    clima_anho(estacion, anho, 1, 12)
    #todo_anho = temp_min_max('CWDK', '2018')
    #print('Las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida son (en ˚C):\n', todo_anho)
    #promedio = temp_max('CWDK', 3, 6)
    #print('El promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida es: ', promedio, '˚C')
    #viento = dir_viento('CWDK', 3, 6)
    #print('La dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida es: ', viento)

# RUN

if __name__ == '__main__':
    main()