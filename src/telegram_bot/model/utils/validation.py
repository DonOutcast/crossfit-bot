def check_float_value(coordinate: str) -> bool:
    try:
        float(coordinate)
        return True
    except (Exception,):
        return False


def check_length_value(max_size: int, user_size: str) -> bool:
    return len(user_size) <= max_size
