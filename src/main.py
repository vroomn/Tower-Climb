from jsonHandlers import *
from tilemap import *
from editor import Editor
from player import *

import pygame
import pygame.gfxdraw

updateLocalJson()

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()
    levelOne = Tilemap(6, 14, 0)

    editor = Editor()

    playerOne = Player((100, screen.get_height()/2), (0, 6*CELLSIZE), "blankSprite.jpeg", InputTypes.WAD)

    dt: float = 0
    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
            
                case pygame.MOUSEBUTTONDOWN:
                    if editor.editingMode:
                        editor.clickCheck()
                
                case pygame.KEYDOWN:
                    if editor.editingMode and event.key == pygame.K_r:
                        editor.tilemap.hotReload()
                    elif event.key == pygame.K_ESCAPE and editor.selectedTileIdx != None:
                        editor.selectedTileIdx = None
                        editor.selectedTextureIdx = None

                    elif event.key == pygame.K_r:
                        levelOne.hotReload()
                    elif event.key == pygame.K_e:
                        screen = editor.toggle()
                        levelOne.hotReload()
                        
                    playerOne.control(event.key, InputTypes.KEYDOWN, dt)

                case pygame.KEYUP:
                    playerOne.control(event.key, InputTypes.KEYUP, dt)

        screen.fill((145, 194, 158))

        if not editor.editingMode:
            levelOne.draw(screen)

            playerOne.movementUpdate(dt)

            playerOne.draw(screen)

        else:
            editor.render(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000
    pygame.quit()

if __name__ == "__main__":
    main()