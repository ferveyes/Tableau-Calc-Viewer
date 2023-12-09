'''
Created on 2023/03/28

@author: YouheiSakurai
'''
from os import environ
from os import system
from pathlib import Path
from subprocess import check_call
from sys import executable


class PackagesInstalled(Exception):
    def __str__(self, *_, **__):
        return ("Packages are installed/upgraded. "
                "Please re-launch the application manually.")


def ensure(**modules):
    try:
        for module in modules:
            __import__(module)
    except ImportError:
        logfile = Path.home() / (
            "." +
            environ.get("__CFBundleIdentifier", "pip-install").split(".")[-1] +
            ".log"
        )
        logfile.unlink(missing_ok=True)
        logfile.touch(exist_ok=True)
        system(f'open "{logfile}"')

        cmd = (
            executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--user",
            "--no-python-version-warning",
            "--disable-pip-version-check",
            "--no-cache-dir",
            # "--only-binary",
            # ":all:",
            "--log",
            str(logfile),
        ) + tuple(modules.values())
        check_call(cmd)
        raise PackagesInstalled()
