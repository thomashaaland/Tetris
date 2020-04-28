# Tetris with python 3.6.7

import math, sys, pygame
import numpy as np
import time
import random

pygame.init()
pygame.font.init()

# Text preparation
pygame.display.set_caption('Tetris')
tetrisFont = pygame.font.SysFont('freesansbold.ttf', 32)
tetrisFontSmall = pygame.font.SysFont('freesansbold.ttf', 24)

color = {'Black':[0,0,0],
         'White':[255,255,255],
         'Red':[255,0,0],
         'Pink':[255,125,125],
         'Green':[0,255,0],
         'lGreen':[125,255,125],
         'Blue':[0,0,255],
         'lBlue':[125,125,255],
         'Purple':[125,0,125]}

cCode = {0: 'Black',
         1: 'White',
         2: 'Red',
         3: 'Pink',
         4: 'Green',
         5: 'lGreen',
         6: 'Blue',
         7: 'lBlue',
         8: 'Purple'}

class Cube(object):
    def __init__(self, pos, color=[150,150,150]):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        x = self.pos[0]
        y = self.pos[1]
        pygame.draw.rect(surface, [self.color[0]*1/3, self.color[1]*1/3, self.color[2]*1/3], [x, y, 20, 20])
        pygame.draw.rect(surface, [self.color[0]*1/2, self.color[1]*1/2, self.color[2]*1/2], [x, y, 18, 18])
        pygame.draw.rect(surface, [self.color[0]*2/3, self.color[1]*2/3, self.color[2]*2/3], [x, y, 15, 15])
        pygame.draw.rect(surface, [self.color[0], self.color[1], self.color[2]], [x+1, y+1, 5, 5])

class Tetramino(object):
    def __init__(self, size, pos = [100, -20]):
        self.size = size
        self.width_max = size[0]
        self.width_min = 0
        self.height = size[1]
        self.pos = pos
        self.increment = 20
        self.tetramino_select = random.randint(0,6)
        self.rotate = 0
        self.rotated_last_cycle = False
        # Design the tetraminos boxwize
        
    # Function for dealing with the tetraminos themselves
    def tetraminos(self):
        rotate = self.rotate
        # The matrix shows the relative position of each block making up a tetramino
        tetramino = []
        tetraminos = [
            [[0,0,0,0],
             [0,1,1,0],
             [0,1,1,0],
             [0,0,0,0]],

            [[0,1,0,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,1,0,0]],

            [[0,0,0],
             [1,1,1],
             [0,1,0]],

            [[0,0,0],
             [1,1,0],
             [0,1,1]],

            [[0,0,0],
             [0,1,1],
             [1,1,0]],

            [[0,1,1],
             [0,1,0],
             [0,1,0]],

            [[1,1,0],
             [0,1,0],
             [0,1,0]]
        ]

        # When rotating: x_dif, y_dif = 0 for rot = 0, 1
        # x_dif = -1 for rot = 2
        # y_dif = -1 for rot = 3

        # Using the matrix to draw the tetramino position 0,0 is leftmost corner
        # dims:
        i_len = len(tetraminos[self.tetramino_select][0])-1
        j_len = len(tetraminos[self.tetramino_select])-1
        self.sColor = color[cCode[self.tetramino_select+2]]
        if rotate == 0:
            for i, row in enumerate(tetraminos[self.tetramino_select]):
                for j, element in enumerate(row):
                    if element == 1:
                        tetramino.append(Cube([self.pos[0] + j*self.increment,
                                               self.pos[1] + i*self.increment], self.sColor))

        if rotate == 1:
            for i, row in enumerate(tetraminos[self.tetramino_select]):
                for j, element in enumerate(row):
                    if element == 1:
                        tetramino.append(Cube([self.pos[0] + i*self.increment,
                                               self.pos[1] + (j_len-j)*self.increment], self.sColor))

        if rotate == 2:
            for i, row in enumerate(tetraminos[self.tetramino_select]):
                for j, element in enumerate(row):
                    if element == 1:
                        tetramino.append(Cube([self.pos[0] + (j_len-j)*self.increment,
                                               self.pos[1] + (i_len-i)*self.increment], self.sColor))

        if rotate == 3:
            for i, row in enumerate(tetraminos[self.tetramino_select]):
                for j, element in enumerate(row):
                    if element == 1:
                        tetramino.append(Cube([self.pos[0] + (i_len-i)*self.increment,
                                               self.pos[1] + j*self.increment], self.sColor))
        """
        [[0, 1, 2, 3],
         [4, 5, 6, 7],
         [8, 9,10,11],
         [12,13,14,15]]
        
        [[12, 8,4,0],
         [13, 9,5,1],
         [14,10,6,2],
         [15,11,7,3]]

        [[15, 14, 13, 12],
         [11, 10,  9,  8],
         [ 7,  6,  5,  4],
         [ 3,  2,  1,  0]]

        [[ 3, 7, 11, 15],
         [ 2, 6, 10, 14],
         [ 1, 5,  9, 13],
         [ 0, 4,  8, 12]]
        """
        return tetramino

    def draw(self, surface):
        self.tetramino = self.tetraminos()
        for cube in self.tetramino:
                     cube.draw(surface)
    
    def update(self, heap, boundary, y_dif=0):
        increment = self.increment
        x_dif = 0
        # Need to move down 1 increment at each time % time_increment
        # and free movement along x and y down
        
        # This happens when keys are pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            has_rotated = False
            has_pressed_space = False
            
            for key in keys:
                if keys[pygame.K_LEFT]:
                    x_dif = -1
                elif keys[pygame.K_RIGHT]:
                    x_dif = 1
                elif keys[pygame.K_DOWN]:
                    y_dif = 1
                elif keys[pygame.K_UP]:
                    has_rotated = True
                elif keys[pygame.K_SPACE]:
                    has_pressed_space = True
                elif keys[pygame.K_ESCAPE]:
                    exit()

            if has_rotated == True:
                self.rotate += 1
                if self.rotate == 4: self.rotate = 0
                self.tetramino = self.tetraminos()
                for cube in self.tetramino:
                    if self.collision(heap, boundary, cube.pos) == True:
                        self.rotate -= 1
                        if self.rotate == -1: self.rotate = 3
                        self.tetramino = self.tetraminos()
                        break

            space_dif = 0
            while has_pressed_space:
                space_dif += 1
                for cube in self.tetramino:
                    if self.collision(heap, boundary,
                                      [cube.pos[0], cube.pos[1] + space_dif * increment]) == True:
                        space_dif -= 1
                        has_pressed_space = False
                        y_dif = space_dif
                        break
                
            if x_dif != 0:
                for cube in self.tetramino:
                    if self.collision(heap, boundary,
                                      [cube.pos[0] + x_dif * increment, cube.pos[1]]) == True:
                        x_dif = 0
                        break

            if y_dif != 0:
                for cube in self.tetramino:
                    if self.collision(heap, boundary,
                                      [cube.pos[0], cube.pos[1] + y_dif * increment]) == True:
                        y_dif = 0
                        break
                        
        self.pos = [self.pos[0] + x_dif * self.increment,
                    self.pos[1] + y_dif * self.increment]


        # Check each tick to see if the collision is immenent
        if y_dif != 0:
            for cube in self.tetramino:
                if self.collision(heap, boundary,
                                  [cube.pos[0], cube.pos[1] + self.increment]) == True:
                    for block in self.tetramino:
                        heap.addBlock([block.pos[0], block.pos[1]], self.sColor)
                    self.__init__(self.size)
                    break
#            self.pos = [self.pos[0], self.pos[1] + self.increment]

    # Need to make collision method, destroys this object,
    # initiates a new one and adds blocks to heap object
    def collision(self, heap, boundary, pos):
        increment = self.increment
        collision = False
        
        for block in boundary.blocks:
            if block.pos == pos:
                collision = True
                
        for block in heap.blocks:
            if block.pos == pos:
                collision = True
                
        return collision

    # Move all collision processing to collision method, call move after collision
    # feed collision info to move function if prudent
    # Collision function need to check the boundary as well as the heap in the same manner
    # In the move function, call the collision method to inquire about the square about
    # to move into, if empty move, else decide what to do based on move direction:
    # along x axis, refuse move. Along y axis, create new tetramino and add to heap
            
class Boundary(object):
    def __init__(self, size, color=(150,150,150)):
        self.increment = 20
        self.num_bottom = size[0] // self.increment
        self.num_height = size[1] // self.increment
        self.size = size
        self.blocks = []
        for i in range(0, self.num_height):
            self.blocks.append(Cube([0, self.increment*i]))
            self.blocks.append(Cube([self.size[0]-self.increment, self.increment*i]))
        for j in range(0, self.num_bottom-2):
            self.blocks.append(Cube([self.increment*(j+1), self.size[1]-self.increment]))

    def draw(self, surface):
        # make the boundary
        for block in self.blocks:
            block.draw(surface)

# The heap is the buildup of debris at the bottom
class Heap(object):
    def __init__(self, size):
        self.blocks = []
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.increment = 20
        self.num_hlines = (self.height // self.increment) - 1
        self.num_vlines = (self.width // self.increment) - 2
        
        
    # method for adding blocks
    def addBlock(self, pos, sColor):
        self.blocks.append(Cube(pos, sColor))
    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    # method for removing full bottom line
    def clearBottomLine(self,score):
        for line in range(0, self.num_hlines):
            counter = 0
            for i in range(len(self.blocks)):
                #print(self.blocks[i].pos)
                if self.blocks[i].pos[1] == line * self.increment:
                    counter += 1
            if counter == self.num_vlines:
                score += self.num_vlines
                k = 0
                for j in range(len(self.blocks)):
                    if self.blocks[k].pos[1] == line * self.increment:
                        self.blocks.remove(self.blocks[k])
                    else: k += 1
                for block in self.blocks:
                    if block.pos[1] < line * self.increment:
                        block.pos[1] += self.increment
        return score
    # Loose method
    def checkIfLoose(self, score, level):
        loose = False
        for block in self.blocks:
            if block.pos[1] == 0:
                loose = True
                break
        if loose == True:
            looseScreen(score, level)

def menu():
    size = width, height = [260, 480]
    menu_size = 120
    
    # Text preparation for ingame
    menuB = True
    mainB = False
    highscoreB = False
    while menuB:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.time.delay(100)
        # Game preparation
        screen = pygame.display.set_mode([size[0] + menu_size, size[1]])
        screen.fill(color['Black'])

        textFont(screen, 'Tetris', color['White'], [width // 2, 100])
        textFontSmall(screen, 'Press Enter to Start', color['White'], [width // 3, 150])
        textFontSmall(screen, 'Press ESC to QUIT', color['White'], [width // 3, 180])
        textFontSmall(screen, 'Press SPACE to view HighScore', color['White'], [width // 3, 210]) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_RETURN]:
                    menuB = False
                    mainB = True
                elif keys[pygame.K_ESCAPE]:
                    exit()
                elif keys[pygame.K_SPACE]:
                    menuB = False
                    highscoreB = True

        pygame.display.update()
        pygame.display.flip()

    if mainB == True:
        main()
    if highscoreB == True:
        highscore()
        
def highscore():
    highscoreB = True
    menuB = False
    size = width, height = [260, 480]
    menu_size = 120
    highscoreFile = open('highscores.md')
    scoreLevel = []
    for line in highscoreFile:
        scoreLevel.append(eval(line.split()[0]))
    highscoreFile.close()
    scoreLevel.sort()
    scoreLevel.reverse()
    score = scoreLevel[0:10]
    
    while highscoreB:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.time.delay(100)
        # Game preparation
        screen = pygame.display.set_mode([size[0] + menu_size, size[1]])
        screen.fill(color['Black'])

        textFont(screen, 'Tetris', color['White'], [width // 2, 70])
        textFontSmall(screen, 'Highscore:', color['White'], [width // 3, 100])
        textFontSmall(screen, 'Press SPACE to return to menu', color['White'], [width // 3, 130])
        for i in range(0,len(score)):
            textFontSmall(screen, '{}: {}'.format(i+1, score[i]), color['White'], [width // 3, 160 + i*30])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_SPACE]:
                    highscoreB = False
                    menuB = True

        pygame.display.update()
        pygame.display.flip()

    if menuB == True:
        menu()

    
def looseScreen(score, level):

    loosescreenB = True
    menuB = False
    size = width, height = [260, 480]
    menu_size = 120
    
    while loosescreenB:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.time.delay(100)
        # Game preparation
        screen = pygame.display.set_mode([size[0] + menu_size, size[1]])
        screen.fill(color['Black'])

        textFont(screen, 'Tetris', color['White'], [width // 2, 70])
        textFont(screen, 'You Lost!', color['White'], [width // 3, 100])

        textFont(screen, 'Your score: {}'.format(score), color['White'], [width // 3, 130])
        """
        if name_typed == True:
            textFontsmall(screen, 'Type your name: ', color['White'], [width // 3 , 160])
        else:
            textFontsmall(screen, '{}'.format(name), color['White'], [width // 3 , 160])
        """
        textFontSmall(screen, 'Press SPACE to return to menu', color['White'], [width // 3, 220])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_SPACE]:
                    loosescreenB = False
                    menuB = True

        pygame.display.update()
        pygame.display.flip()

    if menuB == True:
        filename = './highscores.md'
        filehighscore = open(filename, 'a+')
        filehighscore.write('{} {}\n'.format(level, score))
        filehighscore.close()
        menu()
    

def textFont(screen, string, color, pos):
    textSurface = tetrisFont.render(string, False, color)
    screen.blit(textSurface, pos)

def textFontSmall(screen, string, color, pos):
    textSurface = tetrisFontSmall.render(string, False, color)
    screen.blit(textSurface, pos)
    
def main():
    
    size = width, height = [260, 480]
    menu_size = 120

    # Game preparation
    screen = pygame.display.set_mode([size[0] + menu_size, size[1]])
    
    ######################
    # MENU
    ######################

    #menu()
    
    player = Tetramino(size)
    heap = Heap(size)
    wall = Boundary(size)

    clock = pygame.time.Clock()
    ticker = 0
    score = 0
    level = 0
    
    # Time keeping
    start = time.time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        # Make a proper time ticking even to send to *.move(time)
        pygame.time.delay(10)
        ticker += 1

        
        screen.fill(color['Black'])
        wall.draw(screen)
        
        heap.draw(screen)

        
        level_ticker = 40 - level
        if ticker % level_ticker == 0:
            player.update(heap=heap, boundary=wall, y_dif=1)
        else: player.update(heap=heap, boundary=wall)

        if ticker % 2000 == 0: level += 1
        
        player.draw(screen)
        score = heap.clearBottomLine(score)
        heap.checkIfLoose(score, level)

        ####
        # Making the score board
        ###

        textFont(screen, 'Tetris', color['White'], [width + 20, 30])
        
        # Level
        textFontSmall(screen, 'Level: ', color['White'], [width + 20, 60])
        textFont(screen, '{}'.format(level), color['White'], [width + 20, 90])
        
        # Time listing:

        textFontSmall(screen, 'Time: ', color['White'], [width + 20, 120])

        now = time.time()
        time_spent = now - start
        time_spent_miliseconds = (time_spent // (1/60)) % 60
        time_spent_seconds = (time_spent % 60)//1
        time_spent_minutes = time_spent // 60
        
        timeList = '{:2.0f}:{:2.0f}:{:2.0f}'.format(time_spent_minutes,time_spent_seconds,time_spent_miliseconds)
        textFont(screen, timeList, color['White'], [width +20, 150])

        # Score
        textFontSmall(screen, 'Score: ', color['White'], [width + 20, 180])

        if ticker % 1000 == 0:
            score += 1

        scoreList = '{}'.format(score)
        textFont(screen, scoreList, color['White'], [width + 20, 210])
        
        
        pygame.display.update()
        pygame.display.flip()

menu()
#main()
