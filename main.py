import pygame
import pygame.gfxdraw
import os

CELLSIZE = 64

class Cell:
    def __init__(self, cellSize, posX, posY, xPadding, yPadding) -> None:
        self.image = pygame.Surface((posX * cellSize, posY * cellSize))
        self.rect = pygame.Rect((posX * cellSize)+xPadding, (posY * cellSize)+yPadding, cellSize, cellSize)

        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize

    def attachImg(self, filename: str) -> None:
        self.image = pygame.image.load(os.path.join("Textures", filename))
        self.image = pygame.transform.scale(self.image, (64, 64))

    def draw(self, drawSurface: pygame.Surface) -> None:
        drawSurface.blit(self.image, pygame.Rect(0, 0, 64, 64))

    def wireframeDraw(self, drawSurface: pygame.Surface) -> None:
        pygame.gfxdraw.rectangle(drawSurface, self.rect, (29, 173, 77))

class Tilemap:
    def __init__(self, width, height, cellSize, xPadding, yPadding) -> None:
        self.width = width
        self.height = height

        self.xPadding = xPadding
        self.yPadding = yPadding

        self.cellSize = cellSize

        self.cells: Cell = []
        for row in range(0, self.width):
            for collumn in range(0, self.height):
                self.cells.append(Cell(cellSize, row, collumn, xPadding, yPadding))

    def wireframeDraw(self, screen: pygame.Surface) -> None:
        for i in self.cells:
            i.wireframeDraw(screen)
        pygame.gfxdraw.rectangle(screen, pygame.Rect(self.xPadding, self.yPadding, self.width * self.cellSize, self.height * self.cellSize), (255, 255, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()
    running = True

    stageOne = Tilemap(6, int(screen.get_height() / CELLSIZE), CELLSIZE, 0, 0)
    stageTwo = Tilemap(6, int(screen.get_height() / CELLSIZE), CELLSIZE, screen.get_width()-(CELLSIZE*6), 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key == pygame.K_UP:
                    print("Up Key Pressed")

        screen.fill((145, 194, 158))

        stageOne.wireframeDraw(screen)
        stageTwo.wireframeDraw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()