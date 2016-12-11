from hlt import *
from networking import *
import logging

myID, gameMap = getInit()
sendInit("MyPythonBot")

logging.basicConfig(filename='MyBot.log',level=logging.DEBUG)
logging.debug('Starting debug log')

def isInFriendlyTerritory(location):
    retVal = True
    for dir in CARDINALS:
        if(gameMap.getSite(location, dir).owner != myID):
            retVal = False
    return retVal

def dirToNearestBorder(location):
    retVal = STILL
    DISTANCE_INTERVAL = 4
    MAX_DISTANCE = 5
    distance = 0

    while (retVal==STILL):
        distance += DISTANCE_INTERVAL
        if (distance > MAX_DISTANCE):
            retVal = (location.x + location.y)%2 + 1
        for dir in CARDINALS:
            distanceCounter = distance
            targetLocation = location
            while(distanceCounter > 0):
                targetLocation = gameMap.getLocation(targetLocation, dir)
                distanceCounter -= 1
            if(gameMap.getSite(targetLocation).owner != myID):
                retVal = dir
                break
    return retVal

while True:
    moves = []
    gameMap = getFrame()
    moveToPlanned = [[False for i in range(gameMap.width + 1)] for j in range(gameMap.height + 1)]
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                mystrength = gameMap.getSite(location).strength
                # if at high strength, and in friendly territory, move towards the nearest border
                if (isInFriendlyTerritory(location)):
                    if(mystrength > (6 * gameMap.getSite(location).production)):
                        targetDirection = dirToNearestBorder(location)
                        targetLocation = gameMap.getLocation(location, targetDirection)
                        if(not moveToPlanned[targetLocation.x][targetLocation.y]) and ((mystrength + gameMap.getSite(targetLocation).strength < 300)):
                            moves.append(Move(location, targetDirection))
                            moveToPlanned[targetLocation.x][targetLocation.y] = True
                # if on the border, move if you can capture a site
                else:
                    capturefound = False
                    #check to see if anything can be captured, and take it
                    for dir in CARDINALS:
                        targetLocation = gameMap.getLocation(location, dir)
                        targetSite = gameMap.getSite(targetLocation)
                        if ((targetSite.owner != myID) and ((mystrength > targetSite.strength) or (mystrength == 255))):
                            moves.append(Move(location, dir))
                            moveToPlanned[targetLocation.x][targetLocation.y] = True
                            capturefound = True
                            break
                    # if not, check to see if lots of strength, then combine with a higher strength neighbor that's also on the border (this way we don't trade places)
                    if (capturefound == False) and (mystrength > (6 * gameMap.getSite(location).production)):
                        for dir in CARDINALS: 
                            targetLocation = gameMap.getLocation(location, dir)
                            targetSite = gameMap.getSite(targetLocation)
                            if (targetSite.owner == myID) and (targetSite.strength > mystrength) and (not isInFriendlyTerritory(targetLocation)):
                                moves.append(Move(location, dir))
                                moveToPlanned[targetLocation.x][targetLocation.y] = True
                                capturefound = True
                                break

    sendFrame(moves)
