"""
    This is a setup.py script generated by py2applet

    Usage:
    python setup.py py2app
    """

from distutils.core import setup
import os
import py2exe

rootDir = "C:\\Users\\Saba\\Desktop\\dinoFinalFull - Copy"

artDir = rootDir + "\\art"
soundDir = rootDir + "\\sound"
screenCapDir = rootDir + "\\screenCap"
profileDir = rootDir + "\\profile"
missionDir = rootDir + "\\maps/mission"
userDir = rootDir + "\\maps/user"

artFiles = os.listdir(artDir)
soundFiles = os.listdir(soundDir)
screenCapFiles = os.listdir(screenCapDir)
profileFiles = os.listdir(profileDir)
missionFiles = os.listdir(missionDir)
userFiles = os.listdir(userDir)

artPaths = []
soundPaths = []
screenCapPaths = []
profilePaths = []
missionPaths = []
userPaths = []

for f in artFiles:
    f = os.path.join("art", f)
    artPaths.append(f)

for f in soundFiles:
    f = os.path.join("sound", f)
    soundPaths.append(f)

for f in screenCapFiles:
    f = os.path.join("screenCap", f)
    screenCapPaths.append(f)

for f in profileFiles:
    f = os.path.join("profile", f)
    profilePaths.append(f)

for f in missionFiles:
    f = os.path.join("maps/mission", f)
    missionPaths.append(f)

for f in userFiles:
    f = os.path.join("maps/user", f)
    userPaths.append(f)

setup(
    console = [
        {
            "script" : "dinosInSpace.py",
            "icon_resources" : [(0, "disIcon.ico")]
        }
    ],

    author = "John Saba",
    author_email = "john.t.saba@vanderbilt.edu",
    data_files = [
        ("art", artPaths),
        ("sound", soundPaths),
        ("screenCap", screenCapPaths),
        ("profile", profilePaths),
        ("maps/mission", missionPaths),
        ("maps/user", userPaths),
        ('.', ["dos.ttf", "UNIVERSALFRUITCAKE.ttf"])
    ]
)
