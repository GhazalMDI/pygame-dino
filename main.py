import pygame
import random

from setting import WIDTH, HEIGHT, FPS
from player.player import Player
from obstacles.cactus import Cactus

with open("highscore.txt","r") as file:
    high_score = int(file.read())

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28, bold=True)

# GAME STATE
player = Player()
cacti = []
ground_segments = []

for i in range(20):
    x = i*50
    width = random.randint(20,50)
    ground_segments.append([x,width])

spawn_timer = 0
spawn_delay = 90

score = 0

game_over = False

running = True
is_night = False
night_timer = 0

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
                night_timer = 0
                score = 0
                spawn_timer = 0
                spawn_delay = 90

                game_over = False

    # UPDATE
    if not game_over:

        spawn_timer += 1
        night_timer += 1
        
        if night_timer >= 500:
            is_night = not is_night
            night_timer = 0

        if spawn_timer >= spawn_delay:
            cacti.append(Cactus(800))
            spawn_timer = 0
            spawn_delay = random.randint(60, 170)

        player.update()
        score += 1
        
        for segment in ground_segments:
            segment[0] -= 6
            if segment[0] + segment[1] < 0:
                segment[0] = WIDTH + random.randint(20, 100)

        for cactus in cacti:
            cactus.update()

        # collision
        for cactus in cacti:
            if player.rect.colliderect(cactus.rect):
                if score > high_score:
                    high_score = int(score)
                    
                    with open("highscore.txt","w") as file:
                        file.write(str(high_score))
            
                game_over = True

        # cleanup
        cacti = [c for c in cacti if c.x > -50]


    # DRAW
    if is_night:
        screen.fill((30, 30, 30))
    else:
        screen.fill((255,255,255))

    player.draw(screen)
    
    for segment in ground_segments:
        pygame.draw.line(screen,(83,83,83),(segment[0],340),(segment[0]+segment[1],340),2),

    for cactus in cacti:
        cactus.draw(screen)

    # score
    score_text = font.render(f"{int(score):05d}", True, (83, 83, 83))
    screen.blit(score_text, (WIDTH - 120, 20))

    # game over text
    high_score_text = font.render(f"HI {int(high_score):05d}",True,(83, 83, 83)
)

    screen.blit(score_text, (WIDTH - 120, 20))
    screen.blit(high_score_text, (WIDTH - 270, 20))

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()

