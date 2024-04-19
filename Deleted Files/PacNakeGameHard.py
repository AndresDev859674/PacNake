import pygame
import sys
import random
from pypresence import Presence
import time
import threading

icono = pygame.image.load("hard_mode_logo.png")
pygame.display.set_icon(icono)

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacNake Game 1.0.3 Hard Mode")

# Colores
white = (255, 255, 255)

# Cargar imágenes
background_img = pygame.image.load("background hard.jpg")
head_img = pygame.image.load("snake_head.png")
body_img = pygame.image.load("snake_demon.png")
food_img = pygame.image.load("food_green.png")

# Cargar música
pygame.mixer.music.load("background_music_hard.mp3")
pygame.mixer.music.play(-1)  # -1 significa reproducción en bucle
music_enabled = True  # Variable para controlar si la música está activada o desactivada

# Tamaño de los bloques
block_size = 20

# Velocidad de la serpiente
snake_speed = 25

# Función para mostrar la serpiente en la pantalla
def draw_snake(snake):
    for segment in snake:
        screen.blit(body_img, (segment[0], segment[1]))


# Función para mostrar el texto en la pantalla
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Función del menú principal
def main_menu():
    global music_enabled  # Declarar la variable global

    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_running = False  # Iniciar juego al presionar 'S'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()  # Salir del juego al presionar 'Q'
                elif event.key == pygame.K_c:
                    music_enabled = not music_enabled  # Alternar la variable de música al presionar 'C'

        screen.blit(background_img, (0, 0))
        draw_text("PacNake Hard", 70, white, width // 2 - 150, height // 2 - 100)
        draw_text("Press 'S' to start", 30, white, width // 2 - 150, height // 2)
        draw_text("Press 'Q' to quit", 30, white, width // 2 - 150, height // 2 + 50)
        draw_text("Press 'C' to toggle music", 30, white, width // 2 - 200, height // 2 + 100)
        draw_text("Music: " + ("ON" if music_enabled else "OFF"), 30, white, width // 2 - 200, height // 2 + 150)

        pygame.display.flip()

# Función principal del juego
def game():
    global music_enabled  # Declarar la variable global
    clock = pygame.time.Clock()

    main_menu()

    while True:
        # Inicializar la serpiente
        snake = [(width // 2, height // 2)]
        snake_direction = (block_size, 0)

        # Inicializar la posición de la comida
        food = (random.randrange(0, width - block_size, block_size),
                random.randrange(0, height - block_size, block_size))

        # Inicializar el puntaje y el tiempo
        score = 0
        start_time = time.time()

        game_over = False
        paused = False

        # Configurar la música según la variable de música
        if music_enabled:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_m:
                        main_menu()  # Volver al menú principal al presionar 'M'

            if paused:
                draw_text("Paused", 70, white, width // 2 - 100, height // 2 - 30)
                draw_text("Press 'M' to return to menu", 30, white, width // 2 - 200, height // 2 + 30)
                pygame.display.flip()
                clock.tick(5)  # Reducir la velocidad del bucle al estar pausado
                continue

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and snake_direction != (0, block_size):
                snake_direction = (0, -block_size)
            elif keys[pygame.K_DOWN] and snake_direction != (0, -block_size):
                snake_direction = (0, block_size)
            elif keys[pygame.K_LEFT] and snake_direction != (block_size, 0):
                snake_direction = (-block_size, 0)
            elif keys[pygame.K_RIGHT] and snake_direction != (-block_size, 0):
                snake_direction = (block_size, 0)

            # Actualizar la posición de la serpiente
            snake[0] = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

            # Verificar colisiones con la comida
            if snake[0] == food:
                snake.append((-block_size, -block_size))  # Agregar un nuevo segmento a la serpiente
                food = (random.randrange(0, width - block_size, block_size),
                        random.randrange(0, height - block_size, block_size))
                score += 10  # Incrementar el puntaje por cada pieza de comida

            # Verificar colisiones con los bordes
            if snake[0][0] < 0 or snake[0][0] >= width or snake[0][1] < 0 or snake[0][1] >= height:
                game_over = True

            # Verificar colisiones consigo misma
            for segment in snake[1:]:
                if snake[0] == segment:
                    game_over = True

            # Mover el cuerpo de la serpiente
            snake[1:] = snake[:-1]

            # Dibujar en la pantalla
            screen.blit(background_img, (0, 0))
            screen.blit(food_img, food)
            draw_snake(snake)
            draw_text(f"Score: {score}", 30, white, 10, 10)

            pygame.display.flip()

            # Establecer la velocidad de actualización
            clock.tick(snake_speed)

        # Calcular el tiempo transcurrido
        end_time = time.time()
        elapsed_time = round(end_time - start_time)

        # Mostrar pantalla de Game Over con puntaje y tiempo
        draw_text("Game Over", 70, white, width // 2 - 150, height // 2 - 30)
        draw_text(f"Score: {score}", 30, white, width // 2 - 80, height // 2 + 30)
        draw_text(f"Time: {elapsed_time} seconds", 30, white, width // 2 - 120, height // 2 + 80)
        draw_text("Press 'R' to restart", 30, white, width // 2 - 150, height // 2 + 130)
        draw_text("Press 'M' to return to menu", 30, white, width // 2 - 200, height // 2 + 180)
        pygame.display.flip()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_restart = False
                    elif event.key == pygame.K_m:
                        main_menu()  # Volver al menú principal al presionar 'M'

if __name__ == "__main__":
    game()