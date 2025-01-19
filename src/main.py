import dearpygui.dearpygui as dpg

from config import config
from ui import windows, theme
from control import detection

def main():
    dpg.create_context()
    
    config.load()
    theme.set_global_theme()
    windows.create_viewport()
    windows.primary_window()
    detection.start_if_active()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    
    config.save()
    
    dpg.destroy_context()

if __name__ == "__main__":
    main()
