from enum import Enum
import jsonHandlers
import pygame

class CollisionType(Enum):
    PLAYER = 0
    RECT = 1

players: list[list[object, CollisionType]] = []
def collisionCheck(activeStages):
    towerRects = []
    """j = 0
    for i in jsonHandlers.stages["L0"]:
        if i["cS"] == True:
            x = int(j/14)*64
            y = (j%14)*64
            print(x, y, j)
            towerRects.append(pygame.Rect(x, y, 64, 64))
        j += 1"""

    j = 0
    for item in jsonHandlers.stages[f"L0"]:
        if item["cS"] == True:
            towerRects.append(j)
        j += 1

    leftPlayer = (lambda: players[0][0] if players[0][0].rect.x < 512 else players[1][0])()
    rightPlayer = (lambda: players[0][0] if players[0][0].rect.x > 512 else players[1][0])()

    #leftPlayer.rect.collidelist(towerRects)
    
    for i in towerRects:
        x = int(i/14)*64
        y = (i%14)*64
        
        # Collision Detection Algorithm: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
        if (leftPlayer.rect.x < x + 64 and
            leftPlayer.rect.x + 64 > x and
            leftPlayer.rect.y < y + 64 and
            leftPlayer.rect.y + 64 > y):
            xMove = (lambda: -((leftPlayer.rect.x - x)+64) if leftPlayer.rect.x - x < x - (leftPlayer.rect.x-64) else x - (leftPlayer.rect.x-64))()
            yMove = (lambda: -((leftPlayer.rect.y - y)+64) if abs(leftPlayer.rect.y - y) > y - (leftPlayer.rect.y-64) else y - (leftPlayer.rect.y-64))()
            if abs(xMove) < abs(yMove):
                leftPlayer.rect = leftPlayer.rect.move(xMove, 0)
            else:
                leftPlayer.rect = leftPlayer.rect.move(0, yMove)
        """if (leftPlayer.rect.y < y + 64 and
            leftPlayer.rect.y + 64 > y):
            leftPlayer.rect = leftPlayer.rect.move(0,
                (lambda: -((leftPlayer.rect.y - y)+64) if leftPlayer.rect.y - y > y - (leftPlayer.rect.x-64) else y - (leftPlayer.rect.y-64))())
            
            if (leftPlayer.rect.x < x + 64 and
                leftPlayer.rect.x + 64 > x):
                    leftPlayer.rect = leftPlayer.rect.move(
                    (lambda: -((leftPlayer.rect.x - x)+64) if leftPlayer.rect.x - x < x - (leftPlayer.rect.x-64) else x - (leftPlayer.rect.x-64))(), 0)"""

        x += 640
        if (rightPlayer.rect.x < x + 64 and
            rightPlayer.rect.x + 64 > x and
            rightPlayer.rect.y < y + 64 and
            rightPlayer.rect.y + 64 > y):
            xMove = (lambda: -((rightPlayer.rect.x - x)+64) if rightPlayer.rect.x - x < x - (rightPlayer.rect.x-64) else x - (rightPlayer.rect.x-64))()
            yMove = (lambda: -((rightPlayer.rect.y - y)+64) if abs(rightPlayer.rect.y - y) > y - (rightPlayer.rect.y-64) else y - (rightPlayer.rect.y-64))()
            if abs(xMove) < abs(yMove):
                rightPlayer.rect = rightPlayer.rect.move(xMove, 0)
            else:
                rightPlayer.rect = rightPlayer.rect.move(0, yMove)
