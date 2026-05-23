import pygame
import random

from setting import WIDTH, HEIGHT, FPS
from player.player import Player
from obstacles.cactus import Cactus
from obstacles.bird import Bird

# ---------------- INIT ----------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28, bold=True)

# ---------------- HIGH SCORE ----------------
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0


# ---------------- RESET FUNCTION ----------------
def reset_game():
    return (
        Player(),
        [],   # cacti
        [],   # birds
        0,    # score
        0,    # cactus timer
        0,    # bird timer
        90,   # spawn delay
        False # game over
    )


player, cacti, birds, score, cactus_timer, bird_timer, spawn_delay, game_over = reset_game()

# ---------------- GROUND ----------------
ground_segments = []
for i in range(20):
    x = i * 50
    width = random.randint(20, 50)
    ground_segments.append([x, width])

# ---------------- NIGHT ----------------
is_night = False
night_timer = 0

running = True

# ---------------- GAME LOOP ----------------
while running:

    # -------- EVENTS --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player, cacti, birds, score, cactus_timer, bird_timer, spawn_delay, game_over = reset_game()

    # -------- UPDATE --------
    if not game_over:

        cactus_timer += 1
        bird_timer += 1
        night_timer += 1
        score += 1

        # night/day toggle
        if night_timer >= 500:
            is_night = not is_night
            night_timer = 0

        # spawn cactus
        if cactus_timer >= spawn_delay:
            cacti.append(Cactus(800))
            cactus_timer = 0
            spawn_delay = random.randint(60, 170)

        # spawn bird
        if bird_timer >= 250:
            birds.append(Bird(800))
            bird_timer = 0

        # update player
        player.update()

        # update cactus
        for cactus in cacti:
            cactus.update()

        # update birds
        for bird in birds:
            bird.update()

        # ground movement
        for segment in ground_segments:
            segment[0] -= 6
            if segment[0] + segment[1] < 0:
                segment[0] = WIDTH + random.randint(20, 100)

        # collision cactus
        for cactus in cacti:
            if player.rect.colliderect(cactus.rect):

                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                game_over = True

        # collision bird
        for bird in birds:
            if player.rect.colliderect(bird.rect):

                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                game_over = True

        # cleanup
        cacti = [c for c in cacti if c.x > -50]
        birds = [b for b in birds if b.x > -50]

    # -------- DRAW --------
    if is_night:
        screen.fill((30, 30, 30))
    else:
        screen.fill((255, 255, 255))

    # ground
    for segment in ground_segments:
        pygame.draw.line(
            screen,
            (83, 83, 83),
            (segment[0], 340),
            (segment[0] + segment[1], 340),
            2
        )

    # draw player
    player.draw(screen)

    # draw cactus
    for cactus in cacti:
        cactus.draw(screen)

    # draw birds
    for bird in birds:
        bird.draw(screen)

    # score
    score_text = font.render(f"{score:05d}", True, (83, 83, 83))
    screen.blit(score_text, (WIDTH - 120, 20))

    high_text = font.render(f"HI {high_score:05d}", True, (83, 83, 83))
    screen.blit(high_text, (WIDTH - 270, 20))

    # GAME OVER UI
    if game_over:

        over_text = font.render("GAME OVER", True, (83, 83, 83))
        restart_text = font.render("PRESS SPACE TO RESTART", True, (120, 120, 120))

        screen.blit(over_text, (WIDTH//2 - 150, HEIGHT//2 - 60))
        screen.blit(restart_text, (WIDTH//2 - 200, HEIGHT//2))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()