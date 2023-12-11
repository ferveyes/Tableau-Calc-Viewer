'''
Created on 2023/12/07

@author: YouheiSakurai
'''
from contextlib import suppress

from appscript import CommandError
from HIServices import AXIsProcessTrustedWithOptions
from HIServices import kAXTrustedCheckOptionPrompt

from _darwin.compat.win32gui import GetForegroundWindow
from _darwin.compat.win32gui import GetWindowText


class AccessibilityBlocked(Exception):
    def __str__(self, *_, **__):
        return ("The application is not trusted. Please re-launch the "
                'application after permitting access to "Accessibility" from '
                "Apple menu > System Settings > Privacy & Security.")


def probe_accessibility():
    trusted = AXIsProcessTrustedWithOptions(
        {kAXTrustedCheckOptionPrompt: True}
    )
    if not trusted:
        with suppress(CommandError):
            GetWindowText(GetForegroundWindow())
        raise AccessibilityBlocked()
