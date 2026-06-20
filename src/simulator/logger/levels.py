# ================================================================
# 0. Section: Imports
# ================================================================
import logging



# ================================================================
# 1. Section: Detail Level
# ================================================================
DETAIL = 9

logging.addLevelName(DETAIL, "DETAIL")

def detail(self, msg, *args, **kwargs):
    if self.isEnabledFor(DETAIL):
        self._log(DETAIL, msg, args, stacklevel=2, **kwargs)

logging.Logger.detail = detail
logging.DETAIL = DETAIL