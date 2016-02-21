import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.init()
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
walls = pygame.sprite.Group()
weals = pygame.sprite.Group()
woes = pygame.sprite.Group()
passable_blocks = pygame.sprite.Group()
impassable_blocks = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    global screen_height, screen_width
    wealPoints = 10
    woePoints = -100
    tiles = []
    maze = []
    debug = True
    blockWidth = 0
    blockHeight = 0

    def __init__(self, maze, color, width, height):
        super().__init__()
        self.maze = maze[0]
        self.tiles = maze[1]
        rows = len(self.maze[0])
        cols = len(self.maze)
        self.blockWidth = screen_width / cols
        self.blockHeight = screen_height / rows
        self.blockHeight = 20
        self.blockWidth = 20
        # self.image = pygame.Surface([self.blockWidth, self.blockHeight])
        self.image = pygame.Surface([self.blockWidth, self.blockHeight])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self._col = 1
        self._row = 1
        self.weals = 0
        self.woes = 0
        self.moves = 0
        self.score = 0
        self.rect.x = self.blockWidth * 2
        self.rect.y = self.blockHeight
        self.movingDown = True

    def _move(self, dCol, dRow):
        self.moves += 1
        newCol = self._col + dCol
        newRow = self._row + dRow
        destination = self.maze[newCol][newRow]
        if not destination == self.tiles['wall']:
            self.rect.x += dCol * self.blockWidth
            self.rect.y += dRow * self.blockHeight
            self.maze[self._col][self._row] = self.tiles['blank']
            self._col = newCol
            self._row = newRow
            self.maze[self._col][self._row] = self.tiles['player']
            if destination == self.tiles['weal']:
                self.weals += 1
            if destination == self.tiles['woe']:
                self.woes += 1
                # self.sayMaze()
        else:
            print("move failed")
            self.score -= 1000

    def moveUp(self):
        self._move(0, -1)

    def moveDown(self):
        self._move(0, 1)

    def moveRight(self):
        self._move(1, 0)

    def moveLeft(self):
        self._move(-1, 0)

    def dSay(self, message):
        if self.debug:
            print(message)

    def calculateScore(self):
        score = self.wealPoints * self.weals + self.woePoints * self.woes - self.moves
        return score

    def basicAI(self):
        if not self.maze[self._col + 1][self._row] == self.tiles['wall']:
            self.moveRight()
            print("moving right")
        elif not self.maze[self._col][self._row + 1] == self.tiles['wall'] and self.movingDown:
            return self.moveDown()

        if self.maze[self._col][self._row + 1] == self.tiles['wall']:
            self.movingDown = False
        elif not self.maze[self._col][self._row - 1] == self.tiles['wall'] and not self.movingDown:
            return self.moveUp()
        elif self.maze[self._col][self._row - 1] == self.tiles['wall']:
            self.movingDown = True

    def sayMaze(self):
        rows = len(self.maze[0])
        cols = len(self.maze)

        for row in range(rows):
            newRow = []
            message = ''
            for col in range(cols):
                newRow.append(self.maze[col][row])
            for c in newRow:
                message += c
                message += ' '
            self.dSay(message)
        self.dSay("")


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


def create_maze():
    tiles = {'wall': 'X',
             'weal': '+',
             'woe': '-',
             'blank': ' ',
             'player': 'P'}

    # maze config

    config = createRandomMapConfig()
    rows = config[0]
    cols = config[1]
    openSpaces = config[2]
    numWeals = config[3]
    numWoes = config[4]

    maze = createWalls(cols, rows, openSpaces, tiles)
    if not maze == 'invalid':
        maze = fillOtherCrap(numWeals, numWoes, maze, tiles)

    return maze, tiles


def createRandomMapConfig():
    rows = random.randint(4, 100)
    cols = random.randint(4, 100)
    rows = 10
    cols = 8
    openSpaces = random.randint(2, rows - 1)
    numWeals = int(abs(random.gauss(0, rows * cols * .1)))
    numWoes = int(abs(random.gauss(0, rows * cols * .1)))
    return rows, cols, openSpaces, numWeals, numWoes


def createWalls(cols, rows, openSpaces, tiles):
    if openSpaces < rows:
        maze = []
        i = 2
        if cols % 2 == 0:
            i = 1
        for col in range(cols + i):
            maze.append([])
            for row in range(rows + 2):
                if row == 0:
                    maze[col].append(tiles['wall'])
                if row == rows + 1:
                    maze[col].append(tiles['wall'])
                else:
                    if col % 2 == 0:
                        maze[col].append(tiles['wall'])
                    else:
                        maze[col].append(tiles['blank'])
        for col in range(cols):

            if col % 2 == 0 and col > 0:
                openSpacesThisCol = openSpaces
                while openSpacesThisCol > 0:
                    r = random.randint(1, rows - 1)
                    if maze[col][r] == tiles['wall']:
                        openSpacesThisCol -= 1
                        maze[col][r] = tiles['blank']

    else:
        print("Unacceptable wall parameters")
        return "invalid"
    return maze


def fillOtherCrap(numWeals, numWoes, maze, tiles):
    rows = len(maze[0])
    cols = len(maze)

    if (numWeals + numWoes) > .5 * rows * cols:
        print("Unacceptable maze parameters in fillOtherCrap")
        return 'invalid'
    while numWeals > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['weal']
            numWeals -= 1
    while numWoes > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['woe']
            numWoes -= 1
    return maze


def createSpritesFromMazeList(player):
    maze = player.maze
    rows = len(maze[0])
    cols = len(maze)
    blockWidth = screen_width / cols
    blockHeight = screen_height / rows
    blockWidth = 20
    blockHeight = 20
    currentCol = 0

    for col in maze:
        currentCol += 1
        currentRow = -1
        for row in col:
            currentRow += 1
            # This represents a block
            if row == 'X':
                block = Block(BLACK, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                walls.add(block)
            if row == '+':
                block = Block(GREEN, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                weals.add(block)
            if row == '-':
                block = Block(RED, blockWidth, blockHeight)
                block.rect.x = currentCol * blockWidth
                block.rect.y = currentRow * blockHeight
                woes.add(block)

            all_sprites_list.add(block)


done = False
maze = create_maze()
player = Player(maze, BLUE, 20, 20)
player.maze[1][1] = 'P'
createSpritesFromMazeList(player)
all_sprites_list.add(player)

clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveLeft()
            if event.key == pygame.K_RIGHT:
                player.moveRight()
            if event.key == pygame.K_DOWN:
                player.moveDown()
            if event.key == pygame.K_UP:
                # player.moveUp()
                player.basicAI()
    screen.fill(WHITE)

    weal_hit_list = pygame.sprite.spritecollide(player, weals, True)
    woe_hit_list = pygame.sprite.spritecollide(player, woes, True)

    for weal in weal_hit_list:
        score += 1
        print(score)

    for woe in woe_hit_list:
        score -= 10
        print(score)

    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
