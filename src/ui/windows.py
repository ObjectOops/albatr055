import dearpygui.dearpygui as dpg

from config.constants import APP_TITLE
from config.init_file import Config
from ui.widgets import manual_lock, detect_badusb, log_keys

def create_viewport():
    dpg.create_viewport(
        title=APP_TITLE,
        width=Config.instance.viewport_width,
        height=Config.instance.viewport_height,
        x_pos=Config.instance.viewport_pos[0],
        y_pos=Config.instance.viewport_pos[1]
    )

def primary_window():
    with dpg.window(tag="primary_window") as window:
        dpg.set_primary_window(window, True)
        
        dpg.add_spacer(height=15)
        manual_lock.show()
        dpg.add_separator()
        detect_badusb.show()
        dpg.add_separator()
        log_keys.show()
