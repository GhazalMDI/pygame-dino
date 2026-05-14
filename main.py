import pygame
import random

from setting import WIDTH, HEIGHT, FPS
from player.player import Player
from obstacles.cactus import Cactus


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28, bold=True)

# GAME STATE
player = Player()
cacti = []

spawn_timer = 0
spawn_delay = 90

score = 0
high_score = 0

game_over = False

running = True


# GAME LOOP

while running:

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # restart game
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                player = Player()
                cacti = []

                score = 0
                spawn_timer = 0
                spawn_delay = 90

                game_over = False

    # UPDATE
    if not game_over:

        spawn_timer += 1

        if spawn_timer >= spawn_delay:
            cacti.append(Cactus(800))
            spawn_timer = 0
            spawn_delay = random.randint(60, 120)

        player.update()
        score += 1

        for cactus in cacti:
            cactus.update()

        # collision
        for cactus in cacti:
            if player.rect.colliderect(cactus.rect):
                if score > high_score:
                    high_score = score
            
                game_over = True

        # cleanup
        cacti = [c for c in cacti if c.x > -50]

    # DRAW
    screen.fill((255, 255, 255))

    player.draw(screen)

    for cactus in cacti:
        cactus.draw(screen)

    # score
    score_text = font.render(f"{int(score):05d}", True, (83, 83, 83))
    screen.blit(score_text, (WIDTH - 120, 20))

    # game over text
    if game_over:
        score_text = font.render(f"{int(score)}", True, (83, 83, 83))
        high_score_text = font.render(f"HI {int(high_score)}", True, (83, 83, 83))

        screen.blit(score_text, (WIDTH - 120, 20))
        screen.blit(high_score_text, (WIDTH - 220, 20))

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()