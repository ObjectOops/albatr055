import sys, os

def get_resource(rel_path):
    if is_bundled():
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

def is_bundled():
    return hasattr(sys, "_MEIPASS") and sys._MEIPASS is not None
