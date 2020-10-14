import pygame
import random
from math import sqrt

"""pip install -r requirements.txt
"""
# Creating a window
pygame.init()
pygame.display.set_caption("'97 Retro Snake Game!")
window = pygame.display.set_mode((720, 720))
window.set_alpha(None)
pygame.display.update()

# Initialising pygame mixer
pygame.mixer.init()

# Game clock
clock = pygame.time.Clock()

# Creating a home screen
def home_screen(window):
    exit_game = False
    pygame.display.set_mode((1200, 800))
    pygame.mixer.music.load(r'sfx/game_music.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    while not exit_game:
        window.fill((163, 203, 56))
        snake_img = pygame.image.load(r"sprites/home_screen.jpg").convert_alpha()
        play_btn_image = pygame.image.load(r"sprites/play_button.png").convert_alpha()
        play_btn_image = pygame.transform.scale(play_btn_image, [350, 350])
        window.blit(snake_img, [0, 0])
        window.blit(play_btn_image, [800, 200])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] > 800 and pos[0] < 1150) and (pos[1] > 200 and pos[1] < 550):
                    pygame.mixer.music.stop()
                    gameloop()
        pygame.display.update()
        clock.tick(20)


# Game loop
def gameloop():
    pygame.display.set_caption("'97 Retro Snake Game!")
    window = pygame.display.set_mode((720, 720))
    window.set_alpha(None)
    pygame.display.update()

    # Game variables
    start_game = False
    exit_game = False
    game_over = False
    x_pos, y_pos = 360, 360
    x_velocity, y_velocity = 0, 0
    initial_velocity = 2.5
    food_x, food_y = random.randint(60, 600), random.randint(60, 600)
    score = 0
    direction = None
    fps = 25
    snake_size = 25
    snake_list = []
    font = pygame.font.Font(r"fonts/MinecraftTen.ttf", 25)
    game_overFont = pygame.font.Font(r"fonts/MinecraftTen.ttf", 40)
    eat_count = 0
    # High score text file
    f = open(r"log/high_score.txt", mode="r")
    high_score = f.read()
    f.close()
    # Color dictionary & images
    color = {
        "white": (255, 255, 255),
        "red": (255, 107, 107),
        "yellow": (251, 197, 49),
        "cyan": (72, 219, 251)
    }
    background_image = pygame.image.load(r"sprites/background.png").convert_alpha()
    apple_img = pygame.image.load(r"sprites/food.png").convert_alpha()
    apple_img = pygame.transform.scale(apple_img, (35, 35))
    mushroom_img = pygame.image.load(r"sprites/mushroom.png").convert_alpha()
    mushroom_img = pygame.transform.scale(mushroom_img, (35, 35))

    # Game Functions
    def display_text(text, text_color, x, y):
        screen_text = font.render(text, True, text_color)
        window.blit(screen_text, [x, y])

    def draw_snake(window, snake_color, snakeSize_list, snake_size):
        for x, y in snakeSize_list:
            pygame.draw.rect(window, snake_color, [x, y, snake_size, snake_size])

    while not exit_game:
        if game_over:
            window.blit(background_image, [0, 0])
            window.blit(game_overFont.render("GAME OVER!", True, color["white"]), [270, 350])
            window.blit(font.render("Press SPACE To Play Again", True, color["cyan"]), [220, 400])
            display_text(f"SCORE {score}", color["yellow"], 325, 440)
            display_text(f"HI {high_score}", color["yellow"], 345, 470)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        home_screen(window)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and (direction != "down"):
                        y_velocity -= initial_velocity
                        x_velocity = 0
                        direction = "up"
                        start_game = True
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (direction != "up"):
                        y_velocity += initial_velocity
                        x_velocity = 0
                        direction = "down"
                        start_game = True
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (direction != "left"):
                        x_velocity += initial_velocity
                        y_velocity = 0
                        direction = "right"
                        start_game = True
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (direction != "right"):
                        x_velocity -= initial_velocity
                        y_velocity = 0
                        direction = "left"
                        start_game = True
            # Moving snake
            x_pos += x_velocity
            y_pos += y_velocity

            # Setting up background
            window.fill(color["white"])
            window.blit(background_image, [0, 0])
            display_text(f"SCORE {score}", color["white"], 120, 25)
            display_text(f"HI {high_score}", color["cyan"], 505, 25)

            # Food for snake
            """To draw virtual rectangle for food placement"""
            # pygame.draw.rect(window, color["red"], [60,60, 600,600])
            if eat_count % 5 == 0 and eat_count != 0:
                mushroom = window.blit(mushroom_img, [food_x, food_y])
            else:
                apple = window.blit(apple_img, [food_x, food_y])
            dist = sqrt((x_pos - food_x) ** 2 + (y_pos - food_y) ** 2)
            if dist < 18:
                pygame.mixer.music.load(r"sfx/apple_sfx.wav")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                if eat_count % 5 == 0 and eat_count != 0:
                    score = score + 30
                else:
                    score = score + 20
                if initial_velocity < 18:
                    initial_velocity += 1
                eat_count += 1
                food_x, food_y = random.randint(60, 600), random.randint(60, 600)
                if score > int(high_score):
                    high_score = score
                    f = open(r"high_score.txt", mode="w")
                    f.write(str(high_score))
                    f.close()

            # Game over!
            # Creating head rectangle
            head = []
            head.append(x_pos)
            head.append(y_pos)
            snake_list.append(head)
            if len(snake_list) > snake_size:
                del snake_list[0]

            if head in snake_list[:-1] and start_game is True:
                pygame.mixer.music.load(r"sfx/game_over.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                game_over = True

            """To draw virtual rectangle for game over on wall touch"""
            # pygame.draw.rect(window, color["red"], [50,50, 620,620])
            if x_pos < 50 or y_pos < 50 or x_pos > 640 or y_pos > 640:
                pygame.mixer.music.load(r"sfx/game_over.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                game_over = True

            draw_snake(window, color["yellow"], snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    # Quitting game
    pygame.quit()
    quit()


# Driver Code
if __name__ == '__main__':
    home_screen(window)

