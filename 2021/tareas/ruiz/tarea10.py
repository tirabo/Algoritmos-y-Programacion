import requests
from bs4 import BeautifulSoup
import json

DIR = './2021/tareas/ruiz/'
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
    # pre:  fecha es una fecha en el formato 'AAAAMMDD'
    # post: devuelve la fecha  en el foma dia-nombre del mes-año
    meses= {'01':'enero','02':'febrero','03':'marzo','04':'abril','05':'mayo','06':'junio','07':'julio','08':'agosto','09':'septiembre','10':'octubre','11':'noviembre','12':'diciembre'}
    mes= meses[fecha[4:6]]
    return fecha[6:] + '-' + mes + '-' + fecha[:4]

def eliminar_unidades(registro: dict):
    # pre:    recibe un diccionario tipo    {'desc': 'Despejado', 'temp': '13°', 'dir': 'Noroeste', 'vel': '7 km/h', 'hum': '88%', 'pres': '1015 hPa'}
    # post: modifica el propio diccionario tipo     {'desc': 'Despejado', 'temp': 13, 'dir': 'Noroeste', 'vel': 7, 'hum': 88, 'pres': 1015}
    unidades = {'temp': '°', 'vel': 'km/h', 'hum':'%', 'pres':'hPa'}
    claves = unidades.keys() #temp, vel, hum, pres
    registro_recibido= registro

    #convierto los valores de los diccionarios en listas
    for valor in claves: 
        valor_tomado = list(registro_recibido[valor])    #toma el valor de la clave (ejemplo : 13°)
        unidad = list(unidades[valor])                #crea una lista de las unidades por quitar
        for caracter in unidad:
            valor_tomado.remove(caracter)     #Elimino los caracteres de unidad de los valores

        valor_tomado = ''.join(valor_tomado)
        registro_recibido.update({valor: valor_tomado}) #actualizo diccionario
    
    return registro_recibido


def cantidad_dias(mes,anho:str):
    # post:devuelve la cantidad de dias 
    meses= {'00': 30,'01': 31,'02': 28 ,'03': 29} # {mes(abril , junio , agosto , noviembre) : cantidad de dias que le corresponde (30), ...}
    if mes == '02': #si es febrero
        if int(anho) % 4 == 0 and (int(anho) % 100 == 0 or int(anho) % 400 != 0 ) == True: #si es bisiesto
            dias=meses['03']
        else: dias=meses['02']
    elif mes== '04' or mes== '06' or mes== '08' or mes== '11': #si es abril , junio , agosto , noviembre
        dias=meses['00']
    else: #los meses que quedan
        dias=meses['01']
    return int(dias)


def formato_str(n:int):
    if len(str(n)) == 1: # veo los digitos para poder respetar el formato 'MM'
        formato='0'+ str(n)
    else: 
        formato=str(n)
    return formato


def registros_dia2(fecha: str) -> dict: #misma funcion pero sin eliminar unidades
    tabla={}
    contenido_url = requests.get('https://www.tutiempo.net/registros/saco/' + formatear_fecha(fecha) + '.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")

    horas = registros_tabla(tabla_dia).keys()
    for i in horas: #me aseguro que agrero hora que si esten en los datos del programa
        tabla[i]=registros_tabla(tabla_dia)[i]

    return tabla


# redefinir 
def registros_dia(estacion: str, fecha: str) -> dict:
    tabla={}
    contenido_url = requests.get('https://www.tutiempo.net/registros/'+estacion+'/'+formatear_fecha(fecha)+'.html')
    contenido_estructurado = BeautifulSoup(contenido_url.text, 'lxml') # parsea la página 
    tabla_dia = contenido_estructurado.find('table', {'style': 'width: 100%'}) # extrae la tabla (es la única con style="width: 100%")

    horas = registros_tabla(tabla_dia)
    for i in horas: 
        tabla[i]=registros_tabla(tabla_dia)[i]
    return tabla


def clima_anho(estacion: str, anho: str, mes_ini: int, mes_fin: int):
    # pre: mes_ini <= mes_fin
    # post :Guarda en el archivo 'AAAA.txt', en cada renglón, los datos del clima de cada día en Córdoba desde mes_ini hasta el mes_fin
        assert mes_ini <= mes_fin, 'Error, no cumple que mes_ini <= mes_fin' 
        mes = mes_ini 
        dias= cantidad_dias(mes,anho)
        
        archivo = open(DIR + anho +'.txt','w')
        while mes <= mes_fin:
            mes_str = formato_str(mes)
            for dia in range(1,cantidad_dias(mes_str,anho) +1): #paso por todos los dias del correspondiente mes
                fecha = anho + mes_str + str(dia) #formato que entiende TuTiempo
                toma_datos = registros_dia(estacion,fecha)
                dia_completo = {fecha :toma_datos} # diccionario de diccionario con la fecha y los datos tomados
                archivo.write(json.dumps(dia_completo) + '\n') 
            mes=int(mes) + 1
        archivo.close()


#CREO UN ARCHIVO ANUAL DE TODOS LOS REGISTROS RECIBIDOS 
def archivo_anual(estacion:str, anho:str, mes_ini:int, mes_fin:int):    # Corregir: ¿qué sentido tiene esta función? es igual a clima_anho()
    # post: devuelve el archivo anual del lugar elegido
    clima_anho(estacion, anho, mes_ini, mes_fin) # Corregir:    está mal escrito el parámetro anho


#Obtener las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
def temp_min_max(estacion, anho):
    mes_str= {1:'enero', 2:'febrero', 3:'marzo',4:'abril',5:'mayo',6:'junio',7:'julio',8:'agosto',9:'septiembre',10:'octubre',11:'noviembre',12:'diciembre'}
    archivo= open(DIR + anho +'.txt', 'r')
    registro_dias_anho=[]

    for linea in archivo: 
        registro_dias_anho.append(json.loads(linea))    #lista en la que cada elemento es un dia
    meses = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]} #temperaturas por mes
    for i in range(len(registro_dias_anho)):                #recorre los meses
        for fecha in registro_dias_anho[i].keys():        #recorre dia por dia
            horas= registro_dias_anho[i][fecha]    #diccionario con horas
            mes= int(fecha[4:6])
            for hora in horas.keys():        #recorro las horas
                temperatura= horas[hora]['temp'].replace('°','') #saco unidades para poder comparar 
                meses[mes].append(temperatura.strip())
    
    #Busco los maximos y minimos
    for i in range(1 , 12 + 1 ):
        if len(meses[i]) != 0 : #por si no estan los datos
            maximo=max(meses[i])
            minimo=min(meses[i])
            print('Temperatura máxima de '+ mes_str[i] +' es: '+ maximo +'°')
            print('Temperatura minima de '+ mes_str[i] +' es: '+ minimo +'°'+'\n')
    archivo.close()    

#Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida
def temp_max(estacion, mes_ini, mes_fin):
    # archivo= open(anho+'.txt', 'r') # Corregir: anho no está definido
    maximo = -100 # Agregado por mi para que pylance no chille
    archivo= open(DIR + '2018'+'.txt', 'r') # Agregado por mi 
    registro_dias_anho=[]
    for linea in archivo: 
        registro_dias_anho.append(json.loads(linea))    #lista en la que cada elemento es un dia 
    dias = {}        #temperaturas por dia
    for i in range(len(registro_dias_anho)): #recorre los meses
        for fecha in registro_dias_anho[i]:        #recorre dia por dia
            horas= registro_dias_anho[i][fecha]    #diccionario con horas
            mes=int(fecha[4:6])
            dia= int(fecha[6:])
            dias[fecha]=[] #temperaturas de primavera
            if (mes == 9 and dia >= 22) or mes == 10 or mes == 11 or (mes == 12 and dia <=21):
                for hora in horas:        
                        temperatura= horas[hora]['temp'].replace('°','') #saco unidades para poder comparar
                        dias[fecha].append(temperatura.strip())     #temperaturas en primavera
            else:
                del dias[fecha]
    #Saco el promedio de la temperatura maxima de primavera
    suma_max=0
    for dia in dias:        #recorro dia por dia buscando maximo
            maximo=max(dias[dia])
            if maximo != 'N/D':
                suma_max= suma_max + int(maximo)
    # promedio= suma_max // len(dias) # Corregir: los promedios no se hacen con división entera
    # print('El promedio de la temperatura maxima en primavera fue de: '+ maximo +'°' +'\n') # Corregir: no se puede concatenar str e int. No se debe poner maximo sino promedio.
    promedio= suma_max / len(dias) # Agregada por mi
    print('El promedio de la temperatura máxima en primavera fue de: '+ str(promedio) +'°' +'\n') # Agregada por mi
    archivo.close()


#Calcular la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.
def dir_viento(estacion, mes_ini, mes_fin):
    direccion = ''
    viento = '' # Agregada por mi para que pylance no chille
    # archivo= open(anho +'.txt', 'r') # Corregir: anho    no está definido    
    archivo= open(DIR + '2018' +'.txt', 'r')
    registro_dias_anho=[]
    #Guardo los diccionarios del archivo en una lista en la que cada elemento es un dia 
    for linea in archivo: 
        registro_dias_anho.append(json.loads(linea))
    #Guardo todas las direcciones por mes
    dias = {} 
    for i in range(len(registro_dias_anho)): #recorre los meses
        for fecha in registro_dias_anho[i]:        #recorre dia por dia
            horas= registro_dias_anho[i][fecha]    #diccionario con horas
            mes=int(fecha[4:6])
            dia= int(fecha[6:])
            dias[fecha]=[] #temperaturas de primavera
            if (mes == 9 and dia >= 22) or mes == 10 or mes == 11 or (mes == 12 and dia <=21):
                for hora in horas:        
                        direccion= horas[hora]['dir'].replace('°','') #saco unidades para poder comparar
                        dias[fecha].append(direccion.strip())     #temperaturas en primavera
            else:
                del dias[fecha] #elimino si no es de primavera
    direccion_viento_total=[]
    for dia in dias:        
        direccion_viento_total= direccion_viento_total + dias[dia] #guardo todos las direcciones del viento
    #Saco el promedio de la dirrecion de viento durante la primavera
    dic_viento=[]    #nombre de la direcciones del viento ('Sur', ...)
    repeticion=[]    #veces que los nombres de las direcciones del vientos se repiten 
    for viento in direccion_viento_total:
        if viento not in dic_viento:
            dic_viento.append(viento)     
            repeticion.append(direccion_viento_total.count(viento))
    viento_predomina = dic_viento[direccion.index(max(viento))] #busco la repeticion que se encuntra el nombre del viento
    print('Predomina en primavera el viento de dirección: '+ viento_predomina)
    archivo.close()





def main():
    # Resultados
    #CREO UN ARCHIVO ANUAL DE TODOS LOS REGISTROS RECIBIDOS 
    #Datos:
    estacion = 'sbrj' # Brasil, Rio de Janeiro
    anho = '2018'
    mes_ini = 1
    mes_fin = 12
    # archivo_anual(estacion, anho ,mes_ini , mes_fin)
    
    #Obtener las temperaturas máximas y mínimas de cada mes del año 2018 de la ciudad elegida.
    temp_min_max(estacion , anho)
    #Calcular el promedio de temperaturas máximas diarias durante la primavera del año 2018 en la ciudad elegida
    #Datos:  Primavera (22 de septiembre hasta 21 de diciembre)
    mes_ini = 9
    mes_fin = 12  
    temp_max(estacion, mes_ini,mes_fin)
    #Calcular la dirección del viento predominante durante la primavera del año 2018 en la ciudad elegida.
    #Datos:  Primavera (22 de septiembre hasta 21 de diciembre)
    mes_ini = 9
    mes_fin = 12  
    dir_viento(estacion, mes_ini, mes_fin)
    

# RUN

if __name__ == '__main__':
    main()