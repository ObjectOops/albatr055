import dearpygui.dearpygui as dpg

from config import constants, config
from gui.widgets import manual_lock, detect_params, key_log

def create_viewport():
    dpg.create_viewport(
        small_icon=constants.SMALL_ICON,
        title=constants.APP_TITLE,
        width=config.instance.viewport_width,
        height=config.instance.viewport_height,
        x_pos=config.instance.viewport_pos[0],
        y_pos=config.instance.viewport_pos[1]
    )

def primary_window():
    with dpg.window(tag="primary_window") as window:
        dpg.set_primary_window(window, True)
        
        dpg.add_spacer(height=15)
        manual_lock.widget()
        dpg.add_separator()
        detect_params.widget()
        dpg.add_separator()
        key_log.widget()
