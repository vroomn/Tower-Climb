from os import path
from enum import Enum

import pygame
import pygame.gfxdraw

class InputTypes(Enum):
    KEYDOWN = 0
    KEYUP = 1

    WAD = 2 # WASD but W is jump and there is no "D"
    LUR = 3 # Left, Up, Right

class Player:
    def __init__(self, initPos: tuple[int, int], texture: str, schema: InputTypes) -> None:
        self.rect = pygame.Rect(initPos[0], initPos[1], 64, 64)
        self.surface = pygame.image.load(path.join("Sprite_Imgs", texture))

        self.schema = schema

        self.velocityX = 0
        self.MOVEMENTSPEED = 100
        self.ambientFriction = 50

        self.velocityY = 0
        self.gravityAcc = 60
        self.gravityCap = 100

        self.applyFriction = False

    def control(self, key, mode: InputTypes, dt):
        if mode == InputTypes.KEYUP:
            self.applyFriction = True
        else:
            self.applyFriction = False

        if self.schema == InputTypes.WAD:
            match key:
                case pygame.K_a:
                    self.velocityX = -self.MOVEMENTSPEED * dt
                
                case pygame.K_d:
                    self.velocityX = self.MOVEMENTSPEED * dt

                case pygame.K_w:
                    if self.velocityY < .5 and self.velocityY > -.5:
                        self.velocityY -= 600 * dt

        else:
            print("LUR Input Schema")

    def movementUpdate(self, deltaTime: float):
        if self.velocityY < self.gravityCap:
            self.velocityY += int(self.gravityAcc * deltaTime)

        if self.applyFriction == True:
            if self.velocityX > 0:
                self.velocityX -= 50*deltaTime

                # If overcorrected reset
                if self.velocityX < 0: 
                    self.velocityX = 0
            elif self.velocityX < 0:
                self.velocityX += 50*deltaTime

                # If overcorrected reset
                if self.velocityX > 0: 
                    self.velocityX = 0
        
        if self.rect.y+64 >= 721: # 720 is arbirary floor for skake of testing
            self.velocityY = 0
            self.rect = self.rect.move(0, (720 - (self.rect.y+64)))

        self.rect = self.rect.move(self.velocityX, self.velocityY)

    def draw(self, drawSurface: pygame.Surface):
        drawSurface.blit(self.surface, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    playerOne = Player((100, screen.get_height()/2), "blankSprite.jpeg", InputTypes.WAD)

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