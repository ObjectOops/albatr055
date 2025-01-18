import dearpygui.dearpygui as dpg

from controls import device_lock

def show():
    dpg.add_text("« MANUAL LOCK »")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Lock Keyboard", callback=device_lock.lock_keyboard)
        dpg.add_button(label="Lock Mouse", callback=device_lock.lock_mouse)
        dpg.add_button(label="Set Unlock Passphrase", callback=device_lock.set_passphrase)
