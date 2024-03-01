import pygame
import pygame.gfxdraw
from jsonHandlers import *
from cell import *
from tilemap import *

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
    
    def render(self, drawSurface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(drawSurface)
        self.deleteLevelButton.draw(drawSurface)

        self.tilemap.draw(drawSurface)

        drawSurface.blit(self.text, pygame.Rect(160, 10, 100, 30))

    def clickCheck(self):
        for button in self.buttons:
            button.clickCheck()
        
        self.deleteLevelButton.clickCheck()

    # Function takes *args due to being a callback
    def setTileMapLevel(self, *args) -> None:
        self.tilemap = Tilemap(6, 14, args[0][0], CELLSIZE*2, 40)

        self.text = self.font.render(f"Level {args[0][0]}", False, (255, 255, 255))
        self.deleteLevelButton.args = args[0]

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
        editorDisplaySize = (CELLSIZE*8, (CELLSIZE * 14) + 40)
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
                if editor.editingMode:
                    editor.tilemap.hotReload()

                if event.key == pygame.K_r:
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