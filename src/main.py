from os import path

import pygame
import pygame.gfxdraw

class Player:
    def __init__(self, initPos: tuple[int, int], texture: str) -> None:
        self.rect = pygame.Rect(initPos[0], initPos[1], 64, 64)
        self.surface = pygame.image.load(path.join("Sprite_Imgs", texture))

        self.velocityX = 0
        self.velocityY = 0
        self.gravityAcc = 60
        self.gravityCap = 100

    def movementUpdate(self, deltaTime: float):
        if self.velocityY < self.gravityCap:
            self.velocityY += int(self.gravityAcc * deltaTime)
        
        if self.rect.y+64 >= 720:
            self.velocityY = 0
            self.rect = self.rect.move(0, (720 - (self.rect.y+64)))

        self.rect = self.rect.move(self.velocityX, self.velocityY)

    def draw(self, drawSurface: pygame.Surface):
        drawSurface.blit(self.surface, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    playerOne = Player((10, 0), "blankSprite.jpeg")

    dt: float = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((145, 194, 158))

        playerOne.movementUpdate(dt)

        playerOne.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000
    
    pygame.quit()

if __name__ == "__main__":
    main()