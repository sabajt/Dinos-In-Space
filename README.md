# Dinos-In-Space

Logic Puzzle Game Implemented in Python and Pygame

Released Spring 2012

You can download the binary for the game [here](http://sabajt.itch.io/dinos-in-space)

## Purpose

This was my first attempt at designing a game, and programming a large application after spending about half a year teaching myself how to program. As such, the code was mostly a mess. The horrors are vast: version control wasn't even used in the initial development, which is why some of the python file names had a number postfix - basically a crappy DIY version control involving saving a copy of the entire source.The code still works however, so I'd like to clean it up a bit to make the project a resource for others. In the end, the thing I am most proud of is the game design itself.

## Running From Source

You will need [Python 2.7](http://pygame.org/download.shtml) and the appropriate version of [Pygame](http://pygame.org/download.shtml). Follow the instructions on the Pygame website for installation. This will differ for your operating system.  Pygame is compatible with Windows, OSX and Linux.  If you are installing on OSX, you may also need to install [XQuartz](http://xquartz.macosforge.org/landing/)

Confirm that Pygame is installed correctly by launching Python interpeter on the command line:

```
$ python

Python 2.7.9 (v2.7.9:648dcafa7e5f, Dec 10 2014, 10:10:46) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

Then trying to import Pygame within the interpreter:

```
>>> import pygame
```

If Pygame is setup correctly, you should receive no errors. Now change to the source directory and run the top level module:

```
$ python dinosInSpace.py
```

If everything worked, this should launch the game.  
