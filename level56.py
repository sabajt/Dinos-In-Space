""" level.py

    function
        buildLevel
        wipeData

"""

import pygame
import dinosInSpace
import soundFx56
import scroller56
import radar56
import star56
import static56
import block56
import dino56
import interface56
import tracer56
import infoGraphic56
import controlMenu56
import dataStorage56
import endMessage
import snack
import autoMessage
import gfx56
import modeSwitch
import snackPacket
import simpleLabel

# colors

BERRY = (153, 86, 98)
TWILIGHT = (23, 123, 159)
MOONSTRUCK = (68, 103, 161)
LILAC = (172, 191, 233)
PLUM = (134, 106, 125)
KEYLIME = (198, 227, 171)

# default dino speed

DSPEED = 6
DSTEP = 25

PUZZLE_TITLE_LABEL_CENTER = (400,100)

def buildLevel(screen, mapName, isUserMap, profileName=None, puzzleName=None, _fps=60, imageFrom=None):
    """ builds and positions level objects """

    # define parameters




##    # --------- data testing - temp: only for packing old data lists into .dat
##

#    if not isUserMap:
#
#        mapData = (mode,
#                   mustSave,
#                   gridSize,
#                   bkgObjData,
#                   userBlocks,
#                   goals,
#                   spawns,
#                   sArrows,
#                   linkedArrows,
#                   mines,
#                   switches,
#                   dinoSets,
#                   message
#        )
#
#
#        dataStorage56.writeMap(mapName, mapData, isUserMap)

    (trashThis, # todo: remove this -- was mode (action or puzzle) but no longer needed as just puzzle
    mustSave,
    gridSize,
    bkgObjData,
    userBlocks,
    goals,
    spawns,
    sArrows,
    linkedArrows,
    mines,
    switches,
    dinoSets,
    message)    = dataStorage56.getMap(mapName, isUserMap) # message is always None, left out of laziness
    snax        = None
#    altExits    = None
    cameraPos   = None # default center

#    map mods
#
#    - hardcode background data / messages here (cannot build with map editor)
#    - modify by overwrite
#        > example:
#            -modify speed of first dino (increase by 3x):
#
#                ## map conditional
#                if mapName == "mapName":
#
#                    # overwrite speed data
#                    dinoSets[0][3] = 3 * DSPEED
#
#
#        __________________________________
#        data structure:
#        ----------------------------------
#
#        bkgObj data
#
#            stars: class ("star"), step, color
#            scrolling backgrounds objects
#                (
#                    class, -> "scroll", "float" *, "wrap" *, "cow" **
#                    minSpeed, -> 1
#                    loc, -> (1,1)
#                    imgFile, -> "fileName.png"
#                    scale, -> (20,20) or "2X"
#                    getAt, -> (0,0)
#                    spinRange, -> 1.5
#                    * floatSpeed, -> (.5,1)
#                    ** flashData -> (OFFTIME, VAR_RANGE)
#                 )
#
#        message data
#
#            message = controlMenuXX.messageObject
#
#        dino data
#
#            [type, num, color, speed, spawn, delayStart, delayStep]
#            example: [ "delux", 1, "green", DSPEED, 1, DSTEP, 0 ]
#
#        snax data
#
#            [
#                [imgKey, gridPos, switchChan=0, defState=None]
#                example: ["HAMBURGER", (4,5), 2, "ON"]
#            ]
#
#            ******** must sync new profile data in areaSelect.py AND snackWorld.py for snax *********
#
#
#        ----------------------------------
# puzzle name   :   [file name, locked, complete, difficulty, snacks collected, secret exit found]
#
#   -0 (string) _file name_     : passed as 'dest' to map selector (level)
#   -1 (bool)   _locked_        : controlls player access / preview
#   -2 (bool)   _complete_      : displays if complete, adds to global profile completed count
#   -3 (int)    _difficulty_    : displays difficulty level
#   -4 (list)   _snacks_        : displays how many snacks collected as fraction, pass 'None' if n/a
#   -5 (list)   _exits found    : displays how many alternate exits found, pass 'None' if n/a
#
#   "Roundabout"    :   ["1_Roundabout", False, False, 1, [0,0], [1,1]],


    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| add snax ||||||||||||||||||||||||||||||||||||||||
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    nextTutorial = None
    isLastPuzzle = False
    if not isUserMap:
        puzzleData  = dataStorage56.getPuzzleData(profileName, puzzleName)
        if mapName == "1_TUT1":
            message = True
            nextTutorial = "1_TUT2"
            nextPuzzle = "tut2"
        elif mapName == "1_TUT2":
            message = True
            nextTutorial = "1_TUT3"
            nextPuzzle = "tut3"
        elif mapName == "1_TUT3":
            message = True
            nextTutorial = "1_TUT4"
            nextPuzzle = "tut4"
        elif mapName == "1_TUT4":
            message = True
            nextTutorial = "1_TUT5"
            nextPuzzle = "tut5"
        elif mapName == "1_TUT5":
            message = True
            nextTutorial = "1_TUT6"
            nextPuzzle = "tut6"
        elif mapName == "1_TUT6":
            message = True
            nextTutorial = "1_TUT7"
            nextPuzzle = "tut7"
        elif mapName == "1_TUT7":
            message = True
            nextTutorial = "_TERMINATE" # string is arbitrary as long as it doesn't start with '1_TUT'
            nextPuzzle = "_TERMINATE"   # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        elif mapName == "2_ODD_COLOR_OUT":
            message = True
        elif mapName == "3_SMALL_DETOUR":
            message = True
        elif mapName == "4_GO_FOR_IT":
            message = True
            snax = [
                ["sugar pufz", (1,3)]
            ]
        elif mapName == "5_SWITCHES":
            message = True
        elif mapName == "9_CROSS_PATHS":
            message = True
            snax = [
                ["shrimp nuggets", (3,1), 1, "OFF"],
                ["candydough", (6,1), 1, "ON"]
            ]
        elif mapName == "10_LOOP":
            snax = [
                ["barbequarks", (2,1)],
                ["picklesicle", (4,5)]
            ]
        elif mapName == "11_ISLAND":
            message = True
        elif mapName == "12_SARDINES_1":
            snax = [
                ["fizzy beerwafers", (1,1)]
            ]
        elif mapName == "14_TRY_THE_HARD_WAY":
            message = True
            snax = [
                ["nanocorn", (1,5)]
            ]
        elif mapName == "19_CORRAL":
            message = True
            snax = [
                ["lucky coffee", (3,1)],
                ["munchzilla", (7,2)]
            ]
        elif mapName == "21_SPLIT_UP":
            snax = [
                ["cheese zees", (3,1)],
                ["chocobeanz", (2,5), 2, "ON"]
            ]
        elif mapName == "22_ASTEROID_FIELD":
            message = True
            cameraPos = "R"
        elif mapName == "26_UNDER_YOUR_NOSE":
            snax = [
                ["funtarts", (2,1), 1, "ON"],
                ["grade a milk", (2,2)]
            ]
        elif mapName == "28_SECTIONS":
            message = True
            cameraPos = "TR"
        elif mapName == "29_SARDINES_2":
            message = True
        elif mapName == "30_TASTY_TROVE":
            cameraPos = "L"
            snax = [
                ["penutbutter cubes", (4,4)],
                ["yumzingers", (6,3)]
            ]
        elif mapName == "31_SANDBAR":
            snax = [
                ["xtremophile gummies", (1,1), 1, "ON"],
                ["monster biscuits", (7,3)]
            ]
        elif mapName == "32_HOPSCOTCH":
            cameraPos = "L"
            snax = [
                ["broccolibanana", (5,1), 1, "OFF"]
            ]
        elif mapName == "33_CORNERS":
            snax = [
                ["pizzaballoon", (1,1)]
            ]
        elif mapName == "34_COPY_CAT":
            message = True
            snax = [
                ["marshmelons", (5,3)]
            ]
        elif mapName == "38_NOT_SO_FAST":
            message = True
            snax = [
                ["joybacon", (2,3)],
                ["sushi yumyum cone", (3,1)],
                ["hexberries", (5,5), 2, "OFF"]
            ]
        elif mapName == "39_REALLY_CROWDED_CREW":
            message = True
        elif mapName == "40_RESCUE":
            message = True
            snax = [
                ["lazercut fries", (4,4)]
            ]
        elif mapName == "41_GATEWAY":
            isLastPuzzle = True
            message = True

#        elif mapName == "30_TASTY_TROVE":

#wrapping bkg data: 'wrap', minSpeed, gridPair, imgFile, scaleTo, getAt, spinRange, floatSpeed


#   END MODS -----------------------------------------------///////////////////////////////

    # make everything: code after this point runs every time

    # game, scroller, radar
    game = dinosInSpace.Game(screen, nextTutorial, isLastPuzzle)
    soundFx56.GameSoundManager(game)
    scroller56.Scroller(game, gridSize, cameraPos, _fps)
    radar = radar56.Radar(game)
    radar56.makeGrid(game, gridSize)


    # stars / moving background objects
    if bkgObjData: # note there SHOULD always be bkgobj data
        star56.construct(game, bkgObjData)

    # user blocks
    block56.buildUserBlocks(game, userBlocks)

    # all static blocks except for goals
    if spawns:
        for s in spawns:
            spawn = static56.buildSpawn(game, s[0], s[1], dinoSets)

    if sArrows:
        for a in sArrows:
            arrow = static56.buildStaticArrow(game, a[0], a[1], a[2])

    if mines:
        for m in mines:
            mine = static56.buildMine(game, m[0])

    linkList = []
    if linkedArrows:
        for l in linkedArrows:
            linkArrow = static56.buildLinkedArrow(game, l[0], l[1], l[2], l[3], l[4])
            linkList.append(linkArrow)

    # snax
    snack.initImgLib()
    linkedSnax = {}
    i = 0
    snaxRemaining = False
    if snax:
        for s in snax:
            if not puzzleData[4][i]: # if the snack is not collected already

                if len(s) > 2: # if the snax mod has linked data (4 vs 2 len)
                    newSnack = snack.Snack(snax[i][0], snax[i][1], i, s[3]) # xtra last param is default linked state ("ON" or "OFF")
                else:
                    newSnack = snack.Snack(snax[i][0], snax[i][1], i)
                newSnack.register()
                # linked snax
                if len(s) > 2: # if the snax mod has linked data (4 vs 2 len)
                    linkedSnax[newSnack] = s[2] # object as key and switch channel as value

                snaxRemaining = True
            i += 1
#    game.addGroup(snack.Snack.snaxGroup) -- old place for snax addition

    #switchCount = 0
    if switches:
        for s in switches:
            #switchCount += 1
            switch = static56.buildSwitch(game, s[0])
            myLinkedObjs = []
            for l in linkList:
                if l.getSwitchNum() == s[1]: # s[1] is channel
                    myLinkedObjs.append(l)

            for lsnax in linkedSnax:
                if linkedSnax[lsnax] == s[1]: # if linked snax value (channel) == switch channel
                    myLinkedObjs.append(lsnax)

            switch.setLinked(myLinkedObjs)

    if len(static56.StaticBlock.staticGroup) > 0:
        game.addGroup(static56.StaticBlock.staticGroup) # add all sObj to game

    if snaxRemaining:
        game.addGroup(snack.Snack.snaxGroup)

    # goals (space stations)
    if goals:
        for g in goals:
            goal = static56.buildGoal(game, g[0], g[1], _fps)

    # grid blocks
    interface56.makeGridBox(game, gridSize)

#### snax was here

    # dinos
    for s in dinoSets:
        dinos = dino56.buildDinoSet(game, s, _fps)
    dino56.Dino.setGridSize(gridSize)

    dino56.DinoDelux.setREF_TOTAL()
    game.addGroup(dino56.Dino.dinoGroup)
    game.addGroup(dino56.Dino.packetGroup) ######################  packet group
    snackPacket.initImgLib()

    # depth index for above passing animations
    paDepth = dinosInSpace.Game.getGroupListLen()
    dino56.Dino.setPaDepth(paDepth)

    # cursor >>

    # add objects to radar >>

    # tracer
    block56.Tracer()
    static56.Switch.makeTracers()
    game.addGroup(block56.Tracer.tracerGroup)
    game.addGroup(tracer56.SwitchTracer.switchTracerGroup)

    # counters / infoGraphics, grid
    interface56.CursorCounter(game)
    interface56.ItemMenu(game)
        ##static56.makeGoalCounter(game)
#    radar56.makeGrid(game, gridSize) moved to beginning
##    infoGraphic56.FPS(game) ############ ------------------------------------------------------- F P S
    infoGraphic56.SpawnInfoBox.setLoc()
    infoGraphic56.SpawnInfoBox.addToGame(game)

    # add objects to radar
##    radar56.Radar.setDinoGroup()
##    radar56.Radar.setStaticGroup()
##    radar56.Radar.setBlockGroup()
##    radar.makeImages()
    game.addGroup(radar56.RObj.rObjGroup)

    # cursor
    interface56.Cursor(game, _fps)

    # in game message
    if message: # make messages and stub through a message control menu
        autoMessage.initImgLib()
        autoMessage.StdMessage(game, profileName, puzzleName, _fps)
        game.addGroup(autoMessage.StdMessage.me.stdMessageGroup)
        stub = infoGraphic56.MessageStub(game, True)
        game.addGroup(stub.myGroup)
    else: # make stub independent of message control
        stub = infoGraphic56.MessageStub(game, False)
        game.addGroup(stub.myGroup)

##    if message: # make messages and stub through a message control menu
##        message(game)
##        game.addGroup(message.messageGroup)
##    else: # make stub independent of message control
##        stub = infoGraphic56.MessageStub(game, None)
##        game.addGroup(stub.myGroup)

    # in play control menu and dependants
    simpleLabel.initImgLib()
    formattedName = ""
    if isUserMap:
        for i in mapName:
            if i != "_":
                formattedName += i
            else:
                formattedName += " "
    else:
        formattedName = puzzleName
    inPlayMenu = controlMenu56.InPlayMenu(game)
    label = simpleLabel.Label(formattedName, PUZZLE_TITLE_LABEL_CENTER) # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    controlMenu56.InPlayMenu.inPlayGroup.add(label) # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    inPlayMenu.initDependants()
    game.addGroup(controlMenu56.InPlayMenu.inPlayGroup)

    # endMessage and professor dinostein
    endMessage.initImgLib()

    if isUserMap:
        profileName = "_user"
        puzzleName = mapName

    eMsg = endMessage.EndMessage(game, mustSave, profileName, puzzleName, _fps)
    game.addGroup(eMsg.endMessageGroup)

    # run puzzle !!!!!
    if isUserMap:
        snapshot = game.runGame(_fps, mapName, imageFrom) # map name passed in so photo can be logged
    else:
        snapshot = game.runGame(_fps, None, imageFrom)

    wipeData()

    retry = False
    if game.retry:
        retry = True

    #################
    ### tutorial vars
    #################

    wonTutorialStage = False
    if game.wonTutorialStage:
        if not retry:
            wonTutorialStage = True

    leaveRequest = False
    if game.leaveRequest:
        leaveRequest = True

    #################
    #################
    #################

    #################
    ### endgame vars
    #################

    wonLastStage = False
    if game.wonLastStage and not retry:
        wonLastStage = True

    del(game)

    if not nextTutorial: # normal case
        return retry, snapshot, wonLastStage
    else: # coming from a tutorial stage
        if wonTutorialStage:
            return snapshot, nextTutorial, nextPuzzle, leaveRequest # returns name of next tutorial (or _TERM) to program's main loop
        else:
            return snapshot, mapName, puzzleName, leaveRequest # returns name of the current to program's main loop


def wipeData():
    """ wipes all Data stored in classes that run in the puzzle - call after level ends """
    dinosInSpace.Game.wipe()
    block56.wipe()
    interface56.wipe()
    scroller56.wipe()
    star56.wipe()
    dino56.wipe()
    radar56.wipe()
    static56.wipe()
    tracer56.wipe()
    infoGraphic56.wipe()
    controlMenu56.wipe()
    soundFx56.wipe()
    snack.wipe()
    endMessage.wipe()
    autoMessage.wipe()
    snackPacket.wipe()

#EndMessage.wipe()

# * dino parameter rules:
#
#    - each list is a set of dinos
#    - each list must be the order in which the dinos come out
#    - the delay time b/w any dino must be a min of 10 (see static56.Spawn.setDirTimerKey for why)
#    - give None as last parameter in first set if direction will not change


#bkgObjData = [
#              ("star", 6, BERRY),
#              ("scroll", 1, (5,5), "nPlanet2.png", "2X", (0,0), None),
#              ("cow", 2, (3,3), "testCowUnlit.png", (60*4, 60*4), (0,0), 1.2, (1,0), (10,100) ),
#              ("cow", 2, (3,3), "testCowUnlit.png", (60*4, 60*4), (0,0), 1.2, (.5,0), (100,30) ) # testCow2 and testCowUnlit
#              ]
#    snax = [
#            ["TESTSNACK", (3,1)],
#            ["TESTSNACK", (3,2)]
#            ]


##
##    elif mapName == "2paths":
##
##        # mode, mustSave, grid, stars, planets
##
##        mode = "puzzle"
##        mustSave = 4
##        gridSize = (8,6) # max 24 * 24 ; min 8 * 6
##
##        # stars: class ("star"), step, color
##        # scrolling backgrounds objects
##            #   (
##            #       class, -> "scroll", "float", "wrap", "cow"
##            #       minSpeed, -> 1
##            #       loc, -> (1,1)
##            #       imgFile, -> "fileName.png"
##            #       scale, -> (20,20) or "2X"
##            #       getAt, -> (0,0)
##            #       spinRange, -> 1.5
##            #       *floatSpeed, -> (.5,1)
##            #       **flashData -> (OFFTIME, VAR_RANGE)
##            #   )
##
##        bkgObjData = [
##            ("star", 6, BERRY),
##        ]
##
##        # user / static block
##
##        userBlocks = [
##            [ "arrow", "green", 1 ],
##            [ "arrow", "yellow", 2 ],
##            [ "warp", None, 2 ]
##        ]
##
##        goals = [ # green / blue / red / yellow / None (grey)
##            [ (3, 5), "green" ],
##            [ (8, 4), "yellow" ]
##        ]
##
##        spawns = [
##            [ (2, 2), "south" ]
##        ]
##
##        sArrows = [
##            [ (2, 6), None, "east" ]
##        ]
##
##        linkedArrows = [
##            [ (4, 5), None, "hidden", "north", 1 ], # last param is switch
##            [ (8, 6), None, "north", "west", 1],
##            [ (8, 5), None, "west", "north", 1],
##            [ (4, 6), None, "west", "hidden", 2]
##        ]
##
##        mines = [
##            [ (4, 1) ],
##            [ (5, 1) ],
##            [ (6, 1) ],
##            [ (8, 1) ],
##            [ (6, 2) ],
##            [ (8, 2) ],
##            [ (8, 3) ],
##            [ (5, 2) ],
##            [ (6, 3) ],
##            [ (7, 1) ],
##            [ (7, 2) ],
##            [ (7, 3) ],
##            [ (7, 4) ]
##        ]
##
##        switches = [ # order assigns switch number
##            [ (5, 5), 1 ],
##            [ (3, 3), 2 ]
##        ]
##
##        # dinos
##
##        dinoSets = [
##            # [type, num, color, speed, spawn, delayStart, delayStep, direction]
##            [ "delux", 2, "green", DSPEED, 1, 0, DSTEP ],
##            [ "delux", 2, "yellow", DSPEED, 1, 60, DSTEP ]
##        ]
##
##        # message
##
##        message = None
##
##    elif mapName == "noArrows?":
##
##
##        # mode, mustSave, grid, stars, planets
##
##        mode = "puzzle"
##        mustSave = 8
##        gridSize = (10,6) # max 24 * 24 ; min 8 * 6
##
##        # stars: class ("star"), step, color
##        # scrolling backgrounds objects
##            #   (
##            #       class, -> "scroll", "float", "wrap", "cow"
##            #       minSpeed, -> 1
##            #       loc, -> (1,1)
##            #       imgFile, -> "fileName.png"
##            #       scale, -> (20,20) or "2X"
##            #       getAt, -> (0,0)
##            #       spinRange, -> 1.5
##            #       *floatSpeed, -> (.5,1)
##            #       **flashData -> (OFFTIME, VAR_RANGE)
##            #   )
##
##        bkgObjData = [
##            ("star", 6, BERRY),
##        ]
##
##        # user / static block
##
##        userBlocks = [
##            [ "warp", None, 10 ]
##        ]
##
##        goals = [ # green / blue / red / yellow / None (grey)
##            [ (6, 5), None ],
##        ]
##
##        spawns = [
##            [ (2, 3), "north" ],
##        ]
##
##        sArrows = [
##            [ (1, 2), None, "east" ],
##            [ (1, 5), None, "north" ],
##            [ (2, 1), None, "west" ],
##            [ (3, 1), None, "south" ],
##            [ (3, 3), None, "south" ],
##            [ (3, 4), None, "east" ],
##            [ (4, 4), None, "south" ],
##            [ (4, 5), None, "west" ],
##        ]
##
##        linkedArrows = [
##            [ (6, 1), None, "hidden", "east", 1 ], # last param is switch
##            [ (8, 5), None, "east", "hidden", 1],
##            [ (7, 5), None, "east", "hidden", 2],
##            [ (10, 3), None, "north", "west", 3],
##            [ (9, 5), None, "east", "hidden", 4]
##        ]
##
##        mines = [
##            [ (5, 1) ],
##            [ (5, 2) ],
##            [ (5, 3) ],
##            [ (5, 4) ],
##            [ (5, 5) ],
##            [ (6, 4) ],
##            [ (7, 4) ],
##            [ (8, 4) ],
##            [ (9, 4) ],
##            [ (10, 4) ],
##            [ (1, 6) ],
##            [ (2, 6) ],
##            [ (3, 6) ],
##            [ (4, 6) ],
##            [ (5, 6) ],
##            [ (6, 6) ],
##            [ (7, 6) ],
##            [ (8, 6) ],
##            [ (9, 6) ],
##            [ (10, 6) ],
##            [ (4, 3) ]
##        ]
##
##        switches = [ # [coords, switchNum]
##            [ (6, 2), 1 ],
##            [ (9, 1), 2 ],
##            [ (10, 2), 3],
##            [ (3, 5), 4 ]
##        ]
##
##        # dinos
##
##        dinoSets = [
##            # [type, num, color, speed, spawn, delayStart, delayStep]
##            [ "delux", 1, "green", DSPEED, 1, 0, 30 ],
##            [ "delux", 1, "red", DSPEED, 1, 30, 30 ],
##            [ "delux", 1, "blue", DSPEED, 1, 60, 30 ],
##            [ "delux", 1, "yellow", DSPEED, 1, 90, 30 ]
##        ]
##
##        # message
##
##        message = None
##


##
##    # -------------------------------------------------------------------------------------------------


#
#    nyanData = [
#                ("nyan", 2, gridSize, NYAN_FRAMES, "2X", (53*2-1,0), (4,0)),
#                ("nyan", 2, gridSize, NYAN_FRAMES, "2X", (53*2-1,0), (4,0)),
#                ("nyan", 2, gridSize, NYAN_FRAMES, "2X", (53*2-1,0), (4,0)),
#                ("nyan", 2, gridSize, NYAN_FRAMES, "2X", (53*2-1,0), (4,0))
#                ]
#

#    # NYAN MODE /////////////////////// ?
#    if modeSwitch.ModeSwitch.modes["NYAN"]:
#        for nyancat in nyanData:
#            bkgObjData.append(nyancat)
#


#NYAN_FRAMES = [
#               "nyansmall1.png",
#               "nyansmall2.png",
#               "nyansmall3.png",
#               "nyansmall4.png",
#               "nyansmall5.png",
#               "nyansmall6.png",
#               "nyansmall7.png",
#               "nyansmall8.png",
#               "nyansmall9.png",
#               "nyansmall10.png",
#               "nyansmall11.png",
#               "nyansmall12.png"
#               ]




