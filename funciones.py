from configuracion import *
from principal import *
from extras import *
import math
import random
import string

# Cargar en listaPalabras las palabras del archivo.
def lectura(archivo):

    data = open(archivo)
    listaPalabras = data.readlines()
    c=0

    for palabra in listaPalabras:

        listaPalabras[c]=(palabra[:-1]).upper()
        c+=1

    data.close

    return listaPalabras

""""""""""""""""""""""""""""""""""""

# Puntua la palabra.
def puntuar(listaAciertos):

    ctdadVocales = 0
    ctdadDificiles = 0
    ctdadConsonantes = 0

    for palabra in listaAciertos:

        for l in palabra:
            if (l=='A' or l=='E' or l=='I' or l=='O' or l=='U'):
                ctdadVocales += 1
            else:
                if (l=='J' or l=='K' or l=='Q' or l=='W' or l=='X' or l=='Y' or l=='Z'):
                    ctdadDificiles +=1
                else:
                    ctdadConsonantes +=1


    puntaje=(ctdadVocales*1)+(ctdadDificiles*5)+(ctdadConsonantes*2)

    return puntaje

""""""""""""""""""""""""""""""""""""

# Mueve la letra hacia la izquierda, derecha, o hacia abajo.

def moverLetra(posicion, destino, tablero):

    filaPosicion=posicion[0]
    columnaPosicion=posicion[1]

    filaDestino=destino[0]
    columnaDestino=destino[1]

    letra=tablero[filaPosicion][columnaPosicion]

    tablero[filaPosicion][columnaPosicion]=""
    tablero[filaDestino][columnaDestino]=letra

    return tablero

""""""""""""""""""""""""""""""""""""

# Devuelve una letra del abecedario al azar.
def nuevaLetra():

    vocales='AEIOU'
    consonantes='BCDFGHILMNÃ‘PRST'
    dificiles='KWYZ'

    coeficiente=random.randint(0,9)
    letra=''
    if(0<=coeficiente<5):
        letra=random.choice(vocales)
    else:
        if(5<=coeficiente<8):
            letra=random.choice(consonantes)
        else:
            if(8<=coeficiente<10):
                letra=random.choice(dificiles)

    return letra

""""""""""""""""""""""""""""""""""""

# Inventa una posicion. Por ejemplo: (x, y) x al azar e y bien arriba de

def nuevaPosicion(tablero):

    posicion=[0,random.randrange(0,len(tablero)-1)]
    #Genero una 'x' aleatoria

    return posicion

""""""""""""""""""""""""""""""""""""

# Recorre una lista con los aciertos (si los hubiera)
# y devuelve un string concatenandolos

def muestraAciertos(listaAciertos):
    acierto=''
    for aciertos in listaAciertos:
        acierto=acierto + aciertos + " "

    return acierto

""""""""""""""""""""""""""""""""""""

# Recorre una fila del tablero para atras y adelante tomando como partida
# la columna donde cae la letra. Delimita la zona del string a analizar
# y devuelve una lista con la primera y ultima posicion

def delimitaInicioFin(tablero, filaPalabra, columnaLetra):

    primeraPosicion=0
    ultimaPosicion=len(tablero)-1

    for l in range(primeraPosicion,columnaLetra):

        if(tablero[filaPalabra][l]==''):
            primeraPosicion=l+1


    for l in range(ultimaPosicion, columnaLetra,-1):

        if(tablero[filaPalabra][l]==''):
            ultimaPosicion=l-1

    inicioFin=[primeraPosicion,ultimaPosicion]

    return inicioFin


""""""""""""""""""""""""""""""""""""

# Utiliza inicioFin para delimitar una zona, armar combinaciones de palabras y
# devolver una lista de listas con [0] candidatas [1] inicioFin correspondiente

def armarPalabra(posicion, tablero):


    filaPalabra=posicion[0]
    columnaLetra=posicion[1]

    inicioFin=delimitaInicioFin(tablero, filaPalabra, columnaLetra)

    primeraPosicion=inicioFin[0]
    ultimaPosicion=inicioFin[1]

    # Con la zona de palabra debemos formar todas las combinaciones posibles de +1 letra y guardarlas en una lista

    listaCandidatas=[]
    listaPosiciones=[]

    auxPrimeraPos=primeraPosicion

    # Recorro desde la primera posicion hasta la ultima (esta la descartamos)
    for l in range (primeraPosicion,ultimaPosicion):

        candidata=""
        # Recorro desde la primera posicion hasta la ultima inclusive
        for j in range(auxPrimeraPos, ultimaPosicion+1):

            # A medida que recorro
            candidata=candidata+(tablero[filaPalabra][j])

            if(len(candidata)>1):
                auxPosicion=[l,ultimaPosicion]
                listaCandidatas.append(candidata)
                listaPosiciones.append(auxPosicion)

        auxPrimeraPos+=1

    candidatasInicioFin=[listaCandidatas,listaPosiciones]



    return candidatasInicioFin

""""""""""""""""""""""""""""""""""""

#Recibe los candidatos con las posiciones de armarPalabra,
#las compara con un diccionario, y devuelve una lista de listas con
# [0] aciertos [1] minInicioMaxFin

def compara(candidatasPosiciones, diccionario):

    aciertos=[]
    posicionAcierto=[]

    indicePosiciones=0

    listaCandidatos=candidatasPosiciones[0]
    listaPosiciones=candidatasPosiciones[1]

    inicioAcierto=100
    finAcierto=0


    # Recorro lista de palabras
    for candidata in listaCandidatos:


        #Por cada palabra, recorro el diccionario
        for palabra in diccionario:

            #Si hay coincidencia agrego la palabra a mi lista de aciertos
            if(candidata==palabra):
                aciertos.append(candidata)


                posicionAcierto=listaPosiciones[indicePosiciones]
               # inicioAux=listaPosiciones[indicePosiciones][0]
                #finAux=listaPosiciones[indicePosiciones][1]

                #Se queda con la posicion mas alejada
                if(posicionAcierto[0]<inicioAcierto):
                    inicioAcierto=posicionAcierto[0]

                #Se queda con la posicion mas alejada
                if(posicionAcierto[1]>finAcierto):
                    finAcierto=posicionAcierto[1]

        indicePosiciones+=1

    aciertosConZona=[]
    aciertosConZona.append(aciertos)
    aciertosConZona.append(posicionAcierto)

    return aciertosConZona

""""""""""""""""""""""""""""""""""""

#Une armarPalabra y compara

def devuelveAciertosInicioFin(posicion,tablero,diccionario):

    candidatasInicioFin=armarPalabra(posicion,tablero)
    aciertosInicioFin=compara(candidatasInicioFin,diccionario)

    return aciertosInicioFin

""""""""""""""""""""""""""""""""""""

# Crea un tablero de 10x10 por defecto

def creaTablero(filas=10,columnas=10):

    tablero=[]
    for i in range (filas):
        tablero.append([""]*columnas)

    return tablero

""""""""""""""""""""""""""""""""""""

# Recibe una posicion y una direccion y devuelve
# una lista con coordenadas de destino

def direccionAPosicion(posicion,direccion='down'):

    filaDestino=posicion[0]
    columnaDestino=posicion[1]

    if(direccion=='down'):
        filaDestino+=1
    else:
        if(direccion=='left'):
            columnaDestino-=1
        else:
            if(direccion=='right'):
                columnaDestino+=1

    destino=[filaDestino,columnaDestino]

    return destino

""""""""""""""""""""""""""""""""""""

#Devuelve False si la posicion destino sale de los limites

def dentroDeLimites(destino,tablero):

    bandera=False
    filaDestino=destino[0]
    columnaDestino=destino[1]

    maximoFilaPermitido=(len(tablero))-1
    maximoColumnasPermitido=(len(tablero[0]))-1


    if( (0<=filaDestino<=maximoFilaPermitido)  and  (0<=columnaDestino<=maximoColumnasPermitido)  ):

        bandera=True

    return bandera

""""""""""""""""""""""""""""""""""""

#Devuelve False si la posicion destino esta ocupada

def posicionVacia(destino, tablero):

    bandera=True

    filaDestino=destino[0]
    columnaDestino=destino[1]

    contenidoDestino=tablero[filaDestino][columnaDestino]

    if(contenidoDestino!=""):

        bandera=False

    return bandera

""""""""""""""""""""""""""""""""""""

# Verifica que la posicion destino este dentro de los limites
# y libre para ocupar

def puedeMover(destino, tablero):

    bandera=False

    if(dentroDeLimites(destino,tablero)):
        if(posicionVacia(destino,tablero)):
            bandera=True

    return bandera

""""""""""""""""""""""""""""""""""""

# La funcion mas compleja, devuelve una lista de listas de listas
# barre hace arriba el tablero y la pantalla

def actualizar(matrizPantalla, filaAcierto, inicioFin, tablero):

    letrasEnPantalla=matrizPantalla[0]
    posicionesOcupadas=matrizPantalla[1]

    inicio=inicioFin[0]
    fin=inicioFin[1]

    #Recorremos desde la primera columna hasta la ultima que vamos a limpiar

    while(inicio<=fin):

        filaAux=filaAcierto
        letra=tablero[filaAux][inicio]

        while(letra!='' and filaAux>0):
            #Buscamos las posiciones de cada letra
            posicionBuscada=[filaAux,inicio]
            #Tenemos la posicion en la lista de las letras y sus respectivas coordenadas
            indice=posicionesOcupadas.index(posicionBuscada)

            #Creamos una variable que tenga el contenido de la celda de arriba
            #Si arriba no hay nada debemos eliminar la posicion, sino reemplazamos
            contenidoArriba=tablero[filaAux-1][inicio]

            if(contenidoArriba!=''):
                #Arriba hay una letra, debemos 'tomar' su contenido
                letrasEnPantalla[indice]=contenidoArriba
                tablero[filaAux][inicio]=contenidoArriba
            else:
                letrasEnPantalla.pop(indice)
                posicionesOcupadas.pop(indice)
                tablero[filaAux][inicio]=''

            #'Subo' una fila y repito la operacion hasta que no quede nada,
            # ahi se saldra del bucle y se avanza en la sig. columna

            filaAux-=1
            letra=tablero[filaAux][inicio]

        inicio+=1

    matrizPantalla=[letrasEnPantalla,posicionesOcupadas]
    datos=[matrizPantalla,tablero]

    return datos


