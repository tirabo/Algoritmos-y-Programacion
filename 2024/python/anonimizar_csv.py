import csv
from random import randint

# Abrir el archivo CSV original y crear un nuevo archivo para escribir
def anonimizar(original, modificado, lista_de_campos_a_anonimizar):
    # pre: original y modificado son strings con los nombres de los archivos
    #      lista_de_campos_a_anonimizar es una lista de strings con los nombres de los campos a anonimizar
    # post: crea un nuevo archivo modificado a partir del archivo original, donde los campos de la lista de campos a anonimizar
    #       son reemplazados por un valor random (entero convertido a string)
    with open(original, mode='r') as file, open(modificado, mode='w', newline='') as new_file:
        reader = csv.reader(file)
        writer = csv.writer(new_file)

        row = next(reader)
        # Escribir la primera fila del archivo original en el nuevo archivo
        writer.writerow(row)
        indices = [row.index(campo) for campo in lista_de_campos_a_anonimizar]

        # Iterar sobre cada fila del archivo original
        for row in reader:
            # Modificar el segundo campo (índice 1) de la fila
            for indice in indices:
                row[indice] = str(indice) +'A'+str(randint(10000000, 99999999))
            # Escribir la fila modificada en el nuevo archivo
            writer.writerow(row)


def main():
    # Llamar a la función anonimizar con los nombres de los archivos
    directorio = '2024/python/documentos_de_prueba/'
    anonimizar(directorio + 'Notas_LCC_COM1.csv', directorio + 'Notas_LCC_COM1_anonimizados.csv', ['Alumno','DNI'])
    
    return 0

# RUN

if __name__ == '__main__':
    main()