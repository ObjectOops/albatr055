import dearpygui.dearpygui as dpg
from pynput import keyboard, mouse

from control import logging, detection
from config import config
from util import passphrase_hash
from ui.widgets import manual_lock
from util import inputs

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
                dpg.set_value("passphrase_input", dpg.get_value("passphrase_input") + key.char)
            except AttributeError:
                pass
    
    inputs.set_kb_on_press(on_press)
    inputs.set_kb_on_release(None)
    inputs.disable_hotkey_listening()
    
    manual_lock.passphrase_prompt()
    
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
    # TODO: Implement when pynput library developer publishes a fix.
    
    manual_lock.passphrase_prompt()
    
    dpg.configure_item("primary_window", show=False)
    dpg.set_primary_window("passphrase_prompt", value=True)
    dpg.configure_viewport(0, always_on_top=True, decorated=False)

def unlock_mouse():
    # TODO: Implement when pynput library developer publishes a fix.
    
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

    valid_characters = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    for character in passphrase_1:
        if character not in valid_characters:
            manual_lock.invalid_passphrase_window(
                f"Password characters must be a part of this character set:\n\"{valid_characters}\""
            )
            return

    config.instance.passphrase_hash = passphrase_hash.hash(passphrase_1)
    config.instance.passphrase_enabled = True
    config.save()
    manual_lock.close_set_passphrase_window()

def passphrase_challenge():
    if not config.instance.passphrase_enabled:
        unlock_keyboard()
        unlock_mouse()
        return
    
    passphrase = dpg.get_value("passphrase_input")
    hash = passphrase_hash.hash(passphrase)
    if hash != config.instance.passphrase_hash:
        manual_lock.incorrect_passphrase_notice()
        return
    
    unlock_keyboard()
    unlock_mouse()

