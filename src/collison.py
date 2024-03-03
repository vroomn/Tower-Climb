from enum import Enum
import jsonHandlers

class CollisionType(Enum):
    PLAYER = 0
    RECT = 1

players: list[list[object, CollisionType]] = []
def collisionCheck(activeStages):
    leftTowerRects = []
    leftPlayer = lambda: players[0][0] if players[0][0].rect.x < 512 else players[1][0]
    

    rightTowerRects = []
    rightPlayer = lambda: players[0][0] if players[0][0].rect.x > 512 else players[1][0]
