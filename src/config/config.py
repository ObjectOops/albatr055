import configparser

import dearpygui.dearpygui as dpg

from config.constants import INIT_DEFAULTS, Keys
from util import cli
from gui import gui

def load():
    global instance
    config_parser = configparser.ConfigParser()
    config_parser.read_dict(INIT_DEFAULTS)
    config_parser.read(cli.args.config_file)
    instance = Config(config_parser)

def save():
    global instance
    
    if cli.ephemeral_mode:
        # If in ephemeral mode, do not save to the config file.
        return
    
    config_writer = instance.config_parser
    config_writer[Keys.viewport.NAME] = {
        Keys.viewport.WIDTH: dpg.get_viewport_width(),
        Keys.viewport.HEIGHT: dpg.get_viewport_height(),
        Keys.viewport.POS: dpg.get_viewport_pos()
    }
    config_writer[Keys.detection.NAME] = {
        Keys.detection.ACTIVE: instance.detection_active,
        Keys.detection.LOCK_MOUSE_ON_DETECTION: instance.lock_mouse_on_detection,
        Keys.detection.KEYS_PER_SECOND: instance.kps_threshold,
        Keys.detection.SAMPLE_SIZE: instance.sample_size,
        Keys.detection.LISTEN_HOTKEYS: instance.listen_hotkeys,
        Keys.detection.IGNORE_RECURRING: instance.ignore_recurring,
        Keys.detection.LOG_ON_DETECTION: instance.log_on_detection
    }
    config_writer[Keys.logging.NAME] = {
        Keys.logging.LOG_KEYSTROKES: instance.log_keystrokes
    }
    config_writer[Keys.passphrase.NAME] = {
        Keys.passphrase.HASH: instance.passphrase_hash,
        Keys.passphrase.ENABLE: instance.passphrase_enabled,
        Keys.passphrase.AUTO_UNLOCK_DURATION: instance.auto_unlock_duration,
        Keys.passphrase.AUTO_UNLOCK_ENABLE: instance.auto_unlock_enabled
    }
    
    try:
        with open(cli.args.config_file, "w") as config_file:
            config_writer.write(config_file)
    except:
        gui.save_error()

class Config:
    def __init__(self, config_parser):
        self.config_parser = config_parser
        self.is_daemon = cli.args.background and cli.args.relaunched
        
        viewport = config_parser[Keys.viewport.NAME]
        self.viewport_width = viewport.getint(Keys.viewport.WIDTH)
        self.viewport_height = viewport.getint(Keys.viewport.HEIGHT)
        self.viewport_pos = [int(i) for i in viewport[Keys.viewport.POS][1:-1].split(", ")]
        
        detection = config_parser[Keys.detection.NAME]
        self.detection_active = detection.getboolean(Keys.detection.ACTIVE)
        self.lock_mouse_on_detection = detection.getboolean(Keys.detection.LOCK_MOUSE_ON_DETECTION)
        self.kps_threshold = detection.getfloat(Keys.detection.KEYS_PER_SECOND)
        self.sample_size = detection.getint(Keys.detection.SAMPLE_SIZE)
        self.listen_hotkeys = detection.getboolean(Keys.detection.LISTEN_HOTKEYS)
        self.ignore_recurring = detection.getboolean(Keys.detection.IGNORE_RECURRING)
        self.log_on_detection = detection.getboolean(Keys.detection.LOG_ON_DETECTION)
        
        logging = config_parser[Keys.logging.NAME]
        self.log_keystrokes = logging.getboolean(Keys.logging.LOG_KEYSTROKES)
        
        passphrase = config_parser[Keys.passphrase.NAME]
        self.passphrase_hash = passphrase.get(Keys.passphrase.HASH)
        self.passphrase_enabled = passphrase.getboolean(Keys.passphrase.ENABLE)
        self.auto_unlock_duration = passphrase.getint(Keys.passphrase.AUTO_UNLOCK_DURATION)
        self.auto_unlock_enabled = passphrase.getboolean(Keys.passphrase.AUTO_UNLOCK_ENABLE)
        
        suspect_hotkeys = config_parser[Keys.suspect_hotkeys.NAME]
        self.hotkey_blacklist = [
            i[1:-1] for i in 
            suspect_hotkeys[Keys.suspect_hotkeys.BLACKLIST][1:-1].replace(" ", "").split(",")
        ]
        
        self.log_keystrokes_override = False

instance: Config = None
