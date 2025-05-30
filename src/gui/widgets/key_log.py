import dearpygui.dearpygui as dpg

from config import config, constants
from control import logging
from gui import gui

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
    if not gui.alive:
        # Only show the log in the GUI when the GUI is up.
        # Effect: Do not show the log in the GUI when running as a daemon.
        return
    
    dpg.configure_item("log_entry", tracked=False)
    dpg.remove_alias("log_entry")
    dpg.add_text(line, tag="log_entry", parent="keystroke_log", tracked=dpg.get_value("autoscroll"))

def export_dialog():
    with dpg.file_dialog(
        label="Select Folder",
        directory_selector=True,
        modal=True,
        width=800,
        height=400,
        callback=logging.export_log
    ):
        # Opening shortcuts on Windows in the file dialog 
        # causes the app to crash without exceptions.
        # Unresolved Dear PyGui issue: https://github.com/hoffstadt/DearPyGui/issues/1351
        file_dialog_msg = "A log file will be automatically exported to the selected folder.\nNOTICE: Do not navigate to directories that require higher permissions. This will cause the app to crash."
        if constants.PLATFORM_NAME == "Windows":
            file_dialog_msg += "\nAlso, do not open shortcuts that may appear (i.e. \"My Documents\")."
        with dpg.child_window() as child:
            dpg.add_text(file_dialog_msg, wrap=dpg.get_item_width(child))
