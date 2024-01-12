from os import environ
import sys
import threading

from _darwin.bundle import cwd
from _darwin.bundle import exchook
from _darwin.bundle import pypkg
from _darwin import tkutil


def init():
    if environ.get("__CFBundleIdentifier", "").startswith("com.ferveyes."):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            basepath = sys.executable
        else:
            basepath = __file__
            sys.excepthook = threading.excepthook = exchook.excepthook

            with tkutil.exit_on(pypkg.PackagesInstalled):
                pypkg.ensure(appscript="appscript",
                             lxml="lxml",
                             HIServices="pyobjc-framework-ApplicationServices")

        if (basepath.startswith("/private/var/folders/")
                and "/AppTranslocation/" in basepath):
            # the app bundle is translocated
            # cf. https://github.com/pyinstaller/pyinstaller/issues/7573
            pass
        else:
            cwd.patch(basepath)

    from _darwin import perm

    with tkutil.exit_on(perm.AccessibilityBlocked):
        perm.probe_accessibility()

    with tkutil.exit_on(perm.FilesAndFoldersBlocked, perm.AccessObtained):
        perm.probe_files_and_folders()
