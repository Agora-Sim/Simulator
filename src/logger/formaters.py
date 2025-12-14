# ================================================================
# 0. Section: Imports
# ================================================================
import logging



# ================================================================
# 1. Section: Formatters
# ================================================================
detail_format = logging.Formatter(
    "{separator}{asctime}: {levelname} [{module}.{funcName}] - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)


console_format = logging.Formatter(
    "{levelname} - {message}",
    style="{",
)