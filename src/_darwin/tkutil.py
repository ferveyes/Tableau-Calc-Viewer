'''
Created on 2023/12/09

@author: YouheiSakurai
'''
from contextlib import contextmanager
from sys import exit
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter import Tk
from traceback import format_exception


@contextmanager
def tk_withdraw():
    root = Tk()
    root.withdraw()
    try:
        yield root
    finally:
        root.destroy()


@contextmanager
def exit_on_exception(*expects):
    try:
        yield
    except expects as e:
        with tk_withdraw():
            showinfo(type(e).__name__, str(e))
        exit(0)
    except Exception as e:
        with tk_withdraw():
            showerror("Exception occurs", format_exception(e))
        exit(1)
