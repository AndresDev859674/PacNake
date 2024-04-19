import pygame
import pygame_menu
import sys
import random
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import psutil
from pypresence import Presence
import tkinter.messagebox as messagebox

icono = pygame.image.load("food_logo.png")
pygame.display.set_icon(icono)

# Inicializar Pygame
pygame.init()

# Obtener la información de la CPU y la RAM
cpu_info = f"{psutil.cpu_freq().current / 1000:.2f} GHz {psutil.cpu_count(logical=False)} cores"
ram_info = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB RAM"

# Configuración de la pantalla
width, height = 600, 400
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"PacNake Game - CPU: {cpu_info}, RAM: {ram_info}")

# El resto del código sigue siendo el mismo...

# El resto del código sigue siendo el mismo...

# Colores
white = (255, 255, 255)

# Cargar imágenes
background_img = pygame.image.load("background.jpg")
head_img = pygame.image.load("snake_head.png")
body_img = pygame.image.load("snake_body.png")
food_img = pygame.image.load("food.png")

# Cargar música predeterminada
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # -1 significa reproducción en bucle
music_enabled = True  # Variable para controlar si la música está activada o desactivada

# Tamaño de los bloques
block_size = 20

# Velocidad de la serpiente
snake_speed = 15

# Incremento de puntaje por defecto
score_increment = 10

# Crear un nuevo tema basado en el tema por defecto
my_theme = pygame_menu.themes.THEME_DARK.copy()

# Modificar el estilo del título para que no tenga sombra
my_theme.title_font_shadow = False

# Cambiar el color de fondo del menú principal
my_theme.background_color = (30, 30, 30)  # Fondo oscuro

# Variable para almacenar el nombre del jugador
player_name = ""

# Definir la variable global discord_rpc_enabled
discord_rpc_enabled = False

# Establece el client_id aquí
client_id = "1200235628781117561"
RPC = Presence(client_id)

def update_discord_presence():
    global discord_rpc_enabled
    if discord_rpc_enabled:
        RPC.update(
            details="Playing PacNake",
            state="In a game",
            large_image="icon",
            small_image="food"
        )

# Function to enable or disable Discord RPC
def toggle_discord_rpc(enabled):
    global discord_rpc_enabled
    discord_rpc_enabled = enabled
    if discord_rpc_enabled:
        RPC.connect()
        messagebox.showinfo("Discord RPC Enabled", "Discord RPC has been enabled.")
    else:
        RPC.clear()
        RPC.close()
        messagebox.showinfo("Discord RPC Disabled", "Discord RPC has been disabled.")

# Función para mostrar la serpiente en la pantalla
def draw_snake(snake):
    for segment in snake:
        surface.blit(body_img, (segment[0], segment[1]))

# Función para mostrar el texto en la pantalla
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    surface.blit(render, (x, y))

# Función para obtener la cadena de FPS formateada con información de CPU y RAM
def get_fps_string(clock):
    cpu_info = f"{psutil.cpu_freq().current / 1000:.2f} GHz {psutil.cpu_count(logical=False)} cores"
    ram_info = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB RAM"
    return f"PacNake Game - FPS: {int(clock.get_fps())} - CPU: {cpu_info}, RAM: {ram_info}"

# Función principal del juego
def game():
    global music_enabled, snake_speed, player_name, score, round_num, apples_eaten, start_time  # Agrega start_time a las variables globales
    start_time = time.time()  # Define start_time al comienzo de la función
    clock = pygame.time.Clock()
    # El resto del código permanece sin cambios

    # Inicializar la serpiente
    snake = [(width // 2, height // 2)]
    snake_direction = (block_size, 0)

    # Inicializar la posición de la comida
    food = (random.randrange(0, width - block_size, block_size),
            random.randrange(0, height - block_size, block_size))

    # Inicializar el puntaje, número de rondas y manzanas comidas
    score = 0
    round_num = 1  # Inicializar el número de ronda
    apples_eaten = 0

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
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Si se presiona "Shift" + "M", cargar música desde el dispositivo
                        pygame.mixer.music.stop()
                        select_music()
                    else:
                        # Si se presiona "M", activar/desactivar la música del juego
                        music_enabled = not music_enabled
                        if music_enabled:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                        tk.Tk().withdraw()  # Ocultar la ventana principal
                        messagebox.showinfo('Music', 'Music ' + ('enabled' if music_enabled else 'disabled'))

        if paused:
            draw_text("Paused", 70, white, width // 2 - 100, height // 2 - 30)
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
            score += score_increment  # Incrementar el puntaje por cada pieza de comida
            apples_eaten += 1  # Incrementar el contador de manzanas comidas

            # Comprobar si el puntaje alcanza el umbral para la próxima ronda
            if score == 50:
                round_num = 1.5
            elif score == 100:
                round_num = 2
            elif score == 200:
                round_num = 3
            elif score == 300:
                round_num = 4
            elif score == 400:
                round_num = 5
            elif score == 500:
                round_num = 6
            elif score == 600:
                round_num = 7
            elif score == 700:
                round_num = 8
            elif score == 800:
                round_num = 9
            elif score == 900:
                round_num = 10
            elif score == 1000:
                round_num = 11
            elif score == 1100:
                round_num = 12
            elif score == 1200:
                round_num = 13
            elif score == 1300:
                round_num = 14
            elif score == 1400:
                round_num = 15
            elif score == 1500:
                round_num = 16
            elif score == 1600:
                round_num = 17
            elif score == 1700:
                round_num = 18
            elif score == 1800:
                round_num = 19
            elif score == 1900:
                round_num = 20
            elif score == 2000:
                round_num = 21
            elif score == 100000:
                round_num = "???"

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
        surface.blit(background_img, (0, 0))
        surface.blit(food_img, food)
        draw_snake(snake)
        draw_text(f"Score: {score}", 30, white, 10, 10)
        draw_text(f"Round: {round_num}", 30, white, 500, 10)  # Mostrar el número de ronda
        draw_text(f"Apples Eaten: {apples_eaten}", 30, white, 10, 40)  # Mostrar la cantidad de manzanas comidas

        pygame.display.set_caption(get_fps_string(clock))  # Actualizar el título de la ventana con FPS
        pygame.display.flip()
        
        # Llama a la función para actualizar la presencia de Discord
        update_discord_presence()

        # Establecer la velocidad de actualización
        clock.tick(snake_speed)

    # Calcular el tiempo transcurrido
    end_time = time.time()
    elapsed_time = round(end_time - start_time)

    # Mostrar pantalla de Game Over con puntaje, rondas y tiempo
    game_over_menu = pygame_menu.Menu('Game Over', 600, 400, theme=my_theme)
    game_over_menu.add.label(f"Score: {score}")
    game_over_menu.add.label(f"Rounds: {round_num}")
    game_over_menu.add.label(f"Time: {elapsed_time} seconds")
    game_over_menu.add.button('Retry', start_the_game)
    game_over_menu.add.button('Return To Main Menu', return_to_main_menu)
    game_over_menu.add.selector('Change Difficulty :', [('Normal', 1), ('Hard', 2), ('Very Hard', 3), ('Very Super Hard', 5), ('IMPOSSIBLE', 6), ('???', 7), ('Easy', 4)], onchange=set_difficulty)
    game_over_menu.add.button('Quit Game', pygame_menu.events.EXIT)

    game_over_menu.mainloop(surface)

# Función para regresar al menú principal
def return_to_main_menu():
    os.system("start PacNakeGame.py")  # Abre PacNakeGamePreview.py
    exit()  # Sale del proyecto actual
    
# Función para abrir un cuadro de diálogo y seleccionar un archivo de música .mp3
def select_music():
    root = tk.Tk()
    root.withdraw() # Ocultar la ventana principal
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1) # Reproducir en bucle
        messagebox.showinfo('Music', 'Music loaded successfully')
    root.destroy() # Cerrar la ventana

def set_mods(value, set_mods):
    if set_mods == 1:
        pygame.mixer.music.stop()
        response = messagebox.askyesno('Message', 'Are you sure you want to close the game?')
        if response:
            os.system("start PacNakeGameMegaHack.py")
            exit()
        else:
            pygame.mixer.music.play(-1)  # Vuelve a reproducir la música

# Función para mostrar la información sobre el juego
def show_info():
    messagebox.showinfo('Information', 'Pacman But Snake\nAndres Studios Copyright\nMusics:\nVery Hard: BREAKDOWN (VIP)\nHard: NCS Invisible\nEasy: Tobu CandyLand\nNormal: NCS Energy')

# Función para configurar la dificultad del juego
def set_difficulty(value, difficulty):
    global snake_speed, background_img, body_img, food_img, score_increment  # Agregar variable global para el incremento de puntaje
    if difficulty == 2:  # Si la dificultad es 'Hard'
        snake_speed = 25  # Establecer una velocidad de serpiente más rápida
        background_img = pygame.image.load("background_hard.jpg")
        body_img = pygame.image.load("snake_demon.png")
        food_img = pygame.image.load("food_red.png")
        pygame.mixer.music.load("background_music_hard.mp3")
        score_increment = 30  # Incremento de puntaje por defecto
    elif difficulty == 3:  # Si la dificultad es 'Muy Difícil'
        snake_speed = 35  # Establecer una velocidad de serpiente muy rápida
        background_img = pygame.image.load("background_veryhard.jpg")
        body_img = pygame.image.load("snake_verydemon.png")
        food_img = pygame.image.load("food_demon.png")
        pygame.mixer.music.load("background_music_veryhard.mp3")
        score_increment = 50  # Incremento de puntaje para 'Muy Difícil'
    elif difficulty == 1:  # Si la dificultad es 'Normal'
        snake_speed = 15  # Establecer la velocidad de serpiente normal
        background_img = pygame.image.load("background.jpg")
        body_img = pygame.image.load("snake_body.png")
        food_img = pygame.image.load("food.png")
        pygame.mixer.music.load("background_music.mp3")
        score_increment = 10  # Incremento de puntaje por defecto
    elif difficulty == 6:  # Si la dificultad es 'impossible'
        snake_speed = 55  # Establecer una velocidad de serpiente muy rápida
        background_img = pygame.image.load("background_impossible.jpg")
        body_img = pygame.image.load("snake_verydemon.png")
        food_img = pygame.image.load("food_demon.png")
        pygame.mixer.music.load("background_music_veryhard.mp3")
        score_increment = 1000  # Incremento de puntaje para 'impossible'
    elif difficulty == 7:  # Si la dificultad es '???'
        snake_speed = 35  # Establecer una velocidad de serpiente muy rápida
        background_img = pygame.image.load("background_impossible.jpg")
        body_img = pygame.image.load("snake_verydemon.png")
        food_img = pygame.image.load("food_demon.png")
        pygame.mixer.music.load("726404_Random-Song-10.mp3")
        score_increment = 100000  # Incremento de puntaje para '???'
    elif difficulty == 4:  # Si la dificultad es 'Easy'
        snake_speed = 10  # Establecer una velocidad de serpiente más lenta
        background_img = pygame.image.load("background_easy.jpg")
        body_img = pygame.image.load("snake_body.png")
        food_img = pygame.image.load("food_green.png")
        pygame.mixer.music.load("Tobu - Candyland.mp3")
        score_increment = 5  # Incremento de puntaje por defecto
    else:  # Si la dificultad es 'Super Dificil'
        snake_speed = 45  # Establecer una velocidad de serpiente muy rápida
        background_img = pygame.image.load("background_verysuperhard.jpg")
        body_img = pygame.image.load("snake_verydemon.png")
        food_img = pygame.image.load("food_demon.png")
        pygame.mixer.music.load("background_music_veryhard.mp3")
        score_increment = 500  # Incremento de puntaje para 'Super Dificil'

def show_changelog():
    changelog = '''What's new?

    - Discord Rpc
    - New Main Menu
    - New Game Over
    - New Difficulties
    - Eaten Apples System
    - New Round System
    - The M Key to Mute Music
    - Shift and M Key to Change Music
    - FPS AND CPU AND RAM In The Title Of The Game
    - Improved Textures
    - New Background Music (the worst I played)
    - A Very Big Code
    - And More!'''

    messagebox.showinfo('Changelog', changelog)

# Función para iniciar el juego
def start_the_game():
    game()  # Llamar a la función principal del juego

# Función para cambiar el volumen de la música
def change_volume(text, value):
    try:
        volume = float(value)  # Convertir el valor ingresado a un flotante
        pygame.mixer.music.set_volume(volume)  # Establecer el volumen de la música
        print(f"Volume set to: {volume}")
    except ValueError:
        print("Invalid volume value. Using default volume.")  # En caso de que el valor ingresado no sea un flotante
        pygame.mixer.music.set_volume(0.5)  # Establecer el volumen predeterminado

# Función para reiniciar el juego
def reload_game():
    os.system("start PacNakeGame.py")
    exit()

# Crear el menú principal
menu = pygame_menu.Menu('Welcome To Pacnake', 600, 400, theme=my_theme)

menu.add.button('Play', game)
menu.add.button('Reload', reload_game)
menu.add.button('Changelog Game', show_changelog)
menu.add.button('Select Music', select_music)
menu.add.selector('Mods :', [('MegaHack', 1)], onchange=set_mods)
menu.add.selector('Volume :', [('0.1', 0.1), ('0.2', 0.2), ('0.3', 0.3), ('0.4', 0.4), ('0.5', 0.5), ('0.6', 0.6), ('0.7', 0.7), ('0.8', 0.8), ('0.9', 0.9), ('1.0', 1.0)], onchange=change_volume)
menu.add.selector('Difficulty :', [('Normal', 1), ('Hard', 2), ('Very Hard', 3), ('Very Super Hard', 5), ('IMPOSSIBLE', 6), ('???', 7), ('Easy', 4)], onchange=set_difficulty)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.toggle_switch('Discord RPC', False, onchange=toggle_discord_rpc)  # Toggle switch para activar/desactivar el RPC de Discord

# Ejecutar el menú principal
menu.mainloop(surface)
