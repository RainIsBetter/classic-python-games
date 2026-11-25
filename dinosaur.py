import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 56)

GROUND_Y = 255
GRAVITY = 0.85
JUMP_STRENGTH = -15

SKY = (235, 248, 255)
GROUND_COLOR = (224, 205, 160)
GRASS = (110, 180, 90)
DINO_GREEN = (70, 160, 90)
DINO_DARK = (45, 110, 60)
CACTUS_GREEN = (50, 140, 70)
BIRD_BROWN = (120, 95, 70)
TEXT = (40, 40, 40)
WHITE = (255, 255, 255)

def reset():
    dino = {
        "x": 90,
        "y": GROUND_Y - 62,
        "w": 58,
        "h": 62,
        "vy": 0,
        "on_ground": True,
        "frame": 0
    }
    obstacles = []
    clouds = [[150, 55, 1], [420, 95, 2], [700, 70, 1]]
    score = 0
    speed = 7
    game_over = False
    ground_offset = 0
    return dino, obstacles, clouds, score, speed, game_over, ground_offset

def draw_cloud(surface, x, y):
    pygame.draw.circle(surface, WHITE, (x, y), 18)
    pygame.draw.circle(surface, WHITE, (x + 18, y - 8), 22)
    pygame.draw.circle(surface, WHITE, (x + 40, y), 18)
    pygame.draw.circle(surface, WHITE, (x + 20, y + 5), 18)

def draw_dino(surface, dino, ticks):
    x = int(dino["x"])
    y = int(dino["y"])

    bob = 0 if not dino["on_ground"] else int(math.sin(ticks * 0.02) * 1)

    body = pygame.Rect(x + 8, y + 18 + bob, 34, 28)
    neck = pygame.Rect(x + 30, y + 10 + bob, 12, 18)
    head = pygame.Rect(x + 34, y + 4 + bob, 20, 18)
    tail_points = [(x + 8, y + 28 + bob), (x - 10, y + 20 + bob), (x + 4, y + 36 + bob)]

    # tail
    pygame.draw.polygon(surface, DINO_DARK, tail_points)

    # body / neck / head
    pygame.draw.ellipse(surface, DINO_GREEN, body)
    pygame.draw.rect(surface, DINO_GREEN, neck, border_radius=5)
    pygame.draw.ellipse(surface, DINO_GREEN, head)

    # belly
    pygame.draw.ellipse(surface, (120, 205, 135), (x + 14, y + 28 + bob, 20, 12))

    # spikes
    spike_points = [
        [(x + 13, y + 18 + bob), (x + 17, y + 10 + bob), (x + 21, y + 18 + bob)],
        [(x + 23, y + 16 + bob), (x + 27, y + 7 + bob), (x + 31, y + 16 + bob)],
        [(x + 33, y + 18 + bob), (x + 37, y + 10 + bob), (x + 41, y + 18 + bob)],
    ]
    for pts in spike_points:
        pygame.draw.polygon(surface, DINO_DARK, pts)

    # arms
    pygame.draw.line(surface, DINO_DARK, (x + 33, y + 30 + bob), (x + 45, y + 36 + bob), 4)
    pygame.draw.line(surface, DINO_DARK, (x + 33, y + 34 + bob), (x + 43, y + 42 + bob), 4)

    # legs animation
    if dino["on_ground"]:
        if (ticks // 120) % 2 == 0:
            left_leg = [(x + 18, y + 44 + bob), (x + 13, y + 61 + bob)]
            right_leg = [(x + 33, y + 44 + bob), (x + 36, y + 61 + bob)]
        else:
            left_leg = [(x + 18, y + 44 + bob), (x + 20, y + 61 + bob)]
            right_leg = [(x + 33, y + 44 + bob), (x + 28, y + 61 + bob)]
    else:
        left_leg = [(x + 18, y + 44 + bob), (x + 14, y + 56 + bob)]
        right_leg = [(x + 33, y + 44 + bob), (x + 37, y + 56 + bob)]

    pygame.draw.line(surface, DINO_DARK, left_leg[0], left_leg[1], 5)
    pygame.draw.line(surface, DINO_DARK, right_leg[0], right_leg[1], 5)

    # eye
    pygame.draw.circle(surface, WHITE, (x + 47, y + 12 + bob), 4)
    pygame.draw.circle(surface, (0, 0, 0), (x + 48, y + 12 + bob), 2)

    # mouth
    pygame.draw.line(surface, DINO_DARK, (x + 43, y + 20 + bob), (x + 53, y + 20 + bob), 2)

def make_cactus(speed):
    h = random.randint(38, 68)
    w = random.randint(22, 30)
    return {
        "type": "cactus",
        "rect": pygame.Rect(WIDTH + 20, GROUND_Y - h, w, h),
        "speed": speed
    }

def make_bird(speed):
    y = random.choice([GROUND_Y - 95, GROUND_Y - 125, GROUND_Y - 150])
    return {
        "type": "bird",
        "rect": pygame.Rect(WIDTH + 20, y, 42, 26),
        "speed": speed + 1
    }

def draw_cactus(surface, rect):
    pygame.draw.rect(surface, CACTUS_GREEN, rect, border_radius=4)
    pygame.draw.rect(surface, CACTUS_GREEN, (rect.x - 8, rect.y + 16, 10, 16), border_radius=3)
    pygame.draw.rect(surface, CACTUS_GREEN, (rect.x + rect.width - 2, rect.y + 10, 10, 18), border_radius=3)
    pygame.draw.rect(surface, CACTUS_GREEN, (rect.x + 5, rect.y + 6, rect.width - 10, 6), border_radius=3)

def draw_bird(surface, rect, ticks):
    flap = int(math.sin(ticks * 0.03) * 5)

    # body
    pygame.draw.ellipse(surface, BIRD_BROWN, (rect.x + 8, rect.y + 8, 20, 12))
    # head
    pygame.draw.circle(surface, BIRD_BROWN, (rect.x + 29, rect.y + 12), 6)
    # beak
    pygame.draw.polygon(surface, (240, 170, 60), [(rect.x + 34, rect.y + 12), (rect.x + 41, rect.y + 10), (rect.x + 41, rect.y + 14)])
    # eye
    pygame.draw.circle(surface, WHITE, (rect.x + 30, rect.y + 10), 2)
    pygame.draw.circle(surface, (0, 0, 0), (rect.x + 30, rect.y + 10), 1)
    # wings
    pygame.draw.polygon(surface, (150, 120, 90), [
        (rect.x + 14, rect.y + 14),
        (rect.x + 2, rect.y + 12 - flap),
        (rect.x + 12, rect.y + 20)
    ])
    pygame.draw.polygon(surface, (150, 120, 90), [
        (rect.x + 18, rect.y + 14),
        (rect.x + 6, rect.y + 24 + flap),
        (rect.x + 18, rect.y + 20)
    ])

def get_dino_hitbox(dino):
    # slightly forgiving collision box
    return pygame.Rect(dino["x"] + 8, dino["y"] + 10, 42, 48)

dino, obstacles, clouds, score, speed, game_over, ground_offset = reset()

spawn_timer = 0
running = True

while running:
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if dino["on_ground"] and not game_over:
                    dino["vy"] = JUMP_STRENGTH
                    dino["on_ground"] = False

            if event.key == pygame.K_r and game_over:
                dino, obstacles, clouds, score, speed, game_over, ground_offset = reset()
                spawn_timer = 0

    if not game_over:
        # Dino physics
        dino["vy"] += GRAVITY
        dino["y"] += dino["vy"]

        if dino["y"] >= GROUND_Y - dino["h"]:
            dino["y"] = GROUND_Y - dino["h"]
            dino["vy"] = 0
            dino["on_ground"] = True

        # Difficulty
        score += 1
        speed = 7 + score / 500

        # Clouds
        for cloud in clouds:
            cloud[0] -= cloud[2]
            if cloud[0] < -80:
                cloud[0] = WIDTH + random.randint(20, 100)
                cloud[1] = random.randint(40, 110)

        # Ground scroll
        ground_offset = (ground_offset - int(speed)) % 40

        # Spawn obstacles
        spawn_timer += 1
        min_gap = max(45, int(90 - speed * 3))
        if spawn_timer > random.randint(70, 110):
            if random.random() < 0.75:
                obstacles.append(make_cactus(speed))
            else:
                obstacles.append(make_bird(speed))
            spawn_timer = 0

        # Move obstacles
        for obstacle in obstacles:
            obstacle["rect"].x -= int(obstacle["speed"])

        obstacles = [o for o in obstacles if o["rect"].right > -20]

        # Collision
        dino_hitbox = get_dino_hitbox(dino)
        for obstacle in obstacles:
            if dino_hitbox.colliderect(obstacle["rect"]):
                game_over = True

    # Draw sky
    screen.fill(SKY)

    # Draw clouds
    for cloud in clouds:
        draw_cloud(screen, int(cloud[0]), int(cloud[1]))

    # Background hills
    pygame.draw.ellipse(screen, (195, 225, 190), (40, 185, 180, 80))
    pygame.draw.ellipse(screen, (185, 218, 180), (260, 180, 220, 90))
    pygame.draw.ellipse(screen, (190, 220, 185), (560, 190, 220, 75))

    # Ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, GRASS, (0, GROUND_Y, WIDTH, 6))

    # Ground texture lines
    for i in range(-1, WIDTH // 40 + 2):
        x = i * 40 + ground_offset
        pygame.draw.line(screen, (180, 160, 120), (x, GROUND_Y + 25), (x + 18, GROUND_Y + 28), 2)
        pygame.draw.line(screen, (180, 160, 120), (x + 8, GROUND_Y + 45), (x + 20, GROUND_Y + 42), 2)

    # Obstacles
    for obstacle in obstacles:
        if obstacle["type"] == "cactus":
            draw_cactus(screen, obstacle["rect"])
        else:
            draw_bird(screen, obstacle["rect"], ticks)

    # Dino
    draw_dino(screen, dino, ticks)

    # Score
    score_text = font.render(f"Score: {score // 10}", True, TEXT)
    screen.blit(score_text, (20, 15))

    # Instructions
    if score < 20 and not game_over:
        hint = font.render("Press SPACE or UP to jump", True, TEXT)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 20))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 110))
        screen.blit(overlay, (0, 0))

        game_over_text = big_font.render("Game Over", True, TEXT)
        restart_text = font.render("Press R to restart", True, TEXT)
        final_text = font.render(f"Final Score: {score // 10}", True, TEXT)

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
        screen.blit(final_text, final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()