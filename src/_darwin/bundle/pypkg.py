'''
Created on 2023/03/28

@author: YouheiSakurai
'''
from os import system
from subprocess import check_call
from sys import executable
from tempfile import NamedTemporaryFile


class PackagesInstalled(Exception):
    def __str__(self, *_, **__):
        return ("Packages are installed/upgraded. "
                "Please re-launch the application manually.")


def ensure(**modules):
    try:
        for module in modules:
            __import__(module)
    except ImportError:
        with NamedTemporaryFile(mode="w",
                                encoding="ascii",
                                errors="replace",
                                prefix="pip-install-",
                                suffix=".log",
                                delete=False) as fp:
            system(f'open "{fp.name}"')

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
            fp.name,
        ) + tuple(modules.values())
        check_call(cmd)
        raise PackagesInstalled()
