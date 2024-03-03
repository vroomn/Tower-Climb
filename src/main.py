from jsonHandlers import *
from tilemap import *
from editor import Editor
from player import *
from collison import *

import pygame
import pygame.gfxdraw

updateLocalJson()

def main():
    pygame.init()
    screen = pygame.display.set_mode(((CELLSIZE*2) * 8, CELLSIZE * 14))
    clock = pygame.time.Clock()

    editor = Editor()

    playerOne = Player((CELLSIZE*2+32, screen.get_height()/2), (0, 6*CELLSIZE), "blankSprite.jpeg", InputTypes.WAD)
    playerTwo = Player((800, screen.get_height()/2), (CELLSIZE*10, screen.get_width()), "blankSprite.jpeg", InputTypes.LUR)

    levels = [
        Tilemap(6, 14, 0), Tilemap(6, 14, 1), Tilemap(6, 14, 2),
        Tilemap(6, 14, 0, 640), Tilemap(6, 14, 1, 640), Tilemap(6, 14, 2, 640)]
    leftLevel = 0
    rightLevel = 0

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
                        levels[leftLevel].hotReload()
                        levels[3+rightLevel].hotReload()
                        
                    elif event.key == pygame.K_e:
                        screen = editor.toggle()
                        levels[leftLevel].hotReload()
                        levels[3+rightLevel].hotReload()
                        
                    playerOne.control(event.key, InputTypes.KEYDOWN, dt)
                    playerTwo.control(event.key, InputTypes.KEYDOWN, dt)

                case pygame.KEYUP:
                    playerOne.control(event.key, InputTypes.KEYUP, dt)
                    playerTwo.control(event.key, InputTypes.KEYUP, dt)

        screen.fill((145, 194, 158))

        if not editor.editingMode:
            levels[leftLevel].draw(screen)
            levels[3+rightLevel].draw(screen)

            playerOne.movementUpdate(dt)
            playerOne.draw(screen)

            playerTwo.movementUpdate(dt)
            playerTwo.draw(screen)

            collisionCheck((leftLevel, rightLevel))

        else:
            editor.render(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000
    pygame.quit()

if __name__ == "__main__":
    main()