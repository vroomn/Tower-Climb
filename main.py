import pygame
import pygame.gfxdraw
import os
import json

CELLSIZE = 64

class Cell:
    def __init__(self, cellSize, posX, posY, xPadding, yPadding, idx: int, level: int) -> None:
        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize
        self.idx = idx
        self.level = level

        if len(stages[f"L{level}"]) <= idx:
            stages[f"L{level}"].append({"ts": ["sampleTexture.jpeg"], "cS": None, "mf": []})
            jsonRewrite()

        self.textures = []
        self.getTextures()

        self.baseRect = pygame.Rect((posX * cellSize)+xPadding, (posY * cellSize)+yPadding, cellSize, cellSize)
        if stages[f"L{level}"][self.idx]["cS"] != None:
            # switch statement or the sort that will set the proper collision rect for the object
            pass
        else:
            self.collisonRect = None
        
    # Automatically formatted from furthest background to the foreground objects
    def getTextures(self) -> None:
        for filename in stages[f"L{self.level}"][self.idx]["ts"]:
            texture = pygame.image.load(os.path.join("textures", filename))
            pygame.transform.scale(texture, (CELLSIZE, CELLSIZE))
            self.textures.append(texture)

    def hotReload(self):
        self.getTextures()

    def draw(self, drawSurface: pygame.Surface) -> None:
        for texture in self.textures:
            drawSurface.blit(texture, self.baseRect)

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

with open("testLevels.json") as file:
    stages = json.load(file)

def jsonRewrite(filename: str = "testLevels.json"):
    with open(filename, "w") as file:
        json.dump(stages, file, indent=4)
 
def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()
    running = True
    
    """stageOne = Tilemap(6, int(screen.get_height() / CELLSIZE), CELLSIZE, 0, 0, stages["l1"])
    if stageOne.editedLevel == True:
        stages["l1"] = stageOne.stageData
        with open("levels.json", "w") as file:
            json.dump(stages, file, indent = 4)"""
    
    testCell = Cell(64, 0, 0, 0, 0, 1, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Up Key Pressed")
                elif event.key == pygame.K_r:
                    testCell.hotReload()

        screen.fill((145, 194, 158))

        testCell.draw(screen)

        #stageOne.draw(screen)
        #stageOne.wireframeDraw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()