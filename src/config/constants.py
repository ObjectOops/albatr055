import platform

APP_TITLE = "ALBATR055"
INIT_FILE_PATH = "albatr055.ini"
VALID_PASSPHRASE_CHARACTERS = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
PLATFORM_NAME = platform.system()

class Keys:
    class viewport:
        NAME = "viewport"
        WIDTH = "width"
        HEIGHT = "height"
        POS = "pos"
    class detection:
        NAME = "detection"
        ACTIVE = "active"
        LOCK_MOUSE_ON_DETECTION = "lock_mouse_on_detection"
        KEYS_PER_SECOND = "keys_per_second"
        SAMPLE_SIZE = "sample_size"
        LISTEN_HOTKEYS = "listen_hotkeys"
        IGNORE_RECURRING = "ignore_recurring"
        LOG_ON_DETECTION = "log_on_detection"
    class logging:
        NAME = "logging"
        LOG_KEYSTROKES = "log_keystrokes"
    class passphrase:
        NAME = "passphrase"
        HASH = "hash"
        ENABLE = "enable"
    class suspect_hotkeys:
        NAME = "suspect_hotkeys"
        BLACKLIST = "blacklist"

INIT_DEFAULTS = {
    Keys.viewport.NAME: {
        Keys.viewport.WIDTH: 1000,
        Keys.viewport.HEIGHT: 500,
        Keys.viewport.POS: [630, 220]
    },
    Keys.detection.NAME: {
        Keys.detection.ACTIVE: False,
        Keys.detection.LOCK_MOUSE_ON_DETECTION: True,
        Keys.detection.KEYS_PER_SECOND: 15.0,
        Keys.detection.SAMPLE_SIZE: 6,
        Keys.detection.LISTEN_HOTKEYS: True,
        Keys.detection.IGNORE_RECURRING: True,
        Keys.detection.LOG_ON_DETECTION: True
    },
    Keys.logging.NAME: {
        Keys.logging.LOG_KEYSTROKES: False
    },
    Keys.passphrase.NAME: {
        Keys.passphrase.HASH: "",
        Keys.passphrase.ENABLE: False
    },
    Keys.suspect_hotkeys.NAME: {
        Keys.suspect_hotkeys.BLACKLIST: [
            # Windows
            "<cmd>+r", # Run Dialog
            "<ctrl>+<shift>+<esc>", # Task Manager
            "<cmd>+x", # System Tools
            "<cmd>+e", # File Explorer
            "<cmd>+i", # Settings
            "<alt>+<f4>", # Close Window
            "<ctrl>+<shift>+<enter>" # Launch as Admin
        ]
    }
}
