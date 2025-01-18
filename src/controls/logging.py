import dearpygui.dearpygui as dpg

from config.init_file import Config, save

def toggle_logging():
    Config.instance.log_keystrokes = True
    save()

keystrokes = []

def log_key_down(key):
    global keystrokes
    if Config.instance.log_keystrokes:
        line = f"{key} down"
        keystrokes.append(line)
        log(line)

def log_key_up(key):
    global keystrokes
    if Config.instance.log_keystrokes:
        line = f"{key} up"
        keystrokes.append(line)
        log(line)

def log(line):
    dpg.configure_item("log_entry", tracked=False)
    dpg.remove_alias("log_entry")
    dpg.add_text(line, tag="log_entry", parent="keystroke_log", tracked=dpg.get_value("autoscroll"))
