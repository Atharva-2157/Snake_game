import pygame
import random
import os

pygame.font.init()
pygame.mixer.init()

SCREENWIDTH = 1000
SCREENHEIGHT = 650
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
EXIT_GAME = False
SNAKE_SIZE = 15
FPS = 70
FPS_CLOCK = pygame.time.Clock()

GAME_WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Snake")

SOUNDS = {
    'FOOD_GAIN_BEEP': pygame.mixer.Sound('Sounds\\Food.wav'),
    'SNAKE_DIED_BEEP': pygame.mixer.Sound("Sounds\\snake_died.wav")
}

LABELS = {
    'PLAY': pygame.image.load('Images\\play.png'),
    'QUIT': pygame.image.load('Images\\quit.png'),
    'SCORE': pygame.image.load('Images\\score.png'),
    'HIGH SCORE': pygame.image.load('Images\\high_score.png'),
    'GAME_OVER': pygame.image.load('Images\\game_over.png')
}

IMAGES = {
    'WELCOME': pygame.image.load('Images\\first_edit.png'),
    'GAME_OVER': pygame.image.load('Images\\game_over.jpg'),
}

DIGITS = {
    '0': pygame.image.load('Images\\0.png'),
    '1': pygame.image.load('Images\\1.png'),
    '2': pygame.image.load('Images\\2.png'),
    '3': pygame.image.load('Images\\3.png'),
    '4': pygame.image.load('Images\\4.png'),
    '5': pygame.image.load('Images\\5.png'),
    '6': pygame.image.load('Images\\6.png'),
    '7': pygame.image.load('Images\\7.png'),
    '8': pygame.image.load('Images\\8.png'),
    '9': pygame.image.load('Images\\9.png'),
}

IMAGES['WELCOME'] = pygame.transform.scale(IMAGES['WELCOME'], (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
IMAGES['GAME_OVER'] = pygame.transform.scale(IMAGES['GAME_OVER'], (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
SCORE_IN_GAME = pygame.transform.scale(LABELS['SCORE'], (100, 60)).convert_alpha()
HIGH_SCORE = pygame.transform.scale(LABELS['HIGH SCORE'], (160, 60)).convert_alpha()


class Button:
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(GAME_WINDOW, self.color, [self.x, self.y, self.width, self.height])
        GAME_WINDOW.blit(self.text, (self.x, self.y))

    def isHover(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def plotSnake(snake_list):
    i = 1
    for x, y in snake_list:
        if i % 2 == 0:
            pygame.draw.rect(GAME_WINDOW, BLACK, [x, y, SNAKE_SIZE, SNAKE_SIZE])
        else:
            pygame.draw.rect(GAME_WINDOW, YELLOW, [x, y, SNAKE_SIZE, SNAKE_SIZE])
        i += 1


def welcomeWindow():
    global EXIT_GAME
    play_button = Button(LABELS['PLAY'], GREEN, 470, 200, 65, 35)
    quit_button = Button(LABELS['QUIT'], GREEN, 470, 300, 65, 35)

    while not EXIT_GAME:
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                EXIT_GAME = True

            if event.type == pygame.MOUSEMOTION:
                if play_button.isHover(position):
                    play_button.color = YELLOW
                else:
                    play_button.color = GREEN

                if quit_button.isHover(position):
                    quit_button.color = RED
                else:
                    quit_button.color = GREEN

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.isHover(position):
                    return
                if quit_button.isHover(position):
                    EXIT_GAME = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        GAME_WINDOW.blit(IMAGES['WELCOME'], (0, 0))
        # GAME_WINDOW.fill(WHITE)
        play_button.draw()
        quit_button.draw()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def gameLoop():
    global EXIT_GAME
    game_over = False
    snake_x = 100
    snake_y = 100
    snake_length = 1
    snake_list = []
    direction_x = 0
    direction_y = 0
    temp_x = 0
    temp_y = 0
    velocity = 4
    food_x = random.randint(0, SCREENWIDTH - SNAKE_SIZE)
    food_y = random.randint(60, SCREENHEIGHT - SNAKE_SIZE)
    score = 0

    if not os.path.exists('HighScore.txt'):
        with open('HighScore.txt', 'w') as f:
            f.write('0')

    with open('HighScore.txt', 'r') as f:
        high_score = int(f.read())

    while not EXIT_GAME:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            with open('HighScore.txt', 'w') as f:
                f.write(str(high_score))

            # GAME_WINDOW.fill(YELLOW)
            GAME_WINDOW.blit(IMAGES['GAME_OVER'], (0, 0))
            GAME_WINDOW.blit(LABELS['GAME_OVER'], (300, 50))
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if direction_y > 0 or temp_y > 0:
                            pass
                        else:

                            direction_x = 0
                            direction_y = -velocity
                            temp_x, temp_y = [direction_x, direction_y]

                    if event.key == pygame.K_DOWN:
                        if direction_y < 0 or temp_y < 0:
                            pass
                        else:
                            direction_x = 0
                            direction_y = velocity
                            temp_x, temp_y = [direction_x, direction_y]

                    if event.key == pygame.K_RIGHT:
                        if direction_x < 0 or temp_x < 0:
                            pass
                        else:
                            direction_x = velocity
                            direction_y = 0
                            temp_x, temp_y = [direction_x, direction_y]

                    if event.key == pygame.K_LEFT:
                        if direction_x > 0 or temp_x > 0:
                            pass
                        else:
                            direction_x = -velocity
                            direction_y = 0
                            temp_x, temp_y = [direction_x, direction_y]

                    if event.key == pygame.K_SPACE:
                        if direction_x != 0 or direction_y != 0:
                            temp_x, temp_y = [direction_x, direction_y]
                            direction_x = direction_y = 0
                        else:
                            # assert isinstance(temp_y, int)
                            [direction_x, direction_y] = temp_x, temp_y

                    if event.key == pygame.K_q:
                        game_over = True

            snake_x += direction_x
            snake_y += direction_y

            if snake_x > SCREENWIDTH:
                snake_x = 0
            elif snake_y > SCREENHEIGHT:
                snake_y = 50
            elif snake_x < 0:
                snake_x = SCREENWIDTH
            elif snake_y < 50:
                snake_y = SCREENHEIGHT

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 1
                snake_length += 4
                food_x = random.randint(0, SCREENWIDTH - SNAKE_SIZE)
                food_y = random.randint(60, SCREENHEIGHT - SNAKE_SIZE)
                if score > high_score:
                    high_score = score
                SOUNDS['FOOD_GAIN_BEEP'].play()

            head = [snake_x, snake_y]

            if head not in snake_list:
                snake_list.append(head)

            if snake_length < len(snake_list):
                snake_list.pop(0)

            if head in snake_list[:-1]:
                game_over = True
                SOUNDS['SNAKE_DIED_BEEP'].play()

            GAME_WINDOW.fill(BLUE)
            pygame.draw.rect(GAME_WINDOW, WHITE, [0, 0, SCREENWIDTH, 50])

            GAME_WINDOW.blit(SCORE_IN_GAME, (10, -6))
            k = 0
            my_digits = [x for x in str(score)]
            for i in my_digits:
                GAME_WINDOW.blit(DIGITS[i], (106 + (k * 30), 4))
                k += 1

            GAME_WINDOW.blit(HIGH_SCORE, (300, -6))
            k = 0
            my_digits = [x for x in str(high_score)]
            for i in my_digits:
                GAME_WINDOW.blit(DIGITS[i], (466 + (k * 30), 4))
                k += 1

            pygame.draw.rect(GAME_WINDOW, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
            plotSnake(snake_list)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    while not EXIT_GAME:
        welcomeWindow()
        gameLoop()

    pygame.quit()
