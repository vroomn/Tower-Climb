import pygame
import pygame.gfxdraw
from jsonHandlers import *
from cell import *

class Tilemap:
    def __init__(self, width, height, cellSize, xPadding, yPadding) -> None:
        self.width = width
        self.height = height

        self.xPadding = xPadding
        self.yPadding = yPadding

        self.cellSize = cellSize

        self.cells: Cell = []

        #TODO: Complete refactor to custom json loading system, this is a mess

        self.editedLevel = False
        idxIter = 0
        for row in range(0, self.width):
            for collumn in range(0, self.height):
                #{"idx": idxIter, "ts": ["sampleTexture.jpeg"], "cS": None, "mf": []}
                idxIter += 1

    def hotReload(self, stageData):
        pass

    def draw(self, screen):
        for i in self.cells:
            i.draw(screen)

    def wireframeDraw(self, screen: pygame.Surface) -> None:
        for i in self.cells:
            i.wireframeDraw(screen)
        pygame.gfxdraw.rectangle(screen, pygame.Rect(self.xPadding, self.yPadding, self.width * self.cellSize, self.height * self.cellSize), (255, 255, 255))
 
updateLocalJson()

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()
    running = True
    
    testCell = Cell(64, 0, 0, 0, 0, 0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Up Key Pressed")
                elif event.key == pygame.K_r:
                    pass

        screen.fill((145, 194, 158))

        testCell.wireframeDraw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()