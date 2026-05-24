import pygame
import random

from setting import WIDTH, HEIGHT, FPS
from player.player import Player
from obstacles.cactus import Cactus
from obstacles.bird import Bird


# =========================
# INIT
# =========================
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# for run program with fream
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28, bold=True)


# =========================
# ASSETS
# =========================

# left (x), bottom(y) 
GROUND_Y = 320
GROUND_SPEED = 6
FADE_SPEED = 2

ground_image = pygame.image.load("assets/Track.png")
ground_image = pygame.transform.scale(ground_image, (WIDTH, 40))


# =========================
# HIGH SCORE
# =========================
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


high_score = load_high_score()


# =========================
# RESET GAME
# =========================
def reset_game():
    return {
        "player": Player(),
        "cacti": [],
        "birds": [],
        "score": 0,
        "cactus_timer": 0,
        "bird_timer": 0,
        "spawn_delay": 90,
        "night_timer": 0,
        "background_value": 255,
        "target_background": 255,
        "game_over": False,
        "ground_x1": 0,
        "ground_x2": WIDTH,
    }


game = reset_game()


# =========================
# UPDATE FUNCTIONS
# =========================
def update_background(game):
    game["night_timer"] += 1

    # Toggle day/night
    if 200 <= game["night_timer"] <= 700:
        game["target_background"] = (
            40 if game["target_background"] == 255 else 255
        )
        game["night_timer"] = 0

    # Smooth transition
    if game["background_value"] < game["target_background"]:
        game["background_value"] += FADE_SPEED

    elif game["background_value"] > game["target_background"]:
        game["background_value"] -= FADE_SPEED


def spawn_obstacles(game):
    game["cactus_timer"] += 1
    game["bird_timer"] += 1

    # Spawn cactus
    if game["cactus_timer"] >= game["spawn_delay"]:
        game["cacti"].append(Cactus(WIDTH))
        game["cactus_timer"] = 0
        game["spawn_delay"] = random.randint(60, 170)

    # Spawn bird
    if game["bird_timer"] >= 500:
        game["birds"].append(Bird(WIDTH))
        game["bird_timer"] = 0


def update_obstacles(game):
    for cactus in game["cacti"]:
        cactus.update()

    for bird in game["birds"]:
        bird.update()

    # Remove off-screen obstacles
    game["cacti"] = [c for c in game["cacti"] if c.x > -50]
    game["birds"] = [b for b in game["birds"] if b.x > -50]


def update_ground(game):
    game["ground_x1"] -= GROUND_SPEED
    game["ground_x2"] -= GROUND_SPEED

    if game["ground_x1"] <= -WIDTH:
        game["ground_x1"] = WIDTH

    if game["ground_x2"] <= -WIDTH:
        game["ground_x2"] = WIDTH


def check_collisions(game):
    global high_score

    player = game["player"]

    for obstacle in game["cacti"] + game["birds"]:

        if player.rect.colliderect(obstacle.rect):

            player.die_sound.play()

            if game["score"] > high_score:
                high_score = game["score"]
                save_high_score(high_score)

            game["game_over"] = True
            break


# =========================
# DRAW FUNCTIONS
# =========================
def draw_background(game):
    bg = game["background_value"]

    screen.fill((bg, bg, bg))

def draw_ground(game):
    screen.blit(ground_image, (game["ground_x1"], GROUND_Y))
    screen.blit(ground_image, (game["ground_x2"], GROUND_Y))

def draw_score(game):
    score_text = font.render(
        f"{game['score']:05d}",
        True,
        (83, 83, 83)
    )
    high_text = font.render(
        f"HI {high_score:05d}",
        True,
        (83, 83, 83)
    )
    screen.blit(score_text, (WIDTH - 120, 20))
    screen.blit(high_text, (WIDTH - 270, 20))


def draw_game_over():
    over_text = font.render(
        "GAME OVER",
        True,
        (83, 83, 83)
    )

    restart_text = font.render(
        "PRESS SPACE TO RESTART",
        True,
        (120, 120, 120)
    )

    over_rect = over_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 40)
    )

    restart_rect = restart_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 10)
    )

    screen.blit(over_text, over_rect)
    screen.blit(restart_text, restart_rect)


def draw_objects(game):
    game["player"].draw(screen)

    for cactus in game["cacti"]:
        cactus.draw(screen)

    for bird in game["birds"]:
        bird.draw(screen)


# =========================
# MAIN GAME LOOP
# =========================
running = True

while running:

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if (game["game_over"]and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            game = reset_game()

    # ---------------- UPDATE ----------------
    if not game["game_over"]:

        game["score"] += 1

        game["player"].update()

        update_background(game)
        spawn_obstacles(game)
        update_obstacles(game)
        update_ground(game)

        check_collisions(game)

    # ---------------- DRAW ----------------
    draw_background(game)

    draw_ground(game)

    draw_objects(game)

    draw_score(game)

    if game["game_over"]:
        draw_game_over()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()