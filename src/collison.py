from enum import Enum
import jsonHandlers

class CollisionType(Enum):
    PLAYER = 0
    RECT = 1

players: list[list[object, CollisionType]] = []
def collisionCheck(activeStages):
    towerRects = []
    j = 0
    for item in jsonHandlers.stages[f"L0"]:
        if item["cS"] == True:
            towerRects.append(j)
        j += 1

    leftPlayer = (lambda: players[0][0] if players[0][0].rect.x < 512 else players[1][0])()
    rightPlayer = (lambda: players[0][0] if players[0][0].rect.x > 512 else players[1][0])()

    for i in towerRects:
        x = int(i/14)*64
        y = (i%14)*64
        
        # Collision Detection Algorithm: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
        if (leftPlayer.rect.x < x + 64 and
            leftPlayer.rect.x + 64 > x and
            leftPlayer.rect.y < y + 64 and
            leftPlayer.rect.y + 64 > y):
            print("Left collsion")

        x += 640
        if (rightPlayer.rect.x < x + 64 and
            rightPlayer.rect.x + 64 > x and
            rightPlayer.rect.y < y + 64 and
            rightPlayer.rect.y + 64 > y):
            print("Right collsion")
