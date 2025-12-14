# ================================================================
# 0. Section: Imports
# ================================================================
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import colormaps

from .graphics_utils import tri_colormap



# ================================================================
# 1. Section: Font Initialization
# ================================================================
fm.fontManager.addfont("src/styling/Bricolage_Grotesque/static/BricolageGrotesque-Light.ttf")
fm.fontManager.addfont("src/styling/Bricolage_Grotesque/static/BricolageGrotesque-Regular.ttf")
fm.fontManager.addfont("src/styling/Bricolage_Grotesque/static/BricolageGrotesque-Bold.ttf")

# Find the actual family name Matplotlib sees
for f in fm.fontManager.ttflist:
    if "Bricolage" in f.name:
        print(f.name, f.weight)   # run once to inspect



# ================================================================
# 2. Section: Colormaps
# ================================================================
rwy_trimap = tri_colormap('red_white_yellow', '#CB0D24', "#000000", '#E2C953')
colormaps.register(rwy_trimap, name="red_white_yellow")