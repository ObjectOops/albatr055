import dearpygui.dearpygui as dpg

from config import config
from control import logging

def widget():
    dpg.add_text("« LOGGING »")
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Log Keytrokes",
                default_value=config.instance.log_keystrokes,
                callback=logging.toggle_logging
            )
            dpg.add_checkbox(
                label="Autoscroll",
                tag="autoscroll",
                default_value=True,
                callback=toggle_auto_scroll
            )
        with dpg.child_window(tag="keystroke_log", height=200):
            dpg.add_text("Log", tag="log_entry")
        dpg.add_button(label="Export Log", callback=export_dialog)

def toggle_auto_scroll(_, checkbox):
    dpg.configure_item("log_entry", tracked=checkbox)

def log(line):
    dpg.configure_item("log_entry", tracked=False)
    dpg.remove_alias("log_entry")
    dpg.add_text(line, tag="log_entry", parent="keystroke_log", tracked=dpg.get_value("autoscroll"))

def export_dialog():    
    dpg.add_file_dialog(
        label="Select Folder",
        directory_selector=True,
        modal=True,
        width=400,
        height=200,
        callback=logging.export_log
    )
