
def safe_int(value):
    try:
        return None if value == -99 else int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value):
    try:
        return float(value) if value else None
    except (ValueError, TypeError):
        return None

