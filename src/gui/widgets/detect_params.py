import dearpygui.dearpygui as dpg

from config import config
from control import detection

def widget():
    dpg.add_text("« DETECT BADUSB »")
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Active",
                default_value=config.instance.detection_active,
                callback=detection.toggle_detection
            )
            dpg.add_checkbox(
                label="Lock mouse on detection",
                default_value=config.instance.lock_mouse_on_detection,
                callback=detection.toggle_lock_mouse_on_detection
            )
        with dpg.collapsing_header(label="More"):
            dpg.add_input_float(
                label="Keys per second",
                default_value=config.instance.kps_threshold,
                min_value=0.1,
                min_clamped=True,
                callback=detection.change_kps
            )
            dpg.add_input_int(
                label="Sample size",
                default_value=config.instance.sample_size,
                min_value=2,
                min_clamped=True,
                callback=detection.change_sample_size
            )
            dpg.add_checkbox(
                label="Listen for suspicious hotkeys",
                default_value=config.instance.listen_hotkeys,
                callback=detection.toggle_listen_hotkeys
            )
            dpg.add_checkbox(
                label="Ignore recurring keystrokes",
                default_value=config.instance.ignore_recurring,
                callback=detection.toggle_ignore_recurring
            )
            dpg.add_checkbox(
                label="Log keystrokes on detection",
                default_value=config.instance.log_on_detection,
                callback=detection.toggle_log_on_detection
            )
