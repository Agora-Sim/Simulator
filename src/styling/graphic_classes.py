from dataclasses import dataclass

from .color_converter import hex2rgb

@dataclass
class AlphaColor():
    def __init__(self, hex_color: str, alpha: float = 1.0):
        self.r, self.g, self.b = hex2rgb(hex_color)
        self.a = alpha