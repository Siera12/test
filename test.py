import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Catch Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

# Falling object settings
obj_size = 30
obj_speed = 5
num_objects = 3
objects = []
for _ in range(num_objects):
    obj_x = random.randint(0, WIDTH - obj_size)
    obj_y = random.randint(-HEIGHT, 0)
    objects.append([obj_x, obj_y])

# Score
score = 0
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Sounds
catch_sound = None
gameover_sound = None

clock = pygame.time.Clock()
game_over = False

def reset_game():
    global score, player_x, objects, game_over
    score = 0
    player_x = WIDTH // 2 - player_size // 2
    objects = []
    for _ in range(num_objects):
        obj_x = random.randint(0, WIDTH - obj_size)
        obj_y = random.randint(-HEIGHT, 0)
        objects.append([obj_x, obj_y])
    game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Move falling objects
        for obj in objects:
            obj[1] += obj_speed
            # Collision detection
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            obj_rect = pygame.Rect(obj[0], obj[1], obj_size, obj_size)
            if player_rect.colliderect(obj_rect):
                score += 1
                # catch_sound.play()  # No sound available
                obj[0] = random.randint(0, WIDTH - obj_size)
                obj[1] = random.randint(-HEIGHT, 0)
            elif obj[1] > HEIGHT:
                game_over = True
                # gameover_sound.play()  # No sound available

    # Drawing
    screen.fill(WHITE)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, BLUE, player_rect)
    for obj in objects:
        obj_rect = pygame.Rect(obj[0], obj[1], obj_size, obj_size)
        pygame.draw.rect(screen, RED, obj_rect)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)