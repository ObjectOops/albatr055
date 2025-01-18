import time, pathlib

import dearpygui.dearpygui as dpg

from config.init_file import Config, save
from config.constants import APP_TITLE
from controls import logging

def toggle_logging():
    Config.instance.log_keystrokes = True
    save()

keystrokes = []

def log_key_down(key):
    global keystrokes
    if Config.instance.log_keystrokes or Config.instance.logging_override:
        line = f"{key} down"
        keystrokes.append(line)
        log(line)

def log_key_up(key):
    global keystrokes
    if Config.instance.log_keystrokes or Config.instance.logging_override:
        line = f"{key} up"
        keystrokes.append(line)
        log(line)

def log(line):
    dpg.configure_item("log_entry", tracked=False)
    dpg.remove_alias("log_entry")
    dpg.add_text(line, tag="log_entry", parent="keystroke_log", tracked=dpg.get_value("autoscroll"))

def export_log():
    def export_log_file(sender, app_data):
        current_time = int(time.time())
        path = pathlib.Path(app_data["file_path_name"]) / f"{APP_TITLE.lower()}_log_{current_time}.log"
        with open(path, "w") as writer:
            for keystroke in logging.keystrokes:
                writer.write(f"{keystroke}\n")
    
    dpg.add_file_dialog(
        label="Select Folder",
        directory_selector=True,
        modal=True,
        width=400,
        height=200,
        callback=export_log_file
    )
