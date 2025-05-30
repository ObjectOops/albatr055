import time, threading

from config import config
from control import logging, device_lock, detection
from util import inputs, duration
from gui import gui

def toggle_detection(_, toggle):
    config.instance.detection_active = toggle
    if toggle:
        start_detection()
    else:
        stop_detection()
    config.save()

def toggle_lock_mouse_on_detection(_, toggle):
    config.instance.lock_mouse_on_detection = toggle
    config.save()

def change_kps(_, value):
    config.instance.kps_threshold = value
    config.save()

def change_sample_size(_, value):
    global keystroke_watch
    keystroke_watch.clear()
    
    config.instance.sample_size = value
    config.save()

def toggle_listen_hotkeys(_, toggle):
    config.instance.listen_hotkeys = toggle
    config.save()

def toggle_ignore_recurring(_, toggle):
    config.instance.ignore_recurring = toggle
    config.save()

def toggle_log_on_detection(_, toggle):
    config.instance.log_on_detection = toggle
    config.save()

keystroke_watch = []
def start_detection(event=None):
    global keystroke_watch
    
    def on_press(key):
        count = len(keystroke_watch)
        if not (config.instance.ignore_recurring and count > 0 and key == keystroke_watch[-1][0]):
            current_time = time.time_ns()
            keystroke_watch.append((key, current_time))
            count += 1
        if count >= config.instance.sample_size:
            first = keystroke_watch.pop(0)[1]
            last = keystroke_watch[-1][1]
            delta = last - first
            if delta == 0:
                badusb_detected(f"KPS: div. zero error", event)
                return
            kps = config.instance.sample_size / delta * (10 ** 9)
            if kps >= config.instance.kps_threshold:
                badusb_detected(f"KPS: {kps}", event)
    
    if config.instance.listen_hotkeys:
        inputs.enable_hotkey_listening(lambda note: badusb_detected(note, event))
    
    inputs.set_kb_on_press(on_press)

def start_if_active():
    if config.instance.detection_active:
        start_detection()

def stop_detection():
    inputs.set_kb_on_press(None)
    inputs.disable_hotkey_listening()

def badusb_detected(note, event=None):
    def action():
        device_lock.lock_keyboard()
        if config.instance.lock_mouse_on_detection:
            device_lock.lock_mouse()
        if config.instance.log_on_detection:
            config.instance.log_keystrokes_override = True
            logging.log_badusb(note)
    
    if config.instance.is_daemon:
        config.instance.is_daemon = False # No longer a daemon once GUI starts.
        inputs.set_kb_suppression(True) # GUI takes time to load, so suppress input immediately.
        def immediate_action():
            action()
            gui.add_exit_background(event)
        def post_action():
            detection.start_detection(event)
            config.instance.is_daemon = True # Returns to being a daemon when GUI is closed.
        gui_thread = threading.Thread(
            target=gui.start, 
            args=(immediate_action, post_action), 
            daemon=True
        )
        gui_thread.start()
    else:
        action()

def change_auto_unlock_duration(_, value):
    config.instance.auto_unlock_duration = duration.from_hms(value)
    config.save()

def toggle_auto_unlock_enabled(_, toggle):
    config.instance.auto_unlock_enabled = toggle
    config.save()
