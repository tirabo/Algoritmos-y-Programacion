import requests
from bs4 import BeautifulSoup
import json

CLAVES = ['hora', 'desc', 'temp', 'dir', 'vel', 'hum', 'pres'] 
DIR = './2021/tareas/schliamser/'

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


def formatear_fecha(fecha: str) -> str:
    # pre:    fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha    en el foma dia-nombre del mes-año
    anho = fecha[0:4]
    mes = fecha[4:6]
    dia = fecha[6:8]
    # la url no excluye n° de días de menos de 2 unidades, por lo que no hay que considerar el 0 de la entrada
    # para los días menores a 10
    if dia[0] == '0':
        str_dia = dia[1]
    else:
        str_dia = dia
    meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    nombre_fecha = str_dia + '-' + meses[int(mes)-1] + '-' + str(anho)
    return nombre_fecha


def eliminar_unidades(registro: dict):
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    
    nuevo_dict = registro.copy()
    nuevo_dict['temp'] = nuevo_dict['temp'].replace("°","")
    try:
        nuevo_dict['temp']=int(nuevo_dict['temp'])
    except:
        nuevo_dict['temp'] = None

    nuevo_dict['vel'] = nuevo_dict['vel'].replace("km/h","")
    try:
        nuevo_dict['vel']=int(nuevo_dict['vel'])
    except:
        nuevo_dict['vel'] = None

    nuevo_dict['hum'] = nuevo_dict['hum'].replace("%","")
    try:
        nuevo_dict['hum']=int(nuevo_dict['hum'])
    except:
        nuevo_dict['hum'] = None
    
    nuevo_dict['pres'] = nuevo_dict['pres'].replace("hPa","")
    try:
        nuevo_dict['pres']=int(nuevo_dict['pres'])
    except:
        nuevo_dict['pres'] = None
    return nuevo_dict



#definimos previamente la función es_bisiesto para verificar si corresponden 28 o 29 días en febrero para ese año
def es_bisiesto(anho: int) -> bool:
    #pre: recibe un entero como año
    #post: devuelve un booleano, True sí el año ingresado es bisiesto, False sí no lo es
    bisiesto_ok = anho % 4 == 0
    if bisiesto_ok : 
        if anho % 100 == 0:
            bisiesto_ok = anho % 400 == 0
    return bisiesto_ok


# redefinir 
def registros_dia(estacion: str, fecha: str) -> dict:
    # pre:    recibe la fecha como str del tipo 'AAAAMMDD' y la codificacion de la estacion para ingresar a la url de tutiempo
    # post: devuelve un diccionario    del tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    assert type(estacion)== str and fecha.isdigit() and len(fecha)==8, 'Ingrese una fecha con el formato "AAAAMMDD" formada por enteros'
    contenido_url = requests.get('https://www.tutiempo.net/registros/' + estacion + '/' + formatear_fecha(fecha) + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")
    registros_nuevos={}
    for i in range(24): #recorremos por hora cada url que nos brinda la info del día
        try: #por sí tenemos algun dato faltante, el diccionario contendrá None como valor testigo
            registros_nuevos[i] = eliminar_unidades(registros_tabla(tabla_dia)[i])
        except:
            registros_nuevos[i] = None
    return registros_nuevos


#la función clima_anho a diferencia de la implementada en la celda anterior escribirá 
#el archivo también con el mes para poder implementar las funciones siguientes
def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre:    recibe str anho como 'AAAA', str 'estacion' y mes_ini y mes_fin como int
    # post: devuelve un diccionario    del tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015},
    # por hora en la misma línea y por día en diferentes. Se almacena en un archivo 'AAAAMM.txt'
    precondicion_anho = anho.isdigit() and len(anho)==4
    precondicion_mes = type(mes_ini)==type(mes_fin)== int and mes_ini <= mes_fin and mes_fin <13 and mes_ini >0
    assert    precondicion_anho and precondicion_mes, 'Ingrese año como str "AAAA" de cuatro cifras enteras y meses válidos como enteros, siendo mes_fin >= mes_ini'
    dias=[31,28,31,30,31,30,31,31,30,31,30,31]
    if es_bisiesto(int(anho)):
        dias[1] = 29
    datos= anho+str(mes_ini)+'.txt'
    file0 = open(DIR + datos, 'w')
    
    for mes in range(mes_ini,mes_fin+1):
        if mes <10:
            st_mes = '0'+str(mes)
        else:
            st_mes=str(mes)
        for dia in range(dias[mes-1]):
            if dia <9:
                st_dia = '0'+str(dia+1)
            else:
                st_dia=str(dia+1)
            fecha = str(anho)+st_mes+st_dia                 
            file0.write(json.dumps(registros_dia(estacion,fecha))+'\n')


def temp_min_max(estacion, anho):
    #pre: la función recibe dos str: 'estacion' y 'anho'
    #post: devuelve un diccionario del tipo:{'mes': {'temp_max': int, 'temp_min': int}
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    
    dict_total={} #este diccionario almacenará como clave principal el mes, dentros del mes dos claves de
    #temp_max y temp_min y como valores la temp. máx. y mín. respectivamente
    for j in range(12):
        dict_mes={}
        lista_temp=[] #lista auxiliar para guardar las temperaturas del mes recorrido
        dict={}
        # registros = clima_anho(estacion,anho,j+1,j+1) # Corrección: no deben generarse los archivos cada vez que se corre esta función. Después de correr una vez la función deberías comentar la linea y eso no es muy práctico. La generación de archivos debe hacerse antes.  Fijate que además la variable registro no la usás.
        file0 = open(DIR + anho+str(j+1)+'.txt', 'r')
        linea = file0.readline()
        i=0
        while linea:
            
            dict_mes[i] = json.loads(linea)
            for hora in range(24):
                if dict_mes[i][str(hora)]!=None: #debemos chequear sí hay info o no en la hora. De no haber, el programa continuará con otra línea
                    if dict_mes[i][str(hora)]['temp'] !=None: #debemos chequear sí hay info o no en la clave 'temp'. De no haber, el programa continuara con otra línea
                        lista_temp.append(dict_mes[i][str(hora)]['temp'])
            linea = file0.readline()
            i+=1
            
        dict['temp_max']= max(lista_temp)
        dict['temp_min']= min(lista_temp)
        dict_total[meses[j]] = dict
    print(dict_total)
    return dict_total


def temp_max(estacion, mes_ini, mes_fin):
    #pre: la función recibe un str 'estacion' y dos enteros 'mes_ini' y 'mes_fin', 
    #para los fines de esta función deberían ser mes inicial y final de la primavera
    #post: la función devuelve un entero que representa el promedio de las temp. max de la primavera, y lo imprime en pantalla
    meses_primavera = [3,4,5,6]
    temp_max = [] #lista que almacenará las temperaturas máximas diarias
    for k in meses_primavera:
        #registros = clima_anho(estacion,'2018',k,k) Se comenta esta línea para aprovechar la implementación de la función anterior
        #y los archivos ya generados
        dict_mes={} #diccionario donde se decodificará cada archivo (por mes)
        file0 = open(DIR + '2018'+str(k)+'.txt', 'r')
        linea = file0.readline()
        i=0 #índice del diccionario donde se decodificarán los archivos
        while linea:
            dict_mes[i] = json.loads(linea)
            temp_dia=[] #lista que almacenará las temperaturas del día
            for hora in range(24):
                if dict_mes[i][str(hora)]!=None: #verificamos que haya datos en esa hora
                    if dict_mes[i][str(hora)]['temp'] !=None: #verificamos que haya un valor de temperatura no nulo
                        temp_dia.append(dict_mes[i][str(hora)]['temp'])
            if k==3 and i>=21: #la primavera en Kaliningrado comienza el 21/3
                temp_max.append(max(temp_dia))
            elif k!=3 and k!=6:
                temp_max.append(max(temp_dia))
            elif k==6 and i<21:#la primavera en Kaliningrado finaliza el 21/6
                temp_max.append(max(temp_dia))
            i+=1
            linea = file0.readline()
    promedio= sum(temp_max)/len(temp_max)
    
    print(f'El promedio de temperaturas máximas diarias en primavera es: {promedio:0.2f} °C')
    return promedio


def dir_viento(estacion, mes_ini, mes_fin):
    #pre: la función recibe un str 'estacion' y dos enteros 'mes_ini' y 'mes_fin', 
    #para los fines de esta función deberían ser mes inicial y final de la primavera
    #post: la función devuelve un str con la dirección del viento predominante y lo imprime en pantalla.
    meses_primavera = [3,4,5,6]
    direcciones = [] #lista que almacenará todos los registros de dirección de viento
    for k in meses_primavera:
        #registros = clima_anho(estacion,'2018',k,k) Se comenta esta línea para aprovechar la implementación de la función anterior
        #y los archivos ya generados
        dict_mes={}#diccionario donde se decodificará cada archivo (por mes)
        file0 = open(DIR + '2018'+str(k)+'.txt', 'r')
        linea = file0.readline()
        i=0 #índice del diccionario donde se decodificarán los archivos
        while linea:
            dict_mes[i] = json.loads(linea)
            
            for hora in range(24):
                if dict_mes[i][str(hora)]!=None:#verificamos que haya datos en esa hora
                    if dict_mes[i][str(hora)]['dir'] !=None: #verificamos que haya datos de dirección de viento
                        if k==3 and i>=21:#la primavera en Kaliningrado comienza el 21/3
                            direcciones.append(dict_mes[i][str(hora)]['dir'])
                        elif k!=3 and k!=6:
                            direcciones.append(dict_mes[i][str(hora)]['dir'])
                        elif k==6 and i<21:#la primavera en Kaliningrado finaliza el 21/6
                            direcciones.append(dict_mes[i][str(hora)]['dir'])
            i+=1
            linea = file0.readline()
    direccion = (max(set(direcciones), key=direcciones.count)) #este método nos permite obtener el valor más repetido en una lista
    
    print(f'La dirección predominante del viento en primavera es: {direccion}')
    return direccion


def main():
    # clima_anho('umkk','2018', 1, 12)
    print('Probando temp_min_max')
    temp_min_max('umkk','2018')
    print('Probando temp_max')
    temp_max('umkk',3,6)
    print('Probando dir_viento')
    dir_viento('umkk',3,6)

# RUN

if __name__ == '__main__':
    main()

