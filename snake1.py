import pygame
import sys
import random
from pygame.locals import *

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
SNAKE_COLOR = (44, 62, 80)  # Dark blue
HEAD_COLOR = (52, 152, 219)  # Light blue
FOOD_COLOR = (231, 76, 60)   # Red
BACKGROUND_COLOR = (236, 240, 241)   # Light gray
GRID_COLOR = (189, 195, 199)  # Gray

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings
FPS = 8
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 600
SCREEN_SIZE = 500
GRID_SIZE = 20
GRID_WIDTH = SCREEN_SIZE // GRID_SIZE
GRID_HEIGHT = SCREEN_SIZE // GRID_SIZE
MARGIN = 10
TOP_MARGIN = 90


class Snake(object):
    def __init__(self):
        self.color = SNAKE_COLOR
        self.create()

    def create(self):
        self.length = 2
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.segments = [(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + TOP_MARGIN - 10)]

    def control(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction

    def move(self):
        head = self.segments[0]
        x, y = self.direction

        new_head = (((head[0] - MARGIN) + (x * GRID_SIZE)) % SCREEN_SIZE,
                    ((head[1] - TOP_MARGIN) + (y * GRID_SIZE)) % SCREEN_SIZE)
        new_head = (new_head[0] + MARGIN, new_head[1] + TOP_MARGIN)

        self.segments.insert(0, new_head)

        if len(self.segments) > self.length:
            self.segments.pop()

        if new_head in self.segments[2:]:
            return False

        return True

    def draw(self, surface):
        head = self.segments[0]
        for segment in self.segments:
            draw_rectangle(surface, segment[0], segment[1], GRID_SIZE, GRID_SIZE, self.color)
        draw_rectangle(surface, head[0], head[1], GRID_SIZE, GRID_SIZE, HEAD_COLOR)

    def eat(self):
        self.length += 1


class Food(object):
    def __init__(self):
        self.color = FOOD_COLOR
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE + MARGIN,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE + TOP_MARGIN)

    def draw(self, surface):
        draw_rectangle(surface, self.position[0], self.position[1], GRID_SIZE, GRID_SIZE, self.color)


# Define a global variable to store the high score
high_score = 0

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food = Food()

    global high_score  # Access the global high score variable

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
                if event.key in keys:
                    handle_key_event(snake, event.key)
                elif event.key == K_ESCAPE:
                    if confirm_exit(display_surface):  # Ask for confirmation
                        pygame.quit()
                        sys.exit()

        if not snake.move():
            # Update high score if needed
            if snake.length - 2 > high_score:
                high_score = snake.length - 2
            game_over(display_surface)
            return

        display_surface.fill(BACKGROUND_COLOR)

        check_eating(snake, food)
        draw_grid(display_surface)
        draw_info(display_surface, snake.length, high_score)  # Pass high score to draw_info

        snake.draw(display_surface)
        food.draw(display_surface)

        pygame.display.update()
        clock.tick(FPS)


def confirm_exit(surface):
    font = pygame.font.Font(None, 30)
    text_surface = font.render('Are you sure you want to exit? (y/n)', True, GRAY)
    text_rect = text_surface.get_rect()
    text_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))
    surface.blit(text_surface, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    return True
                elif event.key == K_n:
                    return False

def pause_game(surface):
    font = pygame.font.Font(None, 50)
    text_surface = font.render('Paused', True, GRAY)
    text_rect = text_surface.get_rect()
    text_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))
    surface.blit(text_surface, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return  # Continue the game


def handle_key_event(snake, key):
    key_directions = {K_UP: UP, K_DOWN: DOWN, K_LEFT: LEFT, K_RIGHT: RIGHT}
    snake.control(key_directions[key])


def check_eating(snake, food):
    if snake.segments[0] == food.position:
        snake.eat()
        food.create()


def draw_rectangle(surface, left, top, width, height, color=BLACK):
    rectangle_surface = pygame.Surface((width, height))
    rectangle_surface.fill(color)
    rect = rectangle_surface.get_rect()
    rect.topleft = (left, top)
    surface.blit(rectangle_surface, rect)


def draw_grid(surface):
    for x in range(MARGIN + GRID_SIZE, WINDOW_WIDTH - MARGIN, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, TOP_MARGIN), (x, WINDOW_HEIGHT))
    for y in range(TOP_MARGIN, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (MARGIN, y), (WINDOW_WIDTH - MARGIN, y))


def draw_info(surface, score, high_score):
    font = pygame.font.Font(None, 30)
    score_text = f"Score: {score - 2}"
    high_score_text = f"High Score: {high_score}"
    score_surface = font.render(score_text, True, BLACK)
    high_score_surface = font.render(high_score_text, True, BLACK)
    score_rect = score_surface.get_rect()
    high_score_rect = high_score_surface.get_rect()
    score_rect.topleft = (MARGIN, TOP_MARGIN // 2)
    high_score_rect.topright = (WINDOW_WIDTH - MARGIN, TOP_MARGIN // 2)
    surface.blit(score_surface, score_rect)
    surface.blit(high_score_surface, high_score_rect)


def game_over(surface):
    font = pygame.font.Font(None, 50)
    text_surface = font.render('Game Over', True, GRAY)
    text_rect = text_surface.get_rect()
    text_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))
    surface.blit(text_surface, text_rect)

    # Render buttons
    button_font = pygame.font.Font(None, 30)
    new_game_text = button_font.render('Start New Game', True, BLACK)
    new_game_rect = new_game_text.get_rect()
    new_game_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2) + 50)
    surface.blit(new_game_text, new_game_rect)

    exit_text = button_font.render('Exit', True, BLACK)
    exit_rect = exit_text.get_rect()
    exit_rect.center = ((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2) + 100)
    surface.blit(exit_text, exit_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if new_game_rect.collidepoint(mouse_x, mouse_y):
                    main()  # Start a new game
                elif exit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_RETURN:
                    main()  # Start a new game
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()



if __name__ == '__main__':
    main()
