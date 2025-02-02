import dearpygui.dearpygui as dpg

from util import duration
from control import device_lock, detection
from config import config

def widget():
    dpg.add_text("« MANUAL LOCK »")
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_button(label="Lock Keyboard", callback=device_lock.lock_keyboard)
            dpg.add_button(label="Lock Mouse", callback=device_lock.lock_mouse)
        with dpg.collapsing_header(label="More"):
            dpg.add_button(label="Set Unlock Passphrase", callback=set_passphrase_window)
            with dpg.group(horizontal=True):
                dpg.add_text("Auto Unlock Duration (HH/MM/SS): ")
                dpg.add_time_picker(
                    default_value=duration.to_hms(config.instance.auto_unlock_duration),
                    hour24=True,
                    callback=detection.change_auto_unlock_duration
                )
            dpg.add_checkbox(
                label="Enable Auto Unlock Timer",
                default_value=config.instance.auto_unlock_enabled,
                callback=detection.toggle_auto_unlock_enabled
            )

def set_passphrase_window():
    if dpg.does_item_exist("set_passphrase_prompt"):
        return
        
    with dpg.window(
        label="Set Passphrase",
        tag="set_passphrase_prompt",
        no_collapse=True,
        no_close=True,
        modal=True,
        width=650,
        height=300,
        pos=[25, 25]
    ):
        dpg.add_input_text(
            tag="passphrase_input_1",
            hint="Leave empty for no passphrase.",
            password=True,
            on_enter=True,
            callback=device_lock.set_passphrase
        )
        dpg.add_input_text(
            tag="passphrase_input_2",
            hint="Confirm passphrase.",
            password=True,
            on_enter=True,
            callback=device_lock.set_passphrase
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Confirm", callback=device_lock.set_passphrase)
            dpg.add_button(label="Cancel", callback=close_set_passphrase_window)

def invalid_passphrase_window(text):
    if not dpg.does_item_exist("passphrase_notice"):
        dpg.add_text(
            text,
            tag="passphrase_notice",
            parent="set_passphrase_prompt"
        )

def close_set_passphrase_window():
    dpg.delete_item("set_passphrase_prompt")

def passphrase_prompt():
    if dpg.does_item_exist("passphrase_prompt"):
        return
    
    with dpg.window(
        tag="passphrase_prompt",
        no_close=True,
        no_move=True,
        width=620,
        height=207,
        pos=(0, 0)
    ):
        dpg.add_text("Input Locked")
        if config.instance.passphrase_enabled:
            dpg.add_text("« Enter Passphrase »")
            dpg.add_input_text(
                tag="passphrase_input",
                password=True,
                on_enter=True,
                callback=device_lock.passphrase_challenge
            )
            dpg.add_button(
                label="Submit",
                tag="unlock_button",
                callback=device_lock.passphrase_challenge
            )
        else:
            dpg.add_button(
                label="Unlock",
                tag="unlock_button",
                callback=device_lock.passphrase_challenge
            )

def incorrect_passphrase_notice():
    if not dpg.does_item_exist("challenge_notice"):
        dpg.add_text(
            "Incorrect passphrase.",
            tag="challenge_notice",
            parent="passphrase_prompt"
        )

def close_passphrase_prompt():
    dpg.delete_item("passphrase_prompt")
