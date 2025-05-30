import threading, time, math

import dearpygui.dearpygui as dpg
from pynput import keyboard, mouse

from control import logging, detection, device_lock
from config import config, constants
from util import inputs, duration, passphrase_utils
from gui.widgets import manual_lock

auto_unlock_timer_on = False

def start_auto_unlock_timer_if_enabled():
    global auto_unlock_timer_on
    
    # Catch rare edge case where multiple timers can be started 
    # if a BadUSB is detected after a manual lock was activated.
    if config.instance.auto_unlock_enabled and not auto_unlock_timer_on:
        auto_unlock_timer_on = True
        auto_unlock_timer_thread = threading.Thread(target=auto_unlock_timer, daemon=True)
        auto_unlock_timer_thread.start()

def stop_auto_unlock_timer():
    global auto_unlock_timer_on

    auto_unlock_timer_on = False

# Only reads, so probably fine if not thread-safe.
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
                    val = dpg.get_value("passphrase_input")
                    dpg.set_value("passphrase_input", (val or "") + key.char)
            except AttributeError:
                pass
    
    inputs.set_kb_on_press(on_press)
    inputs.set_kb_on_release(None)
    inputs.disable_hotkey_listening()
    
    manual_lock.passphrase_prompt()
    start_auto_unlock_timer_if_enabled()
    
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
    global mouse_lock_active
    
    inputs.set_mouse_suppression(True)
    inputs.set_mouse_on_click(device_lock.passphrase_challenge)
    logging.log_generic("Locked Mouse")
    
    manual_lock.passphrase_prompt()
    start_auto_unlock_timer_if_enabled()
    
    dpg.configure_item("primary_window", show=False)
    dpg.set_primary_window("passphrase_prompt", value=True)
    dpg.configure_viewport(0, always_on_top=True, decorated=False)
    
    original_pos = dpg.get_viewport_pos()
    original_width = dpg.get_viewport_width()
    original_height = dpg.get_viewport_height()
    dpg.maximize_viewport()
    
    if dpg.does_item_exist("passphrase_input"):
        dpg.focus_item("passphrase_input")
    
    # `mouse_lock_target` must run in a separate thread or it can't determine 
    # the correct position of the submit button.
    # This isn't significant, since the submit button itself is not providing the call 
    # to `device_lock.passphrase_challenge` anymore, but it's nicer from a UI perspective.
    mouse_lock_active = True
    mouse_lock_thread = threading.Thread(
        target=mouse_lock_target, args=(original_pos, original_width, original_height), daemon=True
    )
    mouse_lock_thread.start()

def unlock_mouse():
    global mouse_lock_active
    
    inputs.set_mouse_suppression(False)
    inputs.set_mouse_on_click(None)
    logging.log_generic("Unlocked Mouse")
    
    manual_lock.close_passphrase_prompt()
    
    dpg.configure_item("primary_window", show=True)
    dpg.set_primary_window("primary_window", value=True)
    dpg.configure_viewport(0, always_on_top=False, decorated=True)
    
    mouse_lock_active = False

# This isn't actually needed, but the newer mouse suppression implementation 
# is finicky, so we can keep it around just in case.
mouse_lock_active = False

# Only reads, so probably fine if not thread-safe.
def mouse_lock_target(original_pos, original_width, original_height):
    global mouse_lock_active
    
    # Calculate the position of the unlock button.
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
    pos[0] = math.floor(pos[0])
    pos[1] = math.floor(pos[1])
    
    dpg.configure_viewport(
        0, 
        x_pos=original_pos[0], 
        y_pos=original_pos[1], 
        width=original_width, 
        height=original_height
    )
    
    m = mouse.Controller()
    # while mouse_lock_active:
    #     if m.position[0] == pos[0] and m.position[1] == pos[1]:
    #         time.sleep(0)
    #     else:
    #         m.position = pos
    m.position = pos

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

    if not passphrase_utils.is_valid_passphrase(passphrase_1):
        manual_lock.invalid_passphrase_window(
f"""Passphrase characters must be a
part of this character set:
\"{constants.VALID_PASSPHRASE_CHARACTERS}\""""
        )
        return
    
    passphrase_utils.set_passphrase(passphrase_1)
    config.save()
    manual_lock.close_set_passphrase_window()

def passphrase_challenge():
    if not config.instance.passphrase_enabled:
        unlock_all()
        return
    
    passphrase = dpg.get_value("passphrase_input")
    hash = passphrase_utils.hash_scrypt(passphrase)
    if hash != config.instance.passphrase_hash:
        manual_lock.incorrect_passphrase_notice()
        dpg.set_value("passphrase_input", "")
        dpg.focus_item("passphrase_input")
        return
    
    unlock_all()
