import dearpygui.dearpygui as dpg

from config.init_file import Config
from controls import detection

def show():
    dpg.add_text("« DETECT BADUSB »")
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_checkbox(
                label="Active",
                default_value=Config.instance.detect_active,
                callback=detection.toggle_detection
            )
            dpg.add_checkbox(
                label="Lock mouse on detection",
                default_value=Config.instance.lock_mouse_on_detection,
                callback=detection.toggle_lock_mouse_on_detection
            )
        with dpg.collapsing_header(label="More"):
            dpg.add_input_float(
                label="Keys per second",
                default_value=Config.instance.kps,
                min_value=1.0,
                min_clamped=True,
                callback=detection.change_kps
            )
            dpg.add_input_int(
                label="Sample size",
                default_value=Config.instance.sample_size,
                min_value=1,
                min_clamped=True,
                callback=detection.change_sample_size
            )
            dpg.add_checkbox(
                label="Listen for suspicious hotkeys",
                default_value=Config.instance.listen_hotkeys,
                callback=detection.toggle_listen_hotkeys
            )
            dpg.add_checkbox(
                label="Ignore recurring keystrokes",
                default_value=Config.instance.ignore_recur,
                callback=detection.toggle_ignore_recur
            )
            dpg.add_checkbox(
                label="Log keystrokes on detection",
                default_value=Config.instance.log_on_detection,
                callback=detection.toggle_log_on_detection
            )
