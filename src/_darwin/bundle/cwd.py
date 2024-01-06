'''
Created on 2023/12/09

@author: YouheiSakurai
'''
from os.path import dirname
from unittest import mock


def patch():
    app_bundle_location = dirname(
        __file__.rsplit(".app/Contents/MacOS/", maxsplit=1)[0])
    mock.patch("os.getcwd", return_value=app_bundle_location).start()
