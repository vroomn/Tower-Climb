import pygame
import pygame.gfxdraw
import os

class Cell:
    def __init__(self, filename: str, cellSize, posX, posY) -> None:
        self.image = pygame.image.load(os.path.join("textures", filename))
        self.rect = pygame.Rect(posX, posY, cellSize*2, cellSize*2)

    def draw(self, drawSurface: pygame.Surface) -> None:
        self.image = pygame.transform.scale(self.image, (32, 32))
        drawSurface.blit(self.image, self.rect)

        self.image = pygame.transform.scale(self.image, (64, 64))
        drawSurface.blit(self.image, pygame.Rect(32, 0, 64, 64))

        self.image = pygame.transform.scale(self.image, (128, 128))
        drawSurface.blit(self.image, pygame.Rect(64+32, 0, 128, 128))

class Tilemap:
    def __init__(self, width, height, cellSize) -> None:
        self.width = width
        self.height = height

        self.cellSize = cellSize

        self.testCell = Cell("sampleTexture.jpeg", cellSize, 0, 0)

    def wireframeDraw(self, screen: pygame.Surface) -> None:
        self.testCell.draw(screen)
        pygame.gfxdraw.rectangle(screen, pygame.Rect(0, 0, self.width * self.cellSize, self.height * self.cellSize), (255, 255, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    stageOne = Tilemap(6, 6, 16)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key == pygame.K_UP:
                    print("Up Key Pressed")

        screen.fill((145, 194, 158))

        stageOne.wireframeDraw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()