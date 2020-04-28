import sys, pygame
import numpy as np
pygame.init()

size = width, height = 1800, 960
speed = np.array([4., 4.])
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    speed = speed - np.array([0,-0.1])
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]
    elif ballrect.bottom > height:
        speed[1] = -speed[1]
        ballrect.bottom = height

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
