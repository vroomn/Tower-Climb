from jsonHandlers import *
from tilemap import *
from editor import Editor

import pygame
import pygame.gfxdraw

updateLocalJson()

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
                    levelOne.hotReload()

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