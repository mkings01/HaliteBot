from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("MyPythonBot")

def isInFriendlyTerritory(location):
    retVal = True
    for dir in CARDINALS:
        if(gameMap.getSite(location, dir).owner != myID):
            retVal = False
    return retVal

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                mystrength = gameMap.getSite(location).strength
                # if at high strength, and in friendly territory, move either north or west, depending on your location
                if (isInFriendlyTerritory(location)):
                    if(mystrength > (6 * gameMap.getSite(location).production)):
                        if (x+y)%2 == 1:
                            moves.append(Move(location, NORTH))
                        else:
                            moves.append(Move(location, WEST))
                # if on the border, move if you can capture a site
                else:
                    capturefound = False
                    for dir in CARDINALS:
                        if ((gameMap.getSite(location, dir).owner != myID) and (mystrength >= gameMap.getSite(location, dir).strength)):
                            moves.append(Move(location, dir))
                            capturefound = True
                            break

    sendFrame(moves)
