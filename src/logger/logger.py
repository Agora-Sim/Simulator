# ================================================================
# 0. Section: Imports
# ================================================================
import logging
import logging.handlers as handlers

from pathlib import Path

from .formaters import detail_format, console_format
from .levels import *
from .filters import FunctionSeparatorFilter


# ──────────────────────────────────────────────────────
# 0.1 Subsection: Universal Constants
# ──────────────────────────────────────────────────────
LOG_PATH = Path("../logs")
LOG_PATH.mkdir(exist_ok=True)



# ================================================================
# 1. Section: Logger
# ================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.DETAIL)
logger.propagate = False

# Add handlers if they are not already added
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)
    console_handler.setLevel("INFO")

    file_handler = handlers.TimedRotatingFileHandler(LOG_PATH / "package.log", when='midnight', encoding="utf-8")
    file_handler.setFormatter(detail_format)
    file_handler.setLevel(logging.DETAIL)
    file_handler.addFilter(FunctionSeparatorFilter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)