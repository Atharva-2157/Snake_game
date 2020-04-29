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
blue = (135, 206, 235)
gold = (255, 215, 0)

# Creating Game Window
screen_width: int = 1000
screen_height: int = 550
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg1 = pygame.image.load("Images\\first.jpg")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()


# Function for showing text on screen
def text_screen(text, color, font_size, x, y):
    font = pygame.font.SysFont(None, font_size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# Plot the snake on window
def plot_snake(game_window, snake_list, snake_size):
    i = 1
    for x, y in snake_list:
        if i % 2 == 1:
            pygame.draw.rect(game_window, yellow, [x, y, snake_size, snake_size])
        else:
            pygame.draw.rect(game_window, black, [x, y, snake_size, snake_size])
        i += 1


exit_game = False


def welcome():
    global exit_game
    while not exit_game:
        gameWindow.blit(bgimg1, (0, 0))
        text_screen("Welcome to Snake game", white, 55, 300, 200)
        text_screen("Press Space to Play", white, 55, 330, 250)
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
    game_over: bool = False
    snake_x: int = 45
    snake_y: int = 55
    velocity_x: int = 0
    velocity_y: int = 0
    velocity_update: int = 4
    food_x: int = random.randint(30, screen_width - 30)
    food_y: int = random.randint(30, screen_height - 30)
    snake_size: int = 15
    score: int = 0
    fps: int = 70
    snake_list: list = []
    snake_length: int = 1
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
            text_screen("Game Over!", red, 55, 400, 200)
            text_screen("Score : {}".format(score), red, 55, 425, 250)
            text_screen("Press Enter to go Home Screen", red, 55, 210, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            # When user enter close then gmae will get quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # If any key get pressed
                if event.type == pygame.KEYDOWN:
                    # Handling events for certain keys
                    if event.key == pygame.K_RIGHT:
                        # Move the snake in right direction
                        # Except when it moves in left direction
                        if velocity_x == -velocity_update:
                            pass
                        else:
                            velocity_x = velocity_update
                            velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        # Move the snake in left direction
                        # Except when it moves in right direction
                        if velocity_x == velocity_update:
                            pass
                        else:
                            velocity_x = -velocity_update
                            velocity_y = 0

                    if event.key == pygame.K_UP:
                        # Move the snake in upward direction
                        # Except when it moves in downward direction
                        if velocity_y == velocity_update:
                            pass
                        else:
                            velocity_x = 0
                            velocity_y = -velocity_update

                    if event.key == pygame.K_DOWN:
                        # Move the snake in downward direction
                        # Except when it moves in upward direction
                        if velocity_y == -velocity_update:
                            pass
                        else:
                            velocity_x = 0
                            velocity_y = velocity_update

                    if event.key == pygame.K_SPACE:
                        velocity_x = velocity_y = 0

            # Snake moves in its corresponding direction
            snake_x += velocity_x
            snake_y += velocity_y

            gameWindow.fill(blue)
            pygame.draw.rect(gameWindow, black, [0, 0, screen_width, snake_size])
            pygame.draw.rect(gameWindow, black, [0, 0, snake_size, screen_height])
            pygame.draw.rect(gameWindow, black, [0, screen_height, screen_width, -snake_size])
            pygame.draw.rect(gameWindow, black, [screen_width - snake_size, 0, screen_width, screen_height])

            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            text_screen("Score : {}    High Score : {}".format(score, highscore), white, 25, 16, 0)

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                pygame.mixer.music.load("Sounds\\Food.mp3")
                pygame.mixer.music.play()  # Sound clip play when snake eat food
                score += 1  # Score increment
                snake_length += 4  # Increasing snake length
                # Creates food at different place
                food_x = random.randint(50, screen_width - 50)
                food_y = random.randint(50, screen_height - 50)
                # Maintaining high score
                if score > int(highscore):
                    highscore = score

            head = [snake_x, snake_y]
            if head not in snake_list:
                snake_list.append(head)
            # print(snake_list[-1])

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Sounds\\snake_died.mp3")
                pygame.mixer.music.play()

            if snake_x < snake_size or snake_x > screen_width - snake_size or snake_y < snake_size or snake_y > screen_height - snake_size:
                game_over = True
                pygame.mixer.music.load("Sounds\\snake_died.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    welcome()
    pygame.quit()
    quit()
