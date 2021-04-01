# importaciones
import turtle


# Constantes
PI = 3.14

# Definiciones de funciones

def prueba():
    print('prueba ok')


def prueba_PI():
    print('prueba', PI, 'ok')


def o_exclusivo(sentencia_1, sentencia_2: bool) -> bool:
    return (sentencia_1 and not sentencia_2) or (not sentencia_1 and sentencia_2)


def implica(sentencia_1, sentencia_2: bool) -> int:
    # p => q  equivalente a (not p or q)
    valor_booleano = not sentencia_1 or sentencia_2
    dev = 0
    if valor_booleano == True:
        dev = 1
    else:
        dev = 0
    return dev

def main():
    prueba_PI()


# Correr el programa

if __name__ == "__main__":
    main()
