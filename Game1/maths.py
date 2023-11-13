import constants
from time import perf_counter

# Математические функции

def clump(value, _min, _max):
    return max(_min, min(_max, value))

def default_delta() -> float:
    return 1/constants.FPS

def get_delta(start_: float) -> float:
    return 1/constants.FPS - (perf_counter() - start_)