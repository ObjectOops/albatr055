import time, pathlib

from config import config, constants
from ui.widgets import key_log
from control import logging

keystroke_log = []

def toggle_logging():
    config.instance.log_keystrokes = True
    config.save()

def log_key_down(key):
    global keystroke_log
    if log_enabled():
        line = f"{key} down"
        keystroke_log.append(line)
        key_log.log(line)

def log_key_up(key):
    global keystroke_log
    if log_enabled():
        line = f"{key} up"
        keystroke_log.append(line)
        key_log.log(line)

def log_badusb(note):
    global keystroke_log
    if log_enabled():
        line = f"BadUSB Detected | {note}"
        keystroke_log.append(line)
        key_log.log(line)

def log_generic(msg):
    global keystroke_log
    keystroke_log.append(msg)
    key_log.log(msg)

def log_enabled():
    return config.instance.log_keystrokes or config.instance.log_keystrokes_override

def export_log(_, path_data):
    current_time = int(time.time())
    path = pathlib.Path(path_data["file_path_name"]) / f"{constants.APP_TITLE.lower()}_{current_time}.log"
    with open(path, "w") as writer:
        for keystroke in logging.keystroke_log:
            writer.write(f"{keystroke}\n")
