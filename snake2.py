import pygame
import sys
import random
from pygame.locals import *
import heapq

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
SNAKECOLOR = (167, 187, 199)
HEADCOLOR = (41, 120, 181)
FOODCOLOR = (218, 127, 143)
BGCOLOR = (225, 229, 234)
SCREENCOLOR = (250, 243, 243)

FPS = 20

WINDOW_WIDTH = 520
WINDOW_HEIGHT = 600
SCREEN_SIZE = 500

GRID_SIZE = 20
GRID_WIDTH = SCREEN_SIZE // GRID_SIZE
GRID_HEIGHT = SCREEN_SIZE // GRID_SIZE

MARGIN = 10
TOP_MARGIN = 90

class Node(object):
    def __init__(self, board, coords, nodeID, parent, f, g, head, direction):
        self.board = board
        self.coords = coords
        self.f = f
        self.g = g
        self.head = head
        self.info = {'id': nodeID, 'parent': parent, 'direction': direction}

    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        else:
            return self.f < other.f

    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, Node):
            return False
        return self.f == other.f

# A* Algorithm 
class SnakeAI(object):
    def __init__(self, direction):
        self.coords = [] 
        self.path = None
        self.nodeID = 0
        self.direction = self.getDirection(direction) # 
        self.board = self.getBoard() # 

    # pixel 
    def getBoard(self):
        board = [[0 for x in range(27)] for y in range(27)]
        for i in range(27):
            board[0][i] = board[26][i] = board[i][0] = board[i][26] = 2
        return board

    def getXY(self, coord):
        x = (coord[0] - 10) // 20 + 1
        y = (coord[1] - 90) // 20 + 1
        return x, y

    
    def getDirection(self, direction):
        move = [UP, DOWN, LEFT, RIGHT]
        return move.index(direction)

    
    def clearBoard(self):
        for x in range(1, len(self.board) - 1, 1):
            for y in range(1, len(self.board[0]) - 1, 1):
                self.board[y][x] = 0

    
    def denoteXY(self, coords, coord):
        self.coords.clear()
        x, y = self.getXY(coord)
        self.goal = x, y
        self.board[y][x] = 1
        self.head = self.getXY(coords[0])

        for coord in coords:
            x, y = self.getXY(coord)
            self.coords.append((x, y))
            self.board[y][x] = 2


    def getNextDirection(self, coords, coord):
        if not self.path:
            self.findPath(coords, coord)
        if self.path:
            return self.path.pop()
        else:
            return -1

    # Node  
    # coords 
    def copyCoords(self, coords):
        coordies = []

        for coord in coords:
            coordies.append(coord)

        return coordies

    # Node board
    def copyBoard(self, coords):
        board = self.getBoard()

        for coord in coords:
            x, y = coord
            board[y][x] = 2
        x, y = self.goal
        board[y][x] = 1

        return board

    
    def getHeuristic(self, x, y):
        x1, y1 = self.goal
        return (abs(x - x1) + abs(y - y1))

    
    def findPath(self, coords, coord):
        self.clearBoard()
        self.denoteXY(coords, coord)
        self.path = self.aStar()

   
    def aStar(self):
        h = self.getHeuristic(self.head[0], self.head[1])
        g = 0
        node = Node(self.board, self.coords, 0, 0, h, g, self.coords[0], self.direction)
        open = []
        close = []
        self.expandNode(open, node)

        while open:
            node = heapq.heappop(open)

            if g < node.g:
                g = node.g
            if g - node.g > 1:
                continue

            if node.head == self.goal:
                return self.makePath(close, node.info)

            close.append(node.info)
            self.expandNode(open, node)

        if close:
            path = [close[0]['direction']]
            return path

        return


    def isHole(self, x, y, direction, board):
        if y - 1 >= 0 and direction > 1:
            if x == 25 and board[y - 1][x] == 2:
                return 10

        if y + 1 < 27 and direction > 1:
            if board[y + 1][x] == 2 and x == 1:
                return 10

        if y + 1 < 27 and y - 1 >= 0 and direction > 1:
            if board[y + 1][x] == 2 and board[y - 1][x] == 2:
                return 10
            if (board[y + 1][x] == 2 or board[y - 1][x] == 2):
                return 0

        if x - 1 >= 0 and direction < 2:
            if y == 25 and board[y][x - 1] == 2:
                return 10

        if x + 1 < 27 and direction < 2:
            if board[y][x + 1] == 2 and y == 1:
                return 10

        if x + 1 < 27 and x - 1 >= 0 and direction < 2:
            if board[y][x + 1] == 2 and board[y][x - 1] == 2:
                return 10
            if (board[y][x + 1] == 2 or board[y][x - 1] == 2):
                return 0

        return 3


    def expandNode(self, open, nodes):
        moves = [UP, DOWN, LEFT, RIGHT]
        x, y = nodes.head

        for i in range(4):
            dx, dy = moves[i]
            x1 = x + dx
            y1 = y + dy
            if nodes.board[y1][x1] < 2:
                coords = self.copyCoords(nodes.coords)
                head = (x1, y1)
                coords.insert(0, head)
                coords.pop()
                board = self.copyBoard(coords)
                h = self.getHeuristic(x1, y1)
                if h > 0:
                    h1 = self.isHole(x1, y1, i, board)
                    h += h1
                g = nodes.g + 1
                self.nodeID += 1
                id = self.nodeID
                parent = nodes.info['id']
                node = Node(board, coords, id, parent, g + h, g, head, i)
                heapq.heappush(open, node)

    def makePath(self, closed, information):
        path = [information['direction']]

        while closed:
            info = closed.pop()
            if info['id'] == information['parent']:
                path.append(info['direction'])
                information = info

        return path




class Snake(object):
    def __init__(self):
        self.color = SNAKECOLOR
        self.create()

    
    def create(self):
        self.length = 2 
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) 
        self.coords = [(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + TOP_MARGIN - 10)]

    def control(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction

    
    def move(self):
        cur = self.coords[0]
        x, y = self.direction

        new = (((cur[0] - MARGIN) + (x * GRID_SIZE)) % SCREEN_SIZE,
               ((cur[1] - TOP_MARGIN) + (y * GRID_SIZE)) % SCREEN_SIZE)
        new = (new[0] + MARGIN, new[1] + TOP_MARGIN)

        self.coords.insert(0, new)

        if len(self.coords) > self.length:
            self.coords.pop()

        if new in self.coords[1:]:
            return False

        return True

    
    def draw(self):
        head = self.coords[0]
        for c in self.coords:
            drawRect(c[0] + 1, c[1] + 1, GRID_SIZE - 1, GRID_SIZE - 1, self.color)

        drawRect(c[0] + 1, c[1] + 1, GRID_SIZE - 1, GRID_SIZE - 1, SNAKECOLOR)
        drawRect(head[0] - 1, head[1], GRID_SIZE -  1, GRID_SIZE - 1, HEADCOLOR)

    
    def eat(self):
        self.length += 1


class Feed(object):
    def __init__(self):
        self.color = FOODCOLOR
        self.create()

    def create(self):
        self.coord = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE + MARGIN,
                      random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE + TOP_MARGIN)

    def draw(self):
        drawRect(self.coord[0], self.coord[1], GRID_SIZE, GRID_SIZE, self.color)


def main():
    global CLOCK # FPS 
    global DISPLAY 

    snake = Snake()
    feed = Feed()

    pygame.init()

    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    DISPLAY.fill(BGCOLOR)
    pygame.display.set_caption('2021-1 Artificial Intelligence Project')
    pygame.display.flip()

    while True:
        runGame(snake, feed)
        gameOver()


def runGame(snake, feed):

    screenRect, screenSurf = drawRect(MARGIN, TOP_MARGIN, SCREEN_SIZE, SCREEN_SIZE, SCREENCOLOR)
    infoRect, infoSurf = drawRect(MARGIN, MARGIN, SCREEN_SIZE, TOP_MARGIN - 20)

    path = None
    keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
    sa = SnakeAI(snake.direction)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN:
                if e.key in keys:
                    execEvent(snake, e.key)

        path = sa.getNextDirection(snake.coords, feed.coord)
        if path >= 0:
            execEvent(snake, keys[path])

        if not snake.move():
            snake.draw()
            return

        renderRect(screenSurf, screenRect, SCREENCOLOR)
        renderRect(infoSurf, infoRect, BGCOLOR)

        eatCheck(snake, feed, sa)
        drawGrid()
        showTitle()
        showGameInfo(snake.length)

        pygame.display.update(screenRect)
        pygame.display.update(infoRect)

        CLOCK.tick(FPS)


def eatCheck(snake, feed, sa):
    snake.draw()
    feed.draw()

    if snake.coords[0] == feed.coord:
        snake.eat()

        while True:
            feed.create()
            if feed.coord not in snake.coords:
                break
    return

def execEvent(snake, key):
    event = {K_UP: UP, K_DOWN: DOWN, K_LEFT: LEFT, K_RIGHT: RIGHT}
    snake.control(event[key])


def terminate():
    pygame.quit()
    sys.exit()

def renderRect(surf, rect, color):
    surf.fill(color)
    DISPLAY.blit(surf, rect)

def drawRect(left, top, width, height, color=BLACK):
    surf = pygame.Surface((width, height))
    rect = pygame.Rect(left, top, width, height)
    renderRect(surf, rect, color)
    return (rect, surf)

# 
def makeText(font, text, color, bgcolor, x, y):
    surf = font.render(text, True, color, bgcolor)
    rect = surf.get_rect()
    rect.center = (x, y)
    DISPLAY.blit(surf, rect)
    return rect

# 
def showTitle():
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = ('AI Snake')
    x = (MARGIN + SCREEN_SIZE) // 2
    y = 35
    return makeText(font, text, BLACK, BGCOLOR, x, y)

# 
def showGameInfo(length):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = ("Score: " + str(length - 2))
    x = (MARGIN + SCREEN_SIZE) // 2
    y = 70
    return makeText(font, text, BLACK, BGCOLOR, x, y)


def drawGrid():
    for x in range(MARGIN + GRID_SIZE, WINDOW_WIDTH - MARGIN, GRID_SIZE):
        pygame.draw.line(DISPLAY, BGCOLOR, (x, TOP_MARGIN), (x, 600))
    for y in range(TOP_MARGIN, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(DISPLAY, BGCOLOR, (0, y), (600, y))


def gameOver():
    font = pygame.font.Font('freesansbold.ttf', 100)

    x = (SCREEN_SIZE // 2) + MARGIN
    y = (WINDOW_HEIGHT // 2) - 30
    makeText(font, 'Game', GRAY, None, x, y)

    y = (WINDOW_HEIGHT // 2) + 80
    makeText(font, 'Over', GRAY, None, x, y)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
