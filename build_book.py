# Hace un build del Jupyter Book y el contenido de _build/html se copia  a tirabo.github.io/ayp
import os
import shutil

# Hace un build del Jupyter Book
# os.system('jupyter-book build book/')

# Copia el contenido de _build/html a tirabo.github.io/ayp
shutil.rmtree('../tirabo.github.io/html/ayp') # borra ../tirabo.github.io/ayp y su contenido 
shutil.copytree('book/_build/html', '../tirabo.github.io/html/ayp') # crea el directorio ../tirabo.github.io/ayp y copia en él el contenido de _build/html
os.chdir('../tirabo.github.io') # cambia al directorio ../tirabo.github.io
os.system('ghp-import -n -p -f ./html') # hace un push de html a tirabo.github.io
os.chdir('../Algoritmos-y-Programacion') # cambia al directorio actual
print('Proceso terminado')