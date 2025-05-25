import threading, time, math

import dearpygui.dearpygui as dpg
from pynput import keyboard, mouse

from control import logging, detection
from config import config, constants
from util import passphrase_hash, inputs, duration
from ui.widgets import manual_lock

auto_unlock_timer_on = False
auto_unlock_timer_thread = None

def start_auto_unlock_timer():
    global auto_unlock_timer_on, auto_unlock_timer_thread

    if config.instance.auto_unlock_enabled:
        auto_unlock_timer_on = True
        auto_unlock_timer_thread = threading.Thread(target=auto_unlock_timer)
        auto_unlock_timer_thread.start()

def stop_auto_unlock_timer():
    global auto_unlock_timer_on, auto_unlock_timer_thread

    if config.instance.auto_unlock_enabled:
        auto_unlock_timer_on = False

def auto_unlock_timer():
    global auto_unlock_timer_on
    
    duration_remaining = config.instance.auto_unlock_duration
    while auto_unlock_timer_on:
        dpg.set_value("auto_unlock_timer_widget", duration.to_hms(duration_remaining))
        duration_remaining -= 1
        time.sleep(1)
        if duration_remaining <= 0:
            unlock_all()
            break

def unlock_all():
    stop_auto_unlock_timer()
    
    unlock_keyboard()
    unlock_mouse()

def lock_keyboard():
    inputs.set_kb_suppression(True)
    logging.log_generic("Locked Keyboard")
    
    def on_press(key):
        if not config.instance.passphrase_enabled:
            if key == keyboard.Key.enter:
                passphrase_challenge()
            return
        if key == keyboard.Key.backspace:
            dpg.set_value("passphrase_input", dpg.get_value("passphrase_input")[:-1])
        elif key == keyboard.Key.enter:
            passphrase_challenge()
        else:
            try:
                if key.char is not None and key.char in constants.VALID_PASSPHRASE_CHARACTERS:
                    dpg.set_value("passphrase_input", dpg.get_value("passphrase_input") + key.char)
            except AttributeError:
                pass
    
    inputs.set_kb_on_press(on_press)
    inputs.set_kb_on_release(None)
    inputs.disable_hotkey_listening()
    
    manual_lock.passphrase_prompt()
    start_auto_unlock_timer()
    
    if config.instance.passphrase_enabled:
        dpg.configure_item("passphrase_input", readonly=True)

def unlock_keyboard():
    inputs.set_kb_suppression(False)
    logging.log_generic("Unlocked Keyboard")
    
    inputs.set_kb_on_press(None)
    inputs.set_kb_on_release(None)

    manual_lock.close_passphrase_prompt()
    
    if config.instance.detection_active:
        detection.start_detection()
    
    config.instance.log_keystrokes_override = False
    
    # Manually release the Win key. Otherwise, Windows pretends like it's still being held.
    controller = keyboard.Controller()
    controller.release(keyboard.Key.cmd)

def lock_mouse():
    logging.log_generic("Locked Mouse")
    
    manual_lock.passphrase_prompt()
    start_auto_unlock_timer()
    
    dpg.configure_item("primary_window", show=False)
    dpg.set_primary_window("passphrase_prompt", value=True)
    dpg.configure_viewport(0, always_on_top=True, decorated=False)
    
    original_pos = dpg.get_viewport_pos()
    original_width = dpg.get_viewport_width()
    original_height = dpg.get_viewport_height()
    dpg.maximize_viewport()
    
    if dpg.does_item_exist("passphrase_input"):
        dpg.focus_item("passphrase_input")
    
    while True:
        time.sleep(0)
        if not dpg.does_item_exist("unlock_button"):
            continue
        offset = dpg.get_item_pos("unlock_button")
        rect = dpg.get_item_rect_size("unlock_button")
        if offset != [0, 0] and rect != [0, 0]:
            break
    pos = dpg.get_viewport_pos()
    pos[0] += offset[0] + rect[0] / 2
    pos[1] += offset[1] + rect[1] / 2
    
    dpg.configure_viewport(
        0, 
        x_pos=original_pos[0], 
        y_pos=original_pos[1], 
        width=original_width, 
        height=original_height
    )
    
    mouse_controller = mouse.Controller()
    
    def on_move(x, y):
        print(x, y, pos)
        if x != math.floor(pos[0]) or y != math.floor(pos[1]):
            time.sleep(0.5)
            mouse_controller.position = pos
    
    inputs.set_mouse_on_move(on_move)
    on_move(0, 0)

def unlock_mouse():
    inputs.set_mouse_on_move(None)
    logging.log_generic("Unlocked Mouse")
    
    manual_lock.close_passphrase_prompt()
    
    dpg.configure_item("primary_window", show=True)
    dpg.set_primary_window("primary_window", value=True)
    dpg.configure_viewport(0, always_on_top=False, decorated=True)

def set_passphrase():
    passphrase_1 = dpg.get_value("passphrase_input_1")
    passphrase_2 = dpg.get_value("passphrase_input_2")

    if len(passphrase_1) == 0:
        config.instance.passphrase_enabled = False
        config.save()
        manual_lock.close_set_passphrase_window()
        return

    if passphrase_1 != passphrase_2:
        manual_lock.invalid_passphrase_window("Passphrases do not match.")
        return

    for character in passphrase_1:
        if character not in constants.VALID_PASSPHRASE_CHARACTERS:
            manual_lock.invalid_passphrase_window(
f"""Password characters must be a
part of this character set:
\"{constants.VALID_PASSPHRASE_CHARACTERS}\""""
            )
            return

    config.instance.passphrase_hash = passphrase_hash.hash(passphrase_1)
    config.instance.passphrase_enabled = True
    config.save()
    manual_lock.close_set_passphrase_window()

def passphrase_challenge():
    if not config.instance.passphrase_enabled:
        unlock_all()
        return
    
    passphrase = dpg.get_value("passphrase_input")
    hash = passphrase_hash.hash(passphrase)
    if hash != config.instance.passphrase_hash:
        manual_lock.incorrect_passphrase_notice()
        dpg.set_value("passphrase_input", "")
        dpg.focus_item("passphrase_input")
        return
    
    unlock_all()
