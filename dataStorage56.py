""" dataStorage56.py
    -----------------------------------------
    game (top dir)
        [py files] - python modules
        [pyc files]

        maps
            misssion
                [dat files] - built in maps

            user
                [dat files] - user made maps

        profile
            [dat files] - saved game data
"""

import os
import pickle
import pygame
import dinosInSpace

MAP_DIR         = "maps"
USER_DIR        = "user"
MISSION_DIR     = "mission"
PROFILE_DIR     = "profile"
SCREENCAP_DIR   = "screenCap"
TRACK           = False
MAPS_RECORD     = "_userMapsRecord.dat"
SNAX_ARCHIVE    = "_snaxArchive"
SNAX_MILESTONE  = "_snaxMilestone"

def findNewMaps():
    os.chdir("..")
    os.chdir("..")

    for f in os.listdir("."):
        print f

    os.chdir("Contents")
    os.chdir("Resources")

def writeMap(mapName, mapData, isUserMap):
    """ pickle map data """

    os.chdir(MAP_DIR)

    if isUserMap:
        os.chdir(USER_DIR)
    else:
        os.chdir(MISSION_DIR)

    fileName = mapName + ".dat"

    f = open(fileName, "wb")
    pickle.dump(mapData, f)
    f.close()
    os.chdir("..")
    os.chdir("..")

    track("writeMap")

def getMap(mapName, isUserMap):
    """ unpickle and return map info """

    os.chdir(MAP_DIR)

    if isUserMap:
        os.chdir(USER_DIR)
    else:
        os.chdir(MISSION_DIR)

    fileName = mapName + ".dat"
    f = open(fileName, "rb")
    mapData = pickle.load(f)
    f.close()
    os.chdir("..")
    os.chdir("..")

    track("getMap")

    return mapData

def deleteMap(mapName):
    os.chdir(MAP_DIR)
    os.chdir(USER_DIR)

    fileName = mapName + ".dat"
    os.remove(fileName)

    os.chdir("..")
    os.chdir("..")

    track("deleteMap")

    # remove entry from the maps record
    removeUserMapsEntry(mapName)

def deleteProfile(profileName):
    os.chdir(PROFILE_DIR)

    fileName = profileName + ".dat"
    assert (fileName in os.listdir("."))
    os.remove(fileName)

    track("deleteProfile")

    os.chdir("..")

def checkDir(mapName):
    """ check if user map exists """

    os.chdir(MAP_DIR)
    os.chdir(USER_DIR)

    fileName = mapName + ".dat"
    dirFiles = []

    inDir = False

    for f in os.listdir("."):
        dirFiles.append(f.upper())

    if fileName.upper() in dirFiles:
        inDir = True

    os.chdir("..")
    os.chdir("..")

    track("checkDir")

    return inDir

def writeProfile(profileName, profileData):
    """ pickle user profile data """

    os.chdir(PROFILE_DIR)

    fileName = profileName + ".dat"
    f = open(fileName, "wb")
    pickle.dump(profileData, f)
    f.close()

    track("writeProfile")

    os.chdir("..")

def getProfile(profileName):
    """ unpickle and return profile data """

    os.chdir(PROFILE_DIR)

    fileName = profileName + ".dat"
    f = open(fileName, "rb")
    profileData = pickle.load(f)
    f.close()
    os.chdir("..")

    track("getProfile")

    return profileData

def getPuzzleData(profileName, puzzleName):
    """ get profile data for just one puzzle """

    os.chdir(PROFILE_DIR)

    fileName = profileName + ".dat"
    f = open(fileName, "rb")
    profileData = pickle.load(f)
    puzzleData = profileData[puzzleName]
    f.close()
    os.chdir("..")

    track("getPuzzleData")

    return puzzleData

def modProfile(profileName, puzzleName, win=0, snax=0):
    """
        modify profile data to reflect changes after completing puzzle
        - if any snax are collected, they come in a list (previously index values)
        - set snax to 1 in profile data to mark collected
    """
    os.chdir(PROFILE_DIR)

    fileName = profileName + ".dat"
    f = open(fileName, "rb")
    profileData = pickle.load(f)
    curPuzzle = profileData[puzzleName]

    if win:
        curPuzzle[2] = True

    if snax:
        for s in snax:
            curPuzzle[4][s.index] = 1 # mark as complete
            tempList = profileData["_snaxArchive"]
            tempList.append(s.imageKey)
            profileData["_snaxArchive"] = tempList # add collected snax to archive

    # place puzzle back in profile dict and write to file
    profileData[puzzleName] = curPuzzle
    f.close()
    f = open(fileName, "wb")
    pickle.dump(profileData, f)
    f.close()

    track("modProfile")

    os.chdir("..")

def checkForProfile(profileName):
    """
        check for existing profile before overwriting
        - called by profile creator before launching new game
    """
    os.chdir(PROFILE_DIR)

    inDir = False
    fileName = profileName + ".dat"
    dirFiles = []

    for f in os.listdir("."):
        dirFiles.append(f.upper())

    if fileName.upper() in dirFiles:
        inDir = True

    os.chdir("..")
    track("checkForProfile")

    return inDir

def getSortedProfiles(andNames=False):
    """ return a sorted (alphabetic) list of unpickled profile data """

    os.chdir(PROFILE_DIR)

    fileNames = []
    for p in os.listdir("."):
        if p[-4:] == ".dat":
            fileNames.append(p)

    dataFiles = []
    if fileNames:
        fileNames.sort()
        for n in fileNames:
            f = open(n, "rb")
            data = pickle.load(f)
            dataFiles.append(data)
            f.close()

    os.chdir("..")

    track("getSortedProfiles")

    if not andNames:
        return dataFiles
    else:
        return dataFiles, fileNames

#    # puzzle name   :   [file name, locked, complete, difficulty, snacks collected, secret exit found]
#    #
#    #   -0 (string) _file name_     : passed as 'dest' to map selector (level)
#    #   -1 (bool)   _locked_        : controlls player access / preview
#    #   -2 (bool)   _complete_      : displays if complete, adds to global profile completed count
#    #   -3 (int)    _difficulty_    : displays difficulty level
#    #   -4 (list)   _snacks_        : displays how many snacks collected as a list; 0==notcolected,1== collected; pass 'None' if n/a

def saveDynamicImage(image, sourceName, editOrPlay):
    """ save image as png in screenCap dir w/std prefix _EDIT_ or _PLAY_ """

    os.chdir(SCREENCAP_DIR)
    fileName = "_" + editOrPlay + "_" + sourceName + ".png"
    pygame.image.save(image, fileName)
    os.chdir("..")

    track("saveDynamicImage")

def getDynamicImage(sourceName, editOrPlay):
    """ return screen captured image from map name """

    os.chdir(SCREENCAP_DIR)
    fileName = "_" + editOrPlay +"_" + sourceName + ".png"
    inDir = False
    dirFiles = []
    for f in os.listdir("."): ### clean this up with f == fileName etc
        dirFiles.append(f)
    if fileName in dirFiles:
        inDir = True

    if inDir:
        image = dinosInSpace.loadImage(fileName, None, None, None, True) # True flag is to look in current directory for image
    else:
        foundBackup = False
        if editOrPlay == "EDIT": # grab play snapshot if edit is not there
            fileName = "_PLAY_" + sourceName + ".png"
            for f in os.listdir("."):
                if f == fileName:
                    image = dinosInSpace.loadImage(fileName, None, None, None, True)
                    foundBackup = True
                    break
        if not foundBackup:
            image = dinosInSpace.loadImage("_imageNotFound.png", (400,300), None, None, True)

    #image = image.convert()
    os.chdir("..")

    track("getDynamicImage")
    return image

def removeDynamicImage(sourceName, editOrPlay):
    """ delete a captured image"""

    os.chdir(SCREENCAP_DIR)
    fileName = "_" + editOrPlay +"_" + sourceName + ".png"
    inDir = False
    dirFiles = []
    for f in os.listdir("."):
        dirFiles.append(f)
    if fileName in dirFiles:
        inDir = True
    if inDir:
        os.remove(fileName)
##    else:
##        print "attempted to remove a non-existing image: " + fileName
    os.chdir("..")

    track("removeDynamicImage")


def getUserMapsRecord():
    """ return the record of what user created maps the player has played """

    os.chdir(SCREENCAP_DIR)

    if MAPS_RECORD not in os.listdir("."):
        f = open(MAPS_RECORD, "wb")
        pickle.dump({None:None}, f)
        f.close()
    f = open(MAPS_RECORD, "rb")
    record = pickle.load(f)
    f.close()
    os.chdir("..")

    track("getUserMapsRecord")
    return record

def logUserMapsRecord(mapName):
    """ log a play on the user map record """

    os.chdir(SCREENCAP_DIR)
    f = open(MAPS_RECORD, "rb")
    record = pickle.load(f)
    if mapName not in record:
        record[mapName] = 0 # map name : has completed

    f.close()
    f = open(MAPS_RECORD, "wb")
    pickle.dump(record, f)
    f.close()
    os.chdir("..")

    track("logUserMapsRecord")

def logUserMapsComplete(mapName):
    """ log map completed (for screen overlay) on map record """

    os.chdir(SCREENCAP_DIR)
    f = open(MAPS_RECORD, "rb")
    record = pickle.load(f)
    assert(mapName in record)
    record[mapName] = 1 # complete == 1, incomplete == 0

    f.close()
    f = open(MAPS_RECORD, "wb")
    pickle.dump(record, f)
    f.close()
    os.chdir("..")

    track("logUserMapsComplete")

def removeUserMapsEntry(mapName):

    os.chdir(SCREENCAP_DIR)

    if MAPS_RECORD not in os.listdir("."): # create file if it's not there
        f = open(MAPS_RECORD, "wb")
        pickle.dump({None:None}, f)
        f.close()

    f = open(MAPS_RECORD, "rb")
    record = pickle.load(f)

    for r in record:
        if r == mapName:
            record.pop(r)
            break
    f.close()

    f = open(MAPS_RECORD, "wb")
    pickle.dump(record, f)
    f.close()

    os.chdir("..")
    track("removeUserMapsEntry")

def getSnaxRecord(profileName):
    """ return snax record """

    profile = getProfile(profileName)
    snaxRecord = profile[SNAX_ARCHIVE]

    track("getSnaxRecord")
    return snaxRecord

def logNextMilestone(profileName):
    """ each call converts next milestone to 0, representing that the milestone has been reached """
    profileData = getProfile(profileName)
    milestone = getMilestone(profileName)

    index = 0
    for m in milestone:
        if m:
            break
        index += 1

    milestone[index] = 0
    profileData[SNAX_MILESTONE] = milestone

    writeProfile(profileName, profileData)

    track("logNextMilestone")

def getMilestone(profileName):
    """ return snax milestone record """

    profileData = getProfile(profileName)
    return profileData[SNAX_MILESTONE]

    track("getMilestone")


def track(f_name):
    if TRACK:
        print ">>>>>>>>>>>>>>>> " + f_name + " ran"

