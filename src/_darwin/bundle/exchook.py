'''
Created on 2023/12/19

@author: YouheiSakurai
'''
from functools import partial
from itertools import chain
from os import environ
from os import system
from subprocess import check_output
from sys import executable
from tempfile import NamedTemporaryFile
from traceback import print_exception


def mod_info(modname, attrs):
    try:
        mod = __import__(modname)
    except Exception as e:
        yield f"{modname} {e}"
    else:
        for name in attrs.split():
            attr = getattr(mod, name, None)
            if callable(attr):
                try:
                    yield f"{modname}.{name}()={attr()}"
                except Exception as e:
                    yield f"{modname}.{name}()={e}"
            else:
                yield f"{modname}.{name}={attr}"


def pip_freeze():
    try:
        yield from check_output((executable, "-m", "pip", "freeze"),
                                encoding="ascii",
                                errors=r"replace").splitlines()
    except Exception as e:
        yield f"pip freeze {e}"


def excepthook(exc, value, tb):
    with NamedTemporaryFile(mode="w",
                            encoding="ascii",
                            errors="replace",
                            prefix="py-excepthook-",
                            suffix=".log",
                            delete=False) as fp:
        system(f'open "{fp.name}"')

        print_exception(exc, value, tb, file=fp)
        print_fp = partial(print, file=fp)

        print_fp("== Environment variables")
        for key in environ:
            print_fp(" ", f"{key}={environ[key]}")

        print_fp("== Python packages")
        for package in pip_freeze():
            print_fp(" ", package)

        print_fp("== Misc. information")
        for info in chain(
            mod_info("sys", "argv executable path platform version"),
            mod_info("os", "getcwd getegid geteuid getgid getgroups"),
            mod_info("os", "getlogin getpgrp getpid getppid"),
            mod_info("os", "getresuid getresgid getuid uname"),
            mod_info("platform", "platform uname"),
            mod_info("getpass", "getuser"),
        ):
            print_fp(" ", info)
