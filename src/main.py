import ctypes

import dearpygui.dearpygui as dpg

from util import cli
from config import config, constants
from ui import windows, theme
from control import detection, device_lock

def main():
    cli.init_cli()
    configure_platform()
    
    dpg.create_context()
    
    config.load()
    theme.set_global_theme()
    windows.create_viewport()
    windows.primary_window()
    detection.start_if_active()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    
    immediate_actions()
    
    dpg.start_dearpygui()
    
    config.save()
    
    dpg.destroy_context()

def configure_platform():
    if constants.PLATFORM_NAME == "Windows":
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

def immediate_actions():
    if cli.args.lock == "keyboard":
        device_lock.lock_keyboard()
    elif cli.args.lock == "mouse":
        device_lock.lock_mouse()
    elif cli.args.lock == "all":
        device_lock.lock_keyboard()
        device_lock.lock_mouse()

if __name__ == "__main__":
    main()
