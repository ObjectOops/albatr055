import threading, queue

from pynput import keyboard, mouse

from control import logging
from config import config

kb_on_press_callback = None
kb_on_release_callback = None
key_down_queue = queue.Queue()
key_up_queue = queue.Queue()

def keyboard_on_press(key):
    global key_down_queue
    key_down_queue.put(key)

def keyboard_on_release(key):
    global key_up_queue
    key_up_queue.put(key)

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

def set_kb_suppression(suppress):
    global keyboard_listener
    keyboard_listener._suppress = suppress # Purposefully ignore "private" member.

def key_down_consumer():
    global key_down_queue, kb_on_press_callback
    while True:
        key = key_down_queue.get()
        logging.log_key_down(key)
        if kb_on_press_callback is not None:
            kb_on_press_callback(key)
        key_down_queue.task_done()

def key_up_consumer():
    global key_up_queue, kb_on_release_callback
    while True:
        key = key_up_queue.get()
        logging.log_key_up(key)
        if kb_on_release_callback is not None:
            kb_on_release_callback(key)
        key_up_queue.task_done()

key_down_consumer_thread = threading.Thread(target=key_down_consumer, daemon=True)
key_up_consumer_thread = threading.Thread(target=key_up_consumer, daemon=True)

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

mouse_on_click_callback = None
mouse_event_queue = queue.Queue()

def set_mouse_on_click(callback):
    global mouse_on_click_callback
    mouse_on_click_callback = callback

def mouse_on_click(_):
    # The specific mouse event data does not matter.
    global mouse_event_queue
    mouse_event_queue.put(True)

mouse_listener = mouse.Listener(
    on_click=mouse_on_click
)

def set_mouse_suppression(suppress):
    global mouse_listener
    mouse_listener._suppress = suppress # Purposefully ignore "private" member.

def mouse_consumer():
    global mouse_event_queue, mouse_on_click_callback
    while True:
        mouse_event_queue.get()
        if mouse_on_click_callback is not None:
            mouse_on_click_callback()
        mouse_event_queue.task_done()

mouse_consumer_thread = threading.Thread(target=mouse_consumer, daemon=True)

def start_workers():
    global keyboard_listener, mouse_listener
    global key_down_consumer_thread, key_up_consumer_thread, mouse_consumer_thread
    
    keyboard_listener.start()
    key_down_consumer_thread.start()
    key_up_consumer_thread.start()
    mouse_listener.start()
    mouse_consumer_thread.start()
    
    keyboard_listener.wait()
    mouse_listener.wait()
