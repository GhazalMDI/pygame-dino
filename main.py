import pygame
import random

from setting import WIDTH, HEIGHT, FPS
from player.player import Player
from obstacles.cactus import Cactus
from obstacles.bird import Bird

# ---------------- INIT ----------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")


clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28, bold=True)

ground_image = pygame.image.load("assets/Track.png")
ground_image = pygame.transform.scale(ground_image, (WIDTH, 40))

ground_x1 = 0
ground_x2 = WIDTH
ground_speed = 6

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
        False, # game over
        255,  # background_value
        255,  # target_background
        0     # night_timer
    )


player, cacti, birds, score, cactus_timer, bird_timer, spawn_delay, game_over, background_value,target_background, night_timer = reset_game()

# ---------------- GROUND ----------------
ground_segments = []
for i in range(20):
    x = i * 50
    width = random.randint(20, 50)
    ground_segments.append([x, width])

# ---------------- NIGHT ----------------
night_timer = 0
background_value = 255
target_background = 255

running = True

# ---------------- GAME LOOP ----------------
while running:

    # -------- EVENTS --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player, cacti, birds, score, cactus_timer, bird_timer, spawn_delay, game_over, background_value,target_background, night_timer = reset_game()

    # -------- UPDATE --------
    if not game_over:

        cactus_timer += 1
        bird_timer += 1
        night_timer += 1
        score += 1

        # night/day toggle
        if night_timer >= 200 and night_timer <= 700:
            if target_background == 255:
                target_background = 40
            else:
                target_background = 255

            night_timer = 0

        # spawn cactus
        if cactus_timer >= spawn_delay:
            cacti.append(Cactus(800))
            cactus_timer = 0
            spawn_delay = random.randint(60, 170)

        # spawn bird
        if bird_timer >= 500:
            birds.append(Bird(800))
            bird_timer = 0

        # update player
        player.update()
        
        fade_speed = 2

        if background_value < target_background:
            background_value += fade_speed

        elif background_value > target_background:
            background_value -= fade_speed

        # update cactus
        for cactus in cacti:
            cactus.update()

        # update birds
        for bird in birds:
            bird.update()

        # ground movement
        ground_x1 -= ground_speed
        ground_x2 -= ground_speed

        if ground_x1 <= -WIDTH:
            ground_x1 = WIDTH

        if ground_x2 <= -WIDTH:
            ground_x2 = WIDTH

        # collision cactus
        for cactus in cacti:
            if player.rect.colliderect(cactus.rect):
                player.die_sound.play()
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                game_over = True

        # collision bird
        for bird in birds:
            if player.rect.colliderect(bird.rect):
                player.die_sound.play()
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

                game_over = True

        # cleanup
        cacti = [c for c in cacti if c.x > -50]
        birds = [b for b in birds if b.x > -50]

    # -------- DRAW --------
    screen.fill(
    (
        background_value,
        background_value,
        background_value
    )
)

    # ground
    screen.blit(ground_image, (ground_x1, 320))
    screen.blit(ground_image, (ground_x2, 320))

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

        over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

        screen.blit(over_text, over_rect)
        screen.blit(restart_text, restart_rect)
        
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()