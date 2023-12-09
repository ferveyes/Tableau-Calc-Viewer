'''
Created on 2023/12/09

@author: YouheiSakurai
'''
from pynput import keyboard as _keyboard


_pressed = set()
_listener = _keyboard.Listener(on_press=_pressed.add,
                               on_release=_pressed.discard)
_listener.start()


def is_pressed(key: str):
    return getattr(_keyboard.Key, key.lower()) in _pressed
