import pygame, sys, random

# inicializa todos los módulos de Pygame.
pygame.init()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

def point_won(winner):
    global cpu_points, player_points

    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1 

    reset_ball()

def animate_ball():
    global ball_speed_x, ball_speed_y
    # mueve las coordenadas en 6px.
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # detectar colicion con los borders de la pantalla de juego.
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("cpu")

    if ball.left <= 0:
        point_won("player")

    # detecta la colision de la pelota con el pad.
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1

def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height

def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery - 10:
        cpu_speed = -8
    if ball.centery >= cpu.centery + 10:
        cpu_speed = 8
    
    if cpu.top <= 0:
        cpu.top = 0
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height

def draw_dotted_line(surface, color, start_pos, end_pos, width, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos

    if x1 == x2:
        for y in range(y1, y2, dash_length * 2):
            pygame.draw.line(surface, color, (x1, y), (x1, y + dash_length), width)

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

cpu = pygame.Rect(10, screen_height / 2 - 70, 20, 140)
# ubicamos el cpu a mitad del eje y.
cpu.centery = screen_height/2
cpu_color = (48, 213, 200) # Turquesa neón

player = pygame.Rect(screen_width, screen_height / 2 - 70, 20, 140)
# ubicamos el jugador al centro de la orilla derecha de la ventana.
player.midright = (screen_width - 10, screen_height/2)
player_color = (191, 0, 255) # Púrpura neón

# velocidad en cada eje
ball_speed_x = 8
ball_speed_y = 8
player_speed = 0
cpu_speed = 6

cpu_points, player_points = 0, 0

score_font = pygame.font.Font("./Jersey10-Regular.ttf", 140)
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

    cpu_score_surface = score_font.render(str(cpu_points), True, cpu_color)
    player_score_surface = score_font.render(str(player_points), True, player_color)
    screen.blit(cpu_score_surface, (screen_width/4, 20))
    screen.blit(player_score_surface, (3*screen_width/4, 20))
    

    pygame.draw.rect(screen, ball_color, ball)
    pygame.draw.rect(screen, cpu_color, cpu)
    pygame.draw.rect(screen, player_color, player)
    # Dibujar la línea punteada en el centro del campo
    draw_dotted_line(screen, "white", (screen_width // 2, 0), (screen_width // 2, screen_height), 5)



    # actualizamos la pantalla.
    pygame.display.update()
    # limitamos la cantidad de cuadros por segundo (FPS) a 60.
    clock.tick(60)