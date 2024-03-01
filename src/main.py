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
        self.text = self.font.render(msg, False, (255, 255, 255))
        self.surface.blit(self.text, self.text.get_rect())

        self.callback = callback
        self.args = args
    
    # Returns true if the mouse is over the button (Can be used to check for click)
    def clickCheck(self, mousePos: tuple[int, int] = None) -> object:
        if mousePos == None:
            mousePos = pygame.mouse.get_pos() # Done in case of sequential checks of click where it being passed would be more efficient
        
        if mousePos[0] >= self.rect.x and mousePos[0] <= self.rect.x + self.rect.width:
            if mousePos[1] >= self.rect.y and mousePos[1] <= self.rect.y + self.rect.height:
                return self.callback(self.args)
        else:
            return None

    def draw(self, drawSurface: pygame.Surface):
        drawSurface.blit(self.surface, self.rect)

class Editor:
    def __init__(self) -> None:
        self.editingMode = False

        self.tilemap = Tilemap(6, 14, 0, CELLSIZE*2)

        self.buttons = []
        stageKeys = list(jsonHandlers.stages.keys())
        for i in range(0, len(stageKeys)):
            self.buttons.append(Button(10, 10 + (i*30), f"{stageKeys[i][0]}evel {stageKeys[i][1]}", self.setTileMapLevel, i))
    
    def render(self, drawSurface: pygame.Surface) -> None:
        for button in self.buttons:
            button.draw(drawSurface)

        self.tilemap.draw(drawSurface)

    # Function takes *args due to being a callback
    def setTileMapLevel(self, *args) -> None:
        self.tilemap = Tilemap(6, 14, args[0][0], CELLSIZE*2)

    def clickCheck(self):
        for button in self.buttons:
            button.clickCheck()

    def toggle(self) -> pygame.Surface:
        standardDisplaySize = ((CELLSIZE*2) * 8, CELLSIZE * 14)
        editorDisplaySize = (CELLSIZE*8, CELLSIZE * 14)
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