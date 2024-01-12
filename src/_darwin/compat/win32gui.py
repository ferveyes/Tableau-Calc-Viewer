'''
Created on 2023/12/09

@author: YouheiSakurai
'''
import sys

from appscript import app
from appscript import its


def GetForegroundWindow():
    return app("System Events").processes[its.frontmost == True]  # noqa


def GetWindowText(proc):
    return proc.windows[0].name()[0]


def GetClassName(proc):
    ident = proc.bundle_identifier()[0]
    type_ = proc.creator_type()[0]
    if ident.startswith("com.tableausoftware"):
        return "Qt"
    elif ident == "org.python.python" and type_.lower() == "pytx":
        return "Tk"
    elif (ident.startswith("com.ferveyes.") and
          getattr(sys, "frozen", False) and
          hasattr(sys, "_MEIPASS")):
        return "Tk"
    else:
        return ""
