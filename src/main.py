import dearpygui.dearpygui as dpg

from ui import windows, theme
from config import init_file
from controls import detection

def main():
    dpg.create_context()
    
    init_file.load()
    theme.set_global_theme()
    windows.create_viewport()
    windows.primary_window()
    detection.start_detection_if_active()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    
    init_file.save()
    
    dpg.destroy_context()

if __name__ == "__main__":
    main()
