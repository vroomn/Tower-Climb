import pygame
import pygame.gfxdraw
import os
import json

CELLSIZE = 64

class Cell:
    def __init__(self, cellSize, posX, posY, xPadding, yPadding, idx, stageData) -> None:
        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize
        self.idx = idx

        self.stageData = stageData

        self.attachImg(self.stageData["ts"][0])
        self.rect = pygame.Rect((posX * cellSize)+xPadding, (posY * cellSize)+yPadding, cellSize, cellSize)

    def attachImg(self, filename: str) -> None:
        self.image = pygame.image.load(os.path.join("Textures", filename))
        self.image = pygame.transform.scale(self.image, (64, 64))

    def hotReload(self):
        self.attachImg(self.stageData["ts"][0])

    def draw(self, drawSurface: pygame.Surface) -> None:
        drawSurface.blit(self.image, self.rect)

    def wireframeDraw(self, drawSurface: pygame.Surface) -> None:
        pygame.gfxdraw.rectangle(drawSurface, self.rect, (29, 173, 77))

class Tilemap:
    def __init__(self, width, height, cellSize, xPadding, yPadding, stage) -> None:
        self.width = width
        self.height = height

        self.xPadding = xPadding
        self.yPadding = yPadding

        self.cellSize = cellSize

        self.stageData = stage

        self.cells: Cell = []

        self.editedLevel = False
        idxIter = 0
        for row in range(0, self.width):
            for collumn in range(0, self.height):
                passedCellData = {"idx": idxIter, "ts": ["sampleTexture.jpeg"], "cS": None, "mf": []}
                idxPresent = False
                for i in stage:
                    if i["idx"] == idxIter:
                        passedCellData = i
                        idxPresent = True

                if not idxPresent:
                    stage.append(passedCellData)
                    self.editedLevel = True

                self.cells.append(Cell(cellSize, row, collumn, xPadding, yPadding, idxIter, passedCellData))
                idxIter += 1

    def hotReload(self, stageData):
        self.stageData = stageData
        iterator = 0
        for i in self.cells:
            i.stageData = self.stageData[iterator]
            i.hotReload()
            iterator += 1

    def draw(self, screen):
        for i in self.cells:
            i.draw(screen)

    def wireframeDraw(self, screen: pygame.Surface) -> None:
        for i in self.cells:
            i.wireframeDraw(screen)
        pygame.gfxdraw.rectangle(screen, pygame.Rect(self.xPadding, self.yPadding, self.width * self.cellSize, self.height * self.cellSize), (255, 255, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()
    running = True

    with open("levels.json") as file:
        stages = json.load(file)
    
    stageOne = Tilemap(6, int(screen.get_height() / CELLSIZE), CELLSIZE, 0, 0, stages["l1"])
    if stageOne.editedLevel == True:
        stages["l1"] = stageOne.stageData
        with open("levels.json", "w") as file:
            json.dump(stages, file, indent = 4)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Up Key Pressed")
                elif event.key == pygame.K_r:
                    with open("levels.json") as file:
                        stages = json.load(file)
                    stageOne.hotReload(stages["l1"])
                    print("R pressed")

        screen.fill((145, 194, 158))

        stageOne.draw(screen)
        stageOne.wireframeDraw(screen)
        #stageTwo.wireframeDraw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()