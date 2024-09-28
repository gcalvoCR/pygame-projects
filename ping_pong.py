
import pygame
pygame.font.init()

################# Colores #################
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
AZUL = (0,0,255)

############## Configuracion ##############
VEL = 5
FPS = 60

SIZE_PANTALLA = WIDTH_PANTALLA, HEIGHT_PANTALLA = 900, 500
SIZE_JUGADOR = WIDTH_JUGADOR, HEIGHT_JUGADOR = 20, 80
SIZE_BALLON = WIDTH_BALLON, HEIGHT_BALLON = 20, 20

############### Constantes ################
R = "R" # rojo
N = "N" # negro
DIRECCION_POSITIVA = "positiva"  # para direcciones 
DIRECCION_NEGATIVA = "negativa" # para direcciones

# inicializacion de objetos principales
pantalla = pygame.display.set_mode(SIZE_PANTALLA)
pygame.display.set_caption("PING PONG")
font = pygame.font.SysFont('roboto', 20)
jugador_rojo = pygame.Rect(100 - WIDTH_JUGADOR, HEIGHT_PANTALLA//2 - HEIGHT_JUGADOR//2, 20, 100)
jugador_negro = pygame.Rect(WIDTH_PANTALLA - 100, HEIGHT_PANTALLA//2 - HEIGHT_JUGADOR//2, 20, 100)
bola = pygame.Rect(jugador_rojo.x + WIDTH_JUGADOR, jugador_rojo.y + HEIGHT_JUGADOR//2, WIDTH_BALLON, HEIGHT_BALLON)


def dibujar_elementos(jugador_rojo, jugador_negro, bola, puntaje_rojo, puntaje_negro):
    pantalla.fill(BLANCO)
    
    texto_rojo = font.render("Puntos Rojo: " + str(puntaje_rojo), 1, NEGRO)
    texto_negro = font.render("Puntos Negro: " + str(puntaje_negro), 1, NEGRO)
    
    pantalla.blit(texto_rojo, (10, 10))
    pantalla.blit(texto_negro, (WIDTH_PANTALLA - texto_negro.get_width() - 10, 10))
    
    # dibujar elementos
    pygame.draw.rect(pantalla, ROJO, jugador_rojo)
    pygame.draw.rect(pantalla, NEGRO, jugador_negro)
    pygame.draw.rect(pantalla, AZUL, bola)
    
    pygame.display.update() # volver a renderizar la vista


def handle_jugador(keys_pressed, jugador, turno, es_posicion_inicial, tecla_arriba, tecla_abajo, turno_actual):
    """Maneja el movimiento del jugador"""
    if keys_pressed[tecla_arriba] and jugador.y >= 0:
        jugador.y -= VEL
        if es_posicion_inicial and turno == turno_actual:
            bola.y -= VEL
    if keys_pressed[tecla_abajo] and jugador.y + HEIGHT_JUGADOR <= HEIGHT_PANTALLA:
        jugador.y += VEL
        if es_posicion_inicial and turno == turno_actual:
            bola.y += VEL


def mover_bola(direccion_x, direccion_y):
    """Mueve la bola y actualiza la dirección si choca con las paredes"""
    if direccion_x == DIRECCION_POSITIVA:
        bola.x += 5
        if bola.x + WIDTH_BALLON >= WIDTH_PANTALLA:
            direccion_x = DIRECCION_NEGATIVA
    else:
        bola.x -= 5
        if bola.x <= 0:
            direccion_x = DIRECCION_POSITIVA

    if direccion_y == DIRECCION_POSITIVA:
        bola.y += 4
        if bola.y + HEIGHT_BALLON >= HEIGHT_PANTALLA:
            direccion_y = DIRECCION_NEGATIVA
    else:
        bola.y -= 4
        if bola.y <= 0:
            direccion_y = DIRECCION_POSITIVA

    return direccion_x, direccion_y


def chequear_colisiones(jugador_rojo, jugador_negro, direccion_x):
    """Cambia la dirección de la bola si hay una colisión con los jugadores"""
    if jugador_negro.colliderect(bola):
        direccion_x = DIRECCION_NEGATIVA
    if jugador_rojo.colliderect(bola):
        direccion_x = DIRECCION_POSITIVA
    return direccion_x


def mover_bola_con_jugador(turno, jugador_rojo, jugador_negro):
    """Mueve la bola con el respecto a la posición del jugador"""
    # global bola  # para modificar la posición de la bola
    if turno == R:
        bola.x = jugador_rojo.x + WIDTH_JUGADOR
        bola.y = jugador_rojo.y + HEIGHT_JUGADOR // 2
    else:
        bola.x = jugador_negro.x - WIDTH_JUGADOR
        bola.y = jugador_negro.y + HEIGHT_JUGADOR // 2


def manejar_puntaje(bola, puntaje_rojo, puntaje_negro, turno):
    """Maneja el puntaje cuando la bola cruza los límites de la pantalla"""
    es_posicion_inicial = False
    if bola.x + WIDTH_BALLON >= WIDTH_PANTALLA:
        puntaje_rojo += 1
        turno = R
        es_posicion_inicial = True
    elif bola.x <= 0:
        puntaje_negro += 1
        turno = N
        es_posicion_inicial = True
    
    return puntaje_rojo, puntaje_negro, turno, es_posicion_inicial


def jugar():
    clock = pygame.time.Clock()
    
    running = True
    
    # variables iniciales
    puntaje_rojo = 0
    puntaje_negro = 0
    turno = R  # R: rojo, N: Negro
    es_posicion_inicial = True
    direccion_x = DIRECCION_POSITIVA
    direccion_y = DIRECCION_POSITIVA
    
    while running:
        clock.tick(FPS)  # controlamos la velocidad del loop
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LMETA and turno == R:
                es_posicion_inicial = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RMETA and turno == N:
                es_posicion_inicial = False
        
        keys_pressed = pygame.key.get_pressed()
        handle_jugador(keys_pressed, jugador_rojo, turno, es_posicion_inicial, pygame.K_w, pygame.K_s, R)
        handle_jugador(keys_pressed, jugador_negro, turno, es_posicion_inicial, pygame.K_UP, pygame.K_DOWN, N)

        if es_posicion_inicial:
            mover_bola_con_jugador(turno, jugador_rojo, jugador_negro)
        else:
            direccion_x, direccion_y = mover_bola(direccion_x, direccion_y)
            puntaje_rojo, puntaje_negro, turno, es_posicion_inicial = manejar_puntaje(bola, puntaje_rojo, puntaje_negro, turno)
            direccion_x = chequear_colisiones(jugador_rojo, jugador_negro, direccion_x)
        
        dibujar_elementos(jugador_rojo, jugador_negro, bola, puntaje_rojo, puntaje_negro)
    
    pygame.quit()


if __name__ == "__main__":
    jugar()