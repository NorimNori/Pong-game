import pygame, sys

# inicializa todos los módulos de Pygame.
pygame.init()

def animate_ball():
    global ball_speed_x, ball_speed_y
    # mueve las coordenadas en 6px.
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # detectar colicion con los borders de la pantalla de juego.
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width or ball.left <= 0:
        ball_speed_x *= -1

def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height

def animate_cpu():
    global cpu_speed, cpu_bottom
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -8
    if ball.centery >= cpu.centery:
        cpu_speed = 8
    
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu_bottom = screen_height


# establecer tamaño de la pantalla de juego.
screen_width = 1280
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
# titulo que aparece en la ventana del juego.
pygame.display.set_caption("Pong Pong Wars!!")

# inicializamos el reloj para controlar la velocidad del bucle principal.
clock = pygame.time.Clock()

# cuadrado de 30x30 px. 
            #     (x, y, width, height)
ball = pygame.Rect(0,0,30,30)
# centramos la pelota en la pantalla utilizando las dimensiones
# ball.center define el centro del rectángulo en una tupla (x, y)
ball.center = (screen_width/2, screen_height/2)
ball_color = (255, 255, 0)  # Amarillo neón

cpu = pygame.Rect(0,0,20,100)
# ubicamos el cpu a mitad del eje y.
cpu.centery = screen_height/2
cpu_color = (48, 213, 200) # Turquesa neón

player = pygame.Rect(0,0,20,100)
# ubicamos el jugador al centro de la orilla derecha de la ventana.
player.midright = (screen_width, screen_height/2)
player_color = (191, 0, 255) # Púrpura neón

# velocidad en cada eje
ball_speed_x = 8
ball_speed_y = 8
player_speed = 0
cpu_speed = 6

while True:
    # gestión de eventos.
    for event in pygame.event.get():
        # QUIT: clic en cerrar ventana.
        if event.type == pygame.QUIT:
            # Detenemos el programa.
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -8
            if event.key == pygame.K_DOWN:
                player_speed = 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    animate_ball()
    animate_player()
    animate_cpu()

    # dibujar los ojetos del juego.
    # 1. screen: superficie donde queremos dibujar el objeto.
    # 2. ball_color: es el color que lre queremos dar al objeto.
    # 3. ball: circulo que queremos dibujar.
    
    # evita que la pelota deje una "estela" al moverse.
    screen.fill('black')
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.rect(screen, cpu_color, cpu)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.aaline(screen, 'white', (screen_width/2, 0), (screen_width/2, screen_height))


    # actualizamos la pantalla.
    pygame.display.update()
    # limitamos la cantidad de cuadros por segundo (FPS) a 60.
    clock.tick(60)