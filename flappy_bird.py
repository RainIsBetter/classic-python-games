import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

bird_x = 80
gravity = 0.45
jump_strength = -8
pipe_width = 65
pipe_gap = 160
pipe_speed = 3

def reset():
    return HEIGHT / 2, 0, [], 0, False

def draw_bird(surface, x, y, velocity):
    # Bird tilt based on movement
    angle = max(-30, min(30, -velocity * 3))

    bird_surface = pygame.Surface((50, 40), pygame.SRCALPHA)

    # Body
    pygame.draw.ellipse(bird_surface, (255, 220, 0), (8, 8, 28, 22))

    # Wing
    wing_y = 18 + int(math.sin(pygame.time.get_ticks() * 0.02) * 2)
    pygame.draw.ellipse(bird_surface, (255, 190, 0), (16, wing_y, 16, 10))

    # Eye
    pygame.draw.circle(bird_surface, (255, 255, 255), (30, 15), 5)
    pygame.draw.circle(bird_surface, (0, 0, 0), (31, 15), 2)

    # Beak
    pygame.draw.polygon(
        bird_surface,
        (255, 140, 0),
        [(36, 18), (47, 14), (47, 22)]
    )

    # Tail
    pygame.draw.polygon(
        bird_surface,
        (230, 180, 0),
        [(8, 18), (0, 12), (2, 20), (0, 28)]
    )

    rotated = pygame.transform.rotate(bird_surface, angle)
    rect = rotated.get_rect(center=(x + 15, y + 15))
    surface.blit(rotated, rect.topleft)

def draw_background():
    screen.fill((135, 206, 235))

    # Simple clouds
    pygame.draw.circle(screen, (255, 255, 255), (60, 80), 20)
    pygame.draw.circle(screen, (255, 255, 255), (85, 75), 25)
    pygame.draw.circle(screen, (255, 255, 255), (110, 80), 20)

    pygame.draw.circle(screen, (255, 255, 255), (280, 120), 18)
    pygame.draw.circle(screen, (255, 255, 255), (300, 115), 22)
    pygame.draw.circle(screen, (255, 255, 255), (322, 120), 18)

    # Ground
    pygame.draw.rect(screen, (222, 216, 149), (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.rect(screen, (100, 200, 100), (0, HEIGHT - 90, WIDTH, 10))

bird_y, velocity, pipes, score, game_over = reset()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                velocity = jump_strength

            if event.key == pygame.K_r and game_over:
                bird_y, velocity, pipes, score, game_over = reset()

    if not game_over:
        velocity += gravity
        bird_y += velocity

        # Generate new pipes
        if not pipes or pipes[-1][0] < WIDTH - 220:
            gap_y = random.randint(100, HEIGHT - pipe_gap - 180)
            pipes.append([WIDTH, gap_y, False])

        bird = pygame.Rect(bird_x, int(bird_y), 30, 30)

        for pipe in pipes:
            pipe[0] -= pipe_speed

            top_pipe = pygame.Rect(pipe[0], 0, pipe_width, pipe[1])
            bottom_pipe = pygame.Rect(
                pipe[0],
                pipe[1] + pipe_gap,
                pipe_width,
                HEIGHT - pipe[1] - pipe_gap - 80
            )

            if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
                game_over = True

            if pipe[0] + pipe_width < bird_x and not pipe[2]:
                score += 1
                pipe[2] = True

        pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]

        if bird_y < 0 or bird_y + 30 > HEIGHT - 80:
            game_over = True

    draw_background()

    # Draw pipes
    for x, gap_y, passed in pipes:
        pygame.draw.rect(screen, (40, 180, 60), (x, 0, pipe_width, gap_y))
        pygame.draw.rect(
            screen,
            (40, 180, 60),
            (x, gap_y + pipe_gap, pipe_width, HEIGHT - gap_y - pipe_gap - 80)
        )

        # Pipe caps
        pygame.draw.rect(screen, (30, 150, 50), (x - 4, gap_y - 15, pipe_width + 8, 15))
        pygame.draw.rect(screen, (30, 150, 50), (x - 4, gap_y + pipe_gap, pipe_width + 8, 15))

    # Draw bird
    draw_bird(screen, bird_x, int(bird_y), velocity)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if game_over:
        message = font.render("Game Over! Press R", True, (0, 0, 0))
        screen.blit(message, message.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()