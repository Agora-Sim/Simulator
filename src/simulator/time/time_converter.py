# ================================================================
# 0. Section: Imports
# ================================================================
from .SimTime import SimTime



# ================================================================
# 1. Section: Conversion Function
# ================================================================
def iterations_to_simtime(iterations: int) -> SimTime:
    if iterations < 0:
        raise ValueError("iterations must be non-negative")

    return SimTime(
        years=iterations // 12,
        months=iterations % 12
    )
