import pygame

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