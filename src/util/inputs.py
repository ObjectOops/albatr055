from pynput import keyboard

active_keyboard_listener = None

def set_keyboard_listener(listener):
    global active_keyboard_listener
    if active_keyboard_listener != None:
        active_keyboard_listener.stop()
    active_keyboard_listener = listener
    if active_keyboard_listener != None:
        active_keyboard_listener.start()

active_mouse_listener = None

def set_mouse_listener(listener):
    raise NotImplementedError()
    # global active_mouse_listener
    # if active_mouse_listener != None:
    #     active_mouse_listener.stop()
    # active_mouse_listener = listener
    # if active_mouse_listener != None:
    #     active_mouse_listener.start()
