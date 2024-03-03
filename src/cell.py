import os
import pygame
import jsonHandlers

CELLSIZE = 64

class Cell:
    def __init__(self, posX: int, posY: int, xPadding: int, yPadding: int, idx: int, level: int, cellSize: int = CELLSIZE) -> None:
        self.posX = posX
        self.posY = posY
        self.cellSize = cellSize
        self.idx = idx
        self.level = level

        if len(jsonHandlers.stages[f"L{level}"]) <= idx:
            jsonHandlers.stages[f"L{level}"].append({"ts": ["sampleTexture.jpeg"], "cS": None, "mf": []})
            jsonHandlers.jsonRewrite()

        self.textures: list[pygame.Surface] = []
        self.getTextures()

        self.baseRect = pygame.Rect((posX * cellSize)+xPadding, (posY * cellSize)+yPadding, cellSize, cellSize)
        if jsonHandlers.stages[f"L{level}"][self.idx]["cS"] != None:
            # switch statement or the sort that will set the proper collision rect for the object
            pass
        else:
            self.collisonRect = None
        
    # Automatically formatted from furthest background to the foreground objects
    def getTextures(self) -> None:
        for filename in jsonHandlers.stages[f"L{self.level}"][self.idx]["ts"]:
            texture = pygame.image.load(os.path.join("textures", filename))
            texture = pygame.transform.scale(texture, (CELLSIZE, CELLSIZE))
            self.textures.append(texture)

    def hotReload(self):
        self.getTextures()

    def draw(self, drawSurface: pygame.Surface) -> None:
        for texture in self.textures:
            drawSurface.blit(texture, self.baseRect)

    def wireframeDraw(self, drawSurface: pygame.Surface) -> None:
        pygame.gfxdraw.rectangle(drawSurface, self.baseRect, (29, 173, 77))