# Lectura y análisis de gpx
from math import *
from xml.dom import minidom
import numpy as np
from scipy import interpolate
from scipy import signal
import matplotlib.pyplot as plt
import os
from dateutil.parser import parse

R = 6371000 # radio terrestre en metros
PI = pi

def distancia(punto1, punto2):
    # pre:  punto1 y punto2 son coordenadas de dos puntos en radianes y su elevación en metros.
    # post: distancia entre los dos puntos en metros
    lat1, lon1, ele1 = punto1[0], punto1[1], punto1[2]
    lat2, lon2, ele2 = punto2[0], punto2[1], punto2[2]
    dif_ele = ele2 - ele1
    dist_plana = R*acos(cos(lat1)*cos(lat2)*cos(lon1-lon2) + sin(lat1)*sin(lat2)) # en metros 
    return  (dist_plana**2 + dif_ele**2)**0.5


def leer_gpx(nombre: str):
    # pre: nombre es el archivo a ser leido (poner path completo ./bicicleta/gpx/altas_cumbres.gpx, por ejemplo)
    # post: devuelve una lista de 3-uplas (latitud, longitud,  elevacion)
    recorrido = []
    lat, lon, ele = np.array([]), np.array([]), np.array([]) # datos obligatorios
    time, temp, heart_rate, cadence = np.array([]), np.array([]), np.array([]), np.array([]) # datos opcionales (solo si es un recorrido realizado)
    # Parse the document
    doc = minidom.parse(nombre)
    # getElementsByTagName() returns a list of
    # elements with the given name. Here <trkpt>
    for ubicacion in doc.getElementsByTagName('trkpt'):
        # getAttribute() returns a value associated with a given key
        # within a tag. Here <species name='xxxxx'>
        latitud =  radians(float(ubicacion.getAttribute('lat')))
        longitud = radians(float(ubicacion.getAttribute('lon')))
        # 1. Again getElementsByTagName() returns a list.
        # 2. We use just the first element of the list ([0]).
        # 3. From that we obtain the first child (could be a data node
        # or another element)
        # 4. From the data node we obtain the actual data
        # Here: <common-name>xxxx</common-name>
        elevacion =  float(ubicacion.getElementsByTagName('ele')[0].firstChild.data)
        # latitud, longitud, elevacion son obligatorios en el archivo gpx
        lat = np.append(lat, latitud)
        lon = np.append(lon, longitud)
        ele = np.append(ele, elevacion)

        # OPCIONALES: hora, temperatura ambiente, ritmo cardiaco y cadencia son opcionales (solo aparecen estos datos en recorridos realizados)
        data =  ubicacion.getElementsByTagName('time')
        if len(data) > 0:
            date_str = data[0].firstChild.data
            time_epoch = int(parse(date_str).timestamp()) # convierte "2023-02-16T19:18:18.000Z" a segundos desde 1970
            time = np.append(time,time_epoch)
        else:
            time = np.append(time, np.nan)
        if len(ubicacion.getElementsByTagName('ns3:atemp')) > 0:
            temp = np.append(temp, float(ubicacion.getElementsByTagName('ns3:atemp')[0].firstChild.data))
        else:
            time = np.append(temp, np.nan)
        if len(ubicacion.getElementsByTagName('ns3:hr')) > 0:
            heart_rate = np.append(heart_rate, float(ubicacion.getElementsByTagName('ns3:hr')[0].firstChild.data))
        else:
            heart_rate = np.append(heart_rate, np.nan)
        if len(ubicacion.getElementsByTagName('ns3:cad')) > 0:
            cadence = np.append(cadence, float(ubicacion.getElementsByTagName('ns3:cad')[0].firstChild.data))
        else:
            cadence = np.append(cadence, np.nan)
        # FIN OPCIONALES
    
    # ELIMINAMOS PUNTOS A DISTANCIA PLANA = 0 
    lat_n, lon_n, ele_n = np.array([lat[0]]), np.array([lon[0]]), np.array([ele[0]])
    time_n, temp_n, heart_rate_n, cadence_n = np.array([time[0]]), np.array([temp[0]]), np.array([heart_rate[0]]), np.array([cadence[0]])
    for i in range(1, len(lat)):
        if R*acos(cos(lat[i-1])*cos(lat[i])*cos(lon[i-1]-lon[i]) + sin(lat[i-1])*sin(lat[i])) != 0:
            lat_n = np.append(lat_n, lat[i])
            lon_n = np.append(lon_n, lon[i])
            ele_n = np.append(ele_n, ele[i])
            time_n = np.append(time_n, time[i])
            temp_n = np.append(temp_n, temp[i])
            heart_rate_n = np.append(heart_rate_n, heart_rate[i])
            cadence_n = np.append(cadence_n, cadence[i])
    return  (lat_n, lon_n, ele_n, time_n, temp_n, heart_rate_n, cadence_n)


def recorrido_proc(lat, lon, ele):
    # pre: recorrido es una lista de ternas de (latitud, longitud, elevacion)
    # post: devuelve una 5-upla (latitud, longitud, elevacion, distancia, pendiente) donde 
    #       - distancia en una coordenada es la distancia total desde el origen hasta ese punto
    #       - pendiente es el % de elevación entre ese punto y el anterior (la primera es 0.0)
    dis, pen = np.array([0]), np.array([0])
    distancia_total = 0
    for i in range(1, len(lat)):
        # distancia total
        dist = distancia((lat[i-1], lon[i-1], ele[i-1]), (lat[i], lon[i], ele[i]))
        distancia_total += dist
        dis = np.append(dis, distancia_total)
        # pendiente
        dist_plana = R*acos(cos(lat[i-1])*cos(lat[i])*cos(lon[i-1]-lon[i]) + sin(lat[i-1])*sin(lat[i]))
        pendiente = 100 * (ele[i] - ele[i-1]) / dist_plana
        pen = np.append(pen, pendiente)
    return lat, lon, ele, dis, pen


def declive_acumulado_positivo(elevacion):
    # pre: elevacion es un array numpy con los datos de altura en cada punto del recorrido (interpolados)
    # post: devuelve el declive acumulado positivo
    declive_acumulado = 0
    for i in range(1, len(elevacion)):
        if elevacion[i] - elevacion[i-1] > 0:
            declive_acumulado += elevacion[i] - elevacion[i-1] 
    return declive_acumulado


def main():
    print('directorio actual:', os.getcwd())
    # lectura_gpx = leer_gpx('./bicicleta/gpx/Ascochinga_MTB.gpx')
    lectura_gpx = leer_gpx('./bicicleta/gpx/Punilla_Observatorio.gpx')
    latitud, longitud, elevacion = lectura_gpx[0], lectura_gpx[1], lectura_gpx[2]
    time, temp, heart_rate, cadence = lectura_gpx[3], lectura_gpx[4], lectura_gpx[5], lectura_gpx[6]
    # latitud, longitud, elevacion = 
    nro_puntos = len(latitud)
    print('Número de puntos de la muestra:', nro_puntos)
    # print('puntos 0', len(recorrido))
    # for ubicacion in recorrido:
    #     print(ubicacion)
    """
    rec_proc = recorrido_proc(recorrido)
    print('puntos 1',len(rec_proc))
    # for i in range (1, 100):
    #     print(rec_proc[i])
    with open('./bicicleta/datos.txt', 'w') as file:
        for punto in rec_proc:
            file.write(str(punto)+'\n')
    lat, lon, ele, dis, dec = recorrido_np(rec_proc)
    """
    lat, lon, ele, dis, dec = recorrido_proc(latitud, longitud, elevacion)
    print('Número de puntos de la muestra procesada:', len(lat))
    print('Declive acumulado positivo:', int(declive_acumulado_positivo(ele)), 'metros.')

    # for i in range(len(dis)):
    #     print(dis[i],dec[i])
    x, y = dis, ele # distancia, elevación
    # x, y = dis, dec # distancia, declive

    # LA MEJOR
    # https://docs.scipy.org/doc/scipy/tutorial/interpolate/smoothing_splines.html
    tck = interpolate.splrep(x, y, s = 0) # es mejor suavidad 0 para y = altura
    x_new = np.linspace(x.min(), x.max(), int(nro_puntos * 1.2))
    y_new = interpolate.splev(x_new, tck, der=0)
    print('Declive acumulado positivo corregido:', int(declive_acumulado_positivo(y_new)), 'metros.')
    mask = (~np.isnan(cadence)) & (cadence > 0) # para sacar los NaN y los 0 (esto indica cuando hay movimiento)
    print('La cadencia promedio:', int(np.mean(cadence[mask])), 'rpm.')
    mask_ht = (~np.isnan(heart_rate))  # para sacar los NaN 
    print('La frecuencia cardiaca promedio:', int(np.mean(heart_rate[mask_ht])), 'bpm.')
    dif_dis, dif_time = np.diff(dis[mask]), np.diff(time[mask]) # ver si está bien
    print('La velocidad promedio (en movimiento):', round(3.6 * np.mean(dif_dis / dif_time),1), 'km/h.')  # ver si está bien
    print('El tiempo total:', round((time[-1] - time[0]) / 3600,2), 'horas.')
    print('El tiempo total en movimiento:', round(np.sum(dif_time) / 3600,2), 'horas.') # no está bien
    plt.plot(x, y, '.', label='Datos originales')
    # plt.plot(x, heart_rate, label='Frecuencia cardiaca')
    # plt.plot(x, cadence, label='Cadencia')
    plt.plot(x_new, y_new, label='Curva ajustada')
    plt.legend()
    plt.show()
# Para ver métodos de suavizado: https://pythonguia.com/suavizado-python-scipy/


if __name__ == '__main__':
    main()
