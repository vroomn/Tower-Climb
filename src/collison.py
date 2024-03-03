from enum import Enum
import jsonHandlers

class CollisionType(Enum):
    PLAYER = 0
    RECT = 1

players = []
def collisionCheck(activeStages):
    # Credit to https://stackoverflow.com/questions/9542738/find-a-value-in-a-list (Niklas B.)
    print()
    jsonHandlers.stages