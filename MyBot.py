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
                # if not full strength, move if you can capture a site
                mystrength = gameMap.getSite(location).strength
                capturefound = False
                for dir in CARDINALS:
                    if ((gameMap.getSite(location, dir).owner != myID) and (mystrength >= gameMap.getSite(location, dir).strength)):
                        moves.append(Move(location, dir))
                        capturefound = True
                        break
                # if full strength, move either north or west, depending on your location
                if((capturefound == False) and (mystrength > (6 * gameMap.getSite(location).production))):
                    if (x+y)%2 == 1:
                        moves.append(Move(location, NORTH))
                    else:
                        moves.append(Move(location, WEST))

    sendFrame(moves)
