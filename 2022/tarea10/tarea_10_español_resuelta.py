# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt 
import requests
import os
# from wordcloud import WordCloud

# def bajar_libro(url, titulo):
#     response = requests.get(url)
#     texto = response.text
#     k_ini, k_fin = texto.find(titulo), test.find('FIN')
#     texto = texto[k_ini:k_fin]
#     return  texto

# def formatear_texto(texto):
#     texto_min = texto.lower()
#     caracteres = "(),._:;-'[]¡¿!?*$%&/#\""
#     for x in range(len(caracteres)):
#         texto_min = texto_min.replace(caracteres[x],"")
#     return texto_min

# def check_freq(x):
#     freq = {}
#     for c in set(x):
#         freq[c] = x.count(c)
#     return freq






def main():
    pass
    # url_libro, titulo = "https://www.gutenberg.org/cache/epub/13507/pg13507.txt", '#Cuentos de Amor de Locura y de Muerte#'
    # texto_ori = bajar_libro(url_libro, titulo)
    # text_minuscula_1 = formatear_texto(texto_ori)
    # frecuencias = check_freq(text_minuscula_1)

    # print(os.getcwd())
    # print(os.listdir('../../../'))

    imagen = Image.open('../../../Pictures/perro.png')
    imagen.show() # muestra la imagen

# RUN

if __name__ == '__main__':
    main()

