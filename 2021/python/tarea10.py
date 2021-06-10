import json
import requests
from bs4 import BeautifulSoup


CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 


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
    if len(registro) != 0:
        eliminar_unidades(registro)
    return registro


def registros_tabla(tabla) -> dict:          # procesa una tabla 'bs4.element.Tag', devuelve un diccionario de registros contenidos en esa tabla
    registros = {}
    if tabla != None:
        for fila_tabla in tabla.findAll('tr'):
            registro = registro_fila_tabla(fila_tabla)
            if len(registro) != 0:
                hora = registro.pop('hora')
                hh = int(hora[:2])
                registros[hh] = registro
    return registros


def formatear_fecha(fecha: str) -> str:
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    fecha_formateada = ''
    # Insertar código
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    anho, mes, dia = int(fecha[:4]), int(fecha[4:6]), int(fecha[6:])
    mes = meses[mes - 1]
    fecha_formateada = str(dia) + '-' + mes + '-' + str(anho)
    return fecha_formateada


def eliminar_unidades(registro: dict):
    # pre:  recibe un diccionario tipo  {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo   {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    temperatura = registro['temp'].replace('°','').strip()
    registro['temp'] = int(temperatura) if len(temperatura) <= 2 else None
    velocidad = registro['vel'].replace('km/h','').strip()
    registro['vel'] = int(velocidad) if len(velocidad) <= 3 else None
    humedad = registro['hum'].replace('%','').strip()
    registro['hum'] = int(humedad) if len(humedad) <= 3 and humedad != 'N/D' else None
    presion = registro['pres'].replace('RMK', '').replace('hPa','').strip()
    registro['pres'] = int(presion) if 3 <= len(presion) <= 4 else None
    # Insertar código


def registros_dia(estacion, fecha: str) :
    # 
    nombre_fecha = formatear_fecha(fecha)
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+estacion+'/' + nombre_fecha + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    return registros_tabla(tabla_dia)


def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    pass # insertar código
    n_anho = str(anho)
    mes_dia = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    datos = open(n_anho + '.txt', 'w')
    for i in range(mes_ini - 1, mes_fin):
        for j in  range(mes_dia[i]):
            fecha = n_anho + '{:02}'.format(i+1) + '{:02}'.format(j+1)
            print(fecha)
            dia = registros_dia(estacion, fecha)
            fecha_dia = {fecha : dia}
            datos.write(json.dumps(fecha_dia) + '\n')
    datos.close()


# Obtener las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
def temp_min_max(anho):
    f = open(anho + '.txt', 'r')
    periodo = {}
    for dia in f:
        dic_dia = json.loads(dia)
        for w in dic_dia.keys():
            periodo[w] = dic_dia[w] 
    f.close()

    mes_dia = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    t_min, t_max, t_prom = [], [], []
    for i in range(12):
        t_min_mes, t_max_mes, t_prom_mes = 1000.0, -1000.0, 0
        cont = 0
        for j in  range(mes_dia[i]):
            fecha = str(anho) + '{:02}'.format(i+1) + '{:02}'.format(j+1)
            if fecha in periodo.keys():
                dia = periodo[fecha]
                for h in range(24):
                    clave = str(h)
                    if clave in dia.keys() and dia[clave]['temp'] != None:
                        t_min_mes = min(t_min_mes, dia[clave]['temp'])
                        t_max_mes = max(t_max_mes, dia[clave]['temp'])
                        t_prom_mes, cont = t_prom_mes + dia[clave]['temp'], cont + 1
        if t_min_mes == 1000.0:
            t_min.append(None)
        else:             
            t_min.append(t_min_mes)
        if t_max_mes == -1000.0:
            t_max.append(None)
        else:
            t_max.append(t_max_mes)
        if cont == 0:
            t_prom = None
        else:
            t_prom.append(round(t_prom_mes / cont, 1))
    return (t_min, t_max, t_prom)


    


# Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida.
def temp_max(estacion, mes_ini, mes_fin):
    pass

# Calcular la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.
def dir_viento(estacion, mes_ini, mes_fin):
    pass


def main():
    #dia = registros_dia('saco', '20150506')
    #print(dia)
    #print(json.dumps(dia))
    #clima_anho('saco', '2018', 1,12)
    (t_min, t_max, t_prom) = temp_min_max('2018')
    print('Temperaturas mínimas:', t_min)
    print('Temperaturas máximas:', t_max)
    print('Temperaturas promedio:', t_prom)


# RUN

if __name__ == '__main__':
    main()