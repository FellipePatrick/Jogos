import pygame
pygame.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo")

running = True
FPS = 60

clock = pygame.time.Clock()

# Background
clouds = pygame.image.load("./images/clouds.png").convert()
ground = pygame.image.load("./images/ground.png").convert_alpha()

# Spritesheet
player_sheet = pygame.image.load("./images/player.png").convert_alpha()
frame_width = player_sheet.get_width() // 4
frame_height = player_sheet.get_height()

player_frames_left= [
    player_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    for i in range(4)
]
player_frames_right = [
    pygame.transform.flip(frame, True, False) for frame in player_frames_left
]

# Animação
current_frame = 0
frame_timer = 0
frame_delay = 100  # ms por quadro

# Movimento
position_player_x = 20
right = True
cont_cloud = 0
velocidade = 100

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(FPS)
    frame_timer += dt

    # Movimento do jogador
    moving = False
    if keys[pygame.K_RIGHT]:
        right = True
        if position_player_x <= 555:
            position_player_x += 5
        moving = True
    if keys[pygame.K_LEFT]:
        right = False
        if position_player_x >= 0:
            position_player_x -= 5
        moving = True

    if moving and frame_timer >= frame_delay:
        frame_timer = 0
        current_frame = (current_frame + 1) % 4
    if not moving:
        current_frame = 0  

    cont_cloud -= velocidade * (dt / 5000)
    if cont_cloud <= -600:
        cont_cloud = 0

    screen.fill((0, 0, 0))
    screen.blit(clouds, (cont_cloud, 0))
    screen.blit(clouds, (cont_cloud + 600, 0))
    screen.blit(clouds, (cont_cloud + 1200, 0))

    if right:
        player = player_frames_right[current_frame]
    else:
        player = player_frames_left[current_frame]

    screen.blit(player, (position_player_x, 200))
    screen.blit(ground, (0, 230))
    pygame.display.flip()

pygame.quit()
