import time
import pygame
class Game:
    def __init__(self, screen, loop, initializeGame):
        self.screen = screen
        self.loop = loop
        self.initializeGame = initializeGame
        self.done = False

    def run(self):
        self.initializeGame()
        lastUpdated = time.clock()
        frameRate = .07
        while not self.done:
            if time.clock() - lastUpdated > frameRate:
                pygame.event.get()
                self.loop()
            self.screen.update()




