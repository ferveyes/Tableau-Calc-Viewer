'''
Created on 2023/12/07

@author: YouheiSakurai
'''
from contextlib import suppress
from os import getcwd
from os import getpid
from os import listdir
from threading import Event
from threading import Thread
from time import sleep
from tkinter.filedialog import askdirectory

from appscript import app
from appscript import CommandError
from appscript import its
from HIServices import AXIsProcessTrustedWithOptions
from HIServices import kAXTrustedCheckOptionPrompt

from _darwin.compat.win32gui import GetForegroundWindow
from _darwin.compat.win32gui import GetWindowText


class AccessibilityBlocked(Exception):
    def __str__(self, *_, **__):
        return ("The application is not trusted. Please re-launch the "
                'application after permitting access to "Accessibility" from '
                "Apple menu > System Settings > Privacy & Security.")


class FilesAndFoldersBlocked(Exception):
    def __str__(self, *_, **__):
        return ("The application is not trusted. Please re-launch the "
                'application after permitting access to "Files and Folders" '
                "from Apple menu > System Settings > Privacy & Security.")


class AccessObtained(Exception):
    """Exception to work around a crash GUI initialization may cause

    Ref. issues:
    - https://github.com/moses-palmer/pynput/issues/511
    - https://github.com/moses-palmer/pynput/issues/427
    - https://github.com/moses-palmer/pynput/issues/416
    PRs:
    - https://github.com/moses-palmer/pynput/pull/512
    - https://github.com/moses-palmer/pynput/pull/541
    Reported macOS versions:
    - Catalina (10.x)
    - Big Sur (11.x)
    - Monterey (12.x)
    """
    def __str__(self, *_, **__):
        return ("The application has obtained access to the working "
                "directory. Please re-launch the application.")


def probe_accessibility():
    trusted = AXIsProcessTrustedWithOptions(
        {kAXTrustedCheckOptionPrompt: True}
    )
    if not trusted:
        with suppress(CommandError):
            GetWindowText(GetForegroundWindow())
        raise AccessibilityBlocked()


def probe_files_and_folders():
    try:
        listdir(getcwd())
    except PermissionError:
        try:
            with DialogBoxCloser(attempts=30, interval=0.1):
                # This is a workaround to obtain explicitly granted access.
                # See also https://stackoverflow.com/a/58417016
                askdirectory(initialdir=getcwd(), mustexist=True)
            listdir(getcwd())
            raise AccessObtained()
        except PermissionError:
            raise FilesAndFoldersBlocked()


class DialogBoxCloser(Thread):
    def __init__(self,
                 attempts,
                 interval,
                 key="\r",
                 bundle_identifier="org.python.python",
                 creator_type="PytX",
                 unix_id=getpid()):
        super().__init__(daemon=True)
        self.attempts = attempts
        self.interval = interval
        self.key = key
        self.bundle_identifier = bundle_identifier
        self.creator_type = creator_type
        self.unix_id = unix_id
        self.stopping = Event()

    def run(self):
        for _ in range(self.attempts):
            if self.stopping.is_set():
                break
            p = app("System Events").processes[
                its.bundle_identifier == self.bundle_identifier and
                its.creator_type == self.creator_type and
                its.unix_id == self.unix_id
            ]
            with suppress(CommandError):
                p.frontmost.set(True)
                if all(p.frontmost()) and all(p.windows.focused()):
                    p.keystroke(self.key)
            sleep(self.interval)

    def stop(self, timeout=None):
        self.stopping.set()
        self.join(timeout=timeout)

    def __enter__(self):
        self.start()

    def __exit__(self, *_):
        self.stop()
