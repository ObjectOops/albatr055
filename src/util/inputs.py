from pynput import keyboard, mouse

from control import logging
from config import config

kb_on_press_callback = None
kb_on_release_callback = None

def keyboard_on_press(key):
    global kb_on_press_callback
    logging.log_key_down(key)
    if kb_on_press_callback is not None:
        kb_on_press_callback(key)

def keyboard_on_release(key):
    global kb_on_release_callback
    logging.log_key_up(key)
    if kb_on_release_callback is not None:
        kb_on_release_callback(key)

def set_kb_on_press(callback):
    global kb_on_press_callback
    kb_on_press_callback = callback

def set_kb_on_release(callback):
    global kb_on_release_callback
    kb_on_release_callback = callback

keyboard_listener = keyboard.Listener(
    on_press=keyboard_on_press,
    on_release=keyboard_on_release,
    suppress=False
)
keyboard_listener.start()

def set_kb_suppression(suppress):
    global keyboard_listener
    keyboard_listener._suppress = suppress # Purposefully ignore "private" member.

hotkey_listener = None

def enable_hotkey_listening(callback):
    global hotkey_listener
    hotkey_map = dict()
    for hotkey in config.instance.hotkey_blacklist:
        hotkey_map[hotkey] = lambda hotkey=hotkey: callback(f"Hotkey: {hotkey}")

    disable_hotkey_listening()
    hotkey_listener = keyboard.GlobalHotKeys(hotkey_map)
    hotkey_listener.start()

def disable_hotkey_listening():
    global hotkey_listener
    if hotkey_listener is not None:
        hotkey_listener.stop()
    hotkey_listener = None

mouse_on_move_callback = None

def set_mouse_on_move(callback):
    global mouse_on_move_callback
    mouse_on_move_callback = callback

def mouse_on_move(x, y):
    global mouse_on_move_callback
    if mouse_on_move_callback is not None:
        mouse_on_move_callback(x, y)

mouse_listener = mouse.Listener(
    on_move=mouse_on_move
)
mouse_listener.start()
