# -*- coding: utf-8 -*-
import requests
from wordcloud import WordCloud

def bajar_libro(url, titulo):
    response = requests.get(url)
    texto = response.text
    k_ini, k_fin = texto.find(titulo), test.find('FIN')
    texto = texto[k_ini:k_fin]
    return  texto

def formatear_texto(texto):
    texto_min = texto.lower()
    caracteres = "(),._:;-'[]¡¿!?*$%&/#\""
    for x in range(len(caracteres)):
        texto_min = texto_min.replace(caracteres[x],"")
    return texto_min

def check_freq(x):
    freq = {}
    for c in set(x):
        freq[c] = x.count(c)
    return freq





def main():
    url_libro, titulo = "https://www.gutenberg.org/cache/epub/13507/pg13507.txt", '#Cuentos de Amor de Locura y de Muerte#'
    texto_ori = bajar_libro(url_libro, titulo)
    text_minuscula_1 = formatear_texto(texto_ori)
    frecuencias = check_freq(text_minuscula_1)

# RUN

if __name__ == '__main__':
    main()




"""Las *stop words* o *palabras vacías* es el nombre que reciben las palabras "sin significado" como artículos, pronombres, preposiciones, etc. que son filtradas antes o después del procesamiento de datos en lenguaje natural (texto). Este concepto se extiende apalabras muy utilizadas y que no aportan mucho a un texto literario. Para hacer nube de etiquetas es conveniente eliminar las palabras vacías, pues en caso contrario las palabras más utilizadas pueden no ser las palabras más significativas. 

En  https://github.com/Alir3z4/stop-words podrán encontrar listas de palabras vacías en diferentes idiomas.

**Ejercicio 3.** Con el módulo `requests` bajar la lista de palabras vacías en español y asignar a la variable `palabras_vacias_es` el conjunto de palabras vacías en español.

Observar que cuando se baja el archivo directamente obtenemos código HTML. Como en este cuaderno no queremos trabajar con código HTML (por simplicidad) podemos bajar el archivo en su versión *raw* (cruda o crudo):

https://raw.githubusercontent.com/Alir3z4/stop-words/master/spanish.txt
"""

response = requests.get("https://raw.githubusercontent.com/Alir3z4/stop-words/master/spanish.txt")
pal_v = response.text.strip() + '\n'

palabras_vacias_es = set()

k = pal_v.find('\n')
while k > -1:
    # print(pal_v[:k].strip())
    palabras_vacias_es.add(pal_v[:k].strip())
    pal_v = pal_v[k:].strip()
    k = pal_v.find('\n')

"""**Ejercicio 4.** Con el uso de WordCloud generar un "grafico de nube de palabras", del texto contenido en la variable `texto_minuscula_1`. El gráfico se almacenará en el objeto `libro_wc` de tipo `WordCloud`. Lo  generaremos con el color de fondo blanco.  """

# instantiate a word cloud object
libro_wc = WordCloud(
    background_color='white',
    stopwords=palabras_vacias_es
)

# generate the word cloud
libro_wc.generate(texto_minuscula_1)

"""Importar el módulo `matplotlib.pyplot` como `plt`, para dibijar el gráfico con los siguiente parametros:

- Tamaño de la imagen = 16.0 de ancho, 9.0 de alto.
- Interpolación = bilinear.
- Ejes de coordenadas invisibles (por defecto `pyplot` dibuja el eje `x` y  el  eje `y` con alguna escala).
"""

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16.0, 9.0)
# display the word cloud
plt.imshow(libro_wc, interpolation='bilinear')
plt.axis('off')
plt.show()

"""Generar nuevamente el gráfico. Añadir al formato del mismo la opción `inferno` en el parametro `color_map` de la clase `WordCloud`."""

libro_wc = WordCloud(
    background_color='white',
    stopwords=palabras_vacias_es, 
    colormap=plt.cm.inferno
)
libro_wc.generate(texto_minuscula_1)
plt.rcParams['figure.figsize'] = (16.0, 9.0)
# display the word cloud
plt.imshow(libro_wc, interpolation='bilinear')
plt.axis('off')
plt.show()

"""**Ejercicio 5.** A continuación se pedira realizar el grafico de  "nube de palabras" dentro de una mascara, figura en particular. Para eso importamos los módulos `numpy` como `np` y del módulo `PIL` importamos la función `Image`. 

*Observación.* Python Imaging Library (PIL) es una librería gratuita que permite la edición de imágenes directamente desde Python. Soporta una variedad de formatos, incluídos los más utilizados como GIF, JPEG y PNG. Una gran parte del código está escrito en C, por cuestiones de rendimiento.
"""

import numpy as np
from PIL import Image

"""Accedemos a la mascara en cuestión. Es el archivo 'perro.png' que subimos con la tarea.

Usando  la función `Image` de `PIL` podemos transformar la imagen en un `ndarray` de `numpy`. Alamacenaremos este array en la variable `imagen`. En este caso el resultado es  es un arreglo 2-dimensional (lista de listas) donde los valores en las listas interiores son números enteros que indican diferente niveles de grises: `0` es negro y `255` es blanco. 

"""

from google.colab import drive
drive.mount('/content/drive')

# imagen = np.array(Image.open("/content/drive/Shareddrives/Algoritmos y Programacion/2022-1/Tareas/imagenes/perro.png"))
imagen = np.array(Image.open("/content/drive/Shareddrives/Algoritmos y Programacion/2022-1/Tareas/imagenes/facundo_quiroga.png"))
print(imagen.shape)
# print(imagen[100,:])
img = imagen[:,:,0] + imagen[:,:,1] + imagen[:,:,2] + imagen[:,:,3]
print(img[200,:])

"""Imprima la imagen a partir de la variable `imagen` y  verá la carra de un perro (los colores originales se han perdido). """

fig = plt.figure()
fig.set_figwidth(14) # set width
fig.set_figheight(18) # set height
plt.imshow(imagen, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')
plt.show()

"""Convertir la imagen en una verdadera "máscara" con fondo blanco y todo los demás negro. """

imagen1 = imagen.copy()
imagen1[imagen1 > 0] =  1
imagen1[imagen1 == 0] = 255
imagen1[imagen1 == 1] = 0
mascara = imagen1.copy()

"""Imprimimos la mascara con los siguientes parametros:

- Ancho = 14.

- Alto = 18.

- Interpolación = bilinear.

- Ejes cartesianos invisibles.
"""

fig = plt.figure()
fig.set_figwidth(14) # set width
fig.set_figheight(18) # set height
plt.imshow(mascara, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')
plt.show()

"""Generar el grafico de "nubes de palabras" con la máscara `mascara` con los siguientes parametros:

- Color del fondo = blanco.

- Contorno de la mascara visibles.

- Incluir las stopwords, incluida la palabra said.

- Ancho = 14.

- Alto = 18.

- Interpolación = bilinear.

- Ejes cartesianos invisibles.
"""

# instantiate a word cloud object
libro_wc2 = WordCloud(background_color='white' , mask=mascara,contour_width=1, stopwords=palabras_vacias_es)
# generate the word cloud
libro_wc2.generate(texto_minuscula_1)
# display the word cloud
fig = plt.figure()
fig.set_figwidth(14) # set width
fig.set_figheight(18) # set height
plt.imshow(libro_wc2, interpolation='bilinear')
plt.axis('off')
plt.show()

"""##ANALISIS DE FRECUENCIA DE PALABRAS

El objetivo de ésta parte es analizar la frecuencia, cantidad de veces que se repite un elemento, de las palabras de la variable `texto_minuscula_1` y graficar los resultados obtenidos.

**Ejercicio 5.** En este ejercicio deberás

1. Dividir el texto de la variable `texto_en_minuscula_1` en palabras y  almacenarlas  en la lista `palabras` (puede haber palabas repetidas).
2. Contar la cantidad de palabras almacendas  e imprimir esa cantidad en pantalla.
3. Definir la función `contar_palabras` que recibe una lista de palabras  y calcula la frecuencia (la cantidad de veces que se repite una misma palabra en la lista). La función `contar_palabras` debe devolver un diccionario cuyas claves son las palabras y sus respectivos valores la frecuencia de las mismas. Imprimir la cantidad de palabrás únicas en el texto.
4. Crear el conjunto `uni_palabras` que tiene todas las palabras del texto.
5. Eliminar las palabras que pertenezcan a las palabras vacías y guardarlas en la la lista `palabras_sin_stopwords`.
6. Utilizar la función `contar_palabras()` definida anteriormente, para generar un diccionario llamado `frec_palabras_sin_stopwords`cuyas claves son las palabras de `palabras_sin_stopwords`  y los valores la frecuencia de cada palabra en el texto.
"""

# 1.
palabras = texto_minuscula_1.split()

# 2. 
print('Cantidad total de palabras:', len(palabras))

# 3.
def contar_palabras(lista_palabras):
   dic={}
   for x in lista_palabras:
       if not x in  dic:        
          dic[x] = lista_palabras.count(x)
   return dic
dic = contar_palabras(palabras)
print('Cantidad total de palabras únicas:',len(dic))

# 4. 
uni_palabras = set(palabras) # alternativamente,  uni_palabras = list(dic.keys())

# 5. 
palabras_sin_stopwords = []
for palabra in palabras:
    if  palabra not in palabras_vacias_es:
        palabras_sin_stopwords.append(palabra)
print('Cantidad total de palabras no vacías:',len(palabras_sin_stopwords))

# 6.
frec_palabras_sin_stopwords = contar_palabras(palabras_sin_stopwords)
print(frec_palabras_sin_stopwords)

"""**Ejercicio 6.**  En este ejercicio vamos a determinar las palabras con mayor frecuencia y haremos un gráfico de barras y otro de torta representando las palabras más frecuentes.  

1. A partir del diccionario `frec_palabras_sin_stopwords` crear una lista de listas llamada `frec_palabras_lst` donde en cada coordenada se encuentre `[palabra, frecuencia_palabra]`. Ordenar esta lista en forma descendente con respecto a la frecuencia. 
2. Imprimir las primeras 10 palabras más frecuentes, con su respectiva frecuencia.
3. Crear dos listas, `x` e `y`donde `x` contiene las palabras e `y` la correspondiente frecuencia. Imprimir los primeros diez elementos de `x` y  los los primeros diez elementos de `y`.
4. Utilizar las variables `x` e `y` para dibujar un gráfico de barras con las primeras 10 palabras mas frecuentes. Con los siguientes parametros:
    - Ancho = 15.
    - Alto = 16.
5. Rehacer el gráfico con los siguientes parametros:
    - Ancho = 6.
    - Alto = 5.
        
    Con los labels:
    - "Numero de ocurrencia" en el eje y. Tamaño de fuente = 12.
    - "Palabras" en el eje x. Tamaño de fuente = 12.
    - Rotar 45° cada una de las palabras en x. 
6. Dibujar un gráfico de torta de las diez palabras más frecuentes con los siguientes parametros:
    - Ancho = 15.
    - Alto = 16.
    - Imprimir las respectivas leyendas.
    - En cada porción del gráfico debe figurar el porcentaje correspondiente.
"""

# 1. 
frec_palabras_lst = []
for clave in frec_palabras_sin_stopwords:
    frec_palabras_lst.append([clave, frec_palabras_sin_stopwords[clave]])
frec_palabras_lst.sort(key = lambda t: t[1], reverse = True)
# print(frec_palabras_lst[:20])

# 2. 
for t in frec_palabras_lst[:10]:
    print(t[0], ':', t[1])

# 3. 
x, y = [], []
for t in frec_palabras_lst[:10]:
    x.append(t[0])
    y.append(t[1])

# 4. 
fig, ax = plt.subplots(figsize=(15,16))
plt.bar(x[:10], y[:10])
plt.show()

# 5.
fig, ax = plt.subplots(figsize=(6,5))
plt.bar(x[:10], y[:10])
ax.set_ylabel('Numero de ocurrencia', fontsize=12)
ax.set_xlabel('Palabra', fontsize=12)
ax.xaxis.set_tick_params(rotation=45)
plt.show()

# 6. 
fig, ax = plt.subplots(figsize=(15,16))
y = y[:10]
x = x[:10]
plt.pie(y, labels = x, autopct = '%1.1f%%')
plt.legend()
plt.show()