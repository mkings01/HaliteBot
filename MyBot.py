from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("MyPythonBot")

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                # if full strength, move in a random direction
                mystrength = gameMap.getSite(location).strength
                if mystrength == 255:
                    moves.append(Move(location, random.choice(DIRECTIONS)))
                # otherwise move if you can capture a site
                else:
                    for dir in CARDINALS:
                        if ((gameMap.getSite(location, dir).owner != myID) and (mystrength >= gameMap.getSite(location, dir).strength)):
                            moves.append(Move(location, dir))
                            break
    sendFrame(moves)
