import dearpygui.dearpygui as dpg

from config.init_file import Config
from controls import logging

def show():
    dpg.add_text("« LOGGING »")
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Log Keytrokes",
                default_value=Config.instance.log_keystrokes,
                callback=logging.toggle_logging
            )
            def toggle_auto_scroll(sender, app_data):
                dpg.configure_item("log_entry", tracked=app_data)
            dpg.add_checkbox(
                label="Autoscroll",
                tag="autoscroll",
                default_value=True,
                callback=toggle_auto_scroll
            )
        with dpg.child_window(tag="keystroke_log", height=200):
            dpg.add_text("Log", tag="log_entry")
        dpg.add_button(label="Export Log")
