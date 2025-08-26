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
player_sheet = pygame.image.load("./images/ninja.png").convert_alpha()
frame_width = player_sheet.get_width() // 6
frame_height = player_sheet.get_height() // 3

# === FRAME SETS ===
# Idle (linha 0, colunas 1 a 2)
idle_frames_right = [player_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(1, 3)]
idle_frames_left = [pygame.transform.flip(f, True, False) for f in idle_frames_right]

# Walk (linha 1, colunas 0 a 5)
walk_frames_right = [player_sheet.subsurface(pygame.Rect(i * frame_width, frame_height, frame_width, frame_height)) for i in range(6)]
walk_frames_left = [pygame.transform.flip(f, True, False) for f in walk_frames_right]

# Attack (linha 2, colunas 0 a 3)
# Attack (linha 2, colunas 0 a 5 ping-pong)
attack_base = [
    player_sheet.subsurface(pygame.Rect(i * frame_width, frame_height * 2, frame_width, frame_height))
    for i in range(6)
]
# ping-pong: 0→1→2→3→4→5→4→3→2→1→0
attack_frames_right = attack_base + attack_base[-2::-1]  # inclui o 0 no retorno
attack_frames_left = [pygame.transform.flip(f, True, False) for f in attack_frames_right]

# === NINJA CLASS ===
class Ninja:
    def __init__(self, x, keys, attack_key):
        self.x = x
        self.y = 125
        self.right = True
        self.current_frame = 0
        self.frame_timer = 0
        self.last_moving = False
        self.moving = False
        self.attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.keys = keys
        self.attack_key = attack_key

    def update(self, dt, pressed_keys):
        self.moving = False

        # Ataque
        if pressed_keys[self.attack_key] and not self.attacking:
            self.attacking = True
            self.attack_frame = 0
            self.attack_timer = 0

        if self.attacking:
            self.attack_timer += dt
            if self.attack_timer >= 100:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_frame >= len(attack_frames_right):
                    self.attacking = False
                    self.attack_frame = 0

        # Movimento
        if pressed_keys[self.keys['right']]:
            self.right = True
            self.x += 5 if self.x <= 555 else 0
            self.moving = True
        elif pressed_keys[self.keys['left']]:
            self.right = False
            self.x -= 5 if self.x >= 0 else 0
            self.moving = True

        # Troca de estado: resetar frame
        if self.moving != self.last_moving and not self.attacking:
            self.current_frame = 0
            self.frame_timer = 0
        self.last_moving = self.moving

        # Animação (idle ou walk)
        if not self.attacking:
            self.frame_timer += dt
            if self.moving:
                if self.frame_timer >= 100:
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(walk_frames_right)
            else:
                if self.frame_timer >= 300:
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(idle_frames_right)

    def draw(self, surface):
        if self.attacking:
            frame = attack_frames_right[self.attack_frame] if self.right else attack_frames_left[self.attack_frame]
        elif self.moving:
            frame = walk_frames_right[self.current_frame] if self.right else walk_frames_left[self.current_frame]
        else:
            frame = idle_frames_right[self.current_frame] if self.right else idle_frames_left[self.current_frame]

        surface.blit(frame, (self.x, self.y))


# === INSTANCIANDO NINJAS ===
ninja1 = Ninja(20, keys={'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}, attack_key=pygame.K_k)
ninja2 = Ninja(400, keys={'left': pygame.K_a, 'right': pygame.K_d}, attack_key=pygame.K_f)

# === CÉU ===
cont_cloud = 0
velocidade = 100

# === LOOP PRINCIPAL ===
while running:
    dt = clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizações
    cont_cloud -= velocidade * (dt / 5000)
    if cont_cloud <= -600:
        cont_cloud = 0

    ninja1.update(dt, keys)
    ninja2.update(dt, keys)

    # Desenho
    screen.fill((0, 0, 0))
    screen.blit(clouds, (cont_cloud, 0))
    screen.blit(clouds, (cont_cloud + 600, 0))
    screen.blit(clouds, (cont_cloud + 1200, 0))

    ninja1.draw(screen)
    ninja2.draw(screen)

    screen.blit(ground, (0, 230))
    pygame.display.flip()

pygame.quit()
