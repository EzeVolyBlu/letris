#!/usr/bin/env python3

import math, os, random, sys

import pygame
from pygame.locals import *

from configuracion import *
from funciones import *
from extras import *


def main():
    # centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    # pygame.mixer.init()

    # preparar la ventana
    pygame.display.set_caption("LETRIS 2017")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    # Tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_INICIAL

    contadorAux=0
    tiempo=TIEMPO_MAX

    puntos = 0
    candidata = ""

    diccionario = lectura("paises.txt") #Cargo diccionario con el archivo nombres.txt
    tablero=creaTablero() #Por defecto crea un tablero de 10x10
    letra = nuevaLetra() #Asigna una letra aleatoria a la variable
    proximaLetra=nuevaLetra()
    posicion = nuevaPosicion(tablero) #guarda una posicion pseudoaleatoria del tablero

    letrasEnPantalla = []
    posicionesOcupadas=[]

    matrizPantalla=[letrasEnPantalla,posicionesOcupadas]



    while segundos > fps / 1000:
        # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()

        fps = 3

        # buscar la tecla presionada del modulo de eventos de pygame
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            # ver si se presiono alguna tecla
            """
            OBSERVA SI SE PRESIONA TECLA
            """
            if e.type == KEYDOWN:
                direccion = dameTeclaApretada(e.key)
                #Obtengo las coordenadas a donde INTENTO ir
                destino = direccionAPosicion(posicion,direccion)

                #Pregunto si puedo ocupar ese lugar
                if(puedeMover(destino,tablero)):

                    #En caso positivo actualizo el tablero y la posicion
                    tablero=moverLetra(posicion, destino, tablero)
                    posicion=destino
                    #Si no se puede no hacemos nada

        acierto=''
        segundos = tiempo - pygame.time.get_ticks() / 1000


        #Como se actualiza cada 1/3'', cada 3 unidades hacemos que baje la letra
        """
        CUENTA 1 SEGUNDO
        """
        if(contadorAux>=fps):

            #Nuevamente cargamos las coordenadas a donde queremos ir, no ponemos la direccion porque
            #por defecto baja
            destino = direccionAPosicion(posicion)

            #Si puede mover, se actualiza tablero y posicion
            """
            PUEDE BAJAR
            """
            if(puedeMover(destino,tablero)):

                tablero=moverLetra(posicion, destino, tablero)
                posicion=destino
                """
                NO PUEDE BAJAR
                """
            else:
                #De lo contrario, guardamos la letra y la posicion  tanto en el tablero como en la matriz pantalla
                tablero[posicion[0]][posicion[1]]=letra

                letrasEnPantalla.append(letra)
                posicionesOcupadas.append(posicion)

                matrizPantalla[0]=letrasEnPantalla
                matrizPantalla[1]=posicionesOcupadas


                #Armo una lista de candidatas de la fila donde cae la letra
                aciertosInicioFin=devuelveAciertosInicioFin(posicion,tablero,diccionario)
                listaAciertos=aciertosInicioFin[0]


                #Creamos una variable con la cantidad de aciertos, si es mayor a 0
                # 'Limpiamos' la zona de la palabra

                cantidadAciertos=len(listaAciertos)

                """
                HUBIERON ACIERTOS
                """
                if(cantidadAciertos>0):

                    #Sumamos puntos y tiempo
                    puntos=puntos+puntuar(listaAciertos)
                    tiempo=tiempo+puntos

                    #Delimitamos la zona a actualizar
                    inicioFinZona=aciertosInicioFin[1]

                    #La funcion actualizar renueva las filas del tablero y la matriz pantalla cuando hay un acierto
                    datos=actualizar(matrizPantalla, posicion[0], inicioFinZona, tablero)
                    matrizPantalla=datos[0]
                    tablero=datos[1]

                    #La funcion muestraAciertos muestra en pantalla el acierto
                    acierto=muestraAciertos(listaAciertos)


                """
                NUEVA LETRA
                """
                letra = proximaLetra
                proximaLetra=nuevaLetra()
                posicion=nuevaPosicion(tablero)


            contadorAux=0

        contadorAux+=1

        # limpiar pantalla anterior
        screen.fill(COLOR_FONDO)
        dibujar(screen, letra, posicion, matrizPantalla, puntos, segundos,proximaLetra,acierto)
        pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    main()
