import configparser

import dearpygui.dearpygui as dpg

from config.constants import INIT_FILE_PATH, INIT_DEFAULTS, Keys

def load():
    config_parser = configparser.ConfigParser()
    config_parser.read_dict(INIT_DEFAULTS)
    config_parser.read(INIT_FILE_PATH)
    Config.instance = Config(config_parser)

def save():
    config_writer = Config.instance.config_parser
    config_writer[Keys.viewport.NAME] = {
        Keys.viewport.WIDTH: dpg.get_viewport_width(),
        Keys.viewport.HEIGHT: dpg.get_viewport_height(),
        Keys.viewport.POS: dpg.get_viewport_pos()
    }
    config_writer[Keys.detection.NAME] = {
        Keys.detection.ACTIVE: Config.instance.detect_active,
        Keys.detection.LOCK_MOUSE_ON_DETECTION: Config.instance.lock_mouse_on_detection,
        Keys.detection.KEYS_PER_SECOND: Config.instance.kps,
        Keys.detection.SAMPLE_SIZE: Config.instance.sample_size,
        Keys.detection.LISTEN_HOTKEYS: Config.instance.listen_hotkeys,
        Keys.detection.IGNORE_RECUR: Config.instance.ignore_recur,
        Keys.detection.LOG_ON_DETECTION: Config.instance.log_on_detection
    }
    config_writer[Keys.logging.NAME] = {
        Keys.logging.LOG_KEYSTROKES: Config.instance.log_keystrokes
    }
    config_writer[Keys.passphrase.NAME] = {
        Keys.passphrase.HASH: Config.instance.passphrase_hash,
        Keys.passphrase.ENABLE: Config.instance.passphrase_enabled
    }
    with open(INIT_FILE_PATH, "w") as config_file:
        config_writer.write(config_file)

class Config:
    instance = None
    
    def __init__(self, config_parser):
        self.config_parser = config_parser
        
        viewport = config_parser[Keys.viewport.NAME]
        self.viewport_width = viewport.getint(Keys.viewport.WIDTH)
        self.viewport_height = viewport.getint(Keys.viewport.HEIGHT)
        self.viewport_pos = [int(i) for i in viewport[Keys.viewport.POS][1:-1].split(", ")]
        
        detection = config_parser[Keys.detection.NAME]
        self.detect_active = detection.getboolean(Keys.detection.ACTIVE)
        self.lock_mouse_on_detection = detection.getboolean(Keys.detection.LOCK_MOUSE_ON_DETECTION)
        self.kps = detection.getfloat(Keys.detection.KEYS_PER_SECOND)
        self.sample_size = detection.getint(Keys.detection.SAMPLE_SIZE)
        self.listen_hotkeys = detection.getboolean(Keys.detection.LISTEN_HOTKEYS)
        self.ignore_recur = detection.getboolean(Keys.detection.IGNORE_RECUR)
        self.log_on_detection = detection.getboolean(Keys.detection.LOG_ON_DETECTION)
        
        logging = config_parser[Keys.logging.NAME]
        self.log_keystrokes = logging.getboolean(Keys.logging.LOG_KEYSTROKES)
        
        passphrase = config_parser[Keys.passphrase.NAME]
        self.passphrase_hash = passphrase.get(Keys.passphrase.HASH)
        self.passphrase_enabled = passphrase.get(Keys.passphrase.ENABLE)
