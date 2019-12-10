import pygame
from pygame.locals import *
from configuracion import *

def dameTeclaApretada(key):
    if key == K_UP or key == K_k:
        return "up"
    elif key == K_DOWN or key == K_j:
        return "down"
    elif key == K_RIGHT or key == K_l:
        return "right"
    elif key == K_LEFT or key == K_h:
        return "left"
    else:
        return ""

def dibujar(screen, letra, posicion, matrizPantalla, puntos, segundos,proximaLetra,aciertos):

    letrasEnPantalla=matrizPantalla[0]
    posiciones=matrizPantalla[1]

    defaultFont = pygame.font.Font(pygame.font.get_default_font(), TAMANO_LETRA)
    defaultFontGRANDE = pygame.font.Font(pygame.font.get_default_font(), TAMANO_LETRA_GRANDE)

    pygame.draw.line(screen, (255, 255, 255), (0, ALTO - 70), (ANCHO, ALTO - 70), 5)

    ren1 = defaultFont.render("Puntos: " + str(puntos), 1, COLOR_TEXTO)
    ren2 = defaultFont.render("Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL if segundos < 15 else COLOR_TEXTO)
    ren3 = defaultFontGRANDE.render(letra, 1, COLOR_LETRA)
    ren4 = defaultFont.render("Prox. letra: " + proximaLetra, 1, COLOR_TEXTO)
    ren5 = defaultFont.render( aciertos , 1, COLOR_TIEMPO_FINAL)

    # Estos coeficientes 'regulan' la ubicacion de las letras en el tablero. Lo ideal (*) seria que tomaran su valor
    # en funcion de la cantidad de filas y columnas tenga el tablero

    col=38
    fil=30

    i = 0
    while i < len(letrasEnPantalla):
        posicionLetra=posiciones[i]
        screen.blit(defaultFontGRANDE.render(letrasEnPantalla[i], 1, COLOR_TEXTO), (10 + posicionLetra[1]*col, 50 + posicionLetra[0]*fil))
        i += 1

    screen.blit(ren1, (ANCHO - 120, 10))
    screen.blit(ren2, (10, 10))
    screen.blit(ren3, (10 + posicion[1]*col, 50 + posicion[0]*fil))
    screen.blit(ren4, (10, 400))
    screen.blit(ren5, (ANCHO - 120, 400))
