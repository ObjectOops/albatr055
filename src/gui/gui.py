import ctypes

import dearpygui.dearpygui as dpg

from config import config, constants
from gui import windows, theme
from util import cli

def start(immediate_actions=lambda: None, post_actions=lambda: None):
    configure_platform()
    dpg.create_context()
    
    theme.set_global_theme()
    windows.create_viewport()
    windows.primary_window()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    
    # Two different sets of "immediate actions" that are performed after everything else, 
    # but before the main event loop starts.
    cli.immediate_actions()
    immediate_actions()
    
    dpg.start_dearpygui() # Main event loop.
    
    config.save() # Requires GUI size and position; must be called here.
    
    dpg.destroy_context()
    
    post_actions()

def exit_background(event):
    dpg.stop_dearpygui()
    dpg.destroy_context()
    event.set()

def add_exit_background(event):
    if event is None:
        # `event` should not be `None`, but this behavior is defined just in case.
        return
    dpg.add_separator(parent="primary_window")
    dpg.add_button(
        label="Exit Background", parent="primary_window", callback=lambda: exit_background(event)
    )

def configure_platform():
    if constants.PLATFORM_NAME == "Windows":
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
