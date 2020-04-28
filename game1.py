import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
blue= (135,206,235)
gold = (255,215,0)

# Creating Game Window
screen_width = 1000
screen_height = 550
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg1 = pygame.image.load("Images\\first.jpg")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


# Function for showing text on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# Plot the snake on window
def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


exit_game = False


def welcome():
    global exit_game
    while not exit_game:
        gameWindow.blit(bgimg1, (0, 0))
        text_screen("Welcome to Snake game", white, 300, 200)
        text_screen("Enter Space to Play", white, 330, 250)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()

            pygame.display.update()
            clock.tick(60)


def gameLoop():
    # creating Game Specific Variables
    global exit_game
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    velocity_update = 5
    food_x = random.randint(30, screen_width - 30)
    food_y = random.randint(30, screen_height - 30)
    snake_size = 15
    score = 0
    fps = 70
    snake_list = []
    snake_length = 1
    # check if High Score file exist
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as fp:
            fp.write("0")

    with open("high_score.txt", "r") as fp:
        highscore = fp.read()

    # Creating a Game Loop
    while not exit_game:

        if game_over:
            with open("high_score.txt", "w") as fp:
                fp.write(str(highscore))
            gameWindow.fill(yellow)
            text_screen("Game Over!", red, 400, 200)
            text_screen("Score : {}".format(score), red, 425, 250)
            text_screen("Press Enter to go Home Screen", red, 210, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity_update
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -velocity_update
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -velocity_update

                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = velocity_update

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                pygame.mixer.music.load("Sounds\\Food.mp3")
                pygame.mixer.music.play()
                score += 1
                snake_length += 5
                food_x = random.randint(50, screen_width - 50)
                food_y = random.randint(50, screen_height - 50)
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(blue)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            text_screen("Score : {}    High Score : {}".format(score, highscore), red, 0, 0)

            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Sounds\\snake_died.mp3")
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("Sounds\\snake_died.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
pygame.quit()
quit()
