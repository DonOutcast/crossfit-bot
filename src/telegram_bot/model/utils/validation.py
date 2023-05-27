def check_float_value(coordinate: str) -> bool:
    try:
        float(coordinate)
        return True
    except (Exception,):
        return False
