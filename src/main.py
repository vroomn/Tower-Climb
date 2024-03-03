from jsonHandlers import *
from cell import *
from tilemap import *

import pygame
import pygame.gfxdraw

updateLocalJson()

class Button:

    def __init__(self, xPos: int, yPos: int, msg: str, callback: object, *args, width: int = 100, height: int = 20) -> None:
        self.rect = pygame.Rect(xPos, yPos, width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.fill((209, 118, 65))

        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.setText(msg)

        self.callback = callback
        self.args = list(args)
    
    # Returns true if the mouse is over the button (Can be used to check for click)
    def clickCheck(self, mousePos: tuple[int, int] = None) -> object:
        if mousePos == None:
            mousePos = pygame.mouse.get_pos() # Done in case of sequential checks of click where it being passed would be more efficient
        
        if mousePos[0] >= self.rect.x and mousePos[0] <= self.rect.x + self.rect.width:
            if mousePos[1] >= self.rect.y and mousePos[1] <= self.rect.y + self.rect.height:
                return self.callback(self.args)
        else:
            return None

    def setText(self, msg: str):
        self.text = self.font.render(msg, False, (255, 255, 255))
        self.surface.fill((209, 118, 65))
        self.surface.blit(self.text, self.text.get_rect())

    def draw(self, drawSurface: pygame.Surface):
        drawSurface.blit(self.surface, self.rect)

class Editor:
    def __init__(self) -> None:
        self.editingMode = False

        self.tilemap = Tilemap(6, 14, 0, CELLSIZE*2, 40)

        self.buttons: list[Button] = []
        stageKeys = list(jsonHandlers.stages.keys())
        for i in range(0, len(stageKeys)):
            self.buttons.append(Button(10, 10 + (i*30), f"Level {stageKeys[i][1]}", self.setTileMapLevel, i))

        self.buttons.append(Button(10, 10 + (len(self.buttons)*30), "New Stage", self.addTileMapLevel, None))
        self.deleteLevelButton = Button(260, 10, "Delete Level", self.deleteTilemapLevel, 0)

        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.text = self.font.render(f"Level 0", False, (255, 255, 255))

        self.calculateWindowWidth()

        self.selectedTileIdx = None
        self.selectedTextureIdx = None
        self.textureDeleteButton = Button(580, 64, f"Delete Texture {self.selectedTextureIdx}", self.deleteTexture, 0, width=140)

        self.addTexture = Button(740, 64, "New Texture", self.createTexture, 0)
    
    def render(self, drawSurface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(drawSurface)
        self.deleteLevelButton.draw(drawSurface)

        self.tilemap.draw(drawSurface)

        drawSurface.blit(self.text, pygame.Rect(160, 10, 100, 30))
        if self.selectedTileIdx != None:
            pygame.gfxdraw.rectangle(drawSurface, self.tilemap.cells[self.selectedTileIdx].baseRect, (255, 255, 255))

            for i in range(0, len(self.tilemap.cells[self.selectedTileIdx].textures)):
                drawSurface.blit(self.tilemap.cells[self.selectedTileIdx].textures[i], pygame.Rect((CELLSIZE*9) + (i*(CELLSIZE+10)), CELLSIZE*2, CELLSIZE, CELLSIZE))
            
            if self.selectedTextureIdx != None:
                pygame.gfxdraw.rectangle(drawSurface, pygame.Rect((CELLSIZE*9) + (self.selectedTextureIdx*(CELLSIZE+10)), CELLSIZE*2, CELLSIZE, CELLSIZE), (255, 255, 255))
                self.textureDeleteButton.draw(drawSurface)

                self.drawPossibleTextures(drawSurface)

            self.addTexture.draw(drawSurface)

    def possibleTextureClickcheck(self, mousePos: tuple[int, int]):
        mouseX, mouseY = mousePos
        possibleTextures = os.listdir("textures")
        for i in range(len(possibleTextures)):
            xPos = 576 + ((i*32) - int(i/8)*256)
            if mouseX >= xPos and mouseX <= xPos + 32:
                yPos = 200 + (int(i/8)*32)
                if mouseY >= yPos and mouseY <= yPos+32:
                    #print(f"Tile selected {i}, {possibleTextures[i]}")
                    tmpPosTexs = possibleTextures
                    #tmpPosTexs.reverse()
                    jsonHandlers.stages[f"L{self.deleteLevelButton.args[0]}"][self.selectedTileIdx]["ts"][self.selectedTextureIdx] = tmpPosTexs[i]
                    jsonRewrite()
                    self.tilemap = Tilemap(6, 14, self.addTexture.args[0], CELLSIZE*2, 40)

    def drawPossibleTextures(self, drawSurface: pygame.Surface):
        imgs = os.listdir("textures")
        colCalc = lambda x: int(x/8)
        for i in range(0, len(imgs)):
            drawSurface.blit(pygame.image.load(os.path.join("textures", imgs[i])), pygame.Rect(576 + ((i*32) - colCalc(i)*256), 200 + (colCalc(i)*32), 32, 32))

    def calculateWindowWidth(self):
        textureRows = int(len(os.listdir("textures"))/4)
        if len(os.listdir("textures"))%4 != 0:
            textureRows += 1

        # Minimum width
        if textureRows < 4:
            textureRows = 4
        
        self.editorCalcedWidth = (CELLSIZE* (10 + textureRows))

    def deleteTexture(self, *args):
        jsonHandlers.stages[f"L{self.deleteLevelButton.args[0]}"][self.selectedTileIdx]["ts"].pop(self.selectedTextureIdx)
        jsonRewrite()
        self.tilemap = Tilemap(6, 14, self.deleteLevelButton.args[0], CELLSIZE*2, 40)

    def createTexture(self, *args):
        jsonHandlers.stages[f"L{self.addTexture.args[0]}"][self.selectedTileIdx]["ts"].append("sampleTexture.jpeg")
        jsonRewrite()
        self.tilemap = Tilemap(6, 14, self.addTexture.args[0], CELLSIZE*2, 40)

    def clickCheck(self):
        mousePos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.clickCheck(mousePos)
        
        self.deleteLevelButton.clickCheck(mousePos)

        mouseX = mousePos[0]
        mouseY = mousePos[1]
        if mouseX >= CELLSIZE*2 and mouseX <= CELLSIZE*8:
            if mouseY >= 40:
                mouseX -= 2*CELLSIZE
                mouseY -= 40

                xOverlap = ((mouseX)-(mouseX%CELLSIZE))/CELLSIZE
                yOverlap = (mouseY-(mouseY%CELLSIZE))/CELLSIZE

                self.selectedTileIdx = int((xOverlap*14)+yOverlap)

        mouseX = mousePos[0]
        mouseY = mousePos[1]
        if self.selectedTileIdx != None:
            self.textureDeleteButton.clickCheck(mousePos)
            self.addTexture.clickCheck(mousePos)

            self.possibleTextureClickcheck(mousePos)

            for i in range(0, len(self.tilemap.cells[self.selectedTileIdx].textures)):
                if mouseX >= (CELLSIZE*9) + (i*(CELLSIZE+10)) and mouseX <= (CELLSIZE*9) + (i*(CELLSIZE+10)) + CELLSIZE:
                    if mouseY >= (CELLSIZE*2) and mouseY <= (CELLSIZE*3):
                        self.selectedTextureIdx = i
                        self.textureDeleteButton.setText(f"Delete Texture {i}")

    # Function takes *args due to being a callback
    def setTileMapLevel(self, *args) -> None:
        if args[0][0] != self.tilemap.level:
            self.tilemap = Tilemap(6, 14, args[0][0], CELLSIZE*2, 40)

            self.text = self.font.render(f"Level {args[0][0]}", False, (255, 255, 255))
            self.deleteLevelButton.args = args[0]
            self.addTexture.args = args[0]

            self.selectedTileIdx = None

    def addTileMapLevel(self, *args) -> None:
        self.buttons[-1].rect = self.buttons[-1].rect.move(0, 30)
        self.buttons.insert(len(self.buttons)-1, Button(10, 10 + (len(self.buttons)-1)*30, f"Level {len(self.buttons)-1}", self.setTileMapLevel, len(self.buttons)-1))
        Tilemap(6, 14, len(jsonHandlers.stages.keys()), CELLSIZE*2, 40)
        jsonRewrite()

    def deleteTilemapLevel(self, *args) -> None:
        level = args[0][0]
        self.buttons.pop(level)

        if level != (len(jsonHandlers.stages.keys())-1):
            for i in range(level, len(jsonHandlers.stages.keys())-1):
                jsonHandlers.stages[f"L{i}"] = jsonHandlers.stages[f"L{i+1}"]
        
        jsonHandlers.stages.pop(f"L{len(jsonHandlers.stages.keys())-1}")
        jsonRewrite()

        if level == 0:
            self.tilemap = Tilemap(6, 14, level, CELLSIZE*2, 40)
            self.setText(f"Level {level}")
        else:
            self.tilemap = Tilemap(6, 14, level-1, CELLSIZE*2, 40)
            self.setText(f"Level {level-1}")

        for i in range(level, len(self.buttons)-1):
            self.buttons[i].rect = self.buttons[i].rect.move(0, -30)
            self.buttons[i].args[0] = i
            self.buttons[i].setText(f"Level {i}")

        self.buttons[-1].rect = self.buttons[-1].rect.move(0, -30)

    def setText(self, msg: str):
        self.text = self.font.render(msg, False, (255, 255, 255))

    def toggle(self) -> pygame.Surface:
        standardDisplaySize = ((CELLSIZE*2) * 8, CELLSIZE * 14)
        editorDisplaySize = (self.editorCalcedWidth, (CELLSIZE * 14) + 40)
        newScreen = None

        if self.editingMode:
            newScreen = pygame.display.set_mode(standardDisplaySize)
            self.editingMode = False
            print("Exiting editing mode")
        else:
            newScreen = pygame.display.set_mode(editorDisplaySize)
            self.editingMode = True
            print("Enterting editing mode")

        return newScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()

    levelOne = Tilemap(6, 14, 0)

    editor = Editor()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and editor.editingMode:
                editor.clickCheck()

            if event.type == pygame.KEYDOWN:
                if editor.editingMode and event.key == pygame.K_r:
                    editor.tilemap.hotReload()
                elif event.key == pygame.K_ESCAPE and editor.selectedTileIdx != None:
                    editor.selectedTileIdx = None
                    editor.selectedTextureIdx = None

                elif event.key == pygame.K_r:
                    levelOne.hotReload()
                elif event.key == pygame.K_e:
                    screen = editor.toggle()

        screen.fill((145, 194, 158))

        if not editor.editingMode:
            levelOne.draw(screen)
        else:
            editor.render(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()