import pygame
import sys
import random
from pypresence import Presence
import time

# ... (Código anterior)

# Función para mostrar la serpiente en la pantalla
def draw_snake(snake):
    for segment in snake:
        screen.blit(body_img, (segment[0], segment[1]))

# Función para mostrar el texto en la pantalla
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Resto del código...

icono = pygame.image.load("food_logo.png")
pygame.display.set_icon(icono)

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacNake Game 1.0.3")

# Colores
white = (255, 255, 255)

# Cargar imágenes
background_img = pygame.image.load("background.jpg")
head_img = pygame.image.load("snake_head.png")
body_img = pygame.image.load("snake_body.png")
food_img = pygame.image.load("food.png")

# Cargar música
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # -1 significa reproducción en bucle
music_enabled = True  # Variable para controlar si la música está activada o desactivada

# Tamaño de los bloques
block_size = 20

# Velocidad de la serpiente
snake_speed = 15

# Configuración de Discord RPC
client_id = "1200235628781117561"
RPC = Presence(client_id)
RPC.connect()

# Detalles y estado iniciales del RPC
details = "Playing PacNake"
state = "This is a Test in the Game Code"
      
# Inicializar el estado de Discord RPC
RPC.update(
    details=details,
    state=state,
    large_image="icon",  # Reemplaza con el nombre de tu imagen grande
    large_text="PacNake Game",
    small_image="edit",  # Reemplaza con el nombre de tu imagen pequeña
    small_text="A Test of the Game Code"
)

# Función para actualizar el estado del RPC
def update_rpc(details, state, large_image, large_text, small_image, small_text):
    RPC.update(
        details=details,
        state=state,
        large_image=large_image,
        large_text=large_text,
        small_image=small_image,
        small_text=small_text
    )

# Función para mostrar la serpiente en la pantalla
def draw_snake(snake):
    for segment in snake:
        screen.blit(body_img, (segment[0], segment[1]))

# ... (código anterior)

# Función para mostrar las manzanas comidas en la pantalla
def draw_apples(apples):
    for apple in apples:
        screen.blit(food_img, apple)

# ... (código anterior)


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
        draw_text("PacNake Game", 70, white, width // 2 - 150, height // 2 - 100)
        draw_text("Press 'S' to start", 30, white, width // 2 - 150, height // 2)
        draw_text("Press 'Q' to quit", 30, white, width // 2 - 150, height // 2 + 50)
        draw_text("Press 'C' to toggle music", 30, white, width // 2 - 200, height // 2 + 100)
        draw_text("Music: " + ("ON" if music_enabled else "OFF"), 30, white, width // 2 - 200, height // 2 + 150)

        pygame.display.flip()

# ... (código anterior)

def generate_food_position(snake):
    # Generar una posición aleatoria para la manzana que no esté en la serpiente
    while True:
        food = (random.randrange(0, width - block_size, block_size),
                random.randrange(0, height - block_size, block_size))
        if food not in snake:
            return food

# Función principal del juego
def game():
    global music_enabled  # Declarar la variable global
    clock = pygame.time.Clock()

    while True:
        main_menu()  # Mover la llamada al menú principal al bucle principal del juego

        # Inicializar la serpiente
        snake = [(width // 2, height // 2)]
        snake_direction = (block_size, 0)

        # Inicializar la lista de manzanas
        apples = [generate_food_position(snake) for _ in range(3)]

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
                        return  # Salir del juego y volver al menú principal al presionar 'M'

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

            # Verificar colisiones con las manzanas
            for apple in apples:
                if snake[0] == apple:
                    snake.append((-block_size, -block_size))  # Agregar un nuevo segmento a la serpiente
                    apples.remove(apple)  # Eliminar la manzana comida
                    apples.append(generate_food_position(snake))  # Agregar una nueva manzana
                    score += 10  # Incrementar el puntaje por cada manzana comida

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
            draw_apples(apples)  # Dibujar las manzanas
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
                        return  # Salir del juego y volver al menú principal al presionar 'M'

if __name__ == "__main__":
    game()