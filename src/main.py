import pygame
from player import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    playerOne = Player((100, screen.get_height()/2), "blankSprite.jpeg", InputTypes.LUR)

    dt: float = 0
    running = True
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                
                case pygame.KEYDOWN:
                    playerOne.control(event.key, InputTypes.KEYDOWN, dt)

                case pygame.KEYUP:
                    playerOne.control(event.key, InputTypes.KEYUP, dt)
                
        screen.fill((145, 194, 158))

        playerOne.movementUpdate(dt)

        playerOne.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000
    
    pygame.quit()

if __name__ == "__main__":
    main()