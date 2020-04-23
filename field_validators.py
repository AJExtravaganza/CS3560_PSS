from datetime import datetime


def validate_nonempty_string(value: str):
    if not len(value) > 0:
        raise ValueError()


def validate_date_string(value: str):
    try:
        datetime.strptime(value, '%Y%m%d')
    except Exception:
        raise ValueError()


def validate_time_string(value: str):
    try:
        if not 0.0 <= float(value) <= 23.75:
            raise ValueError()
    except Exception:
        raise ValueError()


def validate_task_duration_string(value: str):
    try:
        if not 0 <= int(value) <= 3600:
            raise ValueError()
    except Exception:
        raise ValueError()
