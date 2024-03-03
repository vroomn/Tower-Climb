from os import path
from enum import Enum
import pygame

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
            match key:
                case pygame.K_LEFT:
                    self.velocityX = -self.MOVEMENTSPEED * dt
                
                case pygame.K_RIGHT:
                    self.velocityX = self.MOVEMENTSPEED * dt

                case pygame.K_UP:
                    if self.velocityY < .5 and self.velocityY > -.5:
                        self.velocityY -= 600 * dt

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