import time

from pynput import keyboard

from util import inputs
from controls import logging, device_lock
from config.init_file import Config, save

def toggle_detection(sender, app_data):
    Config.instance.detect_active = app_data
    if app_data:
        start_detection()
    else:
        stop_detection()
    save()

def toggle_lock_mouse_on_detection(sender, app_data):
    Config.instance.lock_mouse_on_detection = app_data
    save()

def change_kps(sender, app_data):
    Config.instance.kps = app_data
    save()

def change_sample_size(sender, app_data):
    Config.instance.sample_size = app_data
    save()

def toggle_listen_hotkeys(sender, app_data):
    Config.instance.listen_hotkeys = app_data
    save()

def toggle_ignore_recur(sender, app_data):
    Config.instance.ignore_recur = app_data
    save()

def toggle_log_on_detection(sender, app_data):
    Config.instance.log_on_detection = app_data
    save()

def start_detection():
    keystroke_watch = []
    
    def on_press(key):
        logging.log_key_down(key)
        
        if not (Config.instance.ignore_recur and key == keystroke_watch[-1]):
            current_time = time.time_ns()
            keystroke_watch.append(current_time)
        if len(keystroke_watch) > Config.instance.sample_size:
            keystroke_watch.pop(0)
            kps = Config.instance.sample_size / (keystroke_watch[-1] - keystroke_watch[0]) / 10 ** 9
            if kps >= Config.instance.kps:
                badusb_detected()
    
    if Config.instance.listen_hotkeys:
        hotkey_config = dict()
        for hotkey in Config.instance.hotkey_blacklist:
            hotkey_config[hotkey] = badusb_detected
        inputs.set_hotkey_listener(
            keyboard.GlobalHotKeys(hotkey_config)
        )
    inputs.set_keyboard_listener(
        keyboard.Listener(
            on_press=on_press,
            on_release=logging.log_key_up,
        )
    )

def start_detection_if_active():
    if Config.instance.detect_active:
        start_detection()

def stop_detection():
    inputs.set_keyboard_listener(None)
    inputs.set_hotkey_listener(None)
    
def badusb_detected():
    device_lock.lock_keyboard()
    if Config.instance.lock_mouse_on_detection:
        device_lock.lock_mouse()
    if Config.instance.log_on_detection:
        Config.instance.logging_override = True
