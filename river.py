import numpy as np
import matplotlib.pyplot as plt
import random

def cargar_mapa(mapa):
    data = np.loadtxt(mapa)
    data = np.reshape(data, (100,100))
    return data

def dibujar_mapa(A):
    plt.imshow(A, cmap = 'terrain')
    plt.colorbar()
    plt.show()

def dibujar_rio(M, river):
    R = np.zeros((100, 100))
    for r in river:
        # Tuve que cambiar el orden de los índices de la matriz, pues un numpy.ndarray() toma primero las columnas y luego las filas (R[y][x])
        R[r[1], r[0]] = 1
    plt.imshow(M, cmap = 'terrain')
    plt.colorbar()
    plt.imshow(R, cmap = 'Blues', alpha = 0.2)
    plt.show()

# Lista de posibles vecinos del nodo (0, 0) como variable global
VECINOS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

def buscar_peak(M):
    """Buscar el máximo valor de la matriz M. En el caso de existir más de uno, se escogerá de forma aleatoria.
    maximos_locales es un numpy.ndarray que contiene 1D arrays con las coordenadas (y, x) de los máximos.
    La función regresa una lista con las coordenadas (x, y) de un máximo aleatorio (en el caso de que el valor se repita)."""
    peak = M.max()
    maximos_locales = np.argwhere(M == peak)
    maximo = random.choice(maximos_locales)

    return [maximo[1], maximo[0]]

def max_pend(M, x, y):
    """Esta función busca el valor donde la pendiente es máxima para un nodo, comparándolo con sus vecinos.
    Todas las pendientes se adjuntan a un diccionario con su coordenada como key y luego se busca la máxima. 
    En el caso de existir más de una, se coleccionarán en un diccionario y se elegirá una al azar.
    Se retornará la una lista con las coordenads (x, y) representando un nodo vecino con máxima pendiente."""
    pendientes_dict = {}
    for par_ordenado in VECINOS:
        vecino_x, vecino_y = x + par_ordenado[0], y + par_ordenado[1]
        # Comprobar si las coordenadas del vecino están dentro de los límites de M.
        if vecino_x > (M.shape[1] - 1) or vecino_y > (M.shape[0] - 1):
            pendientes_dict[(vecino_x, vecino_y)] = 0
            continue
        else:
            vecino = M[y + par_ordenado[1]][x + par_ordenado[0]]
            pendiente = M[y][x] - vecino
            # Si la pendiente es menor que cero, a esa coordenada se le da el valor 0 para que al coomparar maximos no se cuenten
            if pendiente <= 0:
                pendientes_dict[(vecino_x, vecino_y)] = 0
            else:
                pendientes_dict[(vecino_x, vecino_y)] = pendiente

    # Comprobar que las pendientes no tengan el valor 0 asociado. En tal caso se retorna una lista con [-1, -1] para terminar el proceso.
    pm = pendientes_dict.get(max(pendientes_dict, key=pendientes_dict.get))
    if pm == 0:
        return [-1, -1] #Trucazo... borrar esta anotación xd
    else:
        # Acceder a la key de la pendiente máxima, guardarla en un diccionario
        pendiente_maxima = max(pendientes_dict, key=pendientes_dict.get)
        maximas_pendientes = [w for w, v in pendientes_dict.items() if v == pendientes_dict[pendiente_maxima]]
        coordenada_vecino = random.choice(maximas_pendientes)

        return [coordenada_vecino[0], coordenada_vecino[1]]

def rio(M, i, j):
    """Función que regresa una lista con las coordenadas del vecino del nodo de coordenadas (i, j) tal que este
    sea max_pend(M, i, j). Luego ese vecino pasa a ser el nuevo nodo (i, j).
    La función se detiene cuando se llega a un borde de M o cuando todos los vecinos tienen una pendiente == 0."""
    # Pasar de la función si (i||j==-1)
    if i == -1 or j == -1:
        pass
    else:
        nodos = []
        # Adjuntar el nodo inicial
        nodos.append([i, j])
        while True:
            nodo = max_pend(M, i, j)
            # Comprobar que el siguiente nodo no sobrease los límites inferiores de M o que no sea igual que el actual (pendiente == 0)
            if i + nodo[0] == nodo[0] or j + nodo[1] == nodo[1] or (i == nodo[0] and j == nodo[1]):
                break 
            else:
                nodos.append(nodo)
                i, j = nodo[0], nodo[1]

                # Comprobar que el siguiente nodo no sobrepase los límites superiores de M
                if i + nodo[0] == i or j + nodo[1] == j:
                    break
                else:
                    pass
        
        return nodos

A = cargar_mapa('mapa1.txt')
p = buscar_peak(A)
r = rio(A, p[0], p[1])
dibujar_rio(A, r)
