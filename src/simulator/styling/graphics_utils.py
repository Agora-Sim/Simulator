# ================================================================
# 0. Section: Imports
# ================================================================
import numpy as np

from matplotlib.colors import LinearSegmentedColormap

from .graphic_classes import AlphaColor
from .color_converter import hex2rgb



# ================================================================
# 2. Section: Color Manager
# ================================================================
def pick_colors(color_map: LinearSegmentedColormap, N: int) -> np.ndarray:
    return color_map(np.linspace(0, 1, N))

def build_colormap_transparent2color(ending_color: str, starting_color: str = '#FFFFFF', n_bins: int = 2) -> LinearSegmentedColormap:
    hex_ending_color = ending_color
    hex_starting_color = starting_color

    rgb_ending_color = hex2rgb(hex_ending_color)
    rgb_starting_color = hex2rgb(hex_starting_color)
    rgb_starting_color = (rgb_starting_color[0], rgb_starting_color[1], rgb_starting_color[2], 0)

    colors = [rgb_starting_color, rgb_ending_color]
    personal_cmap = LinearSegmentedColormap.from_list('transparent_to_red', colors, N=n_bins)

    return personal_cmap

def tri_colormap(cmap_name: str, color_1: str, color_2: str, color_3: str, **kwargs) -> LinearSegmentedColormap:
    n_bins = kwargs.get('n_bins', 256)

    color_1 = hex2rgb(color_1)
    color_2 = hex2rgb(color_2)
    color_3 = hex2rgb(color_3)

    colors = [color_1, color_2, color_3]
    cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

    return cmap

def tri_alpha_colormap(color_1: AlphaColor, color_2: AlphaColor, color_3: AlphaColor, **kwargs) -> LinearSegmentedColormap:
    n_bins = kwargs.get('n_bins', 256)

    colors = [
        (color_1.r, color_1.g, color_1.b, color_1.a),
        (color_2.r, color_2.g, color_2.b, color_2.a),
        (color_3.r, color_3.g, color_3.b, color_3.a)
    ]
    cmap = LinearSegmentedColormap.from_list('tri_alpha_cmap', colors, N=n_bins)

    return cmap

def hex2rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))