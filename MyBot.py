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

def dirToNearestBorder(location):
    retVal = STILL
    distance = 1
    while (retVal==STILL):
        for dir in CARDINALS:
            distanceCounter = distance
            targetLocation = location
            while(distanceCounter > 0):
                targetLocation = gameMap.getLocation(targetLocation, dir)
                distanceCounter -= 1
            if(gameMap.getSite(targetLocation).owner != myID):
                retVal = dir
                break
        distance += 1
        if (distance > 4):
            if (location.x + location.y)%2 == 1:
                retVal = NORTH
            else:
                retVal = WEST
    return retVal

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                mystrength = gameMap.getSite(location).strength
                # if at high strength, and in friendly territory, move to the nearest border
                if (isInFriendlyTerritory(location)):
                    if(mystrength > (6 * gameMap.getSite(location).production)):
                        moves.append(Move(location, dirToNearestBorder(location)))
                # if on the border, move if you can capture a site
                else:
                    capturefound = False
                    #check to see if anything can be captured, and take it
                    for dir in CARDINALS:
                        if ((gameMap.getSite(location, dir).owner != myID) and ((mystrength > gameMap.getSite(location, dir).strength) or (mystrength == 255))):
                            moves.append(Move(location, dir))
                            capturefound = True
                            break
                    # if not, check to see if lots of strength, then combine with a higher strength neighbor that's also on the border (this way we don't trade places)
                    if (capturefound == False) and (mystrength > (6 * gameMap.getSite(location).production)):
                        for dir in CARDINALS: 
                            if (gameMap.getSite(location, dir).owner == myID) and (gameMap.getSite(location, dir).strength > mystrength) and (not isInFriendlyTerritory(gameMap.getLocation(location, dir))):
                                moves.append(Move(location, dir))
                                capturefound = True
                                break

    sendFrame(moves)
