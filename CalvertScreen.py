import pygame
import time
class Screen:
    def __init__(self,width, height, drawnObjectGroupsInOrderOfDrawing):
        self.drawnObjectGroups= drawnObjectGroupsInOrderOfDrawing
        self.screen = pygame.display.set_mode([width,height])
        self.screenRate = .5
        self.lastUpdated = time.clock()



    def update(self):
        if time.clock()-self.lastUpdated > self.screenRate:
            for group in self.drawnObjectGroups:
                group.draw(self.screen)
                for item in group:
                    item.update()
            self.lastUpdated = time.clock()

        pygame.display.flip()

