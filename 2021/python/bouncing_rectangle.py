"""
 Rebota un rectángulo contra las paredes.
   
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/ 
  
 Vídeo explicativo: http://youtu.be/-GmKoaX2iMs
"""
 
# Importamos la biblioteca Pygame
import pygame    
 
# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
  
pygame.init()
   
# Establecemos la altura y largo de la pantalla
dimensiones = [700, 500]
pantalla = pygame.display.set_mode(dimensiones)
  
pygame.display.set_caption("Rectángulo saltarín")
  
#Iteramos hasta que el usuario haga click sobre el botón de cerrar
hecho = False
  
# Usado para gestionar cuán rápido se actualiza la pantalla
reloj = pygame.time.Clock()
  
# Posición de partida del rectángulo
rect_x = 50
rect_y = 50
 
# Velocidad y dirección del rectángulo
rect_cambio_x = 2
rect_cambio_y = 2
 
 
 
# ----------------------- BUCLE PRINCIPAL-------------------------------------------------#
 
while not hecho:
    for evento in pygame.event.get():  # El usuario hizo algo
        if evento.type == pygame.QUIT: # Si el usuario hace click sobre cerrar
            hecho = True               # Marca que ya lo hemos hecho, de forma que abandonamos el bucle
 
    # --- Lógica del juego
    # Mueve el punto de partida del rectángulo
    rect_x += rect_cambio_x
    rect_y += rect_cambio_y
 
    # Rebota el rectángulo, si hace falta.
 
    if rect_x > 650 or rect_x < 0:          # Si el valor de x es mayor a 650 y menor a 0 píxeles,
        rect_cambio_x = rect_cambio_x * -1  # modifico la tasa de cambio, de positiva, a negativa. 
    if rect_y > 450 or rect_y < 0:          # Si el valor de y es mayor a 450 y menor a 0 píxeles,
        rect_cambio_y = rect_cambio_y * -1  # modifico la tasa de cambio, de positiva, a negativa. 
        
    # --- Dibujamos
    # Limpia la pantalla y establece su color de fondo
    pantalla.fill(NEGRO)
      
    # Dibujamos los Rectángulos    
    pygame.draw.rect(pantalla, BLANCO, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(pantalla, ROJO, [rect_x + 10, rect_y + 10, 30, 30])
 
    # --- Envolvemos todo
    # Limitamos a 60 fotogramas por segundo
    reloj.tick(60)
  
    # Avancemos y actualicemos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
      
# Pórtate bien con el IDLE. Si nos olvidamos de esta línea, el programa se 'colgará'
# en la salida.
pygame.quit()