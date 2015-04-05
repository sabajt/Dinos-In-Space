""" gameUtil.py
    - pygame main loop structure specific utilities
    John Saba
"""
import pygame

def updateIfMethod(e):
    """ call in main loop instead of update to update sprites w/ specified methods only """
    for s in g:
        methods = dir(s)
        if methodName in methods:
            s.updateMessage()

if __name__ == '__main__':
    print "module intended for import only"
