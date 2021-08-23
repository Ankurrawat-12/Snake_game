import pygame
import random
import os


pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
snake_colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (204, 255, 255), (0, 255, 128),
                (255, 102, 255), (255, 255, 102), (200, 229, 229), (60, 90, 250), (204, 144, 107), (116, 181, 253),
                (236, 181, 253), (86, 255, 137)]
i = 0
s_color = snake_colors[i]
# Creating window
screen_width = 600
screen_height = 400
gameWindow = pygame.display.set_mode((screen_width, screen_height,))

# Back Ground image
bg_img = pygame.image.load("images/game.jpg")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes")
pygame.display.update()

velocity_x = 0
velocity_y = 0
clock = pygame.time.Clock()
wall_collision = True
body_collision = True
font_type = 'Harrington'
fps = 60
font1 = pygame.font.SysFont(font_type, 45)
font2 = pygame.font.SysFont(font_type, 20)
font3 = pygame.font.SysFont(font_type, 25)
font4 = pygame.font.SysFont(font_type, 35)


def text_screen(font, text, color, x, y):
    screen_text = font.render(text, True, color,)
    gameWindow.blit(screen_text, (x, y))


def plot_snake(game_window, snk_list, snk_size):
    for x, y in snk_list:
        pygame.draw.rect(game_window, s_color, [x, y, snk_size, snk_size])


def movements(event, velocity):
    global velocity_y, velocity_x
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        if velocity_x != velocity and velocity_x != -velocity:
            velocity_x += velocity
            velocity_y = 0
        else:
            if velocity_x > 0:
                velocity_x = velocity
                velocity_y = 0
            elif velocity_x < 0:
                velocity_x = -velocity
                velocity_y = 0

    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        if velocity_x != velocity and velocity_x != -velocity:
            velocity_x -= velocity
            velocity_y = 0
        else:
            if velocity_x > 0:
                velocity_x = velocity
                velocity_y = 0
            elif velocity_x < 0:
                velocity_x = -velocity
                velocity_y = 0

    if event.key == pygame.K_UP or event.key == pygame.K_w:
        if velocity_y != velocity and velocity_y != -velocity:
            velocity_y -= velocity
            velocity_x = 0
        else:
            if velocity_y > 0:
                velocity_y = velocity
                velocity_x = 0
            elif velocity_y < 0:
                velocity_y = -velocity
                velocity_x = 0

    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        if velocity_y != velocity and velocity_y != -velocity:
            velocity_y += velocity
            velocity_x = 0
        else:
            if velocity_y > 0:
                velocity_y = velocity
                velocity_x = 0
            elif velocity_y < 0:
                velocity_y = -velocity
                velocity_x = 0


def settings():
    global body_collision, wall_collision, s_color, i
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        text_screen(font1, "Settings", blue, (screen_height / 2) - 60, 20)
        if body_collision:
            text_screen(font4, "Press B to turn off Body collision", red, (screen_height / 2) - 180, 100)
        else:
            text_screen(font4, "Press B to turn on Body collision", green, (screen_height / 2) - 180, 100)
        if wall_collision:
            text_screen(font4, "Press W to turn off Wall collision", red, (screen_height / 2) - 180, 160)
        else:
            text_screen(font4, "Press W to turn on Wall collision", green, (screen_height / 2) - 180, 160)
        text_screen(font4, "Press S to change snake color", s_color, (screen_height / 2) - 180, 220)
        text_screen(font4, "Press Space Bar to go to Home", black, (screen_height / 2) - 180, 280)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if body_collision:
                        body_collision = False
                    else:
                        body_collision = True
                if event.key == pygame.K_w:
                    if wall_collision:
                        wall_collision = False
                    else:
                        wall_collision = True
                if event.key == pygame.K_SPACE:
                    home()
                if event.key == pygame.K_s:
                    if i == len(snake_colors)-1:
                        i = 0
                        s_color = snake_colors[i]
                    elif i < len(snake_colors):
                        i += 1
                        s_color = snake_colors[i]

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


def home():
    pygame.mixer.music.load('Music/home.mp3')
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        text_screen(font1, "Welcome to Snakes", blue, (screen_height/2)-60, 20)
        text_screen(font4, "Press Space Bar to Play", black, (screen_height/2)-180, 100)
        text_screen(font4, "Press Enter for settings", black, (screen_height/2)-180, 160)
        text_screen(font4, "Press End to Quit", black, (screen_height/2)-180, 220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Music/back.mp3')
                    pygame.mixer.music.play()
                    game_loop()
                if event.key == pygame.K_RETURN:
                    settings()
                if event.key == pygame.K_END:
                    exit_game = True

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


# Game Loop
def game_loop():
    global velocity_y, velocity_x, wall_collision, body_collision
    # Game Specific variables
    exit_game = False
    game_over = False
    distance = 8
    snake_x = 300
    snake_y = 200
    score = 0
    velocity = 5
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt") as f:
            f.write("0")
    with open("high_score.txt", "r") as f:
        high_score = f.read()
    food_x = random.randint(44, screen_width - 48)
    food_y = random.randint(34, screen_height - 38)
    snake_size = 10
    food_size = snake_size
    snake_length = 1
    snake_list = []

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            text_screen(font3, "Game Over! Press Enter to Continue", red, (screen_width/2)-180, screen_height/2)
            text_screen(font3, "Press Space Bar to go Home", red, (screen_width/2)-140, (screen_height/2)+60)
            velocity_x = 0
            velocity_y = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('Music/back.mp3')
                        pygame.mixer.music.play()
                        game_loop()
                    if event.key == pygame.K_SPACE:
                        home()
        else:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        score += 50
                        snake_length += 10
                    else:
                        movements(event, velocity)
            food = [food_x, food_y]
            if food in snake_list:
                score += 10
                food_x = random.randint(44, screen_width - 48)
                food_y = random.randint(34, screen_height - 38)
                snake_length += 2
                if score > int(high_score):
                    high_score = score
            if abs(snake_x - food_x) < distance and abs(snake_y - food_y) < distance:
                score += 10
                food_x = random.randint(44, screen_width - 48)
                food_y = random.randint(34, screen_height - 38)
                snake_length += 2
                if score > int(high_score):
                    high_score = score
            snake_x += velocity_x
            snake_y += velocity_y
            gameWindow.fill(white)
            gameWindow.blit(bg_img, (0, 0))
            text_screen(font2, "Score : " + str(score) + " High score : " + str(high_score), blue, (screen_width / 2)
                        - 80, 10)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            head = [snake_x, snake_y]
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 42 or snake_x > screen_width-46 or snake_y < 32 or snake_y > screen_height-36:
                if wall_collision:
                    game_over = True
                    pygame.mixer.music.load('Music/over.mp3')
                    pygame.mixer.music.play()
                else:
                    if snake_x < 42:
                        snake_x = screen_width - 46
                    if snake_x > screen_width - 46:
                        snake_x = 42
                    if snake_y < 32:
                        snake_y = screen_height - 36
                    if snake_y > screen_height - 36:
                        snake_y = 32

            if head in snake_list[:-1]:
                if body_collision:
                    game_over = True
                    pygame.mixer.music.load('Music/over.mp3')
                    pygame.mixer.music.play()
            plot_snake(gameWindow, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

home()
