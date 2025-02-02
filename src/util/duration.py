def to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return {"hour": hours, "min": minutes, "sec": seconds}

def from_hms(hms):
    return hms["hour"] * 3600 + hms["min"] * 60 + hms["sec"]
