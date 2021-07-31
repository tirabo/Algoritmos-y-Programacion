
from itertools import chain, combinations


def dos_subconjuntos(n: int): 
    # devuelve la lista de 2-subconjuntos del conjunto {0,...,n-1}. Los devuelve como 2-uplas. 
    dos_tuplas = []
    for i in range(n):
        for j in range(i+1, n):
            dos_tuplas.append((i,j))
    return dos_tuplas

def powerset2(s):
    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    # Devuelve un iterable con los subconjuntos (es un iterable que se usa una sola vez,  generator en Python)
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]
    

def powerset(s):
    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    x = len(s)
    pow_set = []
    for i in range(1 << x):
        pow_set.append([s[j] for j in range(x) if (i & (1 << j))])
    return pow_set


def lista_de_valencias(n, grafo):
    # n entero,  grafo es un grafo con n vértices
    # post: lista de valencias en orden ascendente 
    val = [0] * n
    for edge in grafo:
        val[edge[0]] += 1
        val[edge[1]] += 1
    val.sort()
    return tuple(val)

def es_conexo(n, grafo):
    vertices = [0]
    for edge in grafo:
        if edge[0] in vertices:
            vertices.append(edge[1])
        if edge[1] in vertices:
            vertices.append(edge[0])
    return set(vertices)

    





def main():
    pass
    dos_6 = dos_subconjuntos(6)
    dos_7 = dos_subconjuntos(7)
    grafos_6 = powerset(dos_6) # todos los grafos de 6 vertices
    # grafos_7 = powerset(dos_7) # todos los grafos de 7 vertices
    i = 0
    posibles_val = []
    for grafo in grafos_6:
        lista_val = lista_de_valencias(6, grafo)
        posibles_val.append(lista_val)
        if lista_val == (2, 2, 2, 2, 2, 4):
            i += 1
            print(grafo)
            print(es_conexo(6, grafo))
        # if i > 100:
        #     break
    conJ_val = set(posibles_val)
    print(i)
    print(len(conJ_val))



if __name__ == '__main__':
    main()
