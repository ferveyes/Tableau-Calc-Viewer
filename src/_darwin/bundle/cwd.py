'''
Created on 2023/12/09

@author: YouheiSakurai
'''
from os import chdir
from os.path import dirname


def to_appdir():
    chdir(dirname(__file__.rsplit(".app/Contents/MacOS/", maxsplit=1)[0]))
