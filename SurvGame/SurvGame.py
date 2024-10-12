import pygame
import time
import random
pygame.font.init()

# Setup game window
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_VEL = 3
PLAYER_LIFE = 3
PLAYER_DIR = 180

# Animal settings
ANIM_WIDTH = 20
ANIM_HEIGHT = ANIM_WIDTH * 4.7
ANIM_VEL = (0, 0)  # x,y velocities

# Health bar settings
border_HP = 20
size_HP = 30

# Time settings
START_TIME = 720
+
# Set font
FONT = pygame.font.SysFont("comicsans", 30)

# Appearances
CHAR = pygame.transform.scale(pygame.image.load("player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
ANIM = pygame.transform.scale(pygame.image.load("wolf.png"), (ANIM_WIDTH, ANIM_HEIGHT))
HEART = pygame.transform.scale(pygame.image.load("heart.png"), (size_HP, int(size_HP * 0.885)))


# %%%%%%%%%%%%%%%%%%%% Helper functions %%%%%%%%%%%%%%%%%%%% #


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def player_dir(p_dir, keys):
    if keys[pygame.K_w]:
        p_dir = 180
    if keys[pygame.K_s]:
        p_dir = 0
    if keys[pygame.K_a]:  # N
        p_dir = 270
        if keys[pygame.K_w]:  # NW
            p_dir = 225
        if keys[pygame.K_s]:  # SW
            p_dir = 315
    if keys[pygame.K_d]:  # O
        p_dir = 90
        if keys[pygame.K_w]:  # NO
            p_dir = 135
        if keys[pygame.K_s]:  # SO
            p_dir = 45

    return p_dir


def player_move(player, keys):
    if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
        player.x += PLAYER_VEL
    if keys[pygame.K_w] and player.y >= 0:
        player.y -= PLAYER_VEL
    if keys[pygame.K_s] and player.y + PLAYER_VEL + player.height <= HEIGHT:
        player.y += PLAYER_VEL

    return player

# %%%%%%%%%%%%%%%%%%%% Drawing functions %%%%%%%%%%%%%%%%%%%% #


def draw_grid():
    block_size = 40  # Set the size of the grid block
    for x in range(0, WIDTH, block_size):
        for y in range(0, HEIGHT, block_size):
            rect = pygame.Surface((block_size, block_size), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
            pygame.draw.rect(rect, (0, 0, 0, 64), rect.get_rect(), 1)  # Draw a black border around the surface
            WIN.blit(rect, (x, y))  # Blit the surface onto the window


def draw_player(player, p_dir):
    image = CHAR
    image, player = rot_center(image, p_dir, player.x, player.y)
    WIN.blit(image, (player.x, player.y))


def draw(player, p_dir, elapsed_time, anims, p_life):
    WIN.blit(BG, (0, 0))
    draw_grid()

    # Display game time
    time_h = "{:02d}".format(int((elapsed_time+0.5)/60) % 24)
    time_m = "{:02d}".format(round(elapsed_time) % 60)
    time_text = FONT.render(f"{time_h}:{time_m}", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw health bar
    if p_life >= 3:
        WIN.blit(HEART, (WIDTH - border_HP - 1 * size_HP, border_HP))
    if p_life >= 2:
        WIN.blit(HEART, (WIDTH - border_HP - 2 * size_HP, border_HP))
    if p_life >= 1:
        WIN.blit(HEART, (WIDTH - border_HP - 3 * size_HP, border_HP))

    # Draw player
    draw_player(player, p_dir)

    # Draw animals
    for anim in anims:
        WIN.blit(ANIM, (anim.x, anim.y))

    pygame.display.update()


# %%%%%%%%%%%%%%%%%%%% Main game loop %%%%%%%%%%%%%%%%%%%% #


def main():
    # Ingame music
    pygame.init()
    pygame.mixer.music.load('perfect-beauty-191271.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0)

    # Switches
    run = True
    hit = False

    # Add player
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    p_life = PLAYER_LIFE
    p_dir = PLAYER_DIR

    # Time
    clock = pygame.time.Clock()
    anim_time = time.time()

    # Init animals
    anim_add_increment = 2000
    anim_count = 0
    anims = []

    # Main game loop
    while run:
        anim_count += clock.tick(60)
        elapsed_time = START_TIME + time.time() - anim_time

        if anim_count > anim_add_increment:
            for _ in range(1):
                anim_x = random.randint(0, WIDTH - ANIM_WIDTH)
                # anim_y = random.randint(0, HEIGHT - int(ANIM_HEIGHT))
                anim = pygame.Rect(anim_x, - int(ANIM_HEIGHT), ANIM_WIDTH, ANIM_HEIGHT)
                anims.append(anim)

            anim_add_increment = max(200, anim_add_increment - 50)
            anim_count = 0

        # User close game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # User inputs
        keys = pygame.key.get_pressed()

        # Player movement
        player = player_move(player, keys)

        # Player facing direction
        p_dir = player_dir(p_dir, keys)

        # Animal movement
        for anim in anims[:]:
            anim.y += ANIM_VEL[1]
            # Direction change
            x_dir = ANIM_VEL[0]
            if random.random() < 0.15:
                x_dir += random.randint(-5, 5)
            anim.x += x_dir * random.randint(-1, 1)

            if anim.y > HEIGHT:
                anims.remove(anim)
            elif anim.y + anim.height >= player.y and anim.colliderect(player):
                anims.remove(anim)
                hit = True
                break

        # Animal encounter
        if hit:
            p_life -= 1
            if p_life < 1:
                lost_text = FONT.render("You were eaten!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.mixer.music.fadeout(4000)
                pygame.time.delay(1000)
                break
            hit = False

        # Draw
        draw(player, p_dir, elapsed_time, anims, p_life)

    pygame.quit()


if __name__ == "__main__":
    main()
