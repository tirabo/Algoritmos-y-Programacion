import copy

# OPERACIONES ELEMENTALES SOBRE GRAFOS
# valencia de un vertice, vertices adyacentes, agregar arista, quitar arista


###  Clase Grafo

class Grafo:
    def __init__(self, vertices_o = set({}), aristas_o = set({})):
        # pre: vértices_o es el conjunto de vértices y arista_o es un lista de pares (x,y) con x, y in vértices_o
        # Incluimos estos parámetros para tener la posibilidad de empezar con un grafo no vacío.
        # Los vértices son elementos donde existe la relación '<' (enteros, cadenas, etc)
        # Cuando se devuelven aristas las aristas son (x_0, x_1) con x_0, x_1 vértices y x_0 < x_1
        assert type(vertices_o) == set and type(aristas_o) == set and all(type(x) == tuple and len(x) == 2 for x in aristas_o) , 'Error: no son conjuntos apropiados.'
        assert all(x[0] < x[1] and all(y in vertices_o for y in x) for x in aristas_o) , 'Error: aristas no apropiadas.'
        
        self.__graph = {} # esta será la lista de adyacencia: un diccionario de listas
        for v in vertices_o:
            self.__graph[v] = []
        # self.__graph asocia a cada vértice de vertices_o una lista vacía
        # Ahora construimos la lista de adyacencia
        for u in aristas_o:
            if u[1] not in self.__graph[u[0]]:
                self.__graph[u[0]].append(u[1])
                self.__graph[u[1]].append(u[0])
        # Las variables anteriores nos dan el estado del grafo (sus vértices y aristas).
        # Los vértices son las claves del diccionario (self.__graph.keys())

    def __str__(self):
        return str((self.vertices(), self.aristas()))

    def vertices(self):
        # post:  devuelve el conjunto de vértices del grafo
        return {v for v in self.__graph.keys()}

    def aristas(self):
        # post:  devuelve el conjunto de aristas del grafo. Las aristas son 2-uplas. 
        arsts = set({})
        for v in self.__graph:
            for w in self.__graph[v]:
                if v < w:
                    arsts.add((v, w))
        return arsts

    def valencia(self, vert):
        # pre: 0 <= vert < len(self.__vertices)
        # post: devuelve la valencia del vértice  v
        assert vert in self.__graph, 'Error:  el vértice '+str(vert)+' no pertenece al grafo'
        return len(self.__graph[vert])

    def adyacentes(self,vert):
        # pre: 0 <= v < len(self.__vertices)
        # post: devuelve los vertices adyacentes a vert
        assert vert in self.__graph, 'Error:  el vértice '+str(vert)+' no pertenece al grafo'
        return {z for z in self.__graph[vert]}
    
    def agregar_vertice(self, new_vert):
        # post: agrega un vértice 
        if new_vert not in self.__graph:
            self.__graph[new_vert] = [] # aumento en 1 el tamaño de la lista de adyacencia. 

    def agregar_arista(self, e): 
        # pre: e == (x, y) 
        # post: agrega arista e = {x, y} (si no está). Sí alguno de los vértices no está, lo agrega.
        assert type(e) == tuple and len(e) == 2 and e[0] != e[1], 'Error: el argumento debe ser un par de elementos distintos'
        if e[0] not in self.vertices():
            self.agregar_vertice(e[0])
        if  e[1] not in self.vertices():
            self.agregar_vertice(e[1])
        if e[1] not in self.__graph[e[0]]: # comprueba que lla arista no esté
            self.__graph[e[1]].append(e[0]) # agrega la arista a la lista de adyacencia
            self.__graph[e[0]].append(e[1]) # agrega la arista a la lista de adyacencia

    def quitar_arista(self, e):
        # pre: e = (x, y) arista
        # post: quita arista e (si está). En  caso contrario no hace nada.
        assert type(e) == tuple and len(e) == 2 and e[0] != e[1], 'Error: el argumento debe ser una 2-upla de elementos distintos' 
        if all(v in self.__graph.keys() for v in e) and e[1] in self.__graph[e[0]]: # comprueba que e  es arista
        # if e in self.aristas(): # se puede cambiar por esta qu es más clara, pero me parece que es mucho menos eficiente
            self.__graph[e[0]].remove(e[1]) 
            self.__graph[e[1]].remove(e[0]) 

    def copiar(self):
        # post: devuelve una copia del grafo
        return Grafo(self.vertices(), self.aristas())


# ALGORITMOS SOBRE GRAFOS

def recorrido_euleriano_max(L: Grafo, v_ini):
    # pre: v_ini vértice de L
    # post: devuelve caminata, una caminata exhaustiva que no repite aristas
    # mod: L termino siendo el grafo original menos la caminata
    sub_caminata = [v_ini]  # sub caminata
    p0 = v_ini
    while len(L.adyacentes(p0)) > 0:  # mientras se pueda avanzar
        p1 = L.adyacentes(p0).pop()
        sub_caminata.append(p1)  # agrega p1 a caminata
        L.quitar_arista((p0,p1)) # quitar arista p0, p1 
        p0 = p1 
    return sub_caminata


def caminata_euleriana(G: Grafo, v_ini) -> list:
    # pre: v_ini vértices de G  a) G grafo con todos los vértices de valencia par, o
    #      b) solo hay dos vertices de valencia impar y v_ini es uno de ellos
    # post: devuelve 'caminata' una lista de vértices que forma un caminata o circuito euleriano que empieza en v_ini.
    assert isinstance(G, Grafo) and v_ini in G.vertices(), 'El primer argumento debe ser un grafo y el segundo un vértice del grafo' 
    vertices_impares = {v for v in G.vertices() if len(G.adyacentes(v)) % 2 == 1}
    assert len(vertices_impares) <= 2, 'Hay '+str(len(vertices_impares)) +' > 2 vértices impares'  
    assert len(vertices_impares) == 0 or (len(vertices_impares) == 2 and v_ini in vertices_impares), 'El vértice debe ser impar'   
    
    libres = G.copiar() # sub grafo de aristas no utilizadas
    caminata = recorrido_euleriano_max(libres, v_ini) # el subgrafo libres que queda es todo de valencias pares (¿por qué?)
    while len(libres.aristas()) > 0: 
        for h in libres.vertices():
            if len(libres.adyacentes(h)) > 0 and h in caminata:
                pos = caminata.index(h)
                caminata =  caminata[:pos] + recorrido_euleriano_max(libres, h) + caminata[pos+1:] # esto también modifica libres
    return caminata



# Alternativo
def caminata_euleriana_alt(G: Grafo, v_ini) -> list:
    # pre: v_ini vértices de G  a) G grafo con todos los vértices de valencia par, o
    #      b) solo hay dos vertices de valencia impar y v_ini es uno de ellos
    # post: devuelve 'caminata' una lista de vértices que forma un caminata o circuito euleriano que empieza en v_ini.
    assert isinstance(G, Grafo) and v_ini in G.vertices(), 'El primer argumento debe ser un grafo y el segundo un vértice del grafo' 
    vertices_impares = {v for v in G.vertices() if len(G.adyacentes(v)) % 2 == 1}
    assert len(vertices_impares) <= 2, 'Hay '+str(len(vertices_impares)) +' > 2 vértices impares'  
    assert len(vertices_impares) == 0 or (len(vertices_impares) == 2 and v_ini in vertices_impares), 'El vértice debe ser impar'    

    libres = G.copiar() # sub grafo de aristas no utilizadas
    caminata = [v_ini]
    while len(libres.aristas()) > 0: 
        for h in libres.vertices(): 
            if len(libres.adyacentes(h)) > 0 and h in caminata:
                pos = caminata.index(h)
                caminata =  caminata[:pos] + recorrido_euleriano_max(libres, h) + caminata[pos+1:] # esto también modifica libres
    return caminata


## INICIO: algoritmo greedy para coloración de vértices

def coloracion_vertices(G: Grafo):
    # pre: G grafo
    # post: devuelve un diccionario  color,  tal que si v  vértice color[v] es el color de v
    color = {}  # si  v  vértice coloreado, color[v] = c dice que el color de v es c.
    recorridos = set()
    for vert in  G.vertices():
        colores_ady = {color[v] for v in recorridos if v in G.adyacentes(vert)}  # colores de los vértices anteriores adyacentes
        i = 1
        while i in colores_ady:
            i = i + 1
        color[vert] = i # primer color no utilizado por los vértices anteriores adyacentes
        recorridos.add(vert)
    return color

## FIN: algoritmo greedy para coloración de vértices


# INICIO: Algoritmo de Kruskal para MST.
# Pseudocódigo Cormen.
# def Kruskal(G = (V,E): grafo; length: E -> int):
#   n = len(V)
#   mst = Grafo() # Contendrá las aristas del MST
#   for v in G.vertices():
#       hacer_conjunto(v) # por cada vértice hace un conjunto  
#   lista_aristas = ordenar las aristas en orden no decreciente según peso
#   while len(mst.aristas()) < n-1:
#       (u, v) = lista_aristas.pop(0) # saca la arista de peso mas bajo. 
#       if conjunto_de(u) != conjunto_de(v): # si los vértices pertenecen a distintos conjuntos
#           mst.agregar_arista((u,v))
#           unir(conjunto_de(u), conjunto_de(v)) 
#   return mst

def kruskal(G: Grafo, pesos):
    # pre: G grafo conexo, pesos es diccionario donde las claves son las aristas y los valores son enteros no negativos 
    mst = Grafo() # Contendrá las aristas del MST
    n = len(G.vertices())
    lista_pesos = []
    for e in pesos:
        lista_pesos.append([pesos[e], e])
    lista_pesos.sort() #  lista de aristas ordenadas por peso
    conjunto_de = {v:v for v in G.vertices()} # conjunto_de[v] == conjunto_de[w] sii v y w pertenecen al mismo conjunto
    while len(mst.aristas()) < n-1:
        e = lista_pesos.pop(0)[1] # arista de menor peso disponible
        if conjunto_de[e[0]] != conjunto_de[e[1]]: # recordemos que e[0] < e[1]
            mst.agregar_arista(e)
            conjunto_de[e[1]] = conjunto_de[e[0]] # unión de los conjuntos
    return mst

#FIN: Algoritmo de Kruskal para MST.



## INICIO: algoritmo Prim para MST con pesos (implementado según Cormen)
#
# def prim(G: Grafo , pesos):
#     r = vértice de G
#     for u in G.vertices():
#         key[u] = INFINITO 
#         padre[u] = NONE # Cuando el algoritmo termina  padre[v] será el padre de v en el MST, para los v que no son raíz (el vértice r). 
#     key[r] = 0
#     cola = G.vertices()
#     while cola != {}:
#         u = un vértice de cola con key[u] mínima
#         cola.remove(u)
#         for v in u.adyacentes():
#             if v in cola and w(u, v) < key[v]:
#                 padre[v] = u
#                 key[v] = w(u, v)
#     mst = Grafo(G.vertices(), {}) # este va a ser el MST. Se inicializa como un grafo con todos los vértices de G y si aristas. 
#     for v in mst.vértices() - {r}:
#         mst.agregar_arista((v,padre[v]))
#     return  mst

def prim(G: Grafo , pesos):
    # pre: pesos un diccionario donde las claves son las aristas  y los valores son reales no negativos. 
    # post: devuelve mst un MST  de G. 
    r =  next(iter(G.vertices())) # toma un vértice de G sin quitarlo
    key, padre = {}, {} # dos diccionarios vacíos. El primero es una "cola de prioridad". El segundo indicará quien será el padre en el MST.
    INFINITO = 0
    for arista in G.aristas():
        INFINITO = max(INFINITO, pesos[arista])
    INFINITO += INFINITO # INFINITO es un valor más alto que todos los pesos
    for u in G.vertices():
        key[u] = INFINITO 
        padre[u] = None # Cuando el algoritmo termina  padre[v] será el padre de v en el MST, para los v que no son raíz (el vértice r). 
    key[r] = 0
    cola = G.vertices()
    while cola != set({}):
        u = min([[key[v],v] for v in cola])[1] # un vértice de cola con key[u] mínima
        cola.remove(u)
        for v in G.adyacentes(u):
            arista = (u,v) if u < v else (v, u)
            if v in cola and pesos[arista] < key[v]:
                padre[v] = u
                key[v] = pesos[arista]
    mst = Grafo(G.vertices(), set({})) # este va a ser el MST. Se inicializa como un grafo con todos los vértices de G y si aristas. 
    for v in mst.vertices() - {r}:
        mst.agregar_arista((v,padre[v]))
    return  mst
## FIN: algoritmo Prim para MST con pesos (implementado según Cormen)

def main():
    # Grafos de prueba
    
    # Grafo 0 (el gran tour)
    G0 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5)})
    # print(G0)
    # print(recorrido_euleriano_max(G0, 0))
    # lista ady= [[1,2,4,5],[0,2,4,5],[0,1,3,5],[2,4],[0,1,3,5],[0,1,2,4]]

    # Grafo 1
    G1 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    #print(G1)
    #print(recorrido_euleriano_max(G1, 0),'\n')
    #lista_ady [[3,4,5,6], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [0,5]]

    # Grafo 2 (cíclico)
    G2 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)})
    # print(G2)
    # print(recorrido_euleriano_max(G2, 0),'\n')
    #lista_ady [[1,5],[0, 2],[1,3],[2,4],[3,5],[4,0]]

    # Grafo 3 
    G3 = Grafo({0, 1, 2, 3, 4, 5}, {(0, 2), (0, 4), (0, 5), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)})
    # print(G3)
    # print(recorrido_euleriano_max(G3, 0))
    # print(recorrido_euleriano_max(G3, 1),'\n')
    #lista_ady [[2, 4, 5], [3, 5], [0, 3, 4, 5], [1, 2, 4], [0, 2, 3, 5], [0, 1, 2, 4]]

    # Grafo 4
    G4 = Grafo({0, 1, 2, 3, 4, 5, 6}, {(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (2, 5), (3, 4), (4, 5), (5, 6)})
    # print(recorrido_euleriano_max(G4, 0))
    #lista_ady [[3,4,5], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [5]]
    
    # Grafo 6 (dos valencias impares)
    G6 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
    #print(G6)
    #print(caminata_euleriana(G6, 0))

    # Grafo 7 (todas valencias pares)
    G7 = Grafo({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, {(0, 1), (0, 11), (1, 2), (2, 3), (2, 4), (2, 7), (3, 4), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10), (8, 11), (9, 10)})
    # print(G7)
    #print(recorrido_euleriano_max(G7,0))
    # G7.agregar_vertice()
    # print(G7)
    # G7.agregar_arista([12, 0])
    # print(G7)
    # print(caminata_euleriana(G7, 0))
    # print(isinstance(G7, Grafo)  )

    #print(coloracion_vertices(G1))
    #print(coloracion_vertices(G7))



    # Pesos en G1
    pesos_G1 =  {(0, 3):5, (0, 4):0, (0, 5):0, (0, 6):0, (1, 2):10, (1, 4):0, (2, 5):0, (3, 4):0, (4, 5):0, (5, 6):0}

    print(kruskal(G1, pesos_G1))
    print(prim(G1, pesos_G1))


    return 0
# RUN

if __name__ == '__main__':
    main()
