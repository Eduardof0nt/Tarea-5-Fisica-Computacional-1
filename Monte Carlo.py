import numpy as np
import matplotlib.pyplot as plt
import time

# np.random.seed(9472749)

def CaminoAleatorio(lista_Pos, N=2):
    """
    Genera una nueva posición aleatoria en el camino aleatorio.
    Toma como parámetros de entrada:
        - lista_Pos: la lista donde se encuentran los puntos recorridos por el camino aleatroio hasta el momento.
        - N: Las dimensiones en las que se ejecuta la simulación. Por defecto es dos pero para esta simulación es 3.
    """
    vec = 2*np.random.rand(N) - 1 #Se genera un vector con componentes aleatorias entre -1 y 1 en la cantidad de dimensiones especificadas.
    
    L = np.sqrt(np.sum(np.power(vec,2))) #Se calcula la norma (longitud) del vector.
    
    nuevaPos = lista_Pos[len(lista_Pos)-1] + vec/L #Se normaliza el vector para que que tenga una longitud de 1 y se suma a la última posición del camino aleatorio para obtener la nueva posición.

    lista_Pos.append(nuevaPos) #Se agrega la nueva posición a la lista y se retorna la lista.

    return lista_Pos

##############################################

def calcular(N, nPasos, indicador):
    """
    Realiza el un camino aleatorio en base a los parámetros dados.
    Tiene como parámetros:
        - N: El número de dimensiones en las que se van a dar los pasos.
        - nPasos: El rádio que se debe alcanzar el camino aleatorio para terminar el cálculo (en pasos).
        - indicador: Cada cuantos pasos se desea imprimir el progreso de la simulación. Se imprime el número de pasos dados hasta el momento y el radio (en pasos) que se tiene en la iteración actual.
    """

    camino = [[0]*N] #Se crea una lista con una posición inicial en el origen con la cantidad de dimenciones especificada.

    i = 1 #Se inicia el contador.
    
    #Se comienza un ciclo while. Ese termina una vez que el camino aleatorio alcanza el radio especificado (en pasos).
    while np.sqrt(np.sum(np.power(camino[i-1],2))) < nPasos:
        camino = CaminoAleatorio(camino, N) #Se asigna la lista obtenida en el cálculo del paso realizado en cada itración (Se devuelve la lista que se tenía hasta el mometo más el paso recientemente calculado).
        if(i%indicador == 0):
            print(str(i) + ': ' + str(np.sqrt(np.sum(np.power(camino[i-1],2))))) #Si se llega a un múltiplo del indicador especificado, se imprime el radio en pasos de la iteración actual.
        i += 1 #Añadir uno al contador.
        
    camino = np.array(camino) #Se convierte la lista calculada a un arreglo de NumPy.
    
    return camino, i-1 #Se retornan el arreglo con el camino calculado y la cantidad de pasos dados para alcanzar el radio especificado.

##############################################

# Simulación
tiempoInicio = time.time() #Se comienza con calcular un tiempo de inicio, esto para calcular el tiempo total que tomó la simulación.
dimensiones = 3 #Número de dimensiones en las cuales se va a realizar la simulación.
c = 299792458 #Velocidad de la luz en m/s.
radio = 5*10**-4#8 #El radio de la región de la cual se desea que la partícula salga en m.
distanciaMedia = 5*10**-5 #La distancia media recorrida por la partícula en cada paso en m.
radioEnPasos =  radio/distanciaMedia #El radio de salida en pasos unitarios. Esta es la cantidad de pasos mínima que se requeriría para que la partícula salga del radio dado si se moviera en todo momento en la misma dirección.
nPasosAproxParaSalir = np.ceil(np.power(radio/distanciaMedia,2)).astype('uint32') #La cantidad promedio de pasos N requerida para que se alcance el radio dado. N≈(R/r)**2.
nIteraciones = 3#10**5 #5#La cantidad de simulaciones independientes que se van a ejecutar para calcular la cantidad de pasos promedio que se requieren para alcanzar el radio dado.
indicadorDeIteraciones = 10**6 #Cada cuantos pasos se desea imprimir el progreso de la simulación. Se imprime el número de pasos dados hasta el momento y el radio (en pasos) que se tiene en la iteración actual de cada una de las simulaciones.


pasosCalculados = [] #Se inicia la lista para guardar la cantidad de pasos que se dieron en cada simulación para llegar al radio de salida. Estos luego se van a promediar para comparar con el valor estimado por medio de cálculos estadísticos.
caminos = [] #Se inicia la lista que guarda los caminos aleatorios obtenidos en cada simulación.

#Información para el usuario.
print('Se estima que se deben dar ' + str(np.format_float_scientific(nPasosAproxParaSalir)) + ' pasos en promedio para alcanzar un radio de ' + str(np.format_float_scientific(radio)) + ' m con pasos de ' + str(np.format_float_scientific(distanciaMedia)) + ' m.')

print('Un fotón dura en promedio {0} años en escapar de esta región'.format(np.format_float_scientific((nPasosAproxParaSalir*distanciaMedia)/(c*31557600.0))))

#Se realiza el número de simulaciones especificadas.
for i  in range(1, nIteraciones+1):
    print('------------------{0}------------------'.format(i))
    #Se obtienen los calculos retornados por cada simulación realizada y se guardan en su arreglo respectivo.
    camino, pasos = calcular(dimensiones, radioEnPasos, indicadorDeIteraciones)
    caminos.append(camino)
    pasosCalculados.append(pasos)

pasosMedios = 0 #Se inicia la variable pasos medios para realizar el cálculo del promerdio de pasos que se dieron para llegar al radio de salida.

#Se suma el valor de la cantidad de pasos realizados en cada simulación y se divide el valor obtenido entre el número total de simulaciones para obtener el promedio.
for p in pasosCalculados:
    pasosMedios += p

pasosMedios /= len(pasosCalculados)

#Información para el usuario.
print('La cantidad de pasos promedio obtenidos es de ' + str(np.format_float_scientific(pasosMedios)) + ' para ' + str(nIteraciones) + ' iteraciones.')

print('El error relativo entre el valor promedio calculado ({1} pasos) y el valor promedio obtenido ({2} pasos) es de {0:.2f}'.format((pasosMedios-nPasosAproxParaSalir)*100/nPasosAproxParaSalir,np.format_float_scientific(nPasosAproxParaSalir),np.format_float_scientific(pasosMedios)) + '%.')

print('\n'*4)

print('En el gráfico, la "x" negra marca el origen y el círculo verde marca el punto de salida del radio especificado.')

print('Se tardaron {0} s en la ejecución.'.format(np.format_float_scientific(time.time()-tiempoInicio)))

#Se grafican los resultados en un espacio de 3 dimensiones (las requeridas para el problema dado).
ax = plt.axes(projection='3d')

#Se grafica el primer camino pbtenido, así como una "X" negra en el origen y un círculo verde para indicar el punto de finalización de la simulación. El camino aleatorio se grafica en rojo.
ax.plot(caminos[0][0,0], caminos[0][0,1], caminos[0][0,2], c=(0,0,0), marker="x")
ax.plot(caminos[0][:,0], caminos[0][:,1], caminos[0][:,2], c=(1, 0, 0), lw=0.5)
ax.plot(caminos[0][-1,0], caminos[0][-1,1], caminos[0][-1,2], c=(0,1,0), marker="o")

ax.set_title('Caminos aleatorios')

plt.show(block=True)
