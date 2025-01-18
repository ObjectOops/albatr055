APP_TITLE = "ALBATR055"
INIT_FILE_PATH = "albatr055.ini"

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
        IGNORE_RECUR = "ignore_recur"
        LOG_ON_DETECTION = "log_on_detection"
    class logging:
        NAME = "logging"
        LOG_KEYSTROKES = "log_keystrokes"
    class passphrase:
        NAME = "passphrase"
        HASH = "hash"
        ENABLE = "enable"

INIT_DEFAULTS = {
    Keys.viewport.NAME: {
        Keys.viewport.WIDTH: 500,
        Keys.viewport.HEIGHT: 250,
        Keys.viewport.POS: [630, 220]
    },
    Keys.detection.NAME: {
        Keys.detection.ACTIVE: False,
        Keys.detection.LOCK_MOUSE_ON_DETECTION: True,
        Keys.detection.KEYS_PER_SECOND: 3.0,
        Keys.detection.SAMPLE_SIZE: 6,
        Keys.detection.LISTEN_HOTKEYS: True,
        Keys.detection.IGNORE_RECUR: False,
        Keys.detection.LOG_ON_DETECTION: True
    },
    Keys.logging.NAME: {
        Keys.logging.LOG_KEYSTROKES: False
    },
    Keys.passphrase.NAME: {
        Keys.passphrase.HASH: "",
        Keys.passphrase.ENABLE: False
    }
}
