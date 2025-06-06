import ctypes

import dearpygui.dearpygui as dpg

from config import config, constants
from gui import windows, theme
from util import cli

alive = False
exit_event = None

def start(immediate_actions=lambda: None, post_actions=lambda: None):
    global alive, exit_event
    
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
    
    alive = True
    dpg.start_dearpygui() # Main event loop.
    alive = False
    
    config.save() # Requires GUI size and position; must be called here.
    
    dpg.destroy_context()
    
    post_actions()
    if exit_event is not None:
        exit_event.set()

def exit_background(event):
    global exit_event
    
    exit_event = event
    dpg.stop_dearpygui()

def add_exit_background(event):
    if event is None:
        # `event` should not be `None`, but this behavior is defined just in case.
        return
    dpg.add_separator(parent="primary_window")
    dpg.add_button(
        label="Exit Background", parent="primary_window", callback=lambda: exit_background(event)
    )

def save_error():
    if alive:
        with dpg.window(label="Error"):
            dpg.add_text("Could not save to disk.")
    else:
        dpg.destroy_context() # Destroy existing context.
        dpg.create_context()
        
        theme.set_global_theme()
        windows.create_viewport()
        
        with dpg.window() as window:
            dpg.set_primary_window(window, True)
            dpg.add_text("Error: Could not save to disk.")
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui() # Will be destroyed by call usually intended for former context.

def configure_platform():
    if constants.PLATFORM_NAME == "Windows":
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
