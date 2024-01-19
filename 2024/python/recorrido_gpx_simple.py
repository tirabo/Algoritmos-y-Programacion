import numpy as np
from xml.dom import minidom
from  math import *
from dateutil.parser import parse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

R = 6371000 # radio terrestre en metros
PI = np.pi # el pi de numpy

def leer_gpx(nombre: str):
    # pre: nombre es el archivo a ser leido (poner path completo ./bicicleta/gpx/altas_cumbres.gpx, por ejemplo)
    # post: devuelve una lista de 3-uplas (latitud, longitud,  elevacion)
    recorrido = []
    lat, lon, ele = np.array([]), np.array([]), np.array([]) # datos obligatorios
    # Parsear el documento
    doc = minidom.parse(nombre)
    # getElementsByTagName() devuelve una lista de
    # elementos con el nombre dado. Aquí <trkpt>
    for ubicacion in doc.getElementsByTagName('trkpt'):
        # getAttribute() devuelve un valor asociado a una clave dada
        # dentro de una etiqueta.
        latitud =  radians(float(ubicacion.getAttribute('lat')))
        longitud = radians(float(ubicacion.getAttribute('lon')))
        # 1. De nuevo getElementsByTagName() devuelve una lista.
        # 2. Usamos sólo el primer elemento de la lista ([0]).
        # 3. De ahí obtenemos el primer hijo (puede ser un nodo de datos
        # u otro elemento)
        # 4. Del nodo de datos obtenemos los datos reales
        elevacion =  float(ubicacion.getElementsByTagName('ele')[0].firstChild.data)
        # latitud, longitud, elevacion son obligatorios en el archivo gpx
        lat = np.append(lat, latitud)
        lon = np.append(lon, longitud)
        ele = np.append(ele, elevacion)
    return  (lat, lon, ele)


def distancia(punto1, punto2):
    # pre:  punto1 y punto2 son coordenadas de dos puntos en radianes y su elevación en metros.
    # post: distancia entre los dos puntos en metros
    lat1, lon1, ele1 = punto1[0], punto1[1], punto1[2]
    lat2, lon2, ele2 = punto2[0], punto2[1], punto2[2]
    dif_ele = ele2 - ele1
    dist_plana = R*acos(cos(lat1)*cos(lat2)*cos(lon1-lon2) + sin(lat1)*sin(lat2)) # en metros 
    return  (dist_plana**2 + dif_ele**2)**0.5


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

    # archivo_gpx = 'Ascochinga_MTB.gpx'
    archivo_gpx = 'Punilla_MTB.gpx'
    # archivo_gpx = 'Punilla_Observatorio.gpx'
    lectura_gpx = leer_gpx('./2023/archivos/' +  archivo_gpx)
    latitud, longitud, elevacion = lectura_gpx[0], lectura_gpx[1], lectura_gpx[2]
    recorrido = recorrido_proc(latitud, longitud, elevacion)
    latitud, longitud, elevacion, distancia, pendiente = recorrido[0], recorrido[1], recorrido[2], recorrido[3], recorrido[4]


    # Grafiquemos el recorrido animado
    # Si lo hacemos con todos los puntos será muy lento 
    velocidad_de_animacion = 5 # cada velocidad_de_animacion  puntos se muestra uno
    # Configuración de la figura y el eje
    indices = np.arange(0, len(longitud), velocidad_de_animacion)
    lon_new, lat_new = longitud[indices], latitud[indices]

    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_xlim(np.min(lon_new), np.max(lon_new))
    ax.set_ylim(np.min(lat_new), np.max(lat_new))

    # Función de actualización de la animación
    def update(frame):
        x = lon_new[:frame+1]
        y = lat_new[:frame+1]
        line.set_data(x, y)
        return line,

    # Función de inicialización de la animación
    def init():
        line.set_data([], [])
        return line,

    # Creación de la animación
    ani = FuncAnimation(fig, update, frames=len(lon_new), init_func=init, blit=True)

    # Mostrar la animación
    plt.show()


if __name__ == '__main__':
    main()