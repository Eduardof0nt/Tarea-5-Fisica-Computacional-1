# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 11:42:48 2021

@author: oscar
"""
import numpy as np
import matplotlib.pyplot as plt
#np.random.seed(9472749)

def calcularEnergía(estados, J):
    '''
    Esta función calcula la energía para cada configuración.
    Parameters
    ----------
    estados : Corresponde a los estados de espines de la configuración.
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.

    Returns
    -------
    valorE : Corresponde al valor de energía para la configuración.
    '''
    energia = 0
    for i in range(0,len(estados)-1):
        estados[0] = estados[-1] #Condición de controno
        energia += estados[i]*estados[i+1]
        
    valorE=-1*energia*J
    
    return valorE

def calcularMagnetización(estados):
    '''
    Esta función calcula la magnetización para cada configuración.
    Parameters
    ----------
    estados : Corresponde a los estados de espines de la configuración.

    Returns
    -------
    magnetizacion : Retorna el valor de magnetización para la configuración.
    '''
    magnetizacion = 0
    for i in range(0,len(estados)):
        estados[0] = estados[-1] #Condición de controno
        magnetizacion +=estados[i]
    return magnetizacion

def crearEstadoInicialAleatorio(N):
    '''
    Esta función crea un estado inicial aleatorio.
    Parameters
    ----------
    N : Número de espines que tiene la configuración.

    Returns
    -------
    estados: Corresponde a la configuración de espines creada.
    '''
    estados = np.random.rand(1,N)[0]
    for i in range(0,len(estados)):
        if estados[i] < 0.5:
            estados[i] = -1
        else:
            estados[i] = 1
    return estados
            
def crearEstadoInicialOrdenado(N, estado):
    '''
    Esta función crea un estado inicial con todos los espines de la configuración incial alineados
    Parameters
    ----------
    N : Número de espines que tiene la configuración.
    estado : Corresponde a ala alineación del espín.

    Returns
    -------
    Retorna la configuración de estados alineada.
    '''
    return np.array([estado]*N)


def realizarSimulacion(N, J, kT, nPasos):
    '''
    Esta función realiza la simulación del Modelo de Ising para una T específica
    Parameters
    ----------
    N : Número de espines que tiene la configuración.
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.
    kT : Representa la constante de Boltzmann por la Temperatura, en donde se mantiene k=1.
    nPasos : Número de pasos que tendrá la simulación.
    
    Returns
    -------
    estadosT : Retorna la configuración de espines para cada paso.
    arregloEnergias : Retorna el arreglo de energías para cada paso.
    arregloMagnetizaciones : Retorna el arreglo de magnetizaciones para cada paso.
    energiasEquilibrio : Retorna el arreglo de energías para cada paso despúes de que se alcanza la condición de equilibrio.
    magnetizacionesEquilibrio : Retorna el arreglo de magnetizaciones para cada paso despúes de que se alcanza la condición de equilibrio.
    energiasCuadEquilibrio : Retorna el arreglo de energías elevadas al cuadrado para cada paso despúes de que se alcanza la condición de equilibrio.
    '''
    B = 1/kT #Se define el parámetro Beta
    #estados = crearEstadoInicialOrdenado(N,1) #Se crea el estado inicial con los espines alineados en dirección positiva
    #estados = crearEstadoInicialOrdenado(N,-1) #Se crea el estado inicial con los espines alineados en dirección negativa
    estados = crearEstadoInicialAleatorio(N) #Se crea el estado inicial con los espines alineados de forma aleatoria
    
    estadosT = estados #Se crea la variable donde se guardan los espines
    energiaInicial = calcularEnergía(estados,J) #Se calcula la energía inicial
    energias = [energiaInicial] #Se inicializa la lista de energías con la energía inicial
    energiasCuad=[energiaInicial**2] #Se inicializa la lista de energías elevadas al cuadrado con la energía inicial
    
    magnetizacionInicial=calcularMagnetización(estados) #Se calcula la magnetización inicial
    magnetizaciones = [magnetizacionInicial] #Se inicializa la lista de energías con la energía inicial
    
    n = nPasos #Se establece un parámetro n para el ciclo while
    nEquilibrio=1000 #Condición en el que el sistema entra en equilibrio
    
    while n > 0: #Se establece un ciclo while para hacer los cálculos para cada paso
    
        pos = np.floor(np.random.rand(1)*N).astype(int)[0] #Se escoge una posición aleatoria en la cual se cambiará la dirección del espín
        estados[pos] *= -1 #Se cambia la dirección del espín en la posición aleatoria 
        energiaActual = calcularEnergía(estados,J) #Se calcula la nueva energía después del cambio
        magnetizacionActual=calcularMagnetización(estados) #Se calcula la nueva magnetización después del cambio
        
        if energiaActual < energiaInicial: #Se establece la condición de energía en la cual se acepta realizar el cambio
        
            energiaInicial = energiaActual #Se realiza el cambio de energía para la siguiente iteración
            magnetizacionInicial=magnetizacionActual #Se realiza el cambio de magnetización para la siguiente iteración
            
            estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
            energias.append(energiaActual) #Se guarda el valor de energía
            magnetizaciones.append(magnetizacionActual) #Se guarda el valor de la magnetización
            energiasCuad.append(energiaActual**2) #Se guarda el valor de energía elevada al cuadrado
            
        else: #Si no se cumple la condición de energía para el cambio
        
            P = np.exp(-B*(energiaActual-energiaInicial)) #Se define la probabilidad para realizar el cambio
            
            if np.random.rand(1) < P: #Mediante a un número aleatorio, se acepta el cambio
                
                energiaInicial = energiaActual #Se realiza el cambio de energía para la siguiente iteración
                magnetizacionInicial=magnetizacionActual #Se realiza el cambio de magnetización para la siguiente iteración
                
                estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
                energias.append(energiaActual) #Se guarda el valor de energía
                magnetizaciones.append(magnetizacionActual) #Se guarda el valor de la magnetización
                energiasCuad.append(energiaActual**2) ##Se guarda el valor de energía elevada al cuadrado
                
            else: #Si no se cumple la condición anterior, se rechaza el cambio
            
                estados[pos] *= -1 #Se vuelve al estado original, pues no se acepta el cambio
                estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
                energias.append(energiaInicial) #Se guarda el valor de energía inicial, pues no se acepta el cambio
                magnetizaciones.append(magnetizacionInicial) #Se guarda el valor de magnetización inicial, pues no se acepta el cambio
                energiasCuad.append(energiaInicial**2) #Se guarda el valor de energía inicial elevada al cuadrado, pues no se acepta el cambio
                
        n -= 1 #Se le resta 1 una vez realizados los cálculos por cada paso
        
    arregloEnergias=np.array(energias) #Se establece el arreglo de energías
    arregloMagnetizaciones=np.array(magnetizaciones) #Se establece el arreglo de magnetizaciones
    arregloEnergiasCuad=np.array(energiasCuad) #Se establece el arreglo de energías elevadas al cuadrado
    energiasEquilibrio=arregloEnergias[nEquilibrio::] #Se toman las energías después del equilibrio
    magnetizacionesEquilibrio=arregloMagnetizaciones[nEquilibrio::] #Se toman las magnetizaciones después del equilibrio
    energiasCuadEquilibrio=arregloEnergiasCuad[nEquilibrio::] #Se toman las energías elevadas al cuadrado después del equilibrio
    
    return estadosT, arregloEnergias , arregloMagnetizaciones , energiasEquilibrio , magnetizacionesEquilibrio , energiasCuadEquilibrio

def ReduceYProm(conjunto, ejecuciones, pasos):
    '''
    Esta función realiza las ejecuciones y calcula el promedio para reducir las fluctuaciones.
    Parameters
    ----------
    conjunto : Corresponde al arreglo de los valores correspondientes a cada ejecución realizada.
    ejecuciones : Corresponde al número de ejecuciones que se realizan para reducir las fluctuaciones.
    pasos : Corresponde al número de pasos que se llevaron a cabo en cada ejecución dependiendo del parámetro.

    Returns
    -------
    arregloProm : Retorna el arreglo de valores promedio para cada caso según las ejecuciones realizadas.

    '''
    arregloProm = np.zeros (pasos) #Se inicializa un arreglo de ceros
    for valor in range(pasos): #Se hace un contador recorrer el valor en cada paso
        suma=0
        for contadorArrelo in range(ejecuciones): 
            suma += conjunto[contadorArrelo][valor] 
        arregloProm[valor]=suma/len(conjunto) #En cada paso se calcula el promedio respecto a todas las ejecuciones y se guarda en el arreglo
        
    return arregloProm

def EnergiaInternaAnalitica(J, N, kB , T):
    '''
    Esta función calcula la energia interna de forma analítica respecto al valor de la temperatura.
    Parameters
    ----------
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.
    N : Corresponde al número de espines.
    kB : Representa la constante de Boltzmann, en donde se mantiene kB=1.
    T : Corresponde al valor de la temperatura.

    Returns
    -------
    valorU : Retorna el valor de la energía interna para la temperatura especificada.
    '''
    valorU=(-1)*J*N*np.tanh(J/(kB*T))
    
    return valorU

def CalorEspAnalitico(J, kB , T):
    '''
    Esta función calcula el calor específico de forma analítica respecto al valor de la temperatura.
    Parameters
    ----------
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.
    kB : Representa la constante de Boltzmann, en donde se mantiene kB=1.
    T : Corresponde al valor de la temperatura.

    Returns
    -------
    valorC : Retorna el valor del calor específico para la temperatura especificada.
    '''
    
    valorC=(J/(kB*T))**2/np.cosh(J/(kB*T))**2
    
    return valorC

def MagnetizacionAnalitica(J, N, kB , T , B):
    '''
    Esta función calcula la magnetización de forma analítica respecto al valor de la temperatura.
    Parameters
    ----------
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.
    N : Corresponde al número de espines.
    kB : Representa la constante de Boltzmann, en donde se mantiene kB=1.
    T : Corresponde al valor de la temperatura.
    B : Corresponde al campo magnético del sistema

    Returns
    -------
    valorM : Retorna el valor de la magnetización para la temperatura especificada.
    '''
    valorM=(N*np.exp(J/(kB*T))*np.sinh(B/(kB*T)))/(np.sqrt(np.exp(2*J/(kB*T))*np.sinh(B/(kB*T))**2+np.exp(-2*J/(kB*T))))
    
    return valorM
    
###############Simulación##################

#Se realiza una primera simulación para T=1 y 1000 pasos, para así definir la condición de equilibrio según el gráfico

nEspines=100
pasos=5000
J=1
T=1

estadosT, energiasT , magnetizacionesT , energiasEquilibrioT , magnetizacionesEquilibrioT , energiasCuadEquilibrioT = realizarSimulacion(nEspines,J,T,pasos)

#Se calculan el valor promedio de energía y magnetización, tomando los valores a partir del equilibrio para T=1

#energiaEquilibrio=np.sum(energiasEquilibrioT)/len(energiasEquilibrioT)
#magnetizacionEquilibrio=np.sum(magnetizacionesEquilibrioT)/len(magnetizacionesEquilibrioT)

#print("Energía Interna para T=1: " , energiaEquilibrio)
#print("Magnetización promedio después del equilibrio T=1: " , magnetizacionEquilibrio)


#Se hace una gráfica para observar el comportamiento de los espines para T=1
fig, ax = plt.subplots(figsize=(10,10) ,  dpi=120)
ax.set_title('Modelo Ising 1D para un kt=1')
ax.imshow(estadosT.T, 'plasma')
ax.set_xlabel('Pasos')
ax.set_ylabel('Espines')
ax.set_aspect('5')

#Se hace el gráfico de energías para T=1 y así poder establecer la condición de equilibrio
fig0, ax0 = plt.subplots(1, 1, dpi=150)
ax0.set_title('Modelo Ising 1D Energías vs. Pasos')
ax0.plot(energiasT, lw=0.5)

#Ahora se realiza la simulación para cada parámetro correspondiente reduciendo las fluctuaciones

repeticiones=25 #Se establecen cuántas ejecuciones se van a hacer
kB=1 #Se define kB=1

#B=0.01 #Se define el valor del campo magnético para la orientación positiva
#B=-0.01 #Se define el valor del campo magnético para la orientación negativa
B=0 #Se define el valor del campo magnético para la orientación aleatoria

valoresT = np.linspace(0.1,5,100) #Se establece el universo de valores de temperatura
#Se inicializan las listas correspondientes para almacenar los datos
listaEPromedio = []
listaMPromedio = []

listaUPromedio = []
listaMPromedioEquilibrio = []
listaU_2Promedio=[]
listaCalorEsp=[]

listaUAnalitica=[]
listaCalorEspAnalitico=[]
listaMagnetizacionAnalitica=[]

#Se recorre el universo de valores de temperatura
for temp in valoresT:
    #Se inicilizan las listas para guardar los valores correspondientes a cada repetición
    listaE = []
    listaM = []
    listaEquilibrioE = []
    listaEquilibrioM = []
    listaEquilibrioECuad = []
    #Se realizan las ejecuciones correspondientes
    for i in range(repeticiones):
        #Se realiza la simulación para la ejecución correspondiente
        resultadoEjecucion=realizarSimulacion(nEspines, 1,temp ,pasos)
        
        #Se guarda la longitud de pasos para cada parámetro y se guarda el resultado de la ejecución de cada parámetro
        #pasosE=len(resultadoEjecucion[1])
        #listaE.append(resultadoEjecucion[1])
        
        #pasosM=len(resultadoEjecucion[2])
        #listaM.append(resultadoEjecucion[2])
        
        pasosEquilibrioE=len(resultadoEjecucion[3])
        listaEquilibrioE.append(resultadoEjecucion[3])
        
        pasosEquilibrioM=len(resultadoEjecucion[4])
        listaEquilibrioM.append(resultadoEjecucion[4])
        
        pasosEquilibrioECuad=len(resultadoEjecucion[5])
        listaEquilibrioECuad.append(resultadoEjecucion[5])
        
    #Se establece el arreglo de arreglos de valores para cada parámetro
    #conjuntoE=np.array(listaE)
    #conjuntoM=np.array(listaM)
    conjuntoEquilibrioE=np.array(listaEquilibrioE)
    conjuntoEquilibrioM=np.array(listaEquilibrioM)
    conjuntoEquilibrioECuad=np.array(listaEquilibrioECuad)
    
    #Se reducen las fluctuaciones y se calculan los promedios de cada ejecución para cada paso
    #progresoE=ReduceYProm(conjuntoE, repeticiones, pasosE)
    #progresoM=ReduceYProm(conjuntoM, repeticiones, pasosM)
    progresoU=ReduceYProm(conjuntoEquilibrioE, repeticiones, pasosEquilibrioE)
    progresoEquilibrioM=ReduceYProm(conjuntoEquilibrioM, repeticiones, pasosEquilibrioM)
    progresoU_2=ReduceYProm(conjuntoEquilibrioECuad, repeticiones, pasosEquilibrioECuad)
    
    #Se calcula el promedio del parámetro para cada temperatura
    #promEnergiaT = np.sum(progresoE)/len(progresoE)
    #promMagnetizacionT=np.sum(progresoM)/len(progresoM)
    promUT = np.sum(progresoU)/len(progresoU)
    promMagnetizacionEquilibrioT=np.sum(progresoEquilibrioM)/len(progresoEquilibrioM)
    promU_2T=np.sum(progresoU_2)/len(progresoU_2)
    
    #Se calcula el calor específico utilizando los promedios de las energías correspondientes
    calorT=(1/nEspines**2)*(promU_2T-promUT**2)/temp**2
    
    #Se calculan la energía interna, el calor específico, y la magnetización de forma analítica
    energiaIntAnalitica=EnergiaInternaAnalitica(J, nEspines, kB, temp)
    calorEspAnalitico=CalorEspAnalitico(J, kB, temp)
    magnetizacionAnalitica=MagnetizacionAnalitica(J, nEspines, kB, temp, B)
    
    #Se guarda el valor obtenido para cada temperatura
    #listaEPromedio.append(promEnergiaT)
    #listaMPromedio.append(promMagnetizacionT)
    listaUPromedio.append(promUT)
    listaMPromedioEquilibrio.append(promMagnetizacionEquilibrioT)
    listaU_2Promedio.append(promU_2T)
    
    listaCalorEsp.append(calorT)
    
    listaUAnalitica.append(energiaIntAnalitica)
    listaCalorEspAnalitico.append(calorEspAnalitico)
    listaMagnetizacionAnalitica.append(magnetizacionAnalitica)

#Se grafican los resultados

# Gráfico Calor Específico Analítico y Simulación

fig3, ax3 = plt.subplots(dpi=120)

color = 'tab:red'
ax3.set_title('Modelo Ising 1D Calor Específico vs. T')
ax3.set_xlabel('kT')
ax3.set_ylabel('C analítico', color=color)
ax3.plot(valoresT, listaCalorEspAnalitico, color=color)
ax3.tick_params(axis='y', labelcolor=color)

ax4 = ax3.twinx()  

color = 'tab:blue'
ax4.set_ylabel('C simulación', color=color)  
ax4.plot(valoresT, listaCalorEsp, color=color)
ax4.tick_params(axis='y', labelcolor=color)

fig3.tight_layout()

# Gráfico Energía Interna analítica y simulación

fig5, ax5 = plt.subplots(dpi=120)

color = 'tab:red'
ax5.set_title('Modelo Ising 1D Energía Interna vs. T')
ax5.set_xlabel('kT')
ax5.set_ylabel('U analítica', color=color)
ax5.plot(valoresT, listaUAnalitica, color=color)
ax5.tick_params(axis='y', labelcolor=color)

ax6 = ax5.twinx()  

color = 'tab:blue'
ax6.set_ylabel('U simulación', color=color)  
ax6.plot(valoresT, listaUPromedio, color=color)
ax6.tick_params(axis='y', labelcolor=color)

fig5.tight_layout()

# Gráfico Magnetización analítica y simulación

fig7, ax7 = plt.subplots(dpi=120)

color = 'tab:red'
ax7.set_title('Modelo Ising 1D Magnetización vs. T')
ax7.set_xlabel('kT')
ax7.set_ylabel('M analítica', color=color)
ax7.plot(valoresT, listaMagnetizacionAnalitica, color=color)
ax7.tick_params(axis='y', labelcolor=color)

ax8 = ax7.twinx()  

color = 'tab:blue'
ax8.set_ylabel('M simulación', color=color)  
ax8.plot(valoresT, listaMPromedioEquilibrio, color=color)
ax8.tick_params(axis='y', labelcolor=color)

fig7.tight_layout()

plt.show()
