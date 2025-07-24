import pygame
import sys

pygame.init()

# Screen setup
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Guy Gets a Taco")
icon = pygame.image.load("images/taco.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
fps = 24

# Load images
player_image = pygame.image.load("images/player.png")
enemy_image = pygame.image.load("images/enemy.png")
taco_image = pygame.image.load("images/taco.png")
taco_truck_image = pygame.image.load("images/taco truck.png")

# Player properties
player_x = 10
player_y = 40
player_width = player_image.get_width()
player_height = player_image.get_height()
player_speed = 15
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Enemy properties
enemy_width = enemy_image.get_width()
enemy_height = enemy_image.get_height()
enemy = pygame.Rect(100, 100, enemy_width, enemy_height)

# Taco truck destination
taco_truck = pygame.Rect(400, 300, taco_truck_image.get_width(), taco_truck_image.get_height())

# Taco items
taco_width = taco_image.get_width()
taco_height = taco_image.get_height()
tacos = [
    pygame.Rect(300, 100, taco_width, taco_height),
    pygame.Rect(400, 100, taco_width, taco_height)
]

# Colors
player_color = (14, 0, 255)
bg_color = (255, 0, 0)
taco_color = (0, 0, 0)
text_color = (255, 255, 255)
ui_color = (0, 0, 0)
title_color = (132, 132, 176)
game_over_color = (204, 0, 0)
you_win_color = (235, 116, 26)

# Font
game_font = pygame.font.SysFont(None, 30)

# Game state
score = 0
game_scene = "title"
score_ui = pygame.Rect(0, 0, screen_width, 40)


def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_enemies():
    global game_scene
    screen.blit(enemy_image, enemy)
    if player.colliderect(enemy):
        game_scene = "game_over"


def draw_tacos():
    global score
    for taco in tacos[:]:
        screen.blit(taco_image, (taco.x, taco.y))
        if taco.colliderect(player):
            tacos.remove(taco)
            score += 15


def draw_sprites():
    global game_scene
    screen.blit(player_image, player)
    draw_enemies()
    draw_tacos()
    screen.blit(taco_truck_image, taco_truck)
    if player.colliderect(taco_truck):
        game_scene = "you_win"
    pygame.draw.rect(screen, ui_color, score_ui)
    draw_text("Score: " + str(score), game_font, text_color, 10, 10)


# Game loop
while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_scene == "title":
                    game_scene = "level"
                elif game_scene in ["game_over", "you_win"]:
                    game_scene = "title"

    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        player.x += player_speed
    elif key[pygame.K_a]:
        player.x -= player_speed
    elif key[pygame.K_w]:
        player.y -= player_speed
    elif key[pygame.K_s]:
        player.y += player_speed

    # Game rendering
    if game_scene == "level":
        screen.fill(bg_color)
        draw_sprites()
    elif game_scene == "title":
        screen.fill(title_color)
        draw_text("Press SPACE to start", game_font, text_color, 200, 200)
    elif game_scene == "game_over":
        screen.fill(game_over_color)
        draw_text("Game Over! Press SPACE to retry", game_font, text_color, 150, 200)
    elif game_scene == "you_win":
        screen.fill(you_win_color)
        draw_text("You Win! Press SPACE to play again", game_font, text_color, 150, 200)

    pygame.display.flip()
