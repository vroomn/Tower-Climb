import jsonHandlers
from cell import *
import pygame

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
            jsonHandlers.jsonRewrite()

        #TODO: Complete refactor to custom json file read/write system, json file is unreasonably long in terms of lines
        self.cells: list[Cell] = []
        idxIter = 0
        for row in range(0, self.width):
            for collumn in range(0, self.height):
                self.cells.append(Cell(row, collumn, self.xPadding, self.yPadding, idxIter, self.level))
                idxIter += 1

    def hotReload(self):
        jsonHandlers.updateLocalJson()
        for cell in self.cells:
            cell.hotReload()

    def draw(self, screen):
        for i in self.cells:
            i.draw(screen)

    def wireframeDraw(self, screen: pygame.Surface) -> None:
        for i in self.cells:
            i.wireframeDraw(screen)
        pygame.gfxdraw.rectangle(screen, pygame.Rect(self.xPadding, self.yPadding, self.width * self.cellSize, self.height * self.cellSize), (255, 255, 255))