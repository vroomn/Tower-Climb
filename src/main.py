import pygame
import pygame.gfxdraw
from jsonHandlers import *
from cell import *

class Tilemap:
    def __init__(self, width: int, height: int, level: int, xPadding: int = 0, yPadding :int = 0, cellSize: int = CELLSIZE) -> None:
        self.width = width
        self.height = height
        self.xPadding = xPadding
        self.yPadding = yPadding

        self.cellSize = cellSize
        self.level = level

        if len(jsonHandlers.stages) <= self.level:
            jsonHandlers.stages[f"L{self.level}"] = []
            jsonRewrite()

        #TODO: Complete refactor to custom json file read/write system, json file is unreasonably long in terms of lines
        self.cells: Cell = []
        idxIter = 0
        for row in range(0, self.width):
            for collumn in range(0, self.height):
                self.cells.append(Cell(row, collumn, self.xPadding, self.yPadding, idxIter, self.level))
                idxIter += 1

    def hotReload(self):
        updateLocalJson()
        for cell in self.cells:
            cell.hotReload()

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

    levelOne = Tilemap(6, 14, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Up Key Pressed")
                elif event.key == pygame.K_r:
                    levelOne.hotReload()

        screen.fill((145, 194, 158))

        levelOne.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()