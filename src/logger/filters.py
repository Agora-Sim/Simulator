# ================================================================
# 0. Section: Imports
# ================================================================
import logging



# ================================================================
# 1. Section: Filters
# ================================================================
class FunctionSeparatorFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.last_func = None

    def filter(self, record):
        if self.last_func is None:
            record.separator = ""
        elif record.funcName != self.last_func:
            record.separator = "\n"   # or "\n" + "-"*60 + "\n"
        else:
            record.separator = ""

        self.last_func = record.funcName
        return True
