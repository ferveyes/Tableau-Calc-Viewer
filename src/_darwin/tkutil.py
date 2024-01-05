'''
Created on 2023/12/09

@author: YouheiSakurai
'''
from contextlib import contextmanager
from sys import exit
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo


@contextmanager
def exit_on(*exceptions, code=0):
    show = showinfo if code == 0 else showerror
    try:
        yield
    except exceptions as e:
        show(type(e).__name__, str(e))
        exit(code)
