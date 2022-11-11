from datetime import datetime, time


def get_time_formatted(time_value: time | datetime) -> str:
    return time_value.strftime("%H:%M")
