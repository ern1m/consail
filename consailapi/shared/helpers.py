from datetime import time


def get_time_formatted(time_value: time) -> str:
    return time_value.strftime("%H:%M")
